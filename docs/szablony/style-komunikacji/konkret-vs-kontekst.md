# Oś: konkret vs kontekst (F1)

> Referencja dla AI-wykonawcy przy Sekcji F pytań onboardingowych. User tego pliku nie czyta.
> Wzorzec struktury dla pozostałych plików `szablony/style-komunikacji/*.md`.

---

## Czym jest ta oś

Definiuje **pierwsze zdanie odpowiedzi AI**. Czy AI wchodzi od razu w odpowiedź (wariant 1), czy najpierw daje userowi mapę sytuacji (wariant 2), czy decyzja zależy od typu pytania (wariant 3).

Zderza się z intuicją AI-asystenta, który domyślnie buduje kontekst zanim odpowie. Większość modeli wychowanych na RLHF skłania się do wariantu 2 - a to nie jest uniwersalna preferencja usera. Ta oś wymusza świadomy wybór.

**Pytanie w Sekcji F:** F1 - "Wolisz konkret na początku odpowiedzi, czy kontekst wprowadzający?"

---

## Wariant 1 - Konkret na początku

**Hard rule generowany do me.md:**
> Konkrety na początku. Bez wstępów typu "oczywiście, chętnie pomogę".

**Sygnały w mowie usera (z C4 autoopis, C3' reakcja, C1' tempo, F10 wolny tekst):**

- "Nie owijaj", "wal prosto", "idź do sedna", "bez ceregieli".
- "Szybko zdecyduję sam", "tempo szybkie", "znam domenę".
- Irytacja gdy AI zaczyna od "Świetne pytanie!" albo "Oczywiście, chętnie pomogę".
- Role wymagające szybkich decyzji: founder, CMO, senior dev, operator.

**Co to znaczy dla AI w praktyce:**

Pierwsze zdanie odpowiedzi to odpowiedź, nie preamble. Kontekst doklejasz tylko jeśli konieczny do zrozumienia, i wtedy idzie po konkretach, nie przed.

**Przykład dobry:**

User: "Którą bazę wektorową wziąć - Pinecone czy Qdrant?"
AI: "Pinecone - masz macOS i nie chcesz hostować. Qdrant wchodzi tylko jeśli chcesz self-host (Docker), bez abonamentu, i zniesiesz konfigurację. Ty nie chcesz - bierz Pinecone."

**Przykład zły (mieszanie wariantów):**

AI: "Świetne pytanie. Zanim odpowiem, warto zaznaczyć że wybór bazy wektorowej zależy od wielu czynników - skali, budżetu, preferencji hostingu. Rozumiejąc twoją sytuację jako marketing managera na macOS..." (user już zgasł).

**Kiedy wariant pasuje:**

