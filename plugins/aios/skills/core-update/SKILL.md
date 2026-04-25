---
name: core-update
description: >
  Audyt aktualnosci dokumentow nawigacyjnych AIOS + update + sprzatanie + opcjonalny reindex Pinecone.
  Pelny pipeline: wykrywa rozjazd rzeczywistego stanu vaulta z tym co opisane w me.md,
  vault-map.md, index.md (Projekty/, Wiedza/ + per-kategoria), _pamiec/DREAM.md,
  _pamiec/aktualny.md. Proponuje zmiany (diff per plik, user zatwierdza 1-litera),
  wykonuje update, czysci _inbox/, przenosi martwe foldery do Kosz/, na koncu
  reindeksuje Pinecone (jesli skonfigurowany - namespace-aware, tylko to co zmienione).
  Triggery: /aios:core-update, "zaktualizuj nawigacje", "audyt AIOS",
  "sprawdz czy wszystko aktualne", "core update", "przeglad vaulta".
---

# AIOS: Core Update

Pelny pipeline aktualizacji dokumentow nawigacyjnych AIOS. Uruchamia sie gdy user podejrzewa rozjazd miedzy rzeczywistym stanem vaulta (foldery, pliki, projekty) a tym co opisane w plikach-fundamentach.

## Filozofia

Dokumenty nawigacyjne sa **source of truth dla AI** - kazda nowa sesja czyta `me.md` + `vault-map.md` + `_pamiec/aktualny.md` + `DREAM.md`. Jesli cos jest tam nieaktualne, AI podejmuje decyzje na podstawie starych danych. Zasada: **lepiej poprawic raz, niz powtarzac te same korekty w kazdej sesji**.

Skill nie robi nic automatycznie bez potwierdzenia - audyt -> diff -> "tak" -> update. User decyduje, AIOS wykonuje.

## Kiedy uruchamiac

- Po okresie gestej pracy (kilka dni rozmow, duzo nowych plikow)
- Po promocji projektu z brudnopisu (`/aios:stworz-projekt` aktualizuje czesc, ale nie wszystko)
- Przed waznym reindexem Pinecone (zeby embeddingi byly aktualne)
- Gdy user wyczuwa "cos jest nieaktualne" w zachowaniu AI

## Input

- Brak argumentow: pelny audyt vaulta.
- `--dry-run`: tylko audyt + raport, bez zmian (zakoncz po Kroku 4).
- `--skip-reindex`: audyt + update + sprzatanie, bez Kroku 7 (Pinecone).
- `--tylko <plik>`: audyt jednego pliku nawigacyjnego (np. `--tylko DREAM.md`).

## Procedura

### Krok 1: Inwentarz rzeczywistego stanu

Zebrac fakty z filesystemu - co faktycznie jest w vaulcie:

1. **`/Projekty/` + podkategorie** - lista folderow projektow per kategoria. Odnotuj daty modyfikacji.
2. **`/Wiedza/` + obszary** - lista obszarow.
3. **`/_inbox/`** - wszystkie pliki (cokolwiek poza `.gitkeep` i `README.md` = nieposortowane).
4. **`/_brudnopis/`** - ostatnie 10 plikow po dacie modyfikacji.
5. **`/Kosz/`** - co tam lezy (bufor przed usunieciem).

### Krok 2: Odczyt dokumentow nawigacyjnych

Przeczytaj w kolejnosci i wyciagnij **co kazdy z nich twierdzi o vault**:

1. `me.md` - tabela "Aktywne projekty" (Status per projekt, sciezka, data ostatniej aktualizacji).
2. `vault-map.md` (jesli istnieje) - struktura folderow na kazdym poziomie.
3. `Projekty/index.md` + per-kategoria - wymienione projekty per kategoria.
4. `Wiedza/index.md`, `Wiedza/*/Wiki/index.md` - obszary + strony Wiki.
5. `_pamiec/DREAM.md` - tabela "Aktywne projekty" + "Log konsolidacji" (data ostatniej konsolidacji).
6. `_pamiec/aktualny.md` - ostatnia sesja (data, projekt, nastepny krok).

### Krok 3: Diff - co sie rozjezdza

Dla kazdego pliku nawigacyjnego zbuduj **liste rozjazdow**:

