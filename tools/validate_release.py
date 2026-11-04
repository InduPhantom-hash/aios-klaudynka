"""Read-only release checks: manifests, skill metadata, links, portable distribution."""
from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    yaml = None

ROOT = Path(__file__).resolve().parents[1]

EXPECTED_SKILLS = {
    "aios-anonimizacja",
    "aios-backpass",
    "aios-data-analysis",
    "aios-debata",
    "aios-doctor",
    "aios-dzien",
    "aios-grilling",
    "aios-init",
    "aios-koniec-sesji",
    "aios-kontynuuj",
    "aios-kustosz",
    "aios-research-faktow",
    "aios-research-rynkowy",
    "aios-sortuj",
    "aios-stworz-projekt",
    "aios-szukaj",
    "aios-weryfikacja",
    "aios-wyjasnij",
}

EXPECTED = {
    "aios": EXPECTED_SKILLS,
}

WRITERS = {
    "aios-init",
    "aios-backpass",
    "aios-sortuj",
    "aios-stworz-projekt",
    "aios-koniec-sesji",
}


def _parse_frontmatter(text: str) -> dict:
    if not (text.startswith("---") and "---" in text[3:]):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    if yaml is not None:
        try:
            loaded = yaml.safe_load(parts[1])
            if isinstance(loaded, dict):
                return loaded
        except Exception:
            pass
    # Resilient fallback parser when PyYAML is not installed
    metadata = {}
    for line in parts[1].splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            metadata[key.strip()] = val.strip().strip('"').strip("'")
    return metadata


def main():
    failures = []
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    if market["metadata"]["version"] != "0.8.0":
        failures.append("Wersja marketplace różni się od kontraktu 0.8.0.")
    count = 0
    for name, expected in EXPECTED.items():
        plugin = ROOT / "plugins" / name
        manifest = json.loads((plugin / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        version = "0.8.0"
        published = next(p for p in market["plugins"] if p["name"] == name)
        if manifest["version"] != version or published["version"] != version:
            failures.append(f"Niespójna wersja pluginu {name}.")
        skills = {p.parent.name: p for p in (plugin / "skills").glob("*/SKILL.md")}
        if set(skills) != expected:
            failures.append(f"Lista skilli {name} różni się od kontraktu.")
        count += len(skills)
        for skill, path in skills.items():
            text = path.read_text(encoding="utf-8")
            metadata = _parse_frontmatter(text)
            if metadata.get("name") != skill or not metadata.get("description"):
                failures.append(f"Nieprawidłowy frontmatter skilla {skill}.")
            if skill in WRITERS and "_skille/rag.md" not in text:
                failures.append(f"Brak wspólnej procedury indeksowania: {skill}.")

    if count != len(EXPECTED_SKILLS):
        failures.append(f"Całkowita liczba skilli ({count}) różni się od wymaganej {len(EXPECTED_SKILLS)}.")

    required_yaml = [
        ROOT / "zadania.md",
        ROOT / "docs/rag.md",
        ROOT / "docs/zgodnosc-skilli.md",
        ROOT / "docs/odbior-0.7.0.md",
        ROOT / "docs/publikacja-0.7.0.md",
        ROOT / "vault-template/_skille/rag.md",
    ]
    for path in required_yaml:
        if not path.exists():
            failures.append(f"Brak dokumentu {path.relative_to(ROOT)}.")
            continue
        text = path.read_text(encoding="utf-8")
        metadata = _parse_frontmatter(text)
        if not all(k in metadata for k in ("typ_wiedzy", "tematy", "podmioty", "ai_summary")):
            failures.append(f"Niepełny YAML: {path.relative_to(ROOT)}.")

    # Check real Markdown links, ignoring code examples and external URLs.
    for path in [ROOT / "README.md", ROOT / "INSTALL.md", *ROOT.glob("docs/*.md"), *ROOT.glob("vault-template/*.md")]:
        body = re.sub(r"```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
        for url in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", body):
            url = unquote(url.strip("<> ").split("#")[0])
            if not url or re.match(r"[a-z]+:", url):
                continue
            if not (path.parent / url).exists():
                failures.append(f"Niedziałający link w {path.relative_to(ROOT)}: {url}")

    private = re.compile(r"/Users/phantom|/Volumes/Karta|Documents/_hub")
    for directory in (ROOT / "vault-template", ROOT / "plugins"):
        for path in directory.rglob("*"):
            if path.is_file() and path.suffix in (".md", ".py", ".json", ".txt"):
                if private.search(path.read_text(encoding="utf-8")):
                    failures.append(f"Prywatna ścieżka autora: {path.relative_to(ROOT)}")

    if failures:
        print("\n".join(failures))
        return 1

    print(json.dumps({
        "status": "passed",
        "skills": count,
        "version": "0.8.0",
        "checks": [
            "manifests",
            "skill-frontmatter",
            "indexing-procedures",
            "document-yaml",
            "local-links",
            "portable-paths",
        ],
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
