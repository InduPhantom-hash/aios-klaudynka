"""Fresh installation seam. Never install dependencies into the test interpreter."""
import json
import os
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="instalacja żółć ")
        self.addCleanup(self.tmp.cleanup)
        self.target = Path(self.tmp.name) / "Mój vault"

    def install(self, *args):
        return subprocess.run([sys.executable, str(ROOT / "install.py"), "--vault", str(self.target), "--no-env", *args],
                              capture_output=True, text=True, timeout=20)

    def test_fresh_install_copies_skills_and_prepares_portable_mcp_payload(self):
        result = self.install("--with-meta")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(json.loads(result.stdout)["status"], "files_ready")
        self.assertEqual(len(list((self.target / "_skille/aios/skills").glob("*/SKILL.md"))), 14)
        self.assertEqual(len(list((self.target / "_skille/aios-meta/skills").glob("*/SKILL.md"))), 4)
        self.assertTrue((self.target / "_skrypty/aios-rag.py").is_file())
        self.assertTrue((self.target / "_skille/dokumentacja/szablony/me-template.md").is_file())
        payload = json.loads((self.target / "_config/mcp-rag.json").read_text(encoding="utf-8"))
        server = payload["mcpServers"]["rag-vault"]
        self.assertTrue(Path(server["command"]).is_absolute())
        self.assertEqual(server["args"][-1], "mcp")
        self.assertIn(str(self.target.resolve()), server["args"])
        self.assertFalse((self.target / "me.md").exists())

    def test_existing_vault_is_refused_without_overwrite(self):
        self.target.mkdir()
        note = self.target / "me.md"
        note.write_text("Mój profil", encoding="utf-8")
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("istnieje", json.loads(result.stdout)["error"])
        self.assertEqual(note.read_text(encoding="utf-8"), "Mój profil")
        self.assertEqual(list(self.target.iterdir()), [note])

    def test_json_output_survives_non_unicode_console_encoding(self):
        result = subprocess.run([sys.executable, str(ROOT / "install.py"), "--vault", str(self.target), "--no-env"],
                                env={**os.environ, "PYTHONIOENCODING": "ascii"}, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(Path(json.loads(result.stdout)["vault"]).resolve(), self.target.resolve())

    def test_failed_dependency_setup_reports_diagnostics_and_preserves_files(self):
        source = Path(self.tmp.name) / "fixture-source"
        source.mkdir()
        shutil.copy2(ROOT / "install.py", source / "install.py")
        for name in ("plugins", "docs", "vault-template"):
            shutil.copytree(ROOT / name, source / name, ignore=shutil.ignore_patterns("__pycache__", ".venv", ".aios"))
        (source / "vault-template/_skrypty/requirements-rag.txt").write_text("klaudynka-missing-test-package==0\n", encoding="utf-8")
        result = subprocess.run([sys.executable, str(source / "install.py"), "--vault", str(self.target)],
                                env={**os.environ, "PIP_NO_INDEX": "1", "PYTHONIOENCODING": "ascii"},
                                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("No matching distribution", result.stderr)
        self.assertEqual(json.loads(result.stdout)["setup"]["status"], "needs_setup")
        self.assertTrue((self.target / "_skrypty/aios-rag.py").exists())


if __name__ == "__main__":
    unittest.main()
