---
name: aios-research-faktow
description: "Zautomatyzowany, oparty na metodologii (SIFT, RADAR, Lateral Reading) system do pogłębionego researchu z wbudowanym filtrem Anty-AI Slop. Zwraca rygorystyczny Evidence Brief. Triggery: /research-faktow, /aios-research-faktow, /aios:research-faktow, 'research faktów', 'sprawdź fakty', 'evidence brief'."
---

# AIOS Research Faktów (Evidence Brief)

## Cel
Twórz rygorystyczny, oparty o metodykę naukową i dziennikarską `Evidence Brief` dla dowolnej dziedziny (agnostyk domenowy). Pracuj wyłącznie na publicznie dostępnych materiałach. Eliminuj halucynacje i "AI Slop" poprzez twardą weryfikację i rygor językowy.

## Etap 1: Intake & Profiler Epistemiczny (Zatrzymanie i Dialog)
Gdy użytkownik podaje temat/pytanie:
1. Określ dziedzinę zapytania (np. medycyna, IT, marketing, socjologia).
2. Zdefiniuj na podstawie zapytania **Hierarchię Dowodów** (co jest szczytem rzetelności w tej dziedzinie, a co dnem).
3. Podziel problem (stosując logikę PICO) na 3-5 atomowych mikrotematów badawczych.
4. **Zatrzymaj się.** Pokaż krótko powyższe ustalenia i zapytaj użytkownika: *"Które z tych mikrotematów mamy zbadać?"*. Nie rozpoczynaj wyszukiwania przed decyzją.

## Etap 2: Ekspedycja Badawcza (Pełna Autonomia - Lateral Reading)
Po wyborze mikrotematów działasz autonomicznie, bez kolejnych pytań.
1. Dla każdego wybranego mikrotematu powołaj osobny wątek wyszukiwania (lub użyj subagentów, jeśli runtime na to pozwala).
2. Zespół ma jedno zadanie: znaleźć surowe fakty i cytaty, a nie formułować gotowe wnioski z pierwszego brzegu.
3. Obowiązuje nakaz stosowania **Lateral Reading** (nie ufaj jednej stronie - po znalezieniu twierdzenia, otwórz nową kartę i sprawdź reputację autora/źródła u niezależnych podmiotów trzecich).

## Etap 3: Bramka QA i Filtracja Źródeł (RADAR)
Gdy zbierzesz urobek (URL, cytat, metadane), przepuść go przez filtr **RADAR**:
- **R**ationale: Jaki był cel publikacji?
- **A**uthority: Jaki jest obiektywny autorytet autora (na podstawie Lateral Reading)?
- **D**ate: Czy dane są aktualne?
- **A**ccuracy: Czy tekst popiera się własnymi danymi/odwołaniami?
- **R**elevance: Czy to odpowiada na nasz mikrotemat?
Odrzuć surowo każdy dowód, który obleje test. Zostaw tylko twarde "cegły".

## Etap 4: Red-Teaming (Trace Claims)
Dla najważniejszych, potwierdzonych twierdzeń z Etapu 3:
1. Wykonaj dodatkowe, dedykowane wyszukiwanie, celowo szukając kontrargumentów (np. "krytyka [teoria X]", "dlaczego [teza Y] jest błędna").
2. Jeśli znajdziesz luki lub dowody przeciwne, bezwzględnie oznacz tezę jako "Spór / Częściowo potwierdzone". 

## Etap 5: Synteza i Raport (PRISMA-style & Anti-Slop)
Wygeneruj końcowy `Evidence Brief` w czystym formacie Markdown. 
Podczas pisania musisz bezwzględnie zastosować **8 Zasad Raportowania i Anti-AI Slop**:
1. **Plain Polish:** Pisz maksymalnie prostym, surowym językiem. Zero "lania wody".
2. **Zakaz strony biernej:** Zamiast "zostało udowodnione", używaj "badanie X udowadnia".
3. **Zakaz nowomowy urzędowej:** Wyeliminuj słowa typu "niniejszy", "w miesiącu", "stanowi".
4. **Zakaz zagnieżdżonych dopełniaczy:** Nie buduj konstrukcji typu "proces budowy strategii rozwoju produktu".
5. **Zero pustych przymiotników:** Całkowity zakaz słów: "kluczowy", "innowacyjny", "kompleksowy", "niezwykły", o ile nie są poparte twardą miarą.
6. **Zero clickbaitów i patosu:** Żadnych wstępów typu "Prawdziwy problem polega na tym", "W dzisiejszym dynamicznie zmieniającym się świecie".
7. **Zero emoji:** Raport to profesjonalny, naukowy dokument, nie używaj w nim emotikon.
8. **Bezwzględna weryfikowalność (Deep Links i Text Fragments):**
   - **Zakaz linkowania do stron głównych** (np. `https://pie.net.pl`). Musisz podać dokładny, pełny adres podstrony/raportu.
   - **Nakaz Text Fragments:** Każdy link przy konkretnym cytacie musi zawierać parametr przeglądarki przenoszący prosto do tekstu, format: `[Tytuł](https://pelny-adres.pl/artykul#:~:text=kilka_slow_z_cytatu)`.
   - Każde źródło MUSI być poparte klikalnym linkiem Markdown.

**Zawartość Raportu:**
1. Pytanie i przyjęta Hierarchia Dowodów.
2. Tabela zweryfikowanych, najlepszych źródeł z oceną ich wiarygodności według RADAR (każde źródło musi być linkiem `[Nazwa](URL)`).
3. Wnioski w podziale na mikrotematy (z podziałem na **Potwierdzone**, **Sporne** i **Niepotwierdzone** - każde twierdzenie wymaga cytatu opatrzonego klikalnym linkiem prosto do domeny).
4. Ograniczenia raportu (czego nie znaleziono, luki w dowodach).
