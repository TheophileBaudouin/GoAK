---
name: bbolt
description: "go.etcd.io/bbolt v1.5.0 — embedded B+tree key-value store, pure Go, ACID transactions, one writer at a time. Use when choosing an embedded KV store for single-process local persistence. Not for multi-writer/multi-node workloads, SQL, or server scenarios."
category: library
tags: [storage, embedded, key-value, bbolt, btree, ac-id]
last-verified: 2026-08-05
---

# bbolt — base clé-valeur embarquée

## Selection

[`go.etcd.io/bbolt`](https://github.com/etcd-io/bbolt) (v1.5.0, Go 1.25+).

**Why it passes the gate** (actual reason, not stars): it is the community
maintained fork of Bolt (etcd-io), with a **frozen, stable API** — a
single-file, zero-dependency, pure-Go B+tree store with full ACID transactions
(no fsync bypass), designed for a single process. It is the storage engine
under etcd, Caddy, and litestream: proven in production, small enough to read
end-to-end, and MIT licensed.

## Admission checklist

- [x] Actively maintained — v1.5.0 (2026-06-21), push 2026-08-03
- [x] Single responsibility — embedded KV store (B+tree, transactions)
- [x] Idiomatic Go — `Tx`/`Bucket` API, no magic, no cgo
- [x] Tests present + CI — yes; code-review 10/10 (scorecard 7.3)
- [x] Documentation — README + godoc + bolt docs
- [x] Real-world usage — etcd, Caddy, litestream, many embedded apps
- [x] Readable end-to-end — ~10 kLOC, layered (page/transaction/bucket)
- [x] Justified by need — the kit covered SQL embarqué (modernc-sqlite) but
      had zero KV-embarqué decision support; NOT popularity

## Minimal use

```go
db, _ := bolt.Open("app.db", 0o600, nil)
db.Update(func(tx *bolt.Tx) error {
    b, _ := tx.CreateBucketIfNotExists([]byte("items"))
    return b.Put([]byte("key"), []byte("value"))
})
db.View(func(tx *bolt.Tx) error {
    v := tx.Bucket([]byte("items")).Get([]byte("key"))
    return nil
})
```

Compilé et vérifié (roundtrip Update/View) avec v1.5.0 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `modernc-sqlite` (déjà au catalogue) | SQL embarqué : choisir quand le requêtage structuré compte ; bbolt quand la simplicité clé-valeur et la lecture à froid comptent. |
| dgraph-io/badger | LSM, plus rapide en écriture mais plus lourd, API plus complexe, maintenance Dgraph incertaine ; pas retenu face à la stabilité bbolt. |
| pebble | Orienté CockroachDB, ~100 kLOC, surdimensionné pour l'embarqué applicatif. |
| Redis (serveur) | Processus externe : différent du besoin « embarqué ». |

## Security note

- **0 advisory** OSV (vérifié 2026-08-05).
- Fichiers non chiffrés par défaut : bbolt protège l'intégrité des pages
  (checksums) mais pas la confidentialité — chiffrer au niveau fichier si
  sensible (voir `source:security:file-encryption`).
- Mode lecture seule propre via `bolt.Open(path, 0o400, &bolt.Options{ReadOnly:true})`.

## Utiliser cette librairie quand

- Persistance locale clé-valeur pour **un seul processus** (cache durable,
  métadonnées, index, state machine compacte).
- Les transactions ACID et la durabilité fsync comptent plus que le débit
  d'écriture.
- Zéro dépendance et zéro cgo sont requis (binaire autonome, embarqué,
  conteneurs slim).

## Ne pas utiliser cette librairie quand

- Plusieurs processus/instances écrivent le même fichier : bbolt est
  **single-writer** (un seul processus, un seul `Update` à la fois ; les autres
  écrivent en attente ou échouent selon timeout).
- Besoin de requêtes SQL, d'index secondaires, de réplication ou de sharding :
  choisir SQLite (modernc-sqlite) ou un serveur (PostgreSQL, Redis).
- Charge d'écriture intense concurrente : le verrouillage exclusif des
  transactions limite le débit (voir `pattern:database:pool-config` pour le
  cas serveur).

## Avantages

- API stable et figée depuis des années (contrat de maintenance prévisible).
- ACID complet, zéro dépendance, pure Go, un seul fichier de données.
- Lecture par pages mappées en mémoire : très bonnes lectures à froid.
- Moteur éprouvé : etcd, Caddy, litestream l'utilisent en production.

## Inconvénients

- Single-writer : pas de concurrence d'écriture, débit borné.
- Pas d'index secondaires ni de requêtage structuré (tout est scan/B+tree).
- Fichier non compacté automatiquement : un fort turnover de données laisse
  des pages libres (compaction manuelle par réécriture).
- Pas de réplication ni de mode serveur intégré.

## Pièges connus

- **Une seule écriture à la fois** : garder les `Update` courts et ne jamais
  retenir un `Tx` ouvert (il verrouille le fichier).
- Les valeurs retournées par `Bucket.Get` ne sont valides que **dans** la
  transaction : copier (`append([]byte(nil), v...)`) avant de sortir du
  callback.
- `bolt.Open` échoue si le fichier est verrouillé par un autre processus
  (TimeOut par défaut ~1 s) : choisir un path par instance.
- Ne pas stocker de données ≥ ~10 Go sans planifier la compaction (fichier
  fragmenté, croissance du fichier de pages libres).

## Sources vérifiées

- [etcd-io/bbolt (repo officiel, v1.5.0)](https://github.com/etcd-io/bbolt)
  — vérifié 2026-08-05
- [pkg.go.dev/go.etcd.io/bbolt](https://pkg.go.dev/go.etcd.io/bbolt) — vérifié
  2026-08-05
- [bbolt Open Options (ReadOnly, TimeOut)](https://pkg.go.dev/go.etcd.io/bbolt#Open)
  — vérifié 2026-08-05
- OSV : aucun advisory pour `go.etcd.io/bbolt` (requête API 2026-08-05)
- Artefacts internes : `source:architecture:embedded-kv`,
  `pattern:database:transaction-boundary`, catalog `modernc-sqlite`
