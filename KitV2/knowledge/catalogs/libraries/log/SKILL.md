---
name: log
description: "charm.land/log/v2 v2.0.0 — colorful, leveled, slog-compatible logging handler for Go. Use when a human-facing CLI/TUI needs styled logs while retaining log/slog; not for high-throughput/security-audit pipelines or a replacement for the standard logging interface."
category: library
tags: [logging, slog, tui, cli, terminal]
last-verified: 2026-08-05
---

# log — colored slog handler

## Selection

[`charm.land/log/v2`](https://github.com/charmbracelet/log) v2.0.0 is a
human-oriented logging handler that implements `log/slog.Handler`. It keeps the
standard structured logging API while adding terminal-friendly levels, formatters,
and optional styling. It is admitted for the focused CLI/TUI presentation layer,
active maintenance, tests, and Charm use; the kit's `slog` rule remains the
interface boundary.

## Admission checklist

- [x] Current v2.0.0 module and active upstream maintenance.
- [x] Single responsibility: human-readable structured log handler.
- [x] Implements standard `slog.Handler` with text/JSON/logfmt options.
- [x] Tests, CI, documentation, and real Charm CLI use exist.
- [x] The kit can retain stdlib `slog` at call sites and swap the handler.

## Minimal use

```go
func newLogger(w io.Writer) *slog.Logger {
    handler := charmLog.New(charmLog.WithOutput(w))
    return slog.New(handler)
}
```

Keep the logger explicitly injected into application components. Choose JSON or
logfmt for machine pipelines and disable styling when output is not a TTY.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `log/slog` | Default choice for services and zero-dependency structured logging. |
| zap / zerolog | Consider for measured high-throughput or JSON-first service workloads. |
| logrus | Legacy compatibility only; do not choose for new code without a reason. |

## When to use this library
- A CLI/TUI needs readable colored logs and the application still wants the
  standard `slog` API.
- Text, JSON, logfmt, caller reporting, or sub-loggers are useful at the edge.
- Styling is a presentation decision, not an audit/security guarantee.

## When NOT to use this library
- The service needs only stdlib `slog` and no human-facing styling.
- Logs feed a high-throughput machine pipeline where performance is measured and
  a specialized JSON logger is justified.
- The requirement includes tamper-proof, encrypted, or compliance-grade audit
  storage; a formatter cannot provide those properties.

## Advantages
- Standard `slog.Handler` compatibility preserves the kit's logging contract.
- Human-readable levels, styles, text/JSON/logfmt formatters, and sub-loggers.
- Terminal color behavior can be disabled at non-TTY output boundaries.

## Disadvantages
- Human-oriented styling is extra surface for a service that already uses
  stdlib `slog`.
- No custom slog levels, tamper-proof audit log, encryption, or compliance
  guarantees.
- Review concurrency behavior and output ownership for high-load use.

## Known pitfalls
- Keep using `slog` in application code; `charm.land/log/v2` is a handler, not
  a reason to hide the logger in global state.
- Select JSON/logfmt or disable colors for pipes, CI, and machine ingestion.
- Use explicit logger injection and handle output errors at the boundary.
- Review upstream concurrency issues before using it as the critical service
  logger under extreme load.

## Verified sources
- [Official charm log repository](https://github.com/charmbracelet/log) — API,
  maintenance, license, checked 2026-08-05.
- [log v2 on pkg.go.dev](https://pkg.go.dev/charm.land/log/v2) — exact version
  and handler API, checked 2026-08-05.
- [log v2.0.0 release](https://github.com/charmbracelet/log/releases/tag/v2.0.0)
  — module migration, checked 2026-08-05.
- [Issue #116](https://github.com/charmbracelet/log/issues/116) — custom level
  limitation, checked 2026-08-05.
- [Issue #176](https://github.com/charmbracelet/log/issues/176) — concurrency
  behavior to review, checked 2026-08-05.
- [OSV package search](https://osv.dev/search?q=charmbracelet%2Flog) — no package
  advisory found at verification time, checked 2026-08-05.
