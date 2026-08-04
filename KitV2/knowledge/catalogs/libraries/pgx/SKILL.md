---
name: pgx
description: "github.com/jackc/pgx/v5 v5.10.0 — PostgreSQL driver and toolkit: native interface (pgxpool, pgx.Tx, COPY, LISTEN/NOTIFY) plus a database/sql adapter. Use when choosing a PostgreSQL driver. Not for other databases, and its native interface differs from database/sql semantics (transaction and error model)."
category: library
tags: [database, postgresql, driver, pgx, pool, sql]
last-verified: 2026-08-05
---

# pgx — driver PostgreSQL

## Selection

[`github.com/jackc/pgx/v5`](https://github.com/jackc/pgx) (v5.10.0, Go 1.25+).

**Why it passes the gate** (actual reason, not stars): it is the de-facto
PostgreSQL driver for Go — a native, pure-Go protocol implementation with
`pgxpool` (pooling), `pgx.Tx`, COPY, `LISTEN/NOTIFY`, and a `database/sql`
adapter (`pgx/v5/stdlib`) for drop-in compat. Heavily fuzzed (scorecard
fuzzing 10/10) and actively maintained. Its recent SQLi advisories are all
fixed in ≥ v5.9.2; the fiche pins that floor.

## Admission checklist

- [x] Actively maintained — v5.10.0 (2026-06-03), push 2026-08-01
- [x] Single responsibility — PostgreSQL protocol driver + toolkit
- [x] Idiomatic Go — native interfaces + stdlib adapter, no magic
- [x] Tests present + CI — yes; fuzzing 10/10
- [x] Documentation — godoc + wiki + extensive examples
- [x] Real-world usage — standard de facto, adoption massive
- [x] Readable end-to-end — layered (protocol/pool/conn), ~30 kLOC
- [x] Justified by need — le catalogue couvrait sqlc/sqlx/gorm mais pas le
      driver natif PostgreSQL ; NOT popularity

## Minimal use

```go
pool, _ := pgxpool.New(ctx, "postgres://user:pass@host:5432/db") // config = pas de connexion
defer pool.Close()
rows, _ := pool.Query(ctx, "SELECT id, name FROM items WHERE tenant_id = $1", 42)
```

Compilé (pgxpool + requête paramétrée `$n`) avec v5.10.0 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `lib/pq` | Maintenance minimale depuis des années, moins de fonctionnalités ; rejeté. |
| `database/sql` + `pgx/v5/stdlib` | Adapter quand un code existant utilise database/sql ; l'interface native est plus rapide (20-63 % selon workloads publiés) et expose COPY/NOTIFY. |
| gorm / sqlx (catalogue) | ORM/helpers au-dessus d'un driver : pgx est le socle ; sqlc reste recommandé pour le SQL typé (voir catalog `sqlc`). |
| `pgconn` seul | Bas niveau (protocole) : pgx = couche d'usage correcte. |

## Security note

- Historique : **5 advisories distincts** — GO-2024-2567 (panic Pipeline, fix v5.5.2),
  CVE-2024-27304 (SQLi, fix v5.5.4), CVE-2026-33815/33816 (memory-safety, fix
  v5.9.0), **GO-2026-5004** (SQLi via littéraux dollar-quoted en protocole
  simple, fix **v5.9.2**). **Épingler ≥ v5.9.2** ; v5.10.0 sain (vérifié
  2026-08-05, OSV).
- Toujours des requêtes paramétrées `$1..$n` ; ne jamais interpoler de valeurs
  (voir `pattern:antipattern:db-placeholder-cache-injection`).
- Scorecard 4.6 (code-review 1/10, token-permissions 0) : processus de revue
  à surveiller — compensé par fuzzing + maintenance active.

## Utiliser cette librairie quand

- Une application Go se connecte à PostgreSQL (interface native pour perf et
  fonctionnalités, stdlib adapter pour compat).
- Besoin de pooling (`pgxpool`), transactions explicites, COPY bulk, ou
  `LISTEN/NOTIFY`.
- La chaîne d'outillage PostgreSQL (sqlc peut générer du pgx) est visée.

## Ne pas utiliser cette librairie quand

- Autre base de données que PostgreSQL (MySQL, SQLite → autres drivers ;
  SQLite embarqué → `modernc-sqlite`).
- Le besoin se limite à du SQL statique typé : `sqlc` génère déjà du pgx —
  préférer le codegen (voir catalog `sqlc`).
- Simple `database/sql` suffit et le projet ne veut pas de dépendance driver
  directe : passer par l'adapter `pgx/v5/stdlib` derrière une interface.

## Avantages

- Interface native complète (COPY, NOTIFY, types PG, pgxpool) + adapter
  database/sql.
- Perf natives documentées supérieures à database/sql sur workloads réels.
- Fuzzé, maintenu activement, standard de facto de l'écosystème.
- Intégration sqlc (codegen typé) éprouvée.

## Inconvénients

- Surface d'API large : le modèle natif (pgx.Tx, err handling, modes de
  requête) diffère de database/sql — courbe d'apprentissage.
- La classe SQLi des placeholders est réapparue 2 fois sur pgx en 2 ans
  (CVE-2024-27304, GO-2026-5004), plus 2 advisories memory-safety : nécessite
  d'épingler les versions et de respecter les modes de requête.
- Scorecard process moyen (code review, token permissions).

## Pièges connus

- **Modes de requête et injection** : `QueryExecModeCacheStatement` +
  littéraux `$tag$` non contrôlés = surface SQLi (GO-2026-5004, fix 5.9.2) —
  épingler ≥ 5.9.2 et préférer `QueryExecModeExec` quand les requêtes sont
  construites dynamiquement (voir anti-pattern dédié).
- `pgxpool.New` ne **se connecte pas** (config seulement) : vérifier la
  connexion avec `pool.Ping(ctx)`.
- Ne jamais retenir un `rows` sans `rows.Close()` (ressources pool) ; itérer
  avec `for rows.Next()` puis `rows.Err()`.
- `LISTEN/NOTIFY` exige une connexion dédiée (pas une requête sur le pool).

## Sources vérifiées

- [jackc/pgx (repo officiel, v5.10.0)](https://github.com/jackc/pgx) — vérifié
  2026-08-05
- [pkg.go.dev/github.com/jackc/pgx/v5](https://pkg.go.dev/github.com/jackc/pgx/v5)
  — vérifié 2026-08-05
- [Advisory GHSA-j88v-2chj-qfwx / GO-2026-5004 (SQLi, fix 5.9.2)](https://github.com/jackc/pgx/security/advisories/GHSA-j88v-2chj-qfwx)
  — vérifié 2026-08-05 (sécurité officielle)
- [Advisory GHSA-mrww-27vc-gghv / CVE-2024-27304 (SQLi, fix 5.5.4)](https://github.com/jackc/pgx/security/advisories/GHSA-mrww-27vc-gghv)
  — vérifié 2026-08-05 (sécurité officielle)
- OSV : 5 advisories distincts pour `github.com/jackc/pgx/v5`, tous corrigés
  ≤ 5.9.2 (requête API 2026-08-05)
- Artefacts internes : `pattern:antipattern:db-placeholder-cache-injection`,
  `pattern:database:pool-config`, catalog `sqlc`
