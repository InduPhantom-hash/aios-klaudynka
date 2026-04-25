---
name: mcp-health
description: >
  Sprawdza ktore MCP serwery z konfiguracji usera odpowiadaja, a ktore leza.
  Lista MCP do sprawdzenia pochodzi z me.md (sekcja Bliznniaki -> MCP do monitorowania).
  Wywoluje lekkie operacje na kazdym MCP i raportuje status.
  Triggery: /aios-meta:mcp-health, "sprawdz MCP", "ktore MCP dzialaja", "health check MCP".
---

# AIOS Meta: MCP Health Check

Testuj kazdy MCP z listy wywolujac minimalna operacje. Raport: dziala / lezy / nie skonfigurowany.

## Krok 1: Wczytaj liste MCP z me.md

Przeczytaj `me.md` -> sekcja `## Bliznniaki` -> `### MCP do monitorowania`. Spodziewasz sie listy nazw MCP, np.:

```
- google-calendar
- tavily
- linear
- pinecone
- obsidian
- session_info
```

Dla kazdej nazwy z listy znajdz odpowiadajaca **lekka operacje testowa** w mapowaniu ponizej. Jesli nazwy MCP nie ma w mapowaniu - oznacz jako `? NIEZNANY` w raporcie i pomin testowanie (user musi dodac mapowanie w SKILL.md albo dopisac do me.md jaka operacja jest read-only).

**Jesli sekcja MCP nie istnieje w me.md albo jest pusta:** powiedz userowi:

> "Nie masz listy MCP do monitorowania w me.md (sekcja Bliznniaki -> MCP do monitorowania). Zeby `/aios-meta:mcp-health` mialo co sprawdzac, dopisz tam nazwy MCP serwerow ktorych uzywasz. Mozesz tez teraz powiedziec ktore wymienic - dopisze do me.md."

## Mapowanie MCP -> operacja read-only

| MCP (alias) | Lekka operacja testowa |
|------------|------------------------|
| google-calendar | `list_calendars` |
| tavily | `tavily_search` z query "test" i `max_results: 1` |
| linear | `list_teams` |
| clickup | `clickup_get_workspace_hierarchy` |
| notion | `notion-search` z pustym query |
| airtable | `list_bases` |
| obsidian | `get_vault_stats` |
| pinecone | `list-indexes` |
| supabase | `list_projects` |
| vercel | `list_projects` |
| posthog | `projects-get` |
| google-analytics | `list_metric_categories` |
| google-search-console | `list_properties` |
| apollo | `apollo_users_api_profile` |
| session_info | `list_sessions` z `limit: 1` |
| n8n | `n8n_health_check` |
| google-drive | `list_recent_files` z `pageSize: 1` |
| gmail | `list_labels` |
| apple-notes | `list_notes` |
| desktop-commander | `get_config` |
| miro | `context_get` |
| firecrawl | `firecrawl_scrape` na `https://example.com` (lekkie) |
| semrush | `keyword_research` z minimalnym query |

## Krok 2: Wywolaj kazdy test

Dla kazdego MCP z listy: wywolaj wskazana operacje.

- Jesli sukces -> status `OK`
- Jesli blad autoryzacji / nie znaleziono narzedzia -> status `BRAK / nie skonfigurowany`
- Jesli timeout lub blad serwera -> status `LEZY`

Wywoluj rownolegle gdzie mozliwe (niezalezne MCP). Nie przerywaj przy pierwszym bledzie - sprawdz wszystkie.

## Krok 3: Raport

```
MCP HEALTH CHECK - [data, godzina]

OK (N):
  google-calendar, tavily, obsidian, pinecone, session_info, ...

LEZY (N):
  n8n     [blad: connection refused]
  ...

BRAK / nie skonfigurowany (N):
  apple-notes, ...

NIEZNANY (N - brakuje mapowania w SKILL.md):
  jakis-niestandardowy-mcp

LACZNIE: N/M sprawdzonych MCP dziala.
```

Dla kazdego problemu: jedno zdanie z bledem (nie pelny stack trace).

## Krok 4: Akcja (opcjonalna)

Jesli ktorys MCP lezy - na koncu napisz jedna linie:
`Zeby naprawic: [konkretna akcja, np. "zrestartuj kontener n8n" / "odnow token w settings"]`

Tylko jesli znasz przyczyne. Nie zgaduj.

## Czego NIE rob

- Nie wywoluj operacji destructive (create, delete, update) - tylko read/list
- Nie probuj "naprawic" MCP automatycznie
- Nie sprawdzaj MCP ktore nie sa na liscie usera w me.md - trzymaj sie jego konfiguracji
- Nie modyfikuj me.md sam (chyba ze user explicite prosi o dopisanie nowego MCP)
