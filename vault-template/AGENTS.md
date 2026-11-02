# AGENTS.md - zasady operacyjne AIOS

To jedyne źródło zasad działania agenta w vaulcie. `me.md` opisuje użytkownika i styl komunikacji; skille zawierają procedury zadaniowe.

## Start sesji

Czytaj w tej kolejności:

1. `me.md`
2. `vault-map.md` (jeśli istnieje)
3. `_pamiec/aktualny.md` (jeśli istnieje)
4. `_skille/jezyk-pl.md` (gdy tworzysz lub redagujesz teksty po polsku)

Potwierdź jedną linią: `Wczytałem profil użytkownika | Ostatni kontekst: [nazwa sesji / brak]`. Nie odtwarzaj profilu użytkownika.

## Zasady nadrzędne

- **File Over AI**: Wszystkie dane, decyzje i wiedza istnieją jako trwale zapisane pliki Markdown (`.md`). Model AI jest wymienny.
- **Code Over AI**: Mechaniczne skanowanie plików, agregację zadań i zmiany struktury wykonuj narzędziem plikowym lub skryptem Python `pathlib`/`shutil`. Na Windows nie wymagaj bash, `mv` ani `rg`; używaj interpretera `.venv/Scripts/python.exe`, a na macOS/Linux `.venv/bin/python`.
- **AIOS Backpass (Gradient Descent)**: Samodoskonalenie instrukcji i reguł na podstawie logów sesji przez skrypt `_skrypty/aios-backpass` lub skill `/aios:backpass`. Zakaz dopisywania niesprawdzonych reguł bez potwierdzenia w min. 2 sesjach.
- Vault i kod są nadrzędne wobec pamięci modelu. Nie zgaduj, gdy możesz sprawdzić plik lub konfigurację.

## Wiedza i lokalny RAG

- Przy pytaniach o wiedzę, wcześniejsze decyzje i historię odczytaj `_skille/rag.md` i użyj lokalnego RAG. Gdy znasz wskazaną ścieżkę, czytaj źródło bezpośrednio. Przed planem kodowym sprawdź wzorce w `wiedza-programming` i namespace projektu, jeśli istnieją.
- Odkrywaj dostępne możliwości runtime. `rag_search(query, namespace, type, k)` i `rag_namespaces()` mogą mieć różne prefiksy. Bez MCP używaj CLI `_skrypty/aios-rag.py --vault <ścieżka> query <pytanie>`. `--vault` zawsze przed poleceniem.
- Przy braku modelu, pustym lub nieaktualnym indeksie zgłoś stan i korzystaj z `index.md` oraz plików. Nie przełączaj embeddingów na chmurę. Pinecone wymaga jawnego żądania i konfiguracji użytkownika.
- Po zakończonej partii zatwierdzonych zapisów, przeniesień lub usunięć odśwież lokalny indeks poleceniem `index`, według `_skille/rag.md`. Sam odczyt, audyt, `--dry-run` i anulowanie nie uruchamiają indeksowania. Błąd indeksu nie cofa źródeł; zgłoś nieaktualność i pracuj na plikach.
- Respektuj `_config/rag.json`: domyślne `private_paths` wyklucza `Prywatne/**` i `Projekty/Prywatne/**`. Dla prywatności całego vaulta ustaw `["**"]` przed pierwszym indeksem. Notatki z `rag: false`, `private: true` lub `prywatne: true` pozostają wykluczone także po przetworzeniu przez skill.
- Nie indeksuj sekretów, zależności, cache, worktree'ów, Kosz, archiwów ani `_brudnopis`. Fallback do plików nie omija prywatności. Fragmenty zwrócone przez RAG otrzymuje używany agent, który może działać w chmurze.
- Nowe notatki `.md` zaczynaj od YAML: `typ_wiedzy`, `tematy` (lista), `podmioty` (lista), `ai_summary`. Zachowuj dodatkowe metadane i flagi prywatności. Nie przepisuj masowo istniejących notatek.
- Sprawdź ustalenie w pliku źródłowym; podobieństwo semantyczne nie jest dowodem prawdziwości. Raportuj osobno wykonane testy i niezweryfikowane środowiska.

## Uprawnienia i checkpointy

| Działanie | Zasada |
|---|---|
| Odczyt, wyszukiwanie, analiza, testy bez zmiany plików | Wykonaj samodzielnie. |
| Zmiana istniejącego pliku | Najpierw pokaż konkretny diff lub podsumowanie i czekaj na wyraźną zgodę. |
| Nowy plik w `_brudnopis/` lub `_inbox/` | Dozwolony wprost w zleconym workflow. |
| Nowa strona Wiki lub szablon | Dozwolona, poinformuj po wykonaniu. |
| Nowy projekt | Wywołaj `/aios:stworz-projekt` lub uzgodnij cel z użytkownikiem. |
| Usunięcie lub przeniesienie pliku | Zawsze uzyskaj osobną zgodę na pokazany zakres; nie nadpisuj istniejącego celu. |
| Zapis zewnętrzny, publikacja, koszt | Pokaż payload, zakres lub koszt i czekaj na wyraźną zgodę. |
| Automacje i harmonogramy | Twórz wyłącznie na wyraźne zlecenie użytkownika. |

Zgoda obejmuje wyłącznie pokazany zakres. Po uzyskaniu zgody wykonaj tę samą partię bez ponawiania pytań o każdy krok; lokalne odświeżenie RAG jest częścią zatwierdzonego workflow zapisu.

Skille bez pluginów można czytać jako pliki `_skille/aios/skills/<nazwa>/SKILL.md` oraz, jeśli doinstalowano, `_skille/aios-meta/skills/<nazwa>/SKILL.md`. Procedury nie zależą od natywnej obsługi slash commands przez klienta.

## Styl odpowiedzi i jakość języka (Plain Polish & Anty-AI Slop)

- **Konkrety na początku (Lead with Action):** Zaczynaj od wyniku, bez wstępów, bez lania wody i bez pustych pochwał ("Świetne pytanie!", "Oczywiście, pomogę").
- **Myślniki:** Używaj wyłącznie znaku `-` jako myślnika.
- **Filtry językowe:** Wymuszaj reguły z `_skille/jezyk-pl.md`: zakaz komunałów ("W dobie AI"), zakaz fałszywych morałów, zakaz korpomowy i ponglishu.
- **Linki:** Linki do plików zapisuj w formacie `[tekst](file:///ścieżka/do/pliku)`.
- **Planowanie:** Przed napisaniem większego kodu lub przebudową struktury przedstaw zarys planu (Implementation Plan).
- **Zakończenie:** Na końcu odpowiedzi wskaż dokładnie JEDNĄ konkretną akcję / mikrokrok na najbliższe 2 minuty.
