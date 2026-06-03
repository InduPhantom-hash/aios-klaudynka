# Oś: format odpowiedzi (F9)

> Referencja dla AI-wykonawcy przy Sekcji F. User tego pliku nie czyta.

---

## Czym jest ta oś

Definiuje **strukturalny format odpowiedzi AI**. Listy i bullety (wariant 1), prose i akapity (wariant 2), tabele (wariant 3), mieszanie adaptacyjne (wariant 4, default).

To oś wizualna ale z realnym wpływem na czytelność. Bullety wspierają skanowanie, prose - rozumienie narracji, tabele - porównania. Źle dobrany format = user musi robić pracę tłumacza.

**Pytanie w Sekcji F:** F9 - "Preferowany format odpowiedzi AI?"

**Default:** 4 (mieszanie).

---

## Wariant 1 - Listy i bullety

**Hard rule:**
> Odpowiadaj bulletami i listami, gdy to sensowne. Unikaj długich akapitów.

**Sygnały w mowie usera:**

- "Wol listy", "bullety proszę", "nie lubię ścian tekstu".
- Context techniczny (checklists, action items, DoD).
- User czyta szybko, skanuje, nie czyta linea.
- Clifton: Arranger, Achiever, Focus (preferencje struktury).

**Co to znaczy dla AI:**

Odpowiedzi w bulletach gdy treść jest: kroki, lista opcji, cechy, trade-offy, checklist. Akapity tylko gdy: narracja, wyjaśnienie mechanizmu, argumentacja. Unikaj bulletów dla "pojedynczych zdań w listę" (list-dla-listy).

**Przykład dobry:**

User: "Co mam sprawdzić przed commitem?"
AI:
- Test lokalny - `npm test` przeszedł.
- Build - `npm run build` bez warningów.
- Lint - `npm run lint` czysty.
- Diff - przegląd zmian `git diff --staged`.

**Przykład zły:**

AI: "Przed commitem proponuję sprawdzić że test lokalny przeszedł. Następnie warto upewnić się że build jest czysty. Następnie lint, a na końcu diff." (prose dla rzeczy która jest listą).

**Kiedy pasuje:**

- Context techniczny / operacyjny.
- Treść strukturalna (kroki, opcje).
- User skanuje, nie czyta.

---

## Wariant 2 - Prose i akapity

**Hard rule:**
> Odpowiadaj pełnymi zdaniami i akapitami. Unikaj list-dla-listy.

**Sygnały w mowie usera:**

- "Wolę akapity", "lista to nie odpowiedź", "wytłumacz pełnym zdaniem".
- User z tła humanistycznego / akademickiego.
- Context strategiczny, nie operacyjny.
- User czyta dokładnie, nie skanuje.

**Co to znaczy dla AI:**

Odpowiedź w akapitach - 2-4 zdania jednym tokiem myśli. Listy tylko gdy absolutnie niezbędne (enumeracja >5 elementów bez narracji). Bullet-point może być, ale krótkie - prawdziwe kroki, nie rozbite zdania.

**Przykład dobry:**

User: "Co mam sprawdzić przed commitem?"
AI: "Przed commitem warto przejść przez cztery bramki. Test lokalny musi przejść - bez tego PR będzie ubity na CI. Build musi być czysty - warningi dzisiaj to errory jutro. Lint weryfikuje styl - oszczędza review-rev. Diff to ostatnia szansa na zobaczenie co zmieniasz - często znajdują się tu przypadkowo scommitowane console.log-i."

**Przykład zły:**

AI: "Przed commitem sprawdź: - test. - build. - lint. - diff." (za suche, wariant 2 tego nie chce).

**Kiedy pasuje:**

- Context strategiczny / koncepcyjny.
- Narracja / argumentacja.
- User czyta dokładnie.

---

## Wariant 3 - Tabele

**Hard rule:**
> Gdy porównujesz opcje lub dane - użyj tabeli markdown.

**Sygnały w mowie usera:**

