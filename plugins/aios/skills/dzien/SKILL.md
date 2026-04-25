---
name: dzien
description: >
  Briefing dnia: kalendarz Google + aktywne projekty + sugestia focusu.
  Triggery: /aios:dzien, "co dzis mam", "plan na dzis", "co jest na kalendarzu".
---

# AIOS: Dzien

User chce wiedziec co ma dzis i od czego zaczac. Daj mu jeden ekran - kalendarz + kontekst projektow + propozycja focusu.

## Krok 1: Pobierz dzisiejsze eventy z Google Calendar

Wywolaj `list_events` z parametrami:
- `startTime`: dzis 00:00:00 w ISO 8601 (uzyj aktualnej daty z kontekstu sesji)
- `endTime`: dzis 23:59:59 w ISO 8601
- `timeZone`: strefa czasowa usera z me.md (sekcja Tozsamosc) lub `Europe/Warsaw` jako fallback
- `orderBy`: startTime
- `pageSize`: 30

Jesli Calendar MCP niedostepny: powiedz "Kalendarz niedostepny" i kontynuuj z samymi projektami.

## Krok 2: Przeczytaj aktywne projekty

Przeczytaj `_pamiec/aktualny.md` - sekcja "Nastepny krok" i projekt.

Nastepnie przeczytaj `me.md` - tabela "Aktywne projekty" - zeby wiedziec co jest aktywne i gdzie leza pliki.

## Krok 3: Zinterpretuj dzien

Na podstawie wydarzen ocen typ dnia:

- **Sesja edukacyjna / szkoleniowa** w kalendarzu (rozpoznawana po slowach kluczowych z me.md - sekcja Aktywne projekty / Nauka) -> dzien nauki, przygotuj kontekst jesli sesja za < 2h
- **Duze bloki bez eventow (>= 3h)** -> deep work mozliwy, zaproponuj projekt do pracy
- **Gesty kalendarz (>= 4 eventy)** -> dzien spotkan, zaproponuj tylko sprawy < 30 min
- **Brak eventow** -> wolny dzien lub weekend, user sam zdecyduje

## Krok 4: Przedstaw briefing

Format:

```
[Data, dzien tygodnia]

Kalendarz:
- HH:MM - HH:MM  Nazwa eventu  [lokalizacja lub link jesli jest]
- ...
(jesli brak eventow: "Brak eventow")

Aktywny projekt: [nazwa projektu z aktualny.md]
Nastepny krok: [z aktualny.md]

Focus na dzis: [1 zdanie sugestii na podstawie kalendarza]
```

Bez naglowkow markdown. Bez "Oto Twoj plan dnia!". Jesli jest duzo eventow - pokaz je wszystkie, nie skracaj.

## Krok 5: Opcjonalne akcje

Po briefingu mozesz zaproponowac (max 1, tylko jesli naprawde trafne):

- `/aios:kontynuuj` - jesli nie wiadomo od czego zaczac

Nie proponuj niczego jesli kontekst jest oczywisty.

## Czego NIE rob

- Nie czytaj calego vaulta "zeby lepiej doradzic"
- Nie pytaj "Czy chcesz zebym sprawdzil cos jeszcze?"
- Nie pisz "Mam nadzieje, ze dzien bedzie produktywny" ani podobnych fraz
