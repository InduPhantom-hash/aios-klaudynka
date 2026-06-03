# Wiedza/Raw

Surowce - artykuły, transkrypty, PDF-y - zanim AI je przetworzy metodą Karpathy do `Wiki/`.

## Konwencja nazw

```
Wiedza/<obszar>/Raw/src-NN-krotki-slug.md
                   src-NN-nazwa.pdf
```

`src-NN` to licznik źródeł w obszarze (np. `src-01`, `src-02`...). Ułatwia referencje z `Wiki/<strona>.md` w polu `zrodla: [src-03, src-07]`.

## Workflow

1. Wrzuć surowiec (kopiuj, nie generuj - to ma być oryginał).
2. Uruchom `/aios:dodaj-do-wiki Wiedza/<obszar>/Raw/<nazwa>.md`.
3. Skill przeczyta, zaproponuje aktualizację istniejących stron w `Wiki/` albo nowe strony. Czeka na Twoje "tak".
4. Log przetwarzania trafia do `Wiedza/<obszar>/Wiki/log.md`.

---

*Metoda Karpathy: Collect (Raw) → Compile (Wiki) → Query (`/aios:szukaj`).*
