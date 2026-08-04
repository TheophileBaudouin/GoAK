---
name: lipgloss
description: "charm.land/lipgloss/v2 — style definitions for terminal layouts (colors, borders, alignment, width, padding) with composable style chaining. Use when formatting CLI/TUI output in Go and you want deterministic, testable styling instead of raw ANSI codes."
category: library
tags: [tui, styling, terminal, ansi, cli]
last-verified: 2026-08-04
---

# lipgloss — terminal styling

## Selection

[`charm.land/lipgloss/v2`](https://github.com/charmbracelet/lipgloss) (v2).

**Why it passes the gate** (actual reason, not stars): styles are immutable,
composable values — `NewStyle().Foreground(...).Bold(true).Width(40)` — that
render to deterministic strings. It handles color-profile-aware output (truecolor
vs 256 vs ANSI via terminal detection), borders, alignment, padding, and
joined/multi-line layouts, all in a tiny, readable API. It is the styling layer
under the whole Charm TUI stack.

## Admission checklist

- [x] Actively maintained — v2.0.x (2026)
- [x] Single responsibility — terminal style definitions
- [x] Idiomatic Go — value-style chaining, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README + charm.sh docs
- [x] Real-world usage — every Charm app (glow, gum, vhs…) and countless others
- [x] Readable end-to-end — yes, small core
- [x] Justified by need — color/layout must degrade correctly per terminal

## Minimal use

```go
style := lipgloss.NewStyle().Foreground(lipgloss.Color("12")).Bold(true)
fmt.Println(style.Render("hello"))
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Raw ANSI escape codes | Not terminal-aware (truecolor on a 256-color terminal breaks), error-prone, untestable. |
| fatih/color | Color output only — no layout, borders, alignment, or width handling. |
| pterm | Broad formatting but imperative and heavier; lipgloss composes with the rest of the Charm stack. |

## Notes

- Lipgloss performs its own color-profile detection; the underlying `termenv`
  project was absorbed — for direct capability detection use
  `colorprofile` in this catalog.
- Styles compose: `style.Copy().Foreground(otherColor)` to derive variants.
- `lipgloss.JoinVertical/Horizontal` and `Width` handle layout without tabs.

## Utiliser cette librairie quand

- Formater la sortie CLI/TUI (couleurs, bordures, alignement, largeur,
  padding) avec des styles déterministes et testables au lieu d'ANSI brut.
- La sortie doit s'adapter au profil couleur du terminal (truecolor vs 256
  vs ANSI).
- Composer avec l'écosystème Charm (bubbletea, bubbles, glamour, huh).

## Ne pas utiliser cette librairie quand

- Une seule couleur en sortie suffit (fatih/color est plus léger).
- Le besoin est du formatage large et impératif (pterm) — lipgloss compose,
  pterm formate.
- La sortie n'est pas un terminal (HTML/web : hors périmètre).

## Avantages

- Styles immutables et composables : valeurs déterministes et testables.
- Détection de profil couleur intégrée (truecolor/256/ANSI).
- Bordures, alignement, padding, layout multi-ligne (`JoinVertical/Horizontal`,
  `Width`) — sans tabulations fragiles.
- Couche de style de toute la stack Charm, très utilisée.

## Inconvénients

- Style terminal seulement : pas de sortie web/HTML.
- La détection de profil est intégrée mais pour une décision explicite du
  profil, passer par `colorprofile` (termenv absorbé — Gotcha).
- API orientée composition : une sortie très simple peut être plus lourde
  qu'un fmt.Printf.

## Pièges connus

- Pour la valeur du profil couleur elle-même (stripping, conversion), utiliser
  `colorprofile` — ne pas déduire des styles lipgloss.
- Dériver les variantes avec `style.Copy().Foreground(...)`, jamais en
  mutant un style partagé.
- Préférer `JoinVertical/Horizontal` et `Width` aux tabulations pour le
  layout.

## Sources vérifiées

- [charmbracelet/lipgloss (repo officiel, v2)](https://github.com/charmbracelet/lipgloss)
  — vérifié 2026-08-04
- [pkg.go.dev/charm.land/lipgloss/v2](https://pkg.go.dev/charm.land/lipgloss/v2)
  — vérifié 2026-08-04
- Artefacts internes : catalog `colorprofile` (détection explicite),
  catalog `glamour` (rendu Markdown stylé)
