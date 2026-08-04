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

## Utiliser cette librairie quand

- Construire un serveur SSH en Go avec la couche session/PTY maintenue au
  lieu du plumbing brut x/crypto/ssh.
- `wish` est trop haut niveau (pas besoin du framework d'apps) : ssh
  directement.
- Les événements PTY, window-size et signaux doivent être gérés proprement.

## Ne pas utiliser cette librairie quand

- Le contrôle total du protocole est requis : x/crypto/ssh directement
  (à construire à la main : sessions, PTYs, signaux).
- Le besoin est un serveur SSH applicatif complet (TUI sur SSH, middlewares) :
  `wish` est le niveau au-dessus.

## Avantages

- Successeur maintenu de gliderlabs/ssh (même forme d'API).
- Session/PTY/window-size/signal déjà résolus, contexte par session.
- Usage réel : Wish, Soft Serve, Wishlist.

## Inconvénients

- Serveur seulement : l'authentification, les limites et la politique de
  session restent à configurer explicitement.
- Dépend de x/crypto/ssh (base) — les advisories de sécurité de x/crypto
  s'appliquent (suivre govulncheck).

## Pièges connus

- Authentification explicite : `ssh.PublicKeyAuth` avec allowlist ; jamais de
  password auth sans rate limiting et lockout (voir `source:ssh:server-security`).
- Configurer `MaxTimeout`, `IdleTimeout`, `MaxSessions` par session.
- Clé hôte dédiée via `ssh.HostKeyFile(path)` — une clé par hôte, jamais
  partagée (voir `pattern:antipattern:sec-ssh-host-key-reuse` et `keygen`).

## Sources vérifiées

- [charmbracelet/ssh (repo officiel, v0.4.x)](https://github.com/charmbracelet/ssh)
  — vérifié 2026-08-04
- [pkg.go.dev/github.com/charmbracelet/ssh](https://pkg.go.dev/github.com/charmbracelet/ssh)
  — vérifié 2026-08-04
- Artefacts internes : `source:ssh:server-security`,
  `pattern:antipattern:sec-ssh-host-key-reuse`, catalogs `wish` et `keygen`
