---
name: ristretto
description: "github.com/dgraph-io/ristretto/v2 v2.4.2 — concurrent generic in-memory cache with TinyLFU admission, sampled-LFU eviction, cost-based capacity, and optional TTL. Use for single-process hot-data caching under a memory budget; not for distributed storage or durable state."
category: library
tags: [cache, memory, performance, tiny-lfu, in-memory]
last-verified: 2026-08-05
---

# ristretto — cache mémoire borné

## Selection

[`github.com/dgraph-io/ristretto/v2`](https://github.com/dgraph-io/ristretto)
v2.4.2, released 2026-07-07, is a generic concurrent cache using TinyLFU admission,
SampledLFU eviction, cost-based capacity, batching, and optional TTL. It is
admitted for a focused single-process hot-cache boundary, active maintenance,
tests, documentation, and real use; not for popularity or distributed storage.

## Admission checklist

- [x] Current v2.4.2 and Go 1.24+.
- [x] Single responsibility: concurrent in-memory cache.
- [x] Generic `Get`/`Set` API with explicit cost and capacity.
- [x] Tests, CI, design documentation, benchmarks, and active releases exist.
- [x] The asynchronous admission/eviction semantics are documented for callers.

## Minimal use

```go
func cacheValue() (string, bool) {
    cache, err := ristretto.NewCache(&ristretto.Config[string, string]{
        NumCounters: 1e4,
        MaxCost: 1 << 20,
        BufferItems: 64,
    })
    if err != nil {
        return "", false
    }
    if !cache.Set("key", "value", 1) {
        return "", false
    }
    cache.Wait()
    value, ok := cache.Get("key")
    return value, ok
}
```

`Set` is buffered and can be dropped under contention; call `Wait` when a test
or boundary needs pending writes applied. Choose `MaxCost` in a meaningful
application unit rather than assuming it means bytes automatically.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `sync.Map`/map+mutex | Prefer for simple low-volume memoization without admission or cost policy. |
| bigcache | Choose for a byte-oriented sharded cache when its serialization model fits. |
| freecache | Choose for a simpler byte cache when TinyLFU/cost semantics are unnecessary. |
| Redis/remote cache | Choose for shared/distributed cache state; Ristretto is process-local. |

## Utiliser cette librairie quand

- Hot data needs a process-local memory budget and an admission policy under
  churn.
- Values are generic and entries can expose a meaningful cost.
- Asynchronous buffered writes and eventual cache admission are acceptable.

## Ne pas utiliser cette librairie quand

- Cache state must be shared between processes or survive process restart.
- Every `Set` must synchronously guarantee admission or every `Get` must observe
  the write immediately.
- Durable data, exact LRU semantics, or a simple one-key memo is required.

## Avantages

- TinyLFU admission plus SampledLFU eviction avoids wasting capacity on cold
  churn better than a naive LRU in the intended workload.
- Generic v2 API, explicit cost, optional TTL, metrics, and concurrent operation.
- Pure Go, single-process deployment, and small focused surface.

## Inconvénients

- Buffered operations can be dropped or delayed under contention.
- Capacity is cost-based; the caller must define a meaningful cost model.
- TTL uses bucket/ticker semantics rather than precise per-entry scheduling.
- It is not durable or distributed.

## Pièges connus

- Call `Wait` when a test or lifecycle boundary needs buffered `Set` operations
  applied; do not assert immediate visibility without that synchronization.
- Treat a false `Set` result as a rejected/dropped admission, not as durable
  storage failure recovery.
- Configure `NumCounters`, `MaxCost`, and `BufferItems` from workload measurements.
- Add an application expiry policy when the cache's TTL granularity is too coarse.
- Never use a process-local cache as the source of truth for user or security
  state.

## Sources vérifiées

- [Official Ristretto repository](https://github.com/dgraph-io/ristretto) —
  maintenance, design, license, checked 2026-08-05.
- [Ristretto v2.4.2 releases](https://github.com/dgraph-io/ristretto/releases) —
  exact version and memory regression fix, checked 2026-08-05.
- [Ristretto v2 on pkg.go.dev](https://pkg.go.dev/github.com/dgraph-io/ristretto/v2)
  — generic API, checked 2026-08-05.
- [Cache implementation](https://github.com/dgraph-io/ristretto/blob/main/cache.go)
  — buffering and lifecycle, checked 2026-08-05.
- [TTL implementation](https://github.com/dgraph-io/ristretto/blob/main/ttl.go)
  — expiry semantics, checked 2026-08-05.
- [Issue #493](https://github.com/dgraph-io/ristretto/issues/493) — v2.4.2
  memory regression context, checked 2026-08-05.
