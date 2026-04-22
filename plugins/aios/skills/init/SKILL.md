---
name: init
description: Onboarding do AIOS-Klaudynki - prowadzi usera przez 57 pytan w 10 sekcjach (A-J) + FIN, generuje me.md, dostosowuje strukture vaulta, opcjonalnie konfiguruje Pinecone. Triggery - "/aios:init", "uruchom onboarding", "wygeneruj me.md", "skonfiguruj AIOS", "zacznij konfiguracje AIOS".
---

# init

Skill onboardingowy AIOS-Klaudynki. Wywolywany raz, po instalacji plugina. Na wyjsciu: gotowy `me.md`, dostosowana struktura `Projekty/`, opcjonalnie skonfigurowany Pinecone, wypelniony `vault-map.md`.

Pelna lista 57 pytan z kompletnymi opcjami i logika warunkowa znajduje sie w `pytania.md` (obok tego pliku).

---

## Zasady dla AI-wykonawcy

1. **Komunikacja po polsku.** Wszystkie pytania, komentarze, raporty.
2. **Tylko lacznik `-`.** Nigdy `—` ani `–` w pytaniach ani generowanych plikach.
3. **Tryb domyslny: batch po sekcji.** Pokazuj 5-10 pytan z danej sekcji na raz, user odpowiada numerkami / skrotami / wolnym tekstem. Nie pytaj-po-pytaniu, chyba ze user poprosi.
4. **Fallback: pytanie-po-pytaniu.** Jesli user w dowolnym momencie mowi "wolniej" / "po jednym" / "rozbij to" - przelacz na tryb pojedynczych pytan do konca sesji.
5. **Zapisuj stan.** Po kazdej ukonczonej sekcji zapisz odpowiedzi do `_pamiec/onboarding-progress.md` (patrz **Obsluga przerw**).
6. **Oddawaj kontrole gdy trzeba.** Rejestracja Pinecone, instalacja MCP, zgoda na utworzenie folderow - to decyzje usera. Nie podejmuj ich za niego.
7. **Nie narzucaj swoich ram.** Paul-Elder, Rapoport, FRIS, Clifton - to *opcjonalne* soczewki. Jesli user ich nie zna, nie wciskaj. Profil psychologiczny jest opcjonalny (Sekcja C).

---

## Krok 0 - Kalibracja wstepna

Zanim ruszysz z sekcja A, zadaj userowi 3 meta-pytania:

1. **Ile masz dzis czasu?** - 30 min (szybki tryb, pomijamy opcjonalne), 45 min (standard), 60+ min (pelny, z PDF-ami profili).
2. **Chcesz zrobic to w jednym posiedzeniu czy etapami?** - jesli etapami, ustal z userem punkty naturalnych przerw (miedzy sekcjami), pokaz jak wznowic (`/aios:init` - skill wczyta `onboarding-progress.md` i wskoczy w to miejsce, gdzie zostalo).
3. **Masz PDF FRIS / Gallup Clifton Strengths?** - jesli tak, user uploaduje w sekcji C. Jesli nie, C przechodzi na sciezke "bez PDF" (C1'-C4').

Na tej podstawie ustal `$TRYB` (`szybki` / `standard` / `pelny`) i `$MA_PROFILE_PDF` (`tak` / `nie`).

**Raport dla usera:**

> OK - pracujemy w trybie $TRYB, jedno posiedzenie / etapami, z / bez PDF. Startuje od sekcji A - Tozsamosc (5 pytan).

---

## Kroki A-J - flow sekcji

Dla kazdej sekcji A-J wykonaj ten sam wzor:

### Wzor wykonania sekcji

1. **Wczytaj pytania sekcji z `pytania.md`.** Sekcje sa oznaczone `## Sekcja X - Nazwa`. Pytania wewnatrz maja IDs (`A1`, `A2`, `B1`, itd.).
2. **Zapowiedz sekcje userowi.** Jedno zdanie: "Sekcja A - Tozsamosc, 5 pytan. Zaraz je wszystkie pokaze, odpowiadaj numerkiem / skrotem / wolnym tekstem."
3. **Pokaz pytania batchem** (chyba ze tryb pytanie-po-pytaniu).
4. **Odbierz odpowiedzi.** Jesli user pominal jakies - dopytaj. Jesli user odpowiedzial niejasno - dopytaj tylko to pytanie, nie cala sekcja.
5. **Zapisz odpowiedzi do bufora sesyjnego.** Nie pisze ich jeszcze do `me.md` - pisze na koncu, w finalizacji. W trakcie sesji trzymam w pamieci + `onboarding-progress.md`.
6. **Krotki raport konczacy sekcje.** "Sekcja A gotowa. Przechodze do B - Zakres systemu (3 pytania)."

### Specyfika poszczegolnych sekcji

**Sekcja A - Tozsamosc (5 pytan).** Imie, rola, kontekst zawodowy, strefa czasowa, jezyk vaulta.