- **Brakuje w dokumencie** - folder/projekt istnieje na dysku, ale nie ma go w indexie/tabeli.
- **Nieaktualny status** - dokument mowi "MVP v0.1", a w rzeczywistosci v0.3.0 LIVE.
- **Bledny opis** - dokument opisuje obszar dzialalnosci niezgodnie z faktami z me.md.
- **Duplikat/kolizja** - dwa dokumenty podaja rozne fakty o tym samym.
- **Zapominane sesje** - `_brudnopis/` z ostatnich dni nie ma wpisu w `DREAM.md` (Log konsolidacji).

Dla kazdego rozjazdu przypisz **priorytet**:

- **K (krytyczny)** - bledne fakty w me.md/DREAM.md, ktore kieruja decyzje AI (np. zly status projektu aktywnego, zla branza).
- **W (wazny)** - brakujace foldery w indexach, brakujace wpisy w DREAM.md Log dla sesji >48h.
- **M (minor)** - brakujace cross-linki, daty aktualizacji.

### Krok 4: Raport - pokaz userowi

Format raportu - zwiezly, bez naglowkow typu "Oto wyniki audytu":

```
Audyt nawigacji AIOS - [data, czas]

Krytyczne (K):
- [plik] - [co jest zle, co ma byc]
- ...

Wazne (W):
- [plik] - [co brakuje]
- ...

Minor (M):
- [plik] - [drobiazg]
- ...

Sprzatanie:
- _inbox/: [N plikow nieposortowanych] - propozycje miejsc
- Kosz/: [co mozna usunac po >30 dniach]
- dead folders: [foldery do przeniesienia do Kosz/]

Reindex (jesli Pinecone skonfigurowany):
- Zmienione pliki (od ostatniej konsolidacji DREAM): [lista namespace-aware]
- Rekomendowane namespace do reindeksu: [lista]

Co robimy? [W] wszystko naraz / [K] tylko krytyczne / [P] pokaz diff per plik / [S] skip update, tylko reindex / [X] anuluj
```

Jesli tryb `--dry-run`: zakoncz tutaj, nie idz do Kroku 5.

### Krok 5: Update dokumentow

Jesli user wybral [W] albo [K]: wykonaj zmiany przez `Edit` (per plik).

**Kolejnosc update** (wazna - dokumenty sie referencjonuja):

1. `me.md` - najpierw (bo DREAM.md i inne odwoluja sie do projektow z tabeli me.md).
2. `vault-map.md` (jesli uzywany) - struktura vaulta.
3. `Projekty/index.md` + per-kategoria.
4. `Wiedza/index.md` + per-obszar.
5. `_pamiec/DREAM.md` - **append** nowych decyzji/sesji do Log konsolidacji (nie nadpisuj, tylko dopisz). Zaktualizuj "Ostatnia konsolidacja: [data]".
6. `_pamiec/aktualny.md` - nadpisuj (to jest zywy stan, nie historia).

**Zasada nadpisywania vs. append:**

- DREAM.md Log konsolidacji = **append only**. Historia ma byc immutable.
- DREAM.md tabela "Aktywne projekty", "Luki / do wypelnienia" = **update w miejscu** (prostowanie faktow).
- aktualny.md = **nadpisywane** (nie historia, tylko teraz).

Jesli user wybral [P] (diff per plik): pokaz proposed edit, czekaj na "tak"/"nie"/"pomin".

### Krok 6: Sprzatanie

**`_inbox/`**: dla kazdego pliku, ktory tam lezy (poza `.gitkeep` i `README.md`), zaproponuj 3-4 opcje docelowego miejsca (tak jak `/aios:sortuj`). User 1-litera decyduje.

Jesli user chce pominac sortowanie: zasugeruj odpalenie `/aios:sortuj` osobno.

