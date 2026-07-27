# INSTALL.md - AIOS-Klaudynka v0.5.0

> **Ten dokument nie jest dla człowieka.** Jest pisany w trybie rozkazującym dla **AI-wykonawcy** (Claude Code, Cowork, Cursor, Codex, Gemini CLI, Antigravity), które instaluje AIOS-Klaudynkę w systemie użytkownika.
>
> Jeśli czytasz ten plik jako AI - jesteś adresatem. Wykonaj kroki po kolei, zadaj pytania userowi tylko tam gdzie to wskazano, oddaj kontrolę do `/aios:init` po skończonej instalacji.
>
> Jeśli czytasz ten plik jako człowiek - to nie dla ciebie. Wklej swojemu AI:
> `Zainstaluj mi AIOS-Klaudynkę z https://github.com/InduPhantom-hash/aios-klaudynka. Przeczytaj INSTALL.md i wykonaj kroki.`

---

## Zasady dla AI-wykonawcy

1. **Komunikuj się z userem po polsku.** Wszystkie komunikaty, pytania, raporty - po polsku.
2. **Używaj tylko łącznika `-`.** Nigdy `—` ani `–`. Dotyczy wszystkich wiadomości do usera i plików które tworzysz.
3. **Raportuj stan po każdym kroku.** User musi wiedzieć co się dzieje - jeden zwięzły komunikat po każdym kroku (co zrobione, co dalej).
4. **Pytaj tylko tam gdzie jest to oznaczone `[PYTANIE DO USERA]`.** Poza tymi miejscami nie przerywaj instalacji pytaniami.
5. **Przy błędach - zatrzymaj się i zdaj raport.** Nie próbuj naprawiać dziur w swoim rozumieniu. Powiedz userowi co się stało i jakie widzisz opcje.
6. **Na końcu oddaj kontrolę do `/aios:init`.** Instalacja kończy się tym, że user ma odpalony plugin i gotowość do onboardingu - nie kontynuuj dalej samodzielnie.

---

## Krok 0 - Wykrycie środowiska

**Cel:** ustalić na jakim systemie i w jakim AI działasz, żeby wybrać właściwą ścieżkę instalacji.

### 0.1 Wykryj OS

```bash
uname -a
```

Zapisz: `macOS` / `Linux` / `Windows` (pod WSL traktuj jako Linux, pod PowerShell jako Windows).

### 0.2 Ustal swój typ AI-wykonawcy

Nie możesz tego "wykryć" programistycznie - to jest informacja o tobie samym. Ustal:

- **Claude Code (CLI)** - masz dostęp do `/plugin marketplace` i `/plugin install` jako slash commands. **Ścieżka TESTED.**
- **Cowork (desktop app Claude)** - masz tool `request_cowork_directory`, narzędzia typu `mcp__cowork__*`, nie masz natywnego marketplace'u GitHub. **Ścieżka PARTIALLY TESTED.**
- **Cursor / Codex / Gemini CLI / inne** - masz dostęp do plików i shell, ale nie masz systemu pluginów Claude Code. **Ścieżka UNTESTED, tryb zdegradowany.**

Zapisz wybraną ścieżkę jako `$INSTALL_MODE`: `cc` / `cowork` / `degraded`.

### 0.3 Raport

Powiedz userowi co wykryłeś, np.:

> Wykryłem: macOS, Claude Code. Instaluję w trybie marketplace (ścieżka przetestowana). Jeśli to nie pasuje - powiedz.

**[PYTANIE DO USERA - tylko jeśli `$INSTALL_MODE = degraded`]:**

> Jestem w trybie zdegradowanym (nie Claude Code ani Cowork). Instalacja przejdzie, ale triggery `/aios:init` itd. nie zadziałają natywnie - będziesz musiał prosić mnie słownie ("wykonaj aios-init"). Kontynuować?

---

## Krok 1 - Warunki wstępne

