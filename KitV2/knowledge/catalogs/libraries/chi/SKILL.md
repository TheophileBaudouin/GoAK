---
name: chi
description: "go-chi/chi v5 — a lightweight HTTP router 100% compatible with net/http, for composable middleware, route groups, and path params. Use when choosing a Go HTTP router or building/maintaining a chi-based REST API."
category: library
tags: [http, router, middleware, rest]
last-verified: 2026-08-02
---

# chi — HTTP router

## Selection

[`github.com/go-chi/chi/v5`](https://github.com/go-chi/chi) (v5, Go 1.23+).

**Why it passes the gate** (actual reason, not stars): it is a ~1000-LOC router
that is **100% compatible with `net/http`** — handlers are plain
`http.HandlerFunc`, middleware are plain `func(http.Handler) http.Handler`. That
means zero vendor lock-in: any `net/http` middleware in the ecosystem works
unchanged. It adds composable middleware (`Use`/`With`), route groups
(`Route`/`Mount`), and path parameters over the stdlib, without inventing a
framework-specific `Context`.

## Admission checklist

- [x] Actively maintained — v5, built for Go 1.23+, recent commits/releases
- [x] Single responsibility — HTTP routing + optional middleware catalogue
- [x] Idiomatic Go — stdlib `net/http` signatures, no magic
- [x] Tests present + CI — yes
- [x] Documentation — README + `_examples/`
- [x] Real-world usage — Cloudflare, Heroku, 99Designs
- [x] Readable end-to-end — ~1000 LOC core
- [x] Justified by need (router + middleware composition), NOT popularity

## Minimal use

```go
r := chi.NewRouter()
r.Use(middleware.RequestID, middleware.Logger, middleware.Recoverer)
r.Get("/items/{id}", getItem)        // chi.URLParam(r, "id")
http.ListenAndServe(":3333", r)
```

See `recipe-rest-chi` for a runnable, tested example.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `net/http` ServeMux (Go 1.22+) | **Correct minimal choice** when you need method+path routing but NOT middleware composition or route groups. The stdlib boundary: prefer it until chi's leverage pays for the dependency. |
| gin / echo | `net/http`-incompatible (own `Context`, own signatures). Couples handlers to the framework; rejected for a kit that values portability. |
| gorilla/mux | Heavier; weaker middleware-composition story than chi; the mux was archived/moved. |

## Security note

`middleware.RealIP` is **deprecated** — vulnerable to IP spoofing
(GHSA-3fxj-6jh8-hvhx et al.). Use exactly one `ClientIPFrom*` middleware matching
your deployment (direct internet → `ClientIPFromRemoteAddr`; behind nginx/
Cloudflare → `ClientIPFromHeader`; behind known proxy CIDRs → `ClientIPFromXFF`).
