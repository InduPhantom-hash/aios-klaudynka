# AIOS-Klaudynka

![AIOS Klaudynka](assets/aios-klaudynka-banner.jpg)

Klaudynka przechowuje wiedzę, profil i zadania w plikach Markdown. Lokalny RAG wyszukuje fragmenty notatek po znaczeniu, korzystając z LanceDB i embeddingów BGE-M3. Źródłem prawdy pozostają pliki, a model AI możesz zmienić bez przenoszenia wiedzy.

**Stan: 0.8.0 (release).** 18 skilli uniwersalnych z jednolitym prefiksem `aios-` w ramach jednego głównego pluginu `aios`. Zakres: nowe instalacje. Wycofano `aios-meta` (funkcjonalności higieny i diagnostyki w pełni przejęte przez `aios-kustosz` oraz `aios-doctor`).

## Co otrzymujesz

- Lokalny indeks wektorowy, pytania PL/EN, filtry obszaru i typu oraz wyniki ze wskazaniem źródła.
- Aktualizację indeksu po zatwierdzonych zmianach plików. Nieudana aktualizacja zachowuje ostatnią poprawną bazę; wyszukiwarka odmawia zwracania nieaktualnych fragmentów.
- Przenośny profil `me.md`, instrukcje `AGENTS.md`, pamięć sesji i zadania w `zadania.md`.
- Nowoczesne inwarianty architektoniczne AIOS (bitemporalność, afirmatywna pamięć, Sandwich Prompting, Clean Context Window, Wayfinder z blokadami Frontier).
- Backpass: analizę logów i propozycje poprawy instrukcji wymagające zatwierdzenia.
- CLI oraz MCP. Brak MCP pozwala korzystać z CLI i procedur zapisanych w plikach.

Indeks i embeddingi działają lokalnie. **Wybrane fragmenty otrzymuje używany agent**, który może działać w chmurze. Instalacja wymaga pobrania zależności i modelu; lokalny RAG działa bez internetu po ich przygotowaniu. Research, kalendarze i trackery mają własne zależności sieciowe.

## Inwarianty architektoniczne AIOS

Wydanie 0.8.0 wdraża zintegrowane inwarianty architektoniczne nowoczesnego ekosystemu AIOS:
- **File Over AI & Code Over AI**: Pliki Markdown są nadrzędnym źródłem prawdy. Do operacji mechanicznych (wyszukiwanie tekstu, sprawdzanie YAML, walidacja ISO-8601, testy) używany jest deterministyczny kod, nie pętle myślowe LLM.
- **Bitemporalność faktów i notatek**: Rozdzielenie czasu zapisu (Transaction Time: nagłówek / `data_wpisu` ISO-8601) od czasu obowiązywania w świecie realnym (Valid Time: pole `status: aktywny | obalony | zastąpiony przez [[link]]`).
- **Zasada Afirmatywnej Pamięci**: Zapis reguł i lekcji proceduralnych w formie pozytywnej (opis stanu pożądanego zamiast gołej negacji), eliminujący efekt Różowego Słonia w modelach językowych.
- **Sandwich Prompting**: Trójstrefowy podział promptów orkiestrujących subagentów zapobiegający zjawisku Lost in the Middle: Head (10-15% budżetu tokenów: tożsamość, inwarianty P0, dozwolone ścieżki), Belly (70-80%: kontekst zadania, surowe dane, diffy Git), Tail (10-15%: re-ewokacja inwariantów, zakaz cheatów, kontrakt formatu odpowiedzi, CTA).
- **Clean Context Window (`messages: []`)**: Każda kolejna faza cyklu inżynieryjnego oraz nowa sesja subagenta bezwzględnie startuje w świeżym procesie z czystą historią konwersacji, pobierając stan wyłącznie z plików na dysku.
- **Wayfinder & Frontier Locks**: Złożone zadania dekomponowane na bilety decyzyjne z blokadami `(Blokuje: X)` i `(Zablokowane przez: Y)`. Agent podejmuje wyłącznie zadania z Frontiera (w pełni odblokowane).
- **Higiena pamięci sesji (limit <= 3 KB)**: Plik bufora sesji `_pamiec/aktualny.md` objęty jest twardym limitem 3072 bajtów, co zapobiega puchnięciu promptu startowego.
- **Audyt Git i ochrona limitów**: Wymuszenie `git -c core.quotepath=off status --porcelain -uall` oraz wykluczenie baz danych i dużych plików binarnych (limit 100 MB).

## Instalacja

Wklej swojemu agentowi:

> Zainstaluj mi AIOS-Klaudynkę z https://github.com/InduPhantom-hash/aios-klaudynka. Przeczytaj INSTALL.md i wykonaj kroki dla nowego vaulta z lokalnym RAG.

