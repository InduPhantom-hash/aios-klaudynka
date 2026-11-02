---
name: research
description: >
  Deep research przez Tavily na podany temat - wynik trafia do Wiedza/OBSZAR/Raw/ jako plik gotowy do /aios:dodaj-do-wiki.
  Triggery: /aios:research, "zbadaj temat", "zrob research o", "wciagnij wiedze o TEMAT".
---

# AIOS: Research

Robisz deep research i zapisujesz wynik do vaulta. Jeden skill call = gotowy plik Raw/ do dalszego przetworzenia.

## Wymagania

- Najpierw sprawdź istniejącą lokalną wiedzę przez `_skille/rag.md`, potem dostępne możliwości wyszukiwania publicznych źródeł. Tavily Research jest opcjonalne; dostępna wyszukiwarka i fetch pozwalają wykonać research ze źródłami. Bez źródeł zewnętrznych zgłoś ograniczenie i nie udawaj świeżego researchu. Operacja płatna wymaga pokazania zakresu/kosztu i zgody.

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

## Krok 2: Zbierz źródła

Sprawdź lokalny RAG, aby nie dublować istniejącej wiedzy. Dla nowych faktów użyj dostępnej wyszukiwarki i pobierz źródła, preferując źródła pierwotne. Gdy użytkownik wybrał dostępne Tavily Research, wywołaj `tavily_research` z parametrami:
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
typ_wiedzy: fakt
tematy: [temat-researchu]
podmioty: []
ai_summary: "Krótkie streszczenie rzeczywistego wyniku researchu."
zrodlo: uzyte-narzedzie
temat: <temat z inputu>
data: YYYY-MM-DD
tryb: mini|pro|auto
status: raw
---

# <Temat - sformatowany jako tytul>

<wynik z odnośnikami do źródeł; dla Tavily zachowaj pełną treść odpowiedzi>
```

Zapisz plik wraz z odnośnikami i oznaczeniem niepotwierdzonych twierdzeń. Jeżeli zapisujesz odpowiedź Tavily, zachowaj jej treść i dodaj frontmatter oraz tytuł. Nie wysyłaj prywatnych notatek ani sekretów jako zapytania do usługi zewnętrznej.

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

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
