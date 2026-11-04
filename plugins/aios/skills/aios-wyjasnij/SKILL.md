---
name: aios-wyjasnij
description: Wyjaśnia trudne pojęcie z vaulta w prostych słowach (jak 12-latkowi metodą Feynmana) i precyzyjnie diagnozuje miejsca, gdzie wyjaśnienie stało się mętne (luki). Używaj przy /wyjasnij, /aios-wyjasnij, /aios:wyjasnij, /feynman, "wytłumacz mi [pojęcie] jak 12-latkowi", "zrób feynmana z [tematu]".
---

# AIOS Wyjaśnij (Metoda Feynmana)

Weź pojęcie z `Wiedza/`, projektu lub notatki, wyjaśnij je w prostych słowach, a następnie wskaż dokładnie te miejsca, w których wyjaśnienie stało się mętne. Te miejsca to luki w zrozumieniu.

**Ten skill czyta wiedzę i nigdy nie edytuje istniejących notatek.** Zapisuje sesję do `_brudnopis/`, aby pozostał trwały ślad nauki, ale nie modyfikuje stron w `Wiedza/` ani materiałów źródłowych. Nauka to nie ingest.

## Jak wywołać

- `/wyjasnij`
- `/aios:wyjasnij`
- `/aios-wyjasnij`
- `/feynman`
- `/aios:feynman`
- "Wytłumacz mi [pojęcie] jak 12-latkowi"
- "Zrób Feynmana z [temat]"
- "W czym w tym temacie ściemniamy?"

## Procedura działania

### 1. Wybór pojęcia

Jeśli użytkownik wskazał temat lub plik, pracuj na nim. Jeśli nie, przejrzyj `Wiedza/` lub bieżący projekt i zaproponuj 3 kandydatów:
- notatkę, której nikt nie dotykał od miesięcy,
- notatkę ze statusem roboczym (draft),
- pojęcie kluczowe dla bieżącego projektu, którego mechanizm brzmi ogólnikowo.

### 2. Pogłębiona lektura

Przeczytaj wskazaną notatkę, powiązane z nią strony oraz pierwotne źródła (w `Raw/` lub RAG). Nie da się prosto wytłumaczyć czegoś, co przeczytało się po łebkach - wtedy powstaje parafraza, a parafraza ukrywa brak zrozumienia.

### 3. Wyjaśnienie dla 12-latka

- **Zero żargonu:** Jeśli pojęcie ma techniczną nazwę, użyj jej raz, a następnie opisz mechanizm słowami zrozumiałymi dla dziecka.
- **Zakaz zamiany pojęć:** "To w zasadzie heurystyka" niczego nie tłumaczy komuś, kto nie wie, czym jest heurystyka.
- **Konkretny przykład na początku:** Sytuacja z ludźmi i fizycznymi przedmiotami, zamiast "wyobraź sobie abstrakcyjny system".
- **Krótkie zdania:** Zdanie, które wymaga wielu przecinków, rozbij na dwa krótsze.
- **Dlaczego to ważne przed tym, jak to działa:** Najpierw sens dla człowieka, potem mechanika.
- **Tylko to, co jest w źródłach:** Jeśli notatka lub źródło nie wyjaśnia jakiegoś kroku, nie dopowiadaj go po cichu. To jest luka i należy ją nazwać w kroku 4.

**Odnośniki pod blokiem tekstu:**
Po każdym akapicie wyjaśnienia wstaw jednoznaczną linię odsyłacza:
`-> [[Nazwa Notatki#Nagłówek]]`

### 4. Diagnoza mętnych miejsc (Luki)

Przejrzyj swoje wyjaśnienie i znajdź każde miejsce, w którym:
- użyłeś trudnego słowa z braku prostego odpowiednika,
- napisałeś "w zasadzie" lub "po prostu", maskując brak detalu,
- opisałeś skutek bez wyjaśnienia przyczyny,
- pominąłeś krok, bo w notatkach też go brakowało.

Podziel luki na 3 kategorie:
- **Luka w vaulcie:** Notatka w bazie jest pobieżna, powierzchowna lub stwierdza fakt bez podania mechanizmu.
- **Luka w źródłach:** Źródła zewnętrzne, z których korzystamy, same nie wyjaśniły mechanizmu.
- **Luka w modelu:** Model przeczytał źródła, ale nie potrafi przełożyć tego prosto (brak zrozumienia).

### 5. Odwrócenie ról (Flip)

Poproś użytkownika o wyjaśnienie jednego wybranego fragmentu mechanizmu własnymi słowami i zadaj jedno pytanie pogłębiające poziom niżej.
Wyjaśnianie obnaża braki tego, kto tłumaczy:
- Gdy agent tłumaczy: ujawniają się luki notatek i bazy.
- Gdy człowiek tłumaczy: ujawniają się luki w jego intuicji tematu.

### 6. Zapis sesji

Zapisz wynik do pliku `_brudnopis/YYYY-MM-DD-feynman-[temat-slug].md`:

```markdown
---
data: YYYY-MM-DD
typ_wiedzy: "wniosek"
tematy: [feynman, nauka, <temat>]
podmioty: [Użytkownik]
ai_summary: "Sesja Feynmana na temat: <temat>. Proste wyjaśnienie pojęcia, diagnoza luk i wnioski."
---

# Feynman: [Pojęcie / Temat]

## Proste wyjaśnienie
[Treść prostego wyjaśnienia w blokach z linkami -> [[Notatka#Sekcja]]]

## Gdzie wyjaśnienie stało się mętne (Luki)
- **Luki w vaulcie:** [co w notatkach jest za płytkie]
- **Luki w źródłach:** [czego źródła nie wyjaśniają]
- **Luki w modelu:** [czego agent nie potrafił uprościć]

## Co zamknęłoby luki
- [Konkretne działania do podjęcia]

## Wnioski z dialogu
[Co wynikło z odwrócenia ról i odpowiedzi użytkownika]

## Rekomendowane następne kroki
1. [Krok 1]
2. [Krok 2]
3. [Krok 3]
```

### 7. Dalsze kroki

Zakończ sesję 2-3 ponumerowanymi, konkretnymi propozycjami (np. zbadanie luki w `_inbox/`, sprawdzenie oryginalnego artykułu, zrobienie Feynmana z pojęcia powiązanego).

## Inwarianty

- Żadna notatka w `Wiedza/` nie jest tworzona ani modyfikowana przez ten skill.
- Zapis trafia wyłącznie do `_brudnopis/`.
- Modyfikacja bazy wiedzy na podstawie luk to osobna, świadoma decyzja i workflow `/dodaj-do-wiki`.
