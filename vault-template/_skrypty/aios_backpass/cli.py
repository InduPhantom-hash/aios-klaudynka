#!/usr/bin/env python3
"""cli.py – Główny interfejs CLI systemu aios-backpass (File Over AI).

Komendy:
  aios-backpass scan     - Skanuje i listuje sesje powiązane z projektem
  aios-backpass distill  - Destyluje transkrypty do formatu pozbawionego szumu
  aios-backpass budget   - Sprawdza podział tokenów i sekcji w AGENTS.md
  aios-backpass ledger   - Wyświetla i zarządza rejestrem luk (gap-ledger.json)
  aios-backpass eval     - Przygotowuje pakiet promptu lub wykonuje ewaluację
  aios-backpass report   - Generuje raport Markdown z dowodami w _pamiec/
  aios-backpass apply    - Interaktywny przegląd i zatwierdzanie diffów (Human Gate)
"""

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import List, Optional

from budget import analyze_file_budget, estimate_tokens
from distiller import DistilledSession, distill_session
from evaluator import (
    GradientStepResult,
    ProposedEdit,
    build_evaluation_prompt,
    call_llm_endpoint,
    validate_and_apply_gradient_step,
)
from ledger import GapLedger
from scanner import scan_all_sessions


# Kolory ANSI dla terminala
class Colors:
    HEADER = "\033[95m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def cmd_scan(args: argparse.Namespace) -> None:
    target_path = Path(args.target).resolve()
    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS: SKANOWANIE SESJI ==={Colors.ENDC}")
    print(f"Katalog docelowy: {target_path}")
    print(f"Okno czasowe: {args.since} | Limit: {args.max_sessions} sesji")

    sessions = scan_all_sessions(target_path, since=args.since, max_sessions=args.max_sessions)
    if not sessions:
        print(f"{Colors.WARNING}Nie znaleziono sesji w zadanym oknie czasowym.{Colors.ENDC}")
        return

    print(f"\nZnaleziono {len(sessions)} powiązanych sesji:")
    print("-" * 78)
    print(f"{'ŚRODOWISKO':<18} {'DATA':<12} {'ROZMIAR':<10} {'TURY':<8} {'ID SESJI'}")
    print("-" * 78)
    for s in sessions:
        h_col = Colors.BLUE if s.harness == "antigravity" else (Colors.GREEN if s.harness == "claude" else Colors.CYAN)
        size_kb = f"{s.size_bytes / 1024:.1f} KB"
        dt = s.created_at[:10] if s.created_at else "---"
        print(f"{h_col}{s.harness:<18}{Colors.ENDC} {dt:<12} {size_kb:<10} {s.turns_count:<8} {s.session_id}")


def cmd_budget(args: argparse.Namespace) -> None:
    target_file = Path(args.file).resolve()
    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS: AUDYT BUDŻETU TOKENÓW ==={Colors.ENDC}")
    print(f"Plik: {target_file}")

    rep = analyze_file_budget(target_file, token_budget=args.limit)
    status_col = Colors.FAIL if rep.is_over_budget else (Colors.WARNING if rep.budget_usage_pct > 85 else Colors.GREEN)

    print(f"Szacowane tokeny: {status_col}{rep.total_est_tokens} / {rep.token_budget} ({rep.budget_usage_pct:.1f}%){Colors.ENDC}")
    print(f"Liczba linii: {rep.total_lines} | Słowa: {rep.total_words} | Znaki: {rep.total_chars}")

    print(f"\n{Colors.BOLD}Podział na sekcje:{Colors.ENDC}")
    print("-" * 78)
    print(f"{'POZIOM':<8} {'SEKCJA':<38} {'TOKENY':<10} {'UDZIAŁ'}")
    print("-" * 78)
    for s in rep.sections:
        print(f"{s.level*'#':<8} {s.title[:36]:<38} {s.est_tokens:<10} {s.token_share_pct:.1f}%")

    if rep.skill_extraction_candidates:
        print(f"\n{Colors.WARNING}{Colors.BOLD}Kandydaci do ekstrakcji do skilli (Skill Release Valve):{Colors.ENDC}")
        for c in rep.skill_extraction_candidates:
            print(f" * {c}")


