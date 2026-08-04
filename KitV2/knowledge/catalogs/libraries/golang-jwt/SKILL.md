---
name: golang-jwt
description: "github.com/golang-jwt/jwt/v5 v5.3.1 — JWT signing and verification (HS256/RS256/ES256/EdDSA), the standard JWT library for Go. Use when choosing a JWT library for REST APIs, mobile clients, or service-to-service auth. Not for classic cookie-based web app sessions (prefer scs) and never use the legacy dgrijalva/jwt-go import path."
category: library
tags: [security, jwt, authentication, tokens, api, rest]
last-verified: 2026-08-05
---

# golang-jwt — JWT sign/verify

## Selection

[`github.com/golang-jwt/jwt/v5`](https://github.com/golang-jwt/jwt) (v5.3.1,
Go 1.21+).

**Why it passes the gate** (actual reason, not stars): it is the standard JWT
implementation for Go — sign, parse, and validate with explicit algorithm
selection and a clean v5 API. Actively maintained (push 2026-08-01), strong
security practices (scorecard 7.8 : security-policy 10/10, pinned 10/10,
SAST 9/10), single responsibility (token lifecycle), mass adoption. This is a
**promotion** of the legacy Source YAML (`golang-jwt.yaml`) to a vetted fiche.

## Admission checklist

- [x] Actively maintained — v5.3.1 (2026-01-28), push 2026-08-01
- [x] Single responsibility — JWT signing/parsing/validation
- [x] Idiomatic Go — clean v5 API, typed claims, no magic
- [x] Tests present + CI — yes; SAST 9/10, scorecard 7.8
- [x] Documentation — godoc + README + migration guide v4→v5
- [x] Real-world usage — standard de facto (adoption massive)
- [x] Readable end-to-end — ~9 kLOC, layered (parser/signing/claims)
- [x] Justified by need — JWT est un besoin auth explicite du catalogue ;
      NOT popularity (promotion d'un Source legacy)

## Minimal use

```go
token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
    "user_id": 123,
    "exp":     time.Now().Add(time.Hour).Unix(),
})
signed, _ := token.SignedString([]byte("secret"))

parsed, err := jwt.Parse(signed, func(t *jwt.Token) (any, error) {
    if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
        return nil, fmt.Errorf("unexpected method %v", t.Header["alg"])
    }
    return []byte("secret"), nil
})
```

Compilé et vérifié (sign + parse) avec v5.3.1 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Sessions cookies (`scs`) | Le bon choix pour une **app web classique** (navigateur) : révocables, HttpOnly. Voir `pattern:security:auth-session-vs-jwt`. |
| `dgrijalva/jwt-go` (ancien import path) | **Abandonné**, historique de CVEs — ne jamais utiliser l'ancien chemin d'import. |
| PASETO (paseto-go) | Format token alternatif plus sûr par construction ; adoption moindre, moins d'outillage. |
| JWT « maison » (HMAC signé à la main) | Anti-pattern : parsing/validation JWT est une classe d'erreur connue. |

## Security note

- Historique : advisory **GO-2025-3553 / GHSA-mh63-6h87-95cp** (allocation
  mémoire excessive pendant le parsing du header, DoS), corrigé en **v5.2.2**
  (v4.5.2 pour la v4). **Épingler ≥ v5.2.2** ; v5.3.1 sain (vérifié 2026-08-05,
  OSV).
- Toujours vérifier l'algorithme dans la keyfunc (whitelist) ou utiliser
  `jwt.WithValidMethods([]string{"HS256", ...})` — anti-alg-confusion.
- JWT n'est **pas révocable** par design : token court (exp) + jti + rotation.
- Ne jamais mettre de données sensibles dans les claims (décodables par le
  client) ; signer n'est pas chiffrer.

## Utiliser cette librairie quand

- API REST, SPA, mobile ou communication service-service : un token porteur
  (`Authorization: Bearer`) est requis.
- L'état d'authentification doit être **stateless** (pas de session côté
  serveur) côté API.
- Multi-clients (web + mobile + services) avec un format standard.

## Ne pas utiliser cette librairie quand

- App web classique servie par templates : les **sessions cookies** (`scs`)
  sont plus simples et révocables — le JWT n'apporte rien ici (voir
  `pattern:security:auth-session-vs-jwt`).
- Besoin de révocation, d'invalidation immédiate ou de logout fort : JWT ne le
  fournit pas — sessions côté serveur ou blacklist/rotation à construire.
- Le login doit passer par Google/GitHub/entreprise : OAuth2/OIDC
  (`golang.org/x/oauth2`) est la réponse, pas un JWT maison.

## Avantages

- Standard JWT complet (HS/RS/ES/EdDSA), API v5 propre et typée.
- Maintien actif + pratiques sécurité fortes (scorecard 7.8, SAST).
- Écosystème massif : docs, middleware, exemples.
- Épingler la version corrige les 2 advisories connus (≤ 5.2.2).

## Inconvénients

- Stateless = non révocable : exp court obligatoire, gestion des clés à soigner.
- 2 advisories historiques (parsing DoS) : exige pin ≥ 5.2.2 et validation de
  l'algorithme.
- Pas de gestion de refresh token / OIDC : à composer (x/oauth2, coreos/go-oidc).

## Pièges connus

- Ne jamais utiliser `github.com/dgrijalva/jwt-go` (abandonné, CVEs).
- Keyfunc sans whitelist d'algorithme = alg confusion (`alg=none`, RS→HS).
- `jwt.Parse` accepte les tokens sans `exp` si le validator ne l'exige pas :
  configurer `jwt.WithExpirationRequired()`.
- Claims sensibles (email, rôle) lisibles par le client : signer ≠ chiffrer.

## Sources vérifiées

- [golang-jwt/jwt (repo officiel, v5.3.1)](https://github.com/golang-jwt/jwt)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/golang-jwt/jwt/v5](https://pkg.go.dev/github.com/golang-jwt/jwt/v5)
  — vérifié 2026-08-05
- [Advisory GO-2025-3553 / GHSA-mh63-6h87-95cp (header parsing DoS, fix 5.2.2)](https://osv.dev/vulnerability/GO-2025-3553)
  — vérifié 2026-08-05 (sécurité officielle)
- OSV : 2 entrées aliases pour `github.com/golang-jwt/jwt/v5`, corrigées ≤ 5.2.2
  (requête API 2026-08-05)
- Artefacts internes : `pattern:security:auth-session-vs-jwt`,
  `pattern:security:fail-closed-auth`, `source:go:x-crypto`,
  `pattern:antipattern:sec-missing-csrf`
