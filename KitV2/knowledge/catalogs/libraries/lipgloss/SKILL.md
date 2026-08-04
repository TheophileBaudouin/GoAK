---
name: lipgloss
description: "charm.land/lipgloss/v2 v2.0.5 — composable terminal styles for colors, borders, padding, alignment, width, and layouts. Use for deterministic Go CLI/TUI output; not for HTML, interactive event loops, or raw terminal capability policy."
category: library
tags: [tui, styling, terminal, ansi, cli]
last-verified: 2026-08-05
---

# lipgloss — styles terminal

## Selection

[`charm.land/lipgloss/v2`](https://github.com/charmbracelet/lipgloss) v2.0.5,
released 2026-07-03, provides value-like composable terminal styles and layout
helpers. It is admitted for deterministic styling, active maintenance, tests,
documentation, and Charm ecosystem use; not for popularity. It is a styling
layer, not a TUI event loop.

## Admission checklist

- [x] Current v2.0.5 release and active upstream maintenance.
- [x] Single responsibility: terminal style and layout values.
- [x] Chained style API with deterministic string rendering.
- [x] Tests, CI, documentation, and broad real use exist.
- [x] v2 migration and terminal-width limitations are documented.

## Minimal use

```go
func heading(text string) string {
    style := lipgloss.NewStyle().Bold(true).Foreground(lipgloss.Color("12"))
    return style.Render(text)
}
```

Use `fmt.Fprintln` or another output boundary to write the returned string. Use
`colorprofile` when the application needs the detected profile as a value; do
not infer that policy from a rendered style.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Raw ANSI escapes | Avoid: not composable or reliably width/profile aware. |
| `fatih/color` | Choose for simple color-only output without borders/layout. |
| `pterm` | Choose for a broader imperative formatting/component layer when its extra surface is justified. |
| Bubble Tea | Companion framework for interactive state, not a styling replacement. |

## Utiliser cette librairie quand

- CLI/TUI output needs colors, borders, padding, alignment, width, or joined
  multi-line layouts.
- Styles must be values that can be composed and rendered in tests.
- The output belongs to the Charm terminal stack and should avoid raw ANSI.

## Ne pas utiliser cette librairie quand

- The output target is HTML, a browser, or a non-terminal document.
- A one-off plain string needs no style abstraction.
- The requirement is event handling, widgets, forms, or a TUI framework.
- The application needs an explicit terminal profile decision rather than style
  rendering.

## Avantages

- Chained styles and layout helpers render deterministic strings.
- Borders, padding, alignment, width, and joins share one composable API.
- v2 separates style values from the framework/event-loop boundary.
- It composes with Bubble Tea, Bubbles, Glamour, and Huh.

## Inconvénients

- Terminal-only output; it does not produce HTML or own terminal events.
- Unicode grapheme width and bordered-table edge cases require testing with real
  content.
- The v2 API/import migration is breaking from v1.
- Very simple output can be clearer with stdlib formatting alone.

## Pièges connus

- Derive a variant with `style.Copy()` rather than mutating shared style state.
- Test emoji/grapheme widths, borders, padding, and wrapped lines if layout is
  part of the user-visible contract.
- Avoid `HasDarkBackground` in non-TTY paths until its pipe behavior is handled;
  select an explicit profile for automation.
- Use `colorprofile` for explicit capability detection and `sequin` for ANSI
  parsing/stripping.

## Sources vérifiées

- [Official Lip Gloss repository](https://github.com/charmbracelet/lipgloss) —
  API, maintenance, license, checked 2026-08-05.
- [Lip Gloss v2.0.5 release](https://github.com/charmbracelet/lipgloss/releases/tag/v2.0.5)
  — exact version and changes, checked 2026-08-05.
- [Lip Gloss on pkg.go.dev](https://pkg.go.dev/charm.land/lipgloss/v2) — API and
  module metadata, checked 2026-08-05.
- [Lip Gloss v2 upgrade guide](https://github.com/charmbracelet/lipgloss/blob/main/UPGRADE_GUIDE_V2.md)
  — migration boundary, checked 2026-08-05.
- [Issue #562](https://github.com/charmbracelet/lipgloss/issues/562) — emoji
  width limitation, checked 2026-08-05.
- [Issue #635](https://github.com/charmbracelet/lipgloss/issues/635) — non-TTY
  background detection limitation, checked 2026-08-05.
