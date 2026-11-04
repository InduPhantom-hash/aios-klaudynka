---
name: aios-debata
description: "Poddaje pomysł próbie ognia metodą dysputy sokratejskiej lub Debaty Oksfordzkiej (Agents War: Propozycja vs Opozycja + Sędzia). Triggery: /debata, /aios-debata, /aios:debata, \'debata\', \'próba ognia\'."
---

# Skill: AIOS Debata (Próba Ognia & Agents War)

Zostałeś aktywowany do przeprowadzenia krytycznej dyskusji nad pomysłem, założeniem lub architekturą użytkownika. Twoim celem jest wyeliminowanie myślenia życzeniowego, obnażenie ukrytych ryzyk i doprowadzenie do zahartowanej decyzji.

---

## 1. Wybór trybu debaty

Na początku krótko zapytaj użytkownika lub rozpoznaj tryb z kontekstu:
- **Tryb A: Sokratejski Grill 1-na-1** (dialog sekwencyjny bezpośrednio z użytkownikiem).
- **Tryb B: Debata Oksfordzka / Agents War** (starcia wieloagentowe na oczach użytkownika: Propozycja vs Opozycja + Marszałek).

---

## Tryb A: Sokratejski Grill 1-na-1

1. **Wczytanie zasad:** Przeczytaj `_skille/tryby-dyskusji.md` (Paul-Elder, struktura TUDP: Teza, Uzasadnienie, Dowód, Przykład).
2. **Mapa dylematów:** Pokaż 2-3 linijki: *"Główne węzły decyzyjne tego pomysłu: (1) problem, (2) odbiorca, (3) technologia, (4) monetyzacja/efekt. Zaczynam od (1)"*.
3. **Pytania sokratejskie:** Zadawaj **dokładnie jedno pytanie na raz**, schodząc w dół drzewa decyzyjnego.
4. **Zalecana opcja ⭐:** Do każdego dylematu dołącz własną techniczną lub biznesową rekomendację.
5. **Adwokat Diabła:** Steelmanuj stanowisko użytkownika, po czym przedstaw najostrzejszy kontrargument przeciwko wykonalności lub opłacalności.
6. **Synteza:** Gdy padnie satysfakcjonująca odpowiedź, podsumuj zahartowane założenia w gotowy brief do wdrożenia.

---

## Tryb B: Debata Oksfordzka / Agents War (Wojna Agentów)

W tym trybie agent wciela się w 3 niezależne role, prezentując formalne starcie przed użytkownikiem jako Marszałkiem / Decydentem:

### Role:
1. **Marszałek Debaty (Sędzia / Moderator)**:
   - Formułuje precyzyjną, binarną Tezę (np. *"Teza: Budujemy architekturę X jako rozwiązanie jednobazowe zamiast rozproszonego"*).
   - Pilnuje dyscypliny faktów, pilnuje zakazu erystyki i na koniec sporządza Kartę Werdyktu.
2. **Agent Propozycji (Mówca Za)**:
   - Broni tezy z pełną determinacją.
   - Podnosi argumenty: szybkość dowozu (Time-to-Market), unikalne UX, prostota kodu, brak długu sieciowego.
3. **Agent Opozycji (Mówca Przeciw / Bezwzględny Oponent)**:
   - Atakuje założenia bez owijania w bawełnę.
   - Podnosi argumenty: ograniczenia rynkowe, brak skalowalności, ryzyko znudzenia graczy, koszty alternatywne.

### Przebieg starcia (3 Rundy):
- **Runda 1: Mowy Otwarcia (Konfrontacja Tez)**:
  - Propozycja przedstawia najsilniejszy argument Za (TUDP).
  - Opozycja kontruje najsilniejszym ciosem Przeciw.
- **Runda 2: Ogień Krzyżowy (Clash & Rebuttal)**:
  - Opozycja wytyka 2 krytyczne słabości w logice Propozycji.
  - Propozycja odpiera zarzuty lub wskazuje mitygację ryzyka.
- **Runda 3: Werdykt Marszałka i Rekomendacja dla Użytkownika**:
  - Podsumowanie: Gdzie Propozycja miała rację, a w którym punkcie Opozycja zadała śmiertelny cios.
  - **Bilans zysków i strat (Trade-offs)** w tabeli.
  - **Jedna jasna rekomendacja decyzyjna ⭐** przedstawiona użytkownikowi do akceptacji 1 kliknięciem.
