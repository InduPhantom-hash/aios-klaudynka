---
name: dodaj-do-wiki
description: Przetwarza surowy material (artykul, transkrypt, PDF) z Wiedza Raw/ na strony wiki w Wiedza Wiki/ metoda Karpathy (Collect Compile Query). Triggery - "przerob ten surowiec", "wciagnij do wiki", "dodaj do wiedzy", "/aios:dodaj-do-wiki", "ingest", wskazanie pliku z Raw/ do przerobienia.
---

# dodaj-do-wiki (Karpathy Raw→Wiki)

Przetwarzasz surowy materiał na skompilowaną wiedzę w Wiki. Cel: wyciągnąć esencję i wpiąć ją w istniejącą strukturę - nie tworzyć encyklopedii, tylko atomowe strony gotowe do wyszukiwania.

## Input

User poda ścieżkę pliku z `Wiedza/<temat>/Raw/`, np.:
- `Wiedza/AI/Raw/src-05-nowy-artykul.md`
- Albo samą nazwę - wtedy znajdź go sam w Raw/ odpowiedniej domeny

## Krok 1: Zrozum surowiec

1. Przeczytaj plik w całości
2. Zidentyfikuj temat główny i powiązane pojęcia (3-7)
3. Wyciągnij kluczowe twierdzenia, definicje, liczby, nazwiska
4. Zapisz 1-2 zdaniowe streszczenie (do log.md w kroku 6)

## Krok 2: Zmapuj na istniejące wiki

1. Sprawdź lokalnym RAG według `_skille/rag.md`, czy temat ma już stronę; otwórz źródło. Następnie przeczytaj `Wiedza/<temat>/Wiki/index.md`. Przy braku RAG użyj lokalnych indeksów.
2. Dla każdego pojęcia z kroku 1: czy istnieje strona?
   - **TAK** → kandydat do aktualizacji
   - **NIE** → kandydat na nową stronę
3. Sprawdź czy istnieje `hot.md` - jeśli tak, dopisz "what's new"

## Krok 3: Aktualizuj istniejące strony

Dla każdej strony do aktualizacji:
1. Przeczytaj obecną treść
2. Zidentyfikuj co nowy materiał uzupełnia, koryguje lub poszerza
3. **Pokaż diff userowi i czekaj na "tak"** - bez zgody nie edytujesz Wiki
4. Po "tak": zastosuj edycje, zaktualizuj w frontmatter `aktualizacja: YYYY-MM-DD` i dodaj `src-NN` do `zrodla: [...]`

## Krok 4: Twórz nowe strony

Dla pojęć bez strony w Wiki:
1. Stwórz `Wiedza/<temat>/Wiki/<nazwa-kebab>.md` z frontmatter:
   ```yaml
   ---
   typ_wiedzy: fakt
   tematy: [lista, tagow]
   podmioty: []
   ai_summary: "Krótkie streszczenie treści strony oparte na źródle."
   tags: [lista, tagow]
   aktualizacja: YYYY-MM-DD
   zrodla: [src-NN]
   ---
   ```
2. Struktura: `# Tytuł` → definicja → kluczowe punkty → szczegóły → `## Powiązane` z linkami `[[inna-strona]]`
3. Zasada: jedno pojęcie = jedna strona. Atomowo, nie encyklopedycznie.
4. Nową stronę utwórz w zatwierdzonym zakresie i poinformuj o ścieżce. Przed zmianą istniejącego indeksu lub logu pokaż diff i uzyskaj zgodę na całą partię zmian.

## Krok 5: Zaktualizuj index.md

Dodaj nowe strony alfabetycznie lub tematycznie:
```markdown
- [[nazwa-strony]] - krótki opis jednozdaniowy
```

## Krok 6: Append do log.md

```markdown
## YYYY-MM-DD - src-NN-nazwa

**Streszczenie:** ...
**Zaktualizowane strony:** [[a]], [[b]]
**Nowe strony:** [[c]]
```

## Krok 7: Finalizacja

Jednolinijkowy raport:
```
Przetworzono src-NN. Zaktualizowane: N stron. Nowe: M stron. Lokalny indeks: [wynik].
```

Po zakończeniu zatwierdzonej partii zapisów odśwież lokalny RAG według `_skille/rag.md`. Pinecone wymaga odrębnej, jawnej prośby; nie proponuj go jako zwykłego odświeżenia.

## Zasady których nie łam

- Nie edytuj Wiki bez pokazania diffu i "tak"
- Nie twórz nowych stron dla pojęć już opisanych gdzie indziej - preferuj update
- Nie kasuj starej treści - uzupełniaj i koryguj z notą źródła
- Nie łącz dwóch tematów w jedną stronę na siłę

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
