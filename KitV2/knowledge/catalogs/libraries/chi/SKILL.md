---
name: chi
description: "go-chi/chi v5 — a lightweight HTTP router 100% compatible with net/http, for composable middleware, route groups, and path params. Use when choosing a Go HTTP router or building/maintaining a chi-based REST API."
category: library
tags: [http, router, middleware, rest]
last-verified: 2026-08-04
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

## Utiliser cette librairie quand

- Construire une API REST Go avec composition de middleware, route groups et
  path params.
- L'interopérabilité `net/http` totale compte : handlers `http.HandlerFunc`,
  middleware `func(http.Handler) http.Handler`, aucun Context maison.
- Réutiliser l'écosystème middleware `net/http` existant sans adaptation.

## Ne pas utiliser cette librairie quand

- Le besoin est un simple routing méthode+path sans middleware ni groupes :
  `net/http` ServeMux (Go 1.22+) est le choix minimal correct.
- Un framework tout-en-un avec son propre `Context` est accepté (gin/echo —
  couplage handlers ↔ framework).
- Avant : gorilla/mux (projet archivé/migré, composition middleware plus
  faible que chi).

## Avantages

- 100 % compatible `net/http` : zéro lock-in, middlewares de l'écosystème
  réutilisables tels quels.
- Noyau compact (~1000 LOC), idiomatique, tests + CI.
- Middleware composables (`Use`/`With`), groupes (`Route`/`Mount`), path
  params — sans inventer de framework.
- Usage réel : Cloudflare, Heroku, 99Designs.

## Inconvénients

- Pas de génération de contrats/clients (OpenAPI à assembler soi-même).
- Pas un framework applicatif : auth, validation, rendu restent à composer.
- Le catalogue de middlewares fournis est inégal : certains ont eu des failles
  (RealIP) — les choisir en connaissance de cause.

## Pièges connus

- `middleware.RealIP` est déprécié et vulnérable au spoofing IP
  (GHSA-3fxj-6jh8-hvhx, GHSA-rjr7-jggh-pgcp, GHSA-9g5q-2w5x-hmxf) : utiliser
  exactement UN `ClientIPFrom*` selon la topologie (voir Security note +
  anti-pattern `pattern:antipattern:sec-ip-trust`).
- Lire les path params avec `chi.URLParam(r, "id")`, jamais manuellement.
- v5 exige Go 1.23+ — vérifier la version minimale du projet consommateur.

## Sources vérifiées

- [go-chi/chi (repo officiel, v5)](https://github.com/go-chi/chi) — vérifié
  2026-08-04
- [pkg.go.dev/github.com/go-chi/chi/v5/middleware](https://pkg.go.dev/github.com/go-chi/chi/v5/middleware)
  — vérifié 2026-08-04
- [Security advisory GHSA-3fxj-6jh8-hvhx](https://github.com/go-chi/chi/security/advisories/GHSA-3fxj-6jh8-hvhx)
  — vérifié 2026-08-04 (sécurité officielle)
- [PR #967 — middleware.ClientIP (remplace RealIP)](https://github.com/go-chi/chi/pull/967)
  — vérifié 2026-08-04
- Artefacts internes : `recipe-rest-chi`, `pattern:antipattern:sec-ip-trust`,
  `pattern:http:middleware-chain`