def cmd_ledger(args: argparse.Namespace) -> None:
    ledger_path = Path(args.ledger_file).resolve() if args.ledger_file else None
    ledger = GapLedger(ledger_path)
    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS: REJESTR LUK (GAP LEDGER) ==={Colors.ENDC}")
    print(f"Ścieżka: {ledger.ledger_path}")
    print(f"Liczba zarejestrowanych luk: {len(ledger.gaps)}")

    graduated = ledger.get_graduated_gaps()
    unconfirmed = ledger.get_unconfirmed_gaps()

    print(f"\n{Colors.GREEN}{Colors.BOLD}1. Luki zakwalifikowane do wdrożenia (Graduated, sesje >= 2): {len(graduated)}{Colors.ENDC}")
    for g in graduated:
        print(f" - [{Colors.GREEN}{g.category}{Colors.ENDC}] ID: {g.gap_id}")
        print(f"   Tytuł: {g.title} (Sekcja: {g.affected_section})")
        print(f"   Sesje ({g.sessions_count}): {', '.join([q.session_id[:8] for q in g.evidence_quotes])}")

    print(f"\n{Colors.WARNING}{Colors.BOLD}2. Luki oczekujące na 2. potwierdzenie (Unconfirmed, 1 sesja): {len(unconfirmed)}{Colors.ENDC}")
    for g in unconfirmed:
        print(f" - [{Colors.WARNING}{g.category}{Colors.ENDC}] ID: {g.gap_id}")
        print(f"   Tytuł: {g.title} (Sekcja: {g.affected_section}) | Data: {g.first_seen[:10]}")


def cmd_distill(args: argparse.Namespace) -> None:
    target_path = Path(args.target).resolve()
    sessions = scan_all_sessions(target_path, since=args.since, max_sessions=args.max_sessions)
    if not sessions:
        print(f"{Colors.WARNING}Brak sesji do destylacji.{Colors.ENDC}")
        return

    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS: DESTYLACJA {len(sessions)} SESJI ==={Colors.ENDC}")
    dist_list = []
    tot_orig = 0
    tot_dist = 0

    for s in sessions:
        d = distill_session(s.file_path, s.harness, s.session_id)
        dist_list.append(d)
        tot_orig += d.original_size_bytes
        tot_dist += d.distilled_size_bytes

    tot_ratio = (tot_dist / max(tot_orig, 1)) * 100
    print(f"Rozmiar surowy: {tot_orig/1024:.1f} KB -> Zdestylowany: {tot_dist/1024:.1f} KB (Odszumienie: {100 - tot_ratio:.1f}%)")

    if args.output:
        out_p = Path(args.output).resolve()
        out_p.parent.mkdir(parents=True, exist_ok=True)
        with open(out_p, "w", encoding="utf-8") as f:
            for d in dist_list:
                f.write(d.compact_text + "\n\n")
        print(f"{Colors.GREEN}Zapisano zdestylowany korpus do: {out_p}{Colors.ENDC}")


def cmd_eval(args: argparse.Namespace) -> None:
    target_repo = Path(args.target).resolve()
    target_file = Path(args.file).resolve() if args.file else target_repo / "AGENTS.md"
    ledger_path = Path(args.ledger_file).resolve() if args.ledger_file else target_repo / ".aios-loop" / "gap-ledger.json"
    ledger = GapLedger(ledger_path)

    sessions = scan_all_sessions(target_repo, since=args.since, max_sessions=args.max_sessions)
    if not sessions:
        print(f"{Colors.WARNING}Brak sesji do ewaluacji.{Colors.ENDC}")
        return

    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS: PRZYGOTOWANIE KROKU GRADIENTOWEGO ==={Colors.ENDC}")
    print(f"Target: {target_file}")
    print(f"Liczba sesji: {len(sessions)}")

    dist_list = [distill_session(s.file_path, s.harness, s.session_id) for s in sessions]
    prompt_text = build_evaluation_prompt(target_file, dist_list, ledger, token_budget=args.limit)

    # Zapis pakietu promptu
    prompt_out = target_repo / "_pamiec" / "backpass-eval-prompt.md"
    prompt_out.parent.mkdir(parents=True, exist_ok=True)
    with open(prompt_out, "w", encoding="utf-8") as f:
        f.write(prompt_text)

    print(f"\n{Colors.GREEN}Pomyślnie wygenerowano pakiet ewaluacyjny (Prompt Packet):{Colors.ENDC}")
    print(f" -> {prompt_out}")
    print(f"Możesz wkleić ten plik do dowolnego AI (Claude, Gemini, ChatGPT, Ollama) lub uruchomić z flagą --auto jeśli masz aktywny endpoint.")

    # Jeśli podano --auto i endpoint jest dostępny
    if args.auto:
        print(f"\n{Colors.BLUE}Próba automatycznego wywołania endpointu LLM ({args.endpoint})...{Colors.ENDC}")
        resp = call_llm_endpoint(prompt_text, endpoint_url=args.endpoint, model_name=args.model)
        if resp:
            print(f"{Colors.GREEN}Otrzymano odpowiedź z modelu.{Colors.ENDC}")
            res_obj = validate_and_apply_gradient_step(
                resp, target_file, dist_list, ledger, token_budget=args.limit
            )
            print(f"\n{Colors.BOLD}Wynik walidacji kroku gradientowego:{Colors.ENDC}")
            print(res_obj.status_summary)
            for p in res_obj.proposed_edits:
                status = f"{Colors.GREEN}[POPRAWNA]{Colors.ENDC}" if p.is_valid else f"{Colors.FAIL}[ODRZUCONA]{Colors.ENDC}"
                print(f" * {status} {p.edit_type.upper()} ({p.section}): {p.justification}")
                if p.validation_error:
                    print(f"   -> Błąd: {p.validation_error}")


