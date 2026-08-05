---
name: recipe-desktop-app
description: "Minimal testable Go side of a Wails v3 desktop app (Go + web frontend). The bound methods (frontend-callable) are plain, tested Go; the GUI wiring is documented. Use when building a desktop app with Wails and you want the service logic unit-testable."
category: recipe
tags: [desktop, wails, tauri-alternative, bindings, frontend]
last-verified: 2026-08-05
---

# recipe-desktop-app — Wails v3 service (testable)

## Problem

Build a desktop app (Go + web frontend) where the frontend calls Go methods —
but keep those methods **unit-testable**, with no GUI/webview in the test suite.

## Solution (and the testability hinge)

Wails v3 binds a Go struct's **exported methods** to the frontend. Those methods
are ordinary Go — so write them as ordinary Go with NO dependency on the Wails
runtime, and test them directly. The Wails wiring (`application.New` + service
registration + the webview) is the untestable shell; it lives here as a reference
snippet, not as a compiled dependency.

[`app.go`](app.go) is a fully tested `App` (a notes service) whose methods
(`AddNote`, `Notes`, `DeleteNote`) are exactly what Wails would expose.

## ⚠ Wails v3 is Beta-to-GA, not stable (issue-mined)

Wails v3 is still in **Beta-to-GA transition** (#5844 release tracker, #4904
"v3 Setup Feedback" open). Implications for a kit consumer:

- **Pin the exact `wails3` version** — the binding/CLI surface is still churning.
- **Mobile is experimental** — Android/iOS support is now documented as
  experimental rather than unsupported. Keep the desktop boundary as the
  stable recipe target; evaluate mobile guides and platform requirements per
  exact release.
- **Platform build pain** — WebKitGTK (Linux) URI handler issues (#4412), webview2
  (Windows) version mismatches; CGO is mandatory.
- For production desktop where stability is critical today, v2 is the stable line
  until v3 GA lands — evaluate per release.

## The Wails wiring (NOT compiled in the kit — needs GUI/webview/CGO)

```go
// main.go — in your real Wails project, not in this test package.
import "github.com/wailsapp/wails/v3/pkg/application"

func main() {
    app := application.New(application.Options{
        Services: []application.Service{
            application.NewService(desktop.NewApp()), // ← the tested App
        },
        // Assets: fs.Sub(embedFS, "frontend/dist"),  // your embedded frontend
    })
    if err := app.Run(); err != nil { panic(err) }
}
```

Then generate the frontend bindings and run/build:

```sh
wails3 generate bindings   # → frontend/bindings/ (type-safe TS calling Go)
wails3 dev                 # dev server + hot reload
wails3 build               # single self-contained executable
```

From the frontend, a bound method is a normal async call:

```ts
import { AddNote } from './bindings/desktop/app'
const note = await AddNote("Buy milk")
```

## Why the package does not import Wails

Importing `github.com/wailsapp/wails/v3/pkg/application` drags in the webview /
platform bindings, which require **CGO + a native GUI toolkit** and break
cross-platform `go test ./...`. The kit's validation gate must run anywhere, so
the testable Go (your service logic) carries zero Wails imports. This mirrors
`recipe-sqlite-sqlc` (the generated `*Queries` stand-in is testable; the sqlc
tooling is documented, not compiled).

## Design rules for a Wails service

- **Stateless HTTP-like methods** are ideal (input → output). Stateful is fine
  but guard it (`sync.Mutex`) — the frontend may fire concurrent calls.
- **Validate inputs in Go**, return `error`. The frontend can ignore errors; Go
  is the trust boundary.
- **Return value types** (`Note` here) get JSON tags — they cross the binding as
  JSON.
- **Don't put I/O you can't test in the bound method.** Factor it out; bind a
  thin wrapper.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Import Wails and compile a real app | Breaks portable `go test`; the webview/CGO dep doesn't belong in the kit. |
| Tauri (Rust) | Different language; not a Go recipe. |
| Fyne / Gio (pure-Go GUI) | Native-Go GUI, no web frontend; a different model — viable recipe if needed, not this one. |

## Verify the behavior (observable)

Run the Wails app with `wails3 dev`, click the note input, type `Buy milk`, and
submit. Observe the new note in the list. Delete it and observe that it
vanishes. Also try an empty note and observe a visible validation error. A
successful Go gate does not prove the webview binding works, so perform this
interaction against the real desktop app.

## Run the tests

```sh
go test ./recipes/recipe-desktop-app/...
```
