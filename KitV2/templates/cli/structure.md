# CLI — reading map

This map explains how to navigate this project. The **Tree facts** section
below is machine-checked by the kit's drift gate (it cannot drift silently);
the role lines, reading path, and boundary explanations are human-reviewed
content and are not machine-verifiable by design.

## Tree facts (machine-checked; do not edit)

```text
top_dirs: .github; cmd; internal
packages: (root) -> main; cmd -> cmd; internal/parser -> parser; internal/scanner -> scanner; internal/toc -> toc; internal/worker -> worker
entry_points: (root)
test_files: cmd/root_test.go; integration_test.go; internal/parser/markdown_test.go; internal/scanner/gitignore_test.go; internal/scanner/scanner_test.go; internal/toc/generator_test.go; internal/toc/tree_test.go; internal/worker/pool_test.go
internal_boundary: present
```

## Directory roles

- (root) — `main` package: thin process entry point; it only calls `cmd.Execute()`.
- `cmd/` — command wiring: the Cobra command surface, flags, and output handling.
- `internal/` — the implementation: Markdown parsing, file scanning, TOC
  generation, and the worker pool that produces the table of contents.
- `.github/` and other dot-dirs — development tooling; not part of the
  application's reading path.

## Reading path

Run the binary on a directory of Markdown files. The process starts in
`main.go`, which delegates to `cmd/` for argument parsing; `internal/scanner/`
walks the target files (respecting `.gitignore`), `internal/parser/` reads
each Markdown document into headings, `internal/toc/` builds the table of
contents tree, and `internal/worker/` runs the file jobs concurrently before
the result is written back to disk.

## Public vs internal boundary

Everything under `internal/` is private implementation and cannot be imported
by external modules — it is the boundary the Go compiler enforces. The public
surface is the command itself: `main.go` is the entry point, `cmd/` is the
command wiring consumers interact with (flags, help, output). `go-toc` is
consumed as a binary, not as a library.

## Where the evidence lives

The behavior is proven by tests: `cmd/root_test.go` covers the command
surface, `internal/parser/`, `internal/scanner/`, `internal/toc/`, and
`internal/worker/` carry focused unit tests, and `integration_test.go`
exercises the whole binary end to end. Run them with `go test -race ./...`.
