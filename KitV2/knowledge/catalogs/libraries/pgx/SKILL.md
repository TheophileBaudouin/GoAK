---
name: pgx
description: "github.com/jackc/pgx/v5 v5.10.0 — native PostgreSQL driver/toolkit with pgxpool, transactions, COPY, LISTEN/NOTIFY, and a database/sql adapter. Use for PostgreSQL; not for other databases or when an ORM/code generator alone is the required boundary."
category: library
tags: [database, postgresql, driver, pgx, pool, sql]
last-verified: 2026-08-05
---

# pgx — driver PostgreSQL

## Selection

[`github.com/jackc/pgx/v5`](https://github.com/jackc/pgx) v5.10.0,
released 2026-06-03, is a pure-Go PostgreSQL protocol driver with native
connections/pools and a `database/sql` adapter. It is admitted for this focused
PostgreSQL boundary, active maintenance, tests/fuzzing, documentation, and
production adoption; it is not chosen only by popularity.

## Admission checklist

- [x] Current v5.10.0 and Go 1.25+.
- [x] Single responsibility: PostgreSQL protocol, pooling, and typed operations.
- [x] Native `pgx` plus `pgx/v5/stdlib` adapter are documented.
- [x] Tests, CI, fuzzing, documentation, and active releases exist.
- [x] Security fixes and protocol hardening are tracked in upstream advisories.

## Minimal use

```go
func query(ctx context.Context, dsn string, tenantID int64) error {
    pool, err := pgxpool.New(ctx, dsn)
    if err != nil {
        return fmt.Errorf("create postgres pool: %w", err)
    }
    defer pool.Close() // pool.Close has no error return
    if err := pool.Ping(ctx); err != nil {
        return fmt.Errorf("ping postgres: %w", err)
    }
    rows, err := pool.Query(ctx,
        "SELECT id, name FROM items WHERE tenant_id = $1", tenantID)
    if err != nil {
        return fmt.Errorf("query items: %w", err)
    }
    defer rows.Close() // rows.Close has no error return
    for rows.Next() {
        // scan the row at this application boundary
    }
    return rows.Err()
}
```

Use `pgxpool` for concurrent application work; a single `pgx.Conn` is not a
concurrency-safe shared pool.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `pgx/v5/stdlib` | Use when existing code requires `database/sql`; native pgx remains the richer boundary. |
| `lib/pq` | Do not start new work on the older maintenance model. |
| GORM/sqlx | Higher-level ORM/helper choices; select them when their abstraction, not just the driver, is required. |
| sqlc | Code generator that can target pgx; complementary to the runtime driver. |

## When to use this library
- A Go service uses PostgreSQL and needs native pooling, transactions, COPY,
  notifications, types, or protocol controls.
- The application can own connection lifecycle, query modes, and parameterized
  SQL policy.
- Existing `database/sql` code needs the pgx driver through `stdlib`.

## When NOT to use this library
- The database is SQLite, MySQL, or another non-PostgreSQL engine.
- SQL code generation or an ORM is the actual required boundary rather than a
  runtime driver.
- A single `database/sql` interface is enough and native pgx features add no
  value.

## Advantages
- Native PostgreSQL features plus a standard-library adapter.
- `pgxpool`, COPY, LISTEN/NOTIFY, typed PostgreSQL values, and tracing.
- Active maintenance, fuzzing, protocol hardening, and sqlc integration.

## Disadvantages
- Native transaction/error/query modes differ from `database/sql` and require
  learning the API.
- Pool configuration and connection ownership are application decisions.
- Security fixes require exact version pinning and safe query-mode choices.

## Known pitfalls
- Pin v5.9.2 or later; the historical placeholder/dollar-quoted SQL injection
  advisory is fixed in current v5.10.0.
- Always use parameters (`$1`...); never interpolate untrusted values.
- `pgxpool.New` creates configuration/pool state but does not prove a live
  database connection; call `Ping` when startup validation requires it.
- Close rows and inspect `rows.Err`; keep LISTEN/NOTIFY on a dedicated connection
  rather than an arbitrary pool query.
- Review PgBouncer compatibility and disable prepared-statement modes when its
  transaction pooling requires that policy.

## Verified sources
- [Official pgx repository](https://github.com/jackc/pgx) — API, maintenance,
  license, checked 2026-08-05.
- [pgx releases](https://github.com/jackc/pgx/releases) — v5.10.0 current tag,
  checked 2026-08-05.
- [pgx v5 on pkg.go.dev](https://pkg.go.dev/github.com/jackc/pgx/v5) — API,
  compatibility, checked 2026-08-05.
- [SQL injection advisory](https://github.com/jackc/pgx/security/advisories/GHSA-j88v-2chj-qfwx)
  — fixed v5.9.2, checked 2026-08-05.
- [Earlier SQL advisory](https://github.com/jackc/pgx/security/advisories/GHSA-mrww-27vc-gghv)
  — fixed version, checked 2026-08-05.
- [pgx changelog](https://github.com/jackc/pgx/blob/master/CHANGELOG.md) —
  v5.10 hardening, checked 2026-08-05.
