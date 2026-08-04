---
name: coder-websocket
description: "github.com/coder/websocket — pure-Go WebSocket client/server with context-aware, concurrency-safe APIs (successor to the deprecated nhooyr/websocket). Use when a Go service needs real-time bidirectional streaming (LLM token streaming, agent events, tool feedback, MCP transport) and you want a small, maintained, zero-CGO transport library."
category: library
tags: [websocket, real-time, streaming, networking, mcp, transport]
last-verified: 2026-08-04
---

# coder/websocket — real-time WebSocket transport

## Selection

[`github.com/coder/websocket`](https://github.com/coder/websocket) (v1.8.x,
Go 1.21+). Successor of the deprecated `nhooyr.io/websocket` — same API shape,
maintained by Coder (v1.8.15, 2026-06, 5.4k★).

**Why it passes the gate** (actual reason, not stars): a small, pure-Go
(no CGO) WebSocket implementation with a context-aware API —
`websocket.Dial(ctx, url, opts)` and `websocket.Accept(w, r, opts)` — and
concurrency-safe `Conn.Write/Read`. Connection lifecycle and cancellation are
driven by `context.Context` like the rest of Go, so it composes with the kit's
context/error rules without special-casing. It is the transport layer only —
no messaging protocol on top (that stays application-level, per the kit's
explicit-event-model guidance).

## Admission checklist

- [x] Actively maintained — v1.8.15 (2026-06), regular releases (2024–2026)
- [x] Single responsibility — WebSocket transport (client + server)
- [x] Idiomatic Go — context-driven lifecycle, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README + pkg.go.dev
- [x] Real-world usage — Coder products, VS Code Server, Tailscale ecosystem
- [x] Readable end-to-end — yes, small focused core
- [x] Justified by need — stdlib has no WebSocket; streaming agents need it

## Minimal use (client)

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

c, _, err := websocket.Dial(ctx, "wss://example.com/events", nil)
if err != nil {
    return err
}
defer c.Close(websocket.StatusNormalClosure, "done")

_, data, err := c.Read(ctx) // ctx cancels the read
```

## Minimal use (server)

```go
// http.Handler
func handleWS(w http.ResponseWriter, r *http.Request) {
    c, err := websocket.Accept(w, r, nil) // upgrades the connection
    if err != nil {
        return
    }
    defer c.Close(websocket.StatusNormalClosure, "done")

    for {
        _, data, err := c.Read(r.Context())
        if err != nil {
            return
        }
        if err := c.Write(ctx, websocket.MessageText, data); err != nil {
            return
        }
    }
}
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `gorilla/websocket` | Mature but archived/maintenance-mode since 2024; older callback-style API. |
| `nhooyr/websocket` | **Deprecated** — upstream moved to coder/websocket (same API). |
| Raw TCP + custom framing | Reinvents WebSocket semantics (subprotocol, ping/pong, close codes); not justified. |

## Notes

- **Transport only** — do not build state synchronization directly on
  WebSocket; define explicit event models at the application layer.
- **Streaming** — token/event streaming works by repeated `Read`/`Write` on one
  connection; cancellation via context, not by closing the socket.
- **v2 churn** — issue #402 (43r) tracks the v2.0.0 wishlist; pin the exact
  v1.8.x version (API may change at the v2 boundary).
- **MCP transport** — a valid transport candidate for MCP servers; the MCP SDK
  remains the higher-level choice when adopting the protocol.
