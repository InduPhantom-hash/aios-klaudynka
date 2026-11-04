---
name: aios-dzien
description: >
  Briefing dnia: opcjonalny kalendarz + aktywne zadania z lokalnych plików projektów + sugestia priorytetu.
  Zasada Code Over AI - szybkie skanowanie lokalnych plików bez pożerania tokenów.
  Triggery: /aios:dzien, /aios-dzien, "co dziś mam", "plan na dziś", "co jest na kalendarzu".
---

# AIOS: Dzień

Użytkownik chce wiedzieć co ma dziś i od czego zacząć. Daj mu jeden zwięzły ekran - kalendarz + kontekst projektów + propozycja focusu.

## Krok 1: Pobierz dzisiejsze eventy ze wszystkich kalendarzy

1. Odkryj dostępną funkcję listowania kalendarzy i pobierz identyfikatory. Nie wymagaj stałego aliasu MCP; bez tej możliwości przejdź do lokalnych zadań.
2. Dla każdego `calendarId` wywołaj równolegle `list_events` z parametrami:
   - `startTime`: dziś 00:00:00 z offsetem strefy czasowej (np. `2026-07-27T00:00:00+02:00`)
   - `endTime`: dziś 23:59:59 z offsetem strefy
   - `timeZone`: strefa z `me.md` lub `Europe/Warsaw`
   - `orderBy`: startTime
3. Scal i posortuj chronologicznie wydarzenia. Zdeduplikuj powtórzenia.

Jeśli Calendar MCP jest niedostępny: napisz "Kalendarz niedostępny" i przejdź do skanowania zadań.

## Krok 2: Skanuj lokalne zadania (Code Over AI)

Odczytaj lokalne pliki zadań przez dostępne narzędzie plikowe lub wykonaj Python poniżej z korzenia vaulta. Działa również na natywnym Windows, bez bash i `grep`:

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path("_skrypty").resolve()))
from aios_rag.engine import Config, chunks
config = Config.load(Path("."))
for path in sorted(Path("Projekty").resolve().rglob("zadania.md")):
    if not config.allowed(path):
        continue
    text = path.read_text(encoding="utf-8")
    if not chunks(path.relative_to(config.vault).as_posix(), text):
        continue
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("- [ ]"):
            print(f"{path.as_posix()}:{number}: {line}")
```

Przed skanowaniem ogranicz katalogi zgodnie z `_skille/rag.md` i prywatnością użytkownika. Prywatne zadania odczytuj tylko przy prośbie obejmującej tę strefę; nie dodawaj ich proaktywnie do ogólnego briefingu.

Skompresuj odnalezione priorytetowe zadania z aktywnych projektów.

## Krok 3: Przedstaw briefing

Format:

```text
[Data, dzień tygodnia]

Kalendarz:
- HH:MM - HH:MM  Nazwa eventu [lokalizacja lub link]
(jeśli brak: "Brak eventów")

Zadania w projektach (AIOS Task Tracker):
- [Projekt A] Nazwa priorytetowego zadania
- [Projekt B] Nazwa priorytetowego zadania

Focus na dziś: [1 zdanie sugestii na podstawie kalendarza i zadań]
```

Bez ozdobników, bez "Witaj!", bez powitań. Używaj wyłącznie znaku `-` jako myślnika.

## Zgodność z lokalnym RAG

To procedura odczytowa: nie uruchamiaj `index` ani `rebuild` i nie zmieniaj konfiguracji. Odczytuj źródła z vaulta; dostępny lokalny RAG może pomóc znaleźć kontekst, lecz jego brak nie blokuje odczytu plików. Wczytaj `_skille/rag.md`, respektuj wykluczenia prywatności także bez RAG, a mechaniczny skan wykonuj przez narzędzie plikowe lub Python `pathlib`, również na Windows. Nazwy integracji MCP ustal z dostępnych capabilities.
