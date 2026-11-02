# AIOS-Klaudynka

![AIOS Klaudynka](assets/aios-klaudynka-banner.jpg)

Klaudynka przechowuje wiedzę, profil i zadania w plikach Markdown. Lokalny RAG wyszukuje fragmenty notatek po znaczeniu, korzystając z LanceDB i embeddingów BGE-M3. Źródłem prawdy pozostają pliki, a model AI możesz zmienić bez przenoszenia wiedzy.

**Stan: 0.7.0, kandydat do wydania.** 14 skilli podstawowych i 4 opcjonalne skille meta. Zakres: nowe instalacje. Migracja starszych vaultów pozostaje poza tym wydaniem.

## Co otrzymujesz

- Lokalny indeks wektorowy, pytania PL/EN, filtry obszaru i typu oraz wyniki ze wskazaniem źródła.
- Aktualizację indeksu po zatwierdzonych zmianach plików. Nieudana aktualizacja zachowuje ostatnią poprawną bazę; wyszukiwarka odmawia zwracania nieaktualnych fragmentów.
- Przenośny profil `me.md`, instrukcje `AGENTS.md`, pamięć sesji i zadania w `zadania.md`.
- Backpass: analizę logów i propozycje poprawy instrukcji wymagające zatwierdzenia.
- CLI oraz MCP. Brak MCP pozwala korzystać z CLI i procedur zapisanych w plikach.

Indeks i embeddingi działają lokalnie. **Wybrane fragmenty otrzymuje używany agent**, który może działać w chmurze. Instalacja wymaga pobrania zależności i modelu; lokalny RAG działa bez internetu po ich przygotowaniu. Research, kalendarze i trackery mają własne zależności sieciowe.

## Instalacja

Wklej swojemu agentowi:

> Zainstaluj mi AIOS-Klaudynkę z https://github.com/InduPhantom-hash/aios-klaudynka. Przeczytaj INSTALL.md i wykonaj kroki dla nowego vaulta z lokalnym RAG.

Wymagania: Python 3.11+, Git, LM Studio z modelem embeddingowym BGE-M3 oraz agent mający dostęp do plików i terminala. RAG stanowi domyślną ścieżkę instalacji. Brak modelu daje jawny status niepełnej konfiguracji; nadal można czytać pliki i używać lokalnego trackera.

Docelowe systemy to macOS, Windows i Linux. LM Studio wymaga m.in. Apple Silicon na macOS, a na x64 procesora z AVX2. Sprawdź [wymagania producenta](https://lmstudio.ai/docs/app/system-requirements). Nie deklarujemy obsługi wszystkich architektur.

**Dowody i ograniczenia:** [raport odbioru](docs/odbior-0.7.0.md) i [macierz 18 skilli](docs/zgodnosc-skilli.md). Testy automatyczne procedur nie dowodzą wykonania każdego skilla przez każdy model AI. Natywne komendy pluginu Claude Code oraz ręczne wywołanie pliku SKILL.md to odrębne ścieżki.

Instrukcje: [instalacja](INSTALL.md), [RAG i prywatność](docs/rag.md), [zmiany](CHANGELOG.md).

## Skille

| Skill core | Zastosowanie |
|---|---|
| `init` | Profil, onboarding quick/full, prywatność i pierwszy indeks |
| `backpass` | Propozycje poprawy instrukcji na podstawie logów |
| `pomysl-do-promptu` | Pomysł, wymagania i prompt do budowy produktu |
| `sortuj` | Porządkowanie wrzutek i aktualizacja indeksu |
| `stworz-projekt` | Struktura nowego projektu |
| `dodaj-do-wiki` | Opracowanie źródeł w strony wiedzy |
| `szukaj` | Lokalny RAG, odczyt źródeł i fallback plikowy |
| `koniec-sesji` | Zapis sesji i aktualizacja pamięci |
| `kontynuuj` | Powrót do ostatniego stanu pracy |
| `dzien` | Zadania dnia i opcjonalny kalendarz |
| `core-update` | Audyt nawigacji i odświeżenie lokalnego indeksu |
| `research` | Research wymagający dostępu do źródeł zewnętrznych |
| `ingest-article` | Pobranie artykułu i zapis źródła |
| `zadania` | Lokalny tracker i opcjonalny eksport |

Plugin `aios-meta` zawiera `audyt-luk`, `mcp-health`, `synchronizuj`, `wizualizuj-vault`. Doinstalowanie opcjonalne. Badanie zewnętrznych źródeł i zapis do zewnętrznych usług wymagają właściwej integracji oraz zgody na zapis.

## Pliki i przenośność

`vault-template/` zawiera strukturę wiedzy, pamięci i projektów, skrypty Python oraz konfigurację RAG. Instalator kopiuje też procedury skilli do `_skille/`. Profil powstaje podczas onboardingu. Indeks `.aios/rag/` i środowisko `.venv/` są danymi lokalnymi wykluczonymi z Git; nie kopiuj ich między komputerami.

Nie indeksujemy domyślnie stref prywatnych, transkryptów, archiwów, sekretów ani plików technicznych. Reguły możesz rozszerzyć w `_config/rag.json`. Nie włączamy automatycznej synchronizacji z chmurą ani harmonogramu indeksowania.

Przykładowe fikcyjne profile: [marketing](docs/przyklady/marketing-manager.md), [developer](docs/przyklady/developer.md), [student](docs/przyklady/student-programowania.md).

## Licencja

[MIT](LICENSE). Copyright (c) 2026 Jakub Orłowski. Wagi modelu i narzędzia zewnętrzne mają odrębne warunki dystrybucji; repozytorium nie zawiera wag ani danych autora.
