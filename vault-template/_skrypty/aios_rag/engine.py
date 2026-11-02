"""Markdown -> local embeddings -> immutable LanceDB generations + atomic pointer."""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from fnmatch import fnmatchcase
import gc
import hashlib
import ipaddress
import json
import math
import os
from pathlib import Path
import re
import shutil
import unicodedata
from urllib.parse import quote, urlparse
import uuid

DIM = 1024
SCHEMA = 1
SKIP_DIRS = {"node_modules", "__pycache__", "venv", "cache", "caches", "dist", "build",
             "target", "kosz", "_archiwum", "_archive", "_archiwum", "_brudnopis",
             "worktrees", "_worktrees", "_config", "_skrypty", "_skille", "secrets", "credentials", "_sekrety"}
SECRET_NAMES = {"secrets.md", "credentials.md", "hasla.md", "hasła.md", "api-keys.md"}
PRIVATE = ["Prywatne/**", "Projekty/Prywatne/**"]


class RagError(RuntimeError):
    """An actionable user-facing error; CLI renders it as JSON, never a secret dump."""


@dataclass
class Config:
    vault: Path
    store: Path
    endpoint: str
    model: str
    timeout: float
    excludes: list[str]
    private_paths: list[str]

    @classmethod
    def load(cls, vault: Path) -> "Config":
        vault = vault.expanduser().resolve()
        if not vault.is_dir():
            raise RagError("Vault nie istnieje.")
        path = vault / "_config/rag.json"
        try:
            raw = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        except (OSError, ValueError) as exc:
            raise RagError("Nieprawidłowy _config/rag.json.") from exc
        if not isinstance(raw, dict) or raw.get("schema", SCHEMA) != SCHEMA:
            raise RagError("Nieobsługiwany format konfiguracji RAG.")
        endpoint = raw.get("endpoint", "http://127.0.0.1:1234/v1")
        if not isinstance(endpoint, str):
            raise RagError("endpoint musi być lokalnym adresem HTTP.")
        try:
            parsed = urlparse(endpoint)
            parsed.port
        except ValueError as exc:
            raise RagError("Nieprawidłowy URL lub port endpointu.") from exc
        host = parsed.hostname or ""
        try:
            loopback = host == "localhost" or ipaddress.ip_address(host).is_loopback
        except ValueError:
            loopback = host == "localhost"
        if parsed.scheme != "http" or not loopback or parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise RagError("Embeddingi wymagają lokalnego endpointu HTTP (localhost/loopback), bez danych logowania.")
        model = raw.get("model", "text-embedding-bge-m3")
        if not isinstance(model, str) or "bge-m3" not in model.lower():
            raise RagError("To wydanie wymaga modelu BGE-M3 (1024 wymiary).")
        timeout = raw.get("timeout", 60)
        if not isinstance(timeout, (int, float)) or not math.isfinite(timeout) or not 0 < timeout <= 180:
            raise RagError("timeout musi mieścić się w zakresie (0, 180] sekund.")
        for key in ("exclude", "private_paths"):
            value = raw.get(key, [])
            if not isinstance(value, list) or any(not isinstance(v, str) or not v or "\\" in v for v in value):
                raise RagError(f"{key}: podaj listę wzorców z separatorami /.")
        store_value = raw.get("store", ".aios/rag")
        if not isinstance(store_value, str) or not store_value.strip():
            raise RagError("store musi być niepustą ścieżką katalogu indeksu.")
        store = Path(store_value).expanduser()
        store = (store if store.is_absolute() else vault / store).resolve()
        if store == vault or store in vault.parents:
            raise RagError("Indeks musi mieć własny podkatalog, poza korzeniem vaulta.")
        return cls(vault, store, endpoint.rstrip("/"), model, float(timeout), raw.get("exclude", []), raw.get("private_paths", PRIVATE))

    def allowed(self, path: Path) -> bool:
        try:
            rel = path.relative_to(self.vault)
        except ValueError:
            return False
        if path.is_symlink() or path.name.casefold() in SECRET_NAMES or any(p.startswith(".") or p.casefold() in SKIP_DIRS for p in rel.parts):
            return False
        if path == self.store or self.store in path.parents:
            return False
        posix = rel.as_posix().casefold()
        if any(fnmatchcase(posix, p.casefold()) or posix == p.rstrip("/**").casefold()
               for p in self.excludes + self.private_paths):
            return False
        return True


def slug(text: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", text.replace("ł", "l").replace("Ł", "L")).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-") or "inne"


