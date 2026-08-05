---
name: recipe-observability-slog-expvar
description: "Instrument net/http with injected JSON slog logs, server-generated request IDs, atomic bounded request/error/in-flight/latency metrics, and an expvar admin handler. Use for minimum private-process observability; not for public metrics endpoints, logger-in-context, tracing, Prometheus, or OpenTelemetry."
category: recipe
tags: [observability, slog, expvar, http, metrics, logging]
last-verified: 2026-08-05
---

# recipe-observability-slog-expvar — logs JSON et métriques privées

## Objectif et cas d'utilisation

Ajouter l'observabilité minimale d'un service `net/http` : un ID aléatoire
généré côté serveur, un log JSON `slog` injecté et des compteurs atomiques de
requêtes, erreurs, requêtes en vol et somme de latence. Le handler `expvar`
expose les valeurs sur un listener d'administration privé uniquement.

## Prérequis et architecture

Créer un `*slog.Logger` avec un `JSONHandler`, une instance `Metrics`, appeler
`Publish` une fois au démarrage et monter `AdminHandler` sur un port/interface
non publique (mTLS, socket locale ou réseau d'administration isolé). `expvar`
expose aussi des informations runtime standard : il ne doit jamais être routé
par le serveur Internet principal.

Le middleware ne met pas de logger dans `context.Context`; il y dépose seulement
l'ID de corrélation, et ne journalise ni query string, ni header, ni corps.

## Composants et choix

- `log/slog` — logs structurés JSON standard, logger injecté.
- `expvar` — exposition stdlib, volontairement locale et sans exporteur.
- `sync/atomic` — compteurs sans lock, sans labels ni dimensions à cardinalité
  forte.
- `crypto/rand` — ID corrélation non contrôlé par le client.

Pattern : `pattern:observability:structured-logging`.

## Alternatives rejetées

- Logger dans le contexte : dépendance cachée et propagation inutile.
- ID fourni par le client : permet collision/usurpation ; cette recipe génère le
  sien puis le retourne dans `X-Request-ID`.
- Prometheus, OpenTelemetry et exporteurs : besoins d'infrastructure distincts,
  hors de cette couche minimale.
- `/debug/vars` public ou métriques avec user ID/path dynamique : exposition ou
  cardinalité non bornée.

## Exemple complet

```go
metrics := &observability.Metrics{}
if err := observability.Publish("orders_metrics", metrics); err != nil {
	return err
}
middleware, err := observability.Middleware(slog.New(slog.NewJSONHandler(os.Stdout, nil)), metrics)
if err != nil {
	return err
}
publicServer := &http.Server{Addr: ":8080", Handler: middleware(app)}
privateServer := &http.Server{Addr: "127.0.0.1:9090", Handler: observability.AdminHandler()}
```

Ne pas remplacer `127.0.0.1:9090` par une adresse publique sans une décision de
sécurité et un contrôle d'accès explicite.

## Bonnes pratiques et pièges

- N'enregistrer que des champs bornés : ID, méthode, statut et durée ; aucun
  secret, query string, corps, token ou user ID.
- Une `Snapshot` atomique n'est pas une transaction : l'observation peut couvrir
  des instants légèrement différents.
- N'appeler `Publish` qu'une fois ; une seconde inscription est une erreur.
- Tester sous `-race` les requêtes concurrentes comme le test de la recipe.

## Limites et extensions

Pas de traces distribuées, histogrammes, export, dashboards, alertes ni métrique
par route/utilisateur. Ajouter ce niveau d'observabilité via une recipe dédiée,
avec politique de cardinalité, coût et exposition.

## Scénario observable et vérification

```sh
go test -race ./recipes/recipe-observability-slog-expvar/...
go run ./probes/observability
```

La probe réalise une requête, vérifie l'ID et la métrique `expvar`, puis affiche
`observability: PASS`.

## Sources primaires

- [log/slog](https://pkg.go.dev/log/slog) — logs structurés et `JSONHandler`.
- [expvar](https://pkg.go.dev/expvar) — registre global et `/debug/vars`.
- [sync/atomic](https://pkg.go.dev/sync/atomic) — compteurs concurrents.
