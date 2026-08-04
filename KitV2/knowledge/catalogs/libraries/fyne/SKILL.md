---
name: fyne
description: "fyne.io/fyne/v2 v2.8.0 — pure-Go API for desktop, mobile, and embedded GUI applications using OpenGL/GLFW. Use when a native GUI without a web frontend is required and CGO is acceptable; prefer Wails for web-based desktop UI."
category: library
tags: [gui, desktop, mobile, embedded, fyne, cgo]
last-verified: 2026-08-05
---

# fyne — toolkit GUI Go

## Selection

[`fyne.io/fyne/v2`](https://github.com/fyne-io/fyne) v2.8.0 is a Go GUI
toolkit for desktop, mobile, and embedded applications. It provides a native
widget/canvas model and uses OpenGL through GLFW. It is admitted for its focused
cross-platform GUI API, maintained releases, tests, documentation, and real
use; it is not a zero-CGO solution.

## Admission checklist

- [x] Current stable release v2.8.0, minimum Go 1.22.
- [x] Single responsibility: cross-platform GUI toolkit.
- [x] Pure-Go application API with a CGO/OpenGL rendering boundary.
- [x] Tests, CI, documentation, and examples are maintained.
- [x] Desktop/mobile/embedded usage is established in the Fyne ecosystem.

## Minimal use

```go
func show() {
    app := fyneapp.New()
    window := app.NewWindow("GoAK")
    window.SetContent(widget.NewLabel("hello"))
    window.ShowAndRun()
}
```

The rendering loop is platform-bound and is not the kit's portable Go test
surface. Keep application/service logic in ordinary Go packages and wire Fyne
at the edge.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Wails | Prefer when the desktop UI is a web frontend and the Go service boundary should remain portable. |
| Gio | Consider for an immediate-mode GPU GUI when its ecosystem and API fit. |
| Web application | Prefer when browser deployment or web accessibility matters more than a native window. |

## Utiliser cette librairie quand

- A native desktop, mobile, or embedded GUI is required without a browser UI.
- The project accepts OpenGL/GLFW, CGO, platform toolchains, and native packaging.
- Widgets, canvas objects, notifications, and platform windows are the desired
  abstraction.

## Ne pas utiliser cette librairie quand

- Zero-CGO cross-compilation is a hard requirement.
- A web frontend is desired: use Wails or a browser deployment boundary.
- The application is primarily a server/service with no native GUI.
- The target platform is outside Fyne's tested driver and packaging support.

## Avantages

- One Go API across desktop, mobile, and embedded targets.
- Widget and canvas abstractions avoid hand-building native event loops.
- v2.8 adds richer canvas objects, scheduled notifications, accessibility
  support, window positioning, and default Wayland support.

## Inconvénients

- OpenGL/GLFW makes CGO and a native compiler part of the build/deployment
  story.
- Cross-compilation requires `CGO_ENABLED=1` and a target C compiler.
- Platform behavior and GUI rendering need host-level tests beyond portable
  `go test`.

## Pièges connus

- Do not claim a Fyne package is zero-CGO: the rendering driver uses OpenGL and
  GLFW.
- Keep Fyne imports at the UI boundary; test validation and domain logic
  without creating a window.
- Check the target OS support and native dependencies before choosing the
  toolkit; v2.8 dropped old Windows/macOS versions.
- Treat accessibility as an explicit feature decision; v2.8 support is off by
  default and requires its documented build configuration.

## Sources vérifiées

- [Official Fyne repository](https://github.com/fyne-io/fyne) — maintenance,
  architecture, license, checked 2026-08-05.
- [Fyne v2.8.0 release](https://github.com/fyne-io/fyne/releases/tag/v2.8.0)
  — exact version, API changes, minimum Go and OS changes, checked 2026-08-05.
- [Fyne v2 on pkg.go.dev](https://pkg.go.dev/fyne.io/fyne/v2) — API and module
  metadata, checked 2026-08-05.
- [Fyne cross-compilation guidance](https://github.com/fyne-io/developer.fyne.io/blob/master/started/cross-compiling.md)
  — CGO/toolchain requirements, checked 2026-08-05.
- [Fyne documentation](https://docs.fyne.io/) — supported GUI model, checked
  2026-08-05.
