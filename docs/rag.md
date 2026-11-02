---
typ_wiedzy: fakt
tematy: [klaudynka, rag, prywatnosc]
podmioty: [LanceDB, BGE-M3, LM Studio, MCP]
ai_summary: "Obsługa lokalnego RAG: konfiguracja, komendy, granice prywatności i odzyskiwanie indeksu."
---

# Lokalny RAG

Markdown pozostaje źródłem prawdy. LanceDB przechowuje pochodny indeks, a lokalny BGE-M3 przygotowuje wektory o 1024 wymiarach. Agent otrzymuje fragmenty, nie gotową odpowiedź wygenerowaną przez drugi model. Przed uznaniem ustalenia odczytuje plik źródłowy.

## Konfiguracja

Plik `_config/rag.json` jest wspólny dla CLI i MCP. Ścieżka `store` odnosi się do korzenia vaulta, nie bieżącego katalogu terminala. Argument `--vault` wskazuje korzeń jawnie; bez niego runner wybiera vault, w którym sam się znajduje.

```json
{
  "schema": 1,
  "store": ".aios/rag",
  "endpoint": "http://127.0.0.1:1234/v1",
  "model": "text-embedding-bge-m3",
  "timeout": 60,
  "exclude": ["Klienci/**"],
  "private_paths": ["Prywatne/**", "Projekty/Prywatne/**"]
}
```

`exclude` i `private_paths` to wzorce ścieżek z separatorami `/`, względem vaulta. `**` wyklucza wszystko. Domyślne prywatne strefy można zmieniać wyłącznie zgodnie z granicami ustalonymi przez użytkownika. Usunięcie wzorca może dopuścić treść do indeksu i później do kontekstu agenta.

Endpoint musi korzystać z HTTP i loopback (`localhost`, `127.0.0.1`, `::1`). Kod nie używa proxy z otoczenia i odrzuca przekierowania. Nie obsługujemy w tym wydaniu embeddingów w chmurze ani na innej maszynie LAN. Model musi być wariantem BGE-M3; identyfikator z lokalnego `/v1/models` wpisz w `model`. Zmiana identyfikatora modelu lub przeniesienie vaulta wymaga `rebuild`.

Instalator nie nadpisuje konfiguracji klienta AI. `_config/mcp-rag.json` zawiera payload z absolutnym interpreterem i argumentami. Przed scaleniem z ustawieniami klienta pokaż diff i uzyskaj zgodę. Format opakowania konfiguracji może się różnić między klientami.

## Komendy i wyniki

Przykłady POSIX z katalogu vaulta. Na Windows zastąp `.venv/bin/python` przez `.venv/Scripts/python.exe`; w PowerShell wywołaj interpreter operatorem `&`.

```sh
.venv/bin/python _skrypty/aios-rag.py --vault . index
.venv/bin/python _skrypty/aios-rag.py --vault . rebuild
.venv/bin/python _skrypty/aios-rag.py --vault . query "Co ustaliliśmy o projekcie?" --k 5
.venv/bin/python _skrypty/aios-rag.py --vault . query "Testowanie" --namespace wiedza-programming --type fakt
.venv/bin/python _skrypty/aios-rag.py --vault . namespaces
.venv/bin/python _skrypty/aios-rag.py --vault . status
.venv/bin/python _skrypty/aios-rag.py --vault . mcp
```

- `index` wylicza hashe treści i przygotowuje embeddingi wyłącznie dla zmienionych dokumentów. Przeniesienie i usunięcie pliku usuwa jego stare fragmenty. Brak zmian nie wywołuje embeddera.
- `rebuild` tworzy pełny indeks od nowa, także po uszkodzeniu magazynu. Nie zmienia dokumentów źródłowych.
- `query` przyjmuje 1-16000 znaków, `k` od 1 do 50, opcjonalnie dokładny filtr `namespace` i `type`. Zwraca `hits` z `path`, `source_path`, `heading`, `title`, `namespace`, `type`, `text` i `score` podobieństwa cosinusowego. Wynik nie jest prawdopodobieństwem poprawności odpowiedzi.
- `namespaces` pokazuje obszary i liczby fragmentów bez modelu. `Wiedza/<obszar>` daje `wiedza-<obszar>`, a `Projekty/<kategoria>/<projekt>` daje `projekty-<projekt>`.
- `status` sprawdza magazyn i aktualność dokumentów, ale nie gotowość modelu. Stany: `not_indexed`, `ready`, `stale`; błędy dają `error` i niezerowy kod wyjścia.
- `mcp` uruchamia wyłącznie read-only narzędzia `rag_search(query, namespace, type, k)` oraz `rag_namespaces()`. Aktualizację wykonuje jawnie CLI po zatwierdzonym zapisie źródeł. MCP czyta konfigurację przy każdym wywołaniu.

