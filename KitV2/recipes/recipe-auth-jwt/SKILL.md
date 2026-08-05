---
name: recipe-auth-jwt
description: "Implement a narrow HS256 JWT Bearer API boundary with injected secret, issuer, audience, TTL, testable clock, strict signature method, expiry, and subject context. Use for one issuer/verifier trust boundary; not for browser cookies, OIDC, key distribution, rotation, or revocation."
category: recipe
tags: [auth, jwt, bearer, api, hs256, security, http]
last-verified: 2026-08-05
---

# recipe-auth-jwt — Bearer API HS256

## Objectif et cas d'utilisation

Émettre et vérifier des JWT HS256 pour une API dont l'émetteur et le vérificateur
partagent une même clé secrète injectée. Le middleware accepte exclusivement
`Authorization: Bearer`, impose HS256, expiration, issuer, audience et subject,
puis transmet uniquement le subject validé dans le contexte de requête.

Utiliser cette recipe à l'intérieur d'une frontière de confiance unique. Pour
les cookies navigateur et CSRF, utiliser `recipe-auth-session-scs`.

## Prérequis et architecture

`Config` exige au moins 32 octets de clé, issuer, audience, TTL et optionnellement
une horloge testable. `Issue` inscrit les claims enregistrés ; `Middleware`
extrait un seul header, configure `WithValidMethods`, puis valide les claims.
Il ne place pas le token ni les claims complets dans `context.Context`.

## Composants et choix

- `github.com/golang-jwt/jwt/v5 v5.3.1` — catalogue `golang-jwt` ; parser et
  validation explicite des claims.
- HS256 — une seule frontière émetteur/vérificateur, clé injectée et jamais
  écrite dans les logs, exemples ou repository.
- Horloge injectée — expiration testable sans sommeil ni variable globale.

Pattern : `pattern:security:auth-session-vs-jwt`.

## Alternatives rejetées

- JWT en cookie : une session navigateur est plus cohérente et gère CSRF.
- `alg=none`, algorithme implicite ou `kid` non borné : aucun chemin n'est
  accepté ; le middleware limite strictement HS256.
- OIDC, rotation, révocation et clés asymétriques : nécessitent une recette de
  distribution de clés et de découverte séparée.

## Exemple complet

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

Dans `listOrders`, récupérer `subject, ok := authjwt.Subject(r.Context())` et
traiter l'absence comme une erreur interne de chaînage, non comme une identité
client fournie.

## Bonnes pratiques et pièges

- Garder TTL court et clé à forte entropie dans un secret store ; ne jamais
  journaliser header Authorization, token ou clé.
- Vérifier signature, exp, issuer, audience et subject ensemble : une signature
  valide n'implique pas que le token soit destiné à cette API.
- Ne pas accepter Basic, query parameter, cookie, header dupliqué ou algorithme
  alternatif dans ce middleware.

## Limites et extensions

La recipe ne couvre ni refresh token, rotation, révocation, permissions, JWKS,
OIDC ni multi-émetteur. Une distribution de clés ou une délégation d'identité
change la frontière de confiance et exige une nouvelle décision sourcée.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-auth-jwt/...
go run ./probes/auth-jwt
```

La probe obtient un token, appelle une route protégée et affiche `auth-jwt:
PASS`. Les tests couvrent header absent, méthode erronée, expiration, issuer,
audience et subject invalides.

## Sources primaires

- [golang-jwt v5](https://pkg.go.dev/github.com/golang-jwt/jwt/v5) — parseur,
  options de validation et claims enregistrés.
- [JWT BCP — RFC 8725](https://www.rfc-editor.org/rfc/rfc8725) — validation
  explicite de l'algorithme et de l'usage du token.

