---
name: aios-kustosz
description: "Zintegrowany strażnik spójności Vaulta AIOS: audyt struktury i luk, lint bazy wiedzy CLI, weryfikacja dat oraz wizualizacja. Triggery: /kustosz, /aios-kustosz, /aios:kustosz, \'kustosz\', \'audyt vaulta\', \'sprawdź vault\', \'stan vaulta\'."
---
# AIOS: Kustosz (Integralność i Higiena Vaulta)

## Cel i kontekst
Centralny strażnik spójności, struktury i bazy wiedzy AIOS. Konsoliduje dotychczasowe narzędzia `aios-core-update`, `aios-meta-audyt-luk`, `aios-lint-md` oraz `aios-meta-wizualizuj-vault`.

Zasady:
- **File Over AI:** badaj rzeczywisty stan plików i katalogów na dysku, nie pamięć podręczną modelu.
- **File Output by Default:** wyniki głębokiego skanowania trafiają do pliku JSON w `_brudnopis/`, a do czatu trafia wyłącznie zwarta tabela.
- **Bezpieczeństwo:** Kustosz to audytor. Nie modyfikuje ani nie usuwa plików bez pokazania diffu i otrzymania wyraźnego `tak`.

## Tryby pracy

### 1. Tryb Domyślny: Szybki Audyt Struktury i Luk (`/kustosz`)
Skanuje fizyczne katalogi vaulta i porównuje je z dokumentami nawigacyjnymi:
1. Sprawdź zgodność z `vault-map.md` oraz listą aktywnych projektów w `_pamiec/DREAM.md`.
2. Zidentyfikuj luki strukturalne:
   - Brakujące pliki `README.md` w projektach i obszarach wiedzy.
   - Puste katalogi `Raw/` lub martwe `index.md`.
   - Brak sekcji "Następny krok" w aktywnych projektach.
   - Osierocone pliki w katalogu głównym vaulta (poza dozwolonymi `_*` i głównymi folderami).
3. Przedstaw zwięzłą tabelę: Element, Rozjazd/Luka, Rekomendowana naprawa.

### 2. Tryb Głęboki: Lint Bazy Wiedzy (`/kustosz --deep` lub `/kustosz --lint`)
Uruchamia zoptymalizowany skrypt CLI do weryfikacji integralności tekstu i metadanych:
```bash
python3 _skille/aios/skills/aios-kustosz/scripts/lint_md.py \
  --target Wiedza \
  --output _brudnopis/kustosz-lint.json
```
Skrypt sprawdza:
- **Ślepe linki** (odwołania do nieistniejących plików .md lub wikilinków).
- **Sieroty** (notatki, do których nie prowadzi żaden link).
- **Puste notatki** (< 50 znaków).
- **Kompletność YAML frontmatter** (wymagane klucze: `typ_wiedzy`, `status`, `data_wpisu`, `tematy`, `podmioty`, `ai_summary`).
- **Format dat ISO-8601** (weryfikacja pól `data`, `date`, `created`, `updated` pod kątem wzorca `YYYY-MM-DD`).

### 3. Tryb Mapy: Wizualizacja Struktury (`/kustosz --mapa`)
Generuje w czacie aktualny diagram Mermaid obrazujący architekturę i statusy aktywnych obszarów vaulta (do głębokości 2-3 poziomów).

## Procedura naprawcza (Checkpoint)
Gdy raport wykaże rozjazdy lub błędy:
1. Przedstaw plan naprawczy w punktach.
2. Przy zmianach w plikach systemowych (`vault-map.md`, `DREAM.md`, `me.md`) zawsze pokaż pełny diff.
3. Czekaj na `tak` przed wprowadzeniem jakiejkolwiek modyfikacji.
