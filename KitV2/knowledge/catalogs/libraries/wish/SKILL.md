---
name: wish
description: "charm.land/wish/v2 v2.0.3 — SSH application framework with middleware, PTY sessions, Bubble Tea integration, access control, and rate limiting. Use for remote Go/TUI applications over SSH; not for a raw SSH server/client or an unbounded public listener."
category: library
tags: [ssh, tui, server, remote, middleware]
last-verified: 2026-08-05
---

# wish — framework d'applications SSH

## Selection

[`charm.land/wish/v2`](https://github.com/charmbracelet/wish) v2.0.3,
released 2026-07-31, builds SSH applications on `charm.land/ssh`. It provides
middleware for logging, access control, rate limiting, metrics, recovery, Git,
and Bubble Tea sessions. It is admitted for this focused remote application
boundary and active Charm maintenance; it is not the lower-level SSH protocol
library.

## Admission checklist

- [x] Current v2.0.3 and active upstream maintenance.
- [x] Single responsibility: middleware/application composition over SSH.
- [x] Bubble Tea, PTY, auth, timeout, access-control, and observability options.
- [x] Tests, CI, documentation, and real Soft Serve/Charm ecosystem use exist.
- [x] Underlying host-key/auth/session trust boundaries are explicit.

## Minimal use

```go
func server(model tea.Model) (*ssh.Server, error) {
    srv, err := wish.NewServer(
        wish.WithAddress(":2222"),
        wish.WithHostKeyPath("/var/lib/app/ssh_host_ed25519"),
        wish.WithBubbletea(model),
    )
    if err != nil {
        return nil, fmt.Errorf("create SSH application: %w", err)
    }
    return srv, nil
}
```

Add public-key allowlists, persistent dedicated host keys, timeouts, rate
limiting, and access-control middleware before exposing the listener. A public
Wish server has no automatic global connection cap; design one at the
infrastructure/application boundary.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `charm.land/ssh` | Prefer for a server/session layer without Wish's middleware/app framework. |
| `golang.org/x/crypto/ssh` | Prefer for low-level protocol/client control; more session plumbing is yours. |
| gliderlabs/ssh | Predecessor/legacy boundary; do not choose for new work without a fresh decision. |
| Local Bubble Tea | Prefer when remote access is not a product requirement. |

## Utiliser cette librairie quand

- A Bubble Tea TUI or Go command must run in remote SSH sessions.
- Middleware for auth, access control, logging, metrics, rate limits, and panic
  recovery should compose around each session.
- The product has an explicit remote workbench/SSH trust model.

## Ne pas utiliser cette librairie quand

- A plain local TUI or one-off SSH handler is sufficient.
- The project needs an SSH client or low-level protocol implementation.
- The public listener cannot provide host-key persistence, authentication,
  timeouts, rate limiting, and connection/resource limits.

## Avantages

- High-level SSH application composition over maintained session/PTY APIs.
- Bubble Tea integration plus auth, access-control, rate-limit, logging,
  recovery, metrics, and Git middleware.
- v2 keeps a clear Charm module path and recent panic containment.

## Inconvénients

- Opinionated middleware/application framework with SSH and Bubble Tea coupling.
- No inherent connection-count cap; goroutine/file-descriptor/memory limits need
  explicit design.
- Security defaults are not a complete deployment policy; allowlists and rate
  limiting must be wired by the consumer.

## Pièges connus

- Persist a dedicated host key and never reuse a client key as a server key.
- Configure public-key/trusted-CA authentication before exposing a server; do
  not rely on “valid SSH key” as application authorization.
- Apply idle/max timeouts and a rate limiter; rate limiting must cover the auth
  threat model and be ordered deliberately with auth middleware.
- Add OS/application resource limits because Wish does not cap concurrent
  connections automatically.
- Pin v2.0.3 and the underlying `charm.land/ssh` version together during
  upgrades.

## Sources vérifiées

- [Official Wish repository](https://github.com/charmbracelet/wish) — API,
  maintenance, license, checked 2026-08-05.
- [Wish v2.0.3 release](https://github.com/charmbracelet/wish/releases/tag/v2.0.3)
  — exact version and recovery changes, checked 2026-08-05.
- [Wish package documentation](https://pkg.go.dev/charm.land/wish/v2) — API and
  module path, checked 2026-08-05.
- [Recover middleware](https://github.com/charmbracelet/wish/blob/main/recover/recover.go)
  — panic boundary, checked 2026-08-05.
- [Rate limiter middleware](https://github.com/charmbracelet/wish/blob/main/ratelimiter/ratelimiter.go)
  — connection-rate policy, checked 2026-08-05.
- [Access-control middleware](https://github.com/charmbracelet/wish/blob/main/accesscontrol/accesscontrol.go)
  — authorization boundary, checked 2026-08-05.
- [Underlying Charm SSH](https://github.com/charmbracelet/ssh) — server/session
  foundation, checked 2026-08-05.
