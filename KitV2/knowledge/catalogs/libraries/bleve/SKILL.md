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
