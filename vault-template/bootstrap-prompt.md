# AIOS Bootstrap Prompt

Gdy rozpoczynasz nową sesję z AI (np. w Cursorze, Gemini CLI, LM Studio, OpenHand, Antigravity lub Claude Code bez automatycznego wczytywania system promptów), skopiuj i wklej poniższy prompt:

```text
Cześć! Działamy w systemie AIOS (File Over AI, Code Over AI).
Przed podjęciem jakichkolwiek działań wczytaj pliki konfiguracyjne z korzenia vaulta w tej kolejności:
1. me.md (profil użytkownika i zasady komunikacji)
2. AGENTS.md (zasady operacyjne i defensywne wykonywanie zadań)
3. _pamiec/aktualny.md (jeśli istnieje - stan ostatniej sesji)
4. vault-map.md (jeśli istnieje - nawigacja)

Przy pytaniu o wiedzę lub decyzje wczytaj _skille/rag.md. Użyj lokalnego rag_search/rag_namespaces dostępnego w runtime, a bez MCP - CLI _skrypty/aios-rag.py przez interpreter tego vaulta (.venv/bin/python na macOS/Linux, .venv/Scripts/python.exe na Windows). --vault podawaj przed poleceniem. Przy braku modelu lub nieaktualnym indeksie zgłoś stan i czytaj pliki; nie przełączaj embeddingów na chmurę. Respektuj _config/rag.json i prywatność notatek również w fallbacku.

Bez natywnych slash commands czytaj procedury z _skille/aios/skills/<nazwa>/SKILL.md. Po zatwierdzonej partii zapisów odśwież lokalny indeks według _skille/rag.md; same odczyty nie uruchamiają indeksowania.

Potwierdź wczytanie jedną zwięzłą linią i podaj gotowość do pracy.
```
