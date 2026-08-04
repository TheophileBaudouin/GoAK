---
name: colorprofile
description: "github.com/charmbracelet/colorprofile — terminal color capability detection (truecolor, 256, 16, or none) for Go. Use when a CLI/TUI must adapt colors to the terminal and TERM/COLORTERM sniffing is not enough."
category: library
tags: [terminal, color, detection, tui, ansi]
last-verified: 2026-08-04
---

# colorprofile — Terminal color detection

## Selection

[`github.com/charmbracelet/colorprofile`](https://github.com/charmbracelet/colorprofile).

**Why it passes the gate** (actual reason, not stars): it centralizes the messy
terminal capability detection logic (TERM/COLORTERM/env parsing, feature
detection) into one tested package, and converts colors between profiles
(hex → 256-color → ANSI). It is the maintained successor of the removed
`termenv` project (which no longer exists in the org — see project Gotchas).

## Admission checklist

- [x] Actively maintained — v0.4.x (2026)
- [x] Single responsibility — color capability detection/conversion
- [x] Idiomatic Go — small pure API
- [x] Tests present + CI — yes
- [x] Documentation — README
- [x] Real-world usage — Lip Gloss v2 and Charm tooling under the hood
- [x] Readable end-to-end — yes
- [x] Justified by need — wrong color handling breaks UX on legacy terminals

## Minimal use

```go
profile := colorprofile.Detect(nil, nil) // honors COLORTERM/TERM
if profile == colorprofile.TrueColor { ... }
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| termenv | Deprecated/removed from the org — do not use. |
| Manual TERM/COLORTERM parsing | Reimplements a bug-prone matrix; detection rules change. |
| `lipgloss` built-in handling | Correct for styling; reach for colorprofile when you need the profile value itself (stripping, conversion, `sequin` decisions). |

## Notes

- `colorprofile.Convert` maps a color to the target profile's palette.
- For stripping ANSI before piping output, combine with `sequin`.
