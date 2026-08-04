---
name: modernc-sqlite
description: "modernc.org/sqlite v1.56.0 — CGO-free SQLite driver for database/sql, cross-compilable with CGO_ENABLED=0. Use when build portability/static targets matter; not when measured native SQLite throughput or unsupported VFS/features decide the project."
category: library
tags: [database, sqlite, driver, pure-go, cgo-free]
last-verified: 2026-08-05
---

# modernc-sqlite — driver SQLite sans CGO

## Selection

[`modernc.org/sqlite`](https://gitlab.com/cznic/sqlite) v1.56.0,
released 2026-08-03, transpiles SQLite's C implementation to Go and registers a
standard `database/sql` driver. It is admitted for static/cross-platform build
portability, active releases, tests, documentation, and the kit's zero-CGO
boundary; it is not selected on theoretical performance.

## Admission checklist

- [x] Current v1.56.0 release and Go 1.25+.
- [x] Single responsibility: SQLite engine exposed through `database/sql`.
- [x] `CGO_ENABLED=0` cross-builds for the supported Go targets.
- [x] Tests, CI, documentation, and a maintained canonical GitLab repository.
- [x] The build portability trade-off is explicit against mattn/go-sqlite3.

## Minimal use

```go
func openDB(dsn string) (*sql.DB, error) {
    db, err := sql.Open("sqlite", dsn)
    if err != nil {
        return nil, fmt.Errorf("open sqlite: %w", err)
    }
    return db, nil
}
```

Register the driver with a blank import in the package that owns the database
wiring. Use `recipe-sqlite-sqlc` for a tested store shape and explicit cleanup.

## Alternatives considered

| Driver | Verdict |
|---|---|
| `mattn/go-sqlite3` | Choose when CGO/native toolchains are acceptable and measured throughput justifies them. |
| `ncruces/go-sqlite3` | Consider for another CGO-free implementation when its WASM/SQLite boundary fits. |
| PostgreSQL/other server DB | Choose when replication, multi-node access, or server-side concurrency is required. |
| SQLCipher | Separate encryption requirement; modernc-sqlite does not provide it natively. |

## Utiliser cette librairie quand

- The application needs SQLite through standard `database/sql` and must build
  statically or cross-compile without a C compiler.
- CGO-free portability matters more than a measured native-driver advantage.
- `sqlc` or ordinary database/sql code can stay within SQLite's supported SQL.

## Ne pas utiliser cette librairie quand

- Native SQLite throughput is measured as the bottleneck and CGO is acceptable.
- The deployment requires an unsupported SQLite VFS, SQLCipher, or platform
  integration not covered by this driver.
- A server database is required for replication or multi-process write scale.
- The project cannot pin the matching `modernc.org/libc` dependency boundary.

## Avantages

- `CGO_ENABLED=0` static and cross-platform builds without a C toolchain.
- Standard `database/sql` integration and compatibility with sqlc patterns.
- Current SQLite engine updates and a maintained pure-Go distribution.
- `NewConnector` provides a connection boundary for instrumentation in current
  releases.

## Inconvénients

- Transpiled engine and `modernc.org/libc` dependency make internals harder to
  debug than a direct C binding.
- Performance and feature parity must be measured for the actual workload.
- Some VFS, transaction, Windows, and advanced SQLite behaviors have open
  upstream issues.

## Pièges connus

- Use driver name `sqlite` and pin the exact `modernc.org/libc` version required
  by the selected sqlite release; mismatches can cause build/type failures.
- Test transaction failure paths and `busy_timeout` behavior for the chosen
  locking mode.
- Check supported target GOOS/GOARCH before promising cross-compilation.
- Do not confuse CGO-free distribution with automatic data encryption,
  replication, or server-grade concurrency.

## Sources vérifiées

- [Canonical sqlite GitLab repository](https://gitlab.com/cznic/sqlite) —
  maintenance, license, checked 2026-08-05.
- [v1.56.0 tags](https://gitlab.com/cznic/sqlite/-/tags) — exact version,
  checked 2026-08-05.
- [sqlite on pkg.go.dev](https://pkg.go.dev/modernc.org/sqlite) — API,
  supported targets, and driver boundary, checked 2026-08-05.
- [v1.56.0 go.mod](https://gitlab.com/cznic/sqlite/-/blob/v1.56.0/go.mod)
  — dependency pinning, checked 2026-08-05.
- [sqlite issues](https://gitlab.com/cznic/sqlite/-/issues) — transaction,
  VFS, and platform limitations, checked 2026-08-05.
- [sqlite CHANGELOG](https://gitlab.com/cznic/sqlite/-/blob/v1.56.0/CHANGELOG.md)
  — current engine/security changes, checked 2026-08-05.
