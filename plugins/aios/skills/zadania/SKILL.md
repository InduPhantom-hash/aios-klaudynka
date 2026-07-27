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
   - Otwórz plik `Projekty/<kategoria>/<projekt>/zadania.md`. Jeśli nie istnieje – utwórz z szablonu `_szablony/zadania.md`.
   - Dopisz nową pozycję `- [ ] <treść zadania>` pod sekcją `## DO ZROBIENIA`.
2. **Dla zadań ogólnych / bez projektu:**
   - Dopisz do `_pamiec/zadania-log.md`.

## Krok 4: Eksport do zewnętrznego bliźniaka (Opcjonalnie)

Jeśli w `me.md` w sekcji `## Bliźniaki -> Task tracker` użytkownik skonfigurował zewnętrzny tracker (ClickUp, Linear, Notion):
- Wywołaj odpowiednie narzędzie API (`clickup_create_task`, `linear`, `notion`), aby utworzyć powiązane zadanie.

## Krok 5: Raport końcowy

Jedna zwięzła linia:
```text
Dodano N zadań do lokalnego trackera (Projekty/.../zadania.md).
```
