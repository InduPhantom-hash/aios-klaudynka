---
typ_wiedzy: fakt
status: aktywny
data_wpisu: 2026-11-04
tematy: [klaudynka, zgodnosc, rag, skille]
podmioty: [AIOS, MCP, LanceDB]
ai_summary: "Macierz 18 skilli uniwersalnych z zależnościami oraz scenariuszami odbioru wydania 0.8.0."
---

# Zgodność skilli 0.8.0

Stan 2026-11-04: wszystkie 18 procedur skonsolidowane z jednolitym prefiksem `aios-` i poddane niezależnemu przeglądowi. Przestarzały plugin `aios-meta` został wycofany (jego zadania w pełni przejęły `aios-kustosz` oraz `aios-doctor`). YAML, nazwy, ścieżki referencji i wspólna procedura RAG przechodzą walidację. Skille są instrukcjami dla agentów; walidacja tekstu nie dowodzi wykonania procedury przez każdy model. Wyniki poniżej rozdzielają te poziomy.

| Skill | Zależność / zmiana | Scenariusz odbioru | Wynik |
|---|---|---|---|
| aios-anonimizacja | Narzędzia lokalne maskowania | Tarcza PII przed chmurą i maskowanie encji | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-backpass | Python, logi sesji | Destylacja i walidacja propozycji, bez samowolnego zastosowania | 7 testów silnika PASS; procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-data-analysis | Pliki danych (CSV, JSON, Parquet) | 7-fazowa analiza danych w stylu senior data analyst | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-debata | Tryby dyskusji | Sokratejska dysputa lub debata oksfordzka subagentów | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-doctor | Capabilities runtime, integracje | Test serwerów MCP, symlinków multi-runtime i trackerów | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-dzien | Lokalny tracker, opcjonalny kalendarz | Zadania dostępne bez kalendarza i RAG | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-grilling | Pytania decyzyjne | Bezwzględny stress-test założeń i decyzji | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-init | Instalator, lokalny RAG | Quick/full zapisuje konfigurację, tworzy indeks i zgłasza gotowość albo brak modelu | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-koniec-sesji | Pamięć sesji, limit 3 KB | Aktualizacja pamięci sesji i zapis wniosków; brudnopis poza indeksem | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-kontynuuj | Pliki pamięci, opcjonalne MCP sesji | Odczyt ostatniego stanu carry-over przy braku MCP | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-kustosz | Skrypt Python, odczyt plików | Audyt struktury i luk, linter dat ISO-8601 i wizualizacja mapy | Skrypt lint_md.py PASS; procedura zgodna po przeglądzie |
| aios-research-faktow | Wyszukiwanie zewnętrzne, SIFT | Rygorystyczny research z filtrem Anty-AI Slop (Evidence Brief) | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-research-rynkowy | Desk research, subagenci | Wyszukiwanie dowodów podważających w literaturze i rynku | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-sortuj | Operacje na plikach | Przeniesiona notatka trafia do RAG pod nową ścieżką | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-stworz-projekt | Szablony projektu | Nowy projekt otrzymuje własny namespace i strukturę | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-szukaj | MCP lub CLI RAG | Zapytanie PL/EN, filtr i odczyt źródła; fallback bez modelu | CLI/MCP i realny BGE-M3 PASS na macOS; procedura zgodna po przeglądzie; test klienta AI niewykonany |
| aios-weryfikacja | Zasada weryfikacji faktów | Weryfikacja hipotez i redukcja over-reliance | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| aios-wyjasnij | Pliki wiedzy | Wyjaśnienie pojęć prostym językiem (jak 12-latkowi) i diagnoza luk | Procedura zgodna po przeglądzie; test agentowy niewykonany |

## Zależności opcjonalne i ograniczenia

- `aios-research-faktow` i `aios-research-rynkowy` wymagają publicznych źródeł i wyszukiwarki; lokalny indeks nie zastępuje świeżego researchu zewnętrznego.
- `aios-doctor` diagnozuje wyłącznie odkryte lub wskazane możliwości środowiska runtime.
- Kalendarz w `aios-dzien` oraz historia sesji w `aios-kontynuuj` są opcjonalne. Brak tych usług nie blokuje ich lokalnej części.
- Zwykłe `aios-szukaj` nie używa chmury. Pinecone wymaga jawnego wyboru, istniejącej konfiguracji i uzgodnionego zakresu.
- Nie wykonano pełnych dialogów onboardingowych quick/full, wszystkich 18 procedur przez klienta AI ani macierzy wszystkich modeli. Nie oznaczać tych scenariuszy jako PASS na podstawie testów silnika.

Dowody systemowe i komendy: [raport odbioru](odbior-0.7.0.md).
