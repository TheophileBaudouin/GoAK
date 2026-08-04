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
