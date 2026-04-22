# Szablon: prywatność (Sekcja H)

> Referencja dla AI-wykonawcy przy **Sekcji H** pytań onboardingowych (6 pytań warunkowych). User tego pliku nie czyta.
> Poziom: dokumentacja budowy `me.md` + konfiguracji vaulta w obszarze danych prywatnych.

---

## Czym jest ta sekcja

Sekcja H ustala **strefę prywatną vaulta** - osobny zbiór reguł cytowania, anonimizacji, proaktywności i tabu, który obowiązuje w obrębie `Prywatne/` albo całego vaulta (jeśli user wybrał B1=prywatne).

To NIE jest oś preferencji komunikacyjnych (te są w Sekcji F). To konfiguracja granic - co wolno, co nie wolno, gdzie synchronizacja jest wyłączona.

**Pytania w Sekcji H:** H1-H6 (patrz `init-pytania-v02.md`).

---

## Warunkowość

Sekcja H uruchamia się tylko jeśli **B1 = prywatne** albo **B1 = hybryda**. Dla **B1 = zawodowe** pomijamy całość - vault nie ma strefy prywatnej, nie ma o czym pisać.

**Default dla hybrydy:** H3 (osobny folder `Prywatne/`) = tak. Użytkownik hybrydowy typowo chce rozgraniczenia - proponuj to jako sugerowany wybór, ale nie narzucaj.

**Edge case:** user wybiera B1=prywatne ale w H3 mówi "nie, nie chcę osobnego folderu". Wtedy całe `Projekty/` traktujesz jako strefę prywatną - reguły z H2, H4, H5, H6 obowiązują globalnie, nie tylko w `Prywatne/`. Zapisz to w `## Prywatność`: "Zasięg: cały vault (brak wydzielonego `Prywatne/`)."

---

## Artefakty generowane

### W `me.md`

Sekcja **`## Prywatność`** - tworzona jeśli którekolwiek z H2-H5 jest wypełnione. Struktura:

```markdown
## Prywatność

Zasięg: $zasięg (cały vault / tylko `Prywatne/`)

Osoby trzecie w notatkach: $tryb (imiennie / inicjały / pseudonimy)
Proaktywność w prywatnym: $tryb (proaktywnie / tylko gdy sam zacznę)

### Styl AI w prywatnym
$wolny-tekst-z-H4 (jeśli wypełniony)
```

Sekcja **`## Hard rules`** - dopisywane reguły z H1, H2 (jeśli nie-imiennie), H5 (jeśli opcja 2), H6:

- `Nie pytaj proaktywnie o: $tematy-H1.` (soft opt-out)
- `Przy cytowaniu notatek zawierających osoby trzecie - używaj $trybu-H2.` (np. `A.` zamiast `Agnieszka`)
- `W obrębie Prywatne/ - nie inicjuj wątków, czekaj na usera.` (hard rule z H5 opcja 2)
- `Nigdy nie komentuj: $tabu-H6. Nawet gdy sam o to zagadnę.` (hard opt-out, analogiczny do C5)

### W strukturze vaulta

- **H3=tak:** `Prywatne/` tworzone przez FIN2 wraz z `index.md` (pustą szablonową stroną).
- **H3=tak i E7=tak (git):** `Prywatne/` dopisane do `.gitignore`. Dodatkowo sugeruj dopisanie do `.gitignore` plików/katalogów wymienionych w H6 jako tabu (jeśli user pisze "moje finanse" - dopisz `Finanse/` do `.gitignore`).

---

## Zachowanie innych skilli w `Prywatne/`

Te zasady są dopisywane do `me.md`, ale również czytane aktywnie przez pozostałe skille:

- **`/aios:stworz-projekt`** - jeśli user promuje wątek z `_brudnopis/` a wątek ma sygnały prywatne (imiona z H2, słowa z H6), zapytaj: "To wygląda na prywatny wątek. Projekt pod `Projekty/` czy `Prywatne/`?" Default dla hybrydy: `Prywatne/`.
- **`/aios:dodaj-do-wiki`** - jeśli surowiec w `Wiedza/Raw/` zawiera dane wrażliwe (na podstawie H6 tabu), nie dodawaj do wiki globalnej - zaproponuj `Prywatne/Wiedza/` zamiast `Wiedza/`.
- **`/aios:sortuj`** - gdy przegląda `_inbox/` z plikiem prywatnym (sygnały jw.), opcja docelowa "Prywatne/" jest na górze listy propozycji, nie pod innymi.
- **`/aios:szukaj`** - przy wyszukiwaniu wyniki z `Prywatne/` są w osobnej grupie na końcu listy z etykietą `(prywatne)`. Nigdy nie pomijaj ich bez info dla usera - to byłoby oszukiwanie o stanie vaulta.
- **`/aios:koniec-sesji`** - transkrypt sesji zawierającej treści z `Prywatne/` nie idzie do `_brudnopis/` globalnego, tylko do `Prywatne/_brudnopis/` (jeśli istnieje) albo skrócony (bez konkretów prywatnych) do globalnego z etykietą `[SESJA: część prywatna skrócona]`.

