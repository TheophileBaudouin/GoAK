---
name: chi
description: "github.com/go-chi/chi/v5 v5.3.1 — lightweight net/http-compatible router with composable middleware, groups, and path parameters. Use for Go HTTP services when ServeMux is too small; not for an all-in-one framework or API generation."
category: library
tags: [http, router, middleware, rest]
last-verified: 2026-08-05
---

# chi — routeur HTTP

## Selection

[`github.com/go-chi/chi/v5`](https://github.com/go-chi/chi) v5.3.1,
released 2026-07-06, adds composable routing on top of standard `net/http`:
plain handlers, middleware, groups, mounts, and path parameters. It is admitted
for this small, focused portability boundary, active maintenance, tests, and
real use; not for popularity.

## Admission checklist

- [x] Current v5.3.1 release and active upstream maintenance.
- [x] Single responsibility: HTTP routing and composable middleware helpers.
- [x] Handlers remain `http.Handler`/`http.HandlerFunc`; no framework context.
- [x] Tests, CI, documentation, and examples are present.
- [x] The dependency is justified only when ServeMux composition is insufficient.

## Minimal use

```go
func routes(handler http.Handler) http.Handler {
    r := chi.NewRouter()
    r.Use(middleware.RequestID, middleware.Recoverer)
    r.Get("/items/{id}", func(w http.ResponseWriter, req *http.Request) {
        id := chi.URLParam(req, "id")
        _, _ = io.WriteString(w, id) // response write is best-effort at this boundary
    })
    r.Mount("/", handler)
    return r
}
```

Use `recipe-rest-chi` for a complete server, JSON boundary, and test. The
standard library's `http.ServeMux` remains the smallest choice for simple
method/path routing.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `net/http` `ServeMux` | Prefer for simple method/path routing without chi's grouping or middleware composition. |
| gin / echo | Choose only when an application explicitly accepts framework-owned contexts and APIs. |
| gorilla/mux | Do not choose for new work without independent maintenance verification; chi keeps the net/http boundary smaller. |

## Utiliser cette librairie quand

- A Go HTTP service needs route groups, mounts, path parameters, and middleware
  composition while keeping standard `net/http` signatures.
- Existing net/http middleware must remain reusable without adapter code.

## Ne pas utiliser cette librairie quand

- `ServeMux` already covers the routing and middleware needs.
- The project wants an all-in-one framework with integrated validation, auth,
  rendering, or API generation.
- The project cannot accept a third-party router dependency.

## Avantages

- Standard handlers and middleware preserve portability and testability.
- Groups, mounts, method routes, and path parameters are compact to compose.
- The core is small compared with full HTTP frameworks.

## Inconvénients

- Authentication, validation, rendering, and API contracts remain application
  responsibilities.
- Middleware security depends on the deployment topology and selected helper.
- OpenAPI/client generation is outside chi's responsibility.

## Pièges connus

- Do not use deprecated `middleware.RealIP`: its trust behavior enabled IP
  spoofing. Use one `ClientIPFrom*` helper matching the actual proxy topology.
- Read parameters with `chi.URLParam`; do not parse path strings manually.
- Review redirect and proxy middleware advisories when upgrading; pin v5.3.1 or
  a later patched release.

## Sources vérifiées

- [Official chi repository](https://github.com/go-chi/chi) — API, maintenance,
  license, checked 2026-08-05.
- [chi v5.3.1 release](https://github.com/go-chi/chi/releases/tag/v5.3.1) —
  exact version, checked 2026-08-05.
- [chi on pkg.go.dev](https://pkg.go.dev/github.com/go-chi/chi/v5) — API and
  standard-library boundary, checked 2026-08-05.
- [RealIP advisory](https://github.com/go-chi/chi/security/advisories/GHSA-3fxj-6jh8-hvhx)
  — trust-boundary limitation, checked 2026-08-05.
- [RedirectSlashes advisory](https://github.com/go-chi/chi/security/advisories/GHSA-mqqf-5wvp-8fh8)
  — upgrade/security scope, checked 2026-08-05.
- [Compress issue #1074](https://github.com/go-chi/chi/issues/1074) — open
  middleware limitation, checked 2026-08-05.
