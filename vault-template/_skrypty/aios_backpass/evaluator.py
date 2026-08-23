#!/usr/bin/env python3
"""evaluator.py – Model-Agnostic Evaluator & Gradient Proposal Engine (File Over AI).

Generuje pakiety ewaluacyjne dla dowolnego AI (Claude, Gemini, GPT, LM Studio, Ollama),
waliduje otrzymane odpowiedzi (wymóg cytatów, próg 2 sesji, limit 5 edycji)
oraz generuje ustrukturyzowane raporty i propozycje diffów.
"""

import json
import os
import re
import urllib.error
import urllib.request
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from budget import analyze_file_budget, estimate_tokens, verify_zero_sum_edit
from distiller import DistilledSession
from ledger import GapLedger, GapRecord


@dataclass
class SingleEvaluation:
    category: str  # rule_violation | missing_rule | stale_rule | unneeded_discovery | positive_reinforcement
    title: str
    affected_section: str
    session_id: str
    quote: str
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProposedEdit:
    edit_type: str  # add | modify | delete | extract_to_skill
    target_file: str
    section: str
    justification: str
    evidence_sessions: List[str]
    old_text: str
    new_text: str
    skill_name: Optional[str] = None
    is_valid: bool = True
    validation_error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GradientStepResult:
    evaluated_sessions_count: int
    evaluations: List[SingleEvaluation]
    proposed_edits: List[ProposedEdit]
    token_delta: int
    new_estimated_tokens: int
    budget_passed: bool
    status_summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "evaluated_sessions_count": self.evaluated_sessions_count,
            "evaluations": [e.to_dict() for e in self.evaluations],
            "proposed_edits": [p.to_dict() for p in self.proposed_edits],
            "token_delta": self.token_delta,
            "new_estimated_tokens": self.new_estimated_tokens,
            "budget_passed": self.budget_passed,
            "status_summary": self.status_summary,
        }


EVALUATION_SYSTEM_PROMPT = """Jesteś rygorystycznym audytorem i optymalizatorem instrukcji dla agentów AI w systemie AIOS.
Twoim celem jest wykonanie kroku 'Gradient Descent' dla pliku instrukcji (np. AGENTS.md) na podstawie zdestylowanych transkryptów prawdziwych sesji.

ZASADY DYSCYPLINY (GRADIENT DESCENT):
1. DOWODY WYŁĄCZNIE Z TRANSKRYPTÓW: Każdy zarzut, błąd lub luka MUSI zawierać dokładny, dosłowny cytat (quote) z transkryptu sesji. Wnioski bez cytatu zostaną automatycznie odrzucone.
2. PRÓG 2 SESJI DLA NOWYCH REGUŁ: Nowa reguła lub zmiana może być zaproponowana TYLKO wtedy, gdy problem wystąpił w co najmniej dwóch różnych sesjach LUB gdy luka jest już w rejestrze (gap-ledger) z poprzednich sesji.
3. MAŁE KROKI (MAX 5 EDYCJI): Zaproponuj maksymalnie 5 małych, precyzyjnych edycji (add, modify, delete, extract_to_skill). Zakaz przepisywania całego pliku od nowa!
4. SZTYWNY BUDŻET TOKENÓW (ZERO-SUM): Plik instrukcji nie może puchnąć. Jeśli dodajesz nową regułę, wskaż co usunąć, skrócić lub przenieść do skilla.
5. SKILL RELEASE VALVE: Rzadkie procedury (< 20% sesji) lub obszerne szablony powinny być wydzielone do osobnych skilli (extract_to_skill), a nie zaśmiecać AGENTS.md.

Zwróć wynik WYŁĄCZNIE jako poprawny format JSON wg poniższego schematu (bez zbędnego tekstu):
{
  "evaluations": [
    {
      "category": "rule_violation" | "missing_rule" | "stale_rule" | "unneeded_discovery" | "positive_reinforcement",
      "title": "Krótki tytuł usterki",
      "affected_section": "Nazwa sekcji w pliku instrukcji",
      "session_id": "ID sesji z której pochodzi dowód",
      "quote": "Dokładny cytat z transkryptu",
      "explanation": "Dlaczego to stanowi stratę/błąd"
    }
  ],
  "proposed_gradient_edits": [
    {
      "edit_type": "add" | "modify" | "delete" | "extract_to_skill",
      "target_file": "AGENTS.md",
      "section": "Nazwa sekcji",
      "justification": "Uzasadnienie z numerami sesji (minimum 2 sesje)",
      "evidence_sessions": ["sess-1", "sess-2"],
      "old_text": "Dokładny istniejący fragment do zastąpienia/usunięcia (lub pusty dla 'add')",
      "new_text": "Nowy fragment (lub pusty dla 'delete')",
      "skill_name": "opcjonalna nazwa skilla jeśli extract_to_skill"
    }
  ]
}
"""


