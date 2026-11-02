---
name: core-update
description: >
  Porównuje rzeczywisty vault z me.md, mapą, indeksami i pamięcią, pokazuje diff i po zgodzie aktualizuje pliki oraz lokalny RAG.
  Triggery: /aios:core-update, zaktualizuj nawigację, audyt AIOS, sprawdź czy wszystko aktualne.
---

# Aktualizacja nawigacji AIOS

Vault i pliki źródłowe są źródłem prawdy. Czytaj `_skille/rag.md`. Procedura: odczyt -> raport i konkretny diff -> zgoda -> zmiany -> lokalny indeks. Nie zmieniaj profilu ani instrukcji tylko dlatego, że raport wskazał rozbieżność.

## Argumenty

- Bez argumentów: pełny audyt nawigacji.
- `--dry-run`: tylko odczyt i raport; bez zapisu, porządkowania, `index` i `rebuild`.
- `--skip-reindex`: po zatwierdzonej aktualizacji pomiń indeksowanie i zgłoś, że indeks może być nieaktualny.
- `--tylko <plik>`: zawęź audyt do wskazanego dokumentu.

## 1. Ustal stan

Odczytaj katalogi projektów i wiedzy oraz potrzebne metadane plików przez dostępne narzędzie plikowe lub Python `pathlib`. Nie wymagaj bash, `mv` ani `rg`; nie podążaj za symlinkami. Archiwa i Kosz sprawdzaj wyłącznie jako strukturę potrzebną do porządkowania, bez dodawania ich do RAG.

Porównaj fakty z `me.md`, `vault-map.md`, `Projekty/index.md`, indeksami kategorii, `Wiedza/index.md`, indeksami Wiki, `_pamiec/DREAM.md` i `_pamiec/aktualny.md`. Brak pliku podstawowego zgłoś; nie buduj go bez zgody. Brudnopisy bez opisu oznacz jako wymagające ręcznej konsolidacji, bez zgadywania treści.

## 2. Pokaż raport i diff

Dla każdej rozbieżności wskaż dokument, stan na dysku, proponowaną poprawkę i priorytet: krytyczne błędne fakty, ważne braki nawigacji albo drobne linki/daty. Przy konflikcie źródeł pokaż oba i poproś o rozstrzygnięcie.

Oddzielnie wypisz propozycje przeniesienia do Kosz, sortowania `_inbox` i zmian nazw. Pokaż konkretny diff istniejących dokumentów. Zapytaj o zakres: wszystkie pokazane zmiany, wybrane pliki, sam lokalny indeks albo anulowanie. Dla `--dry-run` zakończ tutaj.

## 3. Wykonaj zatwierdzone zmiany

1. Popraw zaakceptowane wpisy w `me.md`, bez zmiany hard rules poza jawną zgodą.
2. Uaktualnij mapę i indeksy projektów oraz wiedzy.
3. W `DREAM.md` dopisuj do historii decyzji/sesji, zachowując poprzednie wpisy. Bieżące tabele można poprawiać w zatwierdzonym zakresie.
4. Zapisz bieżący stan w `aktualny.md`. Zachowaj metadane i flagi prywatności.
5. Nowe pliki `.md` opatrz YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`.

Przeniesienie i usunięcie wymagają osobnego potwierdzenia zakresu. Wykonuj mechaniczne operacje przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez nadpisywania istniejącego celu. Nie usuwaj zawartości Kosz automatycznie. Sortowanie może wywołać `/aios:sortuj`.

## 4. Odśwież lokalny RAG

Po zatwierdzonych zapisach/przeniesieniach zastosuj `_skille/rag.md`: uruchom raz `index` przez interpreter `.venv` i `_skrypty/aios-rag.py --vault <ścieżka> index`. Narzędzia MCP są odczytowe; nie oczekuj od nich aktualizacji. `index` rozpoznaje dodane, zmienione, przeniesione i usunięte źródła.

Nie wykonuj pełnego `rebuild` jako zwykłego odświeżenia. Przy błędzie zachowaj źródła i ostatni poprawny indeks, zgłoś nieaktualność oraz fallback do plików. Przy `--skip-reindex` lub anulowaniu nie uruchamiaj indeksowania.

Pinecone nie uczestniczy w tej procedurze. Zewnętrzny upload wymaga odrębnej, jawnej prośby użytkownika, pokazania payloadu i zgody.

## 5. Raport

Podaj liczbę zmienionych i przeniesionych plików, wynik lokalnego `index` albo informację o pominięciu/błędzie oraz jeden następny krok. Nie twórz commitów, nie publikuj i nie dodawaj automacji.
