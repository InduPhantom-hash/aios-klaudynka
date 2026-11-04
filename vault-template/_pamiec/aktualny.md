---
typ_wiedzy: fakt
status: aktywny
data_wpisu: YYYY-MM-DD
ai_summary: Stan ostatniej sesji roboczej, otwarty kontekst i rekomendacja kolejnego mikrokroku.
---

# Stan Ostatniej Sesji (Carry-over)

> [!NOTE]
> Plik stanu sesji. Twardy limit rozmiaru: **3 KB** dla zerowego narzutu tokenów przy starcie sesji.
> Nadpisywany automatycznie przy procedurze `/aios-koniec-sesji`.

## Ostatnia Sesja
- **Data i godzina:** YYYY-MM-DD HH:MM
- **Projekt / Obszar:** [Nazwa projektu lub obszar pracy]
- **Cel sesji:** [Krótki opis celu sesji]
- **Wykonane kroki:**
  - [x] Krok 1
  - [x] Krok 2

## Otwarty Kontekst i Niezamknięte Wątki
- [ ] Zadanie w toku lub oczekujące na weryfikację
- Kluczowe ustalenia / decyzje podjęte w sesji: [[decyzje]]

## Rekomendacja Kolejnego Kroku (Mikrokrok na 2 minuty)
- [ ] Dokładnie jeden natychmiastowy mikrokrok do wykonania na początku kolejnej sesji.