CLI wypisuje JSON. MCP może przekazywać ten sam wynik w bloku tekstowym JSON lub jako structured content, zgodnie z SDK. Błędy CLI zwracają kod 1; błędne argumenty parsera kod 2. Pusta lista trafień jest poprawnym wynikiem.

## Dokumenty i prywatność

Nowy frontmatter: `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`. RAG obsługuje również starsze `type`, `title`, `tytul`, `projekt`, a brak metadanych nie blokuje zwykłej notatki. `rag: false`, `private: true` lub `prywatne: true` wyklucza dokument. Nieprawidłowy YAML zatrzymuje aktualizację, zachowując ostatni działający indeks.

Kod dzieli dokument po nagłówkach, zachowuje bloki kodu i tabele, a długie akapity dzieli na fragmenty. Bardzo duży niepodzielny blok kodu lub tabela może przekroczyć limit modelu; podziel taki dokument źródłowy za zgodą autora, jeśli embedder odmówi przetworzenia.

Domyślnie poza indeksem pozostają katalogi ukryte, zależności, cache, worktree'y, `_brudnopis`, archiwa, Kosz, `_config`, `_skrypty`, `_skille`, typowe katalogi sekretów i nazwy plików z hasłami. Kod nie podąża za symlinkami. Własne ścieżki dodaj do konfiguracji. **To reguły ścieżek i metadanych, nie skaner wszystkich danych wrażliwych.**

Zapytanie sprawdza hashe źródeł przed wyszukaniem. Przy nieaktualności odmawia zwracania fragmentów, zamiast ujawniać wcześniej publiczną, a obecnie wykluczoną treść. Zmiana wykluczeń wymaga `index`. Fallback odczytu plików nadal podlega granicom prywatności; nie wolno użyć go do obejścia wykluczeń.

Indeks może zawierać pełne fragmenty notatek i wcześniejszą generację. Nie synchronizuj `.aios/`, `.venv/` ani wag modeli do repo. `.gitignore` nie wyłącza synchronizacji Finder/iCloud/Drive; ustaw wykluczenia także w narzędziu synchronizacji lub wskaż `store` poza synchronizowanym katalogiem. Wykluczenie treści z wyników nie usuwa historycznych kopii z backupów. Po świadomej decyzji o usunięciu dawnych danych usuń cały pochodny magazyn i odbuduj go z aktualnych źródeł; samo `index` nie stanowi bezpiecznego wymazania danych.

## Błędy i współbieżność

Embeddingi i nowa tabela powstają przed atomową podmianą `CURRENT`. Błąd modelu, wymiaru, YAML lub zapisu nie publikuje częściowego indeksu. Aktualizacja zachowuje poprzednią generację, a sprzątanie obejmuje tylko rozpoznane generacje tego vaulta. Zewnętrzny katalog magazynu powinien służyć wyłącznie RAG.

Operacje bazy używają blokady. Komunikat „indeks zajęty” oznacza konieczność ponowienia po zakończeniu poprzedniej operacji. Po przerwaniu procesu sprawdź, czy zapisany PID nadal działa, zanim usuniesz `write.lock`. Nie usuwaj blokady działającemu procesowi. Równoległe operacje są odrzucane, a nie kolejkowane.

Przy braku modelu uruchom lokalny serwer i BGE-M3, potem ponów `index`. Przy uszkodzeniu bazy użyj `rebuild`. Przy błędzie uprawnień napraw dostęp do katalogu. Źródeł nie cofaj ani nie usuwaj w reakcji na błąd indeksu. Do tego czasu używaj odczytu dozwolonych plików.

Mechanizm atomowej podmiany chroni przed błędami operacji i przerwaniem procesu; nie deklarujemy odporności na każdy przypadek utraty zasilania czy awarii systemu plików. Indeks można odbudować. Nie dodajemy watchera, harmonogramu ani automatycznego Pinecone.
