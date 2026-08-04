---
name: universal
description: "Universal, sourced Go rules for package naming, contexts, errors, interfaces, documentation, and observable examples. Load for every Go implementation."
category: rule
tags: [universal, idiomatic-go, context, errors, interfaces]
last-verified: 2026-08-02
---

# universal — the small set that applies everywhere

- Name packages with short, clear, lower-case words; avoid meaningless names
  such as `util`, `common`, `api`, and `types`. Source:
  [Go package names](https://go.dev/blog/package-names).
- Pass `context.Context` explicitly, normally as the first parameter, through
  request-scoped work. Do not store it in a struct. Source:
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#contexts).
- Return errors as values, handle them, and preserve useful causes with `%w` when
  adding context. Source:
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#handle-errors) and
  [Go Proverbs](https://go-proverbs.github.io/).
- Define interfaces where they are consumed, only when a real consumer needs
  substitution. Return concrete implementations instead of an interface merely
  for mocking. Source:
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#interfaces) and
  [Go Proverbs](https://go-proverbs.github.io/).
- Add doc comments to exported declarations and runnable examples for public
  usage. Source:
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#doc-comments) and
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#examples).
- Keep normal control flow shallow: handle errors early, then continue with the
  successful path. Source:
  [Code Review Comments](https://go.dev/wiki/CodeReviewComments#indent-error-flow).

These are defaults, not substitutes for understanding the user's requested
behavior. A concrete recipe may add constraints, but must cite its own sources.
