# Parsowanie PDF: FRIS i Clifton

> Referencja dla AI-wykonawcy przy Sekcji C onboardingu (`/aios:init`). User tego pliku nie czyta.

---

## Po co ten dokument

W Sekcji C user podaje `$MA_PROFILE_PDF = tak` i wkleja/linkuje raport FRIS albo Clifton Strengths. AI ma przeczytać PDF multimodalnie, wyciągnąć najważniejsze sygnały i zaproponować userowi interpretację do potwierdzenia.

**Dlaczego multimodalnie, a nie tekst:** raporty FRIS i Clifton często mają wykresy, koła, tabele profilu. Plain-text ekstrakcja gubi ranking talentów, procenty stylów, kolorystykę domen. AI musi widzieć PDF jako obraz (Claude multimodal) + tekst (dla cytatów).

**Dlaczego potwierdzenie:** user może mieć raport sprzed lat - interpretacja mogła się zmienić. Albo raport mógł być źle wypełniony. Albo user identyfikuje się z wynikiem częściowo. AI nie zapisuje do me.md bez eksplicitnej zgody na kluczowe elementy.

**Output z Sekcji C:** `$FRIS_STYL`, `$FRIS_PERSPEKTYWA`, `$CLIFTON_TOP5` (lista), `$CLIFTON_DOMINUJACA_DOMENA`. Plus opcjonalnie `$TEMPO` (C6), `$REAKCJA_KRYTYKA` (C7) - hybryda light z C'.

---

## FRIS - co wyciągać

### Cztery style myślenia

FRIS rozróżnia cztery podstawowe style (S, F, I, R) + perspektywy. Użytkownik ma jeden dominujący styl + hierarchię preferencji pozostałych trzech.

**S - Struktura (Strażnik):**

- Myślenie proceduralne, liniowe, oparte na sprawdzonych rozwiązaniach.
- Silne strony: dyscyplina, skrupulatność, powtarzalność.
- W PDF szukaj: wysokie S na wykresie, słowa "konsekwentny", "uporządkowany", "systematyczny".

**F - Fakty (Badacz):**

- Myślenie analityczne, oparte na danych, liczbach, dowodach.
- Silne strony: logika, precyzja, dokładność.
- W PDF szukaj: wysokie F, słowa "analityczny", "rzetelny", "dociekliwy".

**I - Idee (Wizjoner):**

- Myślenie kreatywne, skojarzeniowe, koncepcyjne.
- Silne strony: wizja, generowanie pomysłów, łączenie dziedzin.
- W PDF szukaj: wysokie I, słowa "kreatywny", "oryginalny", "wizjonerski".

**R - Relacje (Partner/Zawodnik):**

- Myślenie skupione na ludziach, interakcji, energii grupy.
- Silne strony: empatia, komunikacja, budowanie relacji.
- W PDF szukaj: wysokie R, słowa "empatyczny", "zespołowy", "zorientowany na ludzi".

### Perspektywy (rozszerzenie)

FRIS poza stylem podaje perspektywę - sposób działania w sytuacji zadaniowej. Perspektywy to kombinacje dwóch najsilniejszych stylów. Najpopularniejsze:

- **Badacz (F>I)** - analiza przed działaniem, gromadzenie danych, głęboka refleksja.
- **Wizjoner (I>F)** - generowanie koncepcji przed analizą, big picture przed szczegółami.
- **Zawodnik (R>I)** - działanie w zespole, energia interakcji, szybkie decyzje.
- **Partner (R>S)** - wsparcie, budowanie relacji długoterminowych, konsekwencja w zespole.
- **Strateg (F>S)** - planowanie oparte na faktach, metodyczne wdrażanie.
- **Entuzjasta (R>F)** - przekonywanie danymi z energią społeczną.

### Co AI zapisuje do me.md

Format preferowany:

> FRIS: S>>F>I>>R (2024, Badacz/Indywidualista)

Znaczenie:

- `S>>F>I>>R` - hierarchia preferencji (`>>` = duża przewaga, `>` = mniejsza).
- `2024` - rok raportu (ważne - style mogą ewoluować).
- `Badacz/Indywidualista` - perspektywa + subtyp (jeśli raport podaje).

Jeśli PDF podaje tylko perspektywę bez hierarchii (stary format) - zapisz samą perspektywę, oznacz jako `?` w hierarchii.

### Sygnały styl pracy (dla buforu AI, nie do me.md wprost)

Styl FRIS informuje jak AI ma się komunikować z userem:

- Badacz → pełny obraz przed rekomendacją (F2=2 default).
- Wizjoner → big picture, unikaj utopienia w szczegółach.
- Zawodnik → energia, tempo, akcja.
- Strateg → metodyczny, oparty na danych.

