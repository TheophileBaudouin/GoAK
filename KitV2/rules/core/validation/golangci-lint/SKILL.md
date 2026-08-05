---
name: golangci-lint
description: "golangci-lint — the meta-linter aggregating go vet, staticcheck, errcheck and ~30 others in one run. The kit's mandatory validation gate. Use when configuring linting, choosing which linters to enable, or triaging false positives."
category: rule
tags: [validation, lint, golangci-lint, ci]
last-verified: 2026-08-02
---

# golangci-lint — the kit's meta-linter

## Role in the kit

`golangci-lint` (golangci-lint/golangci-lint, ~19k★, actively maintained, v2) is
one of the **mandatory validation tools**: every code example in the registry
must pass `golangci-lint run` with zero issues before its module is marked done.
It aggregates many linters behind a single configurable run; with
`linters.default: none` only the linters explicitly enabled in `KitV2/.golangci.yml`
execute — nothing runs by accident.

## Kit config (canonical)

`KitV2/.golangci.yml` is the source of truth for the gate: this document describes
the config actually shipped, and any gate change must land in the config first.
v2 changed the config schema and invocation vs v1 — do not copy v1 configs
blindly.

```yaml
# .golangci.yml — v2, opt-in. Only add linters you can justify.
version: "2"
linters:
  default: none        # opt-in, not opt-out — keeps the gate intentional
  enable:
    - errcheck         # unchecked error returns (catches real bugs)
    - govet            # go vet correctness checks
    - staticcheck      # SA* checks
    - unused           # unused code
    - ineffassign      # ineffectual assignments
    - revive           # only the `exported` rule below
  settings:
    revive:
      rules:
        - name: exported  # every exported identifier needs a doc comment
formatters:
  enable:
    - gofmt
    - goimports
```

`gofmt`/`goimports` run as formatters: they report violations; the repo applies
fixes through its explicit `gofmt -l` output gate, not silently.

## Linters: enable deliberately, not by default

| Linter | Why |
| --- | --- |
| `errcheck` | Catches unchecked error returns — keep ON. (Bare `.Close()` is the classic miss.) |
| `govet` / `staticcheck` | Core correctness. Keep ON. |
| `unused` / `ineffassign` | Dead code and ineffectual assignments — cheap signal, no style opinion. |
| `revive` (`exported` rule only) | Doc comments on the exported API surface; no stylistic rules enabled. |
| `gosec` | Security — deliberately NOT enabled inside golangci-lint: the kit already runs `gosec` as a standalone gate tool, so it would be redundant here. |
| `gocyclo` / `funlen` / `lll` | Style/complexity. Opinionated — enable only with a stated threshold, else noise. |

## Handling false positives

1. Prefer fixing the code over silencing.
2. If a genuine false positive: use a directive, not a blanket disable.

   ```go
   //nolint:errcheck // best-effort close on a drained cursor; error has no recovery path
   _ = rows.Close()
   ```

   Always state the reason inline — a `//nosec`/`//nolint` without justification is a smell.

## Gotchas

- v2 config differs from v1 (`version: "2"`, `linters.default` semantics). A v1
  config silently misbehaves.
- Runs against test files too — `_ = ln.Close()` in tests must be explicit.
- First run downloads linters; CI should cache `~/.cache/golangci-lint`.

## Boundary — what this rule does not cover

- The standalone security scanners `gosec` and `govulncheck` (separate core
  gate rules); golangci-lint's built-in gosec is deliberately not enabled here.
- Style/complexity linters (`gocyclo`, `funlen`, `lll`) — opinionated, enabled
  only with a stated threshold.
