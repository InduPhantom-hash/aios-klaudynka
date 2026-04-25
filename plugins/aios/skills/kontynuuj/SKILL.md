---
name: kontynuuj
description: >
  Wczytuje kontekst poprzedniej sesji i otwiera biezaca z gotowym briefingiem.
  Czyta aktualny.md + transkrypt ostatniej sesji przez session_info MCP (jesli dostepny).
  Triggery: /aios:kontynuuj, "kontynuuj sesje", "co bylo ostatnio", "przypomnij co robilem".
  NIE uruchamia sie automatycznie - tylko na explicite trigger.
---

# AIOS: Kontynuuj sesje

User triggeruje ten skill recznie gdy chce wrocic do przerwanej pracy. Twoje zadanie: dac mu jeden ekran kontekstu i zapytac czy idziemy dalej.

## Krok 1: Przeczytaj aktualny.md

Przeczytaj `_pamiec/aktualny.md`. To glowne zrodlo - skrot tego co bylo, co zdecydowane, co otwarte i jaki jest nastepny krok.

Jesli plik nie istnieje lub jest pusty: pomin, przejdz do Kroku 2 i powiedz o tym na koncu.

## Krok 2: Transkrypt ostatniej sesji (jesli dostepny session_info)

Wywolaj `list_sessions` (limit: 5). Szukasz sesji gdzie `is_child: false` - to sesje usera, nie sub-agenty.

Wybierz najswiezsza sesje inna niz biezaca. Wywolaj `read_transcript` z parametrami:
- `limit: 40` (ostatnie 40 wiadomosci wystarczy do kontekstu)
- `max_wait_seconds: 0` (nie czekaj - chcesz zapisany transkrypt, nie live session)

Jesli `session_info` MCP jest niedostepny (np. inny runtime niz Cowork) lub nie ma poprzednich sesji: pomin ten krok, opieraj sie tylko na `aktualny.md`. Powiedz o tym userowi.

## Krok 3: Zbuduj briefing

Na podstawie obu zrodel (aktualny.md = priorytet, transkrypt = uzupelnienie) wyciagnij:

- **Temat** - co bylo centrum ostatniej sesji (projekt, problem, decyzja)
- **Zrobione** - co zostalo zamkniete lub zatwierdzone
- **Otwarte** - nierozstrzygniete pytania, zawieszone watki, TODO
- **Nastepny krok** - konkretna jedna rzecz do zrobienia teraz

## Krok 4: Przedstaw briefing

Format - krotki, bez naglowkow w stylu raportu:

```
Ostatnio: [1-2 zdania co bylo tematem i co zamknieto]

Otwarte: [lista max 3 punktow, kazdy w jednej linii]

Nastepny krok: [jedna konkretna rzecz]

Idziemy? (albo powiedz od czego chcesz zaczac)
```

Bez wstepow, bez "Witaj!", bez podsumowania ze wlasnie wczytalem pliki.

## Obsluga edge case'ow

**Brak aktualny.md i brak transkryptu:**
> "Nie mam sladu poprzedniej sesji - ani aktualny.md, ani transkrypt przez session_info. Zaczynamy od zera czy cos pamietasz z ostatniej pracy?"

**Aktualny.md jest stary (>7 dni od `data ostatniej sesji`):**
Powiedz o tym: "aktualny.md pochodzi z [data] - moze byc nieaktualny."

**Transkrypt jest z innego projektu niz aktualny.md:**
Powiedz wprost: "Transkrypt dotyczy [X], aktualny.md mowi o [Y]. Ktory kontekst chcesz?"

## Czego NIE rob

- Nie odczytuj calego vaulta zeby "byc pewnym kontekstu"
- Nie pytaj "Czy chcesz zebym wczytal wiecej plikow?" - albo je wczytaj, albo nie
- Nie dawaj briefingu dluzszego niz jeden ekran
- Nie uruchamiaj sie automatycznie na starcie sesji bez triggera
