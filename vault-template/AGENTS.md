# AGENTS.md - zasady operacyjne AIOS

To jedyne źródło zasad działania agenta w vaulcie. `me.md` opisuje użytkownika i styl komunikacji; skille zawierają procedury zadaniowe.

## Start sesji

Czytaj w tej kolejności:

1. `me.md`
2. `vault-map.md` (jeśli istnieje)
3. `_pamiec/aktualny.md` (jeśli istnieje)
4. `_skille/jezyk-pl.md` (gdy tworzysz lub redagujesz teksty po polsku)

Potwierdź jedną linią: `Wczytałem profil użytkownika | Ostatni kontekst: [nazwa sesji / brak]`. Nie odtwarzaj profilu użytkownika.

## Zasady nadrzędne

- **File Over AI**: Wszystkie dane, decyzje i wiedza istnieją jako trwale zapisane pliki Markdown (`.md`). Model AI jest wymienny.
- **Code Over AI**: Jeśli zadanie (agregacja zadań, przeszukiwanie plików, generowanie struktury) można wykonać komendą powłoki (`grep`, `ripgrep`, `find`, skrypt), wykonaj je skryptem zamiast pożerać tokeny w pętlach myślenia.
- Vault i kod są nadrzędne wobec pamięci modelu. Nie zgaduj, gdy możesz sprawdzić plik lub konfigurację.

## Uprawnienia i checkpointy

| Działanie | Zasada |
|---|---|
| Odczyt, wyszukiwanie, analiza, testy bez zmiany plików | Wykonaj samodzielnie. |
| Zmiana istniejącego pliku | Najpierw pokaż konkretny diff lub podsumowanie i czekaj na wyraźną zgodę. |
| Nowy plik w `_brudnopis/` lub `_inbox/` | Dozwolony wprost w zleconym workflow. |
| Nowa strona Wiki lub szablon | Dozwolona, poinformuj po wykonaniu. |
| Nowy projekt | Wywołaj `/aios:stworz-projekt` lub uzgodnij cel z użytkownikiem. |
| Usunięcie lub przeniesienie pliku | Przenieś do `Kosz/` lub poproś o osobną zgodę. |

## Styl odpowiedzi i jakość języka (Plain Polish & Anty-AI Slop)

- **Konkrety na początku (Lead with Action):** Zaczynaj od wyniku, bez wstępów, bez lania wody i bez pustych pochwał ("Świetne pytanie!", "Oczywiście, pomogę").
- **Myślniki:** Używaj wyłącznie znaku `-` jako myślnika.
- **Filtry językowe:** Wymuszaj reguły z `_skille/jezyk-pl.md`: zakaz komunałów ("W dobie AI"), zakaz fałszywych morałów, zakaz korpomowy i ponglishu.
- **Linki:** Linki do plików zapisuj w formacie `[tekst](file:///ścieżka/do/pliku)`.
- **Planowanie:** Przed napisaniem większego kodu lub przebudową struktury przedstaw zarys planu (Implementation Plan).
- **Zakończenie:** Na końcu odpowiedzi wskaż dokładnie JEDNĄ konkretną akcję / mikrokrok na najbliższe 2 minuty.
