---
name: research
description: >
  Deep research przez Tavily na podany temat - wynik trafia do Wiedza/OBSZAR/Raw/ jako plik gotowy do /aios:dodaj-do-wiki.
  Triggery: /aios:research, "zbadaj temat", "zrob research o", "wciagnij wiedze o TEMAT".
---

# AIOS: Research

Robisz deep research i zapisujesz wynik do vaulta. Jeden skill call = gotowy plik Raw/ do dalszego przetworzenia.

## Wymagania

- Tavily MCP (`tavily_research`) skonfigurowane. Bez niego skill nie zadziala - powiedz userowi: "Tavily MCP nie jest podpiete. Sprawdz konfiguracje (sekcja Stos w me.md). Bez Tavily ten skill nie ma zrodla danych."

## Input

```
/aios:research <temat> [--obszar <nazwa>] [--tryb mini|pro]
```

- `<temat>` - opis tematu do zbadania, moze byc zdanie ("jak dziala RAG w LangChain")
- `--obszar` - opcjonalnie: nazwa folderu w `Wiedza/` (np. AI, Marketing, Finanse). Jesli nie podany - pytasz.
- `--tryb` - opcjonalnie: `mini` (waski temat) / `pro` (szeroki, wiele subtopics). Default: `auto`.

## Krok 1: Ustal obszar

Jesli `--obszar` nie podany: zapytaj "Do ktorej domeny wiedzy: [lista istniejacych folderow w Wiedza/] albo nowa?"

Odczytaj istniejace foldery przez liste `Wiedza/`. Zaproponuj najbardziej pasujacy i czekaj na potwierdzenie lub korekte.

Jesli user wybiera nowy obszar - utworz katalog `Wiedza/<nowy>/Raw/` i `Wiedza/<nowy>/Wiki/` z placeholderami `index.md`.

## Krok 2: Wywolaj Tavily research

Wywolaj `tavily_research` z parametrami:
- `input`: temat z inputu (naturalny opis, nie keyword)
- `model`: wartosc z `--tryb` albo `auto` jesli nie podano

Poczekaj na wynik - moze zajac kilka sekund.

## Krok 3: Przygotuj plik Raw/

Sciezka: `Wiedza/<obszar>/Raw/YYYY-MM-DD-<slug>.md`
- `slug` = 3-4 slowa kebab-case z tematu, np. `rag-langchain-embedding-strategie`
- Uzyj aktualnej daty

Struktura pliku:
```markdown
---
zrodlo: tavily-research
temat: <temat z inputu>
data: YYYY-MM-DD
tryb: mini|pro|auto
status: raw
---

# <Temat - sformatowany jako tytul>

<pelny wynik z tavily_research - bez skracania>
```

Zapisz plik. Nie modyfikuj tresci z Tavily - tylko dodaj frontmatter i tytul.

## Krok 4: Raport

```
Raw zapisany: Wiedza/<obszar>/Raw/<nazwa-pliku>.md
Rozmiar: ~N slow
Uruchomic /aios:dodaj-do-wiki?
```

Jesli user odpowie "tak" lub "tak, dodaj" - od razu wywolaj skill `/aios:dodaj-do-wiki` z tym plikiem.

## Czego NIE rob

- Nie streszczaj wyniku z Tavily przed zapisem - caly wynik idzie do pliku
- Nie tworz od razu strony Wiki - to robi `/aios:dodaj-do-wiki` osobno
- Nie pytaj o potwierdzenie przed zapisem do Raw/ (Raw to brudnopis, bezpieczne)
