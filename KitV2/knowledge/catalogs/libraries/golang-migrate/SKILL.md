---
name: golang-migrate
description: "github.com/golang-migrate/migrate/v4 v4.19.1 — versioned SQL migrations executed by the deployment CLI. Use for an explicit, single-run migration step; never import it into application replicas or run it automatically at startup."
category: library
tags: [database, migrations, sql, postgresql, deployment, cli]
last-verified: 2026-08-05
---

# golang-migrate — versioned SQL migrations

## Selection

[`github.com/golang-migrate/migrate/v4`](https://github.com/golang-migrate/migrate)
v4.19.1 is admitted to apply, during deployment, versioned SQL migrations on
PostgreSQL. The CLI reads the files in order and maintains the migration
state. The kit keeps a single external command rather than a Go runtime
import: each application replica stays independent of the schema deployment
protocol.

## Admission checklist

- [x] **Distinct problem**: deploying a versioned schema, not executing the
  application's queries (pgx covers that second boundary).
- [x] **Fresh primary source**: repository, release v4.19.1, CLI documentation,
  and security policy verified on 2026-08-05.
- [x] **Compatible version**: supported v4 line, pinable binary at `v4.19.1`
  and `up`/`down` SQL migrations on the filesystem.
- [x] **Limited responsibility**: base migration, no ORM, HTTP framework, or
  replica orchestration.
- [x] **Maintenance**: active public repository, CI, and release history
  verified; revalidate within 90 days before any new adoption.
- [x] **Operational quality**: order, state, and graceful stop are exposed by
  the tool; the backup/rollback procedure remains the application's concern.
- [x] **Security**: `SECURITY.md` policy and advisory surfaces consulted on
  2026-08-05; URL secrets are neither committed nor logged.
- [x] **Alternatives**: a homegrown runner, `goose`, `tern`, and ORM
  migrations neither reduce the retained decision nor are admitted to the
  catalog.
- [x] **Verifiable real usage**: the PostgreSQL recipe applies this CLI before
  the integration test; it does not import it into the Go process.

## Minimal use

Install the CLI in the deployment environment, then apply the migrations the
project owns once:

```sh
go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.19.1
migrate -path recipes/recipe-postgres-pgx/migrations \
  -database "$DATABASE_URL" up
```

`DATABASE_URL` comes from the deployment's secret store. The application
starts only after this orchestrated step; it never runs `migrate up` at each
replica startup.

## Alternatives considered

| Alternative | Verdict |
| --- | --- |
| Homegrown SQL runner | Rejected: re-implements state, locking, and failure cases. |
| `pressly/goose` | Not admitted: re-evaluate separately if its operational choices become necessary. |
| `jackc/tern` | Not admitted: a pgx-specific alternative to re-evaluate, not a second recipe. |
| ORM migrations | Rejected: the kit keeps revisable SQL and an ORM-free boundary. |
| Go `migrate/v4` import | Rejected here: would create automatic migration in replicas. |

## When to use this library

- A shared database must receive revisable, versioned SQL migrations.
- The pipeline can provide a single, privileged, observable step before the
  application instances are deployed.
- The `up` and `down` files live in VCS and have a reviewed
  compatibility/rollback strategy.

## When NOT to use this library

- Each replica should run migrations at startup.
- An ad-hoc schema change without versioned history is what is wanted.
- The project cannot provide operational locking, a backup, or a repair
  procedure after an interrupted migration.

## Advantages

- Simple CLI, pinnable version, portable SQL files, and ordered migrations.
- Official PostgreSQL support and a clear `NNN_name.up.sql` /
  `NNN_name.down.sql` convention.
- Explicitly separates migration rights from runtime rights.

## Disadvantages

- A migration remains a state change: destructive rollbacks and multi-version
  deployments require human planning.
- The CLI replaces neither backup, SQL review, nor deployment policy.
- Base URLs can contain secrets and require correct encoding.

## Known pitfalls

- Do not add `migrate/v4` to `go.mod` for this recipe nor run the CLI inside
  the HTTP server.
- Run once with a dedicated deployment identity; avoid races between jobs and
  across replicas.
- Test `up` and `down` on a throwaway database, but prefer backward-compatible
  changes over a destructive production rollback.
- Do not write `DATABASE_URL`, passwords, or sensitive SQL into logs.

## Verified sources

- [Official repository](https://github.com/golang-migrate/migrate) — CLI,
  drivers, filesystem usage, and security policy, verified 2026-08-05.
- [Release v4.19.1](https://github.com/golang-migrate/migrate/releases/tag/v4.19.1)
  — retained version pin, verified 2026-08-05.
- [pkg.go.dev documentation v4](https://pkg.go.dev/github.com/golang-migrate/migrate/v4)
  — API and v4-line compatibility, verified 2026-08-05.
- [Official migration guide](https://github.com/golang-migrate/migrate/blob/master/MIGRATIONS.md)
  — conventions and migration practices, verified 2026-08-05.
