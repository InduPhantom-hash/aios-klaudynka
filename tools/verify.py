"""Run acceptance checks and save local evidence. --live uses only local synthetic fixtures."""
from __future__ import annotations

import argparse
from importlib.metadata import version
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / ".aios/review/verification.json")
    args = parser.parse_args()
    environment = {**os.environ, "PYTHONUTF8": "1"}
    environment.pop("AIOS_LIVE_RAG", None)
    commands = [
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        [sys.executable, "vault-template/_skrypty/aios_backpass/tests/run_all_tests.py"],
        [sys.executable, "tools/validate_release.py"],
        ["git", "diff", "--check"],
    ]
    if args.live:
        commands.append([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_live_rag.py", "-v"])
    results = []
    for i, command in enumerate(commands):
        env = dict(environment)
        if args.live and i == len(commands) - 1:
            env["AIOS_LIVE_RAG"] = "1"
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        results.append({"command": command, "exit_code": result.returncode, "stdout": result.stdout, "stderr": result.stderr})
        print(json.dumps({"check": command[1:], "exit_code": result.returncode}))
    payload = {"system": platform.platform(), "python": platform.python_version(), "packages": {p: version(p) for p in ("lancedb", "mcp", "requests", "PyYAML")},
               "live_requested": args.live, "results": results}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return int(any(r["exit_code"] for r in results))


if __name__ == "__main__":
    raise SystemExit(main())
