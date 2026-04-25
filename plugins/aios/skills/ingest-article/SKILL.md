---
name: ingest-article
description: >
  Wyciaga tresc artykulu lub strony z podanego URL przez Tavily Extract i zapisuje do Wiedza/OBSZAR/Raw/.
  Triggery: /aios:ingest-article, "wciagnij ten artykul", "zapisz te strone do wiedzy", "dodaj artykul z URL".
---

# AIOS: Ingest article

Masz URL artykulu lub strony. Wyciagasz tresc i zapisujesz do Raw/ - gotowe do `/aios:dodaj-do-wiki`.

## Wymagania

- Tavily MCP (`tavily_extract`) skonfigurowane. Bez niego skill probuje fallbacku Firecrawl, a jak go tez brak - prosi o reczne wklejenie.

## Input

```
/aios:ingest-article <url> [--obszar <nazwa>] [--query <temat>]
```

- `<url>` - adres strony lub artykulu
- `--obszar` - opcjonalnie: folder w `Wiedza/`. Jesli nie podany - pytasz.
- `--query` - opcjonalnie: fraza do rerankingu tresci (pomaga gdy strona ma duzo niezwiazanego contentu)

## Krok 1: Ustal obszar

Tak samo jak w `/aios:research` - jesli nie podano `--obszar`, zapytaj o domene wiedzy.

## Krok 2: Wyciagnij tresc przez Tavily Extract

Wywolaj `tavily_extract` z parametrami:
- `urls`: `[<url>]`
- `format`: `markdown`
- `query`: wartosc `--query` jesli podana, inaczej pusty string
- `extract_depth`: `basic` (domyslnie). Uzyj `advanced` gdy URL to LinkedIn, strona za paywallem lub z tabelami.

## Krok 3: Przygotuj plik Raw/

Sciezka: `Wiedza/<obszar>/Raw/YYYY-MM-DD-<slug>.md`
- `slug` z tytulu strony (jesli Tavily go zwraca) albo z URL, 3-4 slowa kebab-case

Struktura:
```markdown
---
zrodlo: tavily-extract
url: <url>
data: YYYY-MM-DD
status: raw
---

# <Tytul strony>

<tresc wyekstrahowana przez Tavily - bez skracania>
```

## Krok 4: Raport

```
Raw zapisany: Wiedza/<obszar>/Raw/<nazwa-pliku>.md
Zrodlo: <url>
Uruchomic /aios:dodaj-do-wiki?
```

## Fallback: Firecrawl (gdy Tavily zawiedzie)

Jesli `tavily_extract` zwroci pusty wynik, blad lub widac ze strona jest JS-heavy / za paywallem:

1. Sprawdz czy MCP `firecrawl` jest dostepny (`mcp__firecrawl__scrape` lub `firecrawl_scrape`).
2. Jesli tak - wywolaj Firecrawl scrape na tym samym URL, format `markdown`.
3. Zapisz wynik tak samo jak w Krok 3 - tylko zmien frontmatter `zrodlo: firecrawl-scrape`.
4. Jesli Firecrawl tez niedostepny lub zawiedzie - dopiero wtedy popros o reczne wklejenie tresci.

## Obsluga bledow

**Oba extractory zawiodly (Tavily + Firecrawl):** Powiedz wprost "Nie dotarlem do tresci - strona chroniona. Mozesz wkleic tresc recznie, a zapisze jako Raw/."

**Strona w jezyku innym niz polski/angielski:** Zapisz tak jak jest. Nie tlumacz - `/aios:dodaj-do-wiki` zadba o jezyk wiki.

## Czego NIE rob

- Nie streszczaj przed zapisem
- Nie odrzucaj dlugich artykulow - cala tresc idzie do Raw/
