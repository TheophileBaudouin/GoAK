---
name: ssh
description: "charm.land/ssh v0.4.2 — high-level Go SSH server with sessions, PTY, signals, and net.Listener lifecycle over x/crypto/ssh. Use for SSH servers; not for SSH clients, raw protocol control, or an application framework."
category: library
tags: [ssh, server, pty, sessions, remote]
last-verified: 2026-08-05
---

# ssh — Go SSH server API

## Selection

[`charm.land/ssh`](https://github.com/charmbracelet/ssh) v0.4.2,
released 2026-07-31, is a maintained SSH **server** layer over
`golang.org/x/crypto/ssh`. It provides session, PTY, signal, host-key, and
listener lifecycle helpers without imposing Wish's application framework. It is
admitted for this narrow server boundary, active maintenance, tests, and use in
Wish/Soft Serve; not for popularity.

## Admission checklist

- [x] Current v0.4.2 and Go 1.25+.
- [x] Single responsibility: SSH server sessions and PTY integration.
- [x] `net.Listener`/handler lifecycle over x/crypto/ssh.
- [x] Tests, CI, documentation, and production ecosystem use exist.
- [x] Security hardening and canonical `charm.land/ssh` import are documented.

## Minimal use

```go
func server() *ssh.Server {
    return &ssh.Server{
        Addr: ":2222",
        Handler: func(session ssh.Session) {
            _, _ = io.WriteString(session, "hello\n") // connection may close before a response is written
            _ = session.Exit(0)
        },
    }
}
```

Use `Serve` with an explicitly owned listener and handle its returned error at
the process boundary. Provide a stable host key; automatic generation is not a
production identity policy.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang.org/x/crypto/ssh` | Choose for low-level client/server protocol control when the application will own session/PTY plumbing. |
| Wish | Choose for an SSH application framework with middleware and command/TUI composition. |
| gliderlabs/ssh | Predecessor/superseded boundary; verify before retaining in existing code. |
| SSH client | Use `x/crypto/ssh` client APIs; this package is server-only. |

## When to use this library
- A Go application needs an SSH server with sessions, PTY allocation, window
  size, signals, and an explicit handler.
- Wish is too high-level but raw x/crypto/ssh would duplicate session plumbing.
- Host keys, authentication, timeout, and connection lifecycle can be configured
  as explicit server policy.

## When NOT to use this library
- The application is an SSH client.
- Full protocol control or custom transport semantics are required.
- A complete SSH application framework is desired; use Wish or compose one.
- Host key persistence, authentication, and session limits cannot be managed.

## Advantages
- High-level session/PTY API with the standard SSH cryptographic base.
- Current Charm import path and active patch releases.
- Hooks for authentication, connection lifecycle, PTY, proxy protocol, and
  panic recovery per connection.

## Disadvantages
- Server-only; auth policy, host keys, limits, and application authorization
  remain the consumer's responsibility.
- Depends on x/crypto/ssh and its security lifecycle.
- PTY/signal behavior varies by platform and terminal client.

## Known pitfalls
- Use `charm.land/ssh`; the old GitHub import is a migration boundary.
- Configure public-key authentication with an allowlist; do not enable password
  auth without rate limiting, lockout, and audit policy.
- Set handshake/session/idle timeouts and maximum sessions explicitly.
- Persist a dedicated host key; never regenerate it per process or reuse a key
  across unrelated hosts.
- Keep writes and `Exit` errors at the session boundary; never hide auth or
  protocol failures in application code.

## Verified sources
- [Official Charm SSH repository](https://github.com/charmbracelet/ssh) — API,
  maintenance, license, checked 2026-08-05.
- [SSH v0.4.2 release](https://github.com/charmbracelet/ssh/releases/tag/v0.4.2)
  — exact version and panic recovery, checked 2026-08-05.
- [charm.land/ssh on pkg.go.dev](https://pkg.go.dev/charm.land/ssh) — API,
  server-only boundary, checked 2026-08-05.
- [v0.4.0 security hardening](https://github.com/charmbracelet/ssh/releases/tag/v0.4.0)
  — import/security/permissions changes, checked 2026-08-05.
- [Cross-account advisory](https://github.com/charmbracelet/ssh/security/advisories/GHSA-v386-2qpp-hrr3)
  — authentication boundary and fixed version, checked 2026-08-05.
- [x/crypto/ssh package](https://pkg.go.dev/golang.org/x/crypto/ssh) — underlying
  protocol/client base, checked 2026-08-05.
