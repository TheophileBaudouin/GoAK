---
name: sqlc
description: "sqlc — compile-time type-safe Go generated from SQL (no ORM, no runtime reflection). Use when choosing a Go database access layer, adopting sqlc, or comparing it to sqlx/squirrel/ORMs."
category: library
tags: [database, sql, codegen, type-safety]
last-verified: 2026-08-04
---

# sqlc — SQL → Go code generation

## Selection

[`sqlc`](https://github.com/sqlc-dev/sqlc) (CLI, supports SQLite/PostgreSQL/MySQL).

**Why it passes the gate** (actual reason, not stars): it is the only tool that
takes **plain SQL as the source of truth** and generates type-safe Go query
methods at build time. A `:one` query becomes `GetFoo(ctx, id) (Foo, error)`;
a `:many` query becomes `ListFoos(ctx) ([]Foo, error)`. SQL errors surface at
generation time, and there is no runtime reflection — the generated code is
plain `database/sql`.

## Admission checklist

- [x] Actively maintained — ongoing releases, active community
- [x] Single responsibility — SQL compiler → Go (one thing, well)
- [x] Idiomatic Go — generates stdlib `database/sql` code
- [x] Tests present + CI — yes
- [x] Documentation — docs.sqlc.dev + SQLite tutorial
- [x] Real-world usage — adopted in production services
- [x] Readable end-to-end — `examples/authors/` shows the full workflow
- [x] Justified by need (type safety from SQL), NOT popularity

## Minimal workflow

```sql
-- query.sql
-- name: GetFoo :one
SELECT id, name FROM foos WHERE id = ?;
```

```sh
sqlc generate   # → emits models.go + query.sql.go (type-safe methods)
```

```go
q := db.New(conn)                       // *Queries, generated
foo, err := q.GetFoo(ctx, int64(1))     // type-safe, no manual Scan
```

## Hard limits (the #1 adoption pain — 600 open issues, top by reactions)

sqlc generates code for **static queries only**. It cannot handle:

- **Dynamic WHERE / column lists / ORDER BY** (#3414 "support dynamic queries"
  53👍, #2061 "dynamic order by" 35👍, #200 "optional WHERE" 25👍). If your query
  shape changes at runtime, sqlc is the wrong tool — use `database/sql` + a query
  builder (`squirrel`) or `sqlx`.
- **`sqlc.embed()` NULL handling in LEFT/RIGHT JOINs** (#2348 50👍, #2997 45👍,
  #3240 33👍) — the generated structs may declare non-nullable fields for columns
  that can be NULL. Verify generated nullability, or avoid `embed` on outer joins.
- **SQLite engine gaps** (#3132 "UPDATE FROM not supported") — the SQLite backend
  lacks some Postgres features; check your statement is supported before relying
  on it (relevant to `recipe-sqlite-sqlc`).

Decide sqlc vs raw `database/sql` on this boundary first — it is the single most
common reason users abandon sqlc.

See `recipe-sqlite-sqlc` for a runnable, tested example.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `database/sql` raw | Manual `rows.Scan(&a,&b)`, no compile-time SQL checking — the exact boilerplate sqlc removes. |
| `jmoiron/sqlx` | Reflection-based scanning; still dynamic, SQL not validated until runtime. |
| `Masterminds/squirrel` | A query *builder* — you stop writing SQL, and lose SQL-as-source-of-truth. Not type-safe from SQL. |
| ORM (gorm, ent) | Hides SQL behind a heavy abstraction; rejected for a kit favouring explicit, auditable SQL. |

## Notes

- sqlc is a **build-time tool**, not a runtime dependency — the generated code
  has zero sqlc imports. Nothing to vendor in your binary.
- The generated `*Queries` works against both `*sql.DB` and `*sql.Tx` (via its
  `DBTX` interface), so the same code runs inside or outside a transaction.

## Utiliser cette librairie quand

- SQL est la source de vérité : requêtes statiques typées compilées à la
  génération (`:one`/`:many` → méthodes Go typées).
- L'erreur SQL doit apparaître au moment de la génération, sans réflexion
  runtime.
- Le code généré doit rester du `database/sql` standard (zéro dépendance
  runtime).

## Ne pas utiliser cette librairie quand

- Les requêtes sont **dynamiques** (WHERE/ORDER BY/colonnes variables au
  runtime) : sqlc est statique uniquement (#3414, #2061, #200) — passer à
  database/sql + squirrel/sqlx (voir `pattern:antipattern:db-codegen-dynamic-queries`).
- Des LEFT/RIGHT JOIN avec `sqlc.embed()` doivent gérer la NULLabilité :
  vérifier le code généré ou éviter embed sur les outer joins (#2348, #2997).
- Le moteur cible est SQLite et la requête utilise des features absentes
  (ex. `UPDATE FROM`, #3132).

## Avantages

- SQL comme source de vérité unique : pas de réflexion runtime, typage
  généré.
- Build-time uniquement : zéro import sqlc dans le binaire généré.
- Compatible `*sql.DB` ET `*sql.Tx` (interface DBTX) — même code dans et
  hors transaction.
- Alternatives ORM rejetées pour le kit (SQL explicite et auditable).

## Inconvénients

- **Statique uniquement** : c'est la limite #1 d'adoption (600 issues
  ouvertes, top par réactions) — le périmètre dynamique est hors outil.
- `sqlc.embed()` fragile sur NULL des outer joins (vérifier la nullabilité
  générée).
- Moteur SQLite avec des gaps de features PostgreSQL (vérifier par requête).

## Pièges connus

- Tronquer la décision sur la frontière statique/dynamique AVANT de
  s'engager — c'est la raison la plus fréquente d'abandon.
- Générer et vérifier la nullabilité des embeds sur JOIN.
- Utiliser `sqlc.nembed()` (nullable embed) quand disponible pour les LEFT
  JOIN.

## Sources vérifiées

- [sqlc-dev/sqlc (repo officiel)](https://github.com/sqlc-dev/sqlc) — vérifié
  2026-08-02
- [Issue #3414 — dynamic queries](https://github.com/sqlc-dev/sqlc/issues/3414)
  / [#2061](https://github.com/sqlc-dev/sqlc/issues/2061) /
  [#2348 — embed NULL](https://github.com/sqlc-dev/sqlc/issues/2348) —
  vérifiées 2026-08-04 (issues officielles)
- [docs.sqlc.dev](https://docs.sqlc.dev/) — vérifié 2026-08-02
- Artefacts internes : `recipe-sqlite-sqlc`,
  `pattern:antipattern:db-codegen-dynamic-queries`, catalog
  `modernc-sqlite`
