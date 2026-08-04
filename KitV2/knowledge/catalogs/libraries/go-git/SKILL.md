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
