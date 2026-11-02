---
typ_wiedzy: decyzja
tematy: [klaudynka, rag, wydanie]
podmioty: [AIOS, LanceDB, BGE-M3]
ai_summary: "Kontrakt wydania 0.7.0: lokalny RAG dla nowych instalacji i odbiór 18 skilli."
---

# Wydanie 0.7.0

Zakres zatwierdzony 2026-11-02: nowe instalacje macOS/Windows/Linux, lokalny LanceDB + BGE-M3, bez migracji, harmonogramów i publikacji bez osobnej zgody.
Publiczne granice testów: CLI (index/rebuild/query/namespaces/status), MCP (rag_search/rag_namespaces), instalacja do nowego katalogu. Testy używają prawdziwego LanceDB i lokalnego serwera HTTP zastępującego wyłącznie endpoint embeddingów. Osobny test z prawdziwym BGE-M3 nie zastępuje testów instalacji na innych systemach.

- [x] T1 - Kontrakt i spis 18 skilli. Dowód: `docs/zgodnosc-skilli.md`. (Blokuje: T2, T3, T4)
- [x] T2 - Przenośny RAG, bezpieczny indeks przyrostowy i testy CLI/MCP. Dowód: 18 testów `test_rag.py` PASS (macOS, Python 3.13); 5 usterek niezależnego przeglądu naprawionych i pokrytych regresjami. (Zablokowane przez: T1) (Blokuje: T3, T4)
- [x] T3 - Nowa instalacja, model lokalny, konfiguracja MCP/CLI i onboarding. Dowód: świeża instalacja z osobnym venv i pip check PASS; 3 testy instalatora i rzeczywisty test BGE-M3 PL/EN PASS. (Zablokowane przez: T2) (Blokuje: T5)
- [x] T4 - Procedury 18 skilli i odświeżanie indeksu po zatwierdzonym zapisie. Dowód: niezależny przegląd wszystkich 18, poprawne YAML/nazwy i wspólna procedura; pełne wykonanie przez agentów pozostaje osobną bramką odbioru. (Zablokowane przez: T2) (Blokuje: T5)
- [ ] T5 - Częściowy odbiór: 29 testów macOS PASS, 28 Linux ARM64 Docker PASS, walidator i dokumentacja gotowe. Otwarte: natywny Windows/Linux z modelem i scenariusze klientów AI. (Zablokowane przez: T3, T4) (Blokuje: T6)
- [ ] T6 - Diff, raport i dokładny payload roboczego PR/About przygotowane. Wydanie wstrzymane do pełnego T5; commit, push, roboczy PR i About/topics zatwierdzone 2026-11-02. (Zablokowane przez: T5)

Commit/push/roboczy PR/zmiana About: zatwierdzone 2026-11-02. Merge/tag/pełne wydanie: niezatwierdzone. Nie zmieniać plików profilu ani wiedzy autora poza repozytorium dystrybucji.

## Dowody końcowe

- `docs/odbior-0.7.0.md`: komendy, wyniki, ograniczenia i bramki.
- `docs/publikacja-0.7.0.md`: dokładny payload roboczego PR oraz About/topics.
- `.aios/review/verification.json`: ignorowane lokalne logi końcowego odbioru macOS.
- `.aios/review/changes.patch`: ignorowany pełny diff źródeł do przeglądu.
- Linux Docker Python 3.11: świeża instalacja, 21 testów CLI/MCP/instalatora + 7 Backpass PASS; validator PASS. Python 3.13 również sprawdzony w poprzedniej iteracji.
- Przed zgodą użytkownika nie wykonano push/PR/zmiany About. Zatwierdzony zapis zewnętrzny w toku; merge/tag/pełne wydanie pozostają poza zakresem.
