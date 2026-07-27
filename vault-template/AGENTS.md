# AGENTS.md - zasady operacyjne AIOS

To jedyne źródło zasad działania agenta w vaulcie. `me.md` opisuje użytkownika i styl komunikacji; skille zawierają procedury zadaniowe.

## Start sesji

Czytaj w tej kolejności:

1. `me.md`
2. `vault-map.md` (jeśli istnieje)
3. `_pamiec/aktualny.md` (jeśli istnieje)

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

## Styl odpowiedzi i komunikacji

- Zaczynaj od wyniku. Pisz prostym językiem, bez korpomowy i bez zbędnych wstępów.
- Używaj wyłącznie znaku `-` jako myślnika.
- Linki do plików zapisuj w formacie `[tekst](file:///ścieżka/do/pliku)`.
- Przed napisaniem większego kodu lub przebudową struktury przedstaw zarys planu (Implementation Plan).
