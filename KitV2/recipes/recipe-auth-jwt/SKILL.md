---
name: recipe-auth-jwt
description: "Implement a narrow HS256 JWT Bearer API boundary with injected secret, issuer, audience, TTL, testable clock, strict signature method, expiry, and subject context. Use for one issuer/verifier trust boundary; not for browser cookies, OIDC, key distribution, rotation, or revocation."
category: recipe
tags: [auth, jwt, bearer, api, hs256, security, http]
last-verified: 2026-08-05
---

# recipe-auth-jwt — Bearer API HS256

## Purpose and use case

Issue and verify HS256 JWTs for an API whose issuer and verifier share the same
injected secret key. The middleware accepts exclusively `Authorization:
Bearer`, enforces HS256, expiration, issuer, audience, and subject, then
forwards only the validated subject in the request context.

Use this recipe inside a single trust boundary. For browser cookies and CSRF,
use `recipe-auth-session-scs`.

## Prerequisites and architecture

`Config` requires at least 32 bytes of key, issuer, audience, TTL, and
optionally a testable clock. `Issue` writes the registered claims; `Middleware`
extracts a single header, configures `WithValidMethods`, then validates the
claims. It does not place the token or the full claims in `context.Context`.

## Components and choices

- `github.com/golang-jwt/jwt/v5 v5.3.1` — `golang-jwt` catalog; explicit parser
  and claims validation.
- HS256 — a single issuer/verifier boundary, injected key never written to
  logs, examples, or the repository.
- Injected clock — testable expiration without sleeping or global state.

Pattern: `pattern:security:auth-session-vs-jwt`.

## Rejected alternatives

- JWT in a cookie: a browser session is more coherent and handles CSRF.
- `alg=none`, implicit algorithm, or unbounded `kid`: no such path is accepted;
  the middleware strictly limits to HS256.
- OIDC, rotation, revocation, and asymmetric keys: they require a separate key
  distribution and discovery recipe.

## Complete example

```go
auth, err := authjwt.New(authjwt.Config{
	Key: []byte(os.Getenv("JWT_HS256_KEY")), Issuer: "orders",
	Audience: "orders-api", TTL: 15 * time.Minute,
})
if err != nil {
	return err
}
http.Handle("GET /v1/orders", auth.Middleware(http.HandlerFunc(listOrders)))
```

In `listOrders`, retrieve `subject, ok := authjwt.Subject(r.Context())` and
treat its absence as an internal chaining error, not as a provided client
identity.

## Best practices and pitfalls

- Keep the TTL short and the key high-entropy in a secret store; never log the
  Authorization header, token, or key.
- Verify signature, exp, issuer, audience, and subject together: a valid
  signature does not imply the token is intended for this API.
- Do not accept Basic, query parameter, cookie, duplicated header, or
  alternative algorithm in this middleware.

## Limits and extensions

The recipe covers neither refresh tokens, rotation, revocation, permissions,
JWKS, OIDC, nor multi-issuer. Key distribution or identity delegation changes
the trust boundary and requires a new sourced decision.

## Observable scenario and verification

```sh
go test ./recipes/recipe-auth-jwt/...
go run ./probes/auth-jwt
```

The probe obtains a token, calls a protected route, and prints `auth-jwt:
PASS`. The tests cover missing header, wrong method, expiration, and invalid
issuer, audience, and subject.

## Primary sources

- [golang-jwt v5](https://pkg.go.dev/github.com/golang-jwt/jwt/v5) — parser,
  validation options, and registered claims.
- [JWT BCP — RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) — explicit
  validation of the algorithm and token usage.