**Kosz/**: jesli cos lezy >30 dni, powiedz userowi i zaproponuj fizyczne `rm -rf`. Nie kasuj sam (regulamin: AIOS przenosi do Kosz/, user sam `rm -rf` gdy gotowy).

**Dead folders**: zaproponuj `mv` do Kosz/ z podaniem powodu.

### Krok 7: Reindex Pinecone (opcjonalny)

Jesli nie `--skip-reindex` i `me.md` -> sekcja Stos zawiera Pinecone:

**Wymaganie**: Pinecone MCP musi byc zainstalowany i skonfigurowany. Index name z me.md (sekcja Stos -> Pinecone -> index_name), embedding model z me.md (default: `multilingual-e5-large`).

Jesli MCP niedostepny: powiedz **explicite** "Pinecone MCP niedostepny - pomijam reindex" i zakoncz.

**Strategia reindeksu:**

1. Pobierz liste plikow zmienionych od daty "Ostatnia konsolidacja" z poprzedniej DREAM.md (przed tym updatem).
2. Per namespace policz ile plikow dotkniete:
   - `fundament`: me.md, vault-map.md, CLAUDE.md
   - `pamiec`: _pamiec/DREAM.md, aktualny.md
   - `projekty-<kategoria>` per kategoria z `Projekty/`
   - `wiedza-<obszar>` per obszar z `Wiedza/`
   - `brudnopis` (jesli user explicite chce - domyslnie nie indeksujemy)

3. Dla kazdego namespace z >0 zmianami: wywolaj `upsert-records` (Pinecone MCP). Chunking: per plik, z metadanymi (path, updated, namespace).

4. **NIE indeksuj** (hard rule):
   - `.git/`, `node_modules/`, `.next/`, `__pycache__/`, `.pytest_cache/`
   - `Kosz/`, `_Archiwum/` (chyba ze user explicite prosi)
   - foldery oznaczone w me.md jako "ignoruj w reindeksie"

### Krok 8: Zamkniecie

Pokaz userowi podsumowanie w 1 ekranie:

```
Core update zakonczony.

Zmienione: [N plikow]
Przeniesione do Kosz: [N plikow]
Reindeks Pinecone: [N namespace x M records]  (jesli wykonany)

DREAM.md "Ostatnia konsolidacja" = [data]
aktualny.md = [nowy stan]

Nastepny krok (z aktualny.md): [cytat]
```

Bez wstepow, bez "Gotowe!". Jedna ramka, potem cisza.

## Obsluga edge case'ow

**Brak plikow-fundamentow** (np. me.md nie istnieje): zatrzymaj, powiedz explicite. Nie buduj od zera bez zgody usera.

**Konflikt faktow** (DREAM mowi X, me.md mowi Y): pokaz oba, zapytaj ktory jest prawda. Nie zgaduj.

**Brudnopisy nieopisane** (plik w _brudnopis/ z data ale bez frontmatter): zapisz jako "do konsolidacji manualnej" w raporcie, nie probuj auto-interpretowac.

**Wiele sesji tego samego dnia**: wszystkie musza trafic do DREAM.md Log - nie tylko najnowsza.

**Git uncommitted changes**: na koniec powiedz userowi `git status` pokazuje [N] zmian. Nie commituj sam.

## Czego NIE rob

- Nie kasuj plikow (przenoszenie do Kosz/ - tak, fizyczny `rm` - nigdy).
- Nie nadpisuj DREAM.md Log konsolidacji (append only).
- Nie reindeksuj wszystkiego (tylko zmienione od ostatniej konsolidacji).
- Nie ruszaj `me.md` HARD RULES (to fundament, dotykasz tylko za explicite zgoda).
- Nie zmieniaj filozofii AIOS z vault-map (File Over AI, Karpathy Raw->Wiki, itd.).
- Nie dodawaj nowych kategorii projektow/obszarow wiedzy bez zgody.
- Nie proponuj reindeksu brudnopisu domyslnie (oddzielna decyzja usera).

## Integracje z innymi skillami

- **/aios:sortuj**: skill wywoluje pod-flow `/aios:sortuj` w Kroku 6 dla `_inbox/` (lub sugeruje odpalenie osobno).
- **/aios:koniec-sesji**: po core-update DREAM.md Log jest swiezy - kolejny `/aios:koniec-sesji` moze tylko zapisac aktualny.md.
- **/aios:szukaj**: reindex w Kroku 7 jest warunkiem dzialania `/aios:szukaj --pinecone`.
- **/aios:kontynuuj**: czyta aktualny.md - po core-update aktualny.md jest swiezy.

## Minimum Viable Run

Jesli user chce szybki audyt bez zmian:

```
/aios:core-update --dry-run
```

Dostanie raport w < 60 sekund, decyduje czy uruchomic pelny pipeline.
