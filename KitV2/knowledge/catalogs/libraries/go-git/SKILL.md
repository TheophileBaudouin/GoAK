---
name: go-git
description: "github.com/go-git/go-git/v5 v5.19.1 — pure-Go Git implementation with repository, plumbing, and porcelain APIs. Use when embedding Git operations without a git binary; not for concurrent access to one repository or v6-alpha API adoption."
category: library
tags: [git, vcs, repository, pure-go, automation]
last-verified: 2026-08-05
---

# go-git — Git pur Go

## Selection

[`github.com/go-git/go-git/v5`](https://github.com/go-git/go-git) v5.19.1,
released 2026-05-18, provides Git plumbing and common repository operations in
pure Go. It is admitted for an embeddable Git boundary with active maintenance,
tests, documentation, and real use, not for popularity. The v6 line remains an
alpha migration target and is not the stable recommendation here.

## Admission checklist

- [x] Current stable v5.19.1; v6 is explicitly pre-release.
- [x] Single responsibility: Git repository and transport operations.
- [x] Pure Go, no git binary required for the supported API.
- [x] Tests, CI, documentation, examples, and regular upstream releases exist.
- [x] The package is inspectable and supports both plumbing and common porcelain.

## Minimal use

```go
func openRepository(path string) (*git.Repository, error) {
    repo, err := git.PlainOpen(path)
    if err != nil {
        return nil, fmt.Errorf("open git repository: %w", err)
    }
    return repo, nil
}
```

Use `PlainClone` or explicit repository/transport APIs when the operation needs
network credentials and a controlled filesystem. Keep repository mutation and
concurrency ownership at the application boundary.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `git2go`/libgit2 | Choose when full Git compatibility justifies a C dependency. |
| `os/exec` with the git CLI | Choose when the host guarantees git and exact CLI behavior is more valuable than pure-Go portability. |
| go-git v6 alpha | Track for migration, but do not use as the stable catalog recommendation until v6 is released. |

## Utiliser cette librairie quand

- A Go service must inspect, clone, fetch, commit, or push repositories without
  spawning a git binary.
- Pure-Go portability and an embeddable repository API matter.
- The application can serialize access to each repository and own credentials.

## Ne pas utiliser cette librairie quand

- Multiple goroutines must mutate or read the same repository concurrently
  without an explicit synchronization design.
- Full porcelain parity or exact compatibility with the system Git client is a
  hard requirement.
- A C dependency is acceptable and libgit2 provides the required operation.
- The project is not prepared to review v6's breaking alpha API.

## Avantages

- Pure-Go repository and transport APIs, no external git process.
- Covers common clone/open/fetch/commit/push operations and lower-level Git
  objects.
- Stable v5 line with active maintenance and a clear v6 migration track.

## Inconvénients

- Not thread-safe for concurrent access to one repository.
- Some Git porcelain and edge behavior differ from the command-line client.
- Authentication, redirects, filesystem isolation, and repository locking need
  explicit application policy.
- v6 changes filesystem bounds and transport APIs before stabilization.

## Pièges connus

- Serialize access to a repository; concurrent reads/writes can corrupt or
  produce inconsistent state.
- Treat HTTP redirects and credentials as a trust boundary; do not silently
  replay credentials across origins.
- Pin v5.19.1 for stable code; v6 alpha APIs are subject to change.
- Use bounded repository paths and review filesystem behavior before accepting
  untrusted repository names.

## Sources vérifiées

- [Official go-git repository](https://github.com/go-git/go-git) — maintenance,
  API, license, checked 2026-08-05.
- [go-git releases](https://github.com/go-git/go-git/releases) — stable v5.19.1
  and v6 alpha status, checked 2026-08-05.
- [go-git documentation](https://go-git.github.io/docs/) — supported operations,
  checked 2026-08-05.
- [v5 to v6 migration guide](https://go-git.github.io/docs/tutorials/migrating-from-v5-to-v6/)
  — breaking filesystem/transport changes, checked 2026-08-05.
- [Issue #773](https://github.com/go-git/go-git/issues/773) — concurrency
  limitation, checked 2026-08-05.
- [Issue #2136](https://github.com/go-git/go-git/issues/2136) — HTTP auth
  redirect behavior, checked 2026-08-05.
