# CHANGELOG

Wszystkie zmiany w kolejnych wersjach AIOS-Klaudynki.

Format: [Semantic Versioning](https://semver.org/). Daty: RRRR-MM-DD.

---

## [0.8.0] - 2026-11-04 (release)

### Dodane i Zmienione (Uniwersalny Warsztat Agenta i Nowa Architektura)

- **18 uniwersalnych skilli operacyjnych**:
  - Wszystkie skille skonsolidowane w ramach jednego głównego pluginu `plugins/aios/skills/` bez zaśmiecania bazy reliktami czy opcjonalnymi dodatkami.
  - Ujednolicenie nazewnictwa z prefiksem `aios-` zarówno w katalogach, jak i frontmatterze `SKILL.md` (`name: aios-<nazwa>`) z zachowaniem triggerów `/aios:<nazwa>` i `/aios-<nazwa>`.
  - Zmiana nazwy `aios-feynman` na `aios-wyjasnij` (wyjaśnianie pojęć prostym językiem i diagnoza luk).
  - Usunięcie zdezaktualizowanych reliktów (`aios-zadania`, `aios-dodaj-do-wiki`, `aios-ingest-article`, `aios-core-update`, `aios-pomysl-do-promptu`, `aios-youtube`, `aios-research`) oraz pominięcie skilli opcjonalnych.
  - Ostateczny kanoniczny zestaw 18 skilli: `aios-anonimizacja`, `aios-backpass`, `aios-data-analysis`, `aios-debata`, `aios-doctor`, `aios-dzien`, `aios-grilling`, `aios-init`, `aios-koniec-sesji`, `aios-kontynuuj`, `aios-kustosz`, `aios-research-faktow`, `aios-research-rynkowy`, `aios-sortuj`, `aios-stworz-projekt`, `aios-szukaj`, `aios-weryfikacja`, `aios-wyjasnij`.
- **Wycofanie pluginu `aios-meta`**:
  - Usunięcie przestarzałego pakietu `plugins/aios-meta/`. Zadania higieny, audytu luk i diagnostyki MCP w pełni przejęły `aios-kustosz` oraz `aios-doctor`.
  - Instalator `install.py` zachowuje flagę `--with-meta` jako bezpieczny no-op dla pełnej kompatybilności wstecznej CLI.
- **Inwarianty architektoniczne AIOS w `vault-template/AGENTS.md`**:
  - **Bitemporalność faktów i notatek**: rozdzielenie czasu zapisu (`data_wpisu` ISO-8601) od czasu obowiązywania w świecie realnym (`status: aktywny | obalony | zastąpiony przez [[link]]`).
  - **Zasada Afirmatywnej Pamięci**: pozytywne formułowanie reguł i lekcji, eliminujące błędy negacji w modelach językowych.
  - **Sandwich Prompting**: trójstrefowy podział promptów subagentów (Head 10-15%, Belly 70-80%, Tail 10-15%).
  - **Clean Context Window (`messages: []`)**: faza i podzadania startują w świeżych procesach z czystym oknem kontekstu; stan przekazywany wyłącznie przez pliki dyskowe (File Over AI).
  - **Wayfinder & Frontier Locks**: dekompozycja zadań na Decision Tickets z blokadami zależności `(Blokuje: X)` i `(Zablokowane przez: Y)`.
  - **Higiena pamięci sesji**: ograniczenie bufora `_pamiec/aktualny.md` do twardego limitu <= 3 KB (3072 B).
  - **Preflight Git i limity rozmiaru**: wymuszenie `git -c core.quotepath=off status --porcelain -uall` oraz wykluczenie w `.gitignore` baz wektorowych (`*.lance`), baz danych (`*.db`), modeli ML (`*.tflite`) i plików binarnych powyżej 100 MB.
- **Nowe szablony pamięci i projektów**:
  - `vault-template/_pamiec/aktualny.md`: szablon carry-over sesji z limitem 3 KB i frontmatterem bitemporalnym.
  - `vault-template/_pamiec/lekcje.md`: szablon lekcji inżynieryjnych ze statusem bitemporalnym.
  - `vault-template/_szablony/zadania.md`: zaktualizowany o notację Wayfinder & Frontier.
  - `vault-template/_szablony/decyzja.md`: nagłówek YAML z typem wiedzy i statusem bitemporalnym.
- **Aktualizacja instalatora i manifestów**:
  - `install.py`: podbicie wersji do 0.8.0, instalacja 18 skilli do `_skille/aios/`, prompt poinstalacyjny wskazujący `/aios:init` oraz `_skille/aios/skills/aios-init/SKILL.md`.
  - `.claude-plugin/marketplace.json` i `plugins/aios/.claude-plugin/plugin.json`: wersja 0.8.0, opis 18 uniwersalnych skilli z prefiksem `aios-`, usunięcie wpisu `aios-meta`.
  - `tests/test_install.py`: zaktualizowane asercje dla 18 skilli oraz brak katalogu `aios-meta`.

---

## [0.7.0] - 2026-11-03 (release)

- Lokalny RAG nad Markdown: LanceDB, BGE-M3, CLI i read-only MCP.
- Przyrostowe embeddingi, atomowe przełączanie generacji, zachowanie poprzedniego indeksu przy błędzie i odmowa zwracania nieaktualnych treści.
- Prywatność konfigurowana przed indeksem; wykluczenie stref prywatnych, sekretów, brudnopisów i plików technicznych.
- Instalator Python dla nowych katalogów, własne środowisko i payload MCP bez zmiany ustawień klienta.
- Dostosowanie 14 skilli core i 4 meta; core 0.7.0, meta 0.2.0, spójny marketplace.
- Dokumentacja i testy dla nowych instalacji. Migracja poza zakresem; wyniki środowisk w `docs/odbior-0.7.0.md`.
- Rozszerzenie szablonu vaulta: wdrożenie matrycy zadań Code Over AI (KOD vs LLM) w `AGENTS.md` oraz dodanie szablonu `_szablony/agents-repo.md` dla zewnętrznych repozytoriów programistycznych.

---

## [0.6.0] - 2026-08-23 (release)

### Dodane i Zmienione (AIOS Backpass & Gradient Descent)

- **Nowy silnik i skill `/aios:backpass`**: Samodoskonalenie instrukcji (`AGENTS.md`) i pamięci agentów metodą Gradient Descent na podstawie rzeczywistych transkryptów z dysku (Antigravity, Claude Code, Cursor, Codex, OpenCode, Markdown).
- **Deterministyczny silnik Python (`_skrypty/aios_backpass/`)**:
  - `scanner.py` - skanuje logi sesji w różnych runtime'ach.
  - `distiller.py` - mechaniczne odszumianie logów (redukcja 85-98%) i maskowanie sekretów (API keys, tokeny).
  - `ledger.py` - rejestr luk `gap-ledger.json` z wymogiem corroboracji z co najmniej 2 niezależnych sesji (`min_sessions >= 2`).
  - `budget.py` - Token Budget Guard egzekwujący bilans zero-sum oraz Skill Release Valve (ekstrakcja rzadkich procedur do skilli).
  - `evaluator.py` - generator pakietu ewaluacyjnego model-agnostic (działa z dowolnym modelem) oraz walidator cytatów.
  - `cli.py` + `_skrypty/aios-backpass` - interfejs CLI (`scan`, `distill`, `budget`, `ledger`, `eval`, `apply`).
- **Przenośny skill w vaulcie**: Dodano `_skille/aios-backpass.md` do szablonu vaulta.
- **Aktualizacja manifestu**: Podbito wersję pluginu `aios` do 0.6.0 (14 skilli core).

---

## [0.5.0] - 2026-07-27 (release)

### Dodane i Zmienione (Zasada Code Over AI & File Over AI)

- **Wdrażanie `AGENTS.md` jako SSOT**: Jednolite źródło zasad operacyjnych dla Antigravity, Gemini CLI, Cursor, Codex, OpenHand i Claude Code. `CLAUDE.md` zredukowany do 1-liniowego redirectu.
- **Dodano `bootstrap-prompt.md`**: Uniwersalny prompt startowy dla środowisk AI bez automatycznego ładowania system promptów.
- **Natywny AIOS Task Tracker**: Dodano `_szablony/zadania.md` i obsługę lokalnych `zadania.md` w projektach (100% offline, zero zbędnych opłat i tokenów). Zewnętrzny ClickUp/Linear/Notion jako opcja.
- **Nowy skill Vibe Coding**: `/aios:pomysl-do-promptu` - prowadzi użytkownika od luźnego pomysłu do specyfikacji PRD, makiet i finałowego prompta startowego.
- **Szybki Onboarding `/aios:init --quick`**: Opcja 10-minutowego startu (12 kluczowych pytań) obok pełnego onboardingu `--full`.
- **Zoptymalizowany skill `/aios:dzien`**: Równoległe pobieranie wielu kalendarzy Google (`list_calendars` -> `list_events`) oraz szybkie przeszukiwanie `zadania.md` ripgrepem.
- **Szablony dokumentów (`_szablony/`)**: Utworzono katalog w szablonie vaulta z wzorcami `zadania.md`, `brief-projektu.md`, `decyzja.md`, `index.md`.
- **Usunięcie nieużywanego `Kalendarz/`**: Usunięto pusty folder z szablonu vaulta (zgodnie z "File Over AI: brak ręcznego duplikowania kalendarzy zewnętrznych").

---

## [0.4.0] - 2026-04-25 (beta)

### Dodane - plugin `aios`

- **6 nowych skilli** (plugin `aios` przechodzi z 6 do 12 skilli):
  - `kontynuuj` - wczytuje kontekst poprzedniej sesji z `_pamiec/aktualny.md` + transkrypt przez session_info MCP, otwiera biezaca sesje z gotowym briefingiem.
  - `dzien` - briefing dnia: kalendarz Google + aktywne projekty + sugestia focusu.
  - `core-update` - audyt aktualnosci dokumentow nawigacyjnych AIOS (me.md, vault-map.md, index.md) + update + sprzatanie + reindex Pinecone.
  - `research` - deep research przez Tavily na podany temat, wynik trafia do `Wiedza/<obszar>/Raw/` gotowy do `/aios:dodaj-do-wiki`.
  - `ingest-article` - wyciaga tresc artykulu lub strony z URL przez Tavily Extract i zapisuje do `Wiedza/<obszar>/Raw/`.
  - `zadania` - wyciaga zadania z aktualnej sesji i tworzy je w ClickUp (lista AIOS), z edycja inline przed wysylka.

- **Sekcja E - Blizniaki** w onboardingu `init`:
  - Pytania E10-E13 (opcjonalne, po E8): jakie narzedzia blizniacze uzytkownik ma (Linear, ClickUp, Notion, Airtable, Miro, inne), model synchronizacji (vault = truth, narzedzie = tracker), zakres synchronizacji, preferencje skillowa (auto-check vs. na zadanie).
  - Wygenerowany blok `## Blizniaki` w `me.md` - opis konfiguracji per-narzedzie.
  - Nowy szablon: `docs/szablony/blizniacy.md` - schemat bloku, dwa przyklady, uwagi dla AI.
  - Zaktualizowany `docs/szablony/me-template.md` - blok `## Blizniaki` przed `## Metadane`.
  - `vault-template/me.md` - dodany stub `## Blizniaki` (placeholder).
  - Nowe maksimum: **61 pytan** (57 obligatoryjnych + 4 opcjonalne E10-E13).

### Dodane - plugin `aios-meta` (nowy, opcjonalny)

- Nowy plugin niezalezny od `aios`, skupiony na higienie vaulta i synchronizacji z narzedzniami zewnetrznymi.
- **4 skille:**
  - `audyt-luk` - skanuje vault pod katem luk strukturalnych: brakujace README, puste Raw/, DREAM.md bez delty, aktywne.md bez "Nastepny krok".
  - `mcp-health` - sprawdza ktore MCP serwery z me.md odpowiadaja, a ktore leza; wywoluje lekkie operacje na kazdym i raportuje status.
  - `synchronizuj` - porownuje vault z bliznniakami (ClickUp, Linear, Notion, Airtable) i pokazuje rozjazdy - co jest w vaulcie a nie w blizniaku i odwrotnie.
  - `wizualizuj-vault` - generuje wizualny diagram struktury vaulta inline; opcjonalnie eksportuje do Miro.
- Instalacja opcjonalna (oddzielny krok po instalacji glownego `aios`).

### Zmienione

- `marketplace.json` - dodany wpis dla `aios-meta`, zaktualizowana wersja i opis.
- `CLAUDE.md` (vault-template) - dodana sekcja z 4 skillami `aios-meta` i instrukcja instalacji.
