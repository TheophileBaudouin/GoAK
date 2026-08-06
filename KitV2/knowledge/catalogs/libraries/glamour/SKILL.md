---
name: glamour
description: "charm.land/glamour/v2 v2.0.1 — stylesheet-based Markdown-to-terminal rendering built on goldmark. Use when a Go CLI/TUI renders Markdown with dark/light/notty styles; not for HTML, images, or general terminal styling."
category: library
tags: [tui, markdown, terminal, rendering, cli]
last-verified: 2026-08-05
---

# glamour — terminal Markdown rendering

## Selection

[`charm.land/glamour/v2`](https://github.com/charmbracelet/glamour) v2.0.1,
released 2026-06-12, renders Markdown as styled terminal text using themes and
custom style sheets. It is admitted for the focused Markdown-to-terminal
boundary, active maintenance, tests, and use in Glow/Charm applications, not
for popularity.

## Admission checklist

- [x] Current v2.0.1 release with active upstream maintenance.
- [x] Single responsibility: Markdown parsing/rendering for terminal output.
- [x] Built on goldmark with tests, CI, documentation, and examples.
- [x] Provides dark/light/notty styles and custom style options.
- [x] The project keeps HTML, image rendering, and general styling outside this
      package's responsibility.

## Minimal use

```go
func render(markdown string) (string, error) {
    renderer, err := glamour.NewTermRenderer(glamour.WithStandardStyle("dark"))
    if err != nil {
        return "", fmt.Errorf("create renderer: %w", err)
    }
    out, err := renderer.Render(markdown)
    if err != nil {
        return "", fmt.Errorf("render markdown: %w", err)
    }
    return out, nil
}
```

Use a `notty` style when output is piped or captured. In v2 the module path is
`charm.land/glamour/v2`; the v1 import path and removed auto-style options must
not be copied into new code.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| goldmark | Choose when the output is HTML or a custom AST/renderer boundary is required. |
| lipgloss | Companion for terminal layout and styling, not a Markdown renderer. |
| Hand-written ANSI rendering | Rejected for non-trivial Markdown; it recreates parsing and layout bugs. |
| glow | Choose the complete standalone Markdown reader; glamour is the embeddable renderer. |

## When to use this library
- A CLI/TUI needs to render Markdown documents, reports, or LLM output in a
  terminal.
- Built-in dark/light/notty themes or a custom style sheet are sufficient.
- The output must remain terminal text rather than HTML or images.

## When NOT to use this library
- The target is HTML, a browser, or a rich document format.
- Image rendering is a requirement.
- Only ANSI styling/layout is needed without Markdown parsing.
- A standalone Markdown reader is desired instead of an embedded library.

## Advantages
- Focused Markdown-to-terminal API on top of goldmark.
- Stylesheet-based customization and a plain `notty` mode for pipes/CI.
- v2 has a clear vanity module path and a maintained Charm ecosystem boundary.

## Disadvantages
- Terminal output only; it does not replace an HTML renderer or image pipeline.
- Word wrapping and table width require deliberate configuration for narrow or
  structured output.
- v2 is a breaking import/API migration from the v1 package.

## Known pitfalls
- Use `notty` for pipes, logs, and CI; ANSI escape codes are not a substitute
  for terminal capability detection.
- Configure word wrap for tables and narrow terminals; upstream tracks width
  and punctuation edge cases.
- Do not copy removed v1 `WithAutoStyle` or `WithColorProfile` APIs.
- Keep terminal styling around the rendered document in Lip Gloss, not by
  post-processing arbitrary ANSI strings.

## Verified sources
- [Official Glamour repository](https://github.com/charmbracelet/glamour) —
  maintenance and architecture, checked 2026-08-05.
- [Glamour v2.0.1 on pkg.go.dev](https://pkg.go.dev/charm.land/glamour/v2@v2.0.1)
  — exact version and API, checked 2026-08-05.
- [Glamour v2.0.1 release](https://github.com/charmbracelet/glamour/releases/tag/v2.0.1)
  — release notes, checked 2026-08-05.
- [Glamour v2 upgrade guide](https://github.com/charmbracelet/glamour/blob/main/UPGRADE_GUIDE_V2.md)
  — removed APIs and migration, checked 2026-08-05.
- [Glamour issues](https://github.com/charmbracelet/glamour/issues) — width,
  wrapping, and image limitations, checked 2026-08-05.
