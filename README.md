# AIOS-Klaudynka

> Personalny Agentic OS dla AI-first użytkownika. Twoje AI uczy się ciebie z **twojego** pliku `me.md`, a nie z jakiegoś generycznego promptu.

**Status:** α (alpha). MVP po onboardingu na testerach. Publiczne repo pod licencją MIT.

**Dla kogo:** marketing manager, developer, student programowania, albo ktokolwiek kto pracuje z Claude / ChatGPT / Gemini / LM Studio codziennie i chce żeby AI przestało gadać w kółko te same rzeczy i zaczęło rozumieć **jak** z nim rozmawiać.

---

> **🇬🇧 In short (English).** AIOS-Klaudynka is a personal "Agentic OS" built on plain `.md` files (*File Over AI*). A `/aios:init` onboarding (57 questions) generates your portable `me.md` profile, so any AI - Claude, ChatGPT, Gemini, LM Studio - reads *how you work* at the start of every session. Ships as a Claude Code plugin + a vault template + 6 skills. **Polish-first** (the onboarding and skills are written in Polish), MIT-licensed, and meant to be forked and adapted to yourself.
>
> **Install (Claude Code):** `/plugin marketplace add InduPhantom-hash/aios-klaudynka` → `/plugin install aios@aios-klaudynka` → `/aios:init`. Full documentation below is in Polish.

---

## Co to robi

1. **Onboarding `/aios:init`** - 57 pytań w 10 sekcjach, 30-45 minut. Wypełniasz je rozmową z AI. Wynik: twój `me.md` - przenośny profil, który każde AI czyta na starcie sesji.

2. **Vault AIOS** - lokalna baza plików `.md` w duchu **File Over AI**: pliki są trwałe, AI jest wymienne. Katalogi: `Projekty/`, `Wiedza/`, `Kalendarz/`, `_inbox/`, `_pamiec/`, `_brudnopis/`, `_Archiwum/`, `Kosz/`.

3. **6 skilli** (slash commands w Claude Code, Cowork, albo wywoływanych słownie w Cursor/Codex/Gemini):

| Skill | Co robi |
|-------|---------|
| `/aios:init` | Onboarding - ankieta → `me.md` + konfiguracja vaulta. |
| `/aios:sortuj` | Interaktywne sortowanie `_inbox/` - AI proponuje 3-4 opcje, ty decydujesz literą. |
| `/aios:stworz-projekt` | Promocja wątku z `_brudnopis/` do pełnej struktury `Projekty/<kategoria>/<nazwa>/`. |
| `/aios:dodaj-do-wiki` | Karpathy pipeline: surowiec z `Wiedza/Raw/` → strona w `Wiedza/Wiki/`. |
| `/aios:szukaj` | Hierarchiczne wyszukiwanie (index.md → pełny tekst → semantic fallback). |
| `/aios:koniec-sesji` | Zapis transkryptu do `_brudnopis/`, aktualizacja `_pamiec/aktualny.md`. |

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

**Cowork (częściowo przetestowane):** zbuduj `.plugin` zip z `plugins/aios/` i wgraj w UI Coworka. Szczegóły: `INSTALL.md` sekcja 4B.

**Cursor / Codex / Gemini (tryb zdegradowany, nieprzetestowane):** skopiuj `plugins/aios/` do `_skille/aios/` w swoim vaulcie. Triggery wywołujesz słownie ("wykonaj aios-init").

**Pełna instrukcja:** [`INSTALL.md`](./INSTALL.md). Zakłada usera od zera - bez git, bez konta GitHub.

---

## Struktura repo

```
aios-klaudynka/
├── .claude-plugin/
│   └── marketplace.json           # Repo jest swoim własnym marketplace'em
├── plugins/
│   └── aios/                      # Plugin Claude Code
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── skills/
│           ├── init/              # /aios:init
│           ├── sortuj/            # /aios:sortuj
│           ├── stworz-projekt/    # /aios:stworz-projekt
│           ├── dodaj-do-wiki/     # /aios:dodaj-do-wiki
│           ├── szukaj/            # /aios:szukaj
│           └── koniec-sesji/      # /aios:koniec-sesji
├── vault-template/                # Szablon vaulta kopiowany do $VAULT_PATH
│   ├── CLAUDE.md
│   ├── me.md                      # Placeholder, wypełniany przez /aios:init
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
│   └── parsowanie-pdf.md          # Referencja dla AI przy Sekcji C (FRIS/Clifton)
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

**v0.3 (MVP, 2026-04-22):** ten release. 6 skilli, onboarding 57 pytań, 3 archetypy, PL-only.

**v0.4 (planowane):**
- Tryb `/aios:init --quick` (tylko A+B+D+FIN, reszta default, ~10 min).
- EN translation szablonów i skilli.
- Własne auto-update (`/aios:update`) - obecnie odrzucone, do rozważenia po testach MVP.

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
