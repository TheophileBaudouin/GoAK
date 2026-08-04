---
name: harmonica
description: "github.com/charmbracelet/harmonica v0.2.0 — framework-agnostic spring and projectile physics for Go animations. Use when a TUI or UI needs damped motion math; not for rendering, easing catalogs, or a full animation framework."
category: library
tags: [animation, physics, spring, tui, charm]
last-verified: 2026-08-05
---

# harmonica — physique d'animation

## Selection

[`github.com/charmbracelet/harmonica`](https://github.com/charmbracelet/harmonica)
v0.2.0 is a small MIT-licensed math library for damped spring and projectile
motion. It is framework-agnostic: the caller advances the simulation and maps
its result to a UI. It is admitted for this focused utility and tests in the
Charm ecosystem, with the low release velocity recorded honestly.

## Admission checklist

- [x] Stable tagged release v0.2.0; later upstream commits are not a new tag.
- [x] Single responsibility: spring/projectile simulation.
- [x] No rendering framework or hidden global state.
- [x] Go package documentation and tests exist.
- [x] Useful when a consumer needs physical motion rather than a generic tween.

## Minimal use

```go
func step(spring harmonica.Spring, position, velocity float64) (float64, float64) {
    return spring.Update(position, velocity, 0)
}
```

Create a spring with `NewSpring(deltaTime, angularFrequency, dampingRatio)`;
call `Update` once per frame and render the returned position. `Projectile`
provides the corresponding constant-acceleration model.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Bubble Tea commands/ticks | Use for event scheduling; harmonica supplies only the motion calculation. |
| Generic easing/tween library | Use when fixed easing curves, not physical spring behavior, are required. |
| Ebitengine/Pixi-like UI framework | Use when the project needs rendering and a full game/UI loop. |

## Utiliser cette librairie quand

- A UI animation needs a damped spring, gravity, or projectile trajectory.
- The application wants deterministic per-frame math independent of its renderer.
- Multiple UI frameworks should be able to consume the same motion calculation.

## Ne pas utiliser cette librairie quand

- The project needs rendering, event scheduling, or an animation timeline.
- Fixed easing curves are enough and a physics model adds needless state.
- The project requires a maintained feature-rich animation framework rather than
  a small math utility.

## Avantages

- Tiny, framework-agnostic API with explicit per-frame state.
- Spring parameters map directly to physical behavior.
- Can be tested without a terminal, window, or renderer.

## Inconvénients

- Low-velocity release cadence: v0.2.0 remains the latest tag.
- No rendering, easing catalog, interpolation helpers, or lifecycle manager.
- One spring instance models one spring; consumers manage collections and frame
  scheduling themselves.

## Pièges connus

- Advance with a stable `deltaTime`; inconsistent frame steps change the motion.
- Keep one simulation state per animated value and persist position/velocity
  between frames.
- Choose damping and angular frequency from the desired behavior; do not treat
  the library as a generic zero-configuration tween.
- Pin v0.2.0 and review the pseudo-version separately if consuming unreleased
  changes.

## Sources vérifiées

- [Official harmonica repository](https://github.com/charmbracelet/harmonica) —
  maintenance, license, checked 2026-08-05.
- [harmonica on pkg.go.dev](https://pkg.go.dev/github.com/charmbracelet/harmonica)
  — exact tagged version and API, checked 2026-08-05.
- [Spring implementation](https://github.com/charmbracelet/harmonica/blob/master/spring.go)
  — state/update behavior, checked 2026-08-05.
- [Projectile implementation](https://github.com/charmbracelet/harmonica/blob/master/projectile.go)
  — projectile boundary, checked 2026-08-05.
- [harmonica releases](https://github.com/charmbracelet/harmonica/releases) —
  tagged-release status, checked 2026-08-05.
