# DREAM.md - konsolidacja vaulta

> **Ten plik startuje pusty.** Wypełnia się półautomatycznie przez `/aios:koniec-sesji`
> co 5+ sesji (konsolidacja). To wysoko-poziomowy obraz vaulta - "pamięć długoterminowa"
> ponad pojedynczą sesją (`_pamiec/aktualny.md` trzyma stan ostatniej sesji, DREAM trzyma obraz całości).
>
> Nie edytuj ręcznie bez powodu. Skille (`/aios:koniec-sesji`, `/aios:stworz-projekt`) pokazują
> diff i czekają na "tak" zanim cokolwiek tu zapiszą - to plik fundamentowy.

## Aktywne projekty

| projekt | ścieżka | status |
|---------|---------|--------|
| (puste do pierwszego `/aios:stworz-projekt`) | | |

## Kluczowe decyzje

> Najważniejsze decyzje na poziomie całego systemu/życia, z uzasadnieniem. Append-only.

(puste - wypełni konsolidacja)

## Wzorce pracy

> Powtarzalne wzorce: jak pracujesz, kiedy, czego unikasz, co działa.

(puste - wypełni konsolidacja)

## Luki

> Czego brakuje, otwarte wątki, rzeczy do domknięcia na poziomie systemu.

(puste - wypełni konsolidacja)

## Log konsolidacji

> Append-only. Każda konsolidacja DREAM dopisuje tu wpis (data + co skonsolidowano),
> żeby `/aios:koniec-sesji` wiedział, ile sesji minęło od ostatniego razu.

- (brak konsolidacji jeszcze - pierwsza nastąpi po ~5 sesjach)

---

*Plik z AIOS-Klaudynka vault-template (v0.3.0). Konsoliduje go `/aios:koniec-sesji`.*
