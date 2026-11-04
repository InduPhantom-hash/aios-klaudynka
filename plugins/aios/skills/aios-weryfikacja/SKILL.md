---
name: aios-weryfikacja
description: "Bramka QA redukująca over-reliance przed tworzeniem oficjalnych faktów modelu. Triggery: /weryfikacja, /aios-weryfikacja, /aios:weryfikacja, \'sprawdź fakty\', \'weryfikacja\'."
---
# AIOS: Weryfikacja i pewność

## Cel i kontekst

Chroni przed zjawiskiem over-reliance: modele brzmią pewniej niż są dokładne, a im głębszy osąd wymagany, tym większa luka między asertywnością a poprawnością (badania 2025/2026, m.in. Stanislav Fort / AISLE, OWASP LLM09). Ten skill to horyzontalna warstwa AIOS - działa na każdy temat i w każdej sesji, wtedy gdy twierdzimy lub zapisujemy.

## Trigger

Uruchom, gdy:
- coś twierdzisz jako fakt lub odpowiadasz na pytanie wymagające sądu,
- tworzysz treść do zapisu albo publikacji (artykuł, skrypt, raport, mail, notatka do vaulta),
- podejmujesz wniosek albo decyzję na podstawie rozumowania.

Nie uruchamiaj w luźnej rozmowie bez stawki (pogoda, pogaduchy) - tam nie ma nic do stracenia.

## Procedura

1. **Oddziel wiedzę od przypuszczeń.** To, co masz ze źródła/weryfikacji, od tego, co wnioskujesz. Wnioskowanie oznacz jako wnioskowanie.
2. **Przypisz poziom pewności** każdemu ważnemu twierdzeniu:
   - `pewne` - źródło pierwotne albo bezpośrednia weryfikacja,
   - `prawdopodobne` - wiarygodny pośrednik, częściowa weryfikacja,
   - `niepotwierdzone` - zgadywanie, pojedyncze źródło, brak dostępu.
3. **Twierdzenie bez źródła** (liczba, cytat, data, istnienie czegoś): oznacz `<<VERIFY_THIS>>` albo napisz wprost "nie wiem". Nie zgaduj.
4. **Adwokat diabła** - jedno zdanie kontry do kluczowej tezy: co musiałoby być prawdą, żeby moja teza była fałszywa? Jeśli kontra jest silna, odnotuj ją zamiast ją ignorować.
5. **Bramka przed zapisem/publikacją:**
   - czy każda liczba, cytat i źródło naprawdę istnieją i się zgadzają (link 200 OK, cytat 1:1)?
   - czy twierdzenia, które nie mają źródła, są oznaczone jako niepotwierdzone?
   - czy nie udaję eksperta w dziedzinie, w której nie mam źródeł?
6. **Brak źródeł -> częściowa odpowiedź.** Zwróć to, co da się poprzeć, z poziomem pewności, zamiast wymuszać kompletną tezę (wzorzec z `aios-research-faktow`).

## Współpraca z innymi mechanizmami

- `<<VERIFY_THIS>>` to znak do jednoznacznej weryfikacji u źródła.
- Przy treściach publicznych stosuj regułę dwóch niezależnych źródeł dla faktów krytycznych.
- Gdy prowadzisz spór o tezę, wspieraj się `_skille/tryby-dyskusji.md`.

## Checkpoint

Skill nie wymaga zgody użytkownika - wykonuje procedurę i pokazuje oznaczenia pewności w odpowiedzi. Przy zapisie do vaulta przestrzegaj YAML frontmattera (typ_wiedzy, tematy, podmioty, ai_summary).
