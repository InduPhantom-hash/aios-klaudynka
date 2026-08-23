#!/usr/bin/env python3
"""budget.py – Strażnik budżetu tokenów i zawór bezpieczeństwa (Token Budget Guard & Skill Release Valve).

Pilnuje, aby pliki instrukcji (AGENTS.md) nie ulegały degradacji ("bloat").
Wymusza bilans zero-sum przy przepełnieniu oraz typuje rzadkie reguły do ekstrakcji do skilli.
"""

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SectionBudget:
    title: str
    level: int
    lines_count: int
    words_count: int
    chars_count: int
    est_tokens: int
    token_share_pct: float
    raw_content: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class BudgetReport:
    file_path: str
    total_lines: int
    total_words: int
    total_chars: int
    total_est_tokens: int
    token_budget: int
    budget_usage_pct: float
    is_over_budget: bool
    sections: List[SectionBudget]
    skill_extraction_candidates: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "total_lines": self.total_lines,
            "total_words": self.total_words,
            "total_chars": self.total_chars,
            "total_est_tokens": self.total_est_tokens,
            "token_budget": self.token_budget,
            "budget_usage_pct": round(self.budget_usage_pct, 1),
            "is_over_budget": self.is_over_budget,
            "sections": [s.to_dict() for s in self.sections],
            "skill_extraction_candidates": self.skill_extraction_candidates,
        }


def estimate_tokens(text: str) -> int:
    """Szacuje liczbę tokenów dla tekstu polsko-angielskiego."""
    if not text:
        return 0
    # Średnio 3.6 znaku na token dla mieszanego tekstu PL/EN z kodem markdown
    chars = len(text)
    words = len(text.split())
    # Średnia ważona ze słów i znaków
    return max(int(chars / 3.6), int(words * 1.3))


def analyze_file_budget(
    file_path: Path,
    token_budget: int = 2000,
    skill_token_threshold: int = 250
) -> BudgetReport:
    """Analizuje plik instrukcji pod kątem budżetu tokenów i podziału na sekcje."""
    if not file_path.exists():
        return BudgetReport(
            file_path=str(file_path),
            total_lines=0,
            total_words=0,
            total_chars=0,
            total_est_tokens=0,
            token_budget=token_budget,
            budget_usage_pct=0.0,
            is_over_budget=False,
            sections=[],
            skill_extraction_candidates=[],
        )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    lines = content.splitlines()
    total_lines = len(lines)
    total_words = len(content.split())
    total_chars = len(content)
    total_tokens = estimate_tokens(content)
    usage_pct = (total_tokens / max(token_budget, 1)) * 100.0
    is_over = total_tokens > token_budget

    # Dzielenie na sekcje po nagłówkach # lub ##
    sections: List[SectionBudget] = []
    current_title = "Wstęp"
    current_level = 1
    current_lines: List[str] = []

    for line in lines:
        if line.startswith("#"):
            if current_lines:
                sec_text = "\n".join(current_lines)
                sec_tokens = estimate_tokens(sec_text)
                sec_share = (sec_tokens / max(total_tokens, 1)) * 100.0
                sections.append(
                    SectionBudget(
                        title=current_title,
                        level=current_level,
                        lines_count=len(current_lines),
                        words_count=len(sec_text.split()),
                        chars_count=len(sec_text),
                        est_tokens=sec_tokens,
                        token_share_pct=round(sec_share, 1),
                        raw_content=sec_text,
                    )
                )
                current_lines = []

            header_match = line.lstrip("#")
            current_level = len(line) - len(header_match)
            current_title = header_match.strip()
            current_lines.append(line)
        else:
            current_lines.append(line)

    if current_lines:
        sec_text = "\n".join(current_lines)
        sec_tokens = estimate_tokens(sec_text)
        sec_share = (sec_tokens / max(total_tokens, 1)) * 100.0
        sections.append(
            SectionBudget(
                title=current_title,
                level=current_level,
                lines_count=len(current_lines),
                words_count=len(sec_text.split()),
                chars_count=len(sec_text),
                est_tokens=sec_tokens,
                token_share_pct=round(sec_share, 1),
                raw_content=sec_text,
            )
        )

    # Kandydaci do ekstrakcji do skilli (duże, wyspecjalizowane sekcje)
    skill_candidates: List[str] = []
    for s in sections:
        # Pomiń sekcje nadrzędne jak Zasady operacyjne, Profil, Start sesji
        skip_titles = ("wstęp", "start sesji", "źródła prawdy", "uprawnienia i checkpointy", "styl odpowiedzi")
        if any(st in s.title.lower() for st in skip_titles):
            continue
        if s.est_tokens >= skill_token_threshold or s.token_share_pct > 20.0:
            skill_candidates.append(f"Sekcja '{s.title}' ({s.est_tokens} tokenów, {s.token_share_pct}% całości)")

    return BudgetReport(
        file_path=str(file_path),
        total_lines=total_lines,
        total_words=total_words,
        total_chars=total_chars,
        total_est_tokens=total_tokens,
        token_budget=token_budget,
        budget_usage_pct=usage_pct,
        is_over_budget=is_over,
        sections=sections,
        skill_extraction_candidates=skill_candidates,
    )


def verify_zero_sum_edit(
    current_content: str,
    proposed_content: str,
    token_budget: int = 2000
) -> Tuple[bool, int, str]:
    """Weryfikuje czy proponowana zmiana mieści się w budżecie (zasada zero-sum)."""
    curr_tokens = estimate_tokens(current_content)
    prop_tokens = estimate_tokens(proposed_content)
    delta = prop_tokens - curr_tokens

    if prop_tokens <= token_budget:
        return True, delta, f"Zmiana mieści się w budżecie ({prop_tokens}/{token_budget} tokenów, delta: {delta:+d})."

    # Przekroczono budżet
    overflow = prop_tokens - token_budget
    return False, delta, f"BŁĄD BUDŻETU: Propozycja przekracza limit {token_budget} tokenów o {overflow} tokenów (delta: {delta:+d}). Wymagane usunięcie zbędnych reguł lub ekstrakcja do skilla."


if __name__ == "__main__":
    import sys
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "AGENTS.md"
    rep = analyze_file_budget(target, token_budget=1500)
    print(f"Plik: {rep.file_path}")
    print(f"Tokeny: {rep.total_est_tokens} / {rep.token_budget} ({rep.budget_usage_pct:.1f}%) | Przekroczenie: {rep.is_over_budget}")
    print("\nPodział sekcji:")
    for s in rep.sections:
        print(f" - [{s.level}#] {s.title}: {s.est_tokens} tok ({s.token_share_pct}%)")
    if rep.skill_extraction_candidates:
        print("\nKandydaci do ekstrakcji do skilli:")
        for c in rep.skill_extraction_candidates:
            print(f" * {c}")
