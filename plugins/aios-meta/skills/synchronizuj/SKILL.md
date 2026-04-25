---
name: synchronizuj
description: >
  Porownuje vault z bliznniakami (Linear, ClickUp, Notion, Airtable) i pokazuje rozjazdy - co jest w vaulcie a nie w bliznniaku i odwrotnie.
  Konfiguracja bliznniakow czytana z me.md (sekcja Bliznniaki). Vault = zrodlo prawdy.
  Triggery: /aios-meta:synchronizuj, "sprawdz bliznniaki", "rozjazdy vault", "synchronizuj vault".
---

# AIOS Meta: Synchronizuj Bliznniaki

Porownaj vault z kazdym aktywnym bliznniakiem. Pokaz rozjazdy - nie synchronizuj automatycznie.

Vault = zrodlo prawdy. Bliznniacy = widoki na wybrane fragmenty vaulta.

## Krok 0: Wczytaj konfiguracje z me.md

Przeczytaj `me.md` -> `## Bliznniaki`. Spodziewasz sie wpisow w stylu:

```
### Issue tracker
- typ: linear | github | jira | brak
- workspace: <URL>
- mapowanie projekt vault -> issue tracker:
  | sciezka w vaulcie                        | team_id / repo  | plik issues.md          |
  |------------------------------------------|-----------------|-------------------------|
  | Projekty/Vibe-coding/<projekt-A>/        | <ID>            | issues.md               |
  | Projekty/Vibe-coding/<projekt-B>/        | <ID>            | issues.md               |

### Task tracker
(jak w /aios:zadania)

### Notion
- typ: tak | brak
- index: _pamiec/notion-index.md

### Airtable
- typ: tak | brak
- index: _pamiec/airtable-index.md
```

**Jesli sekcja Bliznniaki nie istnieje albo wszystkie typy = brak:** powiedz "Nie masz skonfigurowanych bliznniakow w me.md - nie ma czego synchronizowac. Uruchom `/aios:init` i wypelnij Sekcje E albo dopisz recznie do me.md."

## Input

```
/aios-meta:synchronizuj [--blizniacy linear|clickup|notion|airtable|all]
```

Jesli `--blizniacy` nie podano: sprawdz wszystkie aktywne (`typ != brak`) z me.md.

## Krok 1: Issue tracker (Linear / GitHub / Jira)

Dla kazdego wiersza tabeli "mapowanie projekt vault -> issue tracker" z me.md:

**Vault -> tracker:**
- Otworz plik wskazany w kolumnie "plik issues.md" (relatywnie do `<sciezka w vaulcie>`).
- Kazda linia z ID issue (format zgodny z trackerem - `LIN-NNN` dla Linear, `#NNN` dla GitHub) to wpis do sprawdzenia.
- Dla kazdego ID: pobierz issue z trackera (`get_issue` / odpowiednik) i porownaj tytul + status z plikiem vault.

**Tracker -> vault:**
- Pobierz otwarte issues z trackera (`list_issues` z filtrem na `team_id` / `repo`).
- Sprawdz czy kazdy ma odpowiadajacy wpis w pliku `issues.md`.

Zapisz rozbieznosci per projekt:
- W vaulcie, brak w trackerze
- W trackerze, brak w vaulcie
- Status rozny

## Krok 2: Task tracker (ClickUp / Linear / Asana / Notion)

Bierze konfiguracje z `## Bliznniaki -> ### Task tracker` (tej samej co `/aios:zadania`).

**Vault -> tracker:**
- Przeczytaj `_pamiec/zadania-log.md` (log z `/aios:zadania`) jesli istnieje.
- Przeczytaj `_pamiec/przypomnienia.md` jesli istnieje.

**Tracker -> vault:**
- Pobierz otwarte zadania (`clickup_filter_tasks` / `list_issues` z filtrem assignee z me.md / `asana_get_tasks`).

Sprawdz:
- Czy zadania z logu/przypomnien maja odpowiadajacy task w trackerze
- Czy sa taski w trackerze bez wpisu w vaulcie

## Krok 3: Notion (opcjonalnie)

Jesli `me.md` -> Bliznniaki -> Notion -> typ: tak: przeczytaj plik wskazany w `index` (default: `_pamiec/notion-index.md`).

Tam powinny byc wymienione strony Notion ktore sa bliznniakami plikow vault.

Dla kazdej pozycji: wywolaj `notion-fetch` i sprawdz czy strona Notion istnieje i czy nie jest pustym placeholderem.

## Krok 4: Airtable (opcjonalnie)

Jesli `me.md` -> Bliznniaki -> Airtable -> typ: tak: przeczytaj plik wskazany w `index`.

Dla kazdej tabeli: `list_records_for_table` + porownaj z odpowiadajacym plikiem vault.

## Krok 5: Raport

```
SYNCHRONIZACJA BLIZNIAKOW - [data]

ISSUE TRACKER (<typ z me.md>):
  <projekt-A>: N issues OK, M rozjazdow
    - W vaulcie, brak w trackerze: [lista ID/tytulow]
    - W trackerze, brak w vaulcie: [lista ID/tytulow]
    - Status rozny: [ID: vault=X, tracker=Y]
  <projekt-B>: ...
  [lub: "Tracker niedostepny / brak pliku issues.md"]

TASK TRACKER (<typ z me.md>):
  N taskow OK, M rozjazdow
  - W vaulcie, brak w trackerze: ...
  - W trackerze, brak w vaulcie: ...
  [lub: "Tracker niedostepny"]

NOTION:
  [raport lub "Notion typ=brak, pomijam"]

AIRTABLE:
  [raport lub "Airtable typ=brak, pomijam"]

LACZNIE: N rozjazdow do naprawienia.
```

## Krok 6: Propozycja naprawy

Po raporcie: jesli sa rozjazdy, zapytaj "Naprawic ktorys z rozjazdow?" i czekaj.

Nie naprawiaj automatycznie - vault = zrodlo prawdy, kazda zmiana wymaga decyzji usera.

## Czego NIE rob

- Nie tworz automatycznie issues ani taskow w bliznniakach
- Nie nadpisuj danych w bliznniakach bez potwierdzenia
- Nie traktuj braku MCP jako bledu - po prostu pomin i zaznacz w raporcie
- Nie hardkoduj sciezek do issues.md - czytaj z me.md (tabela mapowania)
