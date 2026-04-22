---
name: stworz-projekt
description: Promuje watek z brudnopisu do pelnej struktury projektu w Projekty/kategoria/nazwa. Tworzy README.md, aktywne.md, decyzje.md, Raw/, Wiki/index.md. Aktualizuje me.md i _pamiec/DREAM.md. Triggery - "/aios:stworz-projekt", "zrob z tego projekt", "to jest projekt", "promuj brudnopis do projektu".
---

# stworz-projekt

Skill lokalny zgodny z AIOS v2 (File Over AI). Zastepuje wczesniejsze `/promuj`
i `/nowa-domena` z v1.

## Kiedy uruchamia sie

Recznie, gdy user zdecydowal ze watek z `_brudnopis/` zasluguje na pelna
strukture projektu. NIE uruchamia sie automatycznie.

## Input

- `<nazwa>` - nazwa projektu (kebab-case preferowane, np. `bws-kosztorysantka`)
- `<kategoria>` - jedna z: `Praca`, `Hobby`, `Prywatne`, `Vibe-coding`
- (opcjonalnie) sciezka do brudnopisu zrodlowego, np.
  `_brudnopis/2026-04-20-pomysl-x.md`

Jesli user podal tylko nazwe - pytaj o kategorie. Jesli pominie brudnopis -
sprawdz czy rozmawiamy on-the-fly (wtedy zrob zapis z tej sesji).

## Kroki

### 1. Walidacja

1. Czy `<kategoria>` nalezy do `{Praca, Hobby, Prywatne, Vibe-coding}`?
   Jesli nie - zatrzymaj, pytaj.
2. Czy `Projekty/<kategoria>/<nazwa>/` juz istnieje? Jesli tak - pytaj:
   "zaktualizowac czy zmienic nazwe?"
3. Czy user potwierdzil ze to jest PROJEKT (nie archiwum, nie dead-end)?
   Jesli niejasne - pytaj.

### 2. Tworzenie struktury

Utworz katalog projektu ze standardowym szkieletem v2:

```
Projekty/<kategoria>/<nazwa>/
├── README.md                 ← opis projektu, cele, status
├── aktywne.md                ← co aktualnie robimy
├── decyzje.md                ← log kluczowych decyzji
├── Raw/                      ← surowce projektowe (nie Wiedza/Raw - to cross-project)
└── Wiki/                     ← skompilowana wiedza projektowa
    └── index.md              ← spis stron wiki
```

Dla kategorii `Vibe-coding/` dodatkowo: zasugeruj userowi zeby sklonowal lub
skopiowal kod repo do tego samego folderu (`git clone <url> .` w korzeniu
projektu) - caly projekt zyje razem (kod + notatki + Wiki).

### 3. Wypelnienie README.md

Stworz `README.md` z frontmatter:

```yaml
---
projekt: <nazwa>
kategoria: <kategoria>
status: aktywny
start: YYYY-MM-DD
stack: []  # wypelnij tylko dla Vibe-coding
---
```

Tresc (3-5 sekcji, zwiezle):

- **Cel** - po co robimy (1-3 zdania)
- **Status** - gdzie jestesmy teraz
- **Nastepny krok** - konkretnie co zrobic
- **Kontekst** - linki do relevant stron Wiki, brudnopis zrodlowy
- **Otwarte pytania** - luki, decyzje do podjecia

Bazuj na zawartosci brudnopisu zrodlowego. Dla `Vibe-coding/` pytaj usera o
stack (Next.js? FastAPI? Python?) i cel aplikacji jesli brudnopis tego nie
mowi.

### 4. Wypelnienie aktywne.md i decyzje.md

`aktywne.md` - 1-3 zdania "co teraz robimy w tym projekcie". Ma byc zywe -
aktualizowane co sesje.

`decyzje.md` - pusty log z naglowkiem:

```markdown
# Decyzje projektowe - <nazwa>

> Kluczowe decyzje z uzasadnieniem. Append-only.
```

### 5. Wypelnienie Wiki/index.md

```markdown
# <nazwa> - Wiki

Strony skompilowanej wiedzy projektowej (Karpathy method - Raw/ → Wiki/).

## Strony

(lista sie zapelni po pierwszym `/dodaj-do-wiki` na Raw/ w tym projekcie)
```

### 6. Migracja brudnopisu zrodlowego

Jesli projekt zostal wywolany z brudnopisu:

1. Zmien frontmatter brudnopisu: `status: do-archiwum` lub `archiwum`, dodaj
   `projekt: <nazwa>`.
2. Skopiuj kluczowe fragmenty (decyzje, kontekst, planowanie) do
   `Projekty/<kategoria>/<nazwa>/Raw/brudnopis-YYYY-MM-DD.md`.
3. NIE kasuj brudnopisu - zostaje w `_brudnopis/` jako historia.

### 7. Aktualizacja me.md (BEZPIECZNIK)

Otworz `me.md`, znajdz sekcje "Aktywne projekty". Dodaj wiersz tabeli:

```markdown
| <nazwa> | `Projekty/<kategoria>/<nazwa>/` | aktywny |
```

`me.md` to plik fundamentowy (wg CLAUDE.md) - **pokaz diff i czekaj na "tak"**
przed zapisem.

### 8. Aktualizacja _pamiec/DREAM.md (BEZPIECZNIK)

Otworz `_pamiec/DREAM.md`, znajdz sekcje "Aktywne projekty". Dodaj analogicznie.

`DREAM.md` tez jest plikiem fundamentowym - **pokaz diff i czekaj na "tak"**
przed zapisem.

### 9. Podsumowanie dla usera

Po zakonczeniu:

- Wymien 5-7 nowych plikow/katalogow
- Przypomnij o kolejnym kroku z README.md (sekcja "Nastepny krok")
- Jesli Vibe-coding - przypomnij o sklonowaniu kodu

## Edge cases

- **Pusta kategoria** (pominieta w input) - pytaj przed tworzeniem.
- **Ta sama nazwa w innej kategorii** - ostrzezenie, ale nie blokuj (user
  decyduje).
- **Brudnopis z wieloma watkami** - pytaj ktory watek promujemy.
- **Brak brudnopisu** (rozmowa on-the-fly) - wygeneruj plik
  `_brudnopis/YYYY-MM-DD-<nazwa>-zaczyn.md` z transkryptem rozmowy i uzyj go
  jako zrodlo.

## Plain .md alternatywa

Jesli AI nie ma tego skilla (np. ChatGPT), user moze wskazac zawartosc
`_skille/stworz-projekt.md` z vaultu - identyczna procedura, format plain .md.