**Sekcja B - Zakres systemu (3 pytania).** Praca / prywatne / hybryda - decyduje o tym, czy w strukturze `Projekty/` bedzie dzial prywatny, czy osobne kategorie dla domen zawodowych. Aktywuje (lub nie) Sekcje H.

**Sekcja C - Profile psychologiczne (5 pytan, opcjonalne).**
- Jesli `$MA_PROFILE_PDF = tak`: poproś usera o upload PDF (FRIS i/lub Clifton). **AI czyta PDF natywnie (multimodal)** - wyciagnij typ FRIS + top 5 Clifton + dominujace perspektywy. Pokaz userowi propozycje interpretacji: "Wyglada na: <typ FRIS> / <dominujaca perspektywa> / aktywne DECYDUJE, ZMIENIAM, ROZWAZAM. Top 5 Clifton: <lista>. Zgadza sie?". **Czekaj na potwierdzenie** zanim uzyjesz wnioskow do kalibracji Sekcji F.
- Jesli `$MA_PROFILE_PDF = nie`: sciezka bez PDF (C1'-C4') - 4 krotkie pytania o tempo, styl informacji, tolerancje krytyki, autoopis.
- Szczegoly parsowania PDF: patrz `docs/parsowanie-pdf.md` w repo.

**Sekcja D - Projekty i obszary (5 pytan).** Lista glownych obszarow zainteresowan - te staja sie podkatalogami `Projekty/`. Zapisz `$PROJEKTY_KATEGORIE` do bufora.

> **Po D5 - pokaz archetypy** (decyzja 2026-04-21):
>
> 1. Na podstawie odpowiedzi z A2/A3 (rola, branza) i D1 (obszary) wybierz 1-2 najblizsze archetypy z `docs/przyklady/` (marketing manager / developer / student programowania).
> 2. Pokaz userowi: "Widze, ze jestes podobny do archetypu [X]. Oto jak wyglada `me.md` i `Projekty/` u tej persony: [link / fragment]. Chcesz sie zainspirowac struktura, czy idziesz wlasna sciezka?"
> 3. **Nie kopiuj** archetypu automatycznie - user decyduje. Archetyp to wzorzec wizualny, nie szablon do wklejenia.

**Sekcja E - Stos technologiczny (8 pytan).** OS, edytor tekstu, synchronizacja, viewer, Pinecone (tak / nie / pozniej), git, inne narzedzia. Jesli E5=tak, przygotuj liste krokow Pinecone do FIN4 (oddasz userowi na koncu).

**Sekcja F - Preferencje komunikacyjne (10 pytan).** To jest sedno personalizacji. 10 pytan (9 wyboru + 1 wolny tekst) miksuje elementy z `docs/szablony/style-komunikacji/`. Na wyjsciu: wygenerowany blok `## Hard rules` w `me.md`, osobisty dla tego usera. **Sekcja F zawsze 10 pytan** - nie ma trybu skroconego.

**Sekcja G - Rytm i nawyki (4 pytania).** Kiedy user zwykle pracuje, jak czesto otwiera vault, czy chce daily / weekly rytualy. Generuje strukture `Kalendarz/` i ewentualnie propozycje `/aios:koniec-sesji` po kazdej sesji.

**Sekcja H - Prywatne (6 pytan, warunkowe).** Tylko jesli Sekcja B1 = prywatne / hybryda. Patrz `docs/szablony/prywatnosc.md` - tam jest pelny scenariusz obslugi tej sekcji i zapisu w me.md.

**Sekcja I - Materialy do zassania (4 pytania).** Czy user ma LinkedIn, WWW, PDF-y, ktore chce wciagnac do `Wiedza/` na start. Jesli tak - po finalizacji zaproponuj `/aios:dodaj-do-wiki` na pierwszych 3-5 materialach.

**Sekcja J - Finalizacja (5 pytan).** Sciezka vaulta (juz ustalona w INSTALL.md, tylko potwierdzenie), git (potwierdzenie z E7, nie pytanie od nowa), backup (potwierdzenie z E3), podglad `me.md`, ostatnie slowo usera.

---

## Krok finalizujacy (FIN1-FIN5)

Po przejsciu sekcji A-J, z buforem wszystkich odpowiedzi:

### FIN1 - Generuj `me.md`

Wczytaj `docs/szablony/me-template.md`, podstawiaj wartosci z bufora. Zapisz do `<VAULT_PATH>/me.md` (nadpisuje pusty szablon z INSTALL-u). Pokaz userowi finalny plik, poproś o ostatnie korekty.

### FIN2 - Stworz strukture `Projekty/`

Dla kazdej kategorii z `$PROJEKTY_KATEGORIE` - utworz `Projekty/<nazwa>/` z pustym `index.md`. Nie tworz konkretnych projektow - to zrobi `/aios:stworz-projekt`, gdy user je zacznie.

### FIN3 - Stworz `vault-map.md`

Mapa, co user ma gdzie (root level `vault-map.md`). Wylistuj katalogi glowne z krotkim opisem, link do `me.md`, link do `Projekty/index.md`.

