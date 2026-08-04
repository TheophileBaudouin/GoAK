---
name: ssh
description: "charm.land/ssh — high-level SSH server API for Go (sessions, PTY, signal) built on golang.org/x/crypto/ssh. Use when building an SSH server in Go and you want the maintained session/PTY layer instead of raw x/crypto/ssh plumbing."
category: library
tags: [ssh, server, pty, sessions, remote]
last-verified: 2026-08-04
---

# ssh — SSH server API for Go

## Selection

[`charm.land/ssh`](https://github.com/charmbracelet/ssh) (Go 1.22+).

**Why it passes the gate** (actual reason, not stars): it is the maintained
successor of `gliderlabs/ssh`, adding what raw `golang.org/x/crypto/ssh` makes
you build by hand: session handling, PTY allocation, window-size and signal
events, and context-per-session. `wish` (same catalog) builds its app framework
on top of it; use `ssh` directly when you want the server without the app layer.

## Admission checklist

- [x] Actively maintained — v0.4.x, active (2026)
- [x] Single responsibility — SSH server session/PTY layer
- [x] Idiomatic Go — `Handler func(session ssh.Session)` over x/crypto
- [x] Tests present + CI — yes
- [x] Documentation — README + examples
- [x] Real-world usage — Wish, Soft Serve, Wishlist
- [x] Readable end-to-end — yes
- [x] Justified by need — the PTY/session layer is the hard part of SSH servers

## Minimal use

```go
srv := &ssh.Server{
    Addr: ":2222",
    Handler: func(s ssh.Session) {
        io.WriteString(s, "hello\n")
        s.Exit(0)
    },
}
log.Fatal(srv.ListenAndServe())
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang.org/x/crypto/ssh` | Correct low-level base; you hand-build sessions, PTYs, and signals. Choose it only for full control. |
| gliderlabs/ssh | The predecessor — this project is its maintained fork. |
| sshserver / meldium wrappers | Smaller, less proven. |

## Security note

- Handle authentication explicitly: `ssh.PublicKeyAuth` with an allowlist; do not
  enable password auth without rate limiting and lockout.
- Configure `MaxTimeout`, `IdleTimeout`, and per-session `MaxSessions`.
- Host keys: `ssh.HostKeyFile(path)` from a dedicated key (see `keygen`).
