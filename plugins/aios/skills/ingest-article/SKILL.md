---
name: ingest-article
description: >
  Pobiera treść artykułu lub strony z URL i zapisuje do Wiedza/OBSZAR/Raw/ z lokalnym odświeżeniem RAG.
  Triggery: /aios:ingest-article, "wciagnij ten artykul", "zapisz te strone do wiedzy", "dodaj artykul z URL".
---

# AIOS: Ingest article

Masz URL artykulu lub strony. Wyciagasz tresc i zapisujesz do Raw/ - gotowe do `/aios:dodaj-do-wiki`.

## Wymagania

- Odkryj funkcję zwykłego pobrania strony w bieżącym runtime. Gdy HTML jest zaszumiony, użyj dostępnego ekstraktora; Tavily/Firecrawl są opcjonalne. Brak wszystkich możliwości zgłoś i poproś o tekst, bez deklaracji, że sam RAG pobiera internet.

## Input

```
/aios:ingest-article <url> [--obszar <nazwa>] [--query <temat>]
```

- `<url>` - adres strony lub artykulu
- `--obszar` - opcjonalnie: folder w `Wiedza/`. Jesli nie podany - pytasz.
- `--query` - opcjonalnie: fraza do rerankingu tresci (pomaga gdy strona ma duzo niezwiazanego contentu)

## Krok 1: Ustal obszar

Tak samo jak w `/aios:research` - jesli nie podano `--obszar`, zapytaj o domene wiedzy.

## Krok 2: Pobierz treść

Najpierw użyj zwykłego fetch dostępnego w runtime. Gdy wynik nie zawiera treści artykułu, sprawdź capabilities ekstraktorów. Jeśli dostępny jest Tavily Extract, wywołaj go z parametrami:
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
typ_wiedzy: fakt
tematy: [temat-artykulu]
podmioty: []
ai_summary: "Krótkie streszczenie zawartości źródła."
zrodlo: fetch-lub-uzyty-ekstraktor
url: <url>
data: YYYY-MM-DD
status: raw
---

# <Tytul strony>

<treść pobrana przez fetch lub ekstraktor - bez skracania>
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

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
