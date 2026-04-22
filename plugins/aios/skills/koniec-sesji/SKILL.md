---
name: koniec-sesji
description: Zamkniecie sesji AIOS - zapisuje transkrypt do _brudnopis/, aktualizuje _pamiec/aktualny.md i opcjonalnie DREAM.md. Uzywaj zawsze gdy konczysz prace z userem i chcesz zachowac kontekst. Triggery - "/aios:koniec-sesji", "koniec sesji", "zapisz stan", "konczymy prace", "zamknij sesje", "zapisz sesje".
---

# koniec-sesji

Zamykasz sesję z userem. Vault to system - twoje zadanie to zostawić go w stanie gotowym do następnej sesji z dowolnym AI.

## Krok 1: Zapytaj o metadane

Zanim cokolwiek zapiszesz, zapytaj usera o **jedną rzecz**:

> "Tryb tej sesji: eksploracja czy skupienie? Projekt: [zgadnij z kontekstu] - ok?"

Jeśli user potwierdza lub koryguje - masz wszystko do frontmatter.

## Krok 2: Zapisz transkrypt

Nazwa pliku: `_brudnopis/YYYY-MM-DD-<slug>.md`
- slug = 2-4 słowa kebab-case opisujące temat, np. `2026-04-19-aios-skille-setup`
- Użyj dzisiejszej daty z kontekstu sesji

Frontmatter:
```yaml
---
data: YYYY-MM-DD
tryb: eksploracja | skupienie
projekt: <nazwa> | ad-hoc
status: draft
tematy: [tag1, tag2]
---
```

Treść: pełna rozmowa verbatim od początku sesji. Oznacz wypowiedzi `**User:**` / `**AI:**`. Nie kompresuj - historia myślenia jest wartościowa.

## Krok 3: Zaktualizuj aktualny.md

Nadpisz `_pamiec/aktualny.md` (nie appenduj):

```markdown
# Aktualny stan pracy

Data ostatniej sesji: YYYY-MM-DD
Projekt: <nazwa>
Tryb: eksploracja | skupienie

## O czym rozmawialiśmy
<3-5 konkretnych punktów>

## Co zdecydowane i zrobione
<tylko rzeczy wyraźnie zatwierdzone przez usera>

## Co niezdecydowane / do dalszej rozmowy
<otwarte pytania, wątki zawieszone>

## Następny krok
<jedna konkretna rzecz do zrobienia w kolejnej sesji>

## Pliki dotknięte w tej sesji
<ścieżki plików które powstały lub zostały zmienione>
```

## Krok 4: Decyzja o brudnopisie

Zapytaj: "Ta sesja - projekt, archiwum, czy dead-end?"

- **Projekt** → zaproponuj `/stworz-projekt <nazwa> <kategoria>`
- **Archiwum** → zostaje w `_brudnopis/` ze `status: archiwum`
- **Dead-end** → przenieś do `_Archiwum/dead-ends/YYYY-MM-DD-<slug>/` + stwórz `reason.md`

## Krok 5: DREAM.md (opcjonalnie)

Zapytaj: "Zaktualizować DREAM.md?"
Rekomenduj gdy minęło ≥5 sesji od ostatniej konsolidacji (sprawdź Log w DREAM.md).

Jeśli tak:
1. Przeczytaj `_pamiec/DREAM.md`
2. Przeczytaj ostatnie 5-10 plików z `_brudnopis/` (po dacie, descending)
3. Zaktualizuj: Aktywne projekty / Kluczowe decyzje / Wzorce pracy / Luki
4. **Pokaż diff userowi i czekaj na "tak"** - DREAM to fundament systemu
5. Dopisz wpis do "Log konsolidacji" w DREAM.md

## Krok 6: Raport końcowy

Jednolinijkowy, np.:
```
Sesja zapisana: _brudnopis/2026-04-19-aios-skille-setup.md | aktualny.md zaktualizowany | DREAM: pominięty | Następnym razem: uruchomić create-cowork-plugin
```

## Kiedy pominąć ten skill

- Sesja krótsza niż 5 minut i nic znaczącego
- User explicite: "nie zapisuj tego"
- Sesja była tylko wyszukiwaniem, bez nowej wiedzy ani decyzji
