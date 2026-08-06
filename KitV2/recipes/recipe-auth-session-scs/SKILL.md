---
name: recipe-auth-session-scs
description: "Implement browser authentication with an injected scs/v2 SessionManager, secure cookie defaults, credential verifier, synchronizer CSRF token, and protected routes. Use for same-site browser sessions; not for Bearer APIs, distributed session storage without separate admission, or password verification design."
category: recipe
tags: [auth, session, cookie, csrf, scs, http, security]
last-verified: 2026-08-05
---

# recipe-auth-session-scs — browser session and CSRF

## Objective and use case

Authenticate a browser on the same origin with a server-side session and an
opaque cookie. The recipe exposes `VerifyFunc`, an injected
`*scs.SessionManager`, `GET /csrf`, `POST /login`, `POST /logout` and
`GET /protected`. It applies a synchronizer token before every write and logs
neither passwords nor tokens.

Choose this recipe for a browser UI controlled by the same site. For a Bearer
API without cookies, use `recipe-auth-jwt`; the two boundaries are not
interchangeable.

## Prerequisites and architecture

- TLS is active: the cookie is always `Secure`, `HttpOnly` and
  `SameSite=Strict`.
- The credential verifier is injected and returns only a subject.
- `scs` keeps its default in-memory store: this suits tests or a single
  process. A persistent/multi-replica store is an extension point that
  requires separate admission.

`LoadAndSave` loads and writes the session; the login handler validates the
CSRF token, verifies the credentials, calls `RenewToken` after privilege
elevation, then stores the subject and a fresh CSRF token. Subsequent writes
compare tokens with `subtle.ConstantTimeCompare`.

## Components and choices

- `github.com/alexedwards/scs/v2 v2.9.0` — `scs` catalog; explicit session
  management compatible with `net/http`.
- `crypto/rand` + synchronizer token — avoids an extra CSRF middleware.
- `VerifyFunc` — the recipe chooses neither a user table, nor a password
  hash, nor an identity provider.

Patterns: `pattern:security:auth-session-vs-jwt`,
`pattern:antipattern:sec-missing-csrf`, `pattern:http:middleware-chain`.

## Rejected alternatives

- JWT in a cookie: mixes an API boundary with a CSRF risk; choose an opaque
  session here.
- Cookie without `Secure` or `SameSite=Strict`: incompatible with this
  recipe's contract.
- Double-submit cookie, global middleware, or implicit distributed store: a
  distinct need that must document its topology and admission.

## Complete example

```go
sessions := authsessionscs.NewSessionManager()
app, err := authsessionscs.New(sessions, func(ctx context.Context, email, password string) (string, error) {
 if email != "person@example.test" || password != "correct" {
  return "", authsessionscs.ErrInvalidCredentials
 }
 return "user-42", nil
})
if err != nil {
 return err
}
return http.ListenAndServeTLS(":8443", "cert.pem", "key.pem", app.Router())
```

## Best practices and pitfalls

- Fetch `/csrf` before login, then replace the received token after login.
- Require CSRF for logout too; make failures generic.
- Never put passwords, cookies, CSRF tokens, or sensitive subjects in logs.
  Limit the login JSON size as the example does.
- Regenerate the session token on privilege elevation; never set identity
  from a client header.

## Limits and extensions

This recipe provides neither signup, password reset, MFA, rate limiting,
global revocation, persistent storage, nor federation. Add these capabilities
in separate recipes with their own security decisions; do not hide them in the
session middleware.

## Observable scenario and verification

```sh
go test ./recipes/recipe-auth-session-scs/...
go run ./probes/auth-session
```

The probe performs over TLS `GET /csrf`, login, protected read, and logout,
then prints `auth-session: PASS`. Tests cover missing/invalid CSRF, invalid
credentials, and missing dependencies.

## Primary sources

- [scs v2](https://pkg.go.dev/github.com/alexedwards/scs/v2) — sessions,
  `LoadAndSave`, cookies and renewal.
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
  — synchronizer token and safe comparison.
- [net/http](https://pkg.go.dev/net/http) and [crypto/subtle](https://pkg.go.dev/crypto/subtle)
  — HTTP boundaries and constant-time comparison.
