---
name: scs
description: "github.com/alexedwards/scs/v2 v2.9.0 — server-side session management for net/http: cookie session ID + pluggable stores (cookie, Postgres, Redis, SQLite, MySQL). Use when choosing session/cookie auth for a classic web app. Not a full auth framework (no login/password logic) and requires CSRF protection on top."
category: library
tags: [security, sessions, cookies, authentication, web, middleware]
last-verified: 2026-08-05
---

# scs — sessions côté serveur (cookies)

## Selection

[`github.com/alexedwards/scs/v2`](https://github.com/alexedwards/scs)
(v2.9.0, MIT).

**Why it passes the gate** (actual reason, not stars): it is the modern,
actively maintained session manager for `net/http` — a session ID in an
HttpOnly cookie, session data stored server-side with pluggable stores, and a
`LoadAndSave` middleware. Zero security advisories, single responsibility,
maintained by Alex Edwards (auteur de « Let's Go »), adoption massif. C'est le
remplaçant rigoureux de `gorilla/sessions` (dormant depuis 2024-08, refusé à la
gate maintenance).

## Admission checklist

- [x] Actively maintained — v2.9.0 (2025-07-08), push 2025-11-20
- [x] Single responsibility — lifecycle de session côté serveur
- [x] Idiomatic Go — middleware net/http + store interface, no magic
- [x] Tests present + CI — yes (table-driven, httptest)
- [x] Documentation — godoc + README détaillé + exemples par store
- [x] Real-world usage — standard des apps web Go modernes
- [x] Readable end-to-end — small (~674 KB, layered), lisible par module
- [x] Justified by need — le besoin sessions cookies était couvert par un
      projet dormant (gorilla/sessions) ; scs = même besoin, maintenu ;
      NOT popularity

## Minimal use

```go
sm := scs.New()
sm.Lifetime = 24 * time.Hour
sm.Cookie.Secure = true          // HTTPS en production
sm.Cookie.SameSite = http.SameSiteLaxMode

h := sm.LoadAndSave(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    if v, ok := sm.Get(r.Context(), "user_id").(int); ok {
        fmt.Fprintf(w, "authed %d", v)
    }
}))
```

Compilé et vérifié (LoadAndSave + Get) avec v2.9.0 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `gorilla/sessions` | **Refusé** : dormant depuis 2024-08-20 (gate maintenance). scs couvre le besoin. |
| `authboss` (aarondl/authboss) | **Refusé** : framework auth complet opaque (login/reset/email) — viole le principe anti-framework du Kit ; maintenance OK. |
| Sessions « maison » (cookie signé + Secure/HttpOnly) | Possible et parfois justifié, mais réinvente fixation/renouvellement/rotation — scs est plus sûr. |
| JWT stateless | Voir `pattern:security:auth-session-vs-jwt` : mauvais choix pour une app web classique. |

## Security note

- **0 advisory** OSV (vérifié 2026-08-05).
- Cookie de session : `Secure` (HTTPS) et `HttpOnly` par défaut de scs ;
  configurer `SameSite` selon la topologie.
- Sessions côté serveur = **révocables** (logout, invalidation) — le point fort
  face au JWT.
- Appeler `sm.RenewToken(ctx)` après un login réussi (anti-fixation).
- **CSRF obligatoire** sur les endpoints state-changing : SameSite=Strict/Lax
  ne suffit pas toujours (voir `pattern:antipattern:sec-missing-csrf`).

## Utiliser cette librairie quand

- App web classique (templates, back-office, dashboard) servie par `net/http`
  ou chi : l'état d'auth vit côté serveur.
- Besoin de révocation / logout fort, de sessions par utilisateur avec
  invalidation.
- Plusieurs instances derrière un load balancer : store partagé (Postgres,
  Redis) requis.

## Ne pas utiliser cette librairie quand

- API REST / mobile / service-service : un token stateless (JWT) est plus
  adapté (voir `pattern:security:auth-session-vs-jwt`).
- Besoin d'un framework auth complet (reset password, email verification,
  OAuth2) : composer avec `x/oauth2` + bcrypt, ou évaluer un framework dédié
  (authboss refusé au catalogue — décision assumée).
- Single-instance avec zéro dépendance : un cookie signé maison peut suffire
  (cas rares).

## Avantages

- Actif, MIT, zéro advisory : profil sécurité propre.
- Stores pluggables (cookie, Postgres, Redis, SQLite, MySQL) : le choix du
  store ne change pas l'API.
- Middleware `LoadAndSave` simple, compatible chi/net/http.
- `RenewToken` (anti-fixation), `Lifetime`/`IdleTimeout`, `Destroy` — les
  bonnes pratiques sont dans l'API.

## Inconvénients

- Pas de login/password/logout intégré : à composer (bcrypt + handlers).
- Sessions côté serveur = état partagé : store requis pour le
  multi-instance ; cookie store = non révocable côté serveur.
- Pas de protection CSRF intégrée (à ajouter, anti-pattern dédié).
- Scorecard 3.0 avec `Maintained:0` — **cache périmé** contredisant le push
  du 2025-11-20 (même anomalie que filippo.io/age) ; croiser avec GitHub.

## Pièges connus

- `Cookie.Secure` à **true en production** (sinon session volable en clair) ;
  `SameSite` explicite.
- Store cookie (client-side) = données visibles et non révocables : ne pas y
  stocker de secrets ; préférer un store serveur pour l'auth.
- Appeler `RenewToken` après login (fixation) et `Destroy` au logout.
- Ne jamais exposer l'ID de session dans l'URL ni les logs.

## Sources vérifiées

- [alexedwards/scs (repo officiel, v2.9.0)](https://github.com/alexedwards/scs)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/alexedwards/scs/v2](https://pkg.go.dev/github.com/alexedwards/scs/v2)
  — vérifié 2026-08-05
- [godoc scs.Cookie (Secure, HttpOnly, SameSite)](https://pkg.go.dev/github.com/alexedwards/scs/v2#Cookie)
  — vérifié 2026-08-05
- OSV : aucun advisory pour `github.com/alexedwards/scs/v2` (requête API
  2026-08-05)
- Artefacts internes : `pattern:security:auth-session-vs-jwt`,
  `pattern:antipattern:sec-missing-csrf`, `pattern:http:middleware-chain`
