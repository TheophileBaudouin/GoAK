---
name: harmonica
description: "github.com/charmbracelet/harmonica — simple physics-based spring animation library for Go TUIs. Use when animating terminal UI motion (easing, spring, linear/quadratic curves) instead of hand-rolling easing math."
category: library
tags: [tui, animation, physics, easing, terminal]
last-verified: 2026-08-04
---

# harmonica — Spring animation for TUIs

## Selection

[`github.com/charmbracelet/harmonica`](https://github.com/charmbracelet/harmonica).

**Why it passes the gate** (actual reason, not stars): it solves one narrow,
commonly botched problem — frame-rate-independent easing — with a tiny API
(springs, `Linear`/`Quadratic`/`Cubic`/`Exponential` curves, `FPS`-driven
advance). The math (damping, stiffness) is already validated and tested; the
package is stable and dependency-free.

## Admission checklist

- [x] Actively maintained — commits 2026, stable v0.2 API
- [x] Single responsibility — physics-based easing
- [x] Idiomatic Go — small pure functions, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README with usage
- [x] Real-world usage — part of the Charm TUI ecosystem
- [x] Readable end-to-end — yes, tiny
- [x] Justified by need — easing math is easy to get subtly wrong

## Minimal use

```go
spring := harmonica.NewSpring(harmonica.FPS(60), 0.8, 0.5) // damping, stiffness
for !spring.IsSettled() {
    value := spring.Update(1.0)
    renderAt(value) // interpolate position/alpha with the spring value
}
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Hand-rolled easing | Fine for one hardcoded curve; springs and fps-independence are the error-prone part this package covers. |
| `golang.org/x/exp/shiny` anim | Experimental, unrelated scope. |

## Notes

- Drive updates from `tea.Tick` in Bubble Tea, never from blocking sleeps.
- Keep springs short (0.5-1.0s); terminal redraws are cheap but visible.
