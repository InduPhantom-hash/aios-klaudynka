# me.md - Profil $imie

> Fundament kontekstu. Czytany na starcie każdej sesji.
> Ostatnia aktualizacja: $data_generacji

---

<!-- =================================================================
     SZABLON me.md dla AIOS-Klaudynki
     Instrukcja dla AI-wykonawcy wypełniającego ten plik:
     - $zmienna -> podstaw wartość z bufora odpowiedzi (Sekcje A-J).
     - <!-- IF:warunek --> ... <!-- ENDIF --> -> wstaw blok tylko jeśli warunek prawdziwy.
     - <!-- LOOP:$lista --> ... <!-- ENDLOOP --> -> powtórz blok dla każdego elementu listy.
     - <!-- OPT --> ... <!-- /OPT --> -> blok opcjonalny (pomiń jeśli brak danych).
     - Usuń WSZYSTKIE komentarze HTML przed zapisem finalnego pliku.
     - Nigdy nie używaj - ani - (tylko myślnik ASCII "-").
     ================================================================= -->

## Hard rules dla AI

<!-- Hard rules układane w porządku F1, F2 ... F10 (patrz Mapowanie F1-F10 w pytania.md).
     Pomijaj pozycje z wariantu "zależy" (brak hard rule).
     Pozycje z C5, H1, H6, B3, D5 idą na dół, pod osobną podsekcję "Tematy i granice". -->

<!-- LOOP:$hard_rules_F -->
$index. $tresc_hard_rule
<!-- ENDLOOP -->

<!-- IF:$ma_tematy_i_granice -->

### Tematy i granice

<!-- LOOP:$tematy_granice -->
- $tresc_tabu_lub_opt_out
<!-- ENDLOOP -->
<!-- ENDIF -->

---

## Kim jestem

$imie. $rola.
<!-- IF:$branza_wypelniona -->Pracuję w branży $branza.<!-- ENDIF -->

Strefa czasowa: $tz.
Język vaulta: $jezyk.

<!-- OPT: jeśli C4 = autoopis wypełniony, dopisz 1-2 zdania z autoopisu usera. -->
<!-- IF:$autoopis_wypelniony -->

$autoopis
<!-- ENDIF -->

<!-- OPT: jeśli J5 = wolny tekst oznaczony jako "dziennikowe ważne dla mnie" (kategoria c) -->
<!-- IF:$j5_dziennikowe -->

### Dodatkowe notki

$j5_dziennikowe_tresc
<!-- ENDIF -->

---

<!-- IF:$ma_profil_psychologiczny -->
## Profil psychologiczny

<!-- IF:$ma_fris -->
### FRIS

- Styl Myślenia: **$fris_styl_myslenia**. $fris_styl_myslenia_opis
- Styl Działania: **$fris_styl_dzialania**. $fris_styl_dzialania_opis
- Aktywne postawy: $fris_postawy_aktywne. Nieaktywne: $fris_postawy_nieaktywne.
<!-- ENDIF -->

<!-- IF:$ma_clifton -->

### CliftonStrengths Top 5

<!-- LOOP:$clifton_top5 -->
$pozycja. **$nazwa** ($domena) - $opis_krotki
<!-- ENDLOOP -->
<!-- ENDIF -->

<!-- IF:$ma_inne_testy -->

### Inne profile

$inne_testy_tresc
<!-- ENDIF -->

---
<!-- ENDIF -->

<!-- IF:$ma_styl_pracy -->
## Styl pracy

<!-- Wypełniane z C1'-C3' (ścieżka bez PDF) oraz sygnałów kalibracyjnych.
     Jeśli user miał PDF (ścieżka C1-C5) - ta sekcja MOŻE być pominięta, bo profil opisuje styl. -->

<!-- IF:$tempo_wypelnione -->- Tempo decyzji: $tempo.<!-- ENDIF -->
<!-- IF:$format_wypelniony -->- Preferowany format informacji: $format_preferred.<!-- ENDIF -->
<!-- IF:$krytyka_wypelniona -->- Reakcja na krytykę: $krytyka.<!-- ENDIF -->

---
<!-- ENDIF -->

## Aktywne projekty

