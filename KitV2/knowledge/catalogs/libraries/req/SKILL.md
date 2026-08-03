---
name: req
description: "imroc/req — high-level Go HTTP client (requests-style, over net/http). EXTRACT-ONLY: extract retry/client-config patterns; do NOT copy its global package-level API. Canonical HTTP client in the kit stays net/http."
category: library
tags: [http, client, retry, extract-only]
last-verified: 2026-08-02
---

# req — HTTP client (extract-only)

> **extract-only: true** — admitted as a pattern source, NOT as a dependency to
> impose. The kit's canonical HTTP client is stdlib `net/http`.

## Selection (with restriction)

`imroc/req` v3 (4.8k★, pushed 2026-07, CI, in Awesome Go — passes the ≥500★ floor
and the <12mo activity check). It is a capable high-level client: chainable
client/request settings, retries, HTTP/1.1-2-3, request/response/transport
middleware, dump/debug, marshalling.

**Why restricted, not imposed:** its idiomatic style uses **package-level global
state** — `req.DevMode()`, `req.MustGet(...)`, `req.EnableForceHTTP1()` operate
on a shared default client reached via the package name. That is hidden mutable
global state, the exact anti-pattern this kit rejects. Copying it wholesale would
teach agents to reach for globals.

## What you MAY extract

- **Client-config pattern**: build one explicit `*req.Client` (or `*http.Client`),
  reuse it for all requests — never the package-global one.
- **Retry strategy**: configurable retry with backoff and a max-attempts cap.
- **Unified error handling**: an `OnAfterResponse` hook that converts non-2xx API
  bodies into Go errors, so handlers see only success-or-error.
- **Debug dump**: dump full request/response only on error (not in steady state).

These map cleanly onto stdlib `net/http` + a small `Retry` wrapper — you do not
need req for them.

## What you must NEVER copy

- `req.MustGet` / `req.DevMode` / any package-global client call.
- Treating the package name as a singleton Client.
- "Black Magic" auto-behaviours (auto-decode, auto-marshal) that hide what the
  wire actually carries — fine for a quick script, an anti-pattern for auditable
  service code.

## Canonical alternative (the kit default)

stdlib `net/http` with an explicit `*http.Client`, plus a ~15-line retry helper
(see `recipe-worker-pool` for bounded-fanout, and build retry on the same
context-cancellation primitives). Add req only if a team explicitly wants its
ergonomics AND accepts the global-state caveat.

## References

- imroc/req — <https://github.com/imroc/req> (4.8k★, 2026-07)
- The net/http boundary is documented in `chi` (server-side) and the
  stdlib philosophy in `rules/core/philosophy` (when it exists).
