---
name: recipe-rest-chi
description: "Build a minimal idiomatic REST API with the chi v5 router — composable middleware, route groups, path parameters, and JSON in/out. Use when creating or reviewing a Go HTTP/REST service with chi."
category: recipe
tags: [rest, http, chi, router, middleware, json]
last-verified: 2026-08-05
---

# recipe-rest-chi — REST API with chi

## Problem

Build a Go HTTP REST service with composable middleware, grouped routes, path
parameters, and JSON request/response — without locking into a framework that
invents its own handler signatures.

## Solution

[`github.com/go-chi/chi/v5`](https://github.com/go-chi/chi) v5.3.1 — a
lightweight router that is **100% compatible with `net/http`** (~1000 LOC, zero
external dependencies). Handlers and middleware are plain
`http.HandlerFunc` / `func(http.Handler) http.Handler`, so any community
`net/http` middleware works unchanged.

```go
r := chi.NewRouter()
r.Use(middleware.RequestID, middleware.Logger, middleware.Recoverer)
r.Route("/items", func(r chi.Router) {
    r.Get("/", listItems)         // GET  /items
    r.Post("/", createItem)       // POST /items
    r.Get("/{id}", getItem)       // GET  /items/{id}
})
if err := http.ListenAndServe(":3333", r); err != nil {
    return fmt.Errorf("serve REST API: %w", err)
}
```

Path params come from `chi.URLParam(r, "id")`; request bodies are decoded with
the stdlib `encoding/json`. See [`server.go`](server.go) for the full
thread-safe example backing store.

## Why chi (and the stdlib boundary)

As of **Go 1.22**, the stdlib `net/http.ServeMux` gained method+path patterns
(`mux.HandleFunc("GET /items/{id}", ...)`) and `r.PathValue("id")`. For a
truly minimal API with no middleware composition, **the stdlib now suffices** —
prefer it (see the ladder in `rules/core/philosophy`).

Reach for chi when you need its extra leverage:

- **Composable middleware** (`r.Use`, `r.With`) and inline middleware chains.
- **Route groups / sub-routers** (`r.Route`, `r.Mount`) to decompose a large API.
- **Stable, mature** middleware catalogue (`RequestID`, `Recoverer`, `Throttle`,
  `ClientIPFrom*`, ...).

| Alternative | Verdict |
| --- | --- |
| `net/http` 1.22+ ServeMux | Correct minimal choice when middleware/groups aren't needed. |
| gin / echo | `net/http`-incompatible: own `Context`, own handler signatures, opaque. Couples you to the framework. |
| gorilla/mux | Heavier, less idiomatic middleware composition than chi; its mux has been deprecated/moved. |

## Security note

chi's legacy `middleware.RealIP` is **deprecated** — it is vulnerable to IP
spoofing (GHSA-3fxj-6jh8-hvhx and others). Use one of the `ClientIPFrom*`
middlewares instead, picked to match your deployment (direct internet, behind
nginx/Cloudflare, behind known proxy CIDRs).

## Reference

- `github.com/go-chi/chi/v5` — v5, built for Go 1.23+, in production at
  Cloudflare, Heroku, 99Designs. `net/http`-pure, ~1000 LOC.

## Verify the behavior (observable)

From a small `main` that calls `NewStore().Router()` and listens on `127.0.0.1:3333`:

```sh
curl -i -X POST http://127.0.0.1:3333/items/ \
  -H 'Content-Type: application/json' -d '{"name":"coffee"}'
curl -s http://127.0.0.1:3333/items/1
```

Observe `201 Created` and then `{"id":1,"name":"coffee"}`. This checks the
finished HTTP behavior; a green unit-test suite alone does not.

## Run the tests

```sh
go test ./recipes/recipe-rest-chi/...
```

The test suite exercises the handlers in memory. It does not replace the
observable HTTP check above.
