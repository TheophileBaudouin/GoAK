# Plan — recipes prioritaires KitV2 (2026-08-05)

## Goal

Ajouter cinq recipes de référence sans modifier l'architecture du kit : sessions
navigateur, JWT Bearer, PostgreSQL/pgx/migrations, observabilité stdlib et
validation OpenAPI bidirectionnelle.

## Context

Les recettes existantes couvrent déjà CLI, configuration, REST, SQLite/sqlc,
workers, arrêt gracieux, TUI et Wails. Les catalogues admissibles couvrent scs,
golang-jwt, pgx et kin-openapi. `golang-migrate` est encore un pointeur Source
et doit passer la pipeline d'admission avant de devenir une fiche Library.

## Constraints

- Les cinq recipes suivent A1, Z2, Z3, Z6, C0-C2, le charter et les conventions
  déjà publiées ; chacune garde un `SKILL.md` inférieur à 500 lignes.
- Les dépendances runtime Go sont strictement scs v2.9.0, golang-jwt v5.3.1,
  pgx v5.10.0 et kin-openapi v0.146.0. `golang-migrate` v4.19.1 reste une CLI
  de déploiement documentée, sans import runtime ni ajout à `go.mod`.
- Testcontainers, Docker/Podman, OpenTelemetry et Prometheus ne sont pas
  introduits. Aucun runtime de conteneur autorisé n'est disponible localement.
- Les probes restent déterministes et sans service externe. Le scénario
  PostgreSQL réel requiert une `DATABASE_URL` jetable fournie hors dépôt.
- L'index router est uniquement produit par son builder ; les compteurs sont
  dérivés puis validés, jamais inventés.

## Done

- Cinq recipes actives, leurs exemples testés, quatre probes et leurs sources
  primaires sont présents ; aucune recipe Testcontainers n'est créée.
- `golang-migrate` est admis selon les neuf critères Z2 et son ancien pointeur
  est retiré avec ses références adaptées.
- Manifest et capacités sont en 2.3.0, avec les compteurs dérivés 71 skills
  produit (= 13 rules + 15 recipes + 43 catalogues), 15 recipes, 43 catalogues
  et 9 probes après génération. Le total 70 demandé initialement est
  arithmétiquement incompatible avec les trois autres compteurs.
- Les scénarios sans service passent ; le scénario PostgreSQL est exécuté si
  `DATABASE_URL` est fournie, sinon rapporté `BLOCKED`, jamais `PASS`.
- Les validateurs, formatage, analyse, tests, probes et revue fresh-context
  sont enregistrés dans l'évidence finale.

## Acceptance tasks

| ID | État initial | Résultat vérifiable |
| --- | --- | --- |
| PR-01 | PASS | Plan, tâches, décision et ledger créés avant code. |
| PR-02 | PASS | Admission fraîche de golang-migrate v4.19.1 et retrait du pointeur. |
| PR-03 | PASS | Recipes session et JWT, tests d'échec inclus, probes PASS. |
| PR-04 | BLOCKED | Recipe pgx et migrations créées ; scénario réel requiert `DATABASE_URL`. |
| PR-05 | PASS | Recipe slog/expvar, concurrence sous `-race`, probe PASS. |
| PR-06 | PASS | Recipe OpenAPI requête/réponse, probe PASS. |
| PR-07 | PASS | Métadonnées 2.3.0, roadmap, mémoires et routeur généré. |
| PR-08 | PARTIAL | Gates consignés ; PostgreSQL et revue fresh-context restent bloqués. |

## Source ledger

| Décision | Source primaire | État |
| --- | --- | --- |
| Sessions/cookies | https://pkg.go.dev/github.com/alexedwards/scs/v2 | vérifiée le 2026-08-05 |
| JWT Bearer | https://pkg.go.dev/github.com/golang-jwt/jwt/v5 | vérifiée le 2026-08-05 |
| PostgreSQL pgx | https://github.com/jackc/pgx | vérifiée le 2026-08-05 |
| Migrations | https://github.com/golang-migrate/migrate | admission à consigner PR-02 |
| Logs et métriques | https://pkg.go.dev/log/slog ; https://pkg.go.dev/expvar | vérifiées le 2026-08-05 |
| Contrat OpenAPI | https://pkg.go.dev/github.com/getkin/kin-openapi/openapi3filter | vérifiée le 2026-08-05 |
| Tests conteneurisés | https://pkg.go.dev/github.com/testcontainers/testcontainers-go | rejeté : runtime non autorisé/absent |

## Risks and stop conditions

Une dépendance non admise, un besoin de stockage persistant de session, une
authentification OpenAPI fail-open, ou une migration exécutée par chaque
réplique arrête le sous-travail concerné. Un échec répété trois fois d'une même
commande est rapporté plutôt que contourné.