AI **nie cytuje** tego userowi bez F7=1 (patrz `cytowanie-profilu.md`).

---

## Clifton Strengths - co wyciągać

### 34 talenty w 4 domenach

Clifton (Gallup) rozróżnia 34 talenty w 4 domenach. User ma ranking Top 5 (albo Top 10, albo pełne 34 - zależnie od raportu).

**Executing (Wykonawcze) - "jak dopiąć":**

Achiever, Arranger, Belief, Consistency, Deliberative, Discipline, Focus, Responsibility, Restorative.

**Influencing (Wywierające wpływ) - "jak sprzedać/przekonać":**

Activator, Command, Communication, Competition, Maximizer, Self-Assurance, Significance, Woo.

**Relationship Building (Relacyjne) - "jak budować więzi":**

Adaptability, Connectedness, Developer, Empathy, Harmony, Includer, Individualization, Positivity, Relator.

**Strategic Thinking (Strategiczne) - "jak myśleć":**

Analytical, Context, Futuristic, Ideation, Input, Intellection, Learner, Strategic.

### Co AI wyciąga z PDF

1. **Lista Top 5 w kolejności** (najważniejsze - `$CLIFTON_TOP5`).
2. **Dominująca domena** (liczebnie - jeśli 3+ z 5 w jednej domenie, to ona dominuje).
3. **Opcjonalnie Top 10** (jeśli user poda rozszerzony raport).

### Format zapisu do me.md

Format preferowany (przykład):

> Clifton Top 5: Maximizer, Ideation, Significance, Activator, Deliberative (2023, mix Strategic/Influencing)

Znaczenie:

- Lista w kolejności rankingu (pozycja 1 → 5).
- Rok raportu.
- Domena dominująca lub mix dwóch jeśli balans.

### Sygnały dla AI (bufor, nie do me.md)

Clifton informuje AI jak user podejmuje decyzje i reaguje:

**Maximizer** → user nie zadowala się "wystarczające", chce najlepsze. AI pokazuje top options, nie 5 średnich.

**Deliberative** → user waży trade-offy, nie lubi pochopnych decyzji. AI daje pełny obraz, nie jedną rekomendację z punktu.

**Activator** → user chce akcji szybko. AI daje rekomendację first, uzasadnienie drugie.

**Strategic** → user lubi mechanizmy, nie tylko "co robić". AI tłumaczy "dlaczego" obok "co".

**Learner** → user chce się uczyć, nie tylko dostać gotowe. AI pokazuje jak doszedł do wyniku.

**Analytical** → user pyta o dane. AI backup każdego claima liczbami/faktami.

**Ideation** → user lubi burze mózgów. AI daje alternatywy, nie monokulturę jednej opcji.

**Significance** → user chce mieć wpływ, widoczny ślad. AI unika trywialnych zadań jako głównych rekomendacji.

**Empathy / Relator** → user reaguje na ton. AI trzyma ciepło + rzeczowość.

**Command / Competition** → user akceptuje direct push-back. AI nie owija w bawełnę.

AI **nie cytuje** tych sygnałów bez F7=1. Używa niewidzialnie do kalibracji.

---

## Jak czytać PDF multimodalnie

### Krok 1: Rozpoznaj typ raportu

Po pierwszej stronie AI identyfikuje: FRIS / Clifton / Gallup / inny. Jeśli inny (np. DISC, MBTI, Insights) - AI pyta usera jak zmapować na FRIS/Clifton albo pomija.

### Krok 2: Wyciąg kluczowych elementów

**Z FRIS:**

1. Tabela / koło / wykres 4 stylów → hierarchia.
2. Nagłówek perspektywy (jeśli obecny) → `$FRIS_PERSPEKTYWA`.
3. Data wydania raportu → rok do zapisu.

**Z Clifton:**

1. Sekcja "Your Top 5" (zawsze pierwsza po intro) → lista.
2. Opisy każdego talentu - skim dla kontekstu (AI używa tylko nazw, nie opisów).
3. Data wydania / wersja raportu.

### Krok 3: Cytaty na potrzeby weryfikacji

AI wyciąga 2-3 krótkie cytaty (1-2 zdania każdy) z PDF - najczęściej z sekcji "podsumowanie profilu" albo "co cię charakteryzuje". Cytaty służą jako "kotwice" dla usera ("czy to cię opisuje?").

**Przykład:**

> W raporcie znalazłem: "osoba analityczna, potrzebująca pełnego obrazu przed decyzją, z wyraźną preferencją dla merytorycznej dyskusji". Czy się z tym utożsamiasz?

Nie kopiuj całych akapitów - 1-2 zdania wystarczą.

### Krok 4: Propozycja interpretacji

AI prezentuje userowi:

