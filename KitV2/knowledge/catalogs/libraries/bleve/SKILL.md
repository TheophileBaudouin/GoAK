---
name: bleve
description: "github.com/blevesearch/bleve/v2 v2.6.0 — pure-Go full-text and vector search library (Scorch, BM25, faceting, highlighting, geo queries). Use when a Go service needs local embeddable search without an external engine; not for distributed search infrastructure."
category: library
tags: [search, full-text, indexing, bm25, scorch, pure-go]
last-verified: 2026-08-05
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

+ [x] Actively maintained — v2.6.0 (2026-04-30), with upstream changes through 2026-07
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

## When to use this library

+ A Go service needs local full-text search over documents, code, or logs
  without an external engine or a server to deploy.
+ The index must live in-process, with zero-CGO and simple cross-compilation.
+ BM25 ranking, faceting, highlighting, or geo queries are needed, with an
  idiomatic Go API.
+ The write volume can be handled in batches.

## When NOT to use this library

+ The data already lives in SQLite: FTS5 covers the need without a separate
  index to keep in sync.
+ The need is vector similarity, not full-text (sqlite-vec is complementary,
  not a replacement).
+ Distributed multi-node search is required (Elasticsearch brings the server
  infrastructure, bleve does not).
+ Ingestion is a continuous stream of isolated documents with no batching
  possible: Scorch accumulates segments and amplifies writes (see Known
  pitfalls).

## Advantages

+ Pure-Go, zero-CGO, embeddable: `bleve.Open` / `index.Search` with no server.
+ Real inverted index (Scorch format) with BM25 ranking, faceting,
  highlighting, and geo.
+ Active maintenance (v2.6.0, 2026-08, ~11.2k★, 11 contributors) and real
  usage (Couchbase ecosystem).
+ Stable v2 API: the historical API churn (RFC v1.0.0 #1350, v2.0.0 #1495) is
  resolved — pin `v2`.

## Disadvantages

+ Index separate from the source: a second write path to keep in sync.
+ Scorch (append-only segments + merges): write amplification and in-memory
  segment accumulation on unbatched continuous ingestion (issue #1783,
  docs/persister.md).
+ No native vector search — pairing is needed (sqlite-vec, tree-sitter) for
  structural/vector needs.
+ 858 open issues, mostly feature requests.

## Known pitfalls

+ Writing document by document degrades writes heavily: batch (1–200 docs per
  batch, guidance issue #1783) or tune `scorchMergePlanOptions` when batching
  is impossible.
+ On continuous streams, watch in-memory segment accumulation and merge
  frequency (docs/persister.md) — size the index before production, not
  after.
+ Pin `v2` explicitly: the API saw major churn before stabilization.

## Verified sources

+ [blevesearch/bleve (README, v2.6.0)](https://github.com/blevesearch/bleve)
  — verified 2026-08-04 (official repository)
+ [index/scorch/README.md — segmented index](https://github.com/blevesearch/bleve/blob/master/index/scorch/README.md)
  — verified 2026-08-04 (official docs)
+ [docs/persister.md — memory management](https://github.com/blevesearch/bleve/blob/master/docs/persister.md)
  — verified 2026-08-04 (official docs)
+ [Issue #1783 — batching guidance](https://github.com/blevesearch/bleve/issues/1783)
  — verified 2026-08-04 (official issue)
+ Internal artifact: `source:search:index-merge` (performance/Scorch)
