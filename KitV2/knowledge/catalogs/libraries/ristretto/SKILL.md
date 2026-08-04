---
name: ristretto
description: "github.com/dgraph-io/ristretto v2.4 — high-performance in-memory cache with admission policy (TinyLFU), bounded memory, and configurable key/value costs. Use when caching hot data (LLM responses, parsed files, embeddings) with strict memory budgets and you need better hit ratios than a plain LRU."
category: library
tags: [cache, memory, performance, tiny-lfu, in-memory]
last-verified: 2026-08-04
---

# ristretto — bounded in-memory cache

## Selection

[`github.com/dgraph-io/ristretto`](https://github.com/dgraph-io/ristretto)
(v2.4.2, Apache-2.0, ~7.0k★, pushed 2026-07-15).

**Why it passes the gate** (actual reason, not stars): a cache with a real
admission policy — TinyLFU with an LFU "door-keeper" and a sample-based LFU
eviction — plus explicit memory budgeting (per-key cost, `MaxCost`). That
combination gives materially better hit ratios than a plain LRU under churn,
which is the exact profile of LLM-response/parsed-file caching. Small, focused
API, production-grade (used by Dgraph), zero-CGO, actively maintained (v2.4.x
2025-2026).

## Admission checklist

- [x] Actively maintained — v2.4.2 (2026), releases through 2025
- [x] Single responsibility — in-memory cache with admission/eviction policy
- [x] Idiomatic Go — small typed API, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README, design doc, benchmarks
- [x] Real-world usage — Dgraph and the wider Go ecosystem
- [x] Readable end-to-end — yes, compact core
- [x] Justified by need — cache churn needs policy, not just eviction

## Minimal use

```go
cache, _ := ristretto.NewCache(&ristretto.Config{
    NumCounters: 1e7,     // number of keys to track frequency of (approx)
    MaxCost:     1 << 30, // maximum cost of cache (1 GB)
    BufferItems: 64,      // number of keys per Get buffer
})
cache.Set("key", value, 1)
value, ok := cache.Get("key")
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `sync.Map` / hand LRU | No admission policy or memory bound; hit ratio suffers under churn. |
| bigcache (dgraph-free) | Serialized values ([]byte), no cost model — ristretto is typed with budgets. |

## Notes

- `Get` returns `(interface{}, bool)` — type-assert on the consumer side.
- Issue-mined (130 issues): TTL support requested (#43, 25r) — ristretto
  does not expire by TTL natively; pair with an explicit expiry layer if
  needed. GitHub issue tracker is being deprecated by the project (#175).
- Use for hot-path caching where **memory bounds** matter; for ephemeral
  single-key memoization, `sync.Map` or a one-line map+mutex may be enough.
