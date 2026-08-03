---
name: templ
description: "a-h/templ — compiled, type-safe HTML templates for Go (alternative to html/template). Use when rendering HTML server-side and you want compile-time type safety and XSS-safe auto-escaping, with component composition."
category: library
tags: [html, template, type-safe, xss, components]
last-verified: 2026-08-02
---

# templ — type-safe HTML templates

## Selection

`a-h/templ` (10.4k★, pushed 2026-07, CI with `ensure-generated`/`ensure-fmt`,
goreleaser releases).

**Actual reason (not stars):** it compiles `.templ` files to real Go
(`*_templ.go`) so the **compiler** catches type mismatches and bad signatures at
build time — unlike `html/template`'s runtime evaluation. Dynamic content is
auto-HTML-escaped by default (XSS-safe).

## Build integration

`.templ` is NOT runnable Go — it must be generated first.

```sh
templ generate              # parses .templ → emits *_templ.go
templ generate --watch      # dev: regenerate on change
templ generate --proxy=:8080 --watch   # + live reload via SSE
```

Wire `go:generate` so `go generate ./...` stays the single build entry point:

```go
//go:generate templ generate
```

## Component composition

```templ
templ Page(title string, children ...templ.Component) {
    <html><head><title>{title}</title></head>
    @children...
    </html>
}
templ Greeting(name string) {
    <p>Hello, {name}</p>
}
```

Compose via `@Component(...)`, pass children with `children...`, aggregate with
`templ.Join`. Exported (capitalised) components are importable across packages.

## Render to an http.ResponseWriter

```go
templ.Handler(Greeting("world)).ServeHTTP(w, r)
// or, for control:
comp := Greeting("world")
comp.Render(ctx, w)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `html/template` | No dependency, runtime-evaluated (type errors at run time). Fine for small/dynamic templates. |
| `gomarkup`/Jet/etc. | Other engines; templ's compiled-type-safety is its differentiator. |
| Client-side React/Vue | Different deployment model; templ is server-side render only. |
