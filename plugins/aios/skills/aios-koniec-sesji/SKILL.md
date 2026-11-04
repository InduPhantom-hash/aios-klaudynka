---
name: aios-koniec-sesji
description: Zamkniecie sesji AIOS - zapisuje transkrypt do _brudnopis/, aktualizuje _pamiec/aktualny.md i opcjonalnie DREAM.md. Uzywaj zawsze gdy konczysz prace z userem i chcesz zachowac kontekst. Triggery - "/aios:koniec-sesji", "/aios-koniec-sesji", "koniec sesji", "zapisz stan", "konczymy prace", "zamknij sesje", "zapisz sesje".
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
typ_wiedzy: fakt
tematy: [tag1, tag2]
podmioty: []
ai_summary: "Rzeczywisty zakres i wynik sesji."
data: YYYY-MM-DD
tryb: eksploracja | skupienie
projekt: <nazwa> | ad-hoc
status: draft
---
```

Treść: pełna rozmowa verbatim od początku sesji. Oznacz wypowiedzi `**User:**` / `**AI:**`. Nie kompresuj - historia myślenia jest wartościowa.

## Krok 3: Zaktualizuj aktualny.md (limit 3 KB)

Pokaż diff `_pamiec/aktualny.md` i po zatwierdzeniu zastąp bieżący stan, zachowując metadane oraz flagi prywatności.
Upewnij się, że rozmiar pliku nie przekracza **3 KB** (ochrona okna kontekstowego modelu). Nowy plik opatrz bitemporalnym YAML:

```markdown
---
typ_wiedzy: fakt
status: aktywny
data_wpisu: YYYY-MM-DD
tematy: [stan-sesji]
podmioty: []
ai_summary: "Ostatni zatwierdzony stan pracy i następny krok."
---

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

## Krok 3b: Ekstrakcja lekcji proceduralnych (Lesson Mining)

Jeśli w trakcie sesji wykryto błąd, pułapkę techniczną lub nowe sprawdzone rozwiązanie, wyekstrahuj atomową lekcję do `_pamiec/lekcje.md`:
```markdown
### [YYYY-MM-DD] <Tytuł lekcji>
- **Status:** aktywny
- **Kontekst / Trigger**: <kiedy występuje>
- **Pułapka / Błąd**: <co poszło nie tak>
- **Reguła / Rozwiązanie**: <zasada afirmatywna: co należy zrobić>
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

## Zgodność z lokalnym RAG

Przed zapisem wczytaj `_skille/rag.md`. Nowe notatki `.md` zaczynaj od YAML `typ_wiedzy`, `tematy`, `podmioty`, `ai_summary`; zachowaj pola źródłowe i flagi prywatności. Dane prywatne i cytaty z prywatnych logów nie tracą ochrony podczas przetwarzania.

Po zakończonej partii zatwierdzonych zapisów/przeniesień/usunięć uruchom lokalny `index` zgodnie z `_skille/rag.md`. Dotyczy to również nowych raportów, pamięci, `index.md` i plików zadań. `--vault` podaj przed `index`. Przy błędzie zachowaj źródła, zgłoś indeks jako nieaktualny/niedostępny i pracuj na plikach. Nie uruchamiaj indeksowania w samym podglądzie lub po anulowaniu; nie wysyłaj danych do Pinecone automatycznie.

Mechaniczne operacje wykonuj przez narzędzie plikowe lub Python `pathlib`/`shutil`, bez wymogu bash, `mv` lub `rg`. Używaj interpretera vaulta: `.venv/bin/python` na macOS/Linux albo `.venv/Scripts/python.exe` na Windows. Nie nadpisuj celu przeniesienia; zatwierdzenie edycji nie zastępuje osobnej zgody na przeniesienie/usunięcie lub zapis zewnętrzny.