def build_evaluation_prompt(
    target_file_path: Path,
    distilled_sessions: List[DistilledSession],
    ledger: Optional[GapLedger] = None,
    token_budget: int = 2000
) -> str:
    """Tworzy kompletny pakiet promptu (Prompt Packet) do wykonania kroku ewaluacji."""
    instructions_text = ""
    if target_file_path.exists():
        with open(target_file_path, "r", encoding="utf-8", errors="ignore") as f:
            instructions_text = f.read()

    b_report = analyze_file_budget(target_file_path, token_budget=token_budget)

    # Przygotowanie informacji z Gap Ledgera
    ledger_summary = []
    if ledger and ledger.gaps:
        ledger_summary.append("--- AKTYWNY REJESTR LUK (GAP LEDGER) ---")
        for g in ledger.gaps.values():
            ledger_summary.append(
                f"- [{g.status.upper()}] ID: {g.gap_id} | Kat: {g.category} | Sesje: {g.sessions_count} | Tytuł: {g.title}"
            )

    sessions_payload = []
    for s in distilled_sessions:
        sessions_payload.append(s.compact_text)

    prompt = f"""# AIOS BACKPASS: ZLECENIE EWALUACJI I KROKU GRADIENTOWEGO

{EVALUATION_SYSTEM_PROMPT}

==================================================
1. AKTUALNY PLIK INSTRUKCJI ({target_file_path.name})
Budżet: {b_report.total_est_tokens} / {b_report.token_budget} tokenów ({b_report.budget_usage_pct:.1f}%)
==================================================
{instructions_text}

==================================================
2. STAN REJESTRU LUK (GAP LEDGER)
==================================================
{chr(10).join(ledger_summary) if ledger_summary else "Rejestr pusty (brak wcześniej zindeksowanych luk)."}

==================================================
3. ZDESTYLOWANE PRÓBKI SESJI ({len(distilled_sessions)} sesji)
==================================================
{chr(10).join(sessions_payload)}

==================================================
Zwróć poprawny obiekt JSON z polami 'evaluations' oraz 'proposed_gradient_edits'.
"""
    return prompt


