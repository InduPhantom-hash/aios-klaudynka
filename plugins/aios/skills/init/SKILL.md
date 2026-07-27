---
name: init
description: Onboarding do AIOS-Klaudynki - prowadzi usera przez ankietę (tryb --quick w 10 min lub pełny w 45 min), generuje me.md, buduje strukturę vaulta i AIOS Task Tracker. Triggery - "/aios:init", "/aios:init --quick", "uruchom onboarding", "wygeneruj me.md", "skonfiguruj AIOS".
---

# init

Skill onboardingowy AIOS-Klaudynki. Wywoływany po instalacji. Generuje profil `me.md`, dostosowuje strukturę `Projekty/`, tworzy `vault-map.md` oraz konfiguruje system zadań (lokalny Task Tracker lub ClickUp/Notion).

## Krok 0 - Wybór trybu

Zapytaj użytkownika na starcie (lub sprawdź flagę `--quick`):

1. **Tryb Szybki (`/aios:init --quick`) ~10-15 min:** 12 kluczowych pytań (A: Tożsamość, B: Zakres, D: Projekty, E: Stos i Tracker zadań, F: Wytyczne komunikacji). Pomija zaawansowane sekcje psychologiczne i rozbudowane integracje.
2. **Tryb Pełny (`/aios:init --full`) ~45 min:** 61 pytań w 10 sekcjach (A-J), obejmujący profil FRIS/Clifton (PDF), zaawansowane Bliźniaki i strefy prywatności.

## Zasady wykonania (Code Over AI & File Over AI)

- Zapisuj postęp po każdej sekcji w `_pamiec/onboarding-progress.md`.
- Pokazuj pytania w zwięzłych blokach. Używaj wyłącznie znaku `-`.
- Generuj `me.md` z sekcjami: `## Profil`, `## Komunikacja`, `## Hard rules`, `## Aktywne projekty` oraz `## Bliźniaki`.
- W sekcji E zadaj pytanie o system zadań: **Lokalny AIOS Task Tracker (`zadania.md`) [Rekomendowany, 100% offline, zerowy koszt]** vs zewnętrzny bliźniak (ClickUp / Linear / Notion).

## Finalizacja (FIN)

1. Wygeneruj `me.md` w korzeniu vaulta.
2. Utwórz foldery podkategorii w `Projekty/` na podstawie odpowiedzi z Sekcji D.
3. W każdym folderze kategorialnym utwórz szablon `index.md` oraz `zadania.md`.
4. Wygeneruj `vault-map.md`.
5. Usuń `_pamiec/onboarding-progress.md` i przedstaw podsumowanie gotowości.