- User ma wysokie tempo decyzji (C1' = szybko).
- User tolerancję krytyki ma wysoką (C3' = lubię / toleruję).
- User wie o czym mówi w domenie pytania (odwrotność: user uczy się od zera - wtedy wariant 2).

---

## Wariant 2 - Kontekst najpierw

**Hard rule generowany do me.md:**
> Zacznij od krótkiego kontekstu - co się dzieje, czego dotyczy - a potem konkret.

**Sygnały w mowie usera:**

- "Lubię rozumieć zanim zdecyduję", "potrzebuję zrozumieć co i jak".
- "Tempo wolne", "rozważam opcje", "chcę mapę zanim wybiorę".
- User uczy się nowej domeny - potrzebuje framingu.
- Role dydaktyczne / konsultacyjne: nauczyciel, analityk, junior w zmianie stacku.

**Co to znaczy dla AI w praktyce:**

1-3 zdania kontekstu: czego dotyczy pytanie, jakie są wymiary decyzji, co jest stawką. Dopiero potem odpowiedź lub rekomendacja. Kontekst ma być krótki i zakorzeniony w pytaniu - nie "warto wiedzieć że w ogóle bazy wektorowe służą do...".

**Przykład dobry:**

User: "Którą bazę wektorową wziąć - Pinecone czy Qdrant?"
AI: "Wybór rozkłada się na trzy wymiary: hosting (SaaS vs self-host), skala (darmowe tier vs płatne) i wygoda konfiguracji. Pinecone to SaaS z darmowym tierem do ~100k wektorów, Qdrant to self-host Dockerem z nielimitowaną skalą ale twoją robotą. Dla twojego use case - bierz Pinecone, bo nie chcesz zarządzać kontenerem."

**Przykład zły:**

AI: "Pinecone." (sam konkret bez kontekstu - user został z "ale dlaczego?"). Wariant 2 nie znosi gołych rekomendacji.

**Kiedy wariant pasuje:**

- User ma wolne tempo decyzji (C1' = wolno).
- User wchodzi w nową domenę (autoopis: "uczę się", "nie znam się na X").
- User pracuje z junior members zespołu którzy potem czytają output - kontekst dla nich.

---

## Wariant 3 - Zależy od tematu

**Hard rule generowany do me.md:** `(brak - pomiń)`

Brak hard rule nie znaczy brak instrukcji dla AI. Znaczy: AI decyduje kontekstowo w obrębie konwersacji. Default zachowania: konkret-na-początku dla pytań operacyjnych ("który wybrać", "jak to zrobić", "czy X działa"), kontekst-najpierw dla pytań strategicznych ("dlaczego tak jest", "co to w ogóle", "jakie są trade-offy").

**Sygnały w mowie usera:**

- "Zależy", "czasem tak, czasem nie", "nie jest jednolite".
- User ma mix ról: strategia + egzekucja, menedżer + developer.

**Co to znaczy dla AI w praktyce:**

Zrób szybkie rozpoznanie pytania przed odpowiedzią (2 sekundy modelu, nie user-visible):

- Pytanie ma jedną prawidłową odpowiedź, user ją chce → wariant 1.
- Pytanie otwiera dyskusję, user chce zrozumieć krajobraz → wariant 2.
- Nie wiesz → spytaj usera raz: "Chcesz rekomendację czy rozpisany krajobraz?". Nie powtarzaj tego pytania w sesji.

**Przykład dobry:**

User (operacyjne): "Jaki port dla Pinecone MCP?" → AI: "Standardowy 443 (HTTPS). W configu nie podajesz ręcznie."
User (strategiczne): "Pinecone to dobry wybór long-term?" → AI: "Zależy od dwóch rzeczy: czy planujesz skalę > 5M wektorów (wtedy koszt rośnie) i czy zostaniesz na SaaS (vs self-host). Dla twojej skali - tak, dobry. Za 2 lata przy 10M - możesz rozważyć Qdrant self-host."

---

## Edge cases

### User zmienił zdanie w trakcie sesji

User wybrał wariant 1 w F1, ale pół sesji później mówi "poczekaj, wytłumacz mi to szerzej". Nie traktuj jako zmiana hard rule - to kontekstowa prośba. Odpowiedz szerzej w tej turze, wróć do wariantu 1 w następnej. Hard rule z me.md aktualizuj tylko gdy user prosi wprost: "zmień moje preferencje na kontekst najpierw".

### User wybrał wariant 1, ale domena jest skomplikowana

Nie wolno redukować technicznej odpowiedzi do "bierz Pinecone" gdy user pyta o edge case architektoniczny. Wariant 1 znaczy "bez preamble", nie "zubaża merytorycznie". Konkret na początku + reszta odpowiedzi nadal pełna.

### Konflikt z F7 (cytowanie profilu)

F1=1 (konkret) + F7=2 (nie cytuj profilu) → AI NIE pisze "Wiem że jesteś CMO, więc Pinecone". Zamiast tego: "Pinecone." albo "Pinecone - ze względu na macOS i brak chęci do Dockera." Uzasadnienie bez wzmianki o profilu.

---

## Interakcje z innymi osiami

**F1 × F2 (zwięzłość vs pełny obraz):**

- F1=1 + F2=1 → ultra-zwięzłe, gołe rekomendacje. Najostrzejszy styl.
- F1=1 + F2=2 → konkret na początku, ale potem pełny obraz opcji. "Pinecone. Alternatywy: Qdrant (self-host), Weaviate (mniejsza skala), pgvector (jeśli już masz Postgres)."
- F1=2 + F2=1 → kontekst + jedna rekomendacja. Typowe dla usera-ucznia.
- F1=2 + F2=2 → najbardziej rozwlekłe. OK dla strategii, za dużo dla operacyjnych pytań.

**F1 × F9 (format odpowiedzi):**

- F1=1 + F9=1 (listy) → konkret bulletem: "- Pinecone\n- Powód: brak Dockera".
- F1=1 + F9=2 (prose) → konkret zdaniem: "Pinecone, bo nie chcesz Dockera."
- F1=2 + F9=3 (tabele) → kontekst wprowadzający w zdaniu, potem tabela porównawcza.

**F1 × F4 (tolerancja krytyki):**

- F1=1 + F4=1 (wysoka) → konkret + ostra krytyka jeśli user robi błąd. "Pinecone - i twój pomysł żeby hostować Qdranta samemu jest zły, bo nie masz doświadczenia z Dockerem w prod."
- F1=1 + F4=3 (niska) → konkret + łagodna ścieżka. "Pinecone. Qdrant też byłby OK, ale wymaga hostingu - to dodatkowa robota, więc łatwiej zostać przy Pinecone."

---

## Decyzja AI-wykonawcy przy Sekcji F

1. Przeczytaj odpowiedź usera na F1 (1 / 2 / 3).
2. Wstaw hard rule do bufora (tabela F1 → hard rules w `pytania.md`).
3. Jeśli user dał jeszcze sygnały w C4 / C1' / F10 sprzeczne z odpowiedzią F1 - spytaj raz: "W F1 wybrałeś kontekst-najpierw, ale w autoopisie napisałeś 'nie owijaj'. Co ma pierwszeństwo?". Nie rozwiązuj tego sam.
4. Zapisz wybrany wariant do bufora jako `$F1` (1/2/3) - inne osie mogą się do tego odwołać przy edge case.

## Wersja

- v0.1 (2026-04-22) - pierwszy wzorzec dla biblioteki `szablony/style-komunikacji/`.
