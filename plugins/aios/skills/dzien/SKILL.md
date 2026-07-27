---
name: dzien
description: >
  Briefing dnia: kalendarze Google + aktywne zadania z projektów (ripgrep) + sugestia focusu.
  Zasada Code Over AI - szybkie skanowanie lokalnych plików bez pożerania tokenów.
  Triggery: /aios:dzien, "co dziś mam", "plan na dziś", "co jest na kalendarzu".
---

# AIOS: Dzień

Użytkownik chce wiedzieć co ma dziś i od czego zacząć. Daj mu jeden zwięzły ekran - kalendarz + kontekst projektów + propozycja focusu.

## Krok 1: Pobierz dzisiejsze eventy ze wszystkich kalendarzy

1. Wywołaj `list_calendars` i pobierz listę dostępnych identyfikatorów kalendarzy (`calendarId`).
2. Dla każdego `calendarId` wywołaj równolegle `list_events` z parametrami:
   - `startTime`: dziś 00:00:00 z offsetem strefy czasowej (np. `2026-07-27T00:00:00+02:00`)
   - `endTime`: dziś 23:59:59 z offsetem strefy
   - `timeZone`: strefa z `me.md` lub `Europe/Warsaw`
   - `orderBy`: startTime
3. Scal i posortuj chronologicznie wydarzenia. Zdeduplikuj powtórzenia.

Jeśli Calendar MCP jest niedostępny: napisz "Kalendarz niedostępny" i przejdź do skanowania zadań.

## Krok 2: Skanuj lokalne zadania (Code Over AI)

Wykonaj szybkie wyszukiwanie komendą powłoki zamiast wczytywać całe katalogi do kontekstu:

```bash
grep -rn "DO ZROBIENIA" Projekty/*/*/zadania.md || true
```

Skompresuj odnalezione priorytetowe zadania z aktywnych projektów.

## Krok 3: Przedstaw briefing

Format:

```text
[Data, dzień tygodnia]

Kalendarz:
- HH:MM - HH:MM  Nazwa eventu [lokalizacja lub link]
(jeśli brak: "Brak eventów")

Zadania w projektach (AIOS Task Tracker):
- [Projekt A] Nazwa priorytetowego zadania
- [Projekt B] Nazwa priorytetowego zadania

Focus na dziś: [1 zdanie sugestii na podstawie kalendarza i zadań]
```

Bez ozdobników, bez "Witaj!", bez powitań. Używaj wyłącznie znaku `-` jako myślnika.
