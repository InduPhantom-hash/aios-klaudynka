---
name: aios-doctor
description: "Zintegrowany dashboard kondycji środowiska AIOS: testy serwerów MCP, weryfikacja symlinków multi-runtime oraz synchronizacja z zewnętrznymi trackerami. Triggery: /aios-doctor, /aios:doctor, /doctor, \'doktor\', \'stan środowiska\', \'mcp health\', \'sprawdź mcp\', \'sprawdź integracje\'."
---
# AIOS Doctor (Diagnostyka Środowiska i Narzędzi)

## Cel i kontekst
Centralny punkt diagnostyczny środowiska operacyjnego AIOS. Sprawdza kondycję techniczną narzędzi, integralność symlinków między agentami oraz spójność z usługami zewnętrznymi. Konsoliduje dotychczasowe skille: `aios-meta-mcp-health`, `aios-skills-sync` oraz `aios-meta-synchronizuj`.

## Procedura diagnostyczna

### 1. Weryfikacja Serwerów MCP (Health Check)
Sprawdź stan wszystkich wykrytych integracji i serwerów MCP w bieżącym runtime:
1. Dla każdego aktywnego serwera MCP wykonaj najlżejszy, bezskutkowy odczyt (np. `list_*`, `whoami`, `get_profile` lub ping).
2. Oznacz wynik: `Działa (OK)`, `Brak autoryzacji`, `Niedostępny` lub `Błąd`.
3. Nigdy nie wykonuj operacji zapisu ani nie ponawiaj operacji niosących ryzyko kosztowe/uboczne.

### 2. Weryfikacja Spójności Skilli i Środowiska
1. W instalacji Klaudynki zweryfikuj czy folder `_skille/aios/skills/` zawiera komplet skilli oraz czy plik konfiguracji `_config/mcp-rag.json` wskazuje poprawny interpreter `.venv`.
2. Jeśli skonfigurowano multi-runtime (`~/.aios-skills/`), sprawdź status synchronizacji:
```bash
aios-skills status
```
- Upewnij się, że dowiązania symboliczne są poprawne i brak jest zerwanych linków.

### 3. Weryfikacja Zewnętrznych Bliźniaków (Twin Sync)
Sprawdź spójność pomiędzy zadaniami w vaulcie a zewnętrznymi trackerami (ClickUp, kalendarz):
1. Porównaj otwarte pozycje z `Projekty/**/zadania.md` z danymi w zewnętrznym systemie (o ile dane MCP są dostępne).
2. Zidentyfikuj brakujące pozycje, rozbieżne statusy lub osierocone wpisy.
3. Wyświetl tabelę rozjazdów z rekomendacją kierunku synchronizacji (Vault jest zawsze Single Source of Truth).

## Checkpoint i bezpieczeństwo
- Doctor działa wyłącznie w trybie odczytu (read-only).
- Raportuje stan w zwartej tabeli podsumowującej (MCP, Symlinki, Bliźniaki).
- Żadna naprawa, ponowna autoryzacja serwera MCP ani modyfikacja danych w trackerze nie może zostać wykonana bez osobnej, wyraźnej zgody (`tak`).
