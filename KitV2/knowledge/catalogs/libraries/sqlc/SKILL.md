---
name: sqlc
description: "sqlc v1.24.0 — compile-time type-safe code generation from static SQL for Go, Kotlin, Python, and TypeScript. Use when SQL remains the source of truth and query shapes are static; not for dynamic WHERE/ORDER/columns or an ORM abstraction."
category: library
tags: [database, sql, codegen, type-safety]
last-verified: 2026-08-05
---

# sqlc — génération de code depuis SQL

## Selection

[`github.com/sqlc-dev/sqlc`](https://github.com/sqlc-dev/sqlc) v1.24.0 is a
build-time SQL compiler. It validates SQL against a schema and emits typed query
methods without runtime reflection. It targets PostgreSQL, MySQL, and SQLite,
with Go and other language/plugin outputs. It is admitted for explicit static
SQL and active code generation, tests, documentation, and production use; it
is not an ORM and not a dynamic query builder.

## Admission checklist

- [x] Current v1.24.0 release and active upstream maintenance.
- [x] Single responsibility: schema-aware SQL parsing and code generation.
- [x] Generates plain typed code with no sqlc runtime dependency.
- [x] Tests, CI, documentation, examples, and plugin architecture exist.
- [x] The static-query boundary is explicit before adoption.

## Minimal workflow

```sql
-- query.sql
-- name: GetFoo :one
SELECT id, name FROM foos WHERE id = ?;
```

```sh
sqlc generate
```

Generated code is called explicitly by the application:

```go
func getFoo(ctx context.Context, q *db.Queries, id int64) (db.Foo, error) {
    foo, err := q.GetFoo(ctx, id)
    if err != nil {
        return db.Foo{}, fmt.Errorf("get foo: %w", err)
    }
    return foo, nil
}
```

## Hard limits

sqlc generates **static queries only**. Decide this boundary before adopting it:

- Dynamic WHERE, column lists, or ORDER BY need `database/sql` plus a query
  builder/helper instead.
- `sqlc.embed()` on outer joins requires verifying generated nullability; a SQL
  column that can be NULL must not be represented as a guaranteed value.
- Engine-specific features differ, especially between PostgreSQL and SQLite;
  validate every target statement with the selected engine.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| raw `database/sql` | Choose for dynamic SQL or when a query is too small to justify generation. |
| `sqlx` | Choose for a thin reflection/scanning helper when runtime query flexibility matters. |
| Squirrel/query builder | Choose for dynamic SQL construction; it does not replace schema-aware code generation. |
| GORM/Ent | Choose only when an ORM/data-model abstraction is an explicit product decision. |

## Utiliser cette librairie quand

- SQL is the source of truth and query shapes are known at build time.
- Generated methods should expose typed rows/errors without runtime reflection.
- The project wants the same generated query contract across `*sql.DB` and
  `*sql.Tx` through its driver boundary.

## Ne pas utiliser cette librairie quand

- WHERE, ORDER BY, columns, or joins change dynamically at runtime.
- The application needs an ORM's model lifecycle, migrations, or associations.
- The selected database engine does not support the SQL syntax being generated.
- Generated nullability cannot be reviewed for outer joins.

## Avantages

- SQL remains visible/auditable and schema errors surface during generation.
- Generated code has no sqlc runtime dependency or reflection requirement.
- Plugin architecture supports multiple output languages and database engines.
- Generated query interfaces fit transaction boundaries explicitly.

## Inconvénients

- Static-only query model is a hard adoption boundary.
- Generated output must be regenerated and reviewed with schema/query changes.
- Engine differences and nullable joins still require database-specific testing.
- Plugin/codegen versions become part of the build reproducibility policy.

## Pièges connus

- Resolve static versus dynamic SQL before writing the first query; do not force
  dynamic filters into malformed static workarounds.
- Inspect generated nullability for `LEFT`/`RIGHT` joins and `embed` usage.
- Pin the sqlc CLI/plugin versions and run generation in CI so generated code
  cannot silently drift.
- Validate SQLite/PostgreSQL/MySQL-specific features against the actual target
  engine rather than the SQL parser alone.

## Sources vérifiées

- [Official sqlc repository](https://github.com/sqlc-dev/sqlc) — API,
  maintenance, license, checked 2026-08-05.
- [sqlc v1.24.0 release](https://github.com/sqlc-dev/sqlc/releases/tag/v1.24.0)
  — current version and plugin changes, checked 2026-08-05.
- [sqlc package on pkg.go.dev](https://pkg.go.dev/github.com/sqlc-dev/sqlc) —
  CLI/plugin API, checked 2026-08-05.
- [sqlc documentation](https://docs.sqlc.dev/en/latest/overview/) — supported
  engines and workflow, checked 2026-08-05.
- [SQLC issue tracker](https://github.com/sqlc-dev/sqlc/issues) — dynamic-query
  and generation boundaries, checked 2026-08-05.
- [sqlc security advisories](https://github.com/sqlc-dev/sqlc/security/advisories)
  — package-specific security status, checked 2026-08-05.