**Cel:** user startuje "od zera" - zakładamy, że może mu brakować git albo nawet konta GitHub (nie jest potrzebne dla konsumenta publicznego repo). Wszystko co trzeba, doinstaluj.

### 1.1 Sprawdź `git`

```bash
git --version
```

Jeśli brak:

- **macOS:** `xcode-select --install` (to zainstaluje git razem z Command Line Tools).
- **Linux (Debian/Ubuntu):** `sudo apt-get install -y git`.
- **Linux (Fedora/RHEL):** `sudo dnf install -y git`.
- **Windows (PowerShell):** `winget install --id Git.Git -e`.

Jeśli instalacja wymaga sudo i nie masz uprawnień - **zatrzymaj się**, poproś usera o zainstalowanie git ręcznie i wznowienie po tym.

### 1.2 Sprawdź dostęp do `~/`

```bash
ls -la ~
```

Musisz móc czytać i pisać. Jeśli nie - zatrzymaj się, zgłoś problem.

### 1.3 Konto GitHub

**Nie jest wymagane** - pod warunkiem, że repo `aios-klaudynka` jest publiczne (tak jest w MVP). `git clone` bez auth.

Jeśli w trakcie Kroku 3.1 `git clone` prosi o login/hasło albo zwraca `Repository not found` - znaczy, że repo zostało przestawione na prywatne albo nie istnieje. **Zatrzymaj się**, zdaj raport userowi: trzeba albo dodać SSH key / token, albo poczekać aż autor wystawi repo publicznie.

### 1.4 Raport

> Git zainstalowany (wersja X.Y.Z). Gotowy do klonowania repo.

---

## Krok 2 - Lokalizacja vaulta

**Cel:** user wybiera gdzie ma mieszkać jego vault. Nie pytamy o lokalizację repo (repo ląduje w `/tmp/` i jest czyszczone).

### 2.1 Zaproponuj default

**[PYTANIE DO USERA]:**

> Gdzie ma być twój vault AIOS? Domyślnie: `~/Documents/AIOS-Vault/`. Możesz podać inną ścieżkę albo zatwierdzić default.

Zapisz odpowiedź jako `$VAULT_PATH`.

### 2.2 Sprawdź czy ścieżka jest wolna

```bash
ls -la $VAULT_PATH 2>/dev/null
```

Jeśli istnieje i ma zawartość - **[PYTANIE DO USERA]**:

> Ścieżka `$VAULT_PATH` już istnieje i zawiera pliki. Trzy opcje:
> 1. Wybierz inną ścieżkę
> 2. Wyczyść tę i nadpisz (destrukcyjne!)
> 3. Dołącz do istniejącej (tylko jeśli to inny vault AIOS i wiesz co robisz)

Nie kontynuuj bez jednoznacznej odpowiedzi.

#### 2.2 - obsługa wyborów

**Licznik prób:** trzymaj `$RETRY_COUNT` (start: 0). Jeśli dojdzie do 3, przerwij instalację i zgłoś userowi: "Trzy razy trafiłem na zajętą ścieżkę - zakończ inne programy używające tych katalogów albo wskaż czystą lokalizację i uruchom instalację ponownie." Nie pętluj dalej.

**Opcja (1) - nowa ścieżka:**

> [PYTANIE DO USERA]: Podaj nową ścieżkę dla vaulta.

Inkrementuj `$RETRY_COUNT`, zapisz nową wartość jako `$VAULT_PATH`, wróć do 2.2 (sprawdzenie `ls -la $VAULT_PATH`).

**Opcja (2) - wyczyść i nadpisz:**

> [PYTANIE DO USERA - double-opt-in]: To usunie wszystko w `$VAULT_PATH` wraz z plikami ukrytymi (`.git`, `.claude` itd.). Napisz `TAK, USUŃ` (dokładnie te słowa) żeby kontynuować.

Jeśli odpowiedź nie jest dokładnie `TAK, USUŃ` - traktuj jako anulowanie, wróć do pytania z 2.2 ("Trzy opcje...").

