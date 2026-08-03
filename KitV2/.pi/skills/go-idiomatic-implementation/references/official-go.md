# Official Go foundations

Use these sources for general language and API decisions. They are guidance,
not a replacement for the consumer project's contract.

- [Effective Go](https://go.dev/doc/effective_go) — formatting, naming,
  package design, interfaces, errors, and concurrency. The page itself notes
  that it predates modules, generics, and newer libraries; supplement it when
  those topics matter.
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) — review
  guidance for error flow, contexts, goroutine lifetimes, interfaces, naming,
  receivers, documentation, and panic use.
- [Go module layout](https://go.dev/doc/modules/layout) — project-layout
  guidance organized by project shape; it does not prescribe one universal
  repository tree.
- [Go doc comments](https://go.dev/doc/comment) — current documentation rules
  for exported APIs and package comments.
- [Go package names](https://go.dev/blog/package-names) — short, clear package
  names and avoidance of generic catch-all packages.

## Use the sources correctly

- Cite the source for claims that affect the design.
- Prefer the repository's observed ownership and tests over a copied tree.
- If two sources are scoped differently, state the scope instead of presenting
  one as a universal law.
