---
name: bleve
description: "github.com/blevesearch/bleve v2.6 — pure-Go full-text search and indexing library (scorch index, BM25 ranking, faceting, highlighting, geo queries). Use when a Go service needs local full-text search over documents or code (no external search engine) with zero-CGO and embeddable deployment."
category: library
tags: [search, full-text, indexing, bm25, scorch, pure-go]
last-verified: 2026-08-04
---

# bleve — embeddable full-text search

## Selection

[`github.com/blevesearch/bleve/v2`](https://github.com/blevesearch/bleve)
(v2.6.0, Go 1.25+, Apache-2.0, ~11.2k★, pushed 2026-08-04).

**Why it passes the gate** (actual reason, not stars): the main **pure-Go**
full-text search engine — a real inverted index (scorch format) with BM25
ranking, faceting, highlighting, and geo support, embeddable in-process with
zero external server and zero-CGO. That is the exact shape the kit needs for
local search over docs/code in agent tooling. Single responsibility (indexing

+ search), idiomatic Go, active maintenance (v2.6.0, 2026-08), 11 active
contributors.

## Admission checklist

+ [x] Actively maintained — v2.6.0 (2026-08), steady releases
+ [x] Single responsibility — full-text indexing and search
+ [x] Idiomatic Go — `bleve.Open`, `index.Index(docID, doc)`, `search.Search`
+ [x] Tests present + CI — yes
+ [x] Documentation — README, tutorials, examples
+ [x] Real-world usage — Couchbase ecosystem and many Go services
+ [x] Readable end-to-end — yes, layered (index/scorch/query)
+ [x] Justified by need — local search without an external engine

## Minimal use

```go
index, err := bleve.Open("/tmp/example.bleve") // or bleve.New for create
query := bleve.NewMatchQuery("hello world")
searchReq := bleve.NewSearchRequest(query)
results, err := index.Search(searchReq)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| SQLite FTS5 | Great when the data already lives in SQLite; bleve is standalone and index-native. |
| sqlite-vec | Vector similarity, not full-text — complementary (see pointer `sqlite-vec`). |
| External engines (Elasticsearch) | Server infra; bleve is embeddable and zero-CGO. |

## Notes

+ Issue-mined (858 issues): historical API-churn threads (v1.0.0 RFC #1350,
  v2.0.0 proposal #1495) are resolved — v2 API is stable; pin `v2`.
+ Scorch is the default index type: append-only segments with merges —
  design for periodic merges on write-heavy workloads.
+ For code search specifically, consider pairing bleve (full-text) with
  tree-sitter (structure) once tree-sitter reaches ≥1.0 (see pointer).

## Utiliser cette librairie quand

+ Un service Go a besoin de recherche plein-texte locale (documents, code,
  logs) sans moteur externe ni serveur à déployer.
+ L'index doit être embarqué dans le processus, avec zéro-CGO et
  cross-compilation simple.
+ Le ranking BM25, le faceting, le highlight ou les requêtes géo sont
  nécessaires, avec une API Go idiomatique.
+ Le volume d'écriture est maîtrisable par lots (batching).

## Ne pas utiliser cette librairie quand

+ Les données vivent déjà dans SQLite : FTS5 couvre le besoin sans index
  séparé à synchroniser.
+ Le besoin est la similarité vectorielle, pas le plein-texte (sqlite-vec est
  complémentaire, pas un remplaçant).
+ Une recherche distribuée multi-nœuds est exigée (Elasticsearch apporte
  l'infra serveur, pas bleve).
+ L'ingestion est un flux continu de documents isolés sans batching possible :
  Scorch accumule les segments et amplifie les écritures (voir Pièges).

## Avantages

+ Pur-Go, zéro-CGO, embarquable : `bleve.Open` / `index.Search` sans serveur.
+ Vrai index inversé (format Scorch) avec ranking BM25, faceting, highlight,
  géo.
+ Maintenance active (v2.6.0, 2026-08, ~11.2k★, 11 contributeurs) et usage
  réel (écosystème Couchbase).
+ API v2 stable : le churn API historique (RFC v1.0.0 #1350, v2.0.0 #1495)
  est résolu — pinner `v2`.

## Inconvénients

+ Index séparé de la source : double écriture à maintenir en synchronisation.
+ Scorch (segments append-only + merges) : amplification d'écriture et
  accumulation de segments en mémoire sur ingestion continue non batchée
  (issue #1783, docs/persister.md).
+ Pas de recherche vectorielle native — pairing nécessaire (sqlite-vec,
  tree-sitter) pour les besoins structurels/vectoriels.
+ 858 issues ouvertes, majoritairement des demandes de fonctionnalités.

## Pièges connus

+ Écrire document par document dégrade fortement les écritures : batcher
  (1–200 docs par lot, guidance issue #1783) ou régler `scorchMergePlanOptions`
  si le batching est impossible.
+ Sur flux continu, surveiller l'accumulation de segments en mémoire et la
  fréquence des merges (docs/persister.md) — dimensionner l'index avant mise
  en prod, pas après.
+ Pinner `v2` explicitement : l'API a connu du churn majeur avant la
  stabilisation.

## Sources vérifiées

+ [blevesearch/bleve (README, v2.6.0)](https://github.com/blevesearch/bleve)
  — vérifié 2026-08-04 (repo officiel)
+ [index/scorch/README.md — segmented index](https://github.com/blevesearch/bleve/blob/master/index/scorch/README.md)
  — vérifié 2026-08-04 (docs officielles)
+ [docs/persister.md — memory management](https://github.com/blevesearch/bleve/blob/master/docs/persister.md)
  — vérifié 2026-08-04 (docs officielles)
+ [Issue #1783 — batching guidance](https://github.com/blevesearch/bleve/issues/1783)
  — vérifié 2026-08-04 (issue officielle)
+ Artefact interne : `source:search:index-merge` (performance/Scorch)