Jeśli potwierdzone:

```bash
find $VAULT_PATH -mindepth 1 -delete
```

(Patrz Troubleshooting: "Vault zawiera już pliki" - dlaczego nie `rm -rf $VAULT_PATH/*`.)

Po usunięciu przejdź do 2.3.

**Opcja (3) - dołącz do istniejącej:**

Zweryfikuj że to faktycznie vault AIOS - sprawdź obecność `me.md` LUB `_pamiec/` LUB `CLAUDE.md`:

```bash
ls $VAULT_PATH/me.md $VAULT_PATH/_pamiec $VAULT_PATH/CLAUDE.md 2>/dev/null
```

Jeśli żaden z tych markerów nie istnieje - zatrzymaj się, zgłoś: "`$VAULT_PATH` nie wygląda na vault AIOS (brak `me.md`, `_pamiec/`, `CLAUDE.md`). Wybierz opcję 1 albo 2."

Jeśli markery są - pomiń 2.3 (katalog istnieje), ale zmień tryb kopiowania w Kroku 3.3 na **no-overwrite**:

```bash
cp -Rn /tmp/aios-klaudynka/vault-template/. $VAULT_PATH/
```

Flaga `-n` (macOS/BSD i GNU) zapobiega nadpisywaniu istniejących plików. Użytkownik zachowa swoją zawartość, a szablon dopełni tylko brakujące katalogi.

### 2.3 Stwórz katalog (jeśli nie istnieje)

```bash
mkdir -p $VAULT_PATH
```

### 2.4 Raport

> Vault będzie w: `$VAULT_PATH`. Następny krok: pobieram szablon vaulta z GitHuba.

---

## Krok 3 - Pobranie i rozłożenie vault-template

**Cel:** sklonować repo do `/tmp/`, przekopiować `vault-template/` do lokalizacji usera, wyczyścić `/tmp/`.

### 3.1 Klon

```bash
git clone https://github.com/InduPhantom-hash/aios-klaudynka.git /tmp/aios-klaudynka
```

Jeśli `/tmp/aios-klaudynka` już istnieje - usuń najpierw (`rm -rf /tmp/aios-klaudynka`).

### 3.2 Weryfikacja struktury repo

Po klonowaniu sprawdź że istnieją:

- `/tmp/aios-klaudynka/.claude-plugin/marketplace.json`
- `/tmp/aios-klaudynka/plugins/aios/.claude-plugin/plugin.json`
- `/tmp/aios-klaudynka/vault-template/` (katalog)

Jeśli czegoś brakuje - zatrzymaj się, zdaj raport userowi. Repo jest uszkodzone albo klonowanie się nie powiodło.

### 3.3 Kopia vault-template

```bash
cp -R /tmp/aios-klaudynka/vault-template/. $VAULT_PATH/
```

Kropka na końcu source jest świadoma - kopiuje zawartość, nie sam katalog.

### 3.4 Weryfikacja

Sprawdź że w `$VAULT_PATH` istnieją (szablonowe):

- `CLAUDE.md`
- `me.md`
- `_inbox/`
- `_brudnopis/`
- `_pamiec/`
- `_Archiwum/`
- `Kosz/`
- `Projekty/`
- `Wiedza/`
- `Kalendarz/`

Jeśli czegoś brakuje - zatrzymaj się, zdaj raport.

### 3.5 Raport

> Vault rozłożony w `$VAULT_PATH`. Struktura kompletna. Następny krok: instalacja plugina `aios`.

---

## Krok 4 - Instalacja plugina (w zależności od `$INSTALL_MODE`)

### 4A - Claude Code (`$INSTALL_MODE = cc`) - TESTED

To jest natywna ścieżka. Claude Code sam obsłuży kopiowanie pluginu do swojego cache.

**4A.1** W sesji Claude Code wykonaj:

```
/plugin marketplace add InduPhantom-hash/aios-klaudynka
```

