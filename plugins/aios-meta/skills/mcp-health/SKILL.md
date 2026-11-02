---
name: mcp-health
description: "Sprawdza dostępne możliwości MCP i lekkie operacje odczytu, w tym lokalny rag_namespaces; nie zakłada stałych prefiksów. Triggery: /aios-meta:mcp-health, sprawdź MCP, health check MCP."
---

# Diagnostyka MCP

Odczytaj listę integracji z `me.md` -> `Bliźniaki` -> `MCP do monitorowania`. Lokalny RAG sprawdź również wtedy, gdy `_config/rag.json` istnieje, ale onboarding nie dopisał jeszcze listy. Nie zapisuj ani nie indeksuj niczego w tej procedurze.

## 1. Odkryj możliwości

Sprawdź narzędzia faktycznie udostępnione przez bieżący runtime. Aliasy serwerów i prefiksy różnią się między klientami. Szukaj funkcji i opisu, nie wyłącznie pełnej nazwy z dawnej konfiguracji. Brak aliasu w tabeli nie oznacza awarii serwera.

Jeśli nie ma listy integracji, zgłoś to; sprawdź tylko lokalny RAG, jeśli skonfigurowany, i wyświetl pozostałe dostępne możliwości bez wywoływania ich w ciemno.

## 2. Wykonaj lekkie odczyty

| Funkcja integracji | Przykładowa operacja odczytu |
|---|---|
| Lokalny RAG | `rag_namespaces()`; bez embeddingu i połączenia z modelem |
| Kalendarz | lista kalendarzy |
| Tracker zadań | lista zespołów/projektów w ograniczonym zakresie |
| Notion / Airtable / Drive | lista lub wyszukanie pojedynczej pozycji |
| Pinecone, jeśli jawnie skonfigurowany | lista indeksów, bez uploadu |
| Pozostałe | udokumentowana, tania operacja read/list dostępna w runtime |

Nie wykonuj płatnych zapytań wyszukiwania ani pobierania przypadkowej strony jako domyślnego testu. Gdy nie potrafisz ustalić bezpiecznej operacji odczytu, oznacz „niezweryfikowane” i podaj brakującą możliwość.

Dla RAG bez MCP wczytaj `_skille/rag.md` i uruchom CLI `namespaces` oraz `status`. Wynik „CLI działa, MCP niepodłączone” rozróżnia dostępność silnika i integracji. `not_indexed` lub pusty indeks to stan danych, nie dowód awarii MCP. Lista namespace nie dowodzi gotowości BGE-M3.

## 3. Raport

Podaj stan każdej sprawdzonej funkcji:

- działa: odczyt zakończył się sukcesem;
- niepodłączone: runtime nie udostępnia potrzebnej funkcji albo brak autoryzacji;
- błąd: rzeczywisty timeout/odpowiedź serwera, z krótką przyczyną;
- niezweryfikowane: brak bezpiecznej operacji testowej;
- lokalny RAG: osobno dostępność CLI/MCP i stan indeksu.

Nie ujawniaj sekretów, nie poprawiaj konfiguracji samodzielnie, nie usuwaj blokad ani nie uruchamiaj `index`/`rebuild`. Zaproponuj jedną naprawę tylko wtedy, gdy przyczyna wynika z wyniku testu.
