# Evidence — macOS Computer Use resources (2026-08-07)

Raw data collected from primary sources via GitHub REST API and direct HTTP
checks, 2026-08-07. Verdicts in `docs/plans/2026-08-07-computer-use-macos.md`.

## RobotGo — github.com/go-vgo/robotgo

- Releases (latest first): v2.0.0-beta2 (2026-07-29), v2.0.0-beta1
  (2026-07-03), v1.0.2 (2026-03-30), v1.0.1 (2026-02-27), v1.0.0
  (2025-12-04), v0.110.8 (2025-05-17). 75 releases total.
- Repo meta: archived=false, pushed_at=2026-07-29, stargazers=10764,
  license=Apache-2.0.
- Commits: 2026-07-08 (merge #782 wayland-win), 2026-07-07 (merge #781).
- CI: `.github/workflows/go.yml`. Tests: 9 `_test.go`. Go files: 105.
- go.mod (master): module github.com/go-vgo/robotgo, go 1.25.0, requires
  ebitengine/purego v0.10.1, godbus/dbus, jezek/xgb, xgbutil,
  otiai10/gosseract, tailscale/win, vcaesar/go-wayland. go.mod v1.0.2:
  ebitengine/purego v0.10.0 (indirect).
- Build tags (macOS): `darwin.go` = `darwin && (mac || purego)` (purego
  entry, darwin/cg.go uses purego 31x); `robotgo_mac.go` =
  `darwin && !mac && !purego` = cgo fallback (`#include
  <CoreGraphics/CoreGraphics.h>`, `import "C"`). Default (no tags) = cgo.
- README: "macOS, Quartz/CoreGraphics loaded at runtime via purego (no
  Xcode required)" under tag `mac`; "Pure-Go default (all platforms)" under
  tag `purego`; `CGO_ENABLED=0 ... go build -tags "purego,x11"` example.

## darwinkit (ex-macdriver) — progrium/darwinkit

- Repo meta: archived=false, pushed_at=2025-03-08, stargazers=5431,
  license=MIT, default_branch=main.
- Last release v0.5.0 (2024-07-11); last commits 2024-06/07 (README);
  module github.com/progrium/darwinkit, go 1.18.
- 2,886 files; cgo-based (`.m` files); appkit accessibility_* generated
  bindings present; no ScreenCaptureKit bindings.
- Verdict: fails "actively maintained" (no release/commit for ~2 years).

## robotn/gohook

- v1.0.0-beta1 (2026-07-07), v0.42.3 (2025-12-04); pushed 2026-07-08;
  414 stars; MIT. Event hooking only (not input synthesis).

## Apple documentation URLs

- <https://developer.apple.com/documentation/accessibility> — HTTP 200
- <https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/Accessibility/cocoaAXOverview/cocoaAXOverview.html> — HTTP 200
- <https://developer.apple.com/documentation/screencapturekit> — HTTP 200
