---
typ_wiedzy: decyzja
tematy: [klaudynka, github, wydanie]
podmioty: [GitHub, AIOS, LanceDB, BGE-M3]
ai_summary: "Payload publikacji kandydata 0.7.0 oraz warunki wymagane przed zatwierdzeniem zewnętrznych zmian."
---

# Publikacja 0.7.0 - zatwierdzony zakres

Zgoda użytkownika z 2026-11-02 obejmuje commit, push, roboczy PR oraz aktualizację About/topics według pokazanego zakresu. Merge, tag i pełne wydanie wymagają odrębnej decyzji. Instrukcje aktualizacji istniejących vaultów nie należą do zakresu. Docelowe repo: `InduPhantom-hash/aios-klaudynka`, gałąź robocza `codex/klaudynka-local-rag`.

## Zmiany na GitHubie

Zatwierdzony zakres obejmuje commit i push gałęzi roboczej, a następnie roboczy PR o tytule:

> Klaudynka 0.7.0: lokalny RAG dla nowych instalacji

Payload roboczego PR: base `main`, head `codex/klaudynka-local-rag`, draft `true`. Proponowany commit: `feat: add local RAG to Klaudynka 0.7.0`.

Dokładna treść PR:

````markdown
## Summary

Klaudynka 0.6.0 opisywała wyszukiwanie przez hierarchię i Pinecone. Kandydat 0.7.0 dodaje domyślny lokalny RAG dla nowych instalacji:

```text
Markdown -> lokalny BGE-M3 -> LanceDB -> CLI / read-only MCP -> fragment ze źródłem
```

Instalator odmawia nadpisania istniejącego vaulta i przygotowuje własne środowisko Python. Indeksowanie ponawia embeddingi tylko zmienionych dokumentów i publikuje generację po udanym zapisie. Zmiana prywatności działa także w istniejącej sesji MCP; nieaktualny indeks odmawia zwracania fragmentów. Dostosowano 14 skilli core i 4 meta, szablony oraz dokumentację.

## Evidence

- **Before:** brak przenośnego lokalnego RAG w szablonie; test nowej instalacji i testy prywatności wykrywały brak implementacji lub ujawnienie nazwy wykluczonego projektu.
  **After:** macOS: 18 testów RAG, 4 instalatora, 7 Backpass oraz rzeczywisty test BGE-M3 PL/EN przez CLI/MCP PASS. Linux ARM64 w kontenerze Python 3.11: 28 testów PASS; Python 3.13 sprawdzony w poprzedniej iteracji.
- Walidator manifestów, YAML, lokalnych linków i prywatnych ścieżek PASS. Szczegóły i granice dowodów: [raport odbioru](https://github.com/InduPhantom-hash/aios-klaudynka/blob/codex/klaudynka-local-rag/docs/odbior-0.7.0.md).
- PR uruchamia macierz macOS/Windows/Ubuntu z Python 3.11 oraz 3.13. Test CI korzysta z lokalnego fixture embeddingów.
- Niewykonane: natywna instalacja Windows, realny model na natywnym Linuksie, pełny onboarding i wykonanie 18 procedur przez klientów AI. Migracja istniejących vaultów pozostaje poza zakresem.

## Merge Danger

**Door:** two-way. Zmiany dotyczą nowych instalacji; Markdown pozostaje źródłem prawdy, indeks można odbudować.

**Blast Radius:** instalacja. Wyższe wymagania Python i lokalnego modelu; pełna zgodność platform wymaga odbioru. To roboczy kandydat, bez zgody na merge, tag i pełne wydanie.
````

Zatwierdzenie samego push/PR nie oznacza zgody na merge, tag ani publiczne wydanie. PR uruchomi nowy workflow CI na macOS, Windows i Linux. To automatyczne testy z lokalnym serwerem-fixture, bez pobierania i uruchamiania LM Studio.

Payload About:

```json
{
  "description": "Personal Agentic OS in Markdown: local RAG (LanceDB + BGE-M3), 14 core skills + 4 optional meta skills, Backpass and local tasks. Polish-first, MIT.",
  "topics": [
    "agentic-ai", "ai-agents", "aios", "antigravity", "claude-code",
    "code-over-ai", "file-over-ai", "knowledge-management", "obsidian",
    "personal-agentic-os", "personal-knowledge-management", "polish",
    "second-brain", "task-tracker", "rag", "lancedb", "bge-m3", "local-first"
  ]
}
```

Zachowujemy dotychczasowe tematy i dodajemy RAG oraz lokalny stos. Pole homepage pozostaje bez zmiany. Opis strony głównej repo pochodzi z nowego README.

## Bramka wydania

- Zielony CI dla macOS/Windows/Linux i sprawdzona świeża instalacja na natywnym Windows.
- Rzeczywiste zapytanie ze źródłem przez CLI i MCP w środowiskach deklarowanych jako sprawdzone.
- Wykonane lub jawnie ograniczone scenariusze 18 skilli; szczególnie onboarding quick/full i podłączenie klienta AI.
- Akceptacja aktualnego diffu i raportu przez właściciela repo.
- Dopiero potem osobno zatwierdzony merge, tag `v0.7.0`, opis wydania oraz About/topics. Nie nadpisywać historycznego tagu ani starej paczki pluginu.

Jeżeli właściciel wybierze publikację wcześniejszego kandydata, opis musi zachować stan „kandydat” i listę niewykonanych testów. Nie oznaczać go jako pełnego wydania po samym teście jednostkowym lub przeglądzie instrukcji.

## Wykonany zapis zewnętrzny

2026-11-02: wypchnięta gałąź `codex/klaudynka-local-rag` i utworzony [roboczy PR](https://github.com/InduPhantom-hash/aios-klaudynka/pull/2). Opis About oraz 18 tematów repozytorium zaktualizowano i odczytano ponownie przez API. README i instrukcje nowej wersji znajdują się w PR. `main`, tagi i pełne wydanie pozostają bez scalenia.

CI uruchomiony dla trzech systemów i dwóch wersji Python. Pełne przygotowanie środowiska przez `install.py` jest osobnym krokiem każdego zadania. Bieżące wyniki w PR i raporcie odbioru.
