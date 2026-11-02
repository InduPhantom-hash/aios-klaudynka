---
typ_wiedzy: fakt
tematy: [klaudynka, zgodnosc, rag]
podmioty: [AIOS, MCP, LanceDB]
ai_summary: "Macierz 14 skilli core i 4 meta z zależnościami oraz scenariuszami odbioru wydania 0.7.0."
---

# Zgodność skilli 0.7.0

Stan 2026-11-02: wszystkie 18 procedur dostosowane i poddane niezależnemu przeglądowi. YAML, nazwy, ścieżki referencji i wspólna procedura RAG przechodzą walidację. Skille są instrukcjami dla agentów; walidacja tekstu nie dowodzi wykonania procedury przez każdy model. Wyniki poniżej rozdzielają te poziomy.

| Skill | Zależność / zmiana | Scenariusz odbioru | Wynik |
|---|---|---|---|
| init | Instalator, lokalny RAG | Quick/full zapisuje konfigurację, tworzy indeks i zgłasza gotowość albo brak modelu | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| backpass | Python, logi sesji | Destylacja i walidacja propozycji, bez samowolnego zastosowania | 7 testów silnika PASS; procedura zgodna po przeglądzie; test agentowy niewykonany |
| pomysl-do-promptu | Pliki projektu | Powstaje zatwierdzony dokument, potem aktualizacja indeksu | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| sortuj | Operacje na plikach | Przeniesiona notatka trafia do RAG pod nową ścieżką | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| stworz-projekt | Szablony projektu | Nowy projekt otrzymuje własny namespace | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| dodaj-do-wiki | Markdown, indeksowanie | Nowa i zmieniona strona pojawia się w wynikach | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| szukaj | MCP lub CLI RAG | Zapytanie PL/EN, filtr i odczyt źródła; fallback bez modelu | CLI/MCP i realny BGE-M3 PASS na macOS; procedura zgodna po przeglądzie; test klienta AI niewykonany |
| koniec-sesji | Pamięć, prywatność | Aktualizacja pamięci widoczna; brudnopis poza indeksem | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| kontynuuj | Pliki pamięci, opcjonalne MCP sesji | Odczyt ostatniego stanu przy braku MCP | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| dzien | Lokalny tracker, opcjonalny kalendarz | Zadania dostępne bez kalendarza i RAG | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| core-update | Lokalny indeks | Dry-run bez zapisu, aktualizacja po zgodzie, bez automatycznego Pinecone | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| research | Zewnętrzne wyszukiwanie | Jawna zależność; zapis wyniku i lokalne indeksowanie | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| ingest-article | Fetch / opcjonalne MCP | Zapis źródła z metadanymi i odświeżenie indeksu | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| zadania | Lokalny tracker, opcjonalne integracje | Lokalny zapis i indeks; brak wymogu chmury | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| audyt-luk | Odczyt plików | Raport bez zmiany źródeł ani indeksu | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| mcp-health | Dostępne capabilities | rag_namespaces bez embeddingu; brak aliasu nie oznacza awarii | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| synchronizuj | Opcjonalne integracje | Raport różnic; zapis tylko po zgodzie, potem indeks | Procedura zgodna po przeglądzie; test agentowy niewykonany |
| wizualizuj-vault | Lokalna struktura, opcjonalne Miro | Widok lokalny bez MCP i bez zmiany indeksu | Procedura zgodna po przeglądzie; test agentowy niewykonany |

## Zależności opcjonalne i ograniczenia

- `research` wymaga publicznych źródeł i wyszukiwarki; lokalny indeks nie zastępuje świeżego researchu. `ingest-article` wymaga dostępu do wskazanego URL albo dostarczonej treści. Tavily nie jest obowiązkowym dostawcą.
- `synchronizuj` wymaga wybranej integracji do porównania zewnętrznego stanu. `mcp-health` diagnozuje wyłącznie odkryte lub wskazane możliwości.
- Kalendarz w `dzien`, historia sesji w `kontynuuj`, eksport `zadania` i Miro w `wizualizuj-vault` są opcjonalne. Brak tych usług nie blokuje ich lokalnej części.
- Zwykłe `szukaj` nie używa chmury. Pinecone wymaga jawnego wyboru, istniejącej konfiguracji i uzgodnionego zakresu.
- Nie wykonano pełnych dialogów onboardingowych quick/full, wszystkich 18 procedur przez klienta AI ani macierzy wszystkich modeli. Nie oznaczać tych scenariuszy jako PASS na podstawie testów silnika.

Dowody systemowe i komendy: [raport odbioru](odbior-0.7.0.md).
