# AIOS-Klaudynka

![AIOS Klaudynka - Personal Agentic OS](./assets/aios-klaudynka-banner.jpg)

> Personalny Agentic OS oparty na plikach (`File Over AI`) i deterministycznych skryptach (`Code Over AI`). Twoje AI uczy się ciebie z **twojego** profilu `me.md`, wykonuje zadania w lokalnych plikach Markdown bez zbędnych kosztów API i pozwala wymieniać modele AI bez utraty wiedzy.

**Status:** v0.5.0 (Release). 13 skilli core + opcjonalny plugin `aios-meta`. Publiczne repozytorium pod licencją MIT.

**Dla kogo:** [Marketing Manager](docs/przyklady/marketing-manager.md), [Developer](docs/przyklady/developer.md), [Student](docs/przyklady/student-programowania.md), produktowiec - każdy, kto pracuje z AI (Antigravity, Claude, Gemini CLI, Cursor, Codex, OpenHand) i chce, aby system natychmiast rozumiał jego styl pracy oraz porządkował wiedzę i zadania lokalnie.

---

## Co wyróżnia Klaudynkę (Filozofia Systemu)

1. **File Over AI:** Twój vault to trwałe pliki `.md` na Twoim dysku. Możesz je czytać w Obsidianie, VS Code, terminalu czy edytorze tekstu. AI jest narzędziem do ich pielęgnacji - nie właścicielem Twoich danych.
2. **Code Over AI:** Mechaniczne operacje (agregacja zadań, przeszukiwanie plików, porządkowanie struktur) wykonują natywne komendy systemowe (`grep`/`ripgrep`/`find`/skrypty). AI nie marnuje Twoich tokenów na pętle myślenia tam, gdzie wystarczy prosty skrypt.
3. **Natywny AIOS Task Tracker (100% Offline):** Wszystkie zadania żyją w prostych plikach `zadania.md` wewnątrz Twoich projektów. Brak wymogu posiadania płatnych kont w zewnętrznych narzędziach.
4. **Szybki Onboarding (`/aios:init --quick`):** 10-15-minutowy proces (12 kluczowych pytań) buduje Twój przenośny profil `me.md` oraz zasady komunikacji. Dostępny jest także tryb pełny (`--full`).
5. **Wieloplatformowość:** Działa natywnie z Antigravity, Claude Code, Gemini CLI, Cursorem, Codextem i OpenHand dzięki ujednoliconemu plikowi `AGENTS.md` oraz `bootstrap-prompt.md`.

---

## Lista Skilli (Plugin `aios` - 13 skilli)

| Skill | Co robi |
|---|---|
| `/aios:init` | Onboarding - buduje profil `me.md`, strukturę vaulta i Task Trackera (`--quick` / `--full`). |
| `/aios:sortuj` | Interaktywne sortowanie wrzutek z `_inbox/` do docelowych folderów. |
| `/aios:stworz-projekt` | Promocja pomysłu z `_brudnopis/` do pełnej struktury projektu w `Projekty/`. |
| `/aios:pomysl-do-promptu` | **NOWOŚĆ:** Prowadzenie od surowego pomysłu do specyfikacji PRD, makiet i promptu dla Vibe Coding. |
| `/aios:dodaj-do-wiki` | Pipeline wiedzy (metoda Karpathy): surowiec z `Wiedza/Raw/` → strona w `Wiedza/Wiki/`. |
| `/aios:szukaj` | Hierarchiczne i skryptowe wyszukiwanie w vaulcie. |
| `/aios:koniec-sesji` | Zapis transkryptu do `_brudnopis/` i aktualizacja pamięci `_pamiec/aktualny.md`. |
| `/aios:kontynuuj` | Wczytuje kontekst z poprzedniej sesji z gotowym briefingiem. |
| `/aios:dzien` | Briefing dnia: kalendarze Google + aktywne zadania z `zadania.md` (ripgrep) + focus. |
| `/aios:core-update` | Audyt i aktualizacja plików nawigacyjnych AIOS, higiena vaulta. |
| `/aios:research` | Deep research → wynik trafia do `Wiedza/<obszar>/Raw/`. |
| `/aios:ingest-article` | Pobieranie i czyszczenie artykułu z podanego URL do `Wiedza/<obszar>/Raw/`. |
| `/aios:zadania` | Wyciąganie zadań z sesji i zapis do lokalnego `Projekty/<nazwa>/zadania.md` (z opcją ClickUp/Notion). |

### Opcjonalny Plugin `aios-meta` (4 skille higieniczne)
- `/aios-meta:audyt-luk` - skanuje vault pod kątem brakujących plików README i spójności.
- `/aios-meta:mcp-health` - weryfikacja dostępności serwerów MCP.
- `/aios-meta:synchronizuj` - porównywanie stanu vaulta z zewnętrznymi narzędziami.
- `/aios-meta:wizualizuj-vault` - generowanie diagramu drzewa vaulta.

---

## Nowa Struktura Vaulta (`vault-template/`)

```text
AIOS-Vault/
├── me.md                  ← profil użytkownika i hard rules (generowany przez /aios:init)
├── AGENTS.md              ← SSOT instrukcji operacyjnych dla wszystkich agentów AI
├── CLAUDE.md              ← 1-liniowy redirect do AGENTS.md
├── bootstrap-prompt.md    ← prompt startowy dla środowisk AI
├── vault-map.md           ← mapa sitemap vaulta
├── _szablony/             ← szablony zadań, briefów i rejestru decyzji
├── _inbox/                ← skrzynka wrzutowa na surowe notatki
├── _brudnopis/            ← transkrypty i dzienne myślenie na głos
├── _pamiec/               ← skonsolidowana pamięć (aktualny.md, DREAM.md)
├── _Archiwum/             ← zarchiwizowane projekty i dead-endy
├── Kosz/                  ← bufor przed usunięciem
├── Projekty/              ← projekty z podziałem na kategorie (z plikami zadania.md)
└── Wiedza/                ← baza wiedzy (Raw/ oraz Wiki/)
```

---

## Szybki start (Instalacja jednym promptem)

Wklej poniższe polecenie swojemu agentowi AI (Claude Code, Cursor, Antigravity, Gemini CLI):

> `Zainstaluj mi AIOS-Klaudynkę z https://github.com/InduPhantom-hash/aios-klaudynka. Przeczytaj INSTALL.md i wykonaj kroki.`

AI pobierze szablon, przygotuje strukturę i uruchomi 10-15-minutowy onboarding (`/aios:init --quick`), który zbuduje Twój spersonalizowany profil `me.md`.

### Wymagania wstępne
- Dowolne środowisko Agentic AI z dostępem do plików i konsoli (Claude Code, Cursor, Antigravity, Gemini CLI, OpenHand).
- Zainstalowany `git`.
- Opcjonalnie: darmowa aplikacja [Obsidian](https://obsidian.md/) lub edytor Markdown do przeglądania bazy wiedzy.

Pełna instrukcja techniczna krok po kroku oraz rozwiązywanie problemów: [`INSTALL.md`](./INSTALL.md).

---

## Licencja

MIT. Copyright (c) 2026 Jakub Orłowski.

