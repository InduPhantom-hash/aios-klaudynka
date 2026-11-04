#!/usr/bin/env python3
"""Install only into a NEW directory. No client configuration or existing vault is overwritten."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main(argv=None):
    parser = argparse.ArgumentParser(description="Nowa instalacja AIOS-Klaudynki 0.8.0")
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--with-meta", action="store_true", help="Zachowane dla kompatybilności wstecznej; w v0.8.0 wszystkie skille trafiają do wtyczki aios.")
    parser.add_argument("--no-env", action="store_true", help="Tylko pliki, bez pip/modelu; jawny status files_ready.")
    args = parser.parse_args(argv)
    if sys.version_info < (3, 11):
        print(json.dumps({"status": "error", "error": "Wymagany Python 3.11+."}))
        return 1
    root = Path(__file__).resolve().parent
    target = args.vault.expanduser().absolute()
    try:
        if target.exists() or target.is_symlink():
            raise ValueError("Katalog docelowy istnieje. Wybierz nowy katalog; migracja i nadpisywanie nie należą do tego wydania.")
        sources = [root / "vault-template", root / "plugins/aios", root / "docs"]
        for source in sources:
            if not source.is_dir() or any(p.is_symlink() for p in source.rglob("*")):
                raise ValueError("Niepełne źródło instalacji albo symlink. Pobierz pełne repozytorium.")
        target.mkdir(parents=True, exist_ok=False)
        # Cache and author data never travel to the user's vault. Profile is produced by init.
        ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".venv", ".aios", "me.md")
        shutil.copytree(root / "vault-template", target, dirs_exist_ok=True, ignore=ignore)
        shutil.copytree(root / "plugins/aios", target / "_skille/aios", ignore=ignore)
        shutil.copytree(root / "docs", target / "_skille/dokumentacja", ignore=ignore)
        setup = target / "_skrypty/setup-rag.py"
        command = [sys.executable, str(setup), "--vault", str(target)]
        if args.no_env:
            command.append("--payload-only")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=sys.stderr, text=True,
                                encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})
        if result.returncode:
            try:
                setup_result = json.loads(result.stdout)
            except ValueError:
                setup_result = {"status": "needs_setup", "error": "Proces konfiguracji zakończony błędem; szczegóły na stderr."}
            print(json.dumps({"status": "needs_setup", "vault": str(target), "error": "Pliki skopiowane; przygotowanie środowiska nie powiodło się.",
                              "setup": setup_result,
                              "resume": [sys.executable, str(setup), "--vault", str(target)]}, ensure_ascii=True))
            return 1
        print(json.dumps({"status": "files_ready" if args.no_env else "needs_onboarding", "vault": str(target),
                          "next": "Uruchom /aios:init --quick lub przeczytaj _skille/aios/skills/aios-init/SKILL.md. Model i pierwszy indeks skonfiguruj po ustaleniu prywatności."}, ensure_ascii=True))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
