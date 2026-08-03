# Go review — `<change>`

## Scope

- Request/plan: `<path>`
- Diff: `<commit, range, or working tree>`
- Reviewer: `<name or agent>`
- Date: `<YYYY-MM-DD>`

## Mechanical evidence

| Check | Command | Result | Evidence |
| --- | --- | --- | --- |
| Format | `test -z "$(gofmt -l .)"` | `PASS/FAIL/BLOCKED` | `<output/path>` |
| Vet | `go vet ./...` | `PASS/FAIL/BLOCKED` | `<output/path>` |
| Focused tests | `<command>` | `PASS/FAIL/BLOCKED` | `<output/path>` |
| Full gate | `<repository command>` | `PASS/FAIL/BLOCKED` | `<output/path>` |

## Findings

### Blocker

- No evidence-backed findings.

### Should fix

- No evidence-backed findings.

### Nit

- No evidence-backed findings.

## Behavioral evidence

- Starting state: `<state>`
- Action: `<command or user action>`
- Observed result: `<output/state>`
- Verdict: `PASS | PARTIAL | FAIL | BLOCKED`

## Final verdict

`PASS | PARTIAL | FAIL | BLOCKED`

Missing evidence or residual risk: `<none or exact next action>`
