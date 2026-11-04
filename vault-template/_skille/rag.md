---
typ_wiedzy: decyzja
tematy: [aios, rag, prywatnosc, indeksowanie]
podmioty: [LanceDB, BGE-M3, LM Studio, MCP]
ai_summary: "Wspólna procedura lokalnego RAG: wyszukiwanie, aktualizacja po zatwierdzonym zapisie i ochrona prywatnych ścieżek."
---

# Lokalny RAG Klaudynki

Markdown jest źródłem prawdy. LanceDB zawiera odbudowywalny indeks, a BGE-M3 oblicza embeddingi na lokalnym endpointcie LM Studio. Agent otrzymuje wybrane fragmenty, więc agent chmurowy może przesłać je swojemu dostawcy. Lokalny indeks nie oznacza lokalnej pracy każdego agenta.

## Wspólne polecenia

Ustal korzeń vaulta po `me.md` i `_config/rag.json`. Używaj środowiska tego vaulta; nie zakładaj, że systemowy `python` ma zależności RAG. Wszystkie ścieżki przekazuj jako osobne argumenty, bez składania niecytowanego polecenia z tekstu użytkownika. `--vault` występuje przed poleceniem.

Z korzenia vaulta, macOS/Linux:

```sh
".venv/bin/python" "_skrypty/aios-rag.py" --vault "." status
".venv/bin/python" "_skrypty/aios-rag.py" --vault "." index
".venv/bin/python" "_skrypty/aios-rag.py" --vault "." query "pytanie" --k 5
```

Natywny Windows, PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" ".\_skrypty\aios-rag.py" --vault "." status
& ".\.venv\Scripts\python.exe" ".\_skrypty\aios-rag.py" --vault "." index
& ".\.venv\Scripts\python.exe" ".\_skrypty\aios-rag.py" --vault "." query "pytanie" --k 5
```

Pozostałe polecenia: `namespaces`, `rebuild` i `mcp`. `rebuild` wykonuje pełną odbudowę; zwykłe odświeżenie to `index`, które ponownie osadza tylko zmienione dokumenty. Nie uruchamiaj harmonogramu ani procesu obserwującego pliki.

## Wyszukiwanie

1. Odkryj dostępne możliwości w bieżącym runtime. Jeśli istnieją narzędzia o funkcji `rag_search(query, namespace, type, k)` i `rag_namespaces()`, użyj ich niezależnie od prefiksu lub aliasu serwera.
2. Bez MCP użyj CLI `query`; filtry CLI to `--namespace`, `--type`, `--k`. Namespace ustal z `namespaces`, nie zgaduj dawnych kategorii Pinecone. Wiedza ma obszary `wiedza-<obszar>`, projekty `projekty-<projekt>`.
3. Otwórz wskazany plik i sprawdź ustalenie. Cytuj ścieżkę i fragment; wynik semantyczny ani jego score nie stanowią dowodu prawdziwości.
4. Gdy RAG jest niedostępny, pusty albo nieaktualny, powiedz to wprost i przejdź do `index.md` oraz odczytu/wyszukiwania lokalnych plików. Użyj Python `pathlib` albo dostępnego narzędzia plikowego; `rg` jest opcjonalne. Fallback także respektuje wykluczenia prywatności.
5. Nigdy nie zastępuj lokalnego modelu usługą chmurową. Pinecone wymaga osobnego, jawnego żądania użytkownika (np. `--pinecone`), istniejącej konfiguracji i uzgodnionego zakresu danych do przekazania. Nie twórz konta, indeksu ani płatnej operacji przy zwykłym wyszukiwaniu.

## Po zatwierdzonej zmianie źródeł

- Po zakończonej partii zatwierdzonych zapisów, przeniesień lub usunięć uruchom raz CLI `index`. Dotyczy to również `index.md`, plików pamięci, raportów i zadań. Nie indeksuj w trakcie podglądu diffu, `--dry-run`, anulowania ani samego odczytu.
- Zgoda na operację na plikach obejmuje odświeżenie lokalnego indeksu w tej samej procedurze. Nadal przestrzegaj osobnych zgód na modyfikację źródeł, przeniesienie, usunięcie i zapis zewnętrzny.
- Przy błędzie zachowaj zapisane źródła oraz ostatni poprawny indeks. Zgłoś: „Źródła zapisane; indeks nieaktualny lub niedostępny: [krótka przyczyna]. Korzystam z plików”. Nie deklaruj pełnego powodzenia ani nie cofaj zatwierdzonych notatek.
- Przy błędzie blokady sprawdź poprzednią operację. Nie usuwaj `write.lock` w ciemno. Przy uszkodzeniu bazy zaproponuj lokalne `rebuild`, nie usuwaj notatek.

## Prywatność i frontmatter

- Konfiguracja leży w `_config/rag.json`. Domyślne `private_paths` wyklucza `Prywatne/**` i `Projekty/Prywatne/**`. Dodatkowe strefy wskazane przez użytkownika dopisz do konfiguracji przed pierwszym indeksowaniem.
- Gdy cała zawartość vaulta jest prywatna, ustaw `private_paths: ["**"]`. Nie włączaj indeksowania tylko dlatego, że indeks jest lokalny. Zawężenie ochrony wymaga jawnej decyzji użytkownika i podglądu zmiany konfiguracji.
- `rag: false`, `private: true` lub `prywatne: true` we frontmatter wyklucza notatkę. Nie zdejmuj tych oznaczeń przy kopiowaniu, promocji do Wiki lub tworzeniu projektu.
- Sekrety, ukryte katalogi, zależności, cache, worktree'y, archiwa, Kosz i `_brudnopis` pozostają poza indeksem. Samo wywołanie skilla nie zezwala na obejście wykluczeń. Odczyt konkretnego prywatnego pliku wymaga odpowiedniego zakresu prośby użytkownika; nie dołączaj go do ogólnego wyszukiwania.
- Każda nowa notatka `.md` zaczyna się od YAML: `typ_wiedzy`, `status` (`aktywny | obalony | zastąpiony przez [[link]]`), `data_wpisu` (ISO-8601), `tematy` (lista), `podmioty` (lista), `ai_summary`. Zachowaj dodatkowe pola, źródła i flagi prywatności. Starsze metadane są czytelne dla RAG; nie przepisuj istniejących notatek masowo.

```yaml
---
typ_wiedzy: fakt
status: aktywny
data_wpisu: YYYY-MM-DD
tematy: [temat]
podmioty: []
ai_summary: "Jedno zdanie o rzeczywistej zawartości notatki."
---
```
