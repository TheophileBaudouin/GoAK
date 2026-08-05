# Attribution

## Source

- Repository: <https://github.com/sangianpatrick/go-workerpool>
- Pinned release: `v1.0.1`
- Pinned commit: `5d5c611c47489dda3b6e97cd277131d05c814bad`
- License: MIT; the complete upstream `LICENSE` file is retained unchanged.
- Verified: 2026-08-05

## Technical scope

This is a single-purpose, dependency-free Go worker pool with bounded queueing,
context-aware submission, and graceful draining. The pinned source contains 9
Go files and 794 Go lines, including tests, with no vendored source. It does not
include a broker, database, HTTP server, cloud SDK, scheduler, or deployment
stack. Integration belongs to the adopting application through the small
`Handler` interface.

## Adaptations

- Added this attribution file and `template.yaml` for the Kit catalog.
- Replaced the upstream README with a Kit adaptation that explains adoption,
  boundaries, and the executed worker scenario.
- Removed the upstream `_example/` directory because its Kafka example adds an
  unrelated external broker dependency and is outside this focused template's
  scope.
- Added exported API documentation, replaced a nil test context with
  `context.TODO()`, and checked `Submit` errors in tests; these are
  behavior-preserving quality fixes required by the Kit lint gate.
- Removed the upstream `.ai/` project notes because they are agent-session
  material rather than reusable application source.

No worker-pool implementation was authored for the Kit.
