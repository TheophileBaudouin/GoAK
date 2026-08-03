# Review checklist

Use only the sections relevant to the change. A checked box without evidence is
not a verdict.

## Contract and scope

- [ ] The diff implements the approved behavior and no unapproved public or
      schema change.
- [ ] Callers, error behavior, compatibility, and migration effects are known.
- [ ] New dependencies and configuration have an explicit decision and source.

## Correctness and failures

- [ ] Trust-boundary inputs are bounded and validated.
- [ ] Errors are handled once at the right boundary and wrapped when context is
      added; causes remain inspectable.
- [ ] Cancellation reaches I/O and long-running work.
- [ ] Resources close with errors handled.
- [ ] Goroutines have an observable exit path and shared state is safe.

## Go quality

- [ ] Names, package ownership, receiver choices, comments, and formatting fit
      Go conventions and the repository's local rules.
- [ ] Interfaces are consumer-owned and no abstraction exists only for habit.
- [ ] The design does not import a generic layered architecture without a
      demonstrated ownership or compatibility need.

## Tests and evidence

- [ ] Focused success and meaningful failure behavior are covered.
- [ ] Race-sensitive code has a race check where relevant.
- [ ] The full mechanical gate was run or its first failure is recorded.
- [ ] The user-observable scenario was run, with output/state recorded.
- [ ] Missing evidence is `PARTIAL` or `BLOCKED`, never silently `PASS`.

## Sources

- [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
- [Go Test Comments](https://go.dev/wiki/TestComments)
- [Go doc comments](https://go.dev/doc/comment)
- [Go module layout](https://go.dev/doc/modules/layout)