def show_diff(old_text: str, new_text: str) -> None:
    """Wyświetla kolorowy diff w terminalu."""
    old_lines = old_text.splitlines(keepends=True)
    new_lines = new_text.splitlines(keepends=True)
    diff = list(difflib.unified_diff(old_lines, new_lines, fromfile="przed", tofile="po"))
    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            print(f"{Colors.GREEN}{line.rstrip()}{Colors.ENDC}")
        elif line.startswith("-") and not line.startswith("---"):
            print(f"{Colors.FAIL}{line.rstrip()}{Colors.ENDC}")
        elif line.startswith("@"):
            print(f"{Colors.CYAN}{line.rstrip()}{Colors.ENDC}")
        else:
            print(line.rstrip())


def cmd_apply(args: argparse.Namespace) -> None:
    target_repo = Path(args.target).resolve()
    target_file = Path(args.file).resolve() if args.file else target_repo / "AGENTS.md"
    proposals_file = Path(args.proposals).resolve() if args.proposals else target_repo / "_pamiec" / "backpass-proposals.json"

    print(f"{Colors.BOLD}{Colors.CYAN}=== AIOS BACKPASS APPLY: BRAMKA WERYFIKACJI (HUMAN GATE) ==={Colors.ENDC}")

    if not proposals_file.exists():
        print(f"{Colors.FAIL}Nie znaleziono pliku propozycji: {proposals_file}{Colors.ENDC}")
        print("Uruchom najpierw krok ewaluacji 'aios-backpass eval'.")
        return

    with open(proposals_file, "r", encoding="utf-8") as f:
        proposals_data = json.load(f)

    edits = proposals_data.get("proposed_gradient_edits", [])
    if not edits:
        print(f"{Colors.WARNING}Brak propozycji edycji w pliku.{Colors.ENDC}")
        return

    with open(target_file, "r", encoding="utf-8") as f:
        current_content = f.read()

    modified_content = current_content
    applied_count = 0
    ledger = GapLedger(target_repo / ".aios-loop" / "gap-ledger.json")

    for idx, ed in enumerate(edits, 1):
        print(f"\n{Colors.BOLD}--- PROPOZYCJA {idx}/{len(edits)}: [{ed.get('edit_type', '').upper()}] Sekcja: {ed.get('section')} ---{Colors.ENDC}")
        print(f"Uzasadnienie: {ed.get('justification')}")
        ev_sess = ed.get('evidence_sessions', [])
        print(f"Sesje dowodowe: {', '.join(ev_sess)}")

        old_t = ed.get("old_text", "")
        new_t = ed.get("new_text", "")

        print(f"\n{Colors.BOLD}Podgląd zmian (Diff):{Colors.ENDC}")
        show_diff(old_t, new_t)

        try:
            choice = input(f"\n{Colors.BOLD}Czy zatwierdzić tę zmianę? [t/n/q]: {Colors.ENDC}").strip().lower()
        except EOFError:
            choice = "n"

        if choice == "q":
            print("Przerwano procedurę.")
            break
        elif choice in ("t", "y", "tak"):
            e_type = ed.get("edit_type")
            if e_type == "add":
                modified_content += f"\n\n{new_t}"
            elif e_type == "modify" and old_t in modified_content:
                modified_content = modified_content.replace(old_t, new_t, 1)
            elif e_type == "delete" and old_t in modified_content:
                modified_content = modified_content.replace(old_t, "", 1)
            elif e_type == "extract_to_skill":
                skill_name = ed.get("skill_name", "nowy-skill")
                skill_path = target_repo / "_skille" / f"{skill_name}.md"
                skill_path.parent.mkdir(parents=True, exist_ok=True)
                with open(skill_path, "w", encoding="utf-8") as sf:
                    sf.write(f"# Skill: {skill_name}\n\n{old_t}\n")
                if old_t in modified_content:
                    modified_content = modified_content.replace(old_t, f"- Reguła przeniesiona do skilla `_skille/{skill_name}.md`", 1)
                print(f"{Colors.GREEN}Wyodrębniono do skilla: {skill_path}{Colors.ENDC}")

            applied_count += 1
            print(f"{Colors.GREEN}Zaakceptowano zmianę {idx}.{Colors.ENDC}")
        else:
            print(f"{Colors.WARNING}Pominięto zmianę {idx}.{Colors.ENDC}")

    if applied_count > 0:
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(modified_content)
        print(f"\n{Colors.GREEN}{Colors.BOLD}Zapisano {applied_count} zmian w pliku {target_file}.{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}Nie wprowadzono żadnych zmian w pliku {target_file}.{Colors.ENDC}")