def namespace(path: Path) -> str:
    parts = path.parts
    if parts[0] == "Wiedza" and len(parts) >= 2:
        return "wiedza-" + slug(parts[1])
    if parts[0] == "Projekty" and len(parts) >= 3:
        return "projekty-" + slug(parts[2])
    if parts[0] == "_pamiec":
        return "pamiec"
    return "fundament" if len(parts) == 1 else slug(parts[0])


def chunks(path: str, text: str) -> list[dict]:
    import yaml
    meta = {}
    if text.startswith("---\n") or text.startswith("---\r\n"):
        match = re.match(r"^---\s*\n(.*?)\n---\s*(?:\n|$)", text, re.S)
        if not match:
            raise RagError(f"Niedomknięty frontmatter: {path}")
        try:
            meta = yaml.safe_load(match[1]) or {}
        except yaml.YAMLError as exc:
            raise RagError(f"Nieprawidłowy YAML: {path}") from exc
        if not isinstance(meta, dict):
            raise RagError(f"Frontmatter musi być mapą: {path}")
        text = text[match.end():]
    if meta.get("rag") is False or meta.get("private") is True or meta.get("prywatne") is True:
        return []
    title = str(meta.get("title") or meta.get("tytul") or Path(path).stem)
    kind = str(meta.get("typ_wiedzy") or meta.get("type") or ("Projekt" if "projekt" in meta else "Notatka"))
    stack, sections, lines = [], [], []
    fenced = False
    fence_char = ""
    fence_len = 0
    for line in text.splitlines():
        fence = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if fence:
            char = fence[1][0]
            if not fenced:
                fenced, fence_char, fence_len = True, char, len(fence[1])
            elif char == fence_char and len(fence[1]) >= fence_len:
                fenced = False
        head = re.match(r"^(#{1,6})\s+(.+?)\s*#*\s*$", line) if not fenced and not fence else None
        if head:
            if lines:
                sections.append((" > ".join([title] + [v for _, v in stack]), "\n".join(lines).strip()))
                lines = []
            level = len(head[1])
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, head[2]))
        else:
            lines.append(line)
    if lines:
        sections.append((" > ".join([title] + [v for _, v in stack]), "\n".join(lines).strip()))
    result = []
    for heading, body in sections:
        # Paragraph windows. Keep fenced blocks and tables intact, even above target size.
        blocks, block, fenced = [], [], False
        for line in body.splitlines():
            if re.match(r"^\s{0,3}(`{3,}|~{3,})", line):
                fenced = not fenced
            if not line.strip() and not fenced:
                if block:
                    blocks.append("\n".join(block))
                    block = []
            else:
                block.append(line)
        if block:
            blocks.append("\n".join(block))
        bounded = []
        for block in blocks:
            if "```" in block or "~~~" in block or any(line.lstrip().startswith("|") for line in block.splitlines()):
                bounded.append(block)
                continue
            while len(block) > 1800:
                end = block.rfind(" ", 0, 1800)
                if end < 900:
                    end = 1800
                bounded.append(block[:end])
                block = block[end:].lstrip()
            if block:
                bounded.append(block)
        blocks = bounded
        window = ""
        for block in blocks:
            if window and len(window) + len(block) > 1800:
                result.append({"heading": heading, "text": window})
                window = ""
            window = (window + "\n\n" + block).strip()
        if window:
            result.append({"heading": heading, "text": window})
    for i, row in enumerate(result):
        row.update(id=hashlib.sha256(f"{path}:{i}".encode()).hexdigest(), path=path,
                   source_path="vault://" + quote(path, safe="/"), title=title, type=kind,
                   namespace=namespace(Path(path)))
    return result


def embed(config: Config, texts: list[str]) -> list[list[float]]:
    import requests
    try:
        # Ignore HTTP_PROXY and redirects: source text must stay on the configured loopback endpoint.
        with requests.Session() as session:
            session.trust_env = False
            response = session.post(config.endpoint + "/embeddings", json={"model": config.model, "input": texts},
                                    timeout=(min(5, config.timeout), config.timeout), allow_redirects=False)
            if response.status_code != 200:
                raise RagError(f"Lokalny embedder zwrócił HTTP {response.status_code}. Sprawdź LM Studio i BGE-M3.")
            data = response.json()["data"]
        if len(data) != len(texts) or sorted(d["index"] for d in data) != list(range(len(texts))):
            raise ValueError("batch")
        vectors = [d["embedding"] for d in sorted(data, key=lambda d: d["index"])]
        for vector in vectors:
            if len(vector) != DIM or any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in vector):
                raise RagError("Nieprawidłowy embedding: wymagane 1024 skończone liczby w każdym wektorze.")
            if not any(vector):
                raise RagError("Embedder zwrócił zerowy wektor.")
        return vectors
    except requests.RequestException as exc:
        raise RagError("Lokalny embedder niedostępny lub timeout. Uruchom LM Studio, załaduj BGE-M3 i ponów.") from exc
    except (KeyError, ValueError, TypeError) as exc:
        raise RagError("Nieprawidłowa odpowiedź lokalnego embeddera.") from exc


