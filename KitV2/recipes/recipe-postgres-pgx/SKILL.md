---
name: recipe-postgres-pgx
description: "Implement PostgreSQL persistence with an explicit pgx/v5 pool, cancellable open plus Ping, positional SQL parameters, and deployment-run golang-migrate SQL files. Use for native PostgreSQL access; not for database/sql, ORMs, dynamic SQL, replica-start migrations, or Docker-dependent tests."
category: recipe
tags: [postgresql, pgx, database, sql, migrations, persistence]
last-verified: 2026-08-05
---

# recipe-postgres-pgx — pool pgx et migrations SQL

## Objectif et cas d'utilisation

Fournir une frontière PostgreSQL native, petite et observable : `Open` est
annulable, configure un `pgxpool.Pool`, appelle `Ping`, et `Close` libère le
pool. Les requêtes utilisent exclusivement `$1…$n` et enrichissent les erreurs.
Les migrations SQL versionnées sont appliquées séparément par la CLI
`golang-migrate` avant le déploiement.

## Prérequis et architecture

- Une `DATABASE_URL` PostgreSQL est injectée par l'environnement/secret store,
  jamais écrite dans le dépôt ou les logs.
- `pgx/v5 v5.10.0` est la frontière runtime ; pas de `database/sql` ni ORM.
- `golang-migrate v4.19.1` est une CLI de déploiement, absente de `go.mod` et
  jamais exécutée au démarrage des répliques.
- La base d'intégration est exclusivement jetable et réservée au scénario.

`migrations/` contient les paires `up/down`. Une phase de déploiement unique
applique `up`, les instances ouvrent ensuite leur pool, et le test d'intégration
crée puis relit une donnée avant d'appliquer `down -all` au nettoyage.

## Composants et choix

- `github.com/jackc/pgx/v5 v5.10.0` — catalogue `pgx`, pool natif PostgreSQL.
- `golang-migrate` CLI v4.19.1 — catalogue admis, état versionné hors runtime.
- SQL statique paramétré — rend les requêtes révisables et interdit la
  composition de SQL avec entrée non fiable.

Patterns : `pattern:database:versioned-migrations`,
`pattern:antipattern:db-placeholder-cache-injection`.

## Alternatives rejetées

- `database/sql` : le besoin est PostgreSQL natif et `pgxpool` est plus direct.
- ORM ou générateur SQL : abstraction différente ; pas de duplication avec la
  recipe SQLite/sqlc.
- SQL dynamique : augmente le risque d'injection et contourne les paramètres.
- Migrations par réplique : course et droits excessifs ; la CLI est une étape de
  déploiement unique.

## Exemple complet et scénario observable

```sh
go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.19.1
migrate -path recipes/recipe-postgres-pgx/migrations -database "$DATABASE_URL" up
DATABASE_URL="$DATABASE_URL" go test -tags=postgres ./recipes/recipe-postgres-pgx/...
```

Le test réel ouvre le pool, écrit `integration-widget`, le relit puis applique
`down -all`. Il doit viser une base PostgreSQL autorisée et jetable : ne jamais
lancer cette commande contre une base partagée. Sans `DATABASE_URL`, le scénario
est **BLOCKED**, non couvert par une probe simulée.

## Bonnes pratiques et pièges

- Appeler `Ping` après création du pool et propager l'annulation du contexte.
- Fermer le pool ; utiliser `pgx.ErrNoRows` via `errors.Is` pour l'absence.
- Réserver une identité de migration et sérialiser les jobs de déploiement.
- Préférer les migrations rétrocompatibles ; `down` est testé mais n'est pas une
  stratégie de récupération automatique en production.

## Limites et extensions

La recipe ne couvre pas transactions métier, PgBouncer, réplication, backup,
multi-tenant, code generation ni migrations de données longues. Chaque besoin
ajoute une décision explicite au lieu d'élargir ce store exemple.

## Vérification

```sh
go test ./recipes/recipe-postgres-pgx/...
DATABASE_URL="$DATABASE_URL" go test -tags=postgres ./recipes/recipe-postgres-pgx/...
```

Le second test échoue volontairement si l'URL ou la CLI manque. Aucune probe
PostgreSQL n'est créée, afin que `probes/run.sh` reste sans service externe.

## Sources primaires

- [pgx v5](https://pkg.go.dev/github.com/jackc/pgx/v5) — pool, contexte,
  requêtes et erreurs.
- [golang-migrate](https://github.com/golang-migrate/migrate) — CLI, formats
  de migrations et procédure de déploiement.
- [PostgreSQL SQL syntax](https://www.postgresql.org/docs/current/sql.html) —
  paramètres et DDL doivent rester adaptés au moteur cible.

