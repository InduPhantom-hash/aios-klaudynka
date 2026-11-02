---
name: pomysl-do-promptu
description: >
  Interaktywny przewodnik od surowego pomysłu na aplikację do gotowego PRD, makiet UI i potężnego initial prompta dla generatorów Vibe Coding (Cursor, Replit Agent, Antigravity, Vercel).
  Triggery: /aios:pomysl-do-promptu, /pomysl-do-promptu, mam pomysł na aplikację, specyfikacja do promptu.
---

# AIOS: Pomysł do Promptu (Vibe Coding Assistant)

Skill prowadzący użytkownika od luźnego pomysłu biznesowego/aplikacyjnego do kompletnego zestawu specyfikacji i gotowego promptu startowego.

## Przepływ Pracy (7 Kroków)

1. **Brain Dump:** Użytkownik wylewa swój pomysł w dowolnej formie (tekst, punkty, nagranie audio).
2. **Krótki Brief:** AIOS zadaje do 3 doprecyzowujących pytań o cel, odbiorców i kluczową wartość.
3. **Design Direction:** Ustalenie estetyki (kolory, typografia, klimat UI) na podstawie nowoczesnych wzorców webowych.
4. **Specyfikacja Funkcjonalna (MoSCoW):** Podział funkcji na Must-have (MVP 1.0) oraz Should-have/Nice-to-have (V2).
5. **Makiety & Przepływ Ekrany:** Szkic widoków i przejść użytkownika w markdown.
6. **Struktura Plików & Architektura:** Najpierw sprawdź lokalnym RAG wzorce w `wiedza-programming` i namespace projektu, jeśli istnieją, oraz odczytaj źródła. Przy braku RAG użyj indeksów plików. Rekomendacja techniczna (Next.js/Vite/Supabase/Tailwind itp.).
7. **Finałowy Initial Prompt:** Generowanie jednorazowego, potężnego prompta do wklejenia w generator AI (Cursor / Replit / Antigravity).

## Wynik (Output)

Po potwierdzeniu celu i kategorii utwórz folder `Projekty/<zatwierdzona-kategoria>/<nazwa-aplikacji>/` z plikami. Nie zakładaj kategorii `Prywatne`, bo domyślna polityka RAG ją wyklucza:
- `README.md` (Brief i specyfikacja)
- `initial-prompt.md` (Gotowy prompt Vibe Coding)
- `zadania.md` (Zadania wdrożeniowe)

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
