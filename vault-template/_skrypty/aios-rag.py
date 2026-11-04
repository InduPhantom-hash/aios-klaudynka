#!/usr/bin/env python3
"""Portable CLI entry point. Invoke with the vault's Python virtual environment."""
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from aios_rag.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
