# _pamiec

Pamięć długoterminowa vaulta. Tu mieszka stan, który przetrwa sesję.

## Pliki

- **`aktualny.md`** - stan ostatniej sesji. Co robiliście, co zostało otwarte, następny krok. Nadpisywany przez `/aios:koniec-sesji`.
- **`DREAM.md`** (opcjonalnie) - konsolidacja co N sesji. Aktywne projekty, kluczowe decyzje, wzorce pracy, luki. Wysoko-poziomowy obraz vaulta.
- **`onboarding-progress.md`** (tymczasowo) - postęp niedokończonego `/aios:init`. Usuwany po finalizacji.

## Zasady

- `aktualny.md` to pojedynczy plik, nadpisywany, nie append. Zawsze ten sam format.
- `DREAM.md` ma sekcję "Log konsolidacji" - append-only, żebyś wiedział co i kiedy konsolidowałeś.
- Nic tu nie kasuj ręcznie. Jeśli chcesz fresh start - najpierw do `Kosz/`, potem usuń.

---

*Sesję zamyka `/aios:koniec-sesji`. DREAM konsoliduje się półautomatycznie przy `/aios:koniec-sesji` co 5+ sesji.*
