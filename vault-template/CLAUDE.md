# CLAUDE.md - AIOS-Klaudynka vault

Ten plik czyta AI za każdym razem, gdy wchodzi w ten vault. Nie zmieniaj go bez powodu.

## Co to jest

To jest **AIOS-Klaudynka** - Personal Agentic OS oparty na plikach `.md` (File Over AI). Wszystko co istotne, istnieje jako plik - nie jako baza danych, nie jako magia, nie jako ukryty stan.

## Pliki fundamentowe

Zanim cokolwiek zrobisz, przeczytaj w tej kolejności:

1. **`me.md`** - profil użytkownika. Tu są hard rules, rola, preferencje, styl komunikacji. **To jest Twoja konfiguracja dla tej rozmowy.** Stosuj się do tych reguł, dopóki user explicite ich nie cofnie.
2. **`_pamiec/aktualny.md`** (jeśli istnieje) - stan ostatniej sesji. Co robiliście, co zostało otwarte, co jest następnym krokiem.
3. **`vault-map.md`** (jeśli istnieje) - mapa vaulta, generowana przy `/aios:init`. Mówi gdzie co leży.

Jeśli `me.md` nie istnieje - uruchom `/aios:init` (onboarding).

## Skille dostępne w tym vaulcie

Plugin `aios` (6 skilli):

- `/aios:init` - onboarding (jednorazowy, wypełnia `me.md`).
- `/aios:sortuj` - przegląd `_inbox/` i rozmieszczenie plików.
- `/aios:stworz-projekt <nazwa> <kategoria>` - promuje wątek z `_brudnopis/` do pełnej struktury projektu.
- `/aios:dodaj-do-wiki <ścieżka>` - przetwarza materiał z `Wiedza/<X>/Raw/` na stronę w `Wiedza/<X>/Wiki/` (metoda Karpathy).
- `/aios:szukaj <query>` - wyszukiwanie hierarchiczne (index.md → Pinecone fallback).
- `/aios:koniec-sesji` - zamknięcie sesji, zapis do `_brudnopis/`, aktualizacja `_pamiec/aktualny.md`.

## Struktura vaulta

```
AIOS-Klaudynka/
├── me.md                  ← profil usera (generowany przez /aios:init)
├── vault-map.md           ← mapa (generowana przez /aios:init)
├── CLAUDE.md              ← ten plik
├── _inbox/                ← surowe notatki, wrzutki do posortowania
├── _brudnopis/            ← transkrypty sesji, dzienne myślenie na głos
├── _pamiec/               ← pamięć długoterminowa (aktualny.md, DREAM.md)
├── _Archiwum/             ← dead-endy, archiwa
├── Kosz/                  ← bufor przed usunięciem
├── Projekty/              ← aktywne projekty (podkategorie: Praca/Hobby/Prywatne/Vibe-coding/...)
├── Wiedza/                ← zasoby wiedzy (podobszary: AI/Marketing/Programming/...)
│   └── <obszar>/
│       ├── Raw/           ← surowce (artykuły, transkrypty, PDF)
│       └── Wiki/          ← skompilowana wiedza (metoda Karpathy)
└── Kalendarz/             ← daily / weekly / deadliny
```

## Zasady

1. **Nie edytuj `me.md` samodzielnie.** Pokaż diff userowi i czekaj na "tak". `me.md` to fundament.
2. **Nie kasuj plików bez zgody.** Jeśli coś ma zniknąć - najpierw do `Kosz/`, potem (za zgodą) usunięcie.
3. **Zawsze aktualizuj `index.md`.** Jeśli tworzysz nowy plik w `Projekty/<X>/` albo `Wiedza/<X>/Wiki/` - dopisz link do `index.md` w tym folderze. Inaczej `/aios:szukaj` go nie zobaczy.
4. **Zapisuj stan sesji.** Gdy user kończy pracę - uruchom `/aios:koniec-sesji`. Bez tego kontekst się gubi.
5. **Ignoruj prywatne ścieżki w publicznych operacjach.** `_Archiwum/`, `Kosz/`, `_inbox/` nie trafiają do Pinecone ani publicznego indeksu.

## Dokumentacja

- Pełny opis: [INSTALL.md](https://github.com/InduPhantom-hash/aios-klaudynka/blob/main/INSTALL.md)
- README: [README.md](https://github.com/InduPhantom-hash/aios-klaudynka)
