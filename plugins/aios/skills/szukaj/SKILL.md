---
name: szukaj
description: Hierarchiczne wyszukiwanie w vault AIOS. Warstwa 1 - nawigacja po index.md od ogolu do szczegolu. Warstwa 2 - Pinecone przez MCP jesli lokalnie nie znaleziono. Triggery - "/aios:szukaj", "znajdz cos o X", "wyszukaj w wiedzy", "co mam w vaulcie o...", "semantic search".
---

# szukaj

Szukasz w vaulcie usera (ścieżka zdefiniowana w `me.md` jako `$VAULT_PATH`). **Filozofia:** hierarchia `index.md`
od ogolu do szczegolu jest tansza, bardziej przewidywalna i ADHD-friendly niz Pinecone.
Pinecone (przez MCP) wchodzi dopiero gdy hierarchia zawiedzie.

## Filozofia (dlaczego hierarchia > Pinecone)

Pinecone jest dokladniejszy dla fuzzy/semantycznych zapytan, ale drozszy w tokenach
i nieprzewidywalny. Hierarchia `index.md` jest:
- **tansza** (AI czyta 3-5 malych plikow zamiast generowac embedding + query),
- **przewidywalna** (AI nawiguje jak czlowiek w eksploratorze),
- **ADHD-friendly** (zawsze wiesz gdzie jestes i co jest obok).

Pinecone wchodzi dopiero gdy **hierarchia zawiodla** - np. pytanie jest bardzo
luzne semantyczne ("jakies przemyslenia o motywacji") albo AI nie zna obszaru.

## Input

- `<query>` - pytanie naturalnym jezykiem lub fraza
- (opcjonalnie) `--pinecone` - pomin hierarchie, od razu Pinecone
- (opcjonalnie) `--tylko-hierarchia` - pomin Pinecone, tylko lokalnie
- (opcjonalnie) `--projekt <nazwa>` - zaweznie do konkretnego projektu
- (opcjonalnie) `--top N` - liczba wynikow (default 5)

## Procedura - warstwa 1 (hierarchia)

### Krok 1: Klasyfikuj zapytanie

Zdecyduj do ktorego korzenia nawigowac:
- **"O mnie, profil, zasady, HARD RULES"** -> `me.md`
- **"Stan systemu, decyzje, pamiec"** -> `_pamiec/DREAM.md`
- **"O jakims projekcie"** -> `Projekty/index.md` -> `Projekty/<kat>/index.md` -> konkretny projekt
- **"Teoria, metoda, narzedzie"** -> `Wiedza/index.md` -> `Wiedza/<obszar>/Wiki/index.md`
- **"Kalendarz, deadline"** -> `Kalendarz/`
- **"Ostatnia sesja, co robilismy"** -> `_brudnopis/` (po dacie) + `_pamiec/aktualny.md`
- **"Skille, jak cos dziala w AIOS"** -> `_skille/<skill>.md`
- **Nie wiem** -> `vault-map.md` (mapa korzenia)

### Krok 2: Czytaj index.md w odpowiedniej sekcji

Zawsze od ogolu do szczegolu. Przyklad:
```
query: "jak dziala Karpathy wiki method"
-> vault-map.md (mapa) mowi ze AI = Wiedza/AI/
-> Wiedza/index.md (potwierdza obszar AI)
-> Wiedza/AI/Wiki/index.md (lista stron Wiki)
-> tam znajdujesz link do [[karpathy-wiki-method]]
-> czytasz konkretna strone
```

### Krok 3: Zwroc wynik

Jesli znalazles - pokaz sciezke nawigacji + cytat:

```
## Wynik (warstwa 1 - hierarchia)

Sciezka: vault-map -> Wiedza/index -> Wiedza/AI/Wiki/index -> [[karpathy-wiki-method]]
Cytat: "Karpathy wiki method polega na..."
Link: [[Wiedza/AI/Wiki/karpathy-wiki-method.md]]
Powiazane: [[llm-wiki-intro]], [[raw-wiki-workflow]]
```

### Krok 4: Jesli nie znalazles

Idz do warstwy 2 (Pinecone MCP).

## Procedura - warstwa 2 (Pinecone fallback)

Wywolaj tylko jesli warstwa 1 zawiodla (lub user podal `--pinecone`).

### Wymaganie

