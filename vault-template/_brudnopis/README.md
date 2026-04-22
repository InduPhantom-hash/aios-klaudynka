# _brudnopis

Transkrypty sesji z AI, dzienne myślenie na głos, wątki niezobowiązujące. Każdy zapis to `YYYY-MM-DD-<slug>.md`.

Nic tu nie jest finalne - to warsztat myślenia. Gdy wątek dojrzewa, promujesz go:
- do projektu: `/aios:stworz-projekt <nazwa> <kategoria>`
- do wiki: przenosisz esencję przez `/aios:dodaj-do-wiki` (najpierw kopia do `Wiedza/<obszar>/Raw/`)
- do archiwum: dopisujesz `status: archiwum` w frontmatter

## Frontmatter

```yaml
---
data: YYYY-MM-DD
tryb: eksploracja | skupienie
projekt: <nazwa> | ad-hoc
status: draft | archiwum | do-archiwum
tematy: [tag1, tag2]
---
```

---

*Zapis sesji generuje `/aios:koniec-sesji`. Ręcznie też możesz.*
