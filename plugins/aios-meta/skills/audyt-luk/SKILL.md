---
name: audyt-luk
description: >
  Skanuje vault AIOS pod katem luk strukturalnych: brakujace README, puste Raw/, DREAM.md bez delty, aktywne.md bez "Nastepny krok".
  Triggery: /aios-meta:audyt-luk, "sprawdz luki w vaulcie", "co brakuje w vaulcie", "audyt vaulta".
---

# AIOS Meta: Audyt Luk

Skanuj vault i wypisz konkretne luki. Zero filozofii - tylko lista rzeczy do naprawienia.

## Krok 1: Ustal sciezke vaulta

Vault jest w folderze wybranym przez uzytkownika. Sprawdz czy folder roboczy sesji zawiera `me.md` lub charakterystyczne podkatalogi (`_pamiec/`, `Projekty/`, `Wiedza/`). Jesli nie - napisz "Zamontuj vault AIOS jako folder roboczy / cwd" i zakoncz.

Sciezka bazowa: folder w ktorym jest `me.md`.

## Krok 2: Skan - brakujace README

Przejrzyj katalogi:
- `Projekty/` - kazdy podkatalog (rekurencyjnie 2 poziomy)
- `Wiedza/` - kazdy podkatalog

Dla kazdego folderu: sprawdz czy istnieje `README.md`.

Zapisz liste folderow bez README.

## Krok 3: Skan - puste Raw/

Przejrzyj wszystkie `Raw/` w `Wiedza/` i `Projekty/`.

Folder Raw/ uznaj za "pusty" jesli:
- nie ma zadnych plikow .md, LUB
- ostatnia modyfikacja dowolnego pliku jest starsza niz 90 dni

Zapisz liste.

## Krok 4: Skan - DREAM.md bez delty

Przeczytaj `_pamiec/DREAM.md`.

Sprawdz:
- czy plik istnieje
- czy zawiera sekcje aktualizowana w ciagu ostatnich 30 dni (szukaj dat w formacie YYYY-MM-DD w tresci lub frontmatter)
- czy sekcja "Aktywne projekty" lub "Co sie zmienilo" jest wypelniona (nie pusta, nie tylko placeholder)

Jesli ktorys warunek nie spelniony - zapisz jako luke.

## Krok 5: Skan - aktywne.md bez "Nastepny krok"

Przejrzyj pliki `aktywne.md` w:
- `_pamiec/aktualny.md`
- `Projekty/*/aktywne.md` (jesli istnieja)

Sprawdz czy kazdy zawiera niepusta sekcje "Nastepny krok" lub "Next step".

## Krok 6: Raport

Wypisz wyniki w formie:

```
AUDYT VAULTA - [data]

BRAKUJACE README (N):
- Projekty/Kategoria/NazwaProjektu/
- Wiedza/Obszar/
...

PUSTE RAW/ (N):
- Wiedza/Obszar/Raw/  [pusta]
- Projekty/X/Raw/     [ostatni plik: YYYY-MM-DD, 90+ dni temu]
...

DREAM.md:
- OK istnieje i jest aktualne  /  BRAK lub nieaktualne (ostatnia delta: ...)

AKTYWNE.MD BEZ "NASTEPNY KROK" (N):
- _pamiec/aktualny.md
- Projekty/X/aktywne.md
...

LACZNIE: N luk do naprawienia.
```

Jesli brak luk w danej kategorii - napisz `(brak)`.

Nie dawaj rekomendacji ani porad - sam raport. Po raporcie zaproponuj `/aios:core-update` jesli luk jest >5.

## Czego NIE rob

- Nie czytaj zawartosci plikow .md poza tymi wskazanymi w krokach (to skan struktury, nie tresci)
- Nie tworz automatycznie brakujacych plikow - to decyzja usera
- Nie przetwarzaj folderu `_Archiwum/`, `Kosz/`, `node_modules/`, `.git/`
