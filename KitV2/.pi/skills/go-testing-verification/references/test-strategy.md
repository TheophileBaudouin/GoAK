# Test strategy

Choose evidence by risk, not by a fixed test-count target.

## Small pure behavior

- Test the exported function or package seam directly.
- Cover normal input and the meaningful invalid/empty/error result.
- Compare complete values or explicit fields; make failures identify the input
  and expected result.

## HTTP and CLI behavior

- Prefer an in-process request or explicit argument boundary when it proves the
  same contract as the user action.
- Check status/exit result, response or stdout/stderr, and durable side effects
  when applicable.
- Keep signal wiring, framework messages, and process startup outside the pure
  decision seam when the repository's recipe provides one.

## Concurrency and cancellation

- Test cancellation and the first meaningful error, not only successful work.
- Run `go test -race ./...` when shared memory or goroutines are involved.
- Confirm every goroutine has a termination path; a passing test that leaks is
  not sufficient.

## Persistence and integrations

- Use the real local driver or an existing test boundary when that is cheaper
  and more truthful than a mock.
- Verify cleanup and error paths, including close/rollback behavior.
- Keep external services out of unit tests unless the acceptance scenario
  explicitly requires an integration environment.

## Sources

- [Go testing package](https://pkg.go.dev/testing)
- [Using subtests and sub-benchmarks](https://go.dev/blog/subtests)
- [Go Test Comments](https://go.dev/wiki/TestComments)
- [Table-driven tests](https://go.dev/wiki/TableDrivenTests)
- [Go fuzzing](https://go.dev/doc/security/fuzz/)
