---
name: req
description: "github.com/imroc/req/v3 v3.60.0 — high-level HTTP client over net/http with retries, HTTP/1.1/2/3, and request/response middleware. EXTRACT-ONLY: study explicit-client/retry patterns; do not impose its package-global API over the kit's net/http default."
category: library
tags: [http, client, retry, extract-only]
last-verified: 2026-08-05
---

# req — client HTTP (extract-only)

> **extract-only: true** — use the research to inform explicit `net/http`
> patterns; do not copy a package-global singleton into consumer services.

## Selection

[`github.com/imroc/req`](https://github.com/imroc/req) v3.60.0,
released 2026-07-02, is a high-level HTTP client with retries, HTTP/1.1/2/3,
TLS/proxy options, middleware, and response handling. It is admitted as a
pattern source while the kit's canonical client remains an explicit stdlib
`*http.Client`: the convenience package API can hide mutable default state and
wire behavior.

## Admission checklist

- [x] Current v3.60.0 and active upstream maintenance.
- [x] Single responsibility: configurable HTTP client ergonomics.
- [x] Tests, CI, documentation, and a maintained v3 module exist.
- [x] Retry, response-size, and streaming behavior have current issue/release
      evidence.
- [x] Restriction is explicit: this is not the kit's default client dependency.

## What you MAY extract

- Build one explicit client and inject/reuse it rather than using a package
  singleton.
- Retry only eligible transient failures with context, bounded attempts, and
  backoff.
- Convert non-2xx responses into typed/opaque errors at one response boundary.
- Bound response bodies with the current max-size option and use streaming for
  large multipart uploads.

## What you must NEVER copy

- Package-global default-client calls such as `req.MustGet` or `req.DevMode`.
- Auto-decode/auto-marshal behavior when service auditability requires seeing
  the wire contract explicitly.
- Unlimited response reads, retries without a context/attempt cap, or debug
  dumps containing credentials/tokens.

## Canonical alternative (the kit default)

Use stdlib `net/http` with an explicit `*http.Client`, a small retry helper, and
explicit JSON/body handling. Add req only after a project explicitly accepts
its API and dependency/security trade-offs.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `net/http` | Kit default: smallest explicit client boundary and maximum auditability. |
| `go-resty/resty` | Consider when its mature REST ergonomics and middleware match the project better. |
| `goforj/httpx` | Wrapper built on req; not a lower-dependency replacement. |
| Hand-written retry/client singleton | Reject hidden global state and unbounded retry behavior. |

## When to use this library
- As an extract-only source for explicit client setup, bounded retry, response
  middleware, and body-size handling.
- A project explicitly wants HTTP/3/TLS/proxy features and accepts the dependency
  and API boundary after review.

## When NOT to use this library
- The kit's canonical auditable `net/http` client is sufficient.
- Package-global convenience calls would be copied into shared service code.
- The response body may be unbounded or debug output may expose credentials.

## Advantages
- Rich HTTP/1.1/2/3 client, retries, middleware, TLS/proxy options, and upload
  support in one package.
- v3.60 adds response-size bounding and streams large multipart uploads through
  `io.Pipe`.
- Extractable patterns map cleanly to smaller stdlib implementations.

## Disadvantages
- Larger surface and hidden convenience state than explicit `net/http`.
- Auto-read response behavior must be bounded or disabled when handling large or
  untrusted bodies.
- Retry, impersonation, TLS fingerprinting, and HTTP/3 features need security
  and operational review instead of being enabled by default.

## Known pitfalls
- Set a maximum response size; auto-read is enabled by default and an oversized
  response must not be allowed to consume unbounded memory.
- Use a replayable/streaming body intentionally: retries require a body that can
  be recreated or rewound.
- Treat malformed URLs and TLS fingerprinting as security-sensitive options.
- Keep debug dumps off normal paths and redact authorization/cookie headers.

## Verified sources
- [Official req repository](https://github.com/imroc/req) — API, maintenance,
  license, checked 2026-08-05.
- [req v3 on pkg.go.dev](https://pkg.go.dev/github.com/imroc/req/v3) — module and
  API metadata, checked 2026-08-05.
- [req releases](https://github.com/imroc/req/releases) — v3.60.0 current
  release and changes, checked 2026-08-05.
- [req client source](https://github.com/imroc/req/blob/master/client.go) —
  auto-read and response-size behavior, checked 2026-08-05.
- [Issue #406](https://github.com/imroc/req/issues/406) — response size bound,
  checked 2026-08-05.
- [Issue #433](https://github.com/imroc/req/issues/433) — multipart memory
  behavior and fix, checked 2026-08-05.
- [GO-2024-3098](https://pkg.go.dev/vuln/GO-2024-3098) — malformed URL
  advisory, checked 2026-08-05.
