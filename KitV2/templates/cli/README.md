# Go CLI template

Status: **sourced**.

This directory is a minimally adapted copy of
[`danjdewhurst/go-toc`](https://github.com/danjdewhurst/go-toc), pinned to
release `v0.3.0` at commit `1f93495652ca789a75251f3cd6028b8f3adfc624`. Read
[`ATTRIBUTION.md`](./ATTRIBUTION.md) before adapting it. The upstream MIT license
is retained in [`LICENSE`](LICENSE).

## What it provides

A real command-line application that generates Markdown table-of-contents
files. It demonstrates a small `cmd/` entry point, focused `internal/` packages,
fixture-driven tests, integration coverage, and a conventional Cobra command
surface. It is useful as a CLI base when the application has a file-oriented
command and needs a tested package boundary.

## Adopt it

1. Change the module path in `go.mod` and imports from
   `github.com/danjdewhurst/go-toc` to your module path.
2. Rename the command and replace the TOC domain packages with the application's
   focused use case; keep `cmd/` as wiring and `internal/` as implementation.
3. Keep Cobra only if the application needs subcommands, generated help, or
   completion; otherwise replace the command boundary with `flag`.
4. Update release configuration and CI to match the deployment target.
5. Run the checks below and retain tests for success, invalid input, and process
   exit behavior.

## Verify

```sh
go test -race ./...
go vet ./...
go run . --help
go run . .
```

The observable scenario is a CLI invocation against a directory containing
Markdown files and a generated table of contents. Do not add a server, database,
authentication system, or cloud integration unless the application explicitly
requires it.
