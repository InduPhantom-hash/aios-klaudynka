---
name: sortuj
description: Interaktywne sortowanie _inbox - przegladasz plik po pliku, AIOS proponuje 3-4 opcje docelowego miejsca, ty decydujesz 1 litera, AIOS przenosi + aktualizuje index.md. Triggery - "/aios:sortuj", "sortuj inbox", "poukladaj inbox".
---

# sortuj

## Cel

Rozladowac `_inbox/` w trybie **rozmowy** - nie w trybie wielkiego wyboru na start.

Filozofia: rozbic ciezar organizacyjny na atomowe decyzje. Ty mowisz **jedna litere**,
AIOS wykonuje wszystko reszte (mv + update index + metadata).

## Triggery

- `/aios:sortuj` - przejdz po wszystkich plikach w `_inbox/` (poza README.md, .gitkeep)
- `/sortuj <plik>` - tylko jeden konkretny plik z inbox
- `/sortuj --top N` - tylko N najstarszych plikow
- `/sortuj --dzisiaj` - tylko pliki z dzisiejsza data modyfikacji

## Procedura

### Krok 1: Lista plikow

Przeczytaj `_inbox/` (bez ukrytych, bez README.md). Jesli pusto - zglos i zakoncz.

```
_inbox/ ma 4 pliki do posortowania:
  1. mapa-ai-tools-2026.md  (3.2 KB, 20.04.2026)
  2. konferencja-infoshare.txt  (1.8 KB, 19.04.2026)
  3. pomysl-fiszki.md  (0.4 KB, 18.04.2026)
  4. screenshot-figma-layout.png  (120 KB, 20.04.2026)

Ide po kolei. Mozesz przerwac w dowolnym momencie przez "stop".
```

### Krok 2: Per-plik

Dla kazdego:

1. **Odczytaj zawartosc** (pierwsze ~1500 znakow + frontmatter jesli jest).
   Dla obrazkow/PDF - odczyt multimodal (jesli mozliwy) albo transcript z OCR.

2. **Przeanalizuj tresc** - jaki to typ informacji?
   - **Wiedza** (cross-project, patterny, teorie) → sugeruj `Wiedza/<obszar>/Raw/` lub `Wiki/`
   - **Projektowe** (specyficzne dla konkretnego projektu) → sugeruj `Projekty/<kategoria>/<projekt>/`
   - **Nowy pomysl** (nie pasuje do istniejacych) → sugeruj stworzenie projektu
   - **Szum** (mem, przypadkowy download) → sugeruj Kosz/

3. **Pokaz userowi format:**

```
─── [1/4] mapa-ai-tools-2026.md ───
Preview (pierwsze 3 linie):
  # Mapa narzedzi AI 2026
  > Claude, ChatGPT, Gemini, perplexity, LM Studio...
  > Porownanie, uzytki, koszty.

Moja klasyfikacja: wiedza o AI, surowiec do przerobienia.

Opcje:
  [a] Wiedza/AI/Raw/              (surowiec - potem /dodaj-do-wiki)
  [b] Wiedza/AI/Wiki/             (wgraj bez przerobki)
  [c] Projekty/Vibe-coding/?      (jesli to dla konkretnego projektu - ktorego?)
  [d] Nowy projekt                (jesli to zalazek czegos wiekszego)
  [e] Kosz                        (usun)
  [s] Skip                        (zostaw w _inbox, decyzja pozniej)

Twoja decyzja?
```

4. **Czekaj na user.** Akceptuj:
   - jedna litera (`a`, `b`, `c`, `d`, `e`, `s`, `stop`)
   - albo instrukcja slowna ("rozbij na 2 pliki - AI tools do Wiki, Claude-specific do Raw")
   - albo pytanie ("co bedzie w c?")

5. **Wykonaj akcje:**

   **Opcja a (Raw/):**
   ```
   mv _inbox/mapa-ai-tools-2026.md Wiedza/AI/Raw/2026-04-20-mapa-ai-tools.md
   # Dodaj frontmatter jesli brak:
   ---
   title: "Mapa narzedzi AI 2026"
   source: "_inbox"
   ingested: 2026-04-20
   ---
   ```
   Update `Wiedza/AI/index.md` (lista Raw): dodaj wpis.

   **Opcja b (Wiki/):** analogicznie, do `Wiki/`.

   **Opcja c (projekt):** zapytaj ktory projekt (lista z `Projekty/<kategoria>/`).
   Po wyborze: mv do projekt/ + update README projektu.

   **Opcja d (nowy projekt):** wywolaj `/aios:stworz-projekt` inline - zapytaj nazwe i
   kategorie. Po utworzeniu projektu mv pliku do nowego folderu.

   **Opcja e (Kosz):** mv do `Kosz/<YYYY-MM-DD>-<filename>`. User sam sobie usunie.

   **Opcja s (skip):** nie ruszaj. Przejdz do nastepnego pliku.

   **Instrukcja slowna (np. "rozbij"):** splituj plik na 2+ kawalki.

### Krok 3: Log

Po kazdym pliku append do `_brudnopis/YYYY-MM-DD-sortuj.md`:

```
## [HH:MM] mapa-ai-tools-2026.md → Wiedza/AI/Raw/
Akcja: a (Raw)
Decyzja: user
Result: OK. Zaktualizowano Wiedza/AI/index.md.
```

### Krok 4: Podsumowanie

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Koniec /sortuj.

Przeniesiono: 3 pliki
  - 1 do Wiedza/AI/Raw/
  - 1 do Projekty/Vibe-coding/moja-apka/notes/
  - 1 do Kosz/

Nowe projekty: 0
Skip (zostaje w _inbox): 1
Aktualizowane index.md: 3

Log: _brudnopis/2026-04-20-sortuj.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Zasady bezpieczenstwa

- **NIGDY** nie rusza plikow bez explicite decyzji usera.
- Zawsze proponuje `[s] Skip` - watpliwe pliki zostaja w inbox.
- Usuniecie = mv do `Kosz/`, **nie** `rm`.
- Bez edycji tresci plikow (poza dodaniem frontmatter jesli go brakuje).
- Jesli plik jest binarny (obraz, PDF, audio) - propozycje ograniczone do
  `Projekty/<projekt>/resources/` lub `Wiedza/Biblioteka/`.

## Kontekst do wczytania przy starcie

- `_inbox/` (list plikow)
- `Wiedza/index.md`
- `Projekty/index.md`
- `_pamiec/DREAM.md`
- `vault-map.md`
