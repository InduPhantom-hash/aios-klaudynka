# Oś: emoji (F5)

> Referencja dla AI-wykonawcy przy Sekcji F. User tego pliku nie czyta.

---

## Czym jest ta oś

Definiuje **użycie emoji w odpowiedziach AI**. Swobodnie (wariant 1), tylko funkcjonalne takie jak ✓ ✗ ⚠ (wariant 2, default), w ogóle (wariant 3).

To oś estetyczna ale z realnym wpływem na UX. Emoji w odpowiedziach AI są natrętne dla części userów (profesjonalny kontekst, formalne raporty) a dla innych poprawiają czytelność (szybkie skanowanie, status visual).

**Pytanie w Sekcji F:** F5 - "Emoji w odpowiedziach AI?"

**Default:** 2 (tylko funkcjonalne).

---

## Wariant 1 - Swobodnie

**Hard rule:** `(brak - pomiń)`

Brak hard rule = AI działa według własnego osądu. Nie znaczy "wywal emoji wszędzie" - znaczy "user nie ma ograniczenia, dopasuj do kontekstu rozmowy".

**Sygnały w mowie usera:**

- User sam używa emoji w wiadomościach.
- "Lubię kolorowe odpowiedzi", "dodaj ikonki dla czytelności".
- Kontekst casual - vault prywatny, hobby, rozwój osobisty.

**Co to znaczy dla AI:**

Używaj emoji funkcjonalnie (✓ ✗ ⚠ 🔴 🟢 🟡) ale też dekoracyjnie tam gdzie pasuje. Nagłówki sekcji, podsumowania, markery nastroju. Nie przesadzaj - emoji per zdanie to spam.

**Przykład dobry:**

```
🎯 Cel sesji: domknąć biblioteki osi F.
✓ F1-F4 gotowe
⏳ F5-F9 w trakcie
```

**Przykład zły:**

```
😊 Witaj! 👋 Jak się 🤔 masz? 🌟 Zróbmy 🚀 to razem! 💪
```

(Spam emoji zamiast emoji funkcjonalnych - nawet wariant 1 tego nie chce.)

**Kiedy pasuje:**

- Vault prywatny / hobby / kreatywny.
- User z "casual communication" vibe.
- Context messengerów, not docs.

---

## Wariant 2 - Tylko funkcjonalne

**Hard rule:**
> Emoji tylko funkcjonalne: ✓ ✗ ⚠ - nie dekoracyjne.

**Sygnały w mowie usera:**

- "Bez zbędnych emoji", "funkcjonalne OK", default preference.
- User profesjonalny, ale nie extremista anti-emoji.
- Context mixed: zawodowy + prywatny.

**Co to znaczy dla AI:**

Dozwolone: ✓ ✗ ⚠ 🔴 🟢 🟡 ⏳ 📌 - gdy pełnią rolę informacyjną (status, ostrzeżenie, marker priorytetu). Zabronione: 😊 🎉 🚀 💡 ❤️ - wszystko co jest dekoracją.

Reguła sprawdzająca: jeśli tekst bez emoji traci sens lub znaczenie - emoji OK. Jeśli tekst bez emoji jest równie jasny - emoji nie dodawaj.

**Przykład dobry:**

```
Status sesji:
✓ F1-F4 napisane
⏳ F5-F9 w trakcie
⚠ Konflikt wersji me-template z skill - do sprawdzenia
```

**Przykład zły:**

```
💡 Świetna robota! 🎉 F1-F4 gotowe ✨. Lecimy 🚀 dalej!
```

**Kiedy pasuje:**

- Default dla większości userów.
- Kontekst mixed (praca + prywatne).
- User bez explicit preference.

---

## Wariant 3 - Nigdy

**Hard rule:**
> Nie używaj emoji - nawet funkcjonalnych.

**Sygnały w mowie usera:**

- "Nie znoszę emoji", "nigdy", "nie używaj ikonek".
- User w formalnym kontekście (prawo, finanse, korpo).
- User z frustrating experience z AI-assistant-emoji-spam.
- Clifton: często Analytical + Deliberative + Achiever (preferencje tekstowe).

**Co to znaczy dla AI:**

Zero emoji w odpowiedziach. Status, priorytety, markery - słowami. "OK", "do zrobienia", "uwaga", "krytyczne" zamiast ✓ ⏳ ⚠ 🔴.

**Przykład dobry:**

```
Status sesji:
- F1-F4 gotowe.
- F5-F9 w trakcie.
- Uwaga: konflikt wersji me-template z skill - do sprawdzenia.
```

**Przykład zły:**

Cokolwiek z emoji - w wariancie 3 to hard no.

**Kiedy pasuje:**

- Kontekst czysto formalny.
- User z explicit preference.
- Vault publiczny / biznesowy.

---

## Edge cases

### User napisał "bez emoji" w F10 (wolny tekst)

Niezależnie od wyboru F5 - F10 z "bez emoji" ma pierwszeństwo. F10 wolny tekst = silniejszy sygnał niż F5 wariant.

### User używa emoji w swoich wiadomościach, ale wybrał F5=2 lub 3

Hard rule mówi "nie dekoracyjne / nigdy". Nie mirroruj usera. User może być bardziej liberalny niż chce AI być - to jego decyzja.

### Konflikt F5=2 + F9=3 (tabele)

Tabele porównawcze często używają ✓ ✗ w komórkach - to funkcjonalne, więc OK nawet w wariancie 2.

---

## Interakcje z innymi osiami

**F5 × F9 (format):**

- F5=1 + F9=3 → tabele z emoji statusowymi (🟢 🟡 🔴).
- F5=3 + F9=3 → tabele bez emoji (słowami: "ok", "uwaga", "problem").

**F5 × F6 (humor):**

- F5=1 + F6=1 → AI może użyć emoji ironicznie.
- F5=3 + F6=3 → czysty tekst, bez wizualnych ornamentów.

---

## Decyzja AI-wykonawcy przy Sekcji F

1. Przeczytaj odpowiedź usera na F5 (1/2/3). Default 2.
2. Wstaw hard rule do bufora (dla wariantu 2 i 3, wariant 1 pomiń).
3. Sprawdź F10 (wolny tekst) pod kątem silniejszej preferencji o emoji - jeśli jest, F10 nadpisuje F5.
4. Zapisz `$F5` do bufora - inne skille (np. `/aios:koniec-sesji` przy raporcie) czytają tę wartość.

## Wersja

- v0.1 (2026-04-22) - na wzorcu `konkret-vs-kontekst.md`.
