---
name: sequin
description: "github.com/charmbracelet/sequin — human-readable ANSI escape sequence parsing and writing for Go. Use when a TUI/CLI must parse, transform, or measure terminal text that contains ANSI codes (styled output, logs, pipelines)."
category: library
tags: [ansi, terminal, parsing, tui, sequences]
last-verified: 2026-08-04
---

# sequin — ANSI sequence parsing

## Selection

[`github.com/charmbracelet/sequin`](https://github.com/charmbracelet/sequin).

**Why it passes the gate** (actual reason, not stars): ANSI parsing is the
classic "regex over escape bytes" trap — subtle and wrong at the edges (OSC,
hyperlinks, multi-byte SGR). Sequin is a real tokenizer/parser for escape
sequences with an equally clean writer, maintained by the team that owns the
terminal stack. It is the stable sibling of the experimental `x/ansi` packages.

## Admission checklist

- [x] Actively maintained — v0.3.x releases, commits 2026
- [x] Single responsibility — ANSI sequence parse/write
- [x] Idiomatic Go — tokenizer API, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README + examples
- [x] Real-world usage — Charm terminal tooling
- [x] Readable end-to-end — yes
- [x] Justified by need — correct ANSI handling is genuinely hard

## Minimal use

```go
tokens, err := sequin.Parse("\x1b[31mred\x1b[0m")
// tokens: text("red") with an SGR style token around it — inspect/rewrite safely
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Regex over escape codes | Fragile: breaks on OSC/CSI variants, hyperlinks, and multi-byte sequences. |
| `charmbracelet/x/ansi` | Experimental umbrella package — fine to try, but sequin is the stabilized API. |
| ansiwrap (third-party) | Niche, smaller maintenance story. |

## Notes

- Use it before measuring visible string width of styled text (ANSI bytes
  inflate `len()`).
- Pair with `colorprofile` to decide whether to strip or keep codes for a
  given terminal.

## Utiliser cette librairie quand

- Parser, transformer ou mesurer du texte terminal contenant des codes ANSI
  (sorties stylées, logs, pipelines) sans « regex sur bytes d'échappement ».
- La largeur visible d'un texte stylé doit être mesurée (les bytes ANSI
  gonflent `len()`).
- Écrire des séquences ANSI propres sans concaténer des codes bruts.

## Ne pas utiliser cette librairie quand

- Le texte est déjà nettoyé (aucun ANSI) : pas de parsing nécessaire.
- `charmbracelet/x/ansi` (expérimental) suffit pour un prototype — sequin est
  l'API stabilisée, préférable en prod.

## Avantages

- Vrai tokenizer/parser de séquences d'échappement (CSI, OSC, hyperlinks,
  multi-byte SGR) — pas de regex fragile.
- Écrivain propre pour produire des séquences.
- Maintenu par l'équipe qui possède la stack terminal (sibling stable de
  x/ansi).

## Inconvénients

- API orientée tokens : un cas simple « coloriser une chaîne » passe par
  lipgloss plutôt que sequin.
- Surface étroite (parse/write) : les décisions de profil (stripper ou
  garder) restent à `colorprofile`.

## Pièges connus

- Mesurer la largeur visible APRÈS parsing (les bytes ANSI faussent `len()`).
- Combiner avec `colorprofile` pour décider stripper/garder selon le
  terminal cible.
- Ne pas écrire de parser ANSI maison : les cas limites (OSC, hyperlinks)
  sont précisément ce que sequin couvre.

## Sources vérifiées

- [charmbracelet/sequin (repo officiel, v0.3.x)](https://github.com/charmbracelet/sequin)
  — vérifié 2026-08-04
- Artefact interne : catalog `colorprofile` (décision stripper/garder)
