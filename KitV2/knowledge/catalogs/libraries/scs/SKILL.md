---
name: scs
description: "github.com/alexedwards/scs/v2 v2.9.0 — server-side sessions for net/http with a cookie token and pluggable stores. Use for classic browser sessions and revocable login state; not for stateless APIs or a complete authentication framework, and add CSRF protection."
category: library
tags: [security, sessions, cookies, authentication, web, middleware]
last-verified: 2026-08-05
---

# scs — sessions serveur

## Selection

[`github.com/alexedwards/scs/v2`](https://github.com/alexedwards/scs) v2.9.0
is a server-side session manager for `net/http`. A token travels in a cookie;
session data stays in a pluggable store, and `LoadAndSave` wraps the handler.
It is admitted for a focused, maintained session boundary with tests and
standard HTTP integration; it is not a login/authentication framework.

## Admission checklist

- [x] Current v2.9.0 and active upstream maintenance.
- [x] Single responsibility: session lifecycle and storage integration.
- [x] `net/http` middleware, store interface, tests, CI, and documentation.
- [x] Cookie security options, token renewal, lifetime/idle timeout, and destroy
      lifecycle are explicit.
- [x] The maintained replacement decision is distinct from dormant
      `gorilla/sessions`.

## Minimal use

```go
func sessionHandler(sm *scs.SessionManager) http.Handler {
    sm.Cookie.Secure = true
    sm.Cookie.HttpOnly = true
    sm.Cookie.SameSite = http.SameSiteLaxMode
    return sm.LoadAndSave(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if userID, ok := sm.Get(r.Context(), "user_id").(int); ok {
            _, _ = fmt.Fprintf(w, "authenticated %d", userID)
        }
    }))
}
```

Call `RenewToken` after successful login and `Destroy` on logout. Add CSRF
protection to state-changing browser requests; cookie attributes are not a full
CSRF policy.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang-jwt/jwt` | Prefer for explicitly stateless API/service tokens, with revocation/rotation policy. |
| `gorilla/sessions` | Do not choose for new work without an independent maintenance decision; scs is the maintained session boundary in this kit. |
| Cookie/session implementation | Possible for a tiny controlled case, but requires correct renewal, signing, expiry, and store policy. |
| Full auth framework | Choose only when login, password reset, OAuth, and email workflows justify its larger contract. |

## Utiliser cette librairie quand

- A classic browser app uses `net/http`/chi and needs server-side revocable
  session state.
- Logout/invalidation and shared Postgres/Redis/SQLite stores matter.
- Cookie transport plus application-owned authentication handlers is the desired
  boundary.

## Ne pas utiliser cette librairie quand

- A mobile, REST, or service-to-service API needs stateless tokens instead.
- The project needs login/password/OAuth/email workflows from one framework.
- The application cannot provide a secure store or CSRF policy.

## Avantages

- Server-side data keeps the cookie small and allows revocation/destroy.
- Pluggable stores preserve the same manager API across deployments.
- `LoadAndSave`, `RenewToken`, `IdleTimeout`, `Lifetime`, and `Destroy` cover
  the session lifecycle without hiding authentication policy.

## Inconvénients

- Shared server state and store operations are required for multi-instance apps.
- It does not implement identity verification, passwords, OAuth, or CSRF.
- Cookie-store deployments have different visibility/revocation trade-offs than
  server stores.
- Token hashing and cookie security options require deliberate configuration.

## Pièges connus

- Set `Secure=true` for HTTPS production, `HttpOnly=true`, and an explicit
  `SameSite` policy suited to the application.
- Renew the token after login to prevent session fixation; destroy it at logout.
- Never put session IDs in URLs or logs, and never store secrets in a client-side
  cookie store without reviewing its confidentiality model.
- Add CSRF protection to state-changing browser routes; SameSite alone is not a
  complete guarantee.
- Consider `HashTokenInStore` when the store's confidentiality boundary requires
  protection of session tokens at rest.

## Sources vérifiées

- [Official scs repository](https://github.com/alexedwards/scs) — API,
  maintenance, license, checked 2026-08-05.
- [scs releases](https://github.com/alexedwards/scs/releases) — v2.9.0 current
  version and changes, checked 2026-08-05.
- [scs on pkg.go.dev](https://pkg.go.dev/github.com/alexedwards/scs/v2) —
  manager, cookie, store API, checked 2026-08-05.
- [Cookie API](https://pkg.go.dev/github.com/alexedwards/scs/v2#Cookie) —
  Secure/HttpOnly/SameSite/Partitioned behavior, checked 2026-08-05.
- [scs issues](https://github.com/alexedwards/scs/issues) — token hashing and
  store/tagging limitations, checked 2026-08-05.
