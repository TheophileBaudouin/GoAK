---
name: bbolt
description: "go.etcd.io/bbolt v1.5.0 — embedded pure-Go ACID B+tree key-value store with one writer at a time. Use for single-process local persistence; not for SQL, replication, multi-node, or high concurrent write workloads."
category: library
tags: [storage, embedded, key-value, bbolt, btree, acid]
last-verified: 2026-08-05
---

# bbolt — base clé-valeur embarquée

## Selection

[`go.etcd.io/bbolt`](https://github.com/etcd-io/bbolt) v1.5.0 (2026-06-21,
Go 1.25+) is a single-file pure-Go B+tree store with ACID transactions and a
stable bucket API. It is admitted for focused single-process persistence,
active maintenance, tests, documentation, and production use in embedded
systems; not for popularity.

## Admission checklist

- [x] Current v1.5.0 release and active etcd-io maintenance.
- [x] Single responsibility: embedded key-value storage.
- [x] Pure Go, zero direct dependency, tests, CI, and documentation.
- [x] ACID read/write transactions with an explicit single-writer boundary.
- [x] Small enough to inspect and used by real Go infrastructure.

## Minimal use

```go
func put(path string) error {
    db, err := bolt.Open(path, 0o600, nil)
    if err != nil {
        return fmt.Errorf("open bbolt: %w", err)
    }
    defer func() { _ = db.Close() }()
    return db.Update(func(tx *bolt.Tx) error {
        bucket, err := tx.CreateBucketIfNotExists([]byte("items"))
        if err != nil {
            return fmt.Errorf("create bucket: %w", err)
        }
        if err := bucket.Put([]byte("key"), []byte("value")); err != nil {
            return fmt.Errorf("put value: %w", err)
        }
        return nil
    })
}
```

Values returned by `Bucket.Get` are valid only during the transaction; copy
bytes before returning them to the caller.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `modernc-sqlite` | Choose when SQL, joins, or structured queries matter. |
| Badger | Choose when an LSM write model justifies its larger operational/API surface. |
| Pebble | Choose for storage-engine workloads that justify a much larger dependency. |
| Redis/PostgreSQL | Choose when a server, replication, or multi-process access is required. |

## Utiliser cette librairie quand

- One process needs durable local key-value state, metadata, or a compact state
  machine.
- ACID transactions and simple bucket/key access matter more than SQL queries.
- A pure-Go, single-file binary is desirable.

## Ne pas utiliser cette librairie quand

- Multiple processes must write the same file or the workload is write-heavy and
  highly concurrent.
- SQL, secondary indexes, replication, sharding, or a server API is required.
- The application cannot plan manual compaction for high data turnover.

## Avantages

- Pure Go, single-file storage with ACID transactions and stable API.
- Simple bucket/cursor model and no external server.
- v1.5.0 adds options such as `MaxSize` and `NoStatistics` for operational
  control.

## Inconvénients

- One write transaction at a time; long transactions hold the file lock.
- No SQL or secondary indexes, replication, or built-in server mode.
- Memory-mapped files and free pages require platform and compaction planning.
- Data is not encrypted by default.

## Pièges connus

- Keep `Update` callbacks short and never retain a transaction after its callback.
- Copy bytes obtained from `Get` before leaving the read transaction.
- Check `Open`, transaction, bucket, and close errors; do not teach `_` as the
  default path.
- Configure timeout/path ownership when another process may hold the file lock.
- Encrypt sensitive data at the file/application boundary; bbolt provides
  integrity checks, not confidentiality.

## Sources vérifiées

- [Official bbolt repository](https://github.com/etcd-io/bbolt) — maintenance,
  API, license, checked 2026-08-05.
- [bbolt v1.5.0 package](https://pkg.go.dev/go.etcd.io/bbolt@v1.5.0) — exact
  version and API, checked 2026-08-05.
- [bbolt changelog](https://github.com/etcd-io/bbolt/blob/main/CHANGELOG/CHANGELOG-1.5.md)
  — v1.5.0 changes, checked 2026-08-05.
- [bbolt Open API](https://pkg.go.dev/go.etcd.io/bbolt#Open) — options and lock
  behavior, checked 2026-08-05.
- [bbolt limitations](https://github.com/etcd-io/bbolt#caveats--limitations) —
  single-writer and mmap constraints, checked 2026-08-05.