---

## Decyzja AI-wykonawcy w przypadkach krańcowych

### H1 pytanie, ale user wpisał "wszystko"

Nie przyjmuj. Odpowiedź "wszystko" wypacza hard rule - AI nie mógłby w ogóle rozmawiać proaktywnie. Zadaj kontrpytanie: "Co konkretnie chciałbyś wyłączyć? Listę 2-5 tematów, nie 'wszystko'." Jeśli user nalega na "wszystko" - zamiast hard rule w sekcji Hard rules dopisz do `## Prywatność`: "Proaktywność AI: wyłączona w całym vaulcie. AI reaguje tylko gdy user zaczyna." To jest inna semantycznie rzecz niż H1.

### H2 pseudonimy, ale user nie podaje listy

Jeśli user wybiera "3. pseudonimy" ale nie podaje mapowania (np. `Agnieszka -> A.` albo `Agnieszka -> Magda`), dopisz w `## Prywatność`: "Osoby trzecie: pseudonimy (mapowanie do ustalenia na bieżąco)." i dodaj w Hard rules: "Przy pierwszym wystąpieniu nowej osoby w notatce zaproponuj pseudonim, poczekaj na potwierdzenie, zapisz mapowanie w `_pamiec/pseudonimy.md`." Ten plik tworzy się dopiero przy pierwszym użyciu, nie w FIN2.

### H3=tak, E7=nie (brak gita)

Folder `Prywatne/` tworzymy, ale nie dopisujemy do `.gitignore` (nie ma gita). W `## Prywatność` dopisz: "Prywatne/: wydzielone, ale bez git-exclude (vault nie używa gita)." Przypomnij userowi, że jeśli kiedyś zainicjalizuje gita - `Prywatne/` trzeba ręcznie dopisać do `.gitignore` albo użyć `/aios:init --repair`.

### H6 zbiega się z F (tryb sporu)

Przykład: user w F3 wybiera "lubię gdy AI się spiera", ale w H6 dopisuje "nie komentuj zdrowia". To nie jest konflikt - H6 jest hard override. W kodzie priorytetów: H6 > F. Dopisz komentarz inline w `## Hard rules`: "Tabu z H6 obowiązuje mimo F3 'spieraj się' - nie ma sporu o tabu."

### User chce strefę prywatną, ale nie chce odpowiadać na H2-H6

Akceptuj i przejdź dalej. `## Prywatność` wtedy zawiera tylko: "Zasięg: $zasięg. Szczegóły do uzupełnienia później (`/aios:init --rezerwa H`)." Nie blokuj ukończenia onboardingu z powodu niewypełnionej H - to jest sekcja warunkowa i częściowa wypełnialność jest OK. Odrocz zadawanie H na później.

---

## Co NIE trafia do `me.md`

Sekcja H nie generuje:

- **Konkretnych treści prywatnych** (imion, diagnoz, szczegółów finansowych). User wypełnia tylko **meta-konfigurację**: tryby, granice, tabu. Szczegóły zostają w notatkach vaulta, nie w profilu.
- **Deklaracji wiary / orientacji / diagnozy zdrowia.** Jeśli user sam je poda jako odpowiedź - zatrzymaj się: "Tego nie zapisuję w `me.md`. Jeśli chcesz żeby AI o tym pamiętało, zrób notatkę w `Prywatne/`, a w H6 dopisz 'nie komentuj [temat] proaktywnie'."
- **Hasła, API keys, numery kart.** Jeśli user wklei - nie zapisuj i poproś o usunięcie z kontekstu sesji.

Reguła: `me.md` jest **AI-readable profile**. To, co user chce zostawić dla siebie, zostaje poza profilem (w `Prywatne/` vaulta albo w ogóle poza AIOS).

---

## Wersja

v0.1 (2026-04-22) - pierwszy szablon. Dopełnia biblioteki `szablony/` o sekcję H (jedyna warunkowa sekcja onboardingu).
