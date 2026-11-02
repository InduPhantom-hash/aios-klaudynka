---
name: zadania
description: >
  Wyciąga zadania do zrobienia z aktualnej rozmowy i dodaje je do lokalnego AIOS Task Tracker (`Projekty/<nazwa>/zadania.md`) oraz opcjonalnie zewnętrznego bliźniaka (ClickUp/Linear/Notion).
  Zasada File Over AI i Code Over AI - zerowy koszt tokenowy, lokalny zapis markdown.
  Triggery: /aios:zadania, "wrzuć do zadań", "zadania z sesji", "co mam do zrobienia".
---

# AIOS: Zadania

User chce wyciągnąć i uporządkować zadania po rozmowie. Twoje zadanie: wyciągnąć z rozmowy konkretne akcje dla użytkownika, zaktualizować lokalny plik `Projekty/<nazwa>/zadania.md` (AIOS Task Tracker) oraz opcjonalnie wysłać do zewnętrznego trackera.

## Krok 1: Wyciągnij zadania z rozmowy

Przeskanuj rozmowę. Szukaj:
- Rzeczy, które użytkownik zadeklarował, że zrobi ("zrobię", "sprawdzę", "przetestuję").
- Następnych kroków wynikających z ustaleń.
- Zadania manualne / poza komputerem.

**Nie wciągaj:**
- Rzeczy już wykonanych w tej sesji przez AI.
- Luźnych pomysłów bez akcji.

## Krok 2: Pokaż listę do akceptacji

Format bez lania wody:

```text
Zadania z tej sesji:

1. [ ] <treść zadania> (Projekt: <Nazwa / Ogólne>)
2. [ ] <treść zadania> (Projekt: <Nazwa / Ogólne>)

Napisz "ok" lub podaj poprawki.
```

## Krok 3: Dodaj do lokalnego AIOS Task Tracker (File Over AI)

Po zatwierdzeniu przez użytkownika:

1. **Dla zadań z przypisanym projektem:**
   - Otwórz plik `Projekty/<kategoria>/<projekt>/zadania.md`. Jeśli nie istnieje - utwórz z szablonu `_szablony/zadania.md`.
   - Dopisz nową pozycję `- [ ] <treść zadania>` pod sekcją `## DO ZROBIENIA`.
2. **Dla zadań ogólnych / bez projektu:**
   - Dopisz do `_pamiec/zadania-log.md`.

## Krok 4: Eksport do zewnętrznego bliźniaka (Opcjonalnie)

Jeśli użytkownik jawnie poprosił o eksport do skonfigurowanego trackera, pokaż payload: tytuły, opisy, projekt/listę i zakres przesyłanych danych. Po zgodzie odkryj właściwe narzędzie API i utwórz zadania. Sama konfiguracja w `me.md` nie oznacza zgody na zewnętrzny zapis; bez integracji lokalny tracker działa nadal.

## Krok 5: Raport końcowy

Jedna zwięzła linia:
```text
Dodano N zadań do lokalnego trackera (Projekty/.../zadania.md).
```

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
