---
name: wish
description: "charm.land/wish/v2 — SSH application framework: run Bubble Tea TUIs and other apps over SSH sessions with middleware (logging, ratelimit, prometheus). Use when building a remote/SSH agent workbench or exposing a TUI over SSH."
category: library
tags: [ssh, tui, server, remote, middleware]
last-verified: 2026-08-04
---

# wish — SSH application framework

## Selection

[`charm.land/wish/v2`](https://github.com/charmbracelet/wish) (v2).

**Why it passes the gate** (actual reason, not stars): it turns an SSH server
into an application platform — each session gets a PTY, and your handler can be
anything from a Bubble Tea program to a plain command. Middleware compose
(logging, rate limiting, prometheus, access control). This is the foundation of
the kit's **H-shape architecture** (hybrid local-first / remote workbench): the
same TUI logic runs locally and is reachable over SSH.

## Admission checklist

- [x] Actively maintained — v2.0.x (2026)
- [x] Single responsibility — SSH application framework
- [x] Idiomatic Go — middleware chain over `charm.land/ssh`
- [x] Tests present + CI — yes
- [x] Documentation — README + examples + charm.sh docs
- [x] Real-world usage — Soft Serve, Wishlist, many Charm SSH apps
- [x] Readable end-to-end — yes
- [x] Justified by need — remote agent workbenches need a maintained SSH app layer

## Minimal use

```go
srv, _ := wish.NewServer(
    wish.WithAddress(":2222"),
    wish.WithHostKeyPath("~/.ssh/ed25519_host"),
    wish.WithBubbletea(initialModel()), // serve a Bubble Tea app over SSH
)
log.Fatal(srv.ListenAndServe())
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Raw `charm.land/ssh` | The correct base layer — but you build middleware, session handling, and Bubble Tea wiring yourself. Use wish when you want the app framework. |
| gliderlabs/ssh | Predecessor; less active, no maintained Bubble Tea integration. |
| `golang.org/x/crypto/ssh` directly | Lowest level; fine for one-off servers, verbose for app platforms. |

## Security note

- Generate a dedicated host key; never reuse a client key as host key.
- `wish.WithMiddleware(wish.LogMiddleware())` first, then access control —
  default wish setups allow any client with a valid key, so wire
  `wish.WithPublicKeyAuth` / allowlists before exposing anything.
- Pair with `keygen` (this catalog) for host key generation.

## Utiliser cette librairie quand

- Exposer une TUI Bubble Tea (ou un handler SSH) sur des sessions SSH —
  workbench distant / agent remote.
- La **même logique TUI doit tourner en local ET être accessible par SSH**
  (architecture H-shape du kit).
- Les middlewares (logging, rate limiting, prometheus, contrôle d'accès)
  doivent composer autour des sessions.

## Ne pas utiliser cette librairie quand

- Le serveur SSH est simple/one-off : `charm.land/ssh` (couche session/PTY)
  ou x/crypto/ssh suffisent.
- Seule la couche session/PTY est nécessaire, sans framework d'apps.

## Avantages

- Framework d'apps SSH : session → PTY → handler (Bubble Tea ou commande).
- Middlewares composables (logging, ratelimit, prometheus, access control).
- Fondation de l'architecture H-shape du kit (local-first / remote
  workbench).
- Usage réel : Soft Serve, Wishlist, apps SSH Charm.

## Inconvénients

- Framework opiné : le contrôle fin du protocole passe par les couches
  basses (ssh/x/crypto).
- La sécurité par défaut est permissive : allowlist et middlewares à câbler
  explicitement (defaut = tout client avec une clé valide).

## Pièges connus

- Générer une clé hôte DÉDIÉE, jamais réutiliser une clé client (voir
  `pattern:antipattern:sec-ssh-host-key-reuse` + `keygen`).
- Middlewares dans le bon ordre : log d'abord, puis contrôle d'accès —
  l'auth est traitée AVANT le ratelimiter (issue #325) : un ratelimit ne
  protège pas l'auth par défaut.
- `WithPublicKeyAuth`/allowlists avant d'exposer quoi que ce soit ;
  `WithHostKeyPath` vers une clé persistée.
- Observabilité : `promwish` expose les métriques de session
  (voir `source:wish:ssh-metrics`).

## Sources vérifiées

- [charmbracelet/wish (repo officiel, v2)](https://github.com/charmbracelet/wish)
  — vérifié 2026-08-04
- [charmbracelet/promwish](https://github.com/charmbracelet/promwish) —
  vérifié 2026-08-04
- [Issue #325 — auth avant ratelimiter](https://github.com/charmbracelet/wish/issues/325)
  — vérifié 2026-08-04 (issue officielle)
- Artefacts internes : `source:wish:ssh-metrics`,
  `pattern:antipattern:sec-ssh-host-key-reuse`, catalogs `ssh` et `keygen`
