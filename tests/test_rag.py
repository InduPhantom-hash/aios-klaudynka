"""Public CLI/MCP integration tests; only the embedding HTTP service is a fixture."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "vault-template/_skrypty/aios-rag.py"


class Embeddings(BaseHTTPRequestHandler):
    mode = "ok"
    requests_seen = []

    def log_message(self, *args):
        pass

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        type(self).requests_seen.extend(body["input"])
        if self.mode == "error":
            self.send_error(503)
            return
        if self.mode == "timeout":
            time.sleep(0.3)
        data = []
        for i, text in enumerate(body["input"]):
            vector = [0.0] * (768 if self.mode == "wrong-dimension" else 1024)
            # Controlled semantic groups for deterministic plumbing tests, NOT a quality benchmark.
            lower = text.lower()
            if any(w in lower for w in ("rower", "bicycle", "cycling", "pedal", "bike")):
                vector[0] = 1.0
            elif any(w in lower for w in ("zupa", "soup", "cooking", "meal")):
                vector[1] = 1.0
            else:
                vector[2] = 1.0
            data.append({"index": i, "embedding": vector})
        payload = json.dumps({"data": list(reversed(data))}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        try:
            self.wfile.write(payload)
        except (BrokenPipeError, ConnectionResetError):
            pass


class RagTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Embeddings)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="klaudynka żółć ")
        self.addCleanup(self.tmp.cleanup)
        self.vault = Path(self.tmp.name)
        (self.vault / "_config").mkdir()
        self.config = {
            "endpoint": f"http://127.0.0.1:{self.server.server_port}/v1",
            "timeout": 2,
        }
        self.save_config()
        Embeddings.mode = "ok"
        Embeddings.requests_seen = []

    def save_config(self):
        (self.vault / "_config/rag.json").write_text(json.dumps(self.config), encoding="utf-8")

    def note(self, path, text):
        p = self.vault / path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        return p

    def cli(self, *args, ok=True):
        result = subprocess.run(
            [sys.executable, str(RUNNER), "--vault", str(self.vault), *args],
            cwd=self.tmp.name, capture_output=True, text=True, timeout=40,
            env={**os.environ, "PYTHONUTF8": "1"},
        )
        if ok:
            self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout)
        return json.loads(result.stdout)

    def test_index_and_semantic_query_return_source_with_unicode_path(self):
        self.note("Wiedza/Transport/Wiki/żółty rower.md", "---\ntyp_wiedzy: fakt\n---\n# Transport\n## Koła\nRower ułatwia dojazdy.\n")
        self.note("Wiedza/Kuchnia/Wiki/obiad.md", "# Jedzenie\nZupa pomidorowa.")
        indexed = self.cli("index")
        self.assertEqual(indexed["documents"], 2)
        hits = self.cli("query", "How can I start cycling?", "--k", "1")["hits"]
        self.assertEqual(hits[0]["path"], "Wiedza/Transport/Wiki/żółty rower.md")
        self.assertEqual(hits[0]["namespace"], "wiedza-transport")
        self.assertEqual(hits[0]["type"], "fakt")
        self.assertIn("Koła", hits[0]["heading"])
        self.assertIn("Rower", hits[0]["text"])
        self.assertTrue((self.vault / hits[0]["path"]).is_file())

    def test_incremental_add_edit_move_delete_and_no_duplicate_embeddings(self):
        note = self.note("Wiedza/AI/Wiki/start.md", "# Pierwszy\nRower na dojazdy.")
        self.cli("index")
        self.assertEqual(self.cli("index")["embedded"], 0)
        self.note("Wiedza/AI/Wiki/obiad.md", "# Obiad\nZupa na obiad.")
        self.assertEqual(self.cli("index")["embedded"], 1)
        note.write_text("# Zmieniony\nRower elektryczny.", encoding="utf-8")
        self.assertEqual(self.cli("status")["status"], "stale")
        self.assertEqual(self.cli("index")["embedded"], 1)
        moved = self.vault / "Wiedza/AI/Wiki/nowy.md"
        note.rename(moved)
        self.cli("index")
        hit = self.cli("query", "bicycle", "--k", "1")["hits"][0]
        self.assertEqual(hit["path"], "Wiedza/AI/Wiki/nowy.md")
        self.assertIn("elektryczny", hit["text"])
        moved.unlink()
        self.cli("index")
        hits = self.cli("query", "soup")["hits"]
        self.assertEqual([h["path"] for h in hits], ["Wiedza/AI/Wiki/obiad.md"])
        (self.vault / "Wiedza/AI/Wiki/obiad.md").unlink()
        self.assertEqual(self.cli("index")["chunks"], 0)
        self.assertEqual(self.cli("query", "meal")["hits"], [])

    def test_failed_update_keeps_previous_generation_and_refuses_stale_text(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        pointer = (self.vault / ".aios/rag/CURRENT").read_bytes()
        self.note("Wiedza/AI/Wiki/start.md", "# Zmieniony\nZupa na obiad.")
        Embeddings.mode = "error"
        self.cli("index", ok=False)
        self.assertEqual((self.vault / ".aios/rag/CURRENT").read_bytes(), pointer)
        Embeddings.mode = "ok"
        self.assertIn("nieaktualny", self.cli("query", "rower", ok=False)["error"])
        self.cli("index")
        self.assertIn("Zupa", self.cli("query", "meal")["hits"][0]["text"])

    def test_excludes_private_archives_secrets_transcripts_and_generated_files(self):
        self.note("Wiedza/AI/Wiki/public.md", "# Publiczny\nRower dostępny.")
        for path in ["Prywatne/notatka.md", "Projekty/Prywatne/X/README.md", "_brudnopis/sesja.md",
                     "X/_brudnopis/sesja.md", ".git/secret.md", "node_modules/n.md", "_Archiwum/n.md",
                     "Kosz/n.md", ".claude/worktrees/n.md", "secrets/hasla.md", "credentials.md"]:
            self.note(path, "# Nigdy nie wysyłaj\nSENSITIVE_SENTINEL")
        self.note("Wiedza/AI/Wiki/no-rag.md", "---\nrag: false\n---\nSENSITIVE_SENTINEL")
        self.note("Wiedza/AI/Wiki/private.md", "---\nprivate: true\n---\nSENSITIVE_SENTINEL")
        self.assertEqual(self.cli("index")["documents"], 1)
        self.assertFalse(any("SENSITIVE_SENTINEL" in text for text in Embeddings.requests_seen))

    def test_privacy_change_blocks_cached_results_until_reindex(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        self.config["private_paths"] = ["Wiedza/**"]
        self.save_config()
        self.assertEqual(self.cli("namespaces")["namespaces"], {})
        self.assertIn("nieaktualny", self.cli("query", "bicycle", ok=False)["error"])
        self.assertEqual(self.cli("index")["documents"], 0)

    def test_metadata_privacy_hides_project_namespace_without_reindex(self):
        path = self.note("Projekty/Nauka/PoufnyProjekt/README.md", "# Projekt\nRower na dojazdy.")
        self.cli("index")
        self.assertEqual(self.cli("namespaces")["namespaces"], {"projekty-poufnyprojekt": 1})
        path.write_text("---\nprivate: true\n---\n# Projekt\nRower na dojazdy.", encoding="utf-8")
        self.assertEqual(self.cli("namespaces")["namespaces"], {})

    def test_metadata_filters_treat_quotes_as_data_and_map_project_namespace(self):
        self.note("Projekty/Nauka/Żółta Łódź/README.md", "---\ntitle: Decyzja\ntype: \"Owner's decision\"\n---\n# Transport\nRower na dojazdy.")
        self.note("Wiedza/Kuchnia/Wiki/obiad.md", "# Obiad\nZupa na obiad.")
        self.cli("index")
        hits = self.cli("query", "bicycle", "--namespace", "projekty-zolta-lodz", "--type", "Owner's decision")["hits"]
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["type"], "Owner's decision")
        self.assertEqual(self.cli("query", "meal", "--namespace", "x' OR 1=1 --")["hits"], [])

    def test_wrong_dimension_and_timeout_do_not_publish_an_index(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        for mode in ["wrong-dimension", "timeout"]:
            Embeddings.mode = mode
            self.config["timeout"] = 0.05
            self.save_config()
            result = self.cli("index", ok=False)
            self.assertEqual(result["status"], "error")
            self.assertFalse((self.vault / ".aios/rag/CURRENT").exists())

    def test_local_only_configuration_rejects_remote_endpoint_before_sending_text(self):
        self.config["endpoint"] = "https://example.com/v1"
        self.save_config()
        self.assertIn("lokalnego", self.cli("index", ok=False)["error"])
        self.assertEqual(Embeddings.requests_seen, [])

    def test_empty_index_and_diagnostics_do_not_require_an_embedder(self):
        Embeddings.mode = "error"
        self.assertEqual(self.cli("status")["status"], "not_indexed")
        self.assertEqual(self.cli("namespaces")["status"], "not_indexed")
        self.assertEqual(self.cli("index")["documents"], 0)
        self.assertEqual(self.cli("query", "cokolwiek")["hits"], [])
        self.assertEqual(self.cli("namespaces")["namespaces"], {})

    def test_markdown_code_fences_tables_and_legacy_metadata(self):
        table = "| Kolumna | Wartość |\n|---|---|\n" + "| Rower | dane |\n" * 200
        self.note("Wiedza/AI/Wiki/kod.md", "---\ntitle: Poradnik\ntype: Notatka Wiki\n---\n# Prawdziwy\n```python\n# To jest komentarz\nrower = 1\n```\n\n" + table)
        self.cli("index")
        hits = self.cli("query", "cycling", "--k", "10")["hits"]
        self.assertFalse(any("komentarz" in h["heading"] for h in hits))
        self.assertTrue(any(table.strip() in h["text"] for h in hits))
        self.assertTrue(any("```python\n# To jest komentarz\nrower = 1\n```" in h["text"] for h in hits))

    def test_invalid_yaml_fails_without_replacing_last_good_index(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        pointer = (self.vault / ".aios/rag/CURRENT").read_bytes()
        self.note("Wiedza/AI/Wiki/broken.md", "---\ntematy: [niedomknięte\n---\nTreść")
        self.cli("index", ok=False)
        self.assertEqual((self.vault / ".aios/rag/CURRENT").read_bytes(), pointer)

    def test_query_limits_and_exclusive_writer_lock(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        self.cli("query", "", ok=False)
        self.cli("query", "x", "--k", "0", ok=False)
        self.cli("query", "x", "--k", "51", ok=False)
        (self.vault / ".aios/rag/write.lock").write_text("busy")
        self.assertIn("zajęty", self.cli("index", ok=False)["error"])

    def test_cache_cleanup_preserves_foreign_directories(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        foreign = self.note(".aios/rag/generations/manual-backup/notes.md", "Nie usuwaj")
        self.cli("index")
        self.assertEqual(foreign.read_text(encoding="utf-8"), "Nie usuwaj")

    def test_corrupted_store_is_reported_and_rebuild_recovers(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        store = self.vault / ".aios/rag"
        generation = (store / "CURRENT").read_text().strip()
        db = store / "generations" / generation / "db"
        db.rename(db.with_name("broken-db"))
        self.assertIn("rebuild", self.cli("status", ok=False)["error"])
        self.assertIn("rebuild", self.cli("query", "cycling", ok=False)["error"])
        self.cli("rebuild")
        self.assertEqual(len(self.cli("query", "cycling")["hits"]), 1)

    def test_invalid_configuration_types_return_actionable_json_errors(self):
        for key, value in [("store", None), ("store", []), ("endpoint", 1), ("endpoint", "http://127.0.0.1:bad/v1"), ("endpoint", "http://[bad/v1")]:
            original = dict(self.config)
            self.config[key] = value
            self.save_config()
            self.assertEqual(self.cli("index", ok=False)["status"], "error")
            self.config = original

    def test_long_plain_paragraphs_are_chunked_without_losing_tail(self):
        self.note("Wiedza/AI/Wiki/dlugi.md", "# Rower\n" + "Długi akapit opisuje jazdę. " * 300 + "KOŃCOWY_ZNACZNIK")
        self.assertGreater(self.cli("index")["chunks"], 1)
        hits = self.cli("query", "cycling", "--k", "50")["hits"]
        self.assertTrue(all(len(h["text"]) <= 1800 for h in hits))
        self.assertTrue(any("KOŃCOWY_ZNACZNIK" in h["text"] for h in hits))

    def test_mcp_exposes_read_only_tools_and_returns_cli_equivalent_sources(self):
        self.note("Wiedza/AI/Wiki/start.md", "# Start\nRower na dojazdy.")
        self.cli("index")
        import asyncio
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        async def exercise():
            # A slow child prints its own stacks before the client deadline (not just the waiting client).
            probe = ("import faulthandler,runpy,sys; from pathlib import Path; "
                     "faulthandler.dump_traceback_later(20); script=sys.argv.pop(1); "
                     "sys.path.insert(0,str(Path(script).parent)); runpy.run_path(script,run_name='__main__')")
            params = StdioServerParameters(command=sys.executable, args=["-c", probe, str(RUNNER), "--vault", str(self.vault), "mcp"])
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    self.assertEqual({tool.name for tool in tools.tools}, {"rag_search", "rag_namespaces"})
                    result = await session.call_tool("rag_search", {"query": "cycling", "k": 1})
                    self.assertFalse(result.isError, str(result))
                    payload = result.structuredContent or json.loads(result.content[0].text)
                    self.assertEqual(payload["hits"][0]["path"], "Wiedza/AI/Wiki/start.md")
                    ns = await session.call_tool("rag_namespaces", {})
                    ns_payload = ns.structuredContent or json.loads(ns.content[0].text)
                    self.assertEqual(ns_payload["namespaces"], {"wiedza-ai": 1})
                    # Privacy changes apply without restarting an already connected MCP server.
                    self.config["private_paths"] = ["Wiedza/**"]
                    self.save_config()
                    hidden = await session.call_tool("rag_search", {"query": "cycling"})
                    self.assertTrue(hidden.isError)
                    self.assertFalse(any("Rower na dojazdy" in c.text for c in hidden.content if c.type == "text"))
        asyncio.run(asyncio.wait_for(exercise(), timeout=60))


if __name__ == "__main__":
    unittest.main()