<!-- Tabela wypełniana z D1 (obszary) + D3 (najaktywniejszy idzie na górę).
     Pełne konteksty projektów w Projekty/<kategoria>/. -->

| Projekt / Obszar | Ścieżka | Status |
|---|---|---|
<!-- LOOP:$obszary_z_najaktywniejszym_na_gorze -->
| $nazwa_obszaru | `Projekty/$sciezka_obszaru/` | $status |
<!-- ENDLOOP -->

<!-- IF:$ma_projekty_z_D4 -->

**Konkretne projekty utworzone na starcie (z D4):**

<!-- LOOP:$projekty_z_D4 -->
- `Projekty/$kategoria/$nazwa/` - $opis_krotki
<!-- ENDLOOP -->
<!-- ENDIF -->

---

## Stack

| Narzędzie | Rola |
|---|---|
| OS | $os |
| Edytor plików | $edytor |
| Synchronizacja | $sync |
| Główny AI | $ai |
<!-- IF:$pinecone_aktywny -->| Pinecone | $pinecone_status |<!-- ENDIF -->
<!-- IF:$git_aktywny -->| Git | $git_choice |<!-- ENDIF -->

<!-- IF:$inne_narzedzia_wypelnione -->

**Inne narzędzia w kontekście pracy:** $inne_narzedzia_lista
<!-- ENDIF -->

---

## Rytm pracy

- Główne godziny pracy: $godziny_pracy.
- Częstotliwość vault: $czestotliwosc.
<!-- IF:$rytualy_aktywne -->- Rytuały: $rytualy (templates w `Kalendarz/`).<!-- ENDIF -->
- `/aios:koniec-sesji` proponowany: $koniec_sesji_tryb.

---

<!-- IF:$ma_sekcje_prywatnosc -->
## Prywatność

<!-- Sekcja tylko gdy B1 = prywatne lub hybryda. -->

<!-- IF:$h2_wypelnione -->- Osoby trzecie w notatkach: $osoby_trzecie_tryb.<!-- ENDIF -->
<!-- IF:$h3_folder_prywatne -->- Folder `Prywatne/` istnieje<!-- IF:$h3_poza_gitem --> i jest poza gitem<!-- ENDIF -->.<!-- ENDIF -->
<!-- IF:$h5_wypelnione -->- Proaktywność w prywatnym: $proaktywnosc_prywatna_tryb.<!-- ENDIF -->

<!-- IF:$h4_wypelnione -->

### Styl AI w prywatnym

$h4_tresc
<!-- ENDIF -->

---
<!-- ENDIF -->

<!-- IF:$ma_blizniaki -->
## Blizniaki

<!-- Generowany z E10-E13. Szczegoly schematu: docs/szablony/blizniacy.md -->
<!-- Pomijaj cala sekcje jesli E10=brak AND E12=nie AND E13=nie -->

### Task tracker
<!-- IF:$task_tracker_typ_nie_brak -->
- typ: $task_tracker_typ
- workspace: $tracker_workspace
- mapowanie kategoria -> lista:

| kategoria | lista / projekt |
|-----------|-----------------|
<!-- LOOP:$tracker_mapowanie -->
| $kategoria | $lista_lub_projekt |
<!-- ENDLOOP -->
<!-- ELSE -->
- typ: brak
<!-- ENDIF -->

### Search & ingest
- tavily: $tavily_status

### Calendar
- google-calendar: $google_calendar_status
- strefa czasowa: $tz

### MCP do monitorowania
- lista: [$mcp_lista_oddzielona_przecinkami]

---
<!-- ENDIF -->

## Metadane

- Wersja szablonu: me-template v0.2 (2026-04-25 - dodany blok Blizniaki).
- Wygenerowany przez: `/aios:init` w wersji v0.4 (szablon i skill trzymaja sie razem - bump synchroniczny, patrz decyzje.md).
- Tryb onboardingu: $tryb (szybki / standard / pelny).
- Lacznie odpowiedzi w buforze: $n_odpowiedzi / 61 max.
<!-- IF:$j5_kategoria_d -->
- Dodatkowe notatki z onboardingu: `_brudnopis/onboarding-notes-$data_generacji.md` (J5 kategoria d - tekst nie pasowal do F10/E8/Kim jestem).
<!-- ENDIF -->
