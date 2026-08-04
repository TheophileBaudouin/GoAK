---
name: fyne
description: "fyne.io/fyne v2.8 — pure-Go-API GUI toolkit for desktop, mobile, and embedded (OpenGL rendering via cgo glfw). Use when building a desktop app without a web frontend (no browser dependency) and you accept CGO; prefer Wails when a web frontend is desired."
category: library
tags: [gui, desktop, cross-platform, cgo, embedded]
last-verified: 2026-08-04
---

# fyne — pure-Go GUI toolkit

## Selection

[`fyne.io/fyne/v2`](https://github.com/fyne-io/fyne) (v2.8.0, Go 1.22+,
BSD-3-Clause, ~28.5k★, pushed 2026-08-04).

**Why it passes the gate** (actual reason, not stars): a single-responsibility
GUI toolkit (canvas, layout, widgets, windowing) with a deterministic testable
surface (`fyne.io/fyne/v2/test` package drives the app without a display). It
is the main **browser-free** desktop option in Go — the counterpart to Wails
(web frontend). Actively maintained (v2.8.0 = "biggest release since v2.0.0":
hardware acceleration, new canvas objects).

## Admission checklist

- [x] Actively maintained — v2.8.0 (2026), steady cadence (2.6/2.7/2.8)
- [x] Single responsibility — GUI toolkit (canvas, layout, widgets)
- [x] Idiomatic Go — canvas/widget API, `test` package for headless tests
- [x] Tests present + CI — yes
- [x] Documentation — fyne.io docs + examples
- [x] Real-world usage — large community, many desktop apps
- [x] Readable end-to-end — yes, layered and navigable
- [x] Justified by need — pure-Go GUI with no browser dependency

## ⚠ CGO requirement (limit, not a pass)

Fyne renders via OpenGL through cgo (`go-gl/glfw`). Cross-compilation and
static builds require CGO discipline. The kit's zero-CGO preference applies to
*alternatives with a pure-Go equivalent* (SQLite: modernc > mattn); for GUI
toolkits every real option (Wails, Fyne) touches native code. Choose Fyne when
a browser-free desktop app justifies CGO; otherwise prefer Wails.

## Minimal use

```go
package main

import "fyne.io/fyne/v2/app"
import "fyne.io/fyne/v2/widget"

func main() {
    a := app.New()
    w := a.NewWindow("Hello")
    w.SetContent(widget.NewLabel("Hello Fyne!"))
    w.ShowAndRun()
}
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Wails (web frontend) | Different trade-off: Go backend + web UI, no CGO in the Go service logic. Choose per frontend need. |
| Gio (gioui.org) | Immediate-mode GPU GUI, zero-CGO option; smaller ecosystem and docs than Fyne. |
| electron via webview | Heavy; Fyne avoids the browser runtime. |

## Notes

- The `test` package renders widgets headlessly — keep UI logic in
  deterministic functions, drive them via `test`, and keep wiring minimal.
- Desktop-only recipes in this kit use Wails (see `recipe-desktop-app`);
  Fyne is the documented alternative when no web frontend is wanted.

## Utiliser cette librairie quand

- Construire une application desktop sans frontend web (pas de dépendance
  navigateur) et accepter le CGO.
- Un toolkit GUI complet en API Go pure (canvas, layout, widgets, windowing).
- Des tests headless déterministes via le package `test` (sans affichage).

## Ne pas utiliser cette librairie quand

- Un frontend web est souhaité : préférer Wails (`recipe-desktop-app`) —
  logique Go sans CGO.
- Le zéro-CGO est une exigence absolue (Fyne rend via OpenGL/cgo glfw).
- Le besoin est une TUI ou un CLI : hors périmètre (bubbletea/wish).

## Avantages

- API Go pure pour le GUI, écosystème complet et communauté large (~28.5k★).
- Package `test` : rendu headless déterministe, UI testable sans display.
- Active maintenance : v2.8.0 = plus grosse release depuis v2.0.0
  (accélération matérielle, nouveaux objets canvas).
- Couvre desktop, mobile et embedded.

## Inconvénients

- **CGO obligatoire** (OpenGL via go-gl/glfw) : cross-compilation et builds
  statiques exigent une discipline CGO.
- Plus lourd qu'une TUI : il faut accepter le runtime GUI.
- Alternative Gio (gioui.org) : mode immédiat, zéro-CGO, mais écosystème et
  docs plus petits.

## Pièges connus

- Garder la logique UI dans des fonctions déterministes et piloter via `test` —
  le wiring minimal ; ne pas mettre la logique métier dans les callbacks de
  widgets.
- Le CGO n'est pas une option : l'accepter explicitement avant de choisir Fyne
  (le zéro-CGO du kit s'applique aux alternatives pur-Go, pas aux toolkits GUI).
- Pinner `v2` (fyne.io/fyne/v2) ; vérifier la compatibilité des assets
  (images/fonts) entre versions majeures.

## Sources vérifiées

- [fyne-io/fyne (repo officiel, v2.8.0)](https://github.com/fyne-io/fyne) —
  vérifié 2026-08-04
- [docs.fyne.io](https://docs.fyne.io/) — vérifié 2026-08-04
- Artefact interne : `recipe-desktop-app` (choix Wails vs Fyne documenté)
