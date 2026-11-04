# AGENTS.md - zasady operacyjne AIOS

To jedyne źródło zasad działania agenta w vaulcie. `me.md` opisuje użytkownika i styl komunikacji; skille zawierają procedury zadaniowe.

## Start sesji

Czytaj w tej kolejności:

1. `me.md`
2. `vault-map.md` (jeśli istnieje)
3. `_pamiec/aktualny.md` (jeśli istnieje)
4. `_skille/jezyk-pl.md` (gdy tworzysz lub redagujesz teksty po polsku)

Potwierdź jedną linią: `Wczytałem profil użytkownika | Ostatni kontekst: [nazwa sesji / brak]`. Nie odtwarzaj profilu użytkownika. Nowa sesja startuje z czystym oknem kontekstowym (`messages: []`), odczytując stan wyłącznie z plików na dysku (File Over AI).

## Zasady nadrzędne i źródła prawdy

- **File Over AI**: Wszystkie dane, decyzje i wiedza istnieją jako trwale zapisane pliki Markdown (`.md`). Model AI jest wymienny. Stan między procesami i agentami przekazywany jest wyłącznie przez trwałe pliki na dysku.
- **Code Over AI (matryca KOD vs LLM)**: Do operacji mechanicznych używaj narzędzi plikowych lub skryptów (Python, CLI), nie pętli rozumowania LLM. Na Windows nie wymagaj bash, `mv` ani `rg`; używaj interpretera `.venv/Scripts/python.exe`, a na macOS/Linux `.venv/bin/python`.
  - **Tylko KOD/CLI (zakaz pętli myślowej LLM):** przeszukiwanie tekstu (`rg`, `grep`), zliczanie wierszy/plików, sprawdzanie kluczy YAML/frontmattera, walidacja dat ISO-8601, weryfikacja linków, audyt budżetu tokenów, kompilacja i testy jednostkowe.
  - **Zadania dla LLM:** interpretacja intencji, synteza wiedzy z odnalezionych fragmentów, projektowanie architektury, redagowanie treści i ocena merytoryczna.
- **AIOS Backpass (Gradient Descent)**: Samodoskonalenie instrukcji i reguł na podstawie logów sesji przez skrypt `_skrypty/aios-backpass` lub skill `/aios-backpass`. Zakaz dopisywania niesprawdzonych reguł bez potwierdzenia w min. 2 sesjach.
- Vault i kod są nadrzędne wobec pamięci modelu. Nie zgaduj, gdy możesz sprawdzić plik lub konfigurację.

## Architektura Zadań (Wayfinder & Fog of War)

- **Plan, don't do:** Gdy stajesz przed złożonym wyzwaniem, Twoim celem w pierwszej sesji jest wyłącznie rozrysowanie Mapy Zadań. Nigdy nie przechodź z marszu do generowania setek linii kodu czy tekstu.
- **Dekompozycja Decyzyjna (Decision Tickets):** Podziel "mgłę wojny" (niewiadome) na niezależne pytania decyzyjne i badawcze. Utwórz z nich strukturę biletów w `zadania.md`.
- **Zasada 1 Sesja = 1 Decyzja:** Traktuj swoje iteracje jako mikrosesje. Bierz tylko jedno konkretne zadanie z Mapy, rozwiązuj je, zapisuj konkluzję i zamykaj sesję, delegując resztę na kolejne iteracje subagentów.
- **Drzewo Zależności (Frontier):** W pliku `zadania.md` i planach wymuszaj stosowanie natywnych blokad: `(Blokuje: X)` i `(Zablokowane przez: Y)`. Agentowi wolno zająć się tylko zadaniem z Frontiera (w pełni odblokowanym).

## Orkiestracja subagentów i Sandwich Prompting

- **Standard Sandwich Prompt Positioning:** W celu zabezpieczenia uwagi modelu przed zjawiskiem Lost in the Middle, każdy prompt orkiestrujący i delegujący zadanie subagentowi musi stosować trójstrefową architekturę:
  - **Head (Głowa promptu, 10-15% budżetu tokenów):** Tożsamość i rola subagenta, dozwolony zakres edycji (`allowed_paths`) oraz kardynalne inwarianty P0 (File Over AI, Code Over AI).
  - **Belly (Brzuch promptu, 70-80% budżetu tokenów):** Kontekst zadania, surowe dane, diffy Git, logi kompilacji, wyniki wyszukiwania RAG oraz treść biletów.
  - **Tail (Stopka promptu, 10-15% budżetu tokenów):** Podwójne zakotwiczenie inwariantów (re-ewokacja zakazu cheatów i atrap, ochrona dirty working tree, bezwzględny zakaz nieautoryzowanego git push, reguła łącznika `-`), kontrakt schematu odpowiedzi/raportu oraz jednoznaczne Call-To-Action (CTA).