Claude Code pobierze `marketplace.json` z repo i zarejestruje marketplace pod nazwą `aios-klaudynka`.

**Fallback na pełny URL.** Jeśli format `owner/repo` zwróci błąd (niektóre wersje CC, fork z zmienionym ownerem, rename), spróbuj:

```
/plugin marketplace add https://github.com/InduPhantom-hash/aios-klaudynka
```

Pełny URL jest jednoznaczny i odporny na zmiany właściciela.

**4A.2** Zainstaluj plugin:

```
/plugin install aios@aios-klaudynka
```

Claude Code pobierze katalog `plugins/aios/` z marketplace i skopiuje do swojego cache (`~/.claude/plugins/cache/` lub podobnie - to jego sprawa, nie twoja).

**4A.3** Weryfikacja:

```
/plugin list
```

Output jest strukturalny - szukaj w nim ciągu `aios` (albo `aios@aios-klaudynka`). Jeśli plugin jest na liście i status to `enabled` / `active` - weryfikacja OK.

Dodatkowo (smoke-test namespace'u slash-commandów):

```
/aios:init --dry-run
```

Jeśli Claude Code rozpoznaje komendę (choćby zwraca "unknown flag" zamiast "unknown command") - skille są załadowane. Jeśli zwraca "unknown command" albo podobny błąd - plugin jest zainstalowany, ale skille się nie wczytały. Zdaj raport, patrz **Troubleshooting**.

Nie polegaj na `/help` - output tej komendy bywa niestrukturalny i łatwo uznać "widzę komendy" bez realnej weryfikacji.

---

### 4B - Cowork (`$INSTALL_MODE = cowork`) - PARTIALLY TESTED

Cowork nie czyta marketplace'ów GitHub natywnie. Plugin musisz przygotować jako plik `.plugin` (zip) i kazać userowi wgrać ręcznie.

**4B.1** Zbuduj `.plugin` zip:

```bash
cd /tmp/aios-klaudynka/plugins/aios
zip -r /tmp/aios.plugin .
```

Sprawdź że plik powstał: `ls -la /tmp/aios.plugin`.

**4B.2** Przenieś plik w miejsce gdzie user go znajdzie:

```bash
cp /tmp/aios.plugin $VAULT_PATH/aios.plugin
```

(Leży obok vaulta - user go widzi w swoim Finderze/Explorerze.)

**4B.3** **[PYTANIE DO USERA - krok manualny]**:

> Zbudowałem plugin jako `$VAULT_PATH/aios.plugin`. Teraz musisz go wgrać do Coworka ręcznie.
>
> Cowork to research preview i dokładna ścieżka w UI zmienia się między wersjami - zwykle coś w okolicach Settings / Plugins / Upload albo "My Uploads". Jeśli w swojej wersji nie widzisz opcji uploadu `.plugin` - sprawdź aktualną dokumentację Anthropic (docs.claude.com) albo daj znać, opiszę to inaczej.
>
> Po wgraniu pluginu zrestartuj sesję Coworka (nowe skille potrzebują świeżej sesji) i napisz "gotowe".

**4B.4** Po potwierdzeniu - poproś o weryfikację:

> Spróbuj wpisać `/aios:init`. Czy Cowork rozpoznaje tę komendę?

Jeśli nie - zdaj raport, patrz **Troubleshooting**.

---

### 4C - Tryb zdegradowany (`$INSTALL_MODE = degraded`) - UNTESTED

Nie masz native plugin systemu. Skille skopiujemy do `_skille/aios/` wewnątrz vaulta - niektóre AI je znajdą, niektóre nie. Triggery slash-commandowe nie zadziałają - trzeba wywoływać słownie.

**Dlaczego `_skille/aios/`, nie `.claude/plugins/aios/`:** prefix `_` jest spójny z konwencją AIOS (`_inbox/`, `_pamiec/`, `_brudnopis/`, `_Archiwum/`) i jawnie wyodrębnia katalog skilli dla użytkownika, który przegląda vault w Finderze. Dodatkowo unikamy kolizji z Claude Code, który skanując current dir traktuje `.claude/` jako global settings - to mogłoby dać nieprzewidywalne zachowanie u usera mieszającego narzędzia.

**4C.1** Stwórz katalog:

```bash
mkdir -p $VAULT_PATH/_skille/aios
```

**4C.2** Skopiuj plugin:

```bash
cp -R /tmp/aios-klaudynka/plugins/aios/. $VAULT_PATH/_skille/aios/
```

**4C.3** Weryfikacja - sprawdź że istnieje:

- `$VAULT_PATH/_skille/aios/.claude-plugin/plugin.json`
- `$VAULT_PATH/_skille/aios/skills/init/SKILL.md`

**4C.4** **[KOMUNIKAT DO USERA]**:

> Zainstalowałem skille w trybie zdegradowanym - są w `$VAULT_PATH/_skille/aios/`. Twoje AI prawdopodobnie nie rozpozna triggerów `/aios:init` ani podobnych. Żeby uruchomić onboarding, napisz do mnie: **"wykonaj aios-init"** albo **"przeczytaj SKILL.md z `_skille/aios/skills/init/` i wykonaj"**. Tak samo dla pozostałych 5 skilli.

---

## Krok 4.5 - Instalacja plugina `aios-meta` (opcjonalna)

**Cel:** zainstalować opcjonalny plugin `aios-meta` (higiena vaulta, MCP health, synchronizacja z narzędziami zewnętrznymi). Możesz to zrobić teraz albo wrócić do tego później - plugin jest niezależny od `aios` i od vault template.

**Kiedy instalować:** jeśli user używa co najmniej jednego "bliźniaka" (ClickUp, Linear, Notion, Airtable, Miro) albo chce audytować strukturę swojego vaulta. Jeśli użytkownik nie wie co to jest - pomiń ten krok i wróć do niego po zakończeniu onboardingu.

### 4.5A - Claude Code (`$INSTALL_MODE = cc`)

```
/plugin install aios-meta@aios-klaudynka
```

Weryfikacja:

```
/plugin list
```

Szukaj `aios-meta` na liście ze statusem `enabled` / `active`.

### 4.5B - Cowork (`$INSTALL_MODE = cowork`)

**4.5B.1** Zbuduj `.plugin` zip dla `aios-meta`:

```bash
cd /tmp/aios-klaudynka/plugins/aios-meta
zip -r /tmp/aios-meta.plugin .
```

Sprawdź że plik powstał: `ls -la /tmp/aios-meta.plugin`.

**4.5B.2** Przenieś plik w miejsce gdzie user go znajdzie:

```bash
cp /tmp/aios-meta.plugin $VAULT_PATH/aios-meta.plugin
```

**4.5B.3** **[PYTANIE DO USERA - krok manualny]**:

> Zbudowałem plugin `aios-meta` jako `$VAULT_PATH/aios-meta.plugin`. Wgraj go do Coworka tak samo jak plugin `aios` (Settings / Plugins / Upload albo podobne miejsce). Po wgraniu zrestartuj sesję i napisz "gotowe".

**4.5B.4** Po potwierdzeniu - weryfikacja:

> Spróbuj wpisać `/aios-meta:audyt-luk`. Czy Cowork rozpoznaje komendę?

### 4.5C - Tryb zdegradowany (`$INSTALL_MODE = degraded`)

```bash
mkdir -p $VAULT_PATH/_skille/aios-meta
cp -R /tmp/aios-klaudynka/plugins/aios-meta/. $VAULT_PATH/_skille/aios-meta/
```

Skille dostępne przez słowne wywołanie: "wykonaj aios-meta:audyt-luk" albo "przeczytaj SKILL.md z `_skille/aios-meta/skills/audyt-luk/` i wykonaj".

---

## Krok 5 - Uruchomienie onboardingu

**Cel:** oddać kontrolę do `/aios:init`, który poprowadzi ankietę do 61 pytań i wygeneruje `me.md` + konfigurację vaulta.

### 5.0 Smoke-test skilla (zanim oddasz kontrolę)

Zanim pokażesz userowi `/aios:init`, zweryfikuj że skill jest realnie załadowany - nie tylko że plugin jest w cache'u. W CC/Cowork wywołaj:

```
/aios:init --dry-run
```

Jeśli skill odpowiada (choćby błędem "unknown flag" albo powitaniem onboardingu bez startu ankiety) - OK. Jeśli zwraca "unknown command" - wróć do 4A.3 / 4B.4, plugin nie jest aktywny mimo że instalacja przeszła.

W trybie zdegradowanym pomiń ten krok - user wywoła skill słownie.

### 5.1 Claude Code / Cowork (plugin zainstalowany)

**[KOMUNIKAT DO USERA]**:

> Instalacja skończona. Teraz odpal: `/aios:init`. To jest ankieta onboardingowa (10 sekcji, do 61 pytań, około 30-45 min). Wygeneruje twój `me.md` i dostosuje strukturę vaulta. Możesz to zrobić teraz albo kiedy indziej - do momentu wykonania init, vault stoi w stanie szablonowym.

Nie wywołuj `/aios:init` za usera - to jego decyzja kiedy startuje.

### 5.2 Tryb zdegradowany

**[KOMUNIKAT DO USERA]**:

> Instalacja skończona. Kiedy chcesz przejść onboarding, napisz mi: **"wykonaj aios-init"**. Wtedy przeczytam `SKILL.md` z `_skille/aios/skills/init/` i poprowadzę cię przez ankietę. Ankieta ma 10 sekcji i do 61 pytań, zajmuje 30-45 min.

---

## Krok 6 - Sprzątanie

**Cel:** usunąć tymczasowe klony i zipy z `/tmp/`.

### 6.1

```bash
rm -rf /tmp/aios-klaudynka
rm -f /tmp/aios.plugin
```

(Drugie polecenie dotyczy tylko trybu Cowork, ale bezpieczne do wywołania zawsze - `-f` nie dławi się na braku pliku.)

### 6.2 Raport końcowy

> Gotowe. Sprzątnąłem pliki tymczasowe. Twój vault jest w `$VAULT_PATH`, plugin zainstalowany ($INSTALL_MODE). Żeby zacząć - odpal `/aios:init` (lub powiedz mi "wykonaj aios-init" w trybie zdegradowanym).

---

## Troubleshooting

### `/plugin marketplace add` zwraca błąd "invalid marketplace"

Sprawdź czy `marketplace.json` w repo ma poprawną strukturę - pole `name`, `owner`, lista `plugins[]` z pełnymi wpisami. Jeśli repo się niedawno zmieniło, user może mieć zcachowaną starą wersję - `/plugin marketplace remove aios-klaudynka` i ponów.

### `/plugin install aios@aios-klaudynka` - "plugin not found"

Najpierw sprawdź: `/plugin marketplace list`. Czy `aios-klaudynka` w nim jest? Jeśli nie - poprzedni krok się nie powiódł, wróć do 4A.1.

Jeśli jest - sprawdź w repo `plugins/aios/.claude-plugin/plugin.json`. Czy pole `name` to faktycznie `"aios"`? Jeśli w manifeście jest coś innego (np. `"aios-klaudynka"`), to `/plugin install aios@...` nie znajdzie. Wtedy: zainstaluj używając nazwy z manifestu, ALBO popraw manifest w repo i zcommituj (tylko ścieżka dev).

### Plugin `aios` już istnieje (konflikt z inną instalacją)

**Komu dotyczy:** głównie autorowi AIOS-Klaudynki, który może mieć na tej samej maszynie prywatnego plugina `aios` z wcześniejszych iteracji (v1.x / v2.x). Publiczny user instalujący z zera nie trafi na to - ten plugin jest pierwszym o tej nazwie w jego środowisku.

**Objawy:** `/plugin install aios@aios-klaudynka` kończy się błędem "plugin already installed" / "conflict". Alternatywnie: instalacja przechodzi, ale `/aios:init` dalej uruchamia starą wersję i nie widać różnic z nowego marketplace'u.

**Fix:**

1. `/plugin list` - zobacz z jakiego marketplace'u pochodzi aktywny plugin `aios`.
2. `/plugin uninstall aios` - odinstaluj starą wersję.
3. Wróć do 4A.2 i zainstaluj `aios@aios-klaudynka`.

Nie próbuj trzymać obu na raz - namespace slash-commandów (`/aios:*`) jest współdzielony i nie ma przewidywalnego pierwszeństwa.

### Cowork: "plugin upload failed" albo brak opcji uploadu

Najpierw sprawdź że `.plugin` to poprawny zip (`unzip -l /tmp/aios.plugin` - musi pokazać pliki zaczynające się od `.claude-plugin/plugin.json`, `skills/init/SKILL.md` itd., BEZ prefiksu `aios/`). Jeśli jest prefix `aios/` - znaczy że zipowałeś katalog nadrzędny, nie zawartość. Powtórz 4B.1 z `cd .../plugins/aios/` przed `zip -r ... .` (kropka = zawartość current dir).

Jeśli zip jest poprawny a Cowork i tak nie pozwala wgrać - możliwe że w tej wersji Coworka opcja uploadu `.plugin` jest w innym miejscu UI albo została wycofana. Zapytaj usera jaką wersję ma i sprawdź aktualną dokumentację (`docs.claude.com`). Jako fallback - przejdź na tryb zdegradowany (4C): skopiuj rozpakowany plugin do `$VAULT_PATH/_skille/aios/` i dalej pracujcie słownie.

### Tryb zdegradowany: AI "nie widzi" skilli

AI w trybie zdegradowanym nie ma mechanizmu auto-loading skilli z `_skille/`. Trzeba mu wskazać konkretny plik. Zamiast "wykonaj aios-init" próbuj dokładniej: "przeczytaj `$VAULT_PATH/_skille/aios/skills/init/SKILL.md` i wykonaj instrukcje w nim zawarte".

### Git clone fails z "permission denied"

Sprawdź czy masz dostęp sieciowy do `github.com` (niektóre korporacyjne proxy blokują). Jeśli tak - user musi skonfigurować proxy albo zmienić sieć. Nie próbuj obejść - zgłoś jasno.

### Vault zawiera już pliki (konflikt w 2.2)

Nigdy nie nadpisuj milcząco. Jeśli user wybrał "wyczyść i nadpisz" w 2.2 - **najpierw powtórz ostrzeżenie i poproś o ponowne potwierdzenie (double-opt-in, dokładnie `TAK, USUŃ`)**. Destrukcyjne operacje wymagają podwójnego "tak".

Polecenie czyszczenia:

```bash
find $VAULT_PATH -mindepth 1 -delete
```

**Dlaczego `find`, nie `rm -rf $VAULT_PATH/*`:** glob `*` w bashu pomija pliki ukryte (`.git`, `.claude`, `.gitignore`). Jeśli po poprzedniej próbie instalacji zostały takie śmieci, `rm -rf *` by ich nie usunął i kolejny `git clone`/`cp` zderzyłby się z nieusuwalnymi artefaktami. `find -mindepth 1 -delete` usuwa wszystko poniżej `$VAULT_PATH` (łącznie z ukrytymi), ale zachowuje sam katalog - więc nie trzeba go potem odtwarzać.

Alternatywa jeśli `find` nie jest dostępny (rzadkie - zwykle minimalne kontenery): `rm -rf "$VAULT_PATH"/{.[!.],}*` - glob obejmuje też ukryte.

---

## Aktualizacja do nowszej wersji

**MVP (v0.3):** mechanizmu "upgrade in place" nie ma. Jeśli autor wypuszcza nową wersję pluginu:

### Claude Code

```
/plugin uninstall aios
/plugin marketplace update aios-klaudynka
/plugin install aios@aios-klaudynka
```

`/plugin marketplace update` odświeży lokalny cache `marketplace.json`. Reinstall pobierze aktualną wersję pluginu.

### Cowork

Usuń stary plugin w UI Coworka (Settings / Plugins / My Uploads) i wgraj nowy `.plugin` zip zbudowany z aktualnego repo.

### Tryb zdegradowany

```bash
rm -rf $VAULT_PATH/_skille/aios
cd /tmp && rm -rf aios-klaudynka && git clone https://github.com/InduPhantom-hash/aios-klaudynka.git
cp -R /tmp/aios-klaudynka/plugins/aios/. $VAULT_PATH/_skille/aios/
```

### Vault użytkownika

Vault (`$VAULT_PATH`) jest nietykany przez upgrade - zmiany w szablonie `vault-template/` nie są retroaktywnie aplikowane u użytkownika (File Over AI: twój vault to twój vault). Jeśli nowa wersja wprowadza nowy katalog (np. `Kalendarz/` w v0.3), dopisz go sobie ręcznie albo poproś AI o `mkdir -p $VAULT_PATH/<nowy-katalog>`.

Release notes przy każdej wersji będą jawnie wymieniać zmiany w `vault-template/`, żeby dało się je zaaplikować selektywnie.

---

## Checkpoint końcowy

Po wykonaniu wszystkich kroków user powinien mieć:

1. Katalog `$VAULT_PATH` ze szablonową strukturą AIOS.
2. Plugin `aios` zainstalowany (CC: w cache; Cowork: przez UI; degraded: w `_skille/aios/`).
3. Opcjonalnie: plugin `aios-meta` zainstalowany (krok 4.5).
4. Wyczyszczone `/tmp/`.
5. Wiedzę że następny krok to `/aios:init` (albo zdegradowany odpowiednik).

Jeśli którykolwiek z tych punktów nie jest spełniony - **nie raportuj "gotowe"**. Zamiast tego powiedz userowi co nie wyszło i co trzeba zrobić.

---

## Metadane

- **Wersja dokumentu:** v0.4 (beta - dodana sekcja 4.5 dla aios-meta, bump wersji)
- **Ostatnia aktualizacja:** 2026-04-25
- **Zastępuje:** `Raw/INSTALL-v01.md` (deprecated - pisany na błędnych założeniach o mechanizmie instalacji pluginów). Wersja v0.2 była draftem przejściowym bez fixów z review.
- **Zakłada:** repo `aios-klaudynka` jest publiczne na GitHubie. Prywatne repo wymaga dodatkowych kroków (SSH key / token) nieobjętych tym dokumentem.
- **Status ścieżek:**
  - CC (4A, 4.5A) - TESTED
  - Cowork (4B, 4.5B) - PARTIALLY TESTED
  - Degraded (4C, 4.5C) - UNTESTED
- **Target:** macOS + Claude Code + user od zera. Reszta - best effort bez gwarancji.
- **Changelog:**
  - v0.4 (2026-04-25) - dodana sekcja 4.5 (instalacja aios-meta), zaktualizowany checkpoint, bump wersji.
  - v0.3 (2026-04-22) - MVP. K1 (flow 2.2), K2 (find zamiast rm *), K3 (jawność public repo), W1 (`/plugin list`), W2 (`_skille/aios/` zamiast `.claude/plugins/aios/`), W3 (fallback URL), W4 (sekcja Aktualizacja), M2 (smoke-test skilla), M1 (data). 57 pytań (poprzednio 55).
  - v0.2 (2026-04-21) - draft z poprawną architekturą marketplace-based, przed review.
  - v0.1 (2026-04-20) - deprecated, błędne założenia o `cp -R` do `~/.claude/plugins/`.