Pinecone MCP musi byc zainstalowany w Claude (serwer: `pinecone`, pakiet `@pinecone-database/mcp`).
Index `aios`, model `multilingual-e5-large` (integrated embedding, pole `text`).

Jesli MCP niedostepny - powiedz **explicite**: "Pinecone MCP niedostepny.
Sproboj przeladowac lub dokonac wyboru sciezki recznie."

### Krok 1: Wywolaj narzedzie `search-records`

Narzedzie MCP: **`search-records`** (z serwera `pinecone`)

Parametry:
```
indexName: "aios"
query: <query naturalnym jezykiem>
topK: 5 (default, uzyj --top N jesli podane)
namespace: zaleznie od klasyfikacji:
  - Wiedza/AI/*          -> "wiedza-ai"
  - Wiedza/Marketing/*   -> "wiedza-marketing"
  - Wiedza/Programming/* -> "wiedza-programming"
  - Wiedza/Biblioteka/*  -> "wiedza-biblioteka"
  - Projekty/Praca/*     -> "projekty-praca"
  - Projekty/Vibe-coding -> "projekty-vibe"
  - Projekty/Hobby/*     -> "projekty-hobby"
  - Projekty/Prywatne/*  -> "projekty-prywatne"
  - Projekty/Nauka/*     -> "projekty-nauka"
  - me.md, DREAM, mapa   -> "fundament"
  - _brudnopis/*, aktualny.md -> "brudnopis" / "pamiec"
  - _skille/*            -> "skille"
  - nie wiadomo          -> pominac namespace (search all)
```

### Krok 2: Zwroc wynik

```
## Wynik (warstwa 2 - Pinecone)

Uwaga: warstwa 1 (hierarchia) nie znalazla. Uzyto Pinecone MCP.

1. [[Wiedza/AI/Wiki/karpathy-wiki-method.md]]
   Score: 0.82  Namespace: wiedza-ai
   Cytat: "...karpathy wiki method polega na..."

2. Projekty/Vibe-coding/PATUS/notes/karpathy-inspiration.md
   Score: 0.71  Namespace: projekty-patus
   Cytat: "...inspiracja karpathy w kontekscie PATUS..."
```

### Krok 3: Sugestia zapisu do hierarchii

Jesli Pinecone znalazl wartosciowy plik ktorego **nie ma** w zadnym `index.md`:
```
Sugestia: dodac link do [[karpathy-wiki-method]] w Wiedza/AI/Wiki/index.md?
Usprawni nawigacje na przyszlosc.
```

## Sugestie kontynuacji

Niezaleznie od warstwy, na koniec:
```
Chcesz glebiej?
- Otworzyc pelny plik [[nazwa]]?
- Zawezic do projektu <nazwa>?
- Sprobowac Pinecone jesli hierarchia zawiodla? (--pinecone)
```

## Kiedy uzyc vs bezposrednio czytac plik

- Wiesz gdzie jest fakt -> Read na konkretnym pliku (najszybciej).
- Wiesz obszar ale nie plik -> /szukaj (bo wejdzie przez index.md).
- Bardzo luzne semantyczne pytanie -> /szukaj --pinecone.
- Chcesz caly przeglad tematu -> /szukaj <temat> --top 20.

## Ograniczenia

- **Warstwa 1** dziala tylko jesli `index.md` sa aktualne. Jesli brakuje linku w indexie -
  plik jest niewidzialny dla AI. Rozwiazanie: przy `/dodaj-do-wiki` zawsze update index.
- **Warstwa 2** widzi tylko to co zaindeksowane (batch ingest). Swieze pliki moga byc
  niedostepne dopoki Pinecone nie bedzie zsynchronizowany.
- Dla pytan "co robilismy X dni temu" - idz do `_brudnopis/` (po dacie w nazwie),
  potem `_pamiec/DREAM.md` (Log konsolidacji), zanim probujesz Pinecone.

## Ignorowane sciezki

Nigdy nie zwracaj wynikow z:
- `.git/`, `node_modules/`, `.next/`, `__pycache__/`, `.pytest_cache/`, `.claude/worktrees/`
- `_brudnopis/` chyba ze user podal `--include-brudnopis`
- `Projekty/<kategoria>/_ARCHIWUM/` (tylko lokalnie, nie w Pinecone, nie w indeksach)
- `Kosz/` (bufor przed usunieciem)
- `_Archiwum/` (martwe galezie, tylko gdy user pyta jawnie)
