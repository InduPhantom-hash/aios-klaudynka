"""Opt-in real BGE-M3 smoke test over synthetic Markdown in a freshly copied vault."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(os.environ.get("AIOS_LIVE_RAG") == "1", "Wymaga świadomego AIOS_LIVE_RAG=1 i lokalnego BGE-M3.")
class LiveRagTest(unittest.TestCase):
    def test_fresh_vault_real_pl_en_retrieval_and_changed_note(self):
        with tempfile.TemporaryDirectory(prefix="żywy RAG ") as tmp:
            vault = Path(tmp) / "Mój vault"
            subprocess.run([sys.executable, str(ROOT / "install.py"), "--vault", str(vault), "--with-meta", "--no-env"], check=True, capture_output=True)
            notes = {
                "Wiedza/Transport/Wiki/dojazdy.md": "---\ntyp_wiedzy: fakt\ntematy: [transport]\npodmioty: []\nai_summary: Dojazdy na rowerze.\n---\n# Dojazdy\nRower pozwala codziennie dotrzeć do biura, ćwiczyć i omijać korki. Trzeba sprawdzić hamulce, opony i trasę przez park.",
                "Wiedza/Kuchnia/Wiki/pomidorowa.md": "# Obiad\nZupa pomidorowa powstaje z pomidorów i bulionu. Gotuj ją przez dwadzieścia minut, dopraw bazylią i podaj z ryżem.",
                "Wiedza/Programowanie/Wiki/testy.md": "# Testy oprogramowania\nTesty jednostkowe sprawdzają funkcje w izolacji. Testy integracyjne badają współpracę komponentów systemu.",
            }
            for rel, body in notes.items():
                p = vault / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(body, encoding="utf-8")

            def cli(*args):
                result = subprocess.run([sys.executable, str(vault / "_skrypty/aios-rag.py"), "--vault", str(vault), *args], capture_output=True, text=True, timeout=180)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                return json.loads(result.stdout)

            cli("index")
            for query, expected in [
                ("Jak mogę dojeżdżać do pracy bez auta, pedałując?", "Wiedza/Transport/Wiki/dojazdy.md"),
                ("What should I simmer and serve with rice for lunch?", "Wiedza/Kuchnia/Wiki/pomidorowa.md"),
                ("How do I verify that different software components work together?", "Wiedza/Programowanie/Wiki/testy.md"),
            ]:
                hit = cli("query", query, "--k", "1")["hits"][0]
                self.assertEqual(hit["path"], expected)
                self.assertTrue((vault / hit["path"]).exists())
            path = vault / "Wiedza/Transport/Wiki/dojazdy.md"
            path.write_text(notes["Wiedza/Transport/Wiki/dojazdy.md"] + "\nAktualizacja: stacja naprawcza stoi obok mostu.\n", encoding="utf-8")
            self.assertEqual(cli("index")["embedded"], 1)
            self.assertIn("obok mostu", cli("query", "Gdzie jest stacja do naprawy roweru?", "--k", "1")["hits"][0]["text"])
            import asyncio
            from mcp import ClientSession, StdioServerParameters
            from mcp.client.stdio import stdio_client

            async def mcp_query():
                params = StdioServerParameters(command=sys.executable, args=[str(vault / "_skrypty/aios-rag.py"), "--vault", str(vault), "mcp"])
                async with stdio_client(params) as (read, write):
                    async with ClientSession(read, write) as session:
                        await session.initialize()
                        result = await session.call_tool("rag_search", {"query": "What can I cook for lunch?", "k": 1})
                        self.assertFalse(result.isError)
                        payload = result.structuredContent or json.loads(result.content[0].text)
                        self.assertEqual(payload["hits"][0]["path"], "Wiedza/Kuchnia/Wiki/pomidorowa.md")
            asyncio.run(mcp_query())


if __name__ == "__main__":
    unittest.main()
