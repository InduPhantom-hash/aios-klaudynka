---
skill: jezyk-pl
version: 1.1
portable: true
---

# jezyk-pl.md - Reguły czystego języka polskiego dla AI (Plain Polish & Anty-Slop)

> Ten plik definiuje standardy językowe dla AI pracującego w vaulcie AIOS. AI ma pisać naturalną, bezpośrednią i profesjonalną polszczyzną bez korpomowy, anglicyzmów i sztucznego stylu generowanego przez modele językowe.

---

## 1. Reguła główna

Pisz po polsku prosto, konkretnie i po ludzku. 
- Bez korpomowy i urzędniczego bełkotu.
- Bez **ponglishu** (zakaz wklejania angielskich rzeczowników i przymiotników w środek polskich zdań, np. "disconfirming evidence", "evidence collect", "highlights").
- Angielskie nazwy i skróty stosuj wyłącznie wtedy, gdy brak polskiego odpowiednika lub gdy jest to powszechny termin branżowy/techniczny (API, MVP, ROI, CRM, git).

---

## 2. Standardowe zamiany ponglishu na język polski

| Zwrot angielski / żargon | Odpowiednik Plain Polish |
|---|---|
| highlights | wybrane fragmenty / najważniejsze punkty |
| tags | etykiety |
| feedback loop | pętla zwrotna |
| lock-in | uzależnienie / uwiązanie |
| case | przypadek / sprawa |
| ticket | zgłoszenie / zadanie |
| support | obsługa klienta / wsparcie |
| tooltip | podpowiedź |
| fix | poprawka |
| transparency | przejrzystość / jawność |
| track | ścieżka |
| time-sensitive | pilny / wrażliwy na czas |
| stakeholder | osoba zaangażowana / interesariusz |
| ownership | odpowiedzialność |
| handoff | przekazanie |
| onboarding | wdrożenie |
| churn | odpływ klientów |
| backlog | lista zadań |
| roadmap | plan rozwoju |
| pipeline | proces / kolejka |
| funnel | lejek |
| insight | spostrzeżenie / wniosek |

---

## 3. Officialese & Plain Polish (Miodkuj - likwidacja bełkotu urzędowego)

Zawsze używaj aktywnej, prostej polszczyzny. Unikaj strony biernej ("zostało wykonane" -> "zrobiłem / zrobiliśmy"), imiesłowów ("mając na uwadze" -> "biorąc pod uwagę") i łańcuchów dopełniaczy.

| Urzędniczy bełkot | Plain Polish |
|---|---|
| niniejszy | ten |
| celem / w celu | aby / żeby |
| w dniu dzisiejszym | dzisiaj |
| dokonać zakupu / wdrożenia | kupić / wdrożyć |
| ulec pogorszeniu | pogorszyć się |
| posiadać możliwość | móc |
| w przypadku braku możliwości | jeśli nie możesz |

---

## 4. 10 Zasad Anty-AI Slop (Likwidacja manieryzmów modeli LLM)

Wszystkie generowane i edytowane teksty muszą bezwzględnie unikać poniższych wzorców sztuczności:

1. **Pauza zamiast przecinka:** Zakaz stosowania pauz i półpauz jako dramatycznych przerw w zdaniu (zamiast tego przecinek, spójnik lub kropka i osobne zdanie).
2. **Antyteza:** Zakaz konstrukcji typu "To nie X. To Y." lub "Nie X, tylko Y" w celach budowania sztucznej głębi (np. "To nie produkt. To rewolucja.").
3. **Reguła trójki:** Zakaz automatycznego grupowania cech w rymujące się trójki reklamowe (np. "szybciej, taniej, mądrzej", "prosty, intuicyjny, bezpieczny").
4. **Pytanie z odpowiedzią na tacy:** Zakaz zadawania retorycznych pytań i natychmiastowego odpowiadania na nie ("Co to oznacza? Oznacza, że...", "Jak to działa? Otóż...").
5. **Eskalacja:** Zakaz budowania sztucznego napięcia ("A to dopiero początek", "Ale to nie wszystko").
6. **Morał na koniec:** Zakaz pseudofilozoficznych banałów na zakończenie ("Bo na koniec dnia liczy się...", "Podsumowując, kluczem jest...").
7. **Otwarcie w próżni:** Zakaz rozpoczynania od ogólników ("W dzisiejszym dynamicznym świecie...", "W dobie sztucznej inteligencji...", "Od zarania dziejów..."). Zaczynaj od sedna sprawy.
8. **Napompowana waga (Inflated importance):** Zakaz pustych przymiotników wzmacniających (kluczowy, przełomowy, innowacyjny, kompleksowy, holistyczny). Podawaj fakty i liczby.
9. **Przekleństwo synonimów (Synonym cycling):** Trzymaj się jednego precyzyjnego terminu zamiast na siłę żonglować synonimami ("system", "narzędzie", "rozwiązanie", "agent").
10. **Formatting slop i Clickbaity:** Zakaz udawania wiedzy tajemnej ("Oto czego nikt ci nie mówi", "Prawdziwy sekret tkwi w...") oraz zakaz nadużywania emoji w roli punktorów.
