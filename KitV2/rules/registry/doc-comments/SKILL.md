---
name: doc-comments
description: "Go doc-comment conventions — comment immediately preceding the declaration, starting with the symbol's name (or an allowed leading article), with no blank line before it, for every exported identifier. Enforced by revive's exported rule in the lint gate. Use when writing or reviewing exported API surface."
category: rule
tags: [docs, godoc, comments, exported, lint]
last-verified: 2026-08-02
---

# doc-comments — documenting exported identifiers

## The rule

Every **exported** identifier (declared with a capital first letter) must have a
doc comment that:

1. **Immediately precedes** the declaration — no blank line between comment and
   declaration.
2. **Starts with the symbol's name** — optionally after a leading article
   such as "A", "An", or "The" accepted by Go tooling. The identifier should
   remain easy to find in `grep`/godoc/indexing.
3. Says what the identifier **is or does**, not "this is a..." boilerplate.

```go
// Store is a tiny thread-safe in-memory backing store for the example.
type Store struct{ ... }

// NewStore returns an empty Store ready to serve.
func NewStore() *Store { ... }

// Router builds the chi router with a canonical base middleware stack.
func (s *Store) Router() http.Handler { ... }
```

These are the **official Go conventions** (`go/doc`): comments on exported
symbols feed godoc, pkg.go.dev, and IDE hover. Unexported identifiers need no
doc comment.

## Package-level comments

A package comment (immediately above `package foo`) documents the package as a
whole. Required for exported packages when the `package-comments` rule is
enabled. `revive`'s `exported` rule checks exported identifiers; its separate
`package-comments` rule checks the package comment:

```go
// Package restchi shows a minimal idiomatic REST API with the chi router.
package restchi
```

Larger packages may split detailed API docs into a `doc.go` file — same shape,
just its own file. Small packages: one comment above `package`.

## Enforced, not aspirational

This rule is **checked by the lint gate**: `revive`'s `exported` rule runs under
`golangci-lint run ./...` (see `.golangci.yml`). A new exported symbol without a
doc comment fails the gate — so the rule cannot be silently skipped. The doc
style ("what it does", first word = name) is a convention the linter can't
fully judge; follow it for consistency with the recipes.

## Anti-patterns

- `// Store is a struct` — restates the type, says nothing.
- A blank line between the comment and the declaration — breaks the association.
- A comment starting with "This function..." — should start with the name.
- Doc comments on unexported identifiers — noise; godoc ignores them.

## Boundary — what this rule does not cover

- Prose style, spelling, or markup conventions beyond the exported-API
  requirement (first word = name, immediately preceding).
- Which identifiers should be exported in the first place — that is a public
  contract decision, not a doc-comment concern.

## Cross-references

- `recipes/recipe-rest-chi` — a live example of the convention.
- `.golangci.yml` — the `revive` linter enabling `exported`.
- `rules/core/validation/golangci-lint` — how linters are triaged in the gate.
