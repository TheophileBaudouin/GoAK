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
