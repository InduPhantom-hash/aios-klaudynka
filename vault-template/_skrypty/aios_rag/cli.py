from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from .engine import Config, Rag, RagError


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lokalny RAG Klaudynki. Wyniki CLI: JSON; MCP: stdio.")
    parser.add_argument("--vault", type=Path, default=Path(__file__).resolve().parents[2])
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("index", "rebuild", "status", "namespaces", "mcp"):
        commands.add_parser(name)
    query = commands.add_parser("query")
    query.add_argument("query")
    query.add_argument("--namespace")
    query.add_argument("--type", dest="type_filter")
    query.add_argument("--k", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        config = Config.load(args.vault)
        rag = Rag(config)
        if args.command == "mcp":
            from .server import serve
            serve(config)
            return 0
        if args.command in ("index", "rebuild"):
            result = rag.index(rebuild=args.command == "rebuild")
        elif args.command == "query":
            result = rag.query(args.query, args.namespace, args.type_filter, args.k)
        else:
            result = getattr(rag, args.command)()
        print(json.dumps(result, ensure_ascii=True))
        return 0
    except Exception as exc:
        message = str(exc) if isinstance(exc, RagError) else "Błąd lokalnego indeksu lub zależności. Sprawdź instalację i uprawnienia; dla uszkodzonego indeksu wykonaj rebuild."
        print(json.dumps({"status": "error", "error": message}, ensure_ascii=True))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
