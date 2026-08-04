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

## Utiliser cette librairie quand

- Animer du mouvement TUI (position, alpha, taille) avec un easing
  indépendant de la fréquence d'images.
- Besoin de ressorts physiques (damping, stiffness) validés et testés plutôt
  que de la math d'easing maison.
- Le rendu est piloté par `tea.Tick` dans Bubble Tea.

## Ne pas utiliser cette librairie quand

- Une seule courbe codée en dur suffit (easing maison acceptable).
- La TUI n'a pas de boucle d'animation (sortie statique).

## Avantages

- Tiny API, zéro dépendance, pure : springs + courbes
  (Linear/Quadratic/Cubic/Exponential).
- Easing frame-rate-independent (FPS-driven) : le problème le plus souvent
  raté est résolu et testé.
- Stable (v0.2), maintenance active, écosystème Charm.

## Inconvénients

- Surface très étroite : animation physique seulement, pas de moteur de
  transition d'écran.
- Pas de gestion du temps global : le driver (tea.Tick) reste à écrire.

## Pièges connus

- Piloter les mises à jour depuis `tea.Tick`, jamais depuis des `sleep`
  bloquants.
- Garder des ressorts courts (0.5–1.0 s) : les redraws terminal sont visibles.
- Vérifier `IsSettled()` pour terminer l'animation et libérer la boucle.

## Sources vérifiées

- [charmbracelet/harmonica (repo officiel)](https://github.com/charmbracelet/harmonica)
  — vérifié 2026-08-04
- Artefact interne : catalog `bubbletea` (driver tea.Tick)
