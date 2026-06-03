# Changelog

Wszystkie istotne zmiany w AIOS-Klaudynce. Format wg [Keep a Changelog](https://keepachangelog.com/pl/1.1.0/),
wersjonowanie wg [SemVer](https://semver.org/lang/pl/).

## [0.3.0] - 2026-04-22

Pierwszy publiczny release (MVP, alpha), doszlifowany pod publiczne udostępnienie.

### Added
- Plugin `aios` w formacie Claude Code marketplace (repo jest swoim własnym marketplace'em).
- 6 skilli: `init` (onboarding 57 pytań → `me.md`), `sortuj` (`_inbox/`), `stworz-projekt`,
  `dodaj-do-wiki` (Karpathy Raw→Wiki), `szukaj` (hierarchia + opcjonalny Pinecone fallback), `koniec-sesji`.
- Onboarding `/aios:init` - 57 pytań w 10 sekcjach (A-J + FIN), tryby szybki/standard/pełny, obsługa przerw.
- Szablon vaulta (`vault-template/`) w duchu File Over AI: `Projekty/`, `Wiedza/`, `Kalendarz/`,
  `_inbox/`, `_pamiec/`, `_brudnopis/`, `_Archiwum/`, `Kosz/` + `CLAUDE.md` + `me.md` placeholder.
- `vault-template/_pamiec/DREAM.md` - pusty skeleton pliku konsolidacji (sekcje: Aktywne projekty /
  Kluczowe decyzje / Wzorce pracy / Luki / Log konsolidacji), do którego odwołują się skille.
- 3 archetypy `me.md` (marketing manager, developer, student programowania).
- `INSTALL.md` - instrukcja dla AI-wykonawcy: 3 tryby instalacji (Claude Code / Cowork / zdegradowany),
  detekcja OS, troubleshooting, sekcja aktualizacji.
- Biblioteka stylów komunikacji (`docs/szablony/style-komunikacji/`) zasilająca Sekcję F onboardingu.
- Referencja parsowania profili FRIS / Clifton (`docs/parsowanie-pdf.md`) dla Sekcji C.
- Angielski TL;DR w README (zasięg międzynarodowy), reszta dokumentacji PL.
- Licencja MIT.

### Notes
- System jest **w pełni generyczny** - żadnych danych osobowych autora w skillach ani szablonie.
  Profil użytkownika powstaje wyłącznie z `me.md` (generowanego przez `/aios:init`), przykłady w skillach
  są neutralne, a konfiguracja Pinecone (nazwa indexu, mapa namespace) jest opisana jako przykład do dostosowania.
- Zgodne z aktualnym schematem marketplace Claude Code (`claude plugin validate` przechodzi).

[0.3.0]: https://github.com/InduPhantom-hash/aios-klaudynka/releases/tag/v0.3.0
