---
name: errors
description: "Universal Go error-handling rules — the sentinel-vs-typed-vs-opaque decision, wrapping with %w, matching with errors.Is/As, and the handle-once principle. Loaded every session. Use whenever writing or reviewing code that returns, wraps, or handles an error."
category: rule
tags: [errors, universal, core, wrapping, sentinels]
last-verified: 2026-08-02
---

# errors — handling errors once, at the right layer

## The basics (always)

- **Wrap with context**: `fmt.Errorf("create user: %w", err)` — never `%v`
  (loses the chain; `errors.Is`/`As` then stop working).
- **Match, don't compare**: `errors.Is(err, ErrNotFound)`,
  `errors.As(err, &target)` — never `err == ErrFoo` (fails across wrap layers)
  and never a bare type assertion.
- **Never swallow** an error you don't own: `_ = f()` is acceptable only with an
  inline justification (see `rules/core/validation/golangci-lint` on `//nolint:errcheck`).

These are the *decision rules* behind the kit's one-line wrap/match/never-swallow
conventions: this module answers *which* error shape to export and *where* to
handle it.

## The decision rule — sentinel vs. type vs. opaque

Before exporting an error, decide which of three it is. Default to the **least**
surface that a caller actually needs:

| Pattern | When to use | When NOT |
| --- | --- | --- |
| **Sentinel** — `var ErrNotFound = errors.New("not found")` | A caller needs to **branch** on this specific condition (`errors.Is`), and the condition is part of your package's contract. One or two per package, named. | Don't mint a sentinel for every message; a forest of `Err*` is noise callers never match. |
| **Custom type** — `type ValidationError struct{...}` implementing `error` | The caller needs **structured data** from the error (a list of field failures, a code). Matched with `errors.As`. | Don't build a type when `errors.Is` on a sentinel would do — the type adds API to learn. |
| **Opaque / wrapped only** — return `fmt.Errorf("...: %w", err)` with no exported sentinel | The caller can't usefully branch; it only needs to log/handle generically. **This is the default for most internal layers.** | Not when a caller genuinely needs to distinguish (then you owe them a sentinel or type). |

**Lean toward opaque.** Exporting a sentinel/type is expanding your package's
public surface (see `AGENTS.md` Limits — "ask first" for a contract change).
Add one only when a real caller needs to act on it, and name *why* in the doc
comment, not just *what*.

```go
// Package-level sentinel, when a caller must branch on it.
var ErrNotFound = errors.New("not found")

// Opaque wrapping in an internal layer — no new surface.
func (s *Store) Get(ctx context.Context, id int) (Item, error) {
    // ... db miss ...
    return Item{}, fmt.Errorf("get item %d: %w", id, ErrNotFound)
}
```

## Handle once, at the layer with enough context

An error should be **handled in exactly one place**: the layer that can do
something about it (translate it to an HTTP status, retry, fail the job).
Every layer above it **wraps and returns** — it does not log the same error it
also returns.

The anti-pattern: each layer logs *and* returns, so one failure produces N log
lines and a stack of redundant messages. Logging an error you are about to
return is double-handling.

```go
// WRONG — logs and returns; the caller will log again.
func (s *Store) Get(ctx context.Context, id int) (Item, error) {
    item, err := s.db.Get(ctx, id)
    if err != nil {
        slog.Error("get failed", "id", id, "err", err) // double-handling
        return Item{}, fmt.Errorf("get: %w", err)
    }
    return item, nil
}

// RIGHT — wrap and return; the boundary layer logs once (or not at all).
func (s *Store) Get(ctx context.Context, id int) (Item, error) {
    item, err := s.db.Get(ctx, id)
    if err != nil {
        return Item{}, fmt.Errorf("get item %d: %w", id, err)
    }
    return item, nil
}
```

The **boundary** (HTTP handler, CLI command, job entry) is where the error is
finally handled: mapped to a status code / exit code / logged at `Error`. Below
the boundary, wrap and return. Log-level discipline (`Error` for actual
failures the boundary cannot recover from) is a logging concern, not an
error-shape concern.

## Anti-patterns

- `fmt.Errorf("...: %v", err)` — breaks the error chain.
- `err == ErrFoo` after wrapping — always false across a `%w` layer.
- Exporting a sentinel "just in case" — surface you can't take back.
- Logging the same error at every layer — double-handling.
- Returning `nil` to hide an error ("it's probably fine") — data loss.

## Cross-references

- `rules/core/validation/golangci-lint` — `errcheck` makes unchecked returns a gate
  failure; wrapcheck-style discipline is enforced by the wrap-with-`%w` habit.
- The handle-once rule and log-level discipline agree: below the boundary, wrap
  and return; only the boundary layer logs at `Error`.
