---
name: szukaj
description: "Wyszukuje wiedzę lokalnym RAG przez MCP lub CLI, z odczytem źródła i fallbackiem do index.md oraz plików. Pinecone tylko na jawne żądanie. Triggery: /aios:szukaj, znajdź w wiedzy, co mam w vaulcie o."
---

# Szukaj w vaulcie

Przeczytaj `_skille/rag.md`. Ustal korzeń vaulta po `me.md`, respektuj strefy prywatności w `_config/rag.json` oraz flagi notatek. Znana, wskazana ścieżka oznacza bezpośredni odczyt źródła; przy pytaniu o wiedzę użyj lokalnego RAG.

## Argumenty

- `<query>`: pytanie PL/EN lub fraza.
- `--projekt <nazwa>`: zawężenie do namespace projektu ustalonego przez `rag_namespaces()` lub CLI `namespaces`.
- `--top N`: liczba wyników, od 1 do 50, domyślnie 5; w MCP przekaż `k`, w CLI `--k`.
- `--tylko-hierarchia`: pomiń RAG i Pinecone, nawiguj po indeksach oraz lokalnych plikach.
- `--pinecone`: jawne żądanie użycia skonfigurowanej integracji Pinecone; nie uruchamiaj jej jako automatycznego fallbacku.
- `--include-brudnopis`: jawnie odczytaj pasujące pliki z `_brudnopis` poza indeksem RAG. To nie zmienia reguł indeksowania ani ochrony prywatnych notatek.

## Procedura

1. Odkryj dostępne capabilities. Wywołaj `rag_search(query, namespace, type, k)`; nie wymagaj konkretnego prefiksu narzędzia. Bez MCP użyj CLI opisanego w `_skille/rag.md`, np. polecenia `query` z `--vault` przed nim.
2. Namespace sprawdź na liście dostępnych obszarów. Nie mapuj projektów na dawne namespace kategorii. Nieznany obszar oznacza wyszukiwanie bez filtra albo doprecyzowanie celu.
3. Otwórz pliki źródłowe trafień. Podaj ścieżkę, krótki cytat i związek z pytaniem. Oznacz źródło jako lokalny RAG; score informuje o dopasowaniu, nie o pewności twierdzenia.
4. Jeśli indeks jest pusty, nieaktualny lub niedostępny, zaznacz stan i użyj hierarchii: `vault-map.md`, `Projekty/index.md` lub `Wiedza/index.md`, następnie indeks obszaru/projektu i źródło. Gdy indeksy nie obejmują notatki, przeszukaj dozwolone pliki przez Python `pathlib` lub dostępne narzędzie plikowe; `rg` jest opcjonalne.
5. Przy pytaniu o ostatnią sesję odczytaj `_pamiec/aktualny.md`; historię i brudnopisy przeglądaj tylko w zakresie wskazanym przez użytkownika. Nie indeksuj ich przy okazji.

## Pinecone na jawne żądanie

Tylko przy `--pinecone` albo równoważnej prośbie sprawdź konfigurację użytkownika i narzędzia wyszukiwania Pinecone. Nazwę indeksu oraz namespace odczytaj z konfiguracji; nie zakładaj `aios`, modelu embeddingów ani stałej nazwy MCP. Użyj wyłącznie operacji wyszukiwania w zatwierdzonym zakresie. Przy braku konfiguracji zgłoś brak; nie twórz konta, indeksu, uploadu ani kosztu.

## Granice

Ten skill jest odczytowy: nie uruchamia `index`/`rebuild`, nie poprawia notatek i nie dopisuje linków samodzielnie. Możesz wskazać brakujący link w `index.md` jako propozycję do zatwierdzenia. W fallbacku nie omijaj `private_paths`, `exclude`, flag prywatności ani standardowych wykluczeń z `_skille/rag.md`.
