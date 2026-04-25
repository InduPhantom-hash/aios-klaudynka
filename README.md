# AIOS-Klaudynka

> Personalny Agentic OS dla AI-first użytkownika. Twoje AI uczy się ciebie z **twojego** pliku `me.md`, a nie z jakiegoś generycznego promptu.

**Status:** β (beta, v0.4.0). 12 skilli + opcjonalny plugin `aios-meta`. Publiczne repo pod licencją MIT.

**Dla kogo:** marketing manager, developer, student programowania, albo ktokolwiek kto pracuje z Claude / ChatGPT / Gemini / LM Studio codziennie i chce żeby AI przestało gadać w kółko te same rzeczy i zaczęło rozumieć **jak** z nim rozmawiać.

---

## Co to robi

1. **Onboarding `/aios:init`** - do 61 pytań w 10 sekcjach, 30-45 minut. Wypełniasz je rozmową z AI. Wynik: twój `me.md` - przenośny profil, który każde AI czyta na starcie sesji. Od v0.4: Sekcja E opcjonalnie pyta o narzędzia bliźniacze (ClickUp, Linear, Notion itp.) i generuje blok `## Bliźniaki` w `me.md`.

2. **Vault AIOS** - lokalna baza plików `.md` w duchu **File Over AI**: pliki są trwałe, AI jest wymienne. Katalogi: `Projekty/`, `Wiedza/`, `Kalendarz/`, `_inbox/`, `_pamiec/`, `_brudnopis/`, `_Archiwum/`, `Kosz/`.

3. **12 skilli** w pluginie `aios` (slash commands w Claude Code, Cowork, albo wywoływanych słownie w Cursor/Codex/Gemini):

| Skill | Co robi |
|-------|---------|
| `/aios:init` | Onboarding - ankieta → `me.md` + konfiguracja vaulta. |
| `/aios:sortuj` | Interaktywne sortowanie `_inbox/` - AI proponuje 3-4 opcje, ty decydujesz literą. |
| `/aios:stworz-projekt` | Promocja wątku z `_brudnopis/` do pełnej struktury `Projekty/<kategoria>/<nazwa>/`. |
| `/aios:dodaj-do-wiki` | Karpathy pipeline: surowiec z `Wiedza/Raw/` → strona w `Wiedza/Wiki/`. |
| `/aios:szukaj` | Hierarchiczne wyszukiwanie (index.md → pełny tekst → semantic fallback). |
| `/aios:koniec-sesji` | Zapis transkryptu do `_brudnopis/`, aktualizacja `_pamiec/aktualny.md`. |
| `/aios:kontynuuj` | Wczytuje kontekst poprzedniej sesji - otwiera bieżącą z gotowym briefingiem. |
| `/aios:dzien` | Briefing dnia: kalendarz Google + aktywne projekty + sugestia focusu. |
| `/aios:core-update` | Audyt + update dokumentów nawigacyjnych AIOS, sprzątanie, reindex Pinecone. |
| `/aios:research` | Deep research przez Tavily → wynik do `Wiedza/<obszar>/Raw/`. |
| `/aios:ingest-article` | Wyciąga treść artykułu z URL → zapisuje do `Wiedza/<obszar>/Raw/`. |
| `/aios:zadania` | Wyciąga zadania z sesji → tworzy w ClickUp (lista AIOS) po akceptacji. |

4. **Plugin `aios-meta`** (opcjonalny) - 4 skille do higieny vaulta i synchronizacji z narzędziami zewnętrznymi:

| Skill | Co robi |
|-------|---------|
| `/aios-meta:audyt-luk` | Skanuje vault pod kątem luk strukturalnych (brakujące README, puste Raw/ itp.). |
| `/aios-meta:mcp-health` | Sprawdza które MCP z `me.md` odpowiadają, a które leżą. |
| `/aios-meta:synchronizuj` | Porównuje vault z bliźniakami (ClickUp, Linear, Notion) - pokazuje rozjazdy. |
| `/aios-meta:wizualizuj-vault` | Generuje diagram struktury vaulta inline, opcjonalnie eksportuje do Miro. |

---

## Filozofia

