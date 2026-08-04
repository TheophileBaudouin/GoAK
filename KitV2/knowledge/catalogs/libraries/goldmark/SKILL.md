---
name: goldmark
description: "github.com/yuin/goldmark v1.8.5 — CommonMark 0.31.2 compliant markdown parser for Go, zero dependencies, extensible via AST. Use when choosing a markdown→HTML rendering library. Not for sanitizing untrusted HTML output (see pièges) or for non-CommonMark dialects (GFM tables need an extension)."
category: library
tags: [markdown, commonmark, parsing, rendering, goldmark, extension]
last-verified: 2026-08-05
---

# goldmark — parsing markdown (CommonMark)

## Selection

[`github.com/yuin/goldmark`](https://github.com/yuin/goldmark) (v1.8.5,
Go 1.22+).

**Why it passes the gate** (actual reason, not stars): **zero dependencies**,
full CommonMark 0.31.2 compliance, AST-based extension model, and an
extensible renderer — the de-facto markdown engine in the Go ecosystem (Hugo,
Mattermost tools, many docs pipelines). Fuzzed (scorecard fuzzing 10/10) and
actively maintained.

## Admission checklist

- [x] Actively maintained — v1.8.5 (2026-07-28), push 2026-08-02
- [x] Single responsibility — CommonMark parsing + rendering
- [x] Idiomatic Go — AST (`ast.Node`) + renderer visitors, no magic
- [x] Tests present + CI — extensive CommonMark spec tests; fuzzing 10/10
- [x] Documentation — README + godoc + extensions catalogue
- [x] Real-world usage — Hugo et al.
- [x] Readable end-to-end — core ~8 kLOC, layered (parser/AST/renderer)
- [x] Justified by need — the kit covered templ HTML mais pas le markdown ;
      NOT popularity

## Minimal use

```go
md := goldmark.New()                 // extensions : goldmark.New(extension.GFM)
var buf bytes.Buffer
md.Convert([]byte("# Titre\n\nTexte **gras**"), &buf)
```

Compilé et vérifié avec v1.8.5 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `github.com/gomarkdown/markdown` | Conforme mais moins actif, AST moins propre ; goldmark est la référence CommonMark moderne. |
| `github.com/microcosm-cc/bluemonday` (sanitizer) | N'est PAS un parser markdown : à *combiner* avec goldmark quand l'entrée n'est pas de confiance (voir Pièges). |
| Rendu « maison » par regex | Anti-pattern documenté : jamais de markdown par regex (injection, non-conformité). |
| glamour (déjà au catalogue) | Rendu markdown **terminal** (TUI) — complémentaire, pas concurrent (goldmark = HTML/ast). |

## Security note

- Historique : 1 advisory **GO-2026-5320 / CVE-2026-5160 / GHSA-c97m-vxhj-p7j6**
  — XSS via le rendu de certains contenus, corrigé en **v1.7.17**.
  Épingler ≥ v1.7.17 ; v1.8.5 sain (vérifié 2026-08-05, OSV).
- goldmark rend du **HTML brut** présent dans le markdown (blocs HTML et
  `rawHTML` par défaut) : pour une entrée non contrôlée (commentaires, UGC),
  sanitiser la sortie avec bluemonday **et** désactiver les blocs HTML si non
  requis. Le XSS n'est pas un bug du parser : c'est le contrat du rendu.

## Utiliser cette librairie quand

- Rendre du markdown CommonMark en HTML côté serveur (docs, README, articles).
- Besoin d'extensions ciblées (GFM tables/strikethrough, front matter, syntax
  highlighting) via l'AST.
- Entrée de confiance (contenu éditorial interne) : le rendu par défaut suffit.

## Ne pas utiliser cette librairie quand

- L'entrée est du contenu utilisateur non contrôlé **sans** sanitisation en
  aval (bluemonday) : XSS garanti via blocs HTML (advisory GO-2026-5320).
- Besoin d'un dialecte non-CommonMark exotique : vérifier l'extension avant
  d'adopter.
- Le markdown est un détail mineur d'une app TUI : voir `glamour` (rendu
  terminal) à la place.

## Avantages

- Zéro dépendance, conformité CommonMark 0.31.2 testée par la spec officielle.
- AST complet : extensions et transformations (TOC, liens, highlight) sans
  hacks.
- Rendu et parsing séparés : contrôler précisément la sortie.
- Écosystème éprouvé (Hugo) et fuzzing.

## Inconvénients

- Blocs HTML rendus par défaut (danger UGC — nécessite sanitizer).
- v2 en beta avec breaking changes annoncés pour les extensions tierces :
  épingler une v1.8.x exacte en production.
- Pas de moteur de templates (titre/métadonnées) : à composer.

## Pièges connus

- XSS via rendu d'entrées non contrôlées (GO-2026-5320, fix ≥ 1.7.17) :
  sanitiser avec bluemonday ; désactiver `WithUnsafe`/blocs HTML quand non
  nécessaires.
- Extensions tierces : l'API AST peut casser à la frontière v2 — épingler la
  version exacte et tester à chaque bump.
- Ne pas parser des markdown « imbriqués » (ex. markdown dans un champ JSON)
  sans échappement explicite.

## Sources vérifiées

- [yuin/goldmark (repo officiel, v1.8.5)](https://github.com/yuin/goldmark)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/yuin/goldmark](https://pkg.go.dev/github.com/yuin/goldmark)
  — vérifié 2026-08-05
- [Advisory GO-2026-5320 / CVE-2026-5160 (XSS, fix 1.7.17)](https://osv.dev/vulnerability/GO-2026-5320)
  — vérifié 2026-08-05 (sécurité officielle)
- [goldmark v2 beta (breaking extensions)](https://github.com/yuin/goldmark/releases)
  — vérifié 2026-08-05
- Artefacts internes : `pattern:antipattern:sec-unsanitized-rendering`,
  catalog `glamour`
