#!/usr/bin/env python3
"""Create a copied (not symlinked) venv and an MCP payload; never edit global AI settings."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import venv


def main():
    parser = argparse.ArgumentParser(description="Przygotuj lokalny RAG po skopiowaniu nowego vaulta.")
    parser.add_argument("--vault", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--payload-only", action="store_true", help="Bez instalacji zależności.")
    args = parser.parse_args()
    vault = args.vault.expanduser().resolve()
    env = vault / ".venv"
    python = env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    try:
        if sys.version_info < (3, 11):
            raise ValueError("Wymagany Python 3.11+.")
        if not (vault / "_skrypty/requirements-rag.txt").is_file():
            raise ValueError("Brak szablonu RAG w wybranym vaulcie.")
        config = vault / "_config"
        config.mkdir(exist_ok=True)
        payload = {"mcpServers": {"rag-vault": {"command": str(python), "args": [str(vault / "_skrypty/aios-rag.py"), "--vault", str(vault), "mcp"]}}}
        output = config / "mcp-rag.json"
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if output.exists() and output.read_text(encoding="utf-8") != text:
            raise ValueError("mcp-rag.json ma własne zmiany. Pokaż diff i uzgodnij aktualizację przed wznowieniem.")
        if not output.exists():
            output.write_text(text, encoding="utf-8")
        if not args.payload_only:
            if not python.exists():
                if env.exists():
                    raise ValueError("Istnieje niepełny .venv. Sprawdź go przed ponowieniem, bez nadpisywania.")
                venv.EnvBuilder(with_pip=True, symlinks=False).create(env)
            version = subprocess.run([str(python), "-c", "import sys; assert sys.version_info >= (3,11)"], capture_output=True)
            if version.returncode:
                raise ValueError(".venv wymaga Python 3.11+.")
            subprocess.run([str(python), "-m", "pip", "install", "--disable-pip-version-check", "-r", str(vault / "_skrypty/requirements-rag.txt")],
                           check=True, stdout=sys.stderr, stderr=sys.stderr)
        print(json.dumps({"status": "files_ready" if args.payload_only else "environment_ready", "python": str(python), "mcp_payload": str(output),
                          "next": "Onboarding -> prywatność -> lokalny BGE-M3 -> index -> query."}, ensure_ascii=True))
        return 0
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "needs_setup", "error": str(exc)}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
