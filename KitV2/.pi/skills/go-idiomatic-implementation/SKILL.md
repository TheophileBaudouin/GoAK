---
name: go-idiomatic-implementation
description: Apply source-backed, idiomatic Go design while writing or refactoring Go code. Use when changing packages, APIs, error handling, concurrency, tests, or project structure; do not use it as a substitute for a task-specific recipe or public-contract approval.
---

# Idiomatic Go implementation

Use this skill after the behavior and scope are understood. It guides choices;
it does not justify changing a public contract without approval.

## Procedure

1. Read the relevant symbols, callers, tests, module metadata, and local rules
   before editing. Trace the real flow and identify the trust boundaries.
2. Start with the smallest existing package and concrete type that can express
   the behavior. Add a package, interface, constructor, or dependency only when
   the current code demonstrates that it earns its cost.
3. Keep normal control flow obvious: handle errors at the right boundary,
   preserve error causes, keep context as the first parameter for cancellable
   I/O, and make every goroutine's exit path explicit.
4. Define interfaces at the consumer boundary when a real seam is needed. Return
   concrete types unless an interface return is part of an existing contract.
5. Keep state ownership explicit. Avoid package-level mutable state, hidden
   singletons, speculative layers, and generic `utils`/`common` packages.
6. Write or update the smallest focused test for the changed behavior, then run
   the focused check before unrelated cleanup.
7. Run the repository's required mechanical gate and report mechanical and
   behavioral evidence separately.

## Boundaries

- Go's official module-layout page is guidance, not a universal tree. Choose
  the layout that follows ownership and the existing repository contract.
- Functional options, dependency injection, generics, worker pools, and extra
  layers are tools, not defaults. Use them only when the concrete problem needs
  them.
- “Clean code” is not a license to rewrite an untouched package or to import a
  Clean Architecture/DDD template from another ecosystem.
- Follow repository-specific test and dependency rules when they are stricter
  than this skill; ask before changing them.

## References

- [Official Go guidance](references/official-go.md)
- [Modern Go boundaries](references/modern-go-boundaries.md)
