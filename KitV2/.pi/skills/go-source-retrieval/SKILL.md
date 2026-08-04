---
name: go-source-retrieval
category: workflow
tags: [source, retrieval, offline, toolchain, resolve]
last-verified: 2026-08-04
description: Resolve only the Go source or toolchain unit needed for a task through the shipped offline bundle or pinned local toolchain. Use before relying on an API, idiom, or Go tool capability; return blocked instead of inventing unavailable knowledge.
---

# Go source retrieval

Use this skill before generating code that depends on an API or toolchain fact.

## Procedure

1. Classify the request by source and exact unit:
   - `pkg-doc`: package or symbol, for example `fmt` or `io.Reader`;
   - `toolchain`: `help:testflag`, `cmd:gofmt`, `cmd:pprof`, or `cmd:trace`;
   - `effective-go`: the bounded pinned document unit (the current bundle does not split headings).
2. Read metadata first. Select the smallest artifact by stable ID, then exact
   tag, then lexical ID. Do not preload a source family.
3. Resolve with `tools/offline` from the product root. It is offline by
   default, verifies SHA-256 content, and bounds excerpts before context load.
4. If the result is `blocked`, state the exact prerequisite. Never reconstruct
   a missing API or rule from model memory.
5. Carry the returned `pin`, `sha256`, and `verifier` into the source ledger or
   implementation plan when the fact affects generated code.
6. Use only the returned excerpt. Request a larger bounded result only when a
   smaller unit cannot answer the question.

## Deterministic selection

Exact unit matches win, followed by prefix and contains matches, then lexical
unit order. Wall-clock time, model scores, embeddings, and network availability
never choose the authoritative result.

## Validation

Run `go test ./tools/offline` and `GOPROXY=off bash probes/run.sh` after changing
retrieval behavior. A missing local package is `blocked`, not a successful
fallback to an unverified online request.

See `references/retrieval-contract.md` for the product-facing contract.
