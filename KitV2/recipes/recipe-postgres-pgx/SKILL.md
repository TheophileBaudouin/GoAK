---
name: recipe-postgres-pgx
description: "Implement PostgreSQL persistence with an explicit pgx/v5 pool, cancellable open plus Ping, positional SQL parameters, and deployment-run golang-migrate SQL files. Use for native PostgreSQL access; not for database/sql, ORMs, dynamic SQL, replica-start migrations, or Docker-dependent tests."
category: recipe
tags: [postgresql, pgx, database, sql, migrations, persistence]
last-verified: 2026-08-05
---

# recipe-postgres-pgx — pgx pool and SQL migrations

## Purpose and use cases

Provide a small, observable native PostgreSQL boundary: `Open` is cancellable,
configures a `pgxpool.Pool`, calls `Ping`, and `Close` releases the pool.
Queries use exclusively `$1…$n` and wrap errors. Versioned SQL migrations are
applied separately by the `golang-migrate` CLI before deployment.

## Prerequisites and architecture

- A PostgreSQL `DATABASE_URL` is injected by the environment/secret store,
  never written to the repository or the logs.
- `pgx/v5 v5.10.0` is the runtime boundary; no `database/sql` or ORM.
- `golang-migrate v4.19.1` is a deployment CLI, absent from `go.mod` and
  never run at replica startup.
- The integration database is exclusively disposable and reserved for the
  scenario.

`migrations/` contains the `up/down` pairs. A single deployment phase applies
`up`, instances then open their pool, and the integration test creates and
re-reads a record before applying `down -all` during cleanup.

## Components and choices

- `github.com/jackc/pgx/v5 v5.10.0` — `pgx` catalog, native PostgreSQL pool.
- `golang-migrate` CLI v4.19.1 — admitted catalog, versioned state outside the
  runtime.
- Static parameterized SQL — makes queries reviewable and forbids composing
  SQL with untrusted input.

Patterns: `pattern:database:versioned-migrations`,
`pattern:antipattern:db-placeholder-cache-injection`.

## Rejected alternatives

- `database/sql`: the need is native PostgreSQL and `pgxpool` is more direct.
- ORM or SQL generator: different abstraction; no duplication with the
  SQLite/sqlc recipe.
- Dynamic SQL: increases the injection risk and bypasses parameters.
- Per-replica migrations: race and excessive privileges; the CLI is a single
  deployment step.

## Complete example and observable scenario

```sh
go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.19.1
migrate -path recipes/recipe-postgres-pgx/migrations -database "$DATABASE_URL" up
DATABASE_URL="$DATABASE_URL" go test -tags=postgres ./recipes/recipe-postgres-pgx/...
```

The real test opens the pool, writes `integration-widget`, re-reads it, then
applies `down -all`. It must target an authorized, disposable PostgreSQL
database: never run this command against a shared database. Without
`DATABASE_URL`, the scenario is **BLOCKED**, not covered by a simulated probe.

## Best practices and pitfalls

- Call `Ping` after pool creation and propagate context cancellation.
- Close the pool; use `pgx.ErrNoRows` via `errors.Is` for absence.
- Reserve a migration identity and serialize deployment jobs.
- Prefer backward-compatible migrations; `down` is tested but is not an
  automatic recovery strategy in production.

## Limits and extensions

The recipe does not cover business transactions, PgBouncer, replication,
backup, multi-tenancy, code generation, or long-running data migrations. Each
need adds an explicit decision instead of widening this example store.

## Verification

```sh
go test ./recipes/recipe-postgres-pgx/...
DATABASE_URL="$DATABASE_URL" go test -tags=postgres ./recipes/recipe-postgres-pgx/...
```

The second test fails deliberately if the URL or the CLI is missing. No
PostgreSQL probe is created, so that `probes/run.sh` stays free of external
services.

## Primary sources

- [pgx v5](https://pkg.go.dev/github.com/jackc/pgx/v5) — pool, context,
  queries, and errors.
- [golang-migrate](https://github.com/golang-migrate/migrate) — CLI, migration
  formats, and deployment procedure.
- [PostgreSQL SQL syntax](https://www.postgresql.org/docs/current/sql.html) —
  parameters and DDL must stay adapted to the target engine.

