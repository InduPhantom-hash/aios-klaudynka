---
name: backpass
description: "Optymalizuje instrukcje projektowe (AGENTS.md, CLAUDE.md) metodą Gradient Descent na podstawie transkryptów sesji. Triggery: /aios:backpass, /backpass, \"optymalizuj instrukcje\", \"gradient descent\", \"audyt reguł\"."
---

# AIOS Backpass (Gradient Descent dla pamięci i instrukcji)

## Cel i kontekst

Uruchom deterministyczny audyt i optymalizację pliku instrukcji projektu (`AGENTS.md`, `CLAUDE.md`) na podstawie rzeczywistych transkryptów sesji z dysku (`~/.gemini/antigravity/brain/`, `~/.claude/projects/`, `~/.codex/`, `_brudnopis/`, `_pamiec/dziennik/`).

Filozofia **File Over AI** i **Code Over AI**:
- **Wagi** = plik `AGENTS.md` (instrukcje operacyjne).
- **Forward pass** = sesje robocze agentów.
- **Loss signal** = błędy, zbędne odkrywanie wiedzy i korekty użytkownika zapisane w transkryptach.
- **Backward pass** = zwięzły krok gradientowy (max 5 precyzyjnych edycji, popartych cytatami z min. 2 sesji, w ramach limitu tokenów).

## Procedura operacyjna

1. **Skanowanie i destylacja (Krok mechaniczny):**
   Uruchom skrypt silnika z poziomu projektu:
   Z korzenia vaulta użyj interpretera `.venv` (nie wymagaj bash ani wrappera powłokowego):
   ```sh
   ".venv/bin/python" "_skrypty/aios_backpass/cli.py" distill --target . --since 14d --output "_pamiec/backpass-corpus.txt"
   ```
   Windows PowerShell:
   ```powershell
   & ".\.venv\Scripts\python.exe" ".\_skrypty\aios_backpass\cli.py" distill --target . --since 14d --output "_pamiec/backpass-corpus.txt"
   ```
2. **Audyt budżetu tokenów (Budget Guard):**
   Sprawdź bieżący podział sekcji i limit tokenów:
   ```sh
   ".venv/bin/python" "_skrypty/aios_backpass/cli.py" budget --file AGENTS.md --limit 2000
   ```
   Windows PowerShell:
   ```powershell
   & ".\.venv\Scripts\python.exe" ".\_skrypty\aios_backpass\cli.py" budget --file AGENTS.md --limit 2000
   ```
3. **Analiza straty (Loss Evaluation):**
   - Odczytaj zdestylowany korpus `_pamiec/backpass-corpus.txt` oraz stan `.aios-loop/gap-ledger.json`.
   - Zidentyfikuj konkretne naruszenia reguł lub luki.
   - **Reguła twardego dowodu:** Każda zgłoszona luka MUSI zawierać dokładny, dosłowny cytat z transkryptu.
   - **Reguła minimum 2 sesji:** Do propozycji edycji kwalifikują się tylko luki potwierdzone w co najmniej 2 sesjach (lub zarejestrowane w ledgerze).
4. **Krok gradientowy (Gradient Proposal):**
   - Przygotuj maksymalnie 5 edycji (`add`, `modify`, `delete`, `extract_to_skill`).
   - Wymuś bilans zero-sum (brak rozrostu pliku ponad budżet).
   - Rzadkie reguły (<20% sesji) skieruj do ekstrakcji do `_skille/<nazwa>.md`.
5. **Human Gate (Przedstawienie propozycji użytkownikowi):**
   - Wygeneruj czytelny raport w `_pamiec/backpass-report.md` z `rag: false`: zawiera cytaty z logów, więc nie trafia domyślnie do wyszukiwania. Zachowaj też wymagane metadane nowej notatki.
   - Pokaż diffy wraz z cytatami i poproś o zatwierdzenie `[tak/nie]` dla każdej pozycji.
   - Po zatwierdzeniu zaktualizuj plik instrukcji i oznacz luki w ledgerze jako `converted_to_rule`.

## Checkpoint

- Nigdy nie modyfikuj `AGENTS.md` ani `me.md` bez pokazania konkretnego diffa i uzyskania zgody.
- Nie wprowadzaj nowych reguł po jednorazowym, przypadkowym błędzie (wymóg 2 sesji w ledgerze).

## Wynik

Raport podsumowujący: liczba przeskanowanych sesji, zidentyfikowane luki w ledgerze, wskaźnik budżetu tokenów oraz gotowy diff do zatwierdzenia.

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