### FIN4 - Pinecone (warunkowe)

Jesli Sekcja E5 = tak:

- Wyswietl userowi liste krokow: zarejestruj konto na `pinecone.io`, utworz index `<user-chosen-name>`, skopiuj API key, wklej do `~/.claude/settings.json` pod `mcpServers.pinecone.env.PINECONE_API_KEY` (albo odpowiednika w Cowork - user znajdzie w dokumentacji swojego klienta MCP).
- **Nie rob tego za usera.** Podaj instrukcje, poczekaj na potwierdzenie "gotowe".
- Po potwierdzeniu - test: sprobuj wywolac `mcp__pinecone__*` (lub rownowazne w konfiguracji usera). Jesli dziala - raport sukces. Jesli nie - troubleshoot (patrz Error handling).

### FIN5 - Raport koncowy i propozycje dalej

Jedno zwiezle podsumowanie:

> AIOS-Klaudynka skonfigurowana.
> - `me.md` wygenerowany - $N regul, $M projektow, profil $PROFILE.
> - `Projekty/` ma $K kategorii.
> - Pinecone: $PINECONE_STATUS.
> - $MATERIALY_STATUS (jesli I = tak, zaproponuj `/aios:dodaj-do-wiki` na nich).
>
> Co dalej?
> - Chcesz wrzucic pierwsze materialy do Wiedzy?
> - Chcesz zaczac projekt `/aios:stworz-projekt`?
> - Chcesz pobawic sie w sortowanie inboxu?

Oddaj kontrole - user decyduje.

---

## Obsluga przerw

Na poczatku kazdej sekcji - zapisz do `<VAULT_PATH>/_pamiec/onboarding-progress.md`:

```markdown
# Onboarding in progress

**Ostatnio zakonczona sekcja:** $LAST_DONE (np. "B")
**Nastepna sekcja:** $NEXT (np. "C")
**Data:** $DATE
**Tryb:** $TRYB

## Odpowiedzi

<zapisane odpowiedzi z bufora, wszystkie ID pytan + wartosci>
```

Jesli user stopuje ("wroce jutro") - zaakceptuj, powiedz jak wznowic (`/aios:init` - skill wczyta progress i wskoczy w nastepna sekcje).

Jesli user uruchamia `/aios:init` po raz drugi, a plik `onboarding-progress.md` istnieje - zapytaj:

> Widze, ze masz niedokonczony onboarding (zatrzymales sie po sekcji $LAST_DONE). Chcesz: (a) wznowic od $NEXT, (b) zaczac od zera, (c) zobaczyc postep i potem zdecydowac?

Po finalizacji - **usun** `onboarding-progress.md`. Onboarding jednorazowy, nie potrzeba go trzymac.

---

## Error handling

### User odpowiada nonsensem albo trollem

Dopytaj raz konkretnie. Jesli dalej dziwne - przyjmij default z szablonu, idz dalej. Nie blokuj onboardingu.

### PDF profilu nie parsuje sie

Zglos userowi, zapytaj czy chce: (a) podac recznie 3-5 kluczowych zdan z profilu, (b) przejsc na sciezke bez PDF (C1'-C4'), (c) zatrzymac onboarding, zeby poszukac innego pliku.

### Interpretacja PDF zakwestionowana przez usera

Jesli po multimodalnym odczycie user mowi "nie, to nie jest moj profil" / "zle odczytales X" - zapytaj co chce poprawic, wez poprawki, pokaz nowa wersje, czekaj na kolejne potwierdzenie. Nie forsuj automatycznej interpretacji.

### Struktura `Projekty/` juz istnieje z plikami

Nie nadpisuj. Zapytaj usera czy dokleic nowe kategorie obok istniejacych, czy anulowac FIN2.

### Pinecone API key nie dziala

Standard troubleshooting: sprawdz literowki, sprawdz czy klucz jest aktywny w Pinecone dashboard, sprawdz sciezke configa MCP. Jesli w 3 probach nie dziala - zaznacz w `me.md`, ze Pinecone jest "planowany do konfiguracji", idz dalej bez niego. User dokonczy kiedys.

---

## Metadane

- **Wersja skilla:** v0.3 (MVP).
- **Zaleznosci:** `pytania.md` (pytania, obok tego pliku), `docs/szablony/me-template.md` (szablon), `docs/szablony/style-komunikacji/*.md` (biblioteka dla Sekcji F), `docs/szablony/prywatnosc.md` (Sekcja H), `docs/przyklady/*.md` (archetypy pokazywane po D5), `docs/parsowanie-pdf.md` (parsowanie FRIS/Clifton).
- **Uruchamiany przez:** `/aios:init` (CC/Cowork) albo "wykonaj init" (tryb zdegradowany, plain .md w `_skille/aios/`).
- **Output:** `me.md`, struktura `Projekty/*/index.md`, `vault-map.md`, opcjonalnie konfiguracja Pinecone MCP.