**File Over AI.** Twój vault to pliki `.md` w systemie plików. Możesz je otworzyć w Obsidianie, w `cat`-em, w Notesie, w VS Code. AI jest narzędziem do ich pielęgnacji - nie ich właścicielem. Wymieniasz AI (z Claude na Gemini, z Coworka na Cursora) - vault zostaje nietknięty.

**Twoje granice, twoje reguły.** Onboarding nie sprzedaje "najlepszego stylu". Sekcja F zadaje 10 pytań o to, **jak lubisz rozmawiać** (konkret vs kontekst, zwięzłość vs pełny obraz, spór vs współpraca, ton emoji, humor, cytowanie profilu, proaktywność, format odpowiedzi), i z odpowiedzi składa **twoje** hard rules. Każde kolejne AI czyta je na starcie sesji.

**Privacy by design.** Sekcja H (warunkowa) wydziela strefę prywatną z osobnymi regułami cytowania i proaktywności. Opcjonalnie poza gitem.

**α = alpha.** Plugin w formacie Claude Code marketplace, szablon vaulta, 6 skilli. Bez mechanizmu auto-update, bez telemetrii, bez subskrypcji. Upgrade = reinstall (instrukcja w `INSTALL.md`, sekcja "Aktualizacja").

---

## Instalacja

**Claude Code (przetestowane):**

```
/plugin marketplace add InduPhantom-hash/aios-klaudynka
/plugin install aios@aios-klaudynka
/aios:init
```

Opcjonalnie (plugin meta-tools):

```
/plugin install aios-meta@aios-klaudynka
```

**Cowork (częściowo przetestowane):** zbuduj `.plugin` zip z `plugins/aios/` i wgraj w UI Coworka. Szczegóły: `INSTALL.md` sekcja 4B. Dla `aios-meta` - analogicznie z `plugins/aios-meta/`.

**Cursor / Codex / Gemini (tryb zdegradowany, nieprzetestowane):** skopiuj `plugins/aios/` do `_skille/aios/` w swoim vaulcie. Triggery wywołujesz słownie ("wykonaj aios-init").

**Pełna instrukcja:** [`INSTALL.md`](./INSTALL.md). Zakłada usera od zera - bez git, bez konta GitHub.

---

## Struktura repo

```
aios-klaudynka/
├── .claude-plugin/
│   └── marketplace.json           # Repo jest swoim wlasnym marketplace'em
├── plugins/
│   ├── aios/                      # Plugin Claude Code - core (12 skilli)
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       ├── init/              # /aios:init (+ pytania.md)
│   │       ├── sortuj/            # /aios:sortuj
│   │       ├── stworz-projekt/    # /aios:stworz-projekt
│   │       ├── dodaj-do-wiki/     # /aios:dodaj-do-wiki
│   │       ├── szukaj/            # /aios:szukaj
│   │       ├── koniec-sesji/      # /aios:koniec-sesji
│   │       ├── kontynuuj/         # /aios:kontynuuj
│   │       ├── dzien/             # /aios:dzien
│   │       ├── core-update/       # /aios:core-update
│   │       ├── research/          # /aios:research
│   │       ├── ingest-article/    # /aios:ingest-article
│   │       └── zadania/           # /aios:zadania
│   └── aios-meta/                 # Plugin opcjonalny - higiena vaulta (4 skilli)
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           ├── audyt-luk/         # /aios-meta:audyt-luk
│           ├── mcp-health/        # /aios-meta:mcp-health
│           ├── synchronizuj/      # /aios-meta:synchronizuj
│           └── wizualizuj-vault/  # /aios-meta:wizualizuj-vault
├── vault-template/                # Szablon vaulta kopiowany do $VAULT_PATH
│   ├── CLAUDE.md
│   ├── me.md                      # Placeholder, wypelniany przez /aios:init
│   ├── _inbox/
│   ├── _brudnopis/
│   ├── _pamiec/
│   ├── _Archiwum/
│   ├── Kosz/
│   ├── Projekty/
│   ├── Wiedza/
│   └── Kalendarz/
├── docs/
│   ├── przyklady/                 # 3 archetypy me.md
│   │   ├── marketing-manager.md
│   │   ├── developer.md
│   │   └── student-programowania.md
│   ├── szablony/
│   │   ├── me-template.md         # Pelny szablon me.md z warunkami IF/LOOP
│   │   ├── blizniacy.md           # Schemat bloku ## Blizniaki w me.md
│   │   ├── prywatnosc.md          # Szablon sekcji H (prywatnosc)
│   │   └── style-komunikacji/     # 10 szablonow sekcji F (styl komunikacji)
│   └── parsowanie-pdf.md          # Referencja dla AI przy Sekcji C (FRIS/Clifton)
├── CHANGELOG.md                   # Historia zmian
├── INSTALL.md                     # Instrukcja dla AI-wykonawcy
├── README.md                      # ten plik
└── LICENSE                        # MIT
```

