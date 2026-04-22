# pytania.md - 55 pytań onboardingowych AIOS-Klaudynki

> Ten plik jest **referencją dla skilla `init`**. Skill wczytuje sekcje po kolei i zadaje pytania userowi. Format każdego pytania:
>
> ```
> ### $ID - $Tytul
> **Pytanie:** <treść>
> **Typ odpowiedzi:** <wybór z listy / wolny tekst / liczba / ścieżka / tak-nie>
> **Warianty** (jeśli wybór z listy): 1. $A, 2. $B, ...
> **Default** (jeśli jest): $Default
> **Warunkowe** (jeśli dotyczy): $Zaleznosc
> **Generuje:** <co trafia do me.md / struktury vaulta>
> **Uwagi dla AI:** <dodatkowy kontekst dla wykonawcy>
> ```

**Status wersji:** v0.2.2 (hybryda light w C dla ścieżki z PDF, razem 57/57).

**Zmiany v0.2.2 vs v0.2.1 (2026-04-22):**
- Dodane C6 (tempo) i C7 (krytyka) jako uzupełnienie ścieżki z PDF - PDF daje typologię, te 2 pytania praktyczne preferencje pracy. Warunkowe od `$MA_PROFILE_PDF = tak`. Ścieżka bez PDF (C1'-C4') bez zmian.

**Zmiany v02 vs v01:**
- Pole `Generuje:` wstawione przy każdym pytaniu i wypełnione (57/57 po v0.2.2).
- Pole `Warunkowe:` jawnie oznaczone (dawniej implicit).
- Sekcja F: tytuł neutralny (usunięty "Wariant C" z nagłówka - do komentarza wewnątrz).
- J2/J3: potwierdzenie defaultu z E7/E3 zamiast ponownego pytania (DRY).
- Podsumowanie: usunięta wzmianka o "trybie szybkim F = 5 pytań" (decyzja 2026-04-21: F zawsze 10).
- E6: jawna warunkowość od E5 = tak.
- Dodana sekcja **Mapowanie F1-F10 → hard rules** na końcu.

