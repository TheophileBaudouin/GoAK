---
name: golang-jwt
description: "github.com/golang-jwt/jwt/v5 v5.3.1 — JWT signing and verification for Go. Use when an interoperable signed token is required for APIs or service-to-service auth; not for cookie sessions, key management, or unvalidated token trust."
category: library
tags: [auth, jwt, security, token, api]
last-verified: 2026-08-05
---

# golang-jwt — signature et validation JWT

## Selection

[`github.com/golang-jwt/jwt/v5`](https://github.com/golang-jwt/jwt) v5.3.1,
released 2026-01-28, is an MIT-licensed implementation of JWT signing and
verification. It is admitted for a focused interoperable token boundary, active
maintenance, tests, and documented security advisories; it is not a session
framework or a key-management service.

## Admission checklist

- [x] Current stable v5.3.1 with active upstream maintenance.
- [x] Single responsibility: JWT/JWS token parsing, claims, and signing methods.
- [x] Go 1.21+ API with `RegisteredClaims` and parser options.
- [x] Tests, CI, documentation, and security advisory handling are present.
- [x] The token contract is distinct from cookie sessions (`scs`) and OAuth.

## Minimal use

```go
func sign(subject string, key []byte) (string, error) {
    token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.RegisteredClaims{
        Subject: subject,
    })
    signed, err := token.SignedString(key)
    if err != nil {
        return "", fmt.Errorf("sign token: %w", err)
    }
    return signed, nil
}
```

Verification must whitelist the expected signing method and validate issuer,
audience, expiry, and subject for the application's contract. Do not treat a
successful parse alone as authorization.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `scs` | Prefer for classic server-side browser sessions with cookies. |
| `golang.org/x/oauth2` | Prefer for delegated OAuth provider flows; JWT is only one token representation. |
| `lestrrat-go/jwx` | Consider when JWE/JWS breadth or JSON Canonicalization support is a hard requirement. |
| `dgrijalva/jwt-go` | Discontinued predecessor; never use its legacy import path. |

## Utiliser cette librairie quand

- A service needs a signed, interoperable JWT for APIs or service-to-service
  authentication.
- The issuer, audience, expiry, signing method, and key rotation policy are
  explicit application decisions.
- The service can validate claims and signing method at its trust boundary.

## Ne pas utiliser cette librairie quand

- A server-side browser session is the actual requirement: prefer `scs`.
- The application needs key storage, rotation, revocation, or a KMS/HSM policy
  that JWT itself does not provide.
- A token should be trusted merely because it parses or because its header picks
  an algorithm.
- The project needs JWE or broad JOSE capabilities not covered by this package.

## Avantages

- Familiar JWT API and standard v5 module path.
- `RegisteredClaims` and parser options make validation policy explicit.
- Multiple signing methods and interoperable compact token format.
- Small focused responsibility with active maintenance and security advisories.

## Inconvénients

- Signed JWTs are not encrypted and are usually bearer credentials.
- Revocation, rotation, issuer/audience policy, and storage remain application
  responsibilities.
- Parser edge cases and cross-language JSON serialization require explicit tests.

## Pièges connus

- Whitelist the signing method and key source; never accept an algorithm or key
  solely because the token header requests it.
- Validate claims with the parser and application policy; `ParseUnverified` is
  not an authorization path.
- Bound token input before parsing and keep secrets out of logs and URLs.
- Pin a patched v5 release: the project has published fixes for excessive
  header parsing allocation and documented claim-error handling.
- Do not use `SigningMethodNone` in application authentication.

## Sources vérifiées

- [Official golang-jwt repository](https://github.com/golang-jwt/jwt) — API,
  maintenance, license, checked 2026-08-05.
- [Releases](https://github.com/golang-jwt/jwt/releases) — current stable
  v5.3.1, checked 2026-08-05.
- [JWT v5 on pkg.go.dev](https://pkg.go.dev/github.com/golang-jwt/jwt/v5) —
  parser and claims API, checked 2026-08-05.
- [CVE-2025-30204 advisory](https://github.com/golang-jwt/jwt/security/advisories/GHSA-mh63-6h87-95cp)
  — parser allocation issue and fixed versions, checked 2026-08-05.
- [CVE-2024-51744 advisory](https://github.com/golang-jwt/jwt/security/advisories/GHSA-29wx-vh33-7x7r)
  — claim-error handling documentation, checked 2026-08-05.
- [Issue #499](https://github.com/golang-jwt/jwt/issues/499) — parser behavior
  regression to review during upgrades, checked 2026-08-05.
