---
name: naming
description: "Go naming conventions — short lowercase package names (no util/common), one-to-two-letter receiver names, initialisms kept in conventional casing (ID, URL, HTTP), exported identifiers named for consumers. Use when creating packages, APIs, or any exported surface."
category: rule
tags: [naming, packages, conventions, api, idiomatic-go]
last-verified: 2026-08-06
---

# naming — consistent, meaningful identifiers

## The rule

Choose identifiers the way the Go community does, so readers can predict
meaning from names alone.

1. **Package names** — short, lowercase, one word, meaningful in the context
   of what they contain (the baseline imperative is `rules/core/universal`;
   this rule elaborates it). The package name is the prefix of every exported
   identifier (`bytes.Buffer`), so it must not repeat the package name:
   `buffer.Buffer` is a mistake — name the package for what it contains, not
   for the type it exports. Sources:
   [Go package names](https://go.dev/blog/package-names),
   [Effective Go](https://go.dev/doc/effective_go),
   [Style guideline for Go packages](https://rakyll.org/style-packages/).

2. **Exported vs unexported** — an exported identifier starts with a capital
   letter and is part of the public API: name it for consumers and document
   it (see the `doc-comments` rule). An unexported identifier is an
   implementation detail: lowercase, free to rename. Initialisms keep their
   conventional casing — `ID`, `URL`, `HTTP`, never `Id`, `Url`, `Http`
   (Code Review Comments).

3. **Variables and parameters** — short and contextual: single letters for
   trivial scopes (`i` in a loop), descriptive names for non-obvious values.
   A variable name describes its contents, not its type (`users`, not
   `userSlice`).

4. **Receivers** — one or two letters, used consistently for the same type
   (`s *Store`, `c *Client`); never `this` or `self` (Code Review Comments
   #receiver-name).

5. **Files** — lowercase; `snake_case` for multi-word files
   (`http_client.go`), `_test.go` suffix for tests, and
   `_windows.go`-style suffixes for platform-specific files.

## When to apply

Every new identifier, and every review of exported surface. Naming is the
cheapest part of the API to get right and the hardest to change later: a
renamed exported identifier is a breaking change for consumers.

## Boundary — what this rule does not cover

This rule covers identifier choice, not formatting (gofmt), doc comments
(registry rule `doc-comments`), or the decision of what to export (see
`pattern:go:internal-packages` for hiding internal API). Domain-specific
naming (database columns, wire fields) follows that domain's own
conventions.

## Verification

- Mechanical: `gofmt -l .` and the lint gate (revive conventions) catch
  style regressions; grep import paths for `util|common|misc|helpers` as a
  red flag.
- Review: for every exported identifier, ask "can a reader predict what this
  does from its name alone, in the context of its package?"

## Sources

- [Go package names — Go blog](https://go.dev/blog/package-names)
- [Effective Go — names](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Style guideline for Go packages — rakyll](https://rakyll.org/style-packages/)
