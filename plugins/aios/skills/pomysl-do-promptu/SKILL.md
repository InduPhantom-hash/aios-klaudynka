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
6. **Struktura Plików & Architektura:** Rekomendacja techniczna (Next.js/Vite/Supabase/Tailwind itp.).
7. **Finałowy Initial Prompt:** Generowanie jednorazowego, potężnego prompta do wklejenia w generator AI (Cursor / Replit / Antigravity).

## Wynik (Output)

Utworzenie folderu projektu `Projekty/Prywatne/<nazwa-aplikacji>/` z plikami:
- `README.md` (Brief i specyfikacja)
- `initial-prompt.md` (Gotowy prompt Vibe Coding)
- `zadania.md` (Zadania wdrożeniowe)