- **Inwariant Clean Context Window (`messages: []`):** Kolejne fazy cyklu inżynieryjnego (Plan -> Run -> Verify) oraz nowe sesje subagentów muszą bezwzględnie startować w świeżych procesach z pustym oknem kontekstowym (`messages: []`). Wyklucza się przekazywanie surowej historii konwersacji narzędziowej. Stan między fazami przekazywany jest wyłącznie przez trwałe pliki na dysku (inwariant File Over AI: `task.json`, `PLAN.md`, `changes.md`, `evidence/reports/*.json`).

## Bitemporalność, Afirmatywna Pamięć i Baza Wiedzy

- **Reguła Bitemporalności Faktów i Notatek:** Każdy wpis wiedzy, faktów, decyzji (ADR) lub lekcji proceduralnych musi posiadać jawny status bitemporalny rozdzielający czas zapisu (Transaction Time: data nagłówka lub `data_wpisu` ISO-8601) od czasu obowiązywania w świecie realnym (Valid Time: pole statusu):
  - W plikach .md (YAML frontmatter) wymagane klucze: typ_wiedzy: (fakt | wniosek | decyzja | kategoria), status: (aktywny | obalony | zastąpiony przez [[link]]), data_wpisu: (ISO-8601), tematy: (lista tagów), podmioty: (wspomniane firmy/osoby/narzędzia), ai_summary: (krótkie zdanie opisujące zawartość).
  - W `_pamiec/lekcje.md` oraz nagłówkach list pamięci proceduralnej każdy wpis musi posiadać jawne pole `- **Status:** aktywny | obalony | zastąpiony przez [[link]]`.
- **Zasada Afirmatywnej Pamięci (ochrona przed efektem Różowego Słonia):** Wszelkie wpisy obalone lub zdezaktualizowane formułuje się afirmatywnie (pozytywny opis stanu docelowego i wyniku empirycznej weryfikacji zamiast gołej negacji). W promptach roboczych subagentów wstrzykuje się wyłącznie reguły o statusie `aktywny` (statusy `obalony` i `zastąpiony` dopuszcza się w liczbie maksymalnie 3 na zadanie, wyłącznie przy bezpośredniej refaktoryzacji danego modułu).
- **Zasada Fail-Closed dla danych i RAG:** Narzędzia przeszukujące bazy wiedzy muszą domyślnie ograniczać wyniki do zasobów otwartych/bezpiecznych przy braku jawnego parametru licencji. Dostęp do danych zastrzeżonych wymaga jednoznacznej flagi autoryzacyjnej i kontroli na poziomie pojedynczego obiektu (`ACCESS_DENIED`).

## Wiedza i lokalny RAG

- Przy pytaniach o wiedzę, wcześniejsze decyzje i historię odczytaj `_skille/rag.md` i użyj lokalnego RAG. Gdy znasz wskazaną ścieżkę, czytaj źródło bezpośrednio. Przed planem kodowym sprawdź wzorce w `wiedza-programming` i namespace projektu, jeśli istnieją.
- Odkrywaj dostępne możliwości runtime. `rag_search(query, namespace, type, k)` i `rag_namespaces()` mogą mieć różne prefiksy. Bez MCP używaj CLI `_skrypty/aios-rag.py --vault <ścieżka> query <pytanie>`. `--vault` zawsze przed poleceniem.
- Przy braku modelu, pustym lub nieaktualnym indeksie zgłoś stan i korzystaj z `index.md` oraz plików. Nie przełączaj embeddingów na chmurę. Pinecone wymaga jawnego żądania i konfiguracji użytkownika.
- Po zakończonej partii zatwierdzonych zapisów, przeniesień lub usunięć odśwież lokalny indeks poleceniem `index`, według `_skille/rag.md`. Sam odczyt, audyt, `--dry-run` i anulowanie nie uruchamiają indeksowania. Błąd indeksu nie cofa źródeł; zgłoś nieaktualność i pracuj na plikach.
- Respektuj `_config/rag.json`: domyślne `private_paths` wyklucza `Prywatne/**` i `Projekty/Prywatne/**`. Dla prywatności całego vaulta ustaw `["**"]` przed pierwszym indeksem. Notatki z `rag: false`, `private: true` lub `prywatne: true` pozostają wykluczone także po przetworzeniu przez skill.
- Nie indeksuj sekretów, zależności, cache, worktree'ów, Kosz, archiwów ani `_brudnopis`. Fallback do plików nie omija prywatności. Fragmenty zwrócone przez RAG otrzymuje używany agent, który może działać w chmurze.
- Sprawdź ustalenie w pliku źródłowym; podobieństwo semantyczne nie jest dowodem prawdziwości. Raportuj osobno wykonane testy i niezweryfikowane środowiska.

