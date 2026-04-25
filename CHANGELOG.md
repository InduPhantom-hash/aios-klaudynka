# CHANGELOG

Wszystkie zmiany w kolejnych wersjach AIOS-Klaudynki.

Format: [Semantic Versioning](https://semver.org/). Daty: RRRR-MM-DD.

---

## [0.4.0] - 2026-04-25 (beta)

### Dodane - plugin `aios`

- **6 nowych skilli** (plugin `aios` przechodzi z 6 do 12 skilli):
  - `kontynuuj` - wczytuje kontekst poprzedniej sesji z `_pamiec/aktualny.md` + transkrypt przez session_info MCP, otwiera biezaca sesje z gotowym briefingiem.
  - `dzien` - briefing dnia: kalendarz Google + aktywne projekty + sugestia focusu.
  - `core-update` - audyt aktualnosci dokumentow nawigacyjnych AIOS (me.md, vault-map.md, index.md) + update + sprzatanie + reindex Pinecone.
  - `research` - deep research przez Tavily na podany temat, wynik trafia do `Wiedza/<obszar>/Raw/` gotowy do `/aios:dodaj-do-wiki`.
  - `ingest-article` - wyciaga tresc artykulu lub strony z URL przez Tavily Extract i zapisuje do `Wiedza/<obszar>/Raw/`.
  - `zadania` - wyciaga zadania z aktualnej sesji i tworzy je w ClickUp (lista AIOS), z edycja inline przed wysylka.

- **Sekcja E - Blizniaki** w onboardingu `init`:
  - Pytania E10-E13 (opcjonalne, po E8): jakie narzedzia blizniacze uzytkownik ma (Linear, ClickUp, Notion, Airtable, Miro, inne), model synchronizacji (vault = truth, narzedzie = tracker), zakres synchronizacji, preferencje skillowa (auto-check vs. na zadanie).
  - Wygenerowany blok `## Blizniaki` w `me.md` - opis konfiguracji per-narzedzie.
  - Nowy szablon: `docs/szablony/blizniacy.md` - schemat bloku, dwa przyklady, uwagi dla AI.
  - Zaktualizowany `docs/szablony/me-template.md` - blok `## Blizniaki` przed `## Metadane`.
  - `vault-template/me.md` - dodany stub `## Blizniaki` (placeholder).
  - Nowe maksimum: **61 pytan** (57 obligatoryjnych + 4 opcjonalne E10-E13).

### Dodane - plugin `aios-meta` (nowy, opcjonalny)

- Nowy plugin niezalezny od `aios`, skupiony na higienie vaulta i synchronizacji z narzedzniami zewnetrznymi.
- **4 skille:**
  - `audyt-luk` - skanuje vault pod katem luk strukturalnych: brakujace README, puste Raw/, DREAM.md bez delty, aktywne.md bez "Nastepny krok".
  - `mcp-health` - sprawdza ktore MCP serwery z me.md odpowiadaja, a ktore leza; wywoluje lekkie operacje na kazdym i raportuje status.
  - `synchronizuj` - porownuje vault z bliznniakami (ClickUp, Linear, Notion, Airtable) i pokazuje rozjazdy - co jest w vaulcie a nie w blizniaku i odwrotnie.
  - `wizualizuj-vault` - generuje wizualny diagram struktury vaulta inline; opcjonalnie eksportuje do Miro.
- Instalacja opcjonalna (oddzielny krok po instalacji glownego `aios`).

### Zmienione

- `marketplace.json` - dodany wpis dla `aios-meta`, zaktualizowana wersja i opis.
- `CLAUDE.md` (vault-template) - dodana sekcja z 4 skillami `aios-meta` i instrukcja instalacji.

---

## [0.3.0] - 2026-04-22 (alpha, MVP)

Pierwsze publiczne wydanie.

### Dodane

- Plugin `aios` z 6 skillami: `init`, `sortuj`, `stworz-projekt`, `dodaj-do-wiki`, `szukaj`, `koniec-sesji`.
- Onboarding `init` - 57 pytan w 10 sekcjach (A-J + FIN), ~30-45 minut, wynik: `me.md` + konfiguracja vaulta.
- Szablon vaulta (`vault-template/`) - pelna struktura katalogow AIOS.
- 3 przyklady `me.md` dla archetypow: marketing-manager, developer, student-programowania.
- Dokumentacja: `INSTALL.md` (dla AI-wykonawcy, 6 krokow), `README.md`, `LICENSE` (MIT).
- Repo jako wlasny marketplace (`marketplace.json`): `InduPhantom-hash/aios-klaudynka`.
- Opis parsowania PDF profilowych (FRIS/Clifton) w `docs/parsowanie-pdf.md`.
- Szablony stylu komunikacji (10 plikow w `docs/szablony/style-komunikacji/`).

---

[0.4.0]: https://github.com/InduPhantom-hash/aios-klaudynka/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/InduPhantom-hash/aios-klaudynka/releases/tag/v0.3.0
