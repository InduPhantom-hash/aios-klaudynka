---
name: zadania
description: >
  Wyciaga zadania do zrobienia z aktualnej rozmowy i tworzy je w zewnetrznym task trackerze (ClickUp / Linear / Asana / Notion - zaleznie od konfiguracji w me.md).
  Pokazuje liste do akceptacji inline - user edytuje lub zatwierdza, zadania laduja w trackerze z terminami.
  Triggery: /aios:zadania, "wrzuc do trackera", "zanim odejde", "zadania z sesji", "co mam do zrobienia".
  NIE jest czescia koniec-sesji - odpala sie samodzielnie w srodku lub na koncu sesji gdy jest cos do wykonania poza komputerem.
---

# AIOS: Zadania

User odchodzi od kompa lub chce zrzucic zadania z glowy do trackera. Twoje zadanie: wyciagnac z rozmowy konkretne akcje, pokazac liste i stworzyc zatwierdzone zadania w skonfigurowanym trackerze.

## Krok 0: Wczytaj konfiguracje z me.md

Przeczytaj sekcje `## Bliznniaki` -> `### Task tracker` w `me.md`. Spodziewasz sie:

```
- typ: clickup | linear | asana | notion | brak
- workspace: <URL lub ID>
- assignee_id: <ID usera w trackerze, jesli wymagane>
- mapowanie kategoria -> lista:
  | kategoria | slowa kluczowe                | list_id / project_id |
  |-----------|-------------------------------|----------------------|
  | Praca     | klient, marketing, deadline   | <ID>                 |
  | Prywatne  | rodzina, dom, zakupy          | <ID>                 |
  | Nauka     | kurs, szkolenie, sesja        | <ID>                 |
  | Inne      | (brak slow - kategoria default)| <ID>                |
```

**Jesli `typ: brak` lub sekcja nie istnieje:** powiedz userowi:

> "Nie masz skonfigurowanego task trackera w me.md (sekcja Bliznniaki -> Task tracker). Dwie opcje:
> 1. Skonfiguruj teraz: powiedz jakiego uzywasz (ClickUp, Linear, Asana, Notion) i podaj URL workspace + 1-2 listy do mapowania.
> 2. Pomijamy tracker i zapisuje zadania tylko do `_pamiec/zadania-log.md` w vaulcie.
> Co wybierasz?"

Jesli user wybiera (1) - dopisz konfig do me.md, kontynuuj. Jesli (2) - pomin Krok 3 z trackerem, zapisz tylko log.

**Jesli `typ` jest skonfigurowany ale brak mapowania kategorii:** stworz domyslne mapowanie z 1 listy "Inbox" (poprosi usera o `list_id`) i zaproponuj rozbudowanie pozniej.

## Krok 1: Wyciagnij zadania z rozmowy

Przeskanuj cala aktualna rozmowe. Szukaj:
- rzeczy ktore user zadeklarowal ze zrobi ("zrobie", "sprawdze", "skonfiguruje", "przetestuje")
- nastepnych krokow wymienionych w dyskusji
- rzeczy wymagajacych dzialania poza Claude'em (instalacja, konfiguracja po jego stronie, testy manualne)
- decyzji ktore wymagaja follow-up

**Nie wciagaj:**
- rzeczy juz zrobionych w tej sesji
- rzeczy ktore robi AI, nie user
- luznych pomyslow bez konkretnej akcji
- watkow zawieszonych bez decyzji

Dla kazdego zadania wyciagnij jesli padlo w rozmowie: szacowany termin lub kontekst czasowy.

## Krok 2: Pokaz liste inline

Pokaz liste w tym formacie - bez wstepu, bez komentarza:

```
Zadania z tej sesji:

1. [ ] <tresc zadania> - <termin jesli znany, inaczej "bez terminu">
2. [ ] <tresc zadania> - <termin>
...

Edytuj jesli cos nie gra (tresc, termin, kolejnosc). Usun linie ktorych nie chcesz. Terminy w formacie: YYYY-MM-DD lub YYYY-MM-DD HH:MM. Napisz "ok" gdy lista jest dobra.
```

Czekaj. Nie komentuj, nie pytaj - daj userowi przestrzen do edycji.

## Krok 3: Utworz zadania w trackerze

Po "ok" (lub innym sygnale akceptacji) - dla kazdej pozycji ktora zostala na liscie:

### Routing do wlasciwej listy

Wykryj kategorie zadania z kontekstu i dopasuj wedlug **mapowania z me.md** (Krok 0). Algorytm:

1. Dla kazdej kategorii z mapowania, sprawdz czy slowa kluczowe wystepuja w tresci zadania (case-insensitive).
2. Jesli zadanie pasuje do kilku - bierz pierwsza pasujaca wedlug kolejnosci w me.md (user sam je ulozyl).
3. Jesli nic nie pasuje - kategoria default ("Inne", oznaczona w me.md pustymi slowami kluczowymi). Jesli "Inne" tez nie ma w me.md - zatrzymaj sie i zapytaj usera do ktorej listy ma trafic.

### Tworzenie

Wybierz wywolanie wedlug `typ`:

- **clickup**: `clickup_create_task(list_id, name, assignees=[<assignee_id>], due_date, priority)`. Bez `assignee_id` z me.md - taski beda nieprzypisane, ostrzez usera.
- **linear**: `save_issue(team_id, title, description, due_date)`. `team_id` to wartosc `list_id / project_id` z me.md w Linear semantyce.
- **asana**: `asana_create_task(project_id, name, due_on, assignee)`.
- **notion**: `notion-create-pages(parent={database_id}, properties={Name, Date, ...})`.

Parametry uniwersalne:
- `name` / `title`: tresc zadania
- `due_date` / `due_on`: termin jesli podany (format YYYY-MM-DD lub YYYY-MM-DD HH:MM)
- `priority`: `normal` domyslnie, `urgent` jesli w tresci jest "pilne" / "dzis" / "asap"

Tworz zadania jedno po drugim. Nie pytaj o potwierdzenie kazdego z osobna - user juz zatwierdzil liste.

### Zmiana struktury

Jesli user poprosi o dodanie/zmiane kategorii - **zaktualizuj me.md** (sekcja Bliznniaki -> Task tracker -> tabela mapowania). Nie modyfikuj tej sekcji w SKILL.md - to konfiguracja per user, nie kod.

## Krok 4: Zaloguj do vaulta

Dopisz (nie nadpisuj) do `_pamiec/zadania-log.md`:

```markdown
## YYYY-MM-DD

- [ ] <zadanie 1> - <termin> - [<tracker>](url)
- [ ] <zadanie 2> - <termin> - [<tracker>](url)
```

Jesli plik nie istnieje - utworz z naglowkiem:
```markdown
# Zadania - log

Plik generowany przez /aios:zadania. Nie edytuj recznie.
```

## Krok 5: Raport koncowy

Jedna linia:
```
Dodano N zadan do <tracker>. Log: _pamiec/zadania-log.md
```

Nie podsumowuj zadan ponownie - user je widzi.

## Kiedy pominac skill

- Rozmowa nie zawiera zadnych konkretnych akcji dla usera - powiedz wprost "Brak zadan do wyciagniecia z tej rozmowy."
- User mowi "tylko sprawdz" albo pyta o cos bez kontekstu follow-up

## Czego NIE rob

- Nie hardkoduj `list_id` ani `assignee_id` w tresci tego pliku - wszystko czyta sie z me.md
- Nie tworz zadan przed akceptacja listy ("ok" od usera)
- Nie dopisuj rzeczy ktore zrobil AI w tej sesji ("Claude przygotowal X" - to nie zadanie usera)