Wymagania: Python 3.11+, Git, LM Studio z modelem embeddingowym BGE-M3 oraz agent mający dostęp do plików i terminala. RAG stanowi domyślną ścieżkę instalacji. Brak modelu daje jawny status niepełnej konfiguracji; nadal można czytać pliki i używać lokalnego trackera.

Docelowe systemy to macOS, Windows i Linux. LM Studio wymaga m.in. Apple Silicon na macOS, a na x64 procesora z AVX2. Sprawdź [wymagania producenta](https://lmstudio.ai/docs/app/system-requirements). Nie deklarujemy obsługi wszystkich architektur.

**Dowody i ograniczenia:** [raport odbioru](docs/odbior-0.7.0.md) i [macierz 18 skilli](docs/zgodnosc-skilli.md). Testy automatyczne procedur nie dowodzą wykonania każdego skilla przez każdy model AI. Natywne komendy pluginu Claude Code oraz ręczne wywołanie pliku SKILL.md to odrębne ścieżki.

Instrukcje: [instalacja](INSTALL.md), [RAG i prywatność](docs/rag.md), [zmiany](CHANGELOG.md).

## Skille

Wydanie 0.8.0 zawiera 18 skilli uniwersalnych z jednolitym prefiksem `aios-` zorganizowanych w jednym pluginie `aios`:

| Skill | Zastosowanie |
|---|---|
| `aios-init` | Profil, onboarding quick/full, prywatność i pierwszy indeks RAG |
| `aios-szukaj` | Lokalny RAG, odczyt źródeł i fallback plikowy |
| `aios-dzien` | Zadania dnia z lokalnych projektów zadania.md i opcjonalny kalendarz |
| `aios-sortuj` | Porządkowanie wrzutek z _inbox/ i aktualizacja indeksu |
| `aios-stworz-projekt` | Struktura nowego projektu (README, zadania, decyzje, Raw) |
| `aios-koniec-sesji` | Zapis sesji, wniosków i aktualizacja pamięci sesji (limit 3 KB) oraz Lesson Mining |
| `aios-kontynuuj` | Powrót do ostatniego stanu pracy z aktualny.md |
| `aios-kustosz` | Zintegrowany strażnik spójności vaulta: audyt luk, linter CLI dat i mapa bazy |
| `aios-doctor` | Dashboard kondycji środowiska: testy MCP, konfiguracja i synchronizacja |
| `aios-backpass` | Propozycje poprawy instrukcji AGENTS.md metodą Gradient Descent |
| `aios-debata` | Próba ognia: dysputa sokratejska i Debata Oksfordzka agentów |
| `aios-wyjasnij` | Wyjaśnianie trudnych pojęć prostym językiem (metoda Feynmana) i lokalizacja luk w zrozumieniu |
| `aios-anonimizacja` | Tarcza ochrony prywatności przed chmurą i anonimizacja PII |
| `aios-weryfikacja` | Bramka QA redukująca over-reliance przed tworzeniem faktów |
| `aios-data-analysis` | 7-fazowa strukturalna analiza danych w stylu senior analyst |
| `aios-research-faktow` | Rygorystyczny research faktów (SIFT, RADAR, Evidence Brief) |
| `aios-research-rynkowy` | Analiza rynku i literatury z wymuszeniem szukania dowodów podważających |
| `aios-grilling` | Bezkompromisowy stress-test pomysłów, planów i założeń projektowych |

Dotychczasowy plugin `aios-meta` został wycofany; jego zadania w pełni przejęły `aios-kustosz` oraz `aios-doctor`. Wszystkie skille znajdują się teraz w jednym pakiecie `plugins/aios`.

## Pliki i przenośność

`vault-template/` zawiera strukturę wiedzy, pamięci i projektów, skrypty Python oraz konfigurację RAG. Instalator kopiuje też procedury skilli do `_skille/`. Profil powstaje podczas onboardingu. Indeks `.aios/rag/` i środowisko `.venv/` są danymi lokalnymi wykluczonymi z Git; nie kopiuj ich między komputerami.

Nie indeksujemy domyślnie stref prywatnych, transkryptów, archiwów, sekretów ani plików technicznych. Reguły możesz rozszerzyć w `_config/rag.json`. Nie włączamy automatycznej synchronizacji z chmurą ani harmonogramu indeksowania.

Przykładowe fikcyjne profile: [marketing](docs/przyklady/marketing-manager.md), [developer](docs/przyklady/developer.md), [student](docs/przyklady/student-programowania.md).

## Licencja

[MIT](LICENSE). Copyright (c) 2026 Jakub Orłowski. Wagi modelu i narzędzia zewnętrzne mają odrębne warunki dystrybucji; repozytorium nie zawiera wag ani danych autora.
