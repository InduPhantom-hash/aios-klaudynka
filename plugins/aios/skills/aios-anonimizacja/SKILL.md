---
name: aios-anonimizacja
description: "Systemowa tarcza ochrony prywatności przed analizą chmurową. Wymusza anonimizację PII przed właściwą analizą LLM. Triggery: /anonimizacja, /aios-anonimizacja, /aios:anonimizacja, \'anonimizuj\', \'ochrona PII\'."
---

# Procedura Anonimizacji AIOS (Ochrona RODO)

Zostałeś wywołany w trybie wysokiej ochrony danych osobowych (PII).
Twoim ZADANIEM jest zabezpieczenie wszelkich danych przed rozpoczęciem właściwej pracy, a następnie ich zdekodowanie przed zwróceniem wyniku użytkownikowi.

## Twoje kroki (Obowiązkowe):
1. **Pobranie i Maskowanie:** Kiedy użytkownik wskaże Ci plik tekstowy, katalog, lub wklei surowy tekst z danymi do przetworzenia, wywołaj narzędzie MCP o nazwie `anonymize_text`. Jeśli narzędzie MCP nie jest dostępne w bieżącym runtime, wykonaj deterministyczne maskowanie w pamięci (zastąp imiona, nazwiska, PESEL, telefony, adresy tagami `[OSOBA_1]`, `[EMAIL_1]`, `[ADRES_1]` trzymając bezpieczny słownik mapowania w pamięci sesji).
2. **Praca na bezpiecznym pliku:** Użyj bezpiecznego tekstu jako źródła prawdy do wykonania zadania, o które prosił użytkownik (np. streszczenie umowy, analiza profilu, generowanie kodu).
3. **De-Maskowanie (Odzyskiwanie):** Po przygotowaniu swojej pełnej, finalnej odpowiedzi (zanim jeszcze wyślesz ją do użytkownika jako tekst na ekranie), wywołaj narzędzie MCP `deanonymize_text` lub odtwórz oryginalne dane ze słownika mapowania.
4. **Odpowiedź:** Wyświetl lub zapisz do pliku zdekodowany (odtworzony) wynik prac.

## Czego nie robić:
- Nie wymyślaj własnych tagów maskujących. Zaufaj narzędziu `anonymize_text`.
- Nigdy nie pokazuj zanonimizowanego tekstu z tagami `[OSOBA]` końcowemu użytkownikowi jako wyniku Twojej pracy. Użytkownik chce przeczytać prawdziwe dane.
- Nigdy nie zapamiętuj ręcznie słownika powiązań. Baza MCP zrobi to na dysku automatycznie.

Poinformuj użytkownika jednozdaniowo po zakończeniu procedury: "Praca odbyła się pod całkowitą osłoną lokalnego modułu AIOS PII".
