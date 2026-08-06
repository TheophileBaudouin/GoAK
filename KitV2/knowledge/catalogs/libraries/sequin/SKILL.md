---
name: sequin
description: "github.com/charmbracelet/sequin v0.3.1 — CLI for inspecting and explaining ANSI escape sequences. Use when debugging or inspecting styled terminal output; not as a reusable parser library or a styling layer."
category: library
tags: [ansi, terminal, parsing, tui, sequences]
last-verified: 2026-08-05
---

# sequin — ANSI sequence inspection

## Selection

[`github.com/charmbracelet/sequin`](https://github.com/charmbracelet/sequin) v0.3.1,
released 2025-01-27, is a focused CLI that reads ANSI output, executes commands
in a fake TTY, and explains the resulting escape sequences. It is admitted as a
debugging/inspection tool in the Charm terminal ecosystem, not as a reusable Go
library despite the catalog's library surface.

## Admission checklist

- [x] Stable v0.3.1 with active repository maintenance.
- [x] Single responsibility: human-readable ANSI sequence inspection.
- [x] Reads stdin or a command and prints parsed sequence explanations.
- [x] Uses the maintained Charm ANSI parsing stack and has documentation/tests.
- [x] Complements, rather than replaces, Lip Gloss/colorprofile runtime APIs.

## Minimal use

```sh
printf '\033[31mred\033[0m' | sequin
sequin -- go run ./cmd/example
```

There is no supported Go package API to embed; use `charmbracelet/x/ansi` or a
higher-level styling package when code must parse/produce ANSI programmatically.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `charmbracelet/x/ansi` | Use for programmatic ANSI parsing in Go; sequin is the human-facing CLI. |
| Lip Gloss | Use for producing styled terminal output, not explaining existing sequences. |
| Golden/teatest tools | Use for testing rendered TUI output; sequin helps inspect what the output contains. |
| Regex over escape bytes | Reject: it misses OSC/CSI/hyperlink and multi-byte edge cases. |

## When to use this library
- Debugging a CLI/TUI whose output contains ANSI sequences.
- Inspecting a command's terminal protocol, colors, hyperlinks, cursor, or mode
  changes in a readable form.
- Comparing piped/golden output with what a terminal parser sees.

## When NOT to use this library
- A Go service needs a reusable parser or writer API.
- The task is producing styles: use Lip Gloss/colorprofile.
- ANSI is absent and ordinary text measurement is sufficient.
- The application requires complete Kitty graphics/APC interpretation.

## Advantages
- Human-readable inspection instead of manual escape-byte decoding.
- Fake-TTY command execution helps debug output that depends on terminal mode.
- Handles common CSI/OSC/DCS/SGR and terminal control sequences through Charm's
  maintained parser stack.

## Disadvantages
- CLI-only; it is not a library dependency with a stable embedding API.
- APC/Kitty graphics sequences are not fully supported.
- It explains sequences; it does not render or normalize terminal text for an
  application's layout policy.

## Known pitfalls
- Do not infer that a parsed byte length equals visible terminal width; use the
  appropriate width/parser policy for layout.
- Treat unknown sequences as unknown rather than silently discarding them.
- Use a real TTY fixture when terminal-dependent behavior matters; piped input
  and fake TTY execution are different paths.
- Keep `sequin` as a debugging tool and use `x/ansi`, Lip Gloss, or colorprofile
  for program code.

## Verified sources
- [Official sequin repository](https://github.com/charmbracelet/sequin) — README,
  CLI scope, maintenance, license, checked 2026-08-05.
- [sequin v0.3.1 release](https://github.com/charmbracelet/sequin/releases/tag/v0.3.1)
  — exact version and date, checked 2026-08-05.
- [sequin on pkg.go.dev](https://pkg.go.dev/github.com/charmbracelet/sequin) —
  module/package scope, checked 2026-08-05.
- [sequin source](https://github.com/charmbracelet/sequin/blob/main/sgr.go) —
  ANSI/SGR handling, checked 2026-08-05.
- [Charm ANSI package](https://pkg.go.dev/github.com/charmbracelet/x/ansi)
  — programmatic alternative, checked 2026-08-05.
