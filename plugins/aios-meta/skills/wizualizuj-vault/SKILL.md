---
name: wizualizuj-vault
description: >
  Generuje wizualny diagram struktury vaulta AIOS - mapa katalogow, projektow i ich statusow. Opcjonalnie eksportuje do Miro (jesli MCP dostepne).
  Triggery: /aios-meta:wizualizuj-vault, "pokaz strukture vaulta", "diagram vaulta", "mapa vaulta".
---

# AIOS Meta: Wizualizuj Vault

Wygeneruj diagram struktury vaulta. Dwa tryby: inline (widget w czacie) lub eksport do Miro.

## Input

```
/aios-meta:wizualizuj-vault [--tryb inline|miro] [--glebokos 1|2|3]
```

- `--tryb`: `inline` (default) = SVG w czacie; `miro` = tworzy diagram w Miro przez MCP (wymaga Miro MCP w runtime)
- `--glebokos`: jak gleboko wchodzic w strukture katalogow (default: 2)

## Krok 1: Odczytaj strukture vaulta

Ustal sciezke bazowa vaulta (tam gdzie `me.md`).

Przeczytaj strukture katalogow do glebokosci `--glebokos`. Interesuja Cie:

**Poziom 1 (zawsze):**
- `Projekty/` - wszystkie podkatalogi
- `Wiedza/` - wszystkie podkatalogi (obszary wiedzy)
- `_pamiec/` - kluczowe pliki (aktualny.md, DREAM.md)
- `_inbox/` - liczba plikow
- `_brudnopis/` - liczba plikow

**Poziom 2 (jesli `--glebokos >= 2`):**
- Dla kazdego projektu: status z `aktywne.md` (szukaj pola `status:` w frontmatter) lub "brak"
- Dla kazdej kategorii: czy ma podkatalogi (aktywna vs pusta)

**Poziom 3 (jesli `--glebokos >= 3`):**
- Dla kazdego projektu: lista plikow w `Raw/` (ile surowca czeka)

## Krok 2a: Tryb inline - generuj SVG

Utworz diagram jako SVG (przez widget rendering jesli runtime to wspiera, inaczej ASCII tree).

Struktura wizualna:
- Centralny wezel: "AIOS Vault"
- Galezie pierwszego poziomu: Projekty, Wiedza, _pamiec, _inbox, _brudnopis
- Galezie drugiego poziomu: podkatalogi z nazwami
- Kolor wezla projektu wedlug statusu:
  - Aktywny (status: aktywny/active) - zielony
  - Wstrzymany / brak aktywne.md - szary
  - Archiwum - przyciemniony

Uzyj hierarchicznego ukladu (tree layout), nie kolowego. Czcionka czytelna, bez ozdobnikow.

## Krok 2b: Tryb miro - eksport do Miro

Wymaga Miro MCP. Jesli niedostepne - powiedz userowi "Miro MCP nie podpiete, robie inline" i przejdz do 2a.

Wywolaj `diagram_create` (lub odpowiednik z Miro MCP runtime'u) z wezlami odpowiadajacymi strukturze vaulta. Tytul diagramu: `AIOS Vault - [data]`.

Po utworzeniu: podaj URL do diagramu. Zapisz URL do `_pamiec/miro-diagrams.md` (stworz plik jesli nie istnieje, dopisz linie `[YYYY-MM-DD] Struktura vaulta: <url>`).

## Krok 3: Podsumowanie tekstowe

Po diagramie (obydwa tryby) wypisz krotkie podsumowanie:

```
Vault: [sciezka bazowa]
Projekty aktywne: N  |  wstrzymane: M
Wiedza: N obszarow
_inbox: N plikow czeka
_brudnopis: N plikow
```

## Czego NIE rob

- Nie wczytuj tresci plikow - tylko strukture katalogow i frontmatter statusu
- Nie tworz diagramu jesli vault nie jest zamontowany jako folder roboczy
- Przy trybie miro: nie tworz diagramu bez potwierdzenia (operacja tworzy zasob zewnetrzny)