def main() -> None:
    parser = argparse.ArgumentParser(description="AIOS Backpass – Gradient Descent dla instrukcji i pamięci agentów.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan
    p_scan = subparsers.add_parser("scan", help="Skanuje i listuje sesje")
    p_scan.add_argument("--target", default=".", help="Katalog projektu/vaulta")
    p_scan.add_argument("--since", default="14d", help="Okno czasowe (np. 7d, 30d)")
    p_scan.add_argument("--max-sessions", type=int, default=50, help="Maksymalna liczba sesji")

    # distill
    p_dist = subparsers.add_parser("distill", help="Destyluje transkrypty")
    p_dist.add_argument("--target", default=".", help="Katalog projektu")
    p_dist.add_argument("--since", default="14d", help="Okno czasowe")
    p_dist.add_argument("--max-sessions", type=int, default=10, help="Maksymalna liczba sesji")
    p_dist.add_argument("--output", help="Plik wyjściowy dla zdestylowanego korpusu")

    # budget
    p_bud = subparsers.add_parser("budget", help="Sprawdza budżet tokenów")
    p_bud.add_argument("--file", default="AGENTS.md", help="Plik instrukcji")
    p_bud.add_argument("--limit", type=int, default=2000, help="Maksymalny limit tokenów")

    # ledger
    p_led = subparsers.add_parser("ledger", help="Wyświetla Gap Ledger")
    p_led.add_argument("--ledger-file", help="Ścieżka do gap-ledger.json")

    # eval
    p_eval = subparsers.add_parser("eval", help="Generuje pakiet ewaluacyjny")
    p_eval.add_argument("--target", default=".", help="Katalog projektu")
    p_eval.add_argument("--file", help="Plik instrukcji (domyślnie AGENTS.md)")
    p_eval.add_argument("--since", default="14d", help="Okno czasowe")
    p_eval.add_argument("--max-sessions", type=int, default=5, help="Maksymalna liczba sesji")
    p_eval.add_argument("--limit", type=int, default=2000, help="Budżet tokenów")
    p_eval.add_argument("--ledger-file", help="Ścieżka do gap-ledger.json")
    p_eval.add_argument("--auto", action="store_true", help="Automatyczne zapytanie do endpointu")
    p_eval.add_argument("--endpoint", default="http://localhost:1234/v1/chat/completions", help="URL endpointu LLM")
    p_eval.add_argument("--model", default="default", help="Nazwa modelu")

    # apply
    p_app = subparsers.add_parser("apply", help="Interaktywna aplikacja zmian")
    p_app.add_argument("--target", default=".", help="Katalog projektu")
    p_app.add_argument("--file", help="Plik instrukcji")
    p_app.add_argument("--proposals", help="Plik JSON z propozycjami")

    args = parser.parse_args()

    commands = {
        "scan": cmd_scan,
        "distill": cmd_distill,
        "budget": cmd_budget,
        "ledger": cmd_ledger,
        "eval": cmd_eval,
        "apply": cmd_apply,
    }

    commands[args.command](args)


if __name__ == "__main__":
    main()
