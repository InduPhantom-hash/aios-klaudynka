#!/usr/bin/env python3
"""run_all_tests.py – Zestaw testów jednostkowych i integracyjnych dla aios_backpass."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path
import sys

# Dodajemy katalog silnika do ścieżki
sys.path.insert(0, str(Path(__file__).parent.parent))

from scanner import parse_duration_to_seconds, is_path_related, scan_all_sessions, SessionMeta
from distiller import redact_secrets, truncate_snippet, distill_antigravity_transcript, distill_claude_transcript
from ledger import GapLedger, GapRecord, EvidenceQuote
from budget import estimate_tokens, analyze_file_budget, verify_zero_sum_edit
from evaluator import validate_and_apply_gradient_step, build_evaluation_prompt, SingleEvaluation, ProposedEdit


class TestScanner(unittest.TestCase):
    def test_duration_parsing(self):
        self.assertEqual(parse_duration_to_seconds("1d"), 86400.0)
        self.assertEqual(parse_duration_to_seconds("7d"), 7 * 86400.0)
        self.assertEqual(parse_duration_to_seconds("1h"), 3600.0)
        self.assertEqual(parse_duration_to_seconds("30m"), 1800.0)
        self.assertEqual(parse_duration_to_seconds("2w"), 14 * 86400.0)

    def test_path_relation(self):
        target = Path(tempfile.gettempdir()) / "example-vault"
        sub = str(target / "Projekty" / "Przyklad")
        unrelated = str(target.parent / "other-directory")
        self.assertTrue(is_path_related(sub, target))
        self.assertFalse(is_path_related(unrelated, target))


class TestDistiller(unittest.TestCase):
    def test_redact_secrets(self):
        raw = "Klucz to sk-proj-1234567890abcdef1234567890 oraz ghp_1234567890abcdef12345678901234."
        redacted = redact_secrets(raw)
        self.assertNotIn("sk-proj-1234567890", redacted)
        self.assertNotIn("ghp_1234567890", redacted)
        self.assertIn("[REDACTED_API_KEY]", redacted)
        self.assertIn("[REDACTED_GITHUB_TOKEN]", redacted)

    def test_truncate_snippet(self):
        long_t = "A" * 500
        short_t = truncate_snippet(long_t, max_chars=50)
        self.assertEqual(len(short_t), 53)  # 50 + "..."


class TestLedger(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.ledger_file = self.temp_dir / "test-ledger.json"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_gap_graduation_rule_2_sessions(self):
        ledger = GapLedger(self.ledger_file)
        # 1. Pierwsza sesja -> status unconfirmed
        rec1 = ledger.record_evidence(
            title="Agent odpala npm test zamiast pnpm",
            category="rule_violation",
            affected_section="Narzędzia i dane",
            session_id="session-001",
            harness="antigravity",
            quote="npm test failed",
            min_sessions=2,
        )
        self.assertEqual(rec1.status, "unconfirmed")
        self.assertEqual(rec1.sessions_count, 1)

        # 2. Ta sama sesja ponownie -> brak awansu
        rec2 = ledger.record_evidence(
            title="Agent odpala npm test zamiast pnpm",
            category="rule_violation",
            affected_section="Narzędzia i dane",
            session_id="session-001",
            harness="antigravity",
            quote="npm test again",
            min_sessions=2,
        )
        self.assertEqual(rec2.sessions_count, 1)
        self.assertEqual(rec2.status, "unconfirmed")

        # 3. Druga, niezależna sesja -> awans do statusu 'graduated'
        rec3 = ledger.record_evidence(
            title="Agent odpala npm test zamiast pnpm",
            category="rule_violation",
            affected_section="Narzędzia i dane",
            session_id="session-002",
            harness="claude",
            quote="running npm test instead of pnpm",
            min_sessions=2,
        )
        self.assertEqual(rec3.sessions_count, 2)
        self.assertEqual(rec3.status, "graduated")

        # Sprawdzenie zapisu i ponownego odczytu
        ledger.save()
        new_ledger = GapLedger(self.ledger_file)
        self.assertEqual(len(new_ledger.get_graduated_gaps()), 1)


class TestBudget(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.test_file = self.temp_dir / "TEST_AGENTS.md"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_budget_analysis_and_zero_sum(self):
        sample_md = """# Główne Zasady

## Sekcja 1
Zasada pierwsza działania agenta w projekcie.

## Sekcja 2
Zasada druga dotycząca testów i uprawnień.
"""
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write(sample_md)

        rep = analyze_file_budget(self.test_file, token_budget=100)
        self.assertFalse(rep.is_over_budget)
        self.assertEqual(len(rep.sections), 3)

        # Sprawdzenie zero-sum
        ok, delta, msg = verify_zero_sum_edit(sample_md, sample_md + "\n" + ("Nowe reguły. " * 100), token_budget=100)
        self.assertFalse(ok)
        self.assertIn("BŁĄD BUDŻETU", msg)


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.agents_file = self.temp_dir / "AGENTS.md"
        self.ledger_file = self.temp_dir / "gap-ledger.json"

        with open(self.agents_file, "w", encoding="utf-8") as f:
            f.write("# AGENTS.md\n\n## Narzędzia i dane\n- Zawsze używaj pnpm zamiast npm.\n")

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_gradient_step_validation(self):
        ledger = GapLedger(self.ledger_file)
        from distiller import DistilledSession
        mock_sess = [
            DistilledSession(
                session_id="sess-A",
                harness="antigravity",
                file_path="mock.jsonl",
                created_at="2026-08-20T10:00:00Z",
                original_size_bytes=1000,
                distilled_size_bytes=100,
                compression_ratio=0.1,
                turns=[{"role": "assistant", "text": "wykonuję polecenie npm test"}],
                compact_text="[ASSISTANT]: wykonuję polecenie npm test",
            ),
            DistilledSession(
                session_id="sess-B",
                harness="claude",
                file_path="mock2.jsonl",
                created_at="2026-08-21T10:00:00Z",
                original_size_bytes=1000,
                distilled_size_bytes=100,
                compression_ratio=0.1,
                turns=[{"role": "assistant", "text": "wykonuję polecenie npm test"}],
                compact_text="[ASSISTANT]: wykonuję polecenie npm test",
            ),
        ]

        mock_llm_json = json.dumps({
            "evaluations": [
                {
                    "category": "rule_violation",
                    "title": "Użycie npm zamiast pnpm",
                    "affected_section": "Narzędzia i dane",
                    "session_id": "sess-A",
                    "quote": "wykonuję polecenie npm test",
                    "explanation": "Agent zignorował regułę o pnpm",
                }
            ],
            "proposed_gradient_edits": [
                {
                    "edit_type": "modify",
                    "target_file": "AGENTS.md",
                    "section": "Narzędzia i dane",
                    "justification": "Poparte przez sess-A i sess-B",
                    "evidence_sessions": ["sess-A", "sess-B"],
                    "old_text": "- Zawsze używaj pnpm zamiast npm.",
                    "new_text": "- KRYTYCZNE: Zawsze używaj pnpm. Wywołanie npm jest surowo zabronione.",
                }
            ]
        })

        res = validate_and_apply_gradient_step(
            mock_llm_json,
            self.agents_file,
            mock_sess,
            ledger,
            token_budget=500,
            min_sessions_per_gap=2,
        )

        self.assertEqual(len(res.evaluations), 1)
        self.assertEqual(len(res.proposed_edits), 1)
        self.assertTrue(res.proposed_edits[0].is_valid)
        self.assertTrue(res.budget_passed)


if __name__ == "__main__":
    unittest.main()
