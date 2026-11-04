#!/usr/bin/env python3
"""Szybki linter Markdown dla bazy wiedzy AIOS (Kustosz).

Wykrywa ślepe linki, sieroty, puste pliki, braki w nagłówkach YAML oraz niepoprawne formaty dat.
Zgodny ze wzorcem CLI Script i zasadą File Output by Default z Google DeepMind.
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

YAML_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
CODE_BLOCK_PATTERN = re.compile(r"```[\s\S]*?```|`[^`\n]+`")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]\|#]+)(?:#[^\]\|]+)?(?:\|[^\]]+)?\]\]")
MDLINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)#]+)(?:#[^)]+)?\)")

DEFAULT_EXCLUDES = {
    ".git", ".next", "node_modules", "_Archiwum", "Kosz",
    ".gemini", ".claude", "_brudnopis", ".Trash"
}
REQUIRED_YAML_FIELDS = ["typ_wiedzy", "tematy", "podmioty", "ai_summary"]
DATE_FIELDS = ["data", "date", "created", "updated", "utworzono", "zmodyfikowano"]
DATE_REGEX = re.compile(r"^['\"]?(\d{4}-\d{2}-\d{2}(?:[T\s]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?)['\"]?$")



def parse_args():
    parser = argparse.ArgumentParser(description="Linter Markdown AIOS (Kustosz)")
    parser.add_argument("--target", required=True, help="Ścieżka do skanowanego katalogu")
    parser.add_argument("--output", required=True, help="Ścieżka do wyjściowego pliku JSON z raportem")
    parser.add_argument("--check-yaml", action="store_true", default=True, help="Weryfikuj zgodność YAML frontmatter")
    parser.add_argument("--check-dates", action="store_true", default=True, help="Weryfikuj format dat ISO-8601 w YAML")
    return parser.parse_args()


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in DEFAULT_EXCLUDES or part.startswith("."):
            return True
    return False


def resolve_link(target_raw: str, current_file: Path, target_dir: Path, vault_root: Path, all_files: dict) -> Path | None:
    clean = target_raw.strip().replace(".md", "")
    if not clean or re.search(r"email[\s\xa0]+protected", clean, re.I):
        return None

    # 1. Ścieżka względna do bieżącego pliku
    rel_local = current_file.parent / clean
    if rel_local.is_dir() or rel_local.with_suffix(".md").exists():
        return rel_local if rel_local.is_dir() else rel_local.with_suffix(".md")

    # 2. Ścieżka względna do skanowanego katalogu (np. Wiedza/)
    rel_target = (target_dir / clean).with_suffix(".md")
    if rel_target.exists():
        return rel_target

    # 3. Ścieżka względna do całego Vaulta (np. Projekty/...)
    rel_vault = (vault_root / clean).with_suffix(".md")
    if rel_vault.exists():
        return rel_vault

    # 4. Bezpośredni lookup po nazwie pliku / stem w bazie
    target_name = Path(clean).name.lower()
    if target_name in all_files:
        return all_files[target_name][0]

    return None


def main():
    start_time = time.monotonic()
    args = parse_args()
    target_dir = Path(args.target).resolve()
    vault_root = target_dir.parent if target_dir.name in ["Wiedza", "Projekty", "_szablony"] else target_dir

    if not target_dir.exists() or not target_dir.is_dir():
        print(f"Błąd: Katalog {target_dir} nie istnieje.", file=sys.stderr)
        sys.exit(1)

    all_files = {}  # stem/name -> list of Path
    md_paths = []

    for root, _, files in os.walk(target_dir):
        root_path = Path(root)
        if should_skip(root_path):
            continue
        for file in files:
            if file.endswith(".md"):
                file_path = root_path / file
                md_paths.append(file_path)
                stem = file_path.stem.lower()
                all_files.setdefault(stem, []).append(file_path)
                all_files.setdefault(file_path.name.lower(), []).append(file_path)

    # Indeksujemy także pozostałe pliki vaulta, aby poprawnie rozwiązywać linki zewnętrzne
    if vault_root != target_dir:
        for root, _, files in os.walk(vault_root):
            root_path = Path(root)
            if any(part in {".git", ".next", "node_modules", "_Archiwum", "Kosz", ".Trash"} for part in root_path.parts):
                continue
            for file in files:
                if file.endswith(".md"):
                    file_path = root_path / file
                    stem = file_path.stem.lower()
                    all_files.setdefault(stem, []).append(file_path)
                    all_files.setdefault(file_path.name.lower(), []).append(file_path)

    incoming_links = {p: 0 for p in md_paths}
    dead_links = []
    orphans = []
    empty_notes = []
    missing_yaml = []
    invalid_dates = []

    for path in md_paths:
        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        size = len(content.strip())
        if size < 50:
            empty_notes.append({"path": str(path), "size_bytes": size})

        yaml_match = YAML_PATTERN.match(content)
        if args.check_yaml:
            if not yaml_match:
                missing_yaml.append({"path": str(path), "missing": REQUIRED_YAML_FIELDS})
            else:
                yaml_text = yaml_match.group(1)
                missing_fields = [f for f in REQUIRED_YAML_FIELDS if not re.search(rf"^{f}:", yaml_text, re.MULTILINE)]
                if missing_fields:
                    missing_yaml.append({"path": str(path), "missing": missing_fields})

        if args.check_dates and yaml_match:
            yaml_text = yaml_match.group(1)
            for d_field in DATE_FIELDS:
                m = re.search(rf"^{d_field}:\s*(.+)$", yaml_text, re.MULTILINE)
                if m:
                    raw_val = m.group(1).strip()
                    if "#" in raw_val:
                        raw_val = raw_val.split("#")[0].strip()
                    if raw_val and not DATE_REGEX.match(raw_val):
                        invalid_dates.append({
                            "path": str(path),
                            "field": d_field,
                            "value": raw_val,
                            "expected": "YYYY-MM-DD"
                        })

        # Usuń bloki kodu przed szukaniem linków (chroni przed bash [[ ... ]])
        text_no_code = CODE_BLOCK_PATTERN.sub("", content)

        # Ekstrakcja linków wikilink
        raw_links = WIKILINK_PATTERN.findall(text_no_code)

        # Ekstrakcja markdown links (omijając linki zewnętrzne, maile, anchory oraz czyste web-ścieżki bez .md)
        for _, dest in MDLINK_PATTERN.findall(text_no_code):
            if dest.startswith("http") or dest.startswith("#") or dest.startswith("mailto:"):
                continue
            if dest.startswith("/") and not dest.endswith(".md"):
                continue
            raw_links.append(dest)

        for target in raw_links:
            clean_target = target.strip()
            if not clean_target or re.search(r"email[\s\xa0]+protected", clean_target, re.I):
                continue
            resolved = resolve_link(clean_target, path, target_dir, vault_root, all_files)
            if resolved:
                if resolved in incoming_links:
                    incoming_links[resolved] += 1
            else:
                dead_links.append({"source": str(path), "target": clean_target})

    for path, count in incoming_links.items():
        if count == 0 and not path.name.lower().startswith("index") and not path.name.lower().startswith("readme"):
            orphans.append(str(path))

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target_directory": str(target_dir),
        "total_scanned": len(md_paths),
        "execution_time_seconds": round(time.monotonic() - start_time, 3),
        "summary": {
            "dead_links_count": len(dead_links),
            "orphans_count": len(orphans),
            "empty_notes_count": len(empty_notes),
            "missing_yaml_count": len(missing_yaml),
            "invalid_dates_count": len(invalid_dates)
        },
        "details": {
            "dead_links": dead_links[:100],
            "orphans": orphans[:100],
            "empty_notes": empty_notes[:50],
            "missing_yaml": missing_yaml[:100],
            "invalid_dates": invalid_dates[:100]
        }
    }

    out_path = Path(args.output).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"Lint ukończony w {report['execution_time_seconds']}s. "
        f"Przeskanowano: {len(md_paths)} plików. "
        f"Ślepe linki: {len(dead_links)}, Sieroty: {len(orphans)}, Puste: {len(empty_notes)}, "
        f"Braki YAML: {len(missing_yaml)}, Błędne daty: {len(invalid_dates)}. "
        f"Raport: {out_path}"
    )


if __name__ == "__main__":
    main()
