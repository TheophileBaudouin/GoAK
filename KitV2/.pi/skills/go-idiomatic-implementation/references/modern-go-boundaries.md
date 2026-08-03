# Modern boundaries and decisions

Use current package documentation and release notes to verify version-specific
behavior. These are decision prompts, not unconditional rules.

## Package and API boundaries

- Prefer a concrete type until a consumer needs substitutability.
- Define the smallest interface where it is consumed; do not add an interface
  only to make a mock possible.
- Keep packages named after the domain they own. A flat package or one clear
  domain package is preferable to layers named `controller`, `service`, and
  `repository` when those layers add no ownership clarity.
- Keep exported APIs small and document compatibility consequences before
  changing them.

## Errors and cancellation

For the universal context, error, and interface rules, load the canonical
`universal` rule. This reference adds only the following implementation
boundaries:

- Prefer synchronous code when the caller does not need concurrency.
- Do not start a goroutine without a clear termination path.

## Concurrency and performance

- Prefer synchronous code when the caller does not need concurrency.
- For bounded concurrent work, use an existing repository recipe or the
  standard/approved concurrency primitive rather than a custom pool.
- Measure before adding pooling, caching, allocation tricks, or generics for
  abstraction alone.

## Sources

- [Go errors are values](https://go.dev/blog/errors-are-values)
- [Working with errors in Go 1.13](https://go.dev/blog/go1.13-errors)
- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go release notes](https://go.dev/doc/devel/release)
- [Google Go Style Guide](https://google.github.io/styleguide/go/)
