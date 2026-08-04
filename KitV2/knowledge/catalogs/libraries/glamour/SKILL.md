---
name: glamour
description: "charm.land/glamour/v2 — stylesheet-based markdown rendering for terminal apps, with built-in light/dark themes and custom style sheets. Use when a CLI/TUI must render Markdown (docs, LLM output, reports) to the terminal."
category: library
tags: [tui, markdown, terminal, rendering, cli]
last-verified: 2026-08-04
---

# glamour — Markdown rendering for the terminal

## Selection

[`charm.land/glamour/v2`](https://github.com/charmbracelet/glamour) (v2).

**Why it passes the gate** (actual reason, not stars): it renders GitHub-flavored
Markdown to styled terminal output via CSS-like style sheets (dark/light/notty
built in), reusing goldmark for parsing. One function call turns Markdown into
ANSI-styled text that degrades cleanly on non-color terminals (`"notty"`). It is
the rendering engine behind Glow and the Charm docs stack, actively maintained.

## Admission checklist

- [x] Actively maintained — v2.0.x (2026)
- [x] Single responsibility — Markdown → terminal rendering
- [x] Idiomatic Go — `glamour.Render(input, style)` one-call API
- [x] Tests present + CI — yes
- [x] Documentation — README + charm.sh docs
- [x] Real-world usage — Glow, Charm CLI docs, many TUI apps
- [x] Readable end-to-end — yes
- [x] Justified by need — agents/CLIs routinely surface Markdown

## Minimal use

```go
out, err := glamour.Render(markdownText, "dark") // "dark" | "light" | "notty"
fmt.Print(out)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Hand-rolled ANSI styling | Reimplements a parser + theme engine; bugs and inconsistent output. |
| goldmark direct | HTML rendering; you still build the terminal renderer yourself. |
| chroma alone | Syntax highlighting only, no document layout. |

## Notes

- Choose `"notty"` when output may be piped (log files, CI): plain text without
  escape codes.
- Themes are style sheets — `glamour.WithStyles(yourStyleJSON)` for brand
  consistency.
- Pair with `lipgloss` for non-Markdown layout around the rendered text.

## Utiliser cette librairie quand

- Une CLI/TUI doit rendre du Markdown (docs, sortie LLM, rapports) au
  terminal.
- Un rendu GitHub-flavored stylé (thèmes dark/light/notty intégrés) est
  souhaité sans réimplémenter un parseur.
- La sortie doit dégrader proprement sur terminaux sans couleur (`"notty"`).

## Ne pas utiliser cette librairie quand

- Le rendu est de l'HTML (goldmark direct convient).
- Seule la coloration syntaxique est nécessaire (chroma seul suffit).
- Le contenu n'est pas du Markdown : lipgloss couvre le layout simple.

## Avantages

- Une fonction : `glamour.Render(input, style)` — Markdown → ANSI stylé.
- Basé sur goldmark (parseur maintenu), thèmes par feuilles de style
  (`WithStyles`).
- Usage réel : Glow, stack docs de Charm, nombreuses TUIs.
- Dégradation propre (`notty`) pour les pipes et CI.

## Inconvénients

- Rendu terminal seulement : pas de sortie HTML riche (goldmark reste la
  référence pour HTML).
- Thèmes par défaut limités à dark/light/notty — la marque exige une feuille
  de style custom.
- Dépend de la chaîne Charm (goldmark + styles) — coût d'installation pour un
  rendu simple.

## Pièges connus

- Toujours choisir `"notty"` quand la sortie peut être pipée (logs, CI) :
  éviter les codes d'échappement parasites.
- La cohérence de marque passe par `WithStyles` (JSON de style), pas par du
  post-traitement ANSI.
- Pour le layout non-Markdown autour du rendu, combiner avec `lipgloss`.

## Sources vérifiées

- [charmbracelet/glamour (repo officiel, v2)](https://github.com/charmbracelet/glamour)
  — vérifié 2026-08-04
- [pkg.go.dev/charm.land/glamour/v2](https://pkg.go.dev/charm.land/glamour/v2)
  — vérifié 2026-08-04
- Artefact interne : catalog `lipgloss` (layout complémentaire)
