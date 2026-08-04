---
name: go-git
description: "github.com/go-git/go-git v5.19 — pure-Go Git implementation (clone, fetch, commit, branch, diff, log) with no external git binary. Use when a Go service must read or write Git repositories programmatically (repo analysis, agent commits, CI tooling) and you want zero runtime dependency on the git CLI."
category: library
tags: [git, vcs, repository, pure-go, diff, clone]
last-verified: 2026-08-04
---

# go-git — pure-Go Git

## Selection

[`github.com/go-git/go-git/v5`](https://github.com/go-git/go-git) (v5.19.2,
Go 1.21+, Apache-2.0, ~7.6k★, pushed 2026-08-03).

**Why it passes the gate** (actual reason, not stars): a pure-Go reimplementation
of Git's object model and transport (clone, fetch, push, commit, branch,
diff, log, worktree) that needs **no `git` binary** at runtime — the reason it
is used by Gitea, Pulumi, and Keybase. Single responsibility (Git
manipulation), idiomatic Go, extensive tests, active maintenance (v5.19.x
2026, v6 alpha in progress).

## Admission checklist

- [x] Actively maintained — v5.19.2 (2026), v6 alpha active
- [x] Single responsibility — Git object model + transport
- [x] Idiomatic Go — clean public API, `git.PlainClone` style entry points
- [x] Tests present + CI — yes
- [x] Documentation — README + pkg.go.dev + examples
- [x] Real-world usage — Gitea, Pulumi, Keybase
- [x] Readable end-to-end — yes, layered (storage/transport/plumbing)
- [x] Justified by need — agent tools need repo ops without a git binary

## Minimal use

```go
repo, err := git.PlainClone("/tmp/repo", false, &git.CloneOptions{
    URL:      "https://github.com/go-git/go-git",
    Progress: os.Stdout,
})
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Shell out to `git` | Runtime dependency + parsing fragility; go-git is deterministic. |
| `git2go` (libgit2) | CGO dependency; go-git is pure Go. |

## Notes

- `v6` is in alpha (transport/performance rework) — pin `v5` for stability.
- Issue-mined (856 issues): top themes are missing features (sparse
  checkout #90, signed commits #400, credentials #490) — go-git covers the
  core operations well; verify edge-case coverage before relying on advanced
  Git features.
- Preferred pairing: go-git for repo **read/write** in-process; keep
  `git` CLI only when signing or exotic plumbing is required.

## Utiliser cette librairie quand

- Un service Go doit lire/écrire des dépôts Git programmatiquement
  (analyse de repos, commits d'agent, outillage CI) sans dépendance runtime
  au binaire `git`.
- Le clone/fetch/commit/branch/diff/log couvre le besoin (opérations cœur).
- L'environnement interdit ou n'a pas de binaire git (conteneurs minimaux,
  services embarqués).

## Ne pas utiliser cette librairie quand

- La signature de commits, les features exotiques ou le plumbing avancé sont
  requis : garder le CLI `git` (signing #400, credentials #490, sparse
  checkout #90 non couverts).
- Le binaire `git` est disponible et le besoin est simple : shell-out reste
  plus simple (avec parsing à risque).
- Le zéro-CGO est une contrainte absolue et git2go était envisagé : go-git
  est pur-Go (le bon choix dans ce cas).

## Avantages

- Pur-Go : zéro binaire git requis au runtime, déterministe.
- Opérations cœur complètes (clone, fetch, push, commit, branch, diff, log,
  worktree).
- Usage réel : Gitea, Pulumi, Keybase.
- Maintenance active (v5.19.x 2026, v6 alpha en cours).

## Inconvénients

- Fonctionnalités avancées manquantes ou partielles (sparse checkout #90,
  signed commits #400, credentials #490) — 856 issues ouvertes, majorité de
  demandes de features.
- v6 (transport/performance) en alpha : le code sur v5 devra migrer.
- Performances historiquement moindres que git natif sur les gros dépôts
  (rework attendu en v6).

## Pièges connus

- Pinner `v5` : v6 est en alpha (rework transport/performance), pas pour la
  production.
- Vérifier la couverture des cas limites AVANT de s'appuyer sur une feature
  avancée (issue-mining : sparse checkout, signatures, credentials).
- Pour la signature ou le plumbing exotique, garder le CLI `git` — go-git ne
  le remplace pas.

## Sources vérifiées

- [go-git/go-git (repo officiel, v5.19.2)](https://github.com/go-git/go-git)
  — vérifié 2026-08-04
- [pkg.go.dev/github.com/go-git/go-git/v5](https://pkg.go.dev/github.com/go-git/go-git/v5)
  — vérifié 2026-08-04
- [Issue #90 — sparse checkout](https://github.com/go-git/go-git/issues/90) /
  [#400 — signed commits](https://github.com/go-git/go-git/issues/400) /
  [#490 — credentials](https://github.com/go-git/go-git/issues/490) —
  vérifiées 2026-08-04 (issues officielles)
