---
name: recipe-openapi-validation
description: "Validate a startup-loaded embedded OpenAPI document plus bounded net/http requests and buffered responses with a required non-noop AuthenticationFunc. Use when OpenAPI is an executable API contract; not for streaming, hijacking, unbounded bodies, generated code, or fail-open authentication."
category: recipe
tags: [openapi, validation, api, http, contract, security]
last-verified: 2026-08-05
---

# recipe-openapi-validation — contrat HTTP exécutable

## Objectif et cas d'utilisation

Charger et valider un document OpenAPI embarqué au démarrage, puis valider
requête **et** réponse d'un handler `net/http`. La middleware borne les corps,
résout la route, exige une `AuthenticationFunc` réelle, et ne laisse sortir une
réponse qu'après validation de son statut, headers et corps.

Utiliser quand OpenAPI est le contrat réel de l'API. Le contrat n'est pas un
générateur et ne remplace pas la décision d'authentification métier.

## Prérequis et architecture

- `Config.Spec` vient de `go:embed` ou d'un octet contrôlé au démarrage.
- `AuthenticationFunc` est obligatoire et `NoopAuthenticationFunc` est rejeté.
- `MaxBodyBytes` borne autant la requête que le tampon de réponse.
- Les réponses d'erreur `400`, `413` et `500` doivent figurer dans le document,
  comme dans `openapi.yaml`, avec une forme générique stable.

La recipe utilise le routeur legacy de kin-openapi et son validateur filtre.
Elle n'utilise pas `ValidationHandler`, dont la version retenue ne valide pas
les réponses. Cela justifie le petit adaptateur local plutôt qu'un double
middleware incomplet.

## Composants et choix

- `github.com/getkin/kin-openapi v0.146.0` — catalogue `kin-openapi` ; parsing,
  route matching et validation OpenAPI 3.
- `openapi3filter.ValidateRequest`/`ValidateResponse` — contrat à l'entrée et à
  la sortie.
- tampon borné — réponse invalide ou trop grande devient une erreur générique
  conforme au contrat ; son contenu et le détail du validateur ne sont pas
  divulgués.

## Alternatives rejetées

- `ValidationHandler` : rejeté car il porte encore `TODO: validateResponse`.
- `NoopAuthenticationFunc`, callback absente ou fail-open : rejetés.
- Validation seulement de requête : laisse l'API violer son contrat en sortie.
- Streaming, `Hijacker`, `Flusher`, WebSocket et corps au-delà de la limite :
  incompatibles avec la validation entièrement tamponnée.

## Exemple complet

```go
validator, err := openapivalidation.New(context.Background(), openapivalidation.Config{
	Spec: openapivalidation.ExampleSpec, MaxBodyBytes: 1 << 20,
	AuthenticationFunc: func(ctx context.Context, input *openapi3filter.AuthenticationInput) error {
		return verifyBearer(ctx, input.RequestValidationInput.Request.Header.Get("Authorization"))
	},
})
if err != nil {
	return err
}
handler := validator.Middleware(appHandler)
```

## Bonnes pratiques et pièges

- Valider le document au démarrage : un contrat invalide empêche le service de
  démarrer.
- Définir dans le document tous les statuts/headers émis par le handler.
- Garder les limites proportionnées ; les payloads compressés et gros objets
  demandent une recette d'upload séparée.
- Ne jamais inclure corps, token ni détail de validation dans l'erreur client ou
  les logs de réponse invalide.

## Limites et extensions

Le routeur legacy ne couvre pas toutes les formes de chemin/extensions ; tester
les routes réelles du contrat. Pas de streaming, hijacking, export de métriques,
génération de client/serveur, ni autorisation métier. Ces besoins changent la
frontière et exigent une recipe dédiée.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-openapi-validation/...
go run ./probes/openapi-validation
```

La probe valide un `POST /widgets` authentifié et une réponse `201`, puis
affiche `openapi-validation: PASS`. Les tests prouvent une requête invalide,
une réponse invalide masquée et un corps trop grand.

## Sources primaires

- [kin-openapi openapi3filter](https://pkg.go.dev/github.com/getkin/kin-openapi/openapi3filter)
  — entrées de validation et fonction d'authentification.
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — contrat
  des opérations, réponses et security requirements.