1. Wyciąg strukturalny: "FRIS: S>>F>I>>R, Badacz. Clifton Top 5: [lista]."
2. 2-3 cytaty-kotwice.
3. Pytanie: "Zapisać tak do profilu? Czy chcesz coś skorygować?"

User odpowiada: (a) tak, (b) koryguję [co], (c) zmień na [X]. AI zapisuje dopiero po potwierdzeniu.

---

## Weryfikacja z userem

### Case dobry: user potwierdza

User: "Zgadza się, zapisz."

AI zapisuje do `me.md` + updatuje bufor `$FRIS_STYL`, `$CLIFTON_TOP5`.

### Case: user koryguje pojedyncze

User: "Dobrze, ale Significance to nie 3 tylko 5. Zamień z Activator."

AI koryguje listę, zapisuje po korekcie. Nie pyta ponownie.

### Case: user kwestionuje cały wynik

User: "Ten raport jest z 2019 i się nie identyfikuję. Pomiń FRIS."

AI ustawia `$FRIS_STYL = null`, pyta czy przerzucić na C' (wariant bez PDF) dla stylu pracy. Nie nalega.

### Case: user nie rozumie wyniku

User: "Co to znaczy Badacz?"

AI tłumaczy perspektywę w 2-3 zdaniach (bez kopiowania całych akapitów z PDF). Po wyjaśnieniu pyta czy zapisać.

---

## Edge cases

### PDF nie jest raportem FRIS ani Clifton

AI rozpoznaje (np. CV, kontrakt) - odpowiada: "Ten PDF nie wygląda na raport FRIS/Clifton. Podaj właściwy albo zmień na C' (bez PDF)."

### PDF jest raportem, ale rozmyty / z skanów

OCR może pogorszyć dokładność. AI ostrzega: "Jakość tekstu w PDF jest słaba - mogę się mylić. Zweryfikuj szczególnie Top 5." User potwierdza lub koryguje.

### User ma FRIS ale nie Clifton (albo odwrotnie)

Normalny case. AI wypełnia tylko to co dostępne. `$CLIFTON_TOP5 = null` jeśli brak. W me.md pomija linię.

### User ma oba raporty, ale z różnych lat

AI zapisuje oba z datami. Jeśli różnica >5 lat - AI zauważa "Raporty są z różnych lat ({rok_FRIS}, {rok_Clifton}). Jeśli były istotne zmiany, może zrób nowy Clifton."

### User wkleja tylko fragment PDF (screenshot)

AI próbuje wyciągnąć z fragmentu. Jeśli brak Top 5 (tylko opis 1 talentu) - prosi o pełną listę Top 5 w formie tekstu.

---

## Prywatność i konsent

FRIS i Clifton to dane wrażliwe (profilowanie psychologiczne). Sekcja G onboardingu pyta o opt-in do AI-readable w me.md. Jeśli user wybrał G1=nie (profil tylko do prywatnego użytku, nie do me.md) - AI zapisuje do osobnego pliku (`_pamiec/profil-prywatny.md`) z oznaczeniem "Nie-AI-readable". Me.md zostaje bez profilu.

Patrz: `szablony/prywatnosc.md` (jeszcze do napisania) dla pełnej logiki.

---

## Interakcje z innymi sekcjami

**Sekcja C × Sekcja F:**

- FRIS/Clifton informują default dla F2 (zwięzłość), F4 (tolerancja krytyki), F6 (humor). Jeśli user nie wybrał F-osi explicite, AI może zaproponować default oparty na profilu. Ale F7 (cytowanie profilu) nie ma defaultu z profilu - default 2 (nie cytuj).

**Sekcja C × C' (hybryda):**

- C' miało być rozdzielne (tylko bez-PDF). Hybryda light (2026-04-22): C6 (tempo) i C7 (reakcja na krytykę) dodane do C jako doprecyzowanie - sygnały nieobecne w większości raportów FRIS/Clifton.

**Sekcja C × Sekcja G (prywatność):**

- G1 kontroluje czy profil ląduje w me.md. Jeśli G1=nie, C wypełnia bufor, ale nie zapisuje do me.md. Bufor dostępny tylko w obrębie bieżącej sesji.

---

## Wersja

- v0.1 (2026-04-22) - pierwsza iteracja. Pokrywa FRIS (4 style + perspektywy) + Clifton (34 talenty w 4 domenach) + flow multimodalny + weryfikacja z userem.

## TODO (później)

- Dodać mapowanie DISC/MBTI/Insights → FRIS/Clifton (jeśli użytkownik chce przekonwertować).
- Dodać przykładowe screenshoty typowych sekcji FRIS/Clifton (dla AI-wykonawcy w fazie wizualnej identyfikacji).
- Rozszerzyć o raporty Gallup (Strengths Finder) - starsza wersja Clifton, różni się formatem.
