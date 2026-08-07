---
name: robotgo
description: "github.com/go-vgo/robotgo v1.x — cross-platform desktop automation for mouse, keyboard, screenshots, and screen in Go; on macOS cgo by default with a purego build via -tags purego. Use as the physical input/execution layer of macOS computer-use agents, paired with AXUIElement; not for semantic UI understanding."
category: library
tags: [desktop-automation, computer-use, macos, mouse, keyboard, screenshot, automation]
last-verified: 2026-08-07
---

# robotgo — desktop automation (input + screen)

## Selection

[`github.com/go-vgo/robotgo`](https://github.com/go-vgo/robotgo) is a
cross-platform desktop automation library: mouse movement/clicks, keyboard
input, text typing, screenshots, screen info, and clipboard. It is admitted
as the physical input layer of a macOS computer-use stack, paired with the
semantic layer (AXUIElement — see
`knowledge/architecture/macos-computer-use`).

## Admission checklist

- [x] Actively maintained: v1.0.0 (2025-12-04), v1.0.2 (2026-03-30),
  v2.0.0-beta2 (2026-07-29); commits July 2026.
- [x] Single clear responsibility: desktop automation (input synthesis and
  screen capture).
- [x] Readable, idiomatic Go: small API surface over darwin/windows/linux
  layers; the macOS path defaults to cgo and supports a purego build.
- [x] Tests present: 9 `_test.go` files, including darwin.
- [x] CI configured: `.github/workflows/go.yml`.
- [x] Documentation: README + pkg.go.dev.
- [x] Evidence of real-world usage: 10.7k stars, long-standing use in
  automation tooling.
- [x] Small enough to read end-to-end: 105 `.go` files; accepted because the
  API surface is small and the macOS path is self-contained.
- [x] Star count is explicitly NOT sufficient — the reasons above are:
  active releases, CI, tests, docs, and real usage.

## Minimal use

```go
// illustrative — requires a live GUI session, not part of the kit gate.
robotgo.Move(500, 300) // move the mouse
robotgo.Click()        // click at the current position
robotgo.TypeStr("hello")
```

Input synthesis needs macOS Accessibility (TCC) permission; screen capture
needs Screen Recording permission.

## Alternatives considered

| Alternative | Verdict |
| --- | --- |
| AXUIElement (native) | Primary semantic layer — never replace it with coordinates. |
| darwinkit (progrium) | AXUIElement bindings (cgo); NOT admitted — stale (last release v0.5.0, 2024-07). |
| robotn/gohook | Event *listening* only, not input synthesis. |
| Hand-written CGEvent cgo | Full control; use only when RobotGo's API is insufficient. |

## When to use this library

- The execution layer of a macOS computer-use agent, driven by AXUIElement
  semantics (click the element RobotGo points at).
- Cross-platform desktop automation where `-tags purego` keeps the build
  free of a cgo toolchain (`CGO_ENABLED=0` compatible on macOS).
- Automated UI workflows needing mouse/keyboard synthesis or screenshots.

## When NOT to use this library

- Semantic UI understanding: that is AXUIElement's job, not coordinates.
- Event listening only: use gohook (robotn) instead.
- Server or non-GUI workloads: no screen session, no input synthesis.

## Advantages

- Active stable line (v1.x) plus a v2 beta; Apache-2.0.
- Simple API; cross-platform (macOS, Windows, Linux, BSD).
- macOS purego build: no Xcode required, works with `CGO_ENABLED=0`.
- Screenshots and OCR hooks for verification loops.

## Disadvantages

- Event-level only — no semantic UI model; coordinates alone are fragile.
- v2.0.0 is beta; API may shift — pin v1.x for production.
- Broad scope (105 `.go` files) vs. a minimal-purpose library.
- macOS defaults to cgo (CoreGraphics); purego requires the build tag.

## Known pitfalls

- Do not use as the sole computer-use mechanism — pair with AXUIElement.
- Default macOS build is cgo (`robotgo_mac.go`); use `-tags purego` for a
  cgo-free build and verify the input path still suits the use case.
- macOS permissions are mandatory (TCC): Accessibility for input synthesis,
  Screen Recording for capture — missing permission fails silently or at
  first call.
- v2 is beta: pin the latest stable v1.x tag in go.mod.
- Root `robotgo.go` still carries cgo paths for non-purego builds; always
  check which build tag the target platform resolves to.

## Verified sources

- [Official RobotGo repository](https://github.com/go-vgo/robotgo) —
  maintenance, releases, build tags, CI, license; checked 2026-08-07.
- [RobotGo releases](https://github.com/go-vgo/robotgo/releases) — v1.0.0
  (2025-12-04), v1.0.2 (2026-03-30), v2.0.0-beta2 (2026-07-29); checked
  2026-08-07.
- [RobotGo on pkg.go.dev](https://pkg.go.dev/github.com/go-vgo/robotgo) —
  API and module metadata; checked 2026-08-07.
- [RobotGo README — purego build](https://github.com/go-vgo/robotgo)
  — `-tags purego` documentation ("no Xcode required", CGO_ENABLED=0);
  checked 2026-08-07.
- [Apple Accessibility API](https://developer.apple.com/documentation/accessibility)
  — semantic UI layer this library pairs with; checked 2026-08-07.