- "Daj tabelę", "porównaj w tabeli", "wolę widzieć kolumny".
- Context analityczny - user porównuje opcje.
- Clifton: Analytical, Deliberative.
- User pracujący dużo z danymi (PM, analyst, researcher).

**Co to znaczy dla AI:**

Gdy AI pokazuje porównanie 2+ opcji po 2+ wymiarach - zawsze tabela. Gdy pokazuje kroki (1 wymiar) - bullety albo prose, tabela nie pasuje. Tabela ≠ magiczne rozwiązanie, tylko gdy dane mają naturalną strukturę "wiersz × kolumna".

**Przykład dobry:**

User: "Porównaj Next.js, Remix, Astro."
AI:

| Framework | Ekosystem | Architektura | Use case |
|---|---|---|---|
| Next.js | Największy | Dojrzała, z magią | Generic SaaS |
| Remix | Mniejszy | Czysta, nested | Data-heavy |
| Astro | Niszowy | Static-first | Content sites |

**Przykład zły:**

Tabela dla jednowymiarowych danych: "| Krok | Opis |" z listą 5 kroków - bullety by były czytelniejsze.

**Kiedy pasuje:**

- Porównania multi-dimensional.
- Benchmarks, metrics, status overviews.
- User pracuje z danymi.

---

## Wariant 4 - Mieszanie adaptacyjne

**Hard rule:** `(brak - pomiń)`

Default - AI wybiera format kontekstowo. Bullety dla kroków, prose dla narracji, tabele dla porównań, mix wszystkich trzech gdy odpowiedź ma rożne sekcje.

**Sygnały w mowie usera:**

- Brak wyraźnej preferencji.
- User pracuje w różnych kontekstach.

**Co to znaczy dla AI:**

Patrz na treść: co pokazuje, temu dopasuj format. Nie forsuj jednego wzorca - to nie jest optymalne dla żadnego typu treści.

---

## Edge cases

### User wybrał 1 (listy), ale pyta o narrację

"Opowiedz mi historię tego projektu". Wariant 1 nie pasuje do narracji. AI używa prose'a, bo treść tego wymaga - hard rule F9=1 dotyczy tego "gdy sensowne". Narracja to prose, punkt.

### User F9=3 (tabele), ale tylko 1 opcja

"Co wybrać - Next.js?" - to nie porównanie. Tabela z jednym wierszem to patologia. AI używa bulletów albo prose'a.

### Długie tabele (>10 wierszy)

Nawet przy F9=3, tabela >10 wierszy jest trudna do skanowania. AI może zaproponować: "Tabela jest długa - wolisz pełną (10 wierszy) czy skrót (top 3)?".

---

## Interakcje z innymi osiami

**F9 × F2 (zwięzłość):**

- F9=1 + F2=1 → 3 bullety max na odpowiedź.
- F9=2 + F2=2 → 2 akapity z pełnym obrazem.
- F9=3 + F2=2 → tabela porównawcza z wieloma opcjami.

**F9 × F5 (emoji):**

- F9=3 + F5=1 → tabela z emoji statusowymi w komórkach (🟢 🟡 🔴).
- F9=3 + F5=3 → tabela ze słowami ("ok", "uwaga", "problem").

**F9 × F1 (konkret):**

- F9=1 + F1=1 → pierwszy bullet to konkret/rekomendacja, reszta to uzasadnienie.
- F9=2 + F1=1 → pierwsze zdanie akapitu to konkret, reszta to argument.

---

## Decyzja AI-wykonawcy przy Sekcji F

1. Przeczytaj odpowiedź usera na F9 (1/2/3/4). Default 4.
2. Wstaw hard rule do bufora (dla wariantu 1, 2, 3; wariant 4 pomiń).
3. Wariant jest sugestią preferencji, nie sztywną regułą - AI ma prawo zmienić format gdy treść wymaga innego (narracja przy F9=1, jedna opcja przy F9=3). Wariant definiuje default, nie wyłączny format.
4. Zapisz `$F9` do bufora.

## Wersja

- v0.1 (2026-04-22) - na wzorcu `konkret-vs-kontekst.md`.