**Konwencje generowania (globalne):**
- Wszystkie zmienne `$imie`, `$rola` itd. odnoszą się do bufora odpowiedzi usera.
- me.md buduje się z sekcji: `Hard rules` (F + C5), `Kim jestem` (A), `Profil psychologiczny` (C, opcjonalne), `Styl pracy` (C' i F), `Aktywne projekty` (D, tabela), `Stack` (E), `Rytm pracy` (G), `Prywatność` (H, warunkowe).
- Struktura folderów: `Projekty/<kategoria>/index.md` (z D), `Kalendarz/` (z G), `Prywatne/` (z H3, warunkowo), `Wiedza/Raw/` (z I).
- Nazwy folderów bez polskich znaków diakrytycznych (tytuły w `index.md` mogą mieć diakrytyki).

---

## Sekcja A - Tożsamość (5 pytań)

**Cel sekcji:** wiedzieć z kim skill rozmawia i w jakim kontekście (zawodowym / osobistym). Minimum do wygenerowania nagłówka `me.md`.

### A1 - Imię

**Pytanie:** Jak mam się do ciebie zwracać w `me.md`?
**Typ odpowiedzi:** wolny tekst (1 linia)
**Generuje:** wstawia `$imie` jako nagłówek `# me.md - Profil $imie` oraz do zdania otwierającego sekcję "Kim jestem" w `me.md`.
**Uwagi dla AI:** nie pytaj o nazwisko - imię wystarczy.

### A2 - Rola zawodowa

**Pytanie:** Jednym zdaniem - czym się zawodowo zajmujesz?
**Typ odpowiedzi:** wolny tekst
**Generuje:** dopisuje `$rola` jako pierwsze zdanie w sekcji "Kim jestem" w `me.md` (po imieniu). Używane też do dopasowania archetypu po Sekcji D.

### A3 - Branża / domena

**Pytanie:** Jeśli rola tego nie oddaje - w jakiej branży / domenie pracujesz?
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje "Pracuję w branży $branza." jako drugie zdanie sekcji "Kim jestem". Jeśli puste - pomija.

### A4 - Strefa czasowa

**Pytanie:** W jakiej strefie czasowej jesteś?
**Typ odpowiedzi:** wybór z listy + "inne"
**Warianty:** 1. Europe/Warsaw (PL), 2. Europe/London, 3. Europe/Berlin, 4. inne
**Default:** Europe/Warsaw
**Generuje:** dopisuje linię "Strefa czasowa: $tz." w sekcji "Kim jestem". Używane też w Sekcji G do kalibracji rytmu (np. "poranek" w Europe/Warsaw = 6-10).

### A5 - Język vaulta

**Pytanie:** W jakim języku prowadzisz vault?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. polski, 2. angielski, 3. mieszanie
**Default:** polski (v1 Klaudynki jest tylko PL)
**Generuje:** dopisuje linię "Język vaulta: $jezyk." w sekcji "Kim jestem". Używane przez wszystkie pozostałe skille jako default language (np. `/aios:szukaj` odpowiada w tym języku).

---

## Sekcja B - Zakres systemu (3 pytania)

**Cel sekcji:** ustalić czy vault jest zawodowy, prywatny, czy hybrydowy. Decyzja wpływa na strukturę `Projekty/` i czy Sekcja H w ogóle się uruchamia.

### B1 - Zakres vaulta

**Pytanie:** Czego dotyczy ten vault?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tylko zawodowe, 2. tylko prywatne, 3. hybryda (oba)
**Generuje:** zapisuje `$zakres` do bufora sesyjnego. Sterowanie: jeśli `$zakres` = 2 lub 3 - aktywuje Sekcję H. Jeśli `$zakres` = 3 - aktywuje B2. W me.md nie dopisuje osobnego pola (zakres widać po strukturze `Projekty/`).
**Uwagi dla AI:** jeśli 3 (hybryda) - aktywuje Sekcję H. W innych przypadkach H pomijana.

### B2 - Struktura hybrydy

**Pytanie:** Rozdzielasz zawodowe i prywatne w strukturze folderów, czy mieszasz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. rozdziel (osobne katalogi), 2. mieszaj (wspólna struktura)
**Default:** rozdziel
**Warunkowe:** tylko jeśli B1 = hybryda
**Generuje:** jeśli 1 - w FIN2 tworzy dwa root-foldery `Projekty/Praca/` i `Projekty/Prywatne/`, kategorie z D idą pod odpowiedni. Jeśli 2 - kategorie idą płasko pod `Projekty/` bez rozdziału.

### B3 - Dostęp osób trzecich

**Pytanie:** Czy ktoś inny (współpracownik, coach, partner) będzie miał dostęp do tego vaulta?
**Typ odpowiedzi:** tak/nie
**Generuje:** jeśli tak - dopisuje do `## Hard rules` w me.md zdanie: "W vault mogą zaglądać osoby trzecie - uważaj na dane osobowe i prywatne komentarze." Jeśli nie - nic nie dopisuje.
**Uwagi dla AI:** jeśli tak - w hard rules dodaj "ostrożność z danymi osobowymi osób trzecich".

---

## Sekcja C - Profile psychologiczne (5 pytań, opcjonalne)

**Cel sekcji:** zebrać sygnały o stylu myślenia / działania usera, żeby lepiej skalibrować `hard rules` w sekcji F.

**Mechanika PDF (decyzja 2026-04-21):** AI czyta PDF natywnie (multimodal), wyciąga typ FRIS + top 5 Clifton + inne sygnały, pokazuje userowi propozycję interpretacji i prosi o potwierdzenie. Nie wstawia nic do `me.md` bez zgody usera.

**Ścieżka z PDF** (jeśli `$MA_PROFILE_PDF = tak`):

### C1 - PDF FRIS

**Pytanie:** Upload PDF z wynikami FRIS. AI przeczyta i pokaże propozycję interpretacji.
**Typ odpowiedzi:** ścieżka (upload)
**Generuje:** po potwierdzeniu interpretacji przez usera - tworzy w me.md sekcję `## Profil psychologiczny - FRIS` z podsumowaniem: styl myślenia, styl działania, aktywne/nieaktywne postawy. Zapisuje też sygnały do bufora, żeby Sekcja F mogła je wykorzystać jako default propozycje hard rules.
**Uwagi dla AI:** FRIS to polski test (badacz/partner/zawodnik/wizjoner + 4 perspektywy). Wyciągnij dominujący styl myślenia, styl działania, aktywne/nieaktywne postawy. Pokaż userowi "Wygląda na: Badacz / Indywidualista / aktywne DECYDUJĘ, ZMIENIAM, ROZWAŻAM - zgadza się?". Kalibracja Sekcji F po potwierdzeniu.

### C2 - PDF Gallup Clifton Strengths

**Pytanie:** Upload PDF z wynikami Gallup Clifton Strengths. AI wyciągnie top 5.
**Typ odpowiedzi:** ścieżka (upload)
**Generuje:** po potwierdzeniu - dopisuje do `## Profil psychologiczny` podsekcję `### CliftonStrengths Top 5` z listą talentów i ich domeną (Executing / Influencing / Relationship Building / Strategic Thinking). Zapisuje sygnały do bufora dla Sekcji F.
**Uwagi dla AI:** Clifton ma wersje "top 5", "top 10", "top 34". Pokaż userowi top 5 (jeśli dostępne) + domenę każdej. Poproś o potwierdzenie.

### C3 - Inne testy

**Pytanie:** Masz inne testy / profile, które uważasz za istotne? (Enneagram, MBTI, DISC, Big Five...)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Profil psychologiczny` podsekcję `### Inne profile` z wolnym tekstem usera. Brak automatycznego parsowania - treść zostaje jak podał user.

### C4 - Autoopis

**Pytanie:** Wolny tekst - 2-3 zdania o tym jak chcesz żeby AI się do ciebie odnosił.
**Typ odpowiedzi:** wolny tekst
**Generuje:** zapisuje do bufora jako `$autoopis`. Używany w Sekcji F jako hint przy propozycjach hard rules (np. jeśli user napisał "nie owijaj" - F4 default = "wysoka tolerancja krytyki"). Do me.md nie trafia dosłownie, ale AI-wykonawca może zacytować fragment w `## Hard rules` jeśli user potwierdzi ("Hard rule: nie owijaj, idź do sedna.").

### C5 - Tematy tabu profilu

**Pytanie:** Są cechy / wzorce, o których AI **nie powinien wspominać** nawet gdyby je zobaczył? (Prywatność / świadoma zmiana / terapia w toku.)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Hard rules` w me.md zdanie: "Nie wspominaj o: $tematy." (lista z wolnego tekstu usera, oddzielona przecinkami). To jest hard opt-out.

**Uzupełnienie hybrydowe** (tylko jeśli `$MA_PROFILE_PDF = tak`): PDF daje typologię (FRIS / Clifton), ale nie zawsze oddaje praktyczne preferencje pracy. Dwa krótkie pytania domykają sygnał. Pomijamy C2' (format - dubluje F9) i C4' (autoopis - mamy C4).

### C6 - Tempo decyzji (uzupełniające)

**Pytanie:** Niezależnie od profilu - w jakim tempie przetwarzasz decyzje w praktyce?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. szybko, 2. wolno, 3. zależy od kontekstu
**Warunkowe:** tylko jeśli `$MA_PROFILE_PDF = tak` (ścieżka bez PDF ma to samo w C1').
**Generuje:** zapisuje `$tempo` do bufora. Hint dla F2 (zwięzłość) i F8 (proaktywność). Dopisuje do `## Styl pracy` w me.md: "Tempo decyzji: $tempo."
**Uwagi dla AI:** nie kalibruj przez profil z PDF - pytaj wprost, bo ludzie często działają inaczej niż typ sugeruje.

### C7 - Reakcja na krytykę (uzupełniające)

**Pytanie:** Jak w praktyce reagujesz na bezpośrednią krytykę / konfrontację?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. lubię, 2. toleruję, 3. wolę unikać
**Warunkowe:** tylko jeśli `$MA_PROFILE_PDF = tak` (ścieżka bez PDF ma to samo w C3').
**Generuje:** zapisuje `$krytyka` do bufora. Hint dla F3 (spór vs współpraca) i F4 (tolerancja krytyki). Dopisuje do `## Styl pracy`: "Reakcja na krytykę: $krytyka."

**Ścieżka bez PDF** (jeśli `$MA_PROFILE_PDF = nie`):

### C1' - Tempo decyzji

**Pytanie:** W jakim tempie przetwarzasz decyzje?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. szybko, 2. wolno, 3. zależy od kontekstu
**Generuje:** zapisuje do bufora jako `$tempo`. Używane w Sekcji F jako hint dla F2 (zwięzłość vs pełny obraz) i F8 (proaktywność). Dopisuje też do me.md w sekcji `## Styl pracy` linię: "Tempo decyzji: $tempo."

### C2' - Format informacji

**Pytanie:** Lepiej odbierasz informacje jako:
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. bullety i liczby, 2. prose i kontekst, 3. jedno i drugie
**Generuje:** zapisuje `$format_preferred` do bufora. Hint dla F9 (format odpowiedzi AI). Dopisuje do `## Styl pracy`: "Preferowany format informacji: $format."

### C3' - Reakcja na krytykę

**Pytanie:** Jak reagujesz na krytykę / konfrontację?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. lubię, 2. toleruję, 3. wolę unikać
**Generuje:** zapisuje `$krytyka` do bufora. Hint dla F3 (spór vs współpraca) i F4 (tolerancja krytyki). Dopisuje do `## Styl pracy`: "Reakcja na krytykę: $krytyka."

### C4' - Autoopis

**Pytanie:** Wolny tekst - 2-3 zdania o tym jak chcesz żeby AI się do ciebie odnosił.
**Typ odpowiedzi:** wolny tekst
**Generuje:** jak C4 (zapisuje do bufora jako `$autoopis`, używany w Sekcji F).

---

## Sekcja D - Projekty i obszary (5 pytań)

**Cel sekcji:** wygenerować kategorie w `Projekty/`. Nie konkretne projekty - tylko kategorie.

**Mechanika archetypów (decyzja 2026-04-21):** po D1-D5 skill pokazuje 1-2 pasujące archetypy z `docs/przyklady/` (marketing manager / developer / student programowania) jako inspirację - "oto jak wygląda vault marketing managera o podobnym profilu". User może z nich korzystać albo nie.

### D1 - Obszary

**Pytanie:** Wymień 3-7 głównych obszarów twojej pracy / życia, które chciałbyś mieć w vaulcie. (Np. "Marketing klient A", "Marketing klient B", "Rozwój osobisty", "Nauka programowania".)
**Typ odpowiedzi:** lista (3-7 elementów)
**Generuje:** dla każdego `$obszar` - utwórz `Projekty/$obszar/` z pustym `index.md` ("Kategoria: $obszar. Brak aktywnych projektów - dodaj przez `/aios:stworz-projekt`."). Dopisz wiersz w tabeli "Aktywne projekty" w `me.md` (pusty status).
**Uwagi dla AI:** nazwy obszarów bez polskich znaków diakrytycznych w ścieżkach folderów (ale tytuł w `index.md` z diakrytykami OK).

### D2 - Opisy obszarów

**Pytanie:** Dla każdego obszaru - jedno zdanie, czego dotyczy.
**Typ odpowiedzi:** słownik ($obszar -> $opis)
**Generuje:** dopisuje `$opis` pod tytułem `# $obszar` w `Projekty/$obszar/index.md` (jako lead paragraph). Jeśli user pominął dla jakiegoś obszaru - zostaw bez opisu, user uzupełni ręcznie.

### D3 - Najaktywniejszy

**Pytanie:** Który z tych obszarów jest NAJAKTYWNIEJSZY teraz?
**Typ odpowiedzi:** wybór z listy (z D1)
**Generuje:** w `vault-map.md` oznacza ten obszar gwiazdką / prefixem "(aktywny)". W tabeli "Aktywne projekty" w `me.md` - ten obszar idzie na górę.

### D4 - Lista zewnętrzna

**Pytanie:** Masz już gdzieś listę aktywnych konkretnych projektów (Notion, Trello, Asana, kartka)? Możesz mi wkleić, zaproponuję kilka pustych projektów do kategorii.
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli user wkleił listę - AI proponuje utworzenie `Projekty/<kategoria>/<nazwa_projektu>/` dla każdego. Nie tworzy od razu - pokazuje propozycję, czeka na "tak/nie" per projekt. Po akceptacji wywołuje logikę analogiczną do `/aios:stworz-projekt` (README.md, aktywne.md, decyzje.md). Jeśli puste - pomija, user uruchomi `/aios:stworz-projekt` sam później.

### D5 - Obszary wykluczone

**Pytanie:** Czy są obszary których świadomie **nie** chcesz w tym vaulcie? (Np. finanse są w YNAB, nie chcesz ich tu.)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Hard rules` w me.md zdanie: "Nie prowadź w vault: $wykluczone." (żeby AI nie proponował tych obszarów przy `/aios:stworz-projekt`). Jeśli puste - pomija.

---

## Sekcja E - Stos technologiczny (8 pytań)

**Cel sekcji:** ustalić środowisko pracy + decyzja o Pinecone.

### E1 - OS

**Pytanie:** Na jakim systemie pracujesz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. macOS, 2. Linux, 3. Windows, 4. inne
**Generuje:** dopisuje do sekcji `## Stack` w me.md linię: "OS: $os." Używane przez pozostałe skille do kalibracji ścieżek (np. `~/.claude/` na macOS vs `%APPDATA%\Claude\` na Windows).

### E2 - Edytor plików

**Pytanie:** W jakim edytorze będziesz głównie pracować z plikami vaulta?
**Typ odpowiedzi:** wybór z listy + "inny"
**Warianty:** 1. Obsidian, 2. Logseq, 3. VS Code, 4. zwykły edytor tekstu, 5. inny
**Generuje:** dopisuje do `## Stack`: "Edytor: $edytor." Jeśli Obsidian - w FIN3 `vault-map.md` używa wiki-linków (`[[nazwa]]`) zamiast ścieżek; jeśli VS Code / inne - standardowe linki markdown.

### E3 - Synchronizacja

**Pytanie:** Jak synchronizujesz pliki między urządzeniami?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. iCloud, 2. Google Drive, 3. Dropbox, 4. własny serwer, 5. brak
**Generuje:** dopisuje do `## Stack`: "Synchronizacja: $sync." Jeśli 1-3 - używane jako default w J3 (potwierdzenie backupu). Jeśli 4 lub 5 - zostaje jak podał user.

### E4 - Główny AI

**Pytanie:** Który AI będzie głównie pracował z vaultem? (Wiemy z INSTALL-u, ale upewniam się.)
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. Claude Code, 2. Claude Desktop (Cowork), 3. Cursor, 4. inne
**Generuje:** dopisuje do `## Stack`: "Główny AI: $ai." Używane przez pozostałe skille (np. `/aios:koniec-sesji` dostosowuje format logów do tego AI).

### E5 - Pinecone

**Pytanie:** Pinecone jako baza wektorowa dla semantic search w vaulcie?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak (skonfigurujemy teraz), 2. nie (zostaje hierarchiczny search po index.md), 3. zdecyduję później
**Default:** zdecyduję później
**Generuje:** jeśli 1 - aktywuje krok FIN4 (setup Pinecone); jeśli 3 - dopisuje w me.md Stack "Pinecone: planowany do konfiguracji"; jeśli 2 - pomija Pinecone w me.md.
**Uwagi dla AI:** nie blokuj onboardingu na tym. Default "zdecyduję później" bezpieczny.

### E6 - Konto Pinecone

**Pytanie:** Masz już konto na pinecone.io?
**Typ odpowiedzi:** tak/nie
**Warunkowe:** tylko jeśli E5 = tak
**Generuje:** zapisuje `$ma_pinecone_konto` do bufora. Jeśli nie - w kroku FIN4 AI pokaże pełną ścieżkę (rejestracja, index, API key). Jeśli tak - tylko "wygeneruj API key i skopiuj".
**Uwagi dla AI:** jeśli nie - w kroku FIN4 AI pokaże jak założyć konto (kroki: rejestracja, utwórz index, skopiuj API key).

### E7 - Git

**Pytanie:** Czy zamierzasz trzymać vault pod gitem?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak, 2. nie, 3. jeszcze nie wiem
**Default:** nie
**Generuje:** zapisuje `$git_choice` do bufora. Jeśli 1 - w FIN3 tworzy `.gitignore` z `_pamiec/onboarding-progress.md`, `_brudnopis/`, i (jeśli H3=tak) `Prywatne/`. Inicjuje `git init` w FIN2 (za zgodą J2). Dopisuje do `## Stack`: "Git: $git_choice."

### E8 - Inne narzędzia

**Pytanie:** Inne narzędzia, które twój AI powinien znać, że masz? (Np. Linear, Slack, Notion, Figma, GA, GSC...)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Stack` listę: "Inne narzędzia w kontekście pracy: $lista." Lista słownie, nie tabela (bo user wpisał wolnym tekstem).

---

## Sekcja F - Preferencje komunikacyjne (10 pytań)

**Cel sekcji:** wygenerować **własne hard rules** dla tego usera, miksując elementy z `docs/szablony/style-komunikacji/`. To jest KLUCZOWE - każdy user generuje własny, spersonalizowany zestaw reguł, nie dziedziczy cudzych.

**Nota dla AI-wykonawcy:** każdy user generuje własne preferencje. Skill NIE narzuca frameworków Paul-Elder / Rapoport / steelmanowania - to są opcjonalne soczewki, nie domyślne.

Każde pytanie wybiera jedną z 2-3 osiowych preferencji. AI tłumaczy wybór na zdanie w `hard rules` (pełna tabela na końcu pliku w sekcji **Mapowanie F1-F10 → hard rules**).

### F1 - Konkret vs kontekst

**Pytanie:** Wolisz konkret na początku odpowiedzi, czy kontekst wprowadzający?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. konkret na początku (bez wstępu), 2. kontekst najpierw (żeby zrozumieć), 3. zależy od tematu
**Szablon:** `szablony/style-komunikacji/konkret-vs-kontekst.md`
**Generuje:** hard rule w me.md (patrz tabela mapowania). Jeśli 1 - "Konkrety na początku. Bez wstępów typu 'oczywiście, chętnie pomogę'." Jeśli 2 - "Zacznij od kontekstu - co się dzieje, czego dotyczy, a potem konkret." Jeśli 3 - pomiń hard rule, dopisuj kontekstowo w zależności od pytania.
**Uwagi dla AI:** to najważniejsza oś dla F. Nie proponuj defaultu - user sam wybiera.

### F2 - Zwięzłość vs pełny obraz

**Pytanie:** Na pytania decyzyjne - wolisz jedną rekomendację, czy pełny obraz opcji?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. jedna rekomendacja (szybko zdecyduję), 2. pełny obraz 2-4 opcji (sam wybiorę), 3. zależy
**Szablon:** `szablony/style-komunikacji/zwiezlosc-vs-pelny-obraz.md`
**Generuje:** hard rule (patrz tabela). Dodatkowo zapisuje `$F2` do bufora - używane przez inne skille (np. `/aios:stworz-projekt` przy decyzji o strukturze).

### F3 - Spór vs współpraca

**Pytanie:** Gdy twierdzę coś dyskusyjnego - chcesz żeby AI sparował czy raczej się dostosował?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. sparuj uczciwie (debata merytoryczna), 2. dostosuj się (nie wiem jeszcze czego chcę), 3. zależy - pytaj
**Szablon:** `szablony/style-komunikacji/spor-vs-wspolpraca.md`
**Generuje:** hard rule (patrz tabela).

### F4 - Tolerancja krytyki

**Pytanie:** Jak wysoką tolerancję masz na bezpośrednią krytykę swoich pomysłów?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. wysoka (bezpośrednio, nie owijaj), 2. średnia (krytyka z uzasadnieniem), 3. niska (delikatnie, z afirmacją wpierw)
**Szablon:** `szablony/style-komunikacji/tolerancja-krytyki.md`
**Generuje:** hard rule (patrz tabela).

### F5 - Emoji

**Pytanie:** Emoji w odpowiedziach AI?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak, swobodnie, 2. tylko funkcjonalne (✓ ✗ ⚠), 3. nie, nigdy
**Default:** 2
**Generuje:** hard rule (patrz tabela). W przypadku 3 dopisuje też: "Nie używaj emoji - nawet funkcjonalnych."

### F6 - Humor

**Pytanie:** Humor w rozmowie z AI?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. lubię, 2. neutralnie, 3. wolę serio
**Generuje:** hard rule tylko jeśli 1 ("Możesz dodać humor - ironię, lekkość, żart w tym miejscu") albo 3 ("Trzymaj ton rzeczowy, bez humoru"). Jeśli 2 - nie dopisuje (default "jak wyjdzie").

### F7 - Cytowanie profilu

**Pytanie:** Czy AI może odnosić się do twojego profilu zwrotnie? (Np. "wiem, że jesteś X, więc zaproponuję Y.")
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak (lubię tę kalibrację), 2. nie (używaj profilu do kalibracji, ale nie cytuj)
**Default:** 2
**Generuje:** hard rule (patrz tabela). Dla 2 - przykładowe zdanie: "Nie cytuj mi mojego profilu z powrotem. Używaj go do kalibracji stylu, nie do powtarzania 'wiem że jesteś X'."
**Uwagi dla AI:** default "nie" bywa często preferowany, ale nie narzucamy - user wybiera sam.

### F8 - Proaktywność

**Pytanie:** Chcesz żeby AI sugerował kolejne kroki po każdym zadaniu?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak (proponuj co dalej), 2. nie (odpowiadaj tylko na pytania), 3. tylko gdy zapytam
**Generuje:** hard rule (patrz tabela).

### F9 - Format odpowiedzi

**Pytanie:** Preferowany format odpowiedzi AI?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. listy i bullety, 2. prose i akapity, 3. tabele, 4. mieszanie (zależy od treści)
**Default:** 4
**Generuje:** hard rule (patrz tabela). Dla 4 - brak hard rule, AI decyduje kontekstowo.

### F10 - Wolny tekst

**Pytanie:** Jest coś, co AI ma **zawsze** robić albo **nigdy**, a nie wychwyciły tego F1-F9?
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - AI formułuje z tego 1-3 hard rules w trybie rozkazującym i pokazuje userowi do akceptacji przed wklejeniem do me.md. Np. user pisze "nigdy nie używaj myślnika —" - AI proponuje hard rule "Myślniki: tylko `-`, nigdy `—` ani `–`."
**Uwagi dla AI:** to "escape hatch" - user może tu wpisać specyficzną preferencję, np. "nigdy nie używaj myślnika —, tylko -".

---

## Sekcja G - Rytm i nawyki (4 pytania)

**Cel sekcji:** zrozumieć jak user pracuje czasowo - generuje strukturę `Kalendarz/` i propozycje rytuałów.

### G1 - Godziny pracy

**Pytanie:** W jakich godzinach najczęściej pracujesz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. poranek, 2. popołudnie, 3. wieczór, 4. różnie w ciągu dnia
**Generuje:** dopisuje do sekcji `## Rytm pracy` w me.md: "Główne godziny pracy: $okres." Jeśli G3 generuje rytuał - osadzenie rytuału uwzględnia ten okres (np. "daily review rano przed pracą" albo "na koniec dnia").

### G2 - Częstotliwość

**Pytanie:** Jak często otwierasz vault?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. codziennie, 2. kilka razy w tygodniu, 3. sporadycznie
**Generuje:** dopisuje do `## Rytm pracy`: "Częstotliwość vault: $czestotliwosc." Hint dla G3 - jeśli "sporadycznie", zaproponuj tylko weekly review, nie daily. Używane też przez `/aios:szukaj` do kalibracji (gdzie szukać najpierw - świeże vs archiwum).

### G3 - Rytuały

**Pytanie:** Chcesz rytuał daily review / weekly review?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. daily, 2. weekly, 3. oba, 4. żaden
**Generuje:** w FIN2 tworzy `Kalendarz/` + odpowiednie pliki: `Kalendarz/daily-review-template.md` (jeśli 1 lub 3), `Kalendarz/weekly-review-template.md` (jeśli 2 lub 3). Każdy template zawiera 3-5 pytań prowokujących (np. "Co dziś osiągnąłem?", "Co utknęło?"). Jeśli 4 - nie tworzy `Kalendarz/` w ogóle.

### G4 - /aios:koniec-sesji

**Pytanie:** Chcesz, żeby AI proponował `/aios:koniec-sesji` po każdej sesji roboczej?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. tak, 2. nie, 3. czasem (gdy sesja była istotna)
**Generuje:** dopisuje do `## Rytm pracy`: "`/aios:koniec-sesji` proponowany: $tryb." Używane przez wszystkie skille jako sygnał - czy AI ma proponować zamknięcie sesji. Dla 1 - zawsze po 3+ tool calls, dla 2 - nigdy bez prośby usera, dla 3 - AI sam ocenia "istotność" (heurystyka: 5+ plików zmienionych lub 30+ min aktywności).

---

## Sekcja H - Prywatne (6 pytań, warunkowe)

**Warunkowe:** tylko jeśli B1 = prywatne albo B1 = hybryda. Inaczej pomijamy cała sekcję.

**Cel sekcji:** ustalić strefy prywatne w vaulcie (osobne reguły cytowania / anonimizacji / poziomu otwartości).

### H1 - Tematy bez proaktywności

**Pytanie:** Masz tematy, o których chcesz pisać w vaulcie, ale AI NIE powinien cię pytać sam z siebie? (Terapia, relacje, zdrowie, finanse osobiste.)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Hard rules` w me.md: "Nie pytaj proaktywnie o: $tematy." (user musi sam zacząć wątek, AI reaguje tylko gdy user pierwszy go porusza). To jest soft opt-out (w odróżnieniu od C5 który jest hard).

### H2 - Imiona osób trzecich

**Pytanie:** Czy osoby trzecie (partner / dzieci / przyjaciele) mogą pojawiać się w notatkach imiennie czy wolisz inicjały / pseudonimy?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. imiennie, 2. inicjały, 3. pseudonimy
**Generuje:** dopisuje do sekcji `## Prywatność` w me.md: "Osoby trzecie w notatkach: $tryb." Jeśli 2 lub 3 - dodaje hard rule "Przy cytowaniu notatek zawierających osoby trzecie - używaj $trybu (np. 'A.' zamiast 'Agnieszka')."

### H3 - Osobny folder prywatne

**Pytanie:** Chcesz osobny folder `Prywatne/` wyłączony z git / synchronizacji?
**Typ odpowiedzi:** tak/nie
**Default:** tak jeśli E7 = tak, inaczej nie
**Generuje:** jeśli tak - w FIN2 tworzy `Prywatne/` z pustym `index.md`. Jeśli E7=tak - dopisuje `Prywatne/` do `.gitignore`. Dopisuje do `## Prywatność`: "Folder `Prywatne/` istnieje i jest poza gitem." Prywatne projekty z D idą tutaj, a nie pod `Projekty/`.

### H4 - Styl AI w prywatnym

**Pytanie:** W prywatnej części vaulta chcesz inny styl AI? (Np. mniej formalny, więcej miejsca na emocje.)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Prywatność` sekcję `### Styl AI w prywatnym` z wolnym tekstem. Pozostałe skille (np. `/aios:stworz-projekt` w obrębie `Prywatne/`) czytają tę sekcję jako override stylu ustalonego w F.

### H5 - Proaktywność prywatna

**Pytanie:** Czy AI ma proaktywnie wchodzić w prywatne tematy (proponować rytuały, check-iny, refleksje) czy tylko gdy sam zaczniesz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. proaktywnie, 2. tylko gdy sam zacznę
**Default:** 2
**Generuje:** dopisuje do `## Prywatność`: "Proaktywność w prywatnym: $tryb." Dla 2 - dodaje hard rule "W obrębie `Prywatne/` - nie inicjuj wątków, czekaj na usera."

### H6 - Tabu w prywatnym

**Pytanie:** Jest coś, co AI ma **zawsze** pomijać nawet, gdybyś sam o to zagadnął? (Świadome granice - np. "nie komentuj zdrowia".)
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - dopisuje do `## Hard rules` (nie do Prywatność, bo to obowiązuje globalnie): "Nigdy nie komentuj: $tabu. Nawet gdy sam o to zagadnę." To jest twardy opt-out (analogicznie do C5).

---

## Sekcja I - Materiały do zassania (4 pytania)

**Cel sekcji:** dać userowi szybki start z realną Wiedzą, nie pustym folderem.

### I1 - Profile publiczne

**Pytanie:** Masz publiczne profile / strony, które mam wciągnąć na start? (LinkedIn, WWW, blog, portfolio.)
**Typ odpowiedzi:** lista URL-i (opcjonalne)
**Generuje:** zapisuje listę do bufora jako `$url_publiczne`. W FIN5 raportuje: "Masz $N publicznych profili do wciągnięcia. Użyj `/aios:dodaj-do-wiki` - pokażę ci jak." Nie tworzy w FIN automatycznych zadań (bo to może być długie) - zostawia userowi.

### I2 - PDF-y / artykuły

**Pytanie:** Masz ulubione PDF-y / artykuły / książki w wersji tekstowej, które chcesz mieć w `Wiedza/Raw/`? Max 5 na start.
**Typ odpowiedzi:** lista ścieżek / URL-i (opcjonalne)
**Generuje:** jeśli lista ścieżek lokalnych - w FIN2 kopiuje pliki do `Wiedza/Raw/`. Jeśli URL-e - zapisuje do bufora, w FIN5 zaproponuje `/aios:dodaj-do-wiki` na nich. Max 5 - jeśli user podał więcej, bierze pierwsze 5 i mówi "resztę dodasz sam".

### I3 - Transkrypty

**Pytanie:** Masz transkrypty szkoleń / kursów / rozmów, które chcesz zamienić w wiki? Max 3.
**Typ odpowiedzi:** lista ścieżek (opcjonalne)
**Generuje:** jeśli podane - w FIN2 kopiuje do `Wiedza/Raw/transkrypty/`. W FIN5 proponuje `/aios:dodaj-do-wiki` na nich (priorytet, bo transkrypty zwykle są najbardziej wartościowe po przerobieniu).

### I4 - Propozycja /aios:dodaj-do-wiki

**Pytanie:** Czy AI ma zaproponować `/aios:dodaj-do-wiki` na pierwszych materiałach zaraz po finalizacji?
**Typ odpowiedzi:** tak/nie
**Default:** tak (jeśli I1-I3 > 0)
**Generuje:** zapisuje `$propose_wiki_ingest` do bufora. Jeśli tak - w FIN5 raport ma zdanie: "Chcesz żebym od razu uruchomił `/aios:dodaj-do-wiki` na pierwszym materiale z $I2/$I3?". Jeśli nie - user sam uruchomi później.

---

## Sekcja J - Finalizacja (5 pytań)

**Cel sekcji:** ostatnie potwierdzenia przed generowaniem plików.

### J1 - Ścieżka vaulta

**Pytanie:** Vault będzie tutaj: `$VAULT_PATH` (wczytane z INSTALL-u). OK?
**Typ odpowiedzi:** tak/nie (jeśli nie - zapytaj o nową ścieżkę)
**Generuje:** zapisuje finalny `$VAULT_PATH` do bufora. Wszystkie kroki FIN1-FIN5 używają tej ścieżki jako root. Jeśli user zmienił - AI przerwie przed FIN2 i pokaże "Tworzę vault w: $nowa_sciezka. Kontynuować?" (dodatkowe potwierdzenie, bo to destrukcyjne).

### J2 - Potwierdzenie git (DRY z E7)

**Pytanie:** W E7 wybrałeś `$E7` dla gita. Potwierdzamy, czy zmieniasz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. potwierdź (tak wg E7), 2. zmień (wpisz nową wartość)
**Generuje:** potwierdza lub aktualizuje `$git_choice` z E7. Jeśli potwierdzone - w FIN2 działa wg E7 (git init jeśli tak). Jeśli zmienione - nadpisuje i informuje: "Zmieniam decyzję git z '$E7' na '$J2'."
**Uwagi dla AI:** nie pytaj drugi raz o `git init` - tylko potwierdź decyzję z E7. Jeśli user zmienił zdanie, nadpisz `$git_choice`.

### J3 - Potwierdzenie backupu (DRY z E3)

**Pytanie:** W E3 wybrałeś `$E3` dla synchronizacji/backupu. Potwierdzamy, czy zmieniasz?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. potwierdź (tak wg E3), 2. zmień
**Generuje:** potwierdza lub aktualizuje `$sync_choice` z E3. Wpływa na zalecenia w FIN5 ("Pamiętaj: vault jest synchronizowany przez $sync - sprawdź, że `.gitignore` nie koliduje z folderami sync").
**Uwagi dla AI:** analogicznie do J2 - tylko potwierdzenie, nie ponowne pytanie.

### J4 - Podgląd me.md

**Pytanie:** Po wygenerowaniu chcesz od razu zobaczyć finalny `me.md` do przejrzenia, czy zaufasz i sprawdzisz sam później?
**Typ odpowiedzi:** wybór z listy
**Warianty:** 1. pokaż od razu, 2. zaufaj, sprawdzę sam
**Default:** 1 (bezpieczniejsze w MVP)
**Generuje:** jeśli 1 - w FIN5 AI otwiera `me.md` (przez link `computer://`) i czeka na reakcję usera przed raportem końcowym. Jeśli 2 - FIN5 od razu raport końcowy, user sam otwiera plik później.

### J5 - Ostatnie słowo

**Pytanie:** Ostatnia okazja - jest coś, co chciałeś powiedzieć / dodać, a nie zapytałem?
**Typ odpowiedzi:** wolny tekst (opcjonalne)
**Generuje:** jeśli wypełnione - AI ocenia czy to: (a) nowa hard rule - dopisuje do F10, (b) info o stacku - dopisuje do E8, (c) dziennikowe "ważne dla mnie" - dopisuje na końcu `## Kim jestem` jako "Dodatkowe notki" lub (d) nie pasuje nigdzie - zapisuje w bufor do `_brudnopis/onboarding-notes-$DATA.md`. W każdym przypadku pokazuje userowi gdzie umieścił.

---

## Mapowanie F1-F10 → hard rules

Tabela pokazuje dokładne zdanie, które trafia do `## Hard rules` w me.md dla każdej kombinacji F1-F10. AI-wykonawca używa tego jako look-up po Sekcji F.

**Reguła porządku:** hard rules w me.md są numerowane w kolejności przedstawionej poniżej (najpierw F1, potem F2, itd.). F10 zawsze na końcu. Tematy tabu z C5, H1, H6 idą do osobnej podsekcji "Tematy i granice" pod hard rules.

### F1 - Konkret vs kontekst

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (konkret) | "Konkrety na początku. Bez wstępów typu 'oczywiście, chętnie pomogę'." |
| 2 (kontekst) | "Zacznij od krótkiego kontekstu - co się dzieje, czego dotyczy - a potem konkret." |
| 3 (zależy) | (pomiń - nie ma hard rule, AI decyduje kontekstowo) |

### F2 - Zwięzłość vs pełny obraz

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (jedna rekomendacja) | "Przy pytaniu o decyzję - jedna rekomendacja wprost. Nie pokazuj wszystkich opcji jeśli nie poproszę." |
| 2 (pełny obraz) | "Pełny obraz opcji kiedy pytam o decyzję - nie jedna rekomendacja bez alternatyw." |
| 3 (zależy) | (pomiń) |

### F3 - Spór vs współpraca

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (spór) | "Gdy twierdzę coś dyskusyjnego - sparuj uczciwie. Przedstaw kontrargumenty, nawet jeśli to niekomfortowe." |
| 2 (współpraca) | "Gdy twierdzę coś - idź za moją linią myślenia. Nie spieraj się sam z siebie." |
| 3 (zależy) | "Gdy twierdzę coś dyskusyjnego - zapytaj, czy chcę sparować czy kontynuować." |

### F4 - Tolerancja krytyki

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (wysoka) | "Krytykuj bezpośrednio. Bez afirmacji wstępnych, bez owijania w bawełnę." |
| 2 (średnia) | "Krytyka z uzasadnieniem - co jest źle i dlaczego, nie samo 'to nie działa'." |
| 3 (niska) | "Krytykę podawaj delikatnie. Zacznij od tego co działa, potem co można poprawić." |

### F5 - Emoji

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (swobodnie) | (pomiń - brak hard rule, user nie ma preferencji ograniczającej) |
| 2 (funkcjonalne) | "Emoji tylko funkcjonalne: ✓ ✗ ⚠ - nie dekoracyjne." |
| 3 (nigdy) | "Nie używaj emoji - nawet funkcjonalnych." |

### F6 - Humor

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (lubię) | "Możesz dodać humor - ironię, lekkość, żart. Nie forsuj, ale jak wychodzi - zostaw." |
| 2 (neutralnie) | (pomiń) |
| 3 (serio) | "Trzymaj ton rzeczowy, bez humoru." |

### F7 - Cytowanie profilu

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (tak) | "Możesz odnosić się do mojego profilu - 'wiem że lubisz X' to OK." |
| 2 (nie) | "Nie cytuj mi mojego profilu z powrotem. Używaj go do kalibracji stylu, nie do powtarzania 'wiem że jesteś X'." |

### F8 - Proaktywność

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (proponuj) | "Po każdym zadaniu - zaproponuj 1-3 naturalne kolejne kroki." |
| 2 (tylko odpowiedzi) | "Odpowiadaj tylko na moje pytania. Nie proponuj następnych kroków z siebie." |
| 3 (gdy zapytam) | (pomiń - default behavior, brak hard rule) |

### F9 - Format odpowiedzi

| Odpowiedź | Hard rule |
|-----------|-----------|
| 1 (listy) | "Odpowiadaj bulletami i listami, gdy to sensowne. Unikaj długich akapitów." |
| 2 (prose) | "Odpowiadaj pełnymi zdaniami i akapitami. Unikaj list-dla-listy." |
| 3 (tabele) | "Gdy porównujesz opcje lub dane - użyj tabeli markdown." |
| 4 (mieszanie) | (pomiń) |

### F10 - Wolny tekst

Nie ma tabeli - AI formułuje 1-3 hard rules z wolnego tekstu usera, pokazuje propozycję, czeka na akceptację, wkleja zaakceptowane do me.md.

**Przykład:** user wpisuje "zawsze pytaj o strefę czasową gdy ustalamy spotkanie" → AI proponuje hard rule "Przy ustalaniu spotkań - zawsze pytaj o strefę czasową drugiej strony."

---

## Podsumowanie struktury

- **Razem:** 57 pytań (+ 3 meta-pytania w Kroku 0). Wzrost z 55 po dodaniu C6/C7 (hybryda light - decyzja 2026-04-22).
- **Obligatoryjne sekcje:** A, B, D, E, F, G, I, J (44 pytania obligatoryjne).
- **Warunkowe / opcjonalne:**
  - C ścieżka z PDF (5 pytań C1-C5 + 2 uzupełniające C6-C7), zależne od `$MA_PROFILE_PDF = tak`.
  - C ścieżka bez PDF (4 pytania C1'-C4'), zależne od `$MA_PROFILE_PDF = nie`.
  - H (6 pytań, zależne od B1 = prywatne / hybryda).
  - Niektóre pytania warunkowe wewnątrz sekcji (np. B2 zależne od B1 = hybryda, E6 zależne od E5 = tak).
- **Tryby czasowe:**
  - Szybki (30 min): pomija C, pomija I (poza I4=nie), skraca J do potwierdzenia defaultów → ~32 pytania.
  - Standard (45 min): pełne A-G, I, J, H jeśli warunek spełniony → 44-52 pytań.
  - Pełny (60 min): wszystkie 57 pytań + upload PDF w C → 57.

## Status

Szkielet v0.2.2 - wszystkie pola `Generuje:` wypełnione (57/57 po dodaniu C6/C7), tabela mapowania F→hard rules kompletna. **Wypełnienia jeszcze wymagają:**

1. Biblioteka plików `szablony/style-komunikacji/*.md` - 5-8 plików. `konkret-vs-kontekst.md` (F1) gotowy 2026-04-22 jako wzorzec. Pozostałe F2-F9 do napisania.
2. Dokładnych instrukcji parsowania PDF FRIS / Clifton w Sekcji C (decyzja 2026-04-21: multimodal + potwierdzenie) - szczegóły w `init-SKILL-v02.md`, ale warto dopisać przykłady sygnałów w osobnym pliku `docs/parsowanie-pdf.md`.
3. Szablon `szablony/me-template.md` - gotowy 2026-04-22 (v0.1).
4. 3 archetypy w `docs/przyklady/` (marketing manager, developer, student programowania) - pełne me.md + struktura `Projekty/` jako demo.
