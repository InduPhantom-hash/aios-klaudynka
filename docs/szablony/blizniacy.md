# blizniacy.md - schemat bloku `## Blizniaki` w me.md

> **Dla AI-wykonawcy, nie dla usera.** Ten plik opisuje jak wygenerowac sekcje `## Blizniaki` w me.md na podstawie odpowiedzi E10-E13 z onboardingu. User tego pliku nie otwiera.

---

## Po co sekcja `## Blizniaki`?

Cztery skille czytaja te sekcje i na jej podstawie wiedza jak sie laczyc z zewnetrznymi systemami:

- `/aios:zadania` - tworzy zadania w task trackerze (E10-E11)
- `/aios:dzien` - pobiera wydarzenia z kalendarza (E13)
- `/aios-meta:synchronizuj` - porownuje vault z blizniakami (E10-E11)
- `/aios-meta:mcp-health` - sprawdza dostepnosc MCP serwisow (E10-E13)

Jezeli user pominal E10-E13 - sekcja nie powstaje, a skille dzialaja w trybie zdegradowanym (log lokalny bez zewnetrznych trackow).

---

## Kiedy generowac blok?

**Generuj `## Blizniaki`** w FIN1 (po skopiowaniu reszty me.md ze szablonu), jesli speliony jest conajmniej jeden z warunkow:
- E10 != zaden
- E12 = tak
- E13 = tak

**Pominij** (nie dodawaj pustego naglowka) jesli:
- E10 = zaden ORAZ E12 = nie (lub nie odpowiedziano) ORAZ E13 = nie (lub nie odpowiedziano)

---

## Schemat bloku

Wstaw blok po sekcji `## Rytm pracy` (lub po `## Prywatnosc` jesli istnieje), przed `## Metadane`.

```markdown
## Blizniaki

### Task tracker
- typ: $task_tracker_typ
<!-- Wartosci: clickup | linear | asana | notion | github | brak -->
<!-- Jesli typ = brak, pozostale pola tej podsekcji pominaj -->
- workspace: $tracker_workspace
<!-- URL workspace lub organizacji, np. https://app.clickup.com/12345 -->
- mapowanie kategoria -> lista:

| kategoria | lista / projekt |
|-----------|-----------------|
| $kategoria_1 | $lista_1 |
| $kategoria_2 | $lista_2 |
<!-- Wypelnij z E11. Jesli user nie podal mapowania - wstaw "(uzupelnij recznie)" w kolumnie lista / projekt -->
<!-- Kategorie = obszary z D1. Nie musisz miec mapowania dla wszystkich - tylko te ktore user podal -->

### Search & ingest
- tavily: $tavily_status
<!-- Wartosci: tak | nie -->
<!-- NIE przechowuj klucza API w me.md - tylko flage tak/nie -->

### Calendar
- google-calendar: $google_calendar_status
<!-- Wartosci: tak | nie -->
- strefa czasowa: $tz
<!-- Wartosci: skopiuj z A4 (np. Europe/Warsaw) -->

### MCP do monitorowania
- lista: [$mcp_lista]
<!-- Auto-generowana lista MCP na podstawie wszystkich E-odpowiedzi:
     - Jesli E5 = tak -> dodaj "pinecone"
     - Jesli E12 = tak -> dodaj "tavily"
     - Jesli E10 = clickup -> dodaj "clickup"
     - Jesli E10 = linear -> dodaj "linear"
     - Jesli E10 = asana -> dodaj "asana"
     - Jesli E10 = notion -> dodaj "notion"
     - Jesli E10 = github -> dodaj "github"
     - Jesli E13 = tak -> dodaj "google-calendar"
     Jesli lista pusta - wpisz [] -->
```

---

## Przyklad wypelnionego bloku (user: ClickUp + Tavily + Calendar)

```markdown
## Blizniaki

### Task tracker
- typ: clickup
- workspace: https://app.clickup.com/9012345
- mapowanie kategoria -> lista:

| kategoria | lista / projekt |
|-----------|-----------------|
| Marketing | (uzupelnij recznie) |
| Nauka | (uzupelnij recznie) |

### Search & ingest
- tavily: tak

### Calendar
- google-calendar: tak
- strefa czasowa: Europe/Warsaw

### MCP do monitorowania
- lista: [clickup, tavily, google-calendar]
```

---

## Przyklad - tylko Tavily, bez trackera i kalendarza

```markdown
## Blizniaki

### Task tracker
- typ: brak

### Search & ingest
- tavily: tak

### Calendar
- google-calendar: nie
- strefa czasowa: Europe/Warsaw

### MCP do monitorowania
- lista: [tavily]
```

---

## Uwagi dla AI-wykonawcy

1. **Kolejnosc podsekcji stala:** Task tracker -> Search & ingest -> Calendar -> MCP do monitorowania. Nie zmieniaj kolejnosci nawet jesli niektore sa "brak" / "nie".
2. **Typ brak w Task tracker** - wstaw podsekcje z samym "- typ: brak", reszta pol tej podsekcji pominaj (nie pisz pustych workspace: ani tabeli mapowania).
3. **Mapowanie "uzupelnij recznie"** - to jest normalne. User bedzie wiedzial co wpisac po konfiguracji swojego trackera. Nie blokuj onboardingu na brak list_id.
4. **Klucze API nigdy do me.md** - ani Tavily API key, ani ClickUp API token, ani Google Calendar credentials. me.md to plik tekstowy w vaulcie, moze byc synchronizowany (iCloud, GDrive) i widziany przez inne osoby. Klucze ida do konfiguracji klienta AI (`.claude/settings.json` lub odpowiednik).
5. **MCP lista** - sluzy skillowi `mcp-health` do sprawdzenia dostepnosci. Podaj nazwy zgodne z tym jak sa zarejestrowane w konfiguracji klienta AI usera (zazwyczaj to samo co nazwy serwisow lowercase).
6. **Komentarze HTML** - analogicznie jak w me-template.md, usun wszystkie komentarze `<!-- ... -->` przed zapisem finalnego pliku.
