---
name: log
description: "charm.land/log/v2 — minimal, colorful, slog-compatible Go logging library with levels and caller reporting. Use when a CLI/TUI wants human-readable colored logs while keeping the standard log/slog handler interface."
category: library
tags: [logging, slog, tui, cli, terminal]
last-verified: 2026-08-04
---

# log — Colorful slog-compatible logging

## Selection

[`charm.land/log/v2`](https://github.com/charmbracelet/log) (v2).

**Why it passes the gate** (actual reason, not stars): it implements the
standard `log/slog.Handler` interface, so it is a drop-in colored handler for
the kit's mandated `slog` logging story — no logging paradigm change, just a
handler swap. Small, readable, zero magic; the default for Charm CLIs.

## Admission checklist

- [x] Actively maintained — v2.0.x (2026)
- [x] Single responsibility — colored human-readable log handler
- [x] Idiomatic Go — implements `slog.Handler`
- [x] Tests present + CI — yes
- [x] Documentation — README + charm.sh docs
- [x] Real-world usage — Gum, Soft Serve, and other Charm CLIs
- [x] Readable end-to-end — yes, tiny core
- [x] Justified by need — adds color/caller to slog with zero API change

## Minimal use

```go
import slog "log/slog"
import charmLog "charm.land/log/v2"

slog.SetDefault(slog.New(charmLog.New(charmLog.WithTimeFormat(time.Kitchen))))
slog.Info("server started", "port", 8080)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| zap / zerolog | Structured JSON-first; overkill for human-facing CLI logs. Fine when logs feed a pipeline — then keep them instead. |
| Standard slog text handler | Correct default; add charm log only when colored human output matters (CLI/TUI). |

## Notes

- Kit rule `logging` mandates `slog` as the interface: charm log is a handler,
  not a replacement — code keeps using `slog`.
- `WithReportCaller()` adds file:line; keep it off in perf-sensitive paths.
