---
name: recipe-auth-session-scs
description: "Implement browser authentication with an injected scs/v2 SessionManager, secure cookie defaults, credential verifier, synchronizer CSRF token, and protected routes. Use for same-site browser sessions; not for Bearer APIs, distributed session storage without separate admission, or password verification design."
category: recipe
tags: [auth, session, cookie, csrf, scs, http, security]
last-verified: 2026-08-05
---

# recipe-auth-session-scs — session navigateur et CSRF

## Objectif et cas d'utilisation

Authentifier un navigateur sur la même origine avec une session serveur et un
cookie opaque. La recipe expose `VerifyFunc`, un `*scs.SessionManager` injecté,
`GET /csrf`, `POST /login`, `POST /logout` et `GET /protected`. Elle applique
un synchronizer token avant chaque écriture et ne journalise ni mot de passe ni
jeton.

Choisir cette recipe pour une UI navigateur contrôlée par le même site. Pour une
API Bearer sans cookie, utiliser `recipe-auth-jwt` ; les deux frontières ne sont
pas interchangeables.

## Prérequis et architecture

- TLS est actif : le cookie est toujours `Secure`, `HttpOnly` et
  `SameSite=Strict`.
- Le vérificateur de credentials est injecté et renvoie uniquement un subject.
- `scs` garde son store mémoire par défaut : cela convient aux tests ou à un
  processus unique. Un store persistant/multi-réplique est un point d'extension
  qui exige une admission séparée.

`LoadAndSave` charge et écrit la session ; le handler login valide le token
CSRF, vérifie les credentials, appelle `RenewToken` après élévation de
privilège, puis stocke le subject et un token CSRF neuf. Les écritures suivantes
comparent les tokens par `subtle.ConstantTimeCompare`.

## Composants et choix

- `github.com/alexedwards/scs/v2 v2.9.0` — catalogue `scs` ; gestion de session
  explicite et compatible `net/http`.
- `crypto/rand` + token synchronizer — évite un middleware CSRF supplémentaire.
- `VerifyFunc` — la recipe ne choisit ni table utilisateur, ni hash de mot de
  passe, ni fournisseur d'identité.

Patterns : `pattern:security:auth-session-vs-jwt`,
`pattern:antipattern:sec-missing-csrf`, `pattern:http:middleware-chain`.

## Alternatives rejetées

- JWT dans le cookie : mélange une frontière API avec un risque CSRF ; choisir
  une session opaque ici.
- Cookie sans `Secure` ou `SameSite=Strict` : incompatible avec le contrat de
  cette recipe.
- Double-submit cookie, middleware global ou store distribué implicite : besoin
  distinct qui doit documenter sa topologie et son admission.

## Exemple complet

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

## Bonnes pratiques et pièges

- Obtenir `/csrf` avant login, puis remplacer le token reçu après login.
- Exiger CSRF aussi pour logout ; rendre les échecs génériques.
- Ne jamais mettre mot de passe, cookie, token CSRF ou subject sensible dans les
  logs. Limiter la taille du JSON de login comme le fait l'exemple.
- Régénérer le token de session lors d'une montée de privilège ; ne pas fixer
  l'identité depuis un header client.

## Limites et extensions

Cette recipe ne fournit ni inscription, reset de mot de passe, MFA, rate limit,
révocation globale, stockage persistant, ni fédération. Ajouter ces capacités à
des recipes séparées avec leurs décisions de sécurité ; ne les cacher pas dans
le middleware session.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-auth-session-scs/...
go run ./probes/auth-session
```

La probe effectue sur TLS `GET /csrf`, login, lecture protégée et logout, puis
affiche `auth-session: PASS`. Les tests couvrent CSRF manquant/invalide,
credentials invalides et dépendances absentes.

## Sources primaires

- [scs v2](https://pkg.go.dev/github.com/alexedwards/scs/v2) — sessions,
  `LoadAndSave`, cookies et renouvellement.
- [OWASP CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)
  — synchronizer token et comparaison sûre.
- [net/http](https://pkg.go.dev/net/http) et [crypto/subtle](https://pkg.go.dev/crypto/subtle)
  — frontières HTTP et comparaison constante.