---

## Wymagania

- **Runtime:** Claude Code (najlepiej), Cowork (OK), Cursor / Codex / Gemini CLI (tryb zdegradowany, słowne triggery).
- **System:** macOS / Linux / Windows (WSL). Przetestowane: macOS.
- **Git:** instaluje się w trakcie `INSTALL.md` jeśli brak.
- **Konto GitHub:** nie jest wymagane (repo jest publiczne).

---

## Przykłady `me.md`

Zanim przejdziesz onboarding, zobacz jak wygląda `me.md` innych archetypów. To pomoże ci zrozumieć **co** generuje `/aios:init`:

- [marketing-manager](./docs/przyklady/marketing-manager.md) - lead z agencji, manages team, mix strategia+egzekucja.
- [developer](./docs/przyklady/developer.md) - senior backend dev, Go / Python, ~10 lat doświadczenia.
- [student-programowania](./docs/przyklady/student-programowania.md) - pierwszy rok, uczy się Pythona, szukający patternów.

Żaden z nich nie jest "właściwy". Twój `me.md` będzie inny - bo różnisz się od nich, i bo różne AI będzie inaczej z tobą rozmawiać niż z nimi.

---

## Roadmapa

**v0.3 (alpha, 2026-04-22):** pierwsze publiczne wydanie. 6 skilli, onboarding 57 pytań, 3 archetypy, PL-only.

**v0.4 (beta, 2026-04-25):** ten release.
- 12 skilli w `aios` (kontynuuj, dzien, core-update, research, ingest-article, zadania).
- Sekcja E Bliźniaki w onboardingu (E10-E13 opcjonalne, 61 max pytań).
- Nowy plugin `aios-meta` (4 skilli: audyt-luk, mcp-health, synchronizuj, wizualizuj-vault).

**v0.5 (planowane):**
- Tryb `/aios:init --quick` (tylko A+B+D+FIN, reszta default, ~10 min).
- Wynieść hardcoded ścieżki (np. `Vibe-coding/` w `stworz-projekt`) jako konfigurowalne w `me.md`.
- EN translation szablonów i skilli.

**v1.0 (cel):** production-ready dla co najmniej 3 użytkowników z różnych archetypów, pełne testy ścieżek Cowork i zdegradowanych, dokumentacja EN+PL.

---

## Dlaczego "Klaudynka"

Wewnętrzna nazwa autora pre-release. Zanim nazwiemy coś sensownie, używamy imienia. Tak zostało.

**Projekt autorski, nie oficjalny Anthropic.**

---

## Licencja

MIT. Copyright (c) 2026 Jakub Orłowski.

Używaj, forkuj, modyfikuj, komercjalizuj - zachowaj copyright notice.

---

## Zgłaszanie problemów

GitHub Issues w tym repo. Pisz po polsku albo po angielsku.

**Co pomaga zdiagnozować:**

1. Wersja AIOS-Klaudynki (z `/plugin list` albo sprawdź commit w klonie).
2. Środowisko: `$INSTALL_MODE` (cc / cowork / degraded), OS, wersja AI (Claude Code 1.x, Cowork research preview itp.).
3. Który krok z `INSTALL.md` się wywalił - numer sekcji.
4. Pełny tekst błędu. Nie parafrazuj.

---

## Autor

Jakub Orłowski - [github.com/InduPhantom-hash](https://github.com/InduPhantom-hash)

Kontakt: przez GitHub Issues tego repo.
