# Instalacja AIOS-Klaudynki 0.8.0

Instrukcja dla agenta instalującego **nowy vault**. Nie migruj ani nie nadpisuj istniejącej instalacji. Najpierw przedstaw docelową ścieżkę i zakres instalacji użytkownikowi. Nie usuwaj zajętego katalogu, aby ponowić instalację.

## 1. Sprawdź środowisko

Ustal system, interpreter Python 3.11+ i dostępność Git. Na Windows użyj natywnego PowerShell i `py -3.13` albo odpowiedniego `python`; na macOS/Linux `python3`. Sprawdź wersję, zamiast zakładać, co oznacza komenda. Nie instaluj globalnych narzędzi z uprawnieniami administratora bez zgody.

LM Studio i BGE-M3 działają lokalnie. Sprawdź [wymagania sprzętowe](https://lmstudio.ai/docs/app/system-requirements). Przy nieobsługiwanym sprzęcie zgłoś brak zgodności lokalnego RAG. Nie zmieniaj go po cichu na usługę chmurową.

Uzgodnij nowy katalog docelowy. Istniejący katalog wymaga wybrania innej lokalizacji; migracja nie należy do tego wydania. Pobierz repo do nowego katalogu roboczego:

```text
git clone https://github.com/InduPhantom-hash/aios-klaudynka.git klaudynka-source
```

## 2. Uruchom instalator

Z katalogu pobranego repo, macOS/Linux:

```sh
python3 install.py --vault "$HOME/Documents/AIOS-Vault" --with-meta
```

Windows, PowerShell:

```powershell
py -3.13 install.py --vault "$HOME/Documents/AIOS-Vault" --with-meta
```

W v0.8.0 wszystkie 18 skilli trafia bezpośrednio do wtyczki `aios`. Flaga `--with-meta` jest zachowana jako bezpieczny no-op dla pełnej kompatybilności wstecznej wywołań. Instalator:

- odmawia zapisu do istniejącego katalogu;
- kopiuje szablon oraz 18 procedur uniwersalnych skilli z prefiksem `aios-`;
- tworzy własne `.venv` i instaluje przypięte zależności RAG;
- przygotowuje `_config/mcp-rag.json`, bez zmiany ustawień klienta AI;
- zwraca `needs_onboarding`, a nie deklarację gotowości całego systemu.

`--no-env` kopiuje tylko pliki i daje status `files_ready`. Jest to wariant diagnostyczny; nie oznacza gotowego RAG. Nie wykorzystuj go do ukrycia błędu instalacji.

Przy przerwanym przygotowaniu zależności zachowaj pliki i wznów bez ponownego kopiowania:

```sh
python3 "/pełna/ścieżka/AIOS-Vault/_skrypty/setup-rag.py" --vault "/pełna/ścieżka/AIOS-Vault"
```

Na Windows użyj właściwego interpretera (`py -3.13`). Skrypt przygotowania nie nadpisze własnych zmian w payloadzie MCP. Przy błędzie pokaż komunikat i kolejny krok; nie czyść katalogów automatycznie.

## 3. Uruchom onboarding i ustal prywatność

Przeczytaj `_skille/aios/skills/aios-init/SKILL.md` w nowym vaulcie i wykonaj `--quick` albo `--full`. Profil `me.md` powstaje dopiero wtedy. Nigdy nie kopiuj profilu autora repozytorium.

Przed pierwszym indeksem ustal strefy prywatności i zapisz je do `_config/rag.json`. Domyślnie `Prywatne/**` i `Projekty/Prywatne/**` pozostają poza indeksem. Dla prywatności całego vaulta użyj `private_paths: ["**"]`. Wykluczenie obszaru oznacza brak RAG dla jego treści; nie omijaj go wyszukiwaniem tekstowym bez wyraźnej zgody.

Nowe dokumenty wiedzy mają frontmatter `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`. Pola starszych dokumentów pozostają obsługiwane. `rag: false`, `private: true` lub `prywatne: true` wyklucza dokument.

## 4. Przygotuj lokalne embeddingi

Zainstaluj LM Studio, pobierz model embeddingowy BGE-M3 i uruchom lokalny serwer. Pobranie modelu wymaga internetu i miejsca na dysku. Nie pobieraj modelu generacyjnego o podobnej nazwie.

Domyślny adres: `http://127.0.0.1:1234/v1`. Sprawdź dostępność modelu przez lokalne `GET /v1/models`. W `_config/rag.json` wpisz rzeczywisty identyfikator BGE-M3 z tej listy (domyślnie `text-embedding-bge-m3`). Model musi zwracać 1024 wymiary. Endpoint pozostaje na loopback; serwer RAG odrzuca zdalne adresy, przekierowania i proxy środowiskowe.

Zasady endpointu opisuje [dokumentacja embeddingów LM Studio](https://lmstudio.ai/docs/developer/openai-compat/embeddings). Nie zmieniaj konfiguracji działającego prywatnego Huba użytkownika, aby uruchomić Klaudynkę.

## 5. Zbuduj indeks i sprawdź wynik

Z katalogu vaulta, macOS/Linux:

```sh
.venv/bin/python _skrypty/aios-rag.py --vault . index
.venv/bin/python _skrypty/aios-rag.py --vault . status
.venv/bin/python _skrypty/aios-rag.py --vault . query "Jakie mam projekty?" --k 3
```

Windows, PowerShell:

```powershell
& .venv/Scripts/python.exe _skrypty/aios-rag.py --vault . index
& .venv/Scripts/python.exe _skrypty/aios-rag.py --vault . status
& .venv/Scripts/python.exe _skrypty/aios-rag.py --vault . query "Jakie mam projekty?" --k 3
```

Odczytaj źródło wskazane w wyniku. Jeśli nie ma dozwolonych dokumentów, pusty indeks jest poprawny, ale nie dowodzi działania modelu. Po zgodzie użytkownika możesz utworzyć neutralną notatkę testową w dozwolonej strefie i wykonać zapytanie. Nie deklaruj gotowości modelu na podstawie samego `status` lub `namespaces`, bo nie korzystają z embeddingów.

## 6. Wybierz MCP albo CLI

W obu wariantach działa ten sam lokalny silnik. Sprawdź capabilities bieżącego klienta AI.

- **MCP:** pokaż zawartość `_config/mcp-rag.json` i diff względem ustawień klienta. Po zgodzie scal tylko wpis `rag-vault`, zachowując pozostałe serwery. Dla klienta używającego innego formatu przenieś `command` i listę `args` zgodnie z jego dokumentacją. Nie zakładaj jednego formatu dla Codex, Claude, Cursor czy Gemini. Przetestuj `rag_namespaces` i `rag_search` po ponownym podłączeniu.
- **CLI:** agent wywołuje komendy z kroku 5. Slash commands nie są wymagane; procedury odczytuje z `_skille/aios/skills/<nazwa>/SKILL.md`.

Jeśli użytkownik chce natywny plugin Claude Code, repo zawiera marketplace `.claude-plugin/marketplace.json` i pluginy w `plugins/`. Skorzystaj z mechanizmu instalacji pluginów dostępnego w danej wersji klienta. Podłączenie pluginu nie zastępuje instalacji silnika, modelu ani indeksowania. Status ścieżek agentowych podaje [raport odbioru](docs/odbior-0.7.0.md).

## 7. Raport gotowości

Oddziel: pliki, środowisko Python, profil, prywatność, model, indeks, zapytanie ze źródłem oraz MCP/CLI. Wymień sprawdzone i niesprawdzone elementy. Przy braku modelu zachowaj pliki i udostępnij pracę bez RAG, bez automatycznego Pinecone.

Po zmianach plików stosuj wspólną procedurę `_skille/rag.md`. Nie twórz watchera, usługi startowej ani harmonogramu. Nie przenoś `.venv` i indeksu między komputerami; na nowej maszynie przygotuj środowisko i odbuduj indeks.

Szczegóły poleceń, prywatności i naprawy: [docs/rag.md](docs/rag.md). Weryfikacja systemów: [raport odbioru](docs/odbior-0.7.0.md). Starsza paczka `aios-v0.3.0.plugin` jest artefaktem historycznym; instalator 0.8.0 korzysta z aktualnych katalogów źródłowych.
