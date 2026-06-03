# Wiedza - index

Zasoby wiedzy cross-project, przetwarzane metodą Karpathy (Raw → Wiki). Struktura:

```
Wiedza/
└── <obszar>/           ← np. AI, Marketing, Programming, Biblioteka
    ├── Raw/            ← surowce (artykuły, PDF, transkrypty)
    └── Wiki/           ← skompilowane strony (atomowe pojęcia)
        ├── index.md    ← spis stron w obszarze
        └── *.md        ← pojedyncze strony
```

## Obszary

(lista wypełni się jak zaczniesz dodawać materiały)

## Jak to działa

1. Wrzucasz surowiec do `Wiedza/<obszar>/Raw/src-NN-nazwa.md` (albo `.pdf`).
2. Uruchamiasz `/aios:dodaj-do-wiki Wiedza/<obszar>/Raw/src-NN-nazwa.md`.
3. Skill wyciąga pojęcia, aktualizuje istniejące strony albo tworzy nowe w `Wiki/`.
4. Szukasz potem przez `/aios:szukaj <query>` - od ogółu (index) do szczegółu (konkretna strona).

---

*Dodaj materiał do wiki: `/aios:dodaj-do-wiki <ścieżka>`.*
