---
typ_wiedzy: fakt
tematy: [klaudynka, testy, odbior]
podmioty: [AIOS, LanceDB, BGE-M3, LM Studio, MCP, Docker]
ai_summary: "Dowody lokalnego wdrożenia 0.7.0 i jawne braki przed pełnym wydaniem na trzy systemy."
---

# Odbiór kandydata 0.7.0

Stan na 2026-11-02: kandydat wypchnięty do [roboczego PR](https://github.com/InduPhantom-hash/aios-klaudynka/pull/2), opis About i tematy repo zaktualizowane. Bez scalenia do main, tagu i pełnego wydania. Źródła RAG działają niezależnie od prywatnego Huba autora. Markdown pozostaje źródłem prawdy. Pełne wydanie wymaga zamknięcia niżej wymienionych bramek; sam zestaw testów kodu nie dowodzi działania wszystkich procedur agentowych.

## Potwierdzone wyniki

| Obszar | Wynik i granica dowodu |
|---|---|
| Nowa instalacja macOS, Python 3.13 | PASS: nowy katalog ze spacjami i polskimi znakami, własne venv, zależności, `pip check` |
| Silnik CLI/MCP | 18 testów integracyjnych PASS: rzeczywisty LanceDB, lokalny HTTP-fixture embeddingów, rzeczywista sesja MCP stdio |
| Instalator | 3 testy PASS: nowe pliki i payload MCP, odmowa nadpisania, JSON przy konsoli ASCII |
| Realny lokalny BGE-M3 na macOS | PASS: syntetyczne notatki, pytania PL/EN ze wskazaniem oczekiwanego źródła, aktualizacja notatki i zapytanie MCP |
| Linux ARM64 w Dockerze | PASS dla świeżej instalacji Python 3.13, CLI/MCP z lokalnym fixture i 7 testów Backpass; nie jest to test GUI LM Studio na natywnym Linuksie |
| Minimalny Python 3.11 w Linux ARM64 | PASS: świeża instalacja, pip check, 21 testów instalatora/CLI/MCP i 7 testów Backpass; realny model pominięty. Nie zastępuje macOS/Windows 3.11 |
| Backpass | 7 testów PASS; usunięte prywatne ścieżki autora z demo i fixture testowego |
| 18 skilli | Niezależny przegląd procedur i walidacja YAML/nazw/referencji; pełne wykonanie przez agentów niewykonane |
| Manifesty i paczka | Wspólny validator sprawdza core 0.7.0, meta 0.2.0, 18 skilli, YAML nowych dokumentów, lokalne linki i brak prywatnych ścieżek |

W środowisku czystej instalacji potwierdzono: LanceDB 0.33.0, MCP 1.28.0, requests 2.34.2, PyYAML 6.0.3. Model pochodzi z istniejącego lokalnego LM Studio, bez zmiany jego konfiguracji i bez użycia prywatnych notatek. Automatyczne pobranie modelu od zera nie należało do wykonanego testu.

Testy z fixture weryfikują przepływ, filtry i ochronę stanu; nie mierzą jakości semantycznej BGE-M3. Odrębny test rzeczywisty obejmuje mały korpus syntetyczny, nie benchmark jakości całego vaulta.

## Komendy odtwarzające

Po instalacji zależności do osobnego środowiska, z katalogu repo:

```text
python -m unittest discover -s tests -v
python vault-template/_skrypty/aios_backpass/tests/run_all_tests.py
python tools/validate_release.py
git diff --check
```

Pierwsza komenda wykrywa 22 testy: 21 wykonuje, a rzeczywisty model pomija bez jawnego opt-in. Realny test lokalnego modelu:

```sh
AIOS_LIVE_RAG=1 python -m unittest discover -s tests -p test_live_rag.py -v
```

Na PowerShell ustaw `$env:AIOS_LIVE_RAG="1"` i uruchom tę samą komendę Python. Nie kieruj testu do zdalnego embeddera. Fixture używa własnego tymczasowego serwera na loopback, więc wymaga możliwości otwarcia lokalnego portu.

`python tools/verify.py --live` zbiera powyższe komendy, wersje i pełne logi w ignorowanym `.aios/review/verification.json`. Nie nadpisuje profilu ani danych vaulta. Wymaga Git do sprawdzenia diffu i istniejącego lokalnego BGE-M3 dla ostatniej próby. Bez `--live` omija prawdziwy model.

Workflow `.github/workflows/verify.yml` przygotowuje sześć zadań: macOS, Windows i Ubuntu, każde z Python 3.11 oraz 3.13. Workflow uruchomiono po zatwierdzonym push i utworzeniu PR; bieżący wynik widnieje w PR. Każde zadanie przygotowuje także świeży vault z własnym środowiskiem Python przez `install.py`. Testy CI korzystają z fixture, nie z GUI LM Studio.

## Poprawki z przeglądu

- Lista obszarów respektuje aktualne flagi `rag: false` i `private: true` bez reindeksu; nazwa wykluczonego projektu znika od razu.
- Działający MCP ponownie czyta konfigurację prywatności przy każdym wywołaniu. Test zmienia granice w tej samej sesji i potwierdza odmowę zwrócenia poprzedniej treści.
- Sprzątanie magazynu pomija obce katalogi i rozpoznaje generacje należące do właściwego vaulta.
- Uszkodzona baza zgłasza potrzebę `rebuild`; test potwierdza odzyskanie działania.
- Błędne typy konfiguracji, URL, wymiary wektorów i timeout dają kontrolowany błąd. Nie zastępują działającego indeksu.
- Długie akapity mają ograniczone fragmenty, kod i tabele zachowują spójność.
- Wyjście JSON działa przy konsoli bez Unicode. Dokumenty i konfiguracje pozostają UTF-8.
- Szablony referencyjne trafiają do `_skille/dokumentacja`, poza indeksem. Starszy plik Backpass kieruje do jednej aktualnej procedury.

## Niewykonane bramki

- Natywna instalacja i realny BGE-M3 na Windows; brak maszyny/VM Windows w tej sesji.
- Natywny Linux z GUI LM Studio i prawdziwym modelem; kontener potwierdza część Python/CLI/MCP.
- Pełne quick/full, podłączenie MCP w docelowym kliencie i scenariusze wszystkich 18 skilli wykonane przez agentów. Integracyjny test MCP nie jest testem UI konkretnego klienta.
- Zewnętrzne integracje i ich operacje zapisujące. Lokalne sprawdzenie ich instrukcji nie dowodzi działania kont użytkownika.
- Ostateczny wynik macierzy GitHub Actions oraz osobno zatwierdzony merge, tag i pełne wydanie.

SDK MCP/Pydantic emituje w czystym środowisku ostrzeżenie o definicji `lifespan`; inicjalizacja, wywołania narzędzi i zamknięcie sesji w testach przechodzą. Nie ukrywamy ostrzeżenia w logach.

Niezatwierdzone działania zewnętrzne i gotowy payload: [publikacja](publikacja-0.7.0.md). Szczegóły procedur: [macierz skilli](zgodnosc-skilli.md).
