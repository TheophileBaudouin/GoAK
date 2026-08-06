---
name: coder-websocket
description: "github.com/coder/websocket v1.8.15 — pure-Go WebSocket transport with context-aware client/server APIs and concurrent connection support. Use for bidirectional real-time streams; not for application-level messaging, state synchronization, or a one-way HTTP stream."
category: library
tags: [websocket, real-time, streaming, networking, mcp, transport]
last-verified: 2026-08-05
---

# coder/websocket — WebSocket transport

## Selection

[`github.com/coder/websocket`](https://github.com/coder/websocket) v1.8.15,
released 2026-06-15, is the maintained successor to `nhooyr.io/websocket`. It
implements RFC 6455 in a small pure-Go package with context-aware dialing,
acceptance, reads, writes, and close handling. It is admitted for the transport
boundary only; the application owns its message model and authorization.

## Admission checklist

- [x] Current v1.8.15 release, active Coder maintenance, CI, and tests.
- [x] Single responsibility: WebSocket client/server transport.
- [x] Pure Go and compatible with standard HTTP handlers.
- [x] Context-aware operations and documented concurrency constraints.
- [x] Documentation, examples, and real use in Coder's ecosystem.

## Minimal use

```go
func echo(w http.ResponseWriter, r *http.Request) error {
    c, err := websocket.Accept(w, r, nil)
    if err != nil {
        return fmt.Errorf("accept websocket: %w", err)
    }
    defer func() { _ = c.Close(websocket.StatusNormalClosure, "done") }() // close reports no recoverable handler error

    _, data, err := c.Read(r.Context())
    if err != nil {
        return fmt.Errorf("read websocket message: %w", err)
    }
    if err := c.Write(r.Context(), websocket.MessageText, data); err != nil {
        return fmt.Errorf("write websocket message: %w", err)
    }
    return nil
}
```

The handler's caller handles the returned error at the HTTP boundary. Configure
`AcceptOptions.OriginPatterns` explicitly when cross-origin clients are part of
the contract; origins are rejected by default.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `gorilla/websocket` | Existing deployments may keep it, but its maintenance history and API boundary are weaker for new context-aware code. |
| `nhooyr.io/websocket` | Deprecated predecessor; use coder/websocket for new work. |
| `gobwas/ws` | Choose for event-driven low-level performance only if the project accepts its more complex API. |
| HTTP streaming/SSE | Prefer when the protocol is one-way and WebSocket bidirectionality is unnecessary. |
| Raw TCP framing | Rejected unless the project explicitly owns WebSocket semantics, close codes, and ping/pong. |

## When to use this library
- A Go service needs bidirectional real-time events, tool feedback, or token
  streaming over WebSocket.
- Context cancellation, standard HTTP integration, and a small pure-Go transport
  matter.
- The application is prepared to define authentication and event semantics.

## When NOT to use this library
- One-way HTTP streaming or SSE is sufficient.
- The project needs MCP or another complete application protocol: use its SDK
  and select a transport deliberately.
- The project expects built-in state synchronization, authorization, or durable
  message delivery.

## Advantages
- Pure Go, context-aware, standard HTTP server/client boundary.
- Client and server APIs share the same connection model and close codes.
- `wsjson` and `wspb` helpers cover common typed message encodings.
- Origin checks are restrictive by default on server acceptance.

## Disadvantages
- The library is transport only; event schema, auth, heartbeats, and recovery
  remain application responsibilities.
- Only one reader and one writer may operate on a connection at a time; design
  the concurrency ownership explicitly.
- Context cancellation closes the connection rather than providing a protocol
  level graceful partial shutdown.
- The v2 boundary is still a future compatibility concern; pin v1.8.15.

## Known pitfalls
- Check `Accept` before using the connection, and treat `Close` as an operation
  whose error may matter at the boundary.
- Set a read limit and validate Origin/subprotocols for the trust boundary.
- Do not run multiple concurrent readers or writers on one connection.
- Define application-level events and authorization; WebSocket framing is not
  state synchronization or authentication.

## Verified sources
- [coder/websocket repository](https://github.com/coder/websocket) — API,
  maintenance, license, checked 2026-08-05.
- [v1.8.15 release](https://github.com/coder/websocket/releases/tag/v1.8.15)
  — exact version and release date, checked 2026-08-05.
- [Package documentation](https://pkg.go.dev/github.com/coder/websocket) —
  Dial/Accept/Conn API and concurrency limits, checked 2026-08-05.
- [Issue #546](https://github.com/coder/websocket/issues/546) — prepared-write
  limitation, checked 2026-08-05.
- [Issue #402](https://github.com/coder/websocket/issues/402) — v2 boundary,
  checked 2026-08-05.