@contextmanager
def lock(config: Config):
    config.store.mkdir(parents=True, exist_ok=True)
    path = config.store / "write.lock"
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise RagError("Indeks zajęty. Ponów po zakończeniu poprzedniej operacji; po awarii sprawdź write.lock.") from exc
    try:
        os.write(fd, str(os.getpid()).encode())
        os.close(fd)
        yield
    finally:
        path.unlink(missing_ok=True)


class Rag:
    """Public application API shared by CLI and MCP; all outputs are JSON-compatible."""
    def __init__(self, config: Config):
        self.config = config

    def snapshot(self):
        pointer = self.config.store / "CURRENT"
        if not pointer.exists():
            return None, None
        try:
            name = pointer.read_text(encoding="ascii").strip()
            if not re.fullmatch(r"[0-9a-f]{32}", name):
                raise ValueError("generation")
            folder = self.config.store / "generations" / name
            manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
            if manifest["schema"] != SCHEMA or manifest["model"] != self.config.model or manifest["dim"] != DIM or manifest["vault"] != str(self.config.vault):
                raise RagError("Konfiguracja indeksu zmieniła się. Wykonaj rebuild dla tego vaulta i modelu.")
            table = self.table(folder)
            if table.count_rows() != manifest["chunks"]:
                raise RagError("Uszkodzony indeks RAG. Wykonaj rebuild.")
            del table
            return folder, manifest
        except (OSError, ValueError, KeyError) as exc:
            raise RagError("Uszkodzony indeks RAG. Wykonaj rebuild.") from exc

    def table(self, folder):
        import lancedb
        if not (folder / "db").is_dir():
            raise RagError("Brak bazy indeksu. Wykonaj rebuild.")
        try:
            return lancedb.connect(str(folder / "db")).open_table("vault")
        except Exception as exc:
            raise RagError("Nie można odczytać bazy indeksu. Wykonaj rebuild.") from exc

    def documents(self):
        docs = {}
        for base, dirs, files in os.walk(self.config.vault, followlinks=False):
            dirs[:] = sorted(d for d in dirs if self.config.allowed(Path(base) / d))
            for name in sorted(files):
                path = Path(base) / name
                if path.suffix.lower() != ".md" or not self.config.allowed(path):
                    continue
                rel = path.relative_to(self.config.vault).as_posix()
                text = path.read_text(encoding="utf-8-sig")
                rows = chunks(rel, text)
                if rows:
                    docs[rel] = (hashlib.sha256(text.encode()).hexdigest(), rows)
        return docs

    def index(self, rebuild=False):
        import lancedb
        import pyarrow as pa
        with lock(self.config):
            old_folder, old = (None, None) if rebuild else self.snapshot()
            docs = self.documents()
            hashes = {p: value[0] for p, value in docs.items()}
            if old and old["hashes"] == hashes:
                return {"status": "unchanged", "documents": len(docs), "chunks": old["chunks"], "embedded": 0}
            retained = []
            if old_folder:
                db = lancedb.connect(str(old_folder / "db"))
                table = db.open_table("vault")
                retained = [r for r in table.to_arrow().to_pylist() if r["path"] in hashes and old["hashes"].get(r["path"]) == hashes[r["path"]]]
                del table, db
            changed = [row for path, (_, rows) in docs.items() if not old or old["hashes"].get(path) != hashes[path] for row in rows]
            for start in range(0, len(changed), 16):
                batch = changed[start:start + 16]
                vectors = embed(self.config, [r["heading"] + "\n\n" + r["text"] for r in batch])
                for row, vector in zip(batch, vectors):
                    row["vector"] = vector
            rows = retained + changed
            generation = uuid.uuid4().hex
            folder = self.config.store / "generations" / generation
            folder.mkdir(parents=True)
            committed = False
            pointer_tmp = self.config.store / (generation + ".tmp")
            try:
                schema = pa.schema([(k, pa.string()) for k in ("id", "path", "source_path", "title", "type", "namespace", "heading", "text")] + [("vector", pa.list_(pa.float32(), DIM))])
                db = lancedb.connect(str(folder / "db"))
                table = db.create_table("vault", data=pa.Table.from_pylist(rows, schema=schema))
                del table, db
                manifest = {"schema": SCHEMA, "model": self.config.model, "dim": DIM, "vault": str(self.config.vault), "hashes": hashes, "chunks": len(rows)}
                (folder / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
                with pointer_tmp.open("w", encoding="ascii") as stream:
                    stream.write(generation)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(pointer_tmp, self.config.store / "CURRENT")
                committed = True
                # Readers also hold the lock. Keep the previous committed generation for recovery.
                gc.collect()
                for previous in folder.parent.iterdir():
                    if previous.is_dir() and not previous.is_symlink() and re.fullmatch(r"[0-9a-f]{32}", previous.name) and previous not in (folder, old_folder):
                        try:
                            owned = json.loads((previous / "manifest.json").read_text(encoding="utf-8"))
                            if owned.get("vault") == str(self.config.vault) and owned.get("schema") == SCHEMA:
                                shutil.rmtree(previous, ignore_errors=True)
                        except (OSError, ValueError, AttributeError):
                            pass
            finally:
                pointer_tmp.unlink(missing_ok=True)
                if not committed:
                    shutil.rmtree(folder, ignore_errors=True)
            return {"status": "ready", "documents": len(docs), "chunks": len(rows), "embedded": len(changed)}

    def status(self):
        if not (self.config.store / "CURRENT").exists():
            return {"status": "not_indexed", "documents": 0, "chunks": 0}
        with lock(self.config):
            _, manifest = self.snapshot()
            current = {p: value[0] for p, value in self.documents().items()}
            return {"status": "ready" if current == manifest["hashes"] else "stale", "documents": len(manifest["hashes"]), "chunks": manifest["chunks"], "model": self.config.model}

    def namespaces(self):
        import lancedb
        from collections import Counter
        if not (self.config.store / "CURRENT").exists():
            return {"status": "not_indexed", "namespaces": {}}
        with lock(self.config):
            folder, _ = self.snapshot()
            db = lancedb.connect(str(folder / "db"))
            table = db.open_table("vault")
            allowed_documents = set(self.documents())
            counts = Counter(r["namespace"] for r in table.to_arrow().select(["namespace", "path"]).to_pylist()
                             if r["path"] in allowed_documents and self.visible(r["path"]))
            return {"status": "ready", "namespaces": dict(sorted(counts.items()))}

    def visible(self, rel: str):
        path = self.config.vault / rel
        if not self.config.allowed(path) or not path.is_file():
            return False
        # An ancestor becoming a symlink must never expose a different source.
        return path.resolve().is_relative_to(self.config.vault) and not any(p.is_symlink() for p in path.parents if p != self.config.vault)

    def query(self, query: str, namespace_filter=None, type_filter=None, k=5):
        import lancedb
        if not isinstance(query, str) or not query.strip() or len(query) > 16000:
            raise RagError("Zapytanie musi zawierać 1-16000 znaków.")
        if not isinstance(k, int) or isinstance(k, bool) or not 1 <= k <= 50:
            raise RagError("k musi mieścić się w zakresie 1-50.")
        for value in (namespace_filter, type_filter):
            if value is not None and (not isinstance(value, str) or len(value) > 200):
                raise RagError("Filtr musi być tekstem do 200 znaków.")
        with lock(self.config):
            folder, manifest = self.snapshot()
            if not folder:
                raise RagError("Brak indeksu. Wykonaj index.")
            # Refuse stale retrieval: old private/deleted/edited text must not reach an agent.
            hashes = {p: value[0] for p, value in self.documents().items()}
            if hashes != manifest["hashes"]:
                raise RagError("Indeks nieaktualny. Wykonaj index; użyj odczytu plików do tego czasu.")
            if not manifest["chunks"]:
                return {"status": "ready", "hits": []}
            vector = embed(self.config, [query])[0]
            db = lancedb.connect(str(folder / "db"))
            table = db.open_table("vault")
            filters = []
            for key, value in (("namespace", namespace_filter), ("type", type_filter)):
                if value is not None:
                    filters.append(key + " = '" + value.replace("'", "''") + "'")
            search = table.search(vector).distance_type("cosine")
            if filters:
                search = search.where(" AND ".join(filters), prefilter=True)
            hits = []
            for row in search.limit(k).to_list():
                if self.visible(row["path"]):
                    hits.append({key: value for key, value in row.items() if key not in ("vector", "_distance", "id")}
                                | {"score": round(1 - float(row["_distance"]), 4)})
            return {"status": "ready", "hits": hits}
