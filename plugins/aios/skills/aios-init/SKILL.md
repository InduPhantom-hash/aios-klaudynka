---
name: aios-init
description: "Onboarding Klaudynki: profil me.md, struktura vaulta, lokalny Task Tracker oraz domyślny RAG LanceDB/BGE-M3. Tryby --quick i --full. Triggery: /aios:init, /aios-init, uruchom onboarding, skonfiguruj AIOS."
---

# Pierwsza konfiguracja Klaudynki

Ta procedura dotyczy nowej instalacji. Nie migruj istniejącego vaulta i nie nadpisuj profilu. Najpierw odczytaj `me.md`, jeśli istnieje, oraz `AGENTS.md` i `_skille/rag.md`. Instalator `install.py` przygotowuje pliki, `.venv`, skille w `_skille/aios/skills/` i wzór `_config/mcp-rag.json`; integracja MCP zależy od capabilities klienta.

## 1. Wybierz tryb i zbierz profil

- `--quick`: krótkie pytania o cel, zakres prywatny/zawodowy, kategorie projektów, narzędzia i komunikację. Nie pomijaj granic prywatności.
- `--full`: przejdź sekcje z sąsiedniego `pytania.md`, łącznie z opcjonalnymi integracjami i granicami prywatności. Dokumenty referencyjne instalator kopiuje do `_skille/dokumentacja/szablony/`, a przykłady profili do `_skille/dokumentacja/przyklady/`. Jeśli ich brakuje, zgłoś niepełną instalację; nie udawaj odczytu brakującego szablonu.
- Zapisuj zatwierdzony postęp w `_pamiec/onboarding-progress.md`, z metadanymi i `rag: false`. Nie zapisuj kluczy ani niepotrzebnych danych wrażliwych.
- System zadań: domyślnie lokalny `zadania.md`; zewnętrzny tracker jest opcjonalny i wymaga osobnej konfiguracji oraz zgody na zapis.

## 2. Ustaw prywatność przed pierwszym indeksem

Odczytaj odpowiedzi o strefach prywatnych i przygotuj konfigurację `_config/rag.json`:

- Zachowaj domyślne `private_paths`: `Prywatne/**`, `Projekty/Prywatne/**`.
- Dodaj wszystkie dodatkowe strefy wyłączone przez użytkownika, jako wzorce względne z `/`.
- Jeśli użytkownik określa cały vault jako prywatny albo nie wydziela osobnej strefy dla treści prywatnych, ustaw `private_paths` na `["**"]`. Nie interpretuj lokalności embeddingów jako zgody na ujawnienie notatek agentowi.
- Każda nowa prywatna notatka zachowuje także `rag: false`, `private: true` lub `prywatne: true`, gdy takie oznaczenie wskazał użytkownik.
- Przed zmianą istniejącego `_config/rag.json` pokaż konkretny diff i uzyskaj zgodę. Nie uruchamiaj pierwszego indeksu przed zatwierdzeniem granic prywatności.

## 3. Wygeneruj pliki w zatwierdzonym zakresie

Utwórz `me.md` z profilem, komunikacją, hard rules, aktywnymi projektami, granicami prywatności oraz opcjonalnymi bliźniakami. Parametry techniczne RAG pozostają w `_config/rag.json`; w profilu zapisz tylko informację, że system korzysta z lokalnego RAG.

Utwórz zaakceptowane kategorie `Projekty/`, ich `index.md`, projekty i pliki zadań `zadania.md` oraz `vault-map.md`. Każdy nowy plik `.md` zaczyna się od bitemporalnego YAML: `typ_wiedzy`, `status: aktywny`, `data_wpisu: YYYY-MM-DD`, `tematy`, `podmioty`, `ai_summary`; zachowaj dodatkowe metadane. Przed zmianą istniejących plików pokaż diff i czekaj na zgodę.

## 4. Potwierdź RAG

1. Sprawdź `.venv` i lokalny model BGE-M3 według INSTALL. Bez modelu zgłoś niepełną konfigurację i kontynuuj pracę na plikach; nie zmieniaj endpointu na chmurę.
2. Uruchom CLI `index` według `_skille/rag.md`, a następnie `status`.
3. Jeżeli istnieje dozwolona notatka, wywołaj `query` z pytaniem o jej treść, otwórz wskazane źródło i sprawdź dopasowanie. Nie zakładaj, że sam `status` lub pusty indeks dowodzą działania modelu.
4. Jeśli nie ma dozwolonych notatek, np. `private_paths: ["**"]`, zgłoś „Indeks pusty zgodnie z prywatnością; wyszukiwanie semantyczne niezweryfikowane”. Nie zmieniaj ochrony, żeby wymusić test.
5. Odkryj w kliencie `rag_search` i `rag_namespaces`. Bez nich sprawdź CLI i podaj status „CLI dostępne, MCP niepodłączone”. Nie wymagaj konkretnego prefiksu nazwy narzędzia.

## 5. Zakończ

Przedstaw oddzielnie: profil i pliki, prywatność, lokalny indeks i model, MCP/CLI oraz brakujące integracje. Gotowość wyszukiwania deklaruj dopiero po rzeczywistym zapytaniu i sprawdzeniu źródła. Zapisz wynik w `aktualny.md` i odśwież lokalny indeks po tym zapisie. Plik postępu usuwaj wyłącznie po osobnym potwierdzeniu; możesz pozostawić go z zakończonym statusem i `rag: false`.