def validate_and_apply_gradient_step(
    raw_response_json: str,
    target_file_path: Path,
    distilled_sessions: List[DistilledSession],
    ledger: GapLedger,
    token_budget: int = 2000,
    max_edits: int = 5,
    min_sessions_per_gap: int = 2
) -> GradientStepResult:
    """Deterministycznie waliduje propozycję LLM i aktualizuje Gap Ledger."""
    # Ekstrakcja JSON jeśli model dodał znaczniki markdown
    clean_json = raw_response_json.strip()
    if "```json" in clean_json:
        m = re.search(r"```json\s*(.*?)\s*```", clean_json, re.DOTALL)
        if m:
            clean_json = m.group(1).strip()
    elif "```" in clean_json:
        m = re.search(r"```\s*(.*?)\s*```", clean_json, re.DOTALL)
        if m:
            clean_json = m.group(1).strip()

    try:
        data = json.loads(clean_json)
    except Exception as e:
        return GradientStepResult(
            evaluated_sessions_count=len(distilled_sessions),
            evaluations=[],
            proposed_edits=[],
            token_delta=0,
            new_estimated_tokens=0,
            budget_passed=False,
            status_summary=f"BŁĄD PARSOWANIA JSON: {e}",
        )

    # 1. Parsowanie ewaluacji i aktualizacja ledgera
    eval_objs: List[SingleEvaluation] = []
    session_corpus = {s.session_id: s.compact_text for s in distilled_sessions}

    for ev in data.get("evaluations", []):
        quote = ev.get("quote", "").strip()
        sess_id = ev.get("session_id", "")
        
        # Mechaniczne odrzucenie jeśli brak cytatu lub cytat zmyślony
        if not quote or len(quote) < 8:
            continue
        
        # Sprawdzamy czy cytat faktycznie istnieje w podanej sesji
        if sess_id in session_corpus:
            corpus_text = session_corpus[sess_id]
            # Uproszczone sprawdzenie podciągu (usuwamy białe znaki)
            clean_quote = " ".join(quote.split())
            clean_corp = " ".join(corpus_text.split())
            if clean_quote.lower() not in clean_corp.lower() and clean_quote[:30].lower() not in clean_corp.lower():
                # Odrzucamy halucynację
                continue

        ev_obj = SingleEvaluation(
            category=ev.get("category", "missing_rule"),
            title=ev.get("title", "Nieznana luka"),
            affected_section=ev.get("affected_section", "Ogólne"),
            session_id=sess_id,
            quote=quote,
            explanation=ev.get("explanation", ""),
        )
        eval_objs.append(ev_obj)

        # Rejestracja w ledgerze
        if ev_obj.category in ("rule_violation", "missing_rule", "stale_rule", "unneeded_discovery"):
            ledger.record_evidence(
                title=ev_obj.title,
                category=ev_obj.category,
                affected_section=ev_obj.affected_section,
                session_id=ev_obj.session_id,
                harness="auto",
                quote=ev_obj.quote,
                min_sessions=min_sessions_per_gap,
            )

    ledger.save()

    # 2. Parsowanie i walidacja edycji (Gradient Step)
    raw_edits = data.get("proposed_gradient_edits", [])[:max_edits]
    proposed_edits: List[ProposedEdit] = []

    with open(target_file_path, "r", encoding="utf-8", errors="ignore") as f:
        current_content = f.read()

    simulated_content = current_content

    for ed in raw_edits:
        e_type = ed.get("edit_type", "modify")
        sect = ed.get("section", "Ogólne")
        just = ed.get("justification", "")
        ev_sessions = ed.get("evidence_sessions", [])
        old_t = ed.get("old_text", "")
        new_t = ed.get("new_text", "")
        skill_n = ed.get("skill_name")

        # Reguła próg 2 sesji
        # Sprawdzamy czy powiązana luka ma status 'graduated' lub czy podano >= 2 sesje
        is_graduated = len(set(ev_sessions)) >= min_sessions_per_gap
        if not is_graduated:
            # Sprawdzamy w ledgerze
            for g in ledger.gaps.values():
                if g.status == "graduated" and (sect.lower() in g.affected_section.lower() or g.title.lower() in just.lower()):
                    is_graduated = True
                    break

        if not is_graduated and e_type == "add":
            proposed_edits.append(
                ProposedEdit(
                    edit_type=e_type,
                    target_file=str(target_file_path.name),
                    section=sect,
                    justification=just,
                    evidence_sessions=ev_sessions,
                    old_text=old_t,
                    new_text=new_t,
                    skill_name=skill_n,
                    is_valid=False,
                    validation_error=f"Odrzucono: brak potwierdzenia z minimum {min_sessions_per_gap} sesji (obecnie: {len(ev_sessions)}). Luka została zapisana w ledgerze i oczekuje na drugie potwierdzenie.",
                )
            )
            continue

        # Sprawdzamy czy old_text istnieje w pliku dla 'modify'/'delete'
        if e_type in ("modify", "delete") and old_t:
            if old_t not in simulated_content:
                # Spróbujmy znaleźć dopasowanie po liniach
                found = False
                for line in old_t.splitlines():
                    if line.strip() and line.strip() in simulated_content:
                        found = True
                        break
                if not found:
                    proposed_edits.append(
                        ProposedEdit(
                            edit_type=e_type,
                            target_file=str(target_file_path.name),
                            section=sect,
                            justification=just,
                            evidence_sessions=ev_sessions,
                            old_text=old_t,
                            new_text=new_t,
                            skill_name=skill_n,
                            is_valid=False,
                            validation_error="Odrzucono: wskazany stary fragment (old_text) nie istnieje w bieżącej wersji pliku.",
                        )
                    )
                    continue

        # Zastosuj w symulacji
        if e_type == "add":
            simulated_content += f"\n\n{new_t}"
        elif e_type == "modify":
            if old_t in simulated_content:
                simulated_content = simulated_content.replace(old_t, new_t, 1)
        elif e_type == "delete":
            if old_t in simulated_content:
                simulated_content = simulated_content.replace(old_t, "", 1)
        elif e_type == "extract_to_skill":
            if old_t in simulated_content:
                simulated_content = simulated_content.replace(old_t, f"- Reguła przeniesiona do skilla `_skille/{skill_n or 'skill'}.md`", 1)

        proposed_edits.append(
            ProposedEdit(
                edit_type=e_type,
                target_file=str(target_file_path.name),
                section=sect,
                justification=just,
                evidence_sessions=ev_sessions,
                old_text=old_t,
                new_text=new_t,
                skill_name=skill_n,
                is_valid=True,
            )
        )

    # 3. Weryfikacja budżetu tokenów (Zero-Sum Guard)
    curr_tokens = estimate_tokens(current_content)
    new_tokens = estimate_tokens(simulated_content)
    token_delta = new_tokens - curr_tokens
    budget_ok, delta, msg = verify_zero_sum_edit(current_content, simulated_content, token_budget=token_budget)

    valid_count = len([p for p in proposed_edits if p.is_valid])
    summary = f"Krok gradientowy: {valid_count} poprawnych propozycji edycji (delta: {token_delta:+d} tokenów, nowy stan: {new_tokens}/{token_budget}). {msg}"

    return GradientStepResult(
        evaluated_sessions_count=len(distilled_sessions),
        evaluations=eval_objs,
        proposed_edits=proposed_edits,
        token_delta=token_delta,
        new_estimated_tokens=new_tokens,
        budget_passed=budget_ok,
        status_summary=summary,
    )


def call_llm_endpoint(prompt: str, endpoint_url: str = "http://localhost:1234/v1/chat/completions", model_name: str = "default") -> Optional[str]:
    """Wywołuje lokalny lub zdalny endpoint zgodny z OpenAI API (np. LM Studio, LiteLLM, Ollama)."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": EVALUATION_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.1,
    }
    req = urllib.request.Request(endpoint_url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Evaluator] Endpoint niedostępny ({endpoint_url}): {e}")
        return None


if __name__ == "__main__":
    from distiller import distill_session
    from scanner import scan_all_sessions

    target_repo = Path("/Users/phantom/Documents/AIOS-Vault")
    agents_file = target_repo / "AGENTS.md"
    ledger = GapLedger()
    sessions = scan_all_sessions(target_repo, since="7d", max_sessions=2)
    dist_list = [distill_session(s.file_path, s.harness, s.session_id) for s in sessions]

    prompt = build_evaluation_prompt(agents_file, dist_list, ledger)
    print("Wygenerowano Prompt Packet (długość znaków:", len(prompt), ")")
    print(prompt[:500] + "\n...")