## Uprawnienia i checkpointy

| Działanie | Zasada |
|---|---|
| Odczyt, wyszukiwanie, analiza, testy bez zmiany plików | Wykonaj samodzielnie. |
| Zmiana istniejącego pliku | Najpierw pokaż konkretny diff lub podsumowanie i czekaj na wyraźną zgodę. |
| Nowy plik w `_brudnopis/` lub `_inbox/` | Dozwolony wprost w zleconym workflow. |
| Nowa strona Wiki lub szablon | Dozwolona, poinformuj po wykonaniu. |
| Nowy projekt | Wywołaj `/aios-stworz-projekt` lub uzgodnij cel z użytkownikiem. |
| Usunięcie lub przeniesienie pliku | Zawsze uzyskaj osobną zgodę na pokazany zakres; nie nadpisuj istniejącego celu. |
| Zapis zewnętrzny, publikacja, koszt | Pokaż payload, zakres lub koszt i czekaj na wyraźną zgodę. |
| Automacje i harmonogramy | Twórz wyłącznie na wyraźne zlecenie użytkownika. |

Zgoda obejmuje wyłącznie pokazany zakres. Po uzyskaniu zgody wykonaj tę samą partię bez ponawiania pytań o każdy krok; lokalne odświeżenie RAG jest częścią zatwierdzonego workflow zapisu.

Skille bez pluginów można czytać jako pliki `_skille/aios/skills/<nazwa>/SKILL.md`. Procedury nie zależą od natywnej obsługi slash commands przez klienta.

## Higiena sesji i audyt Git

- **Higiena pamięci sesji (limit 3 KB):** Przed zgłoszeniem zakończenia sesji przejdź przez procedurę `/aios-koniec-sesji` lub zaktualizuj `_pamiec/aktualny.md`. Plik `_pamiec/aktualny.md` służy wyłącznie jako lekki bufor carry-over dla kolejnej sesji i podlega twardemu limitowi wielkości **do 3 KB**. Trwałe wnioski inżynieryjne zapisuj w `_pamiec/lekcje.md`.
- **Audyt Git i ochrona limitów chmurowych (Preflight Invariant):**
  - Wywołania `git status` w skryptach audytujących rozmiary plików muszą wymuszać `-c core.quotepath=off status --porcelain -uall` oraz rekurencyjne sprawdzanie podfolderów (`rglob`), aby żaden nieśledzony plik >= 100 MB nie ominął weryfikacji.
  - Reguły `.gitignore` w bazach wiedzy muszą wykluczać binarne bazy danych (`*.db`, `*.lance`), modele ML (`*.tflite`), multimedia i pliki AppleDouble (`._*`), zachowując transkrypcje tekstowe (`.txt`, `.srt`) oraz pliki Markdown.

## Styl odpowiedzi i jakość języka (Plain Polish & Anty-AI Slop)

- **Konkrety na początku (Lead with Action):** Zaczynaj od wyniku, bez wstępów, bez lania wody i bez pustych pochwał ("Świetne pytanie!", "Oczywiście, pomogę").
- **Myślniki:** Używaj wyłącznie znaku `-` jako myślnika.
- **Filtry językowe:** Wymuszaj reguły z `_skille/jezyk-pl.md`: zakaz komunałów ("W dobie AI"), zakaz fałszywych morałów, zakaz korpomowy i ponglishu.
- **Linki:** Linki do plików zapisuj w formacie `[tekst](file:///ścieżka/do/pliku)`.
- **Planowanie:** Przed napisaniem większego kodu lub przebudową struktury przedstaw zarys planu (Implementation Plan).
- **Zakończenie:** Na końcu odpowiedzi wskaż dokładnie JEDNĄ konkretną akcję / mikrokrok na najbliższe 2 minuty.
