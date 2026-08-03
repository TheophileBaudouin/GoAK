---
name: logging
description: "Idiomatic Go logging rules — log/slog as the default, request-scoped logging via explicit logger injection, log-level discipline (Error = actual failure). Use when adding logging to a service, handler, or background worker."
category: rule
tags: [logging, slog, observability, structured]
last-verified: 2026-08-02
---

# logging — structured logging with log/slog

## 1. log/slog is the default

Use the standard library `log/slog` (stable since Go 1.21). Do not reach for a
third-party logger (zap, zerolog) unless a measured need justifies it — `slog`
covers structured, leveled, handler-pluggable logging with zero dependencies,
which is the kit's stdlib-first stance.

```go
import "log/slog"

slog.Info("user created", "id", id, "team", team)
// -> time=... level=INFO msg="user created" id=42 team=platform
```

Key-value pairs as variadic args — never `fmt.Sprintf` into the message and
never `fmt.Println` in service code (the release checklist gates this).

## 2. Request-scoped logger — explicit injection, not context.Value

Inject the logger as a field on the type that does the work, set in its
constructor:

```go
type Store struct {
    log *slog.Logger
}

func NewStore(log *slog.Logger) *Store {
    if log == nil {
        log = slog.Default() // sensible fallback, never nil
    }
    return &Store{log: log}
}

func (s *Store) createItem(...) {
    s.log.Info("item created", "id", id, "name", name)
}
```

**Why injection over a logger stashed in `context.Value`:**

- The dependency is **visible** in the type signature and constructor — matches
  the kit's "dependency injection over globals" rule.
- It is **trivially testable**: inject a `slog.New(slog.NewTextHandler(&buf, nil))`
  and assert on the captured output. A `context.Value` logger is invisible to
  the test and to the reader.
- `context.Context` carries **cancellation and request-scoped values**, not
  infrastructure. Overloading it to smuggle a logger hides wiring and makes
  every function that needs a log line also drag a `context` it may not need.

Derive a child logger for request-scoped fields at the boundary, then inject
*that*:

```go
func (s *Server) handler(w http.ResponseWriter, r *http.Request) {
    log := s.log.With("req_id", middleware.GetReqID(r.Context()))
    // pass `log` (or a store built around it) downstream — explicit.
}
```

## 3. Log-level discipline

| Level | Use for | Not for |
|---|---|---|
| `Error` | An operation **failed** and the call site cannot recover — data not saved, a dependency is down | "interesting" events, control flow |
| `Warn` | Something unexpected but handled (a cache miss falling back to origin, a not-found that may be a probe) | Routine noise |
| `Info` | A meaningful business event (user created, job completed) — the audit trail you'd grep in prod | Per-request access lines at high volume (those belong in an access log, not slog at Info) |
| `Debug` | Internal detail useful when reproducing a bug | Anything shipped to prod logs at volume |

`Error` is **not** a catch-all for "I want to see this." If the code handled
the error and continued, that is `Warn`, not `Error`.

## Anti-patterns

- `fmt.Println` / `log.Printf` in service code — unstructured, no level, not
  pluggable.
- Stashing `*slog.Logger` in `context.Value` — hides the dependency, hard to test.
- `Error` for non-fatal events — trains responders to ignore the level.
- Logging the same error at every layer (see `rules/core/errors`: handle once, at the
  layer with enough context; the others wrap and return, they do not log).

## Cross-references

- `rules/core/errors` — handle-once rule; logging and error-handling must agree.
- `rules/core/validation/golangci-lint` — no rule bans `fmt.Println` today; the
  release checklist (`/checklist-release`) gates "structured logging, not
  fmt.Println" manually.
