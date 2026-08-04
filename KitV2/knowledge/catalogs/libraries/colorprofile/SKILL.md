---
name: colorprofile
description: "github.com/charmbracelet/colorprofile v0.4.3 — terminal color-profile detection and downsampling for Go. Use when a CLI/TUI must adapt output to TTY, ANSI, 256-color, or truecolor capabilities; not for general color-space or styling work."
category: library
tags: [terminal, color, detection, tui, ansi]
last-verified: 2026-08-05
---

# colorprofile — détection de profil terminal

## Selection

[`github.com/charmbracelet/colorprofile`](https://github.com/charmbracelet/colorprofile)
v0.4.3 is a small tested package that detects terminal color capability from
writers, environment, terminfo, and tmux, then converts colors to the target
profile. It is admitted for this narrow terminal boundary and use in Charm's
terminal stack, not for star count.

## Admission checklist

- [x] Current v0.4.3 release and active upstream maintenance.
- [x] Single responsibility: terminal profile detection and color conversion.
- [x] Small Go API with tests, CI, and documentation.
- [x] Handles `NO_COLOR`, `CLICOLOR`, TTY, terminfo, and profile conversion.
- [x] Real use as a lower-level component in Charm terminal tooling.

## Minimal use

```go
profile := colorprofile.Env(os.Environ())
if profile == colorprofile.TrueColor {
    // render the truecolor path
}
```

Use `colorprofile.Detect(writer, env)` when the output writer and environment
must both participate. `NewWriter` can downsample ANSI output while writing;
`colorprofile` does not provide terminal styling itself.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `lipgloss` | Prefer for styling; use colorprofile when the profile value or writer conversion is itself required. |
| `muesli/termenv` | Broader terminal styling/detection surface; colorprofile is the focused Charm component. |
| Manual `TERM` parsing | Avoid: it duplicates a changing, edge-case-heavy capability matrix. |
| `sequin` | Companion for parsing/stripping ANSI sequences, not profile detection. |

## Utiliser cette librairie quand

- A CLI/TUI must choose between no color, ANSI, 256-color, and truecolor.
- Output must be downsampled through an `io.Writer` for the target terminal.
- Environment, TTY, terminfo, or tmux signals need a single tested decision.

## Ne pas utiliser cette librairie quand

- The application only needs styles: use Lip Gloss or another styling layer.
- It needs ICC, image color-space, or general color mathematics.
- The terminal target is fixed and no runtime profile decision is needed.

## Avantages

- Focused API for detection and palette conversion.
- Handles common terminal environment conventions instead of requiring manual
  parsing.
- Small, tested, and composable with Charm's styling and ANSI packages.

## Inconvénients

- Detection remains heuristic for unusual terminals and multiplexers.
- It is not a styling framework and does not solve general color management.
- `FORCE_COLOR` is not the same input as the supported `CLICOLOR_FORCE` policy.

## Pièges connus

- Test `NO_COLOR`, `CLICOLOR`, `CLICOLOR_FORCE`, tmux, and non-TTY output in the
  consumer's actual output path.
- An open tmux issue can misclassify `COLORTERM=truecolor`; do not treat
  detection as an absolute hardware guarantee.
- Use `Convert` before rendering, and use `sequin` separately when ANSI needs
  to be stripped for a pipe or log.

## Sources vérifiées

- [Official colorprofile repository](https://github.com/charmbracelet/colorprofile)
  — maintenance, API, license, checked 2026-08-05.
- [colorprofile v0.4.3 on pkg.go.dev](https://pkg.go.dev/github.com/charmbracelet/colorprofile@v0.4.3)
  — exact version and API, checked 2026-08-05.
- [colorprofile releases](https://github.com/charmbracelet/colorprofile/releases)
  — current tag, checked 2026-08-05.
- [Issue #76](https://github.com/charmbracelet/colorprofile/issues/76) — tmux
  detection limitation, checked 2026-08-05.
- [PR #85](https://github.com/charmbracelet/colorprofile/pull/85) — pending
  `FORCE_COLOR` behavior, checked 2026-08-05.
