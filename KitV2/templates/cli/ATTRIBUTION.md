# Attribution

## Source

- Repository: <https://github.com/danjdewhurst/go-toc>
- Pinned release: `v0.3.0`
- Pinned commit: `1f93495652ca789a75251f3cd6028b8f3adfc624`
- License: MIT; the complete upstream `LICENSE` file is retained unchanged.
- Verified: 2026-08-05

## Technical scope

This is a real, single-purpose Go CLI that generates Markdown table of
contents files. Its structure is a small `cmd/` entry point plus focused
`internal/` packages for parsing, scanning, rendering, and worker coordination.
The pinned source contains 16 Go files and 3,975 Go lines, with tests and CI.
Its only direct runtime dependencies are Cobra and go-gitignore; it does not
include a database, server, cloud SDK, auth system, or deployment stack.

## Adaptations

- Added this attribution file and `template.yaml` for the Kit catalog.
- Kept the upstream source tree, CI configuration, release configuration,
  and MIT license unchanged.
- Replaced the upstream README with a Kit adaptation that explains adoption,
  boundaries, and the executed smoke scenario.
- Added explicit handling for CLI output and temporary-directory cleanup errors
  in the copied command and tests; these are behavior-preserving quality fixes
  required by the Kit lint gate.
- Simplified one parser branch with a tagged switch, corrected one exported
  documentation comment, and added scoped Pi-lens suppressions for deliberate
  error propagation. These changes preserve upstream behavior and keep the
  template clean under the Kit diagnostics.
- The upstream module path remains in `go.mod` so the copied tree can be
  validated without rewriting imports. When adopting it, replace the module
  path and run `go mod tidy`.

No CLI behavior was authored for the Kit.
