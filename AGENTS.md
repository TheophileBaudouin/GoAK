# Go Engineering Kit — metaproject contract

`KIT_CHARTER.md` is the process authority; when an artifact conflicts with it,
the charter wins. This repository develops the standalone `KitV2/` product.
Root `.agent/`, `.pi/memory/`, and `docs/` are metaproject-only. KitV2 is a
compact registry of sourced Go patterns, not a framework.
Every change must reduce decisions, preserve public contracts, and remain
verifiable by observable application behavior as well as code checks.

## Decision order

1. Smallest solution that satisfies the requested behavior.
2. Existing kit recipe or interface.
3. Standard library or platform capability.
4. Existing vetted dependency.
5. New dependency or abstraction only with evidence and approval.

## Evidence rules

- Every rule added to `KitV2/rules/` or `KitV2/knowledge/` cites a primary,
verifiable source. Consult `.agent/sources/Go-dev-kit-sources-et-references.md`
first; its ordering and priorities are strict, while `KIT_CHARTER.md` and kit
rules remain higher authority.
  Unsupported ideas are hypotheses, not doctrine.
- `golang-standards/project-layout` is not Go authority. Go does not prescribe a
  universal project tree; use official package naming guidance and Go Proverbs.
- Use Go-native design: small consumer-owned interfaces, concrete returns, and
  explicit errors. Do not import broad OOP/Clean Code/GoF doctrine as default.
- Tests, lint, coverage, `gosec`, and `govulncheck` prove mechanical properties,
  not user intent. Recipes require a runnable, user-observable scenario.
- Document confidence honestly: recipe-covered shapes have higher confidence;
  outside recipes the kit provides generic guidance only.

## Work protocol

For non-trivial work, create a todo list before editing. Research first, then
write a short plan in `docs/plans/`, keep one writer per worktree, and use a
fresh read-only review before declaring completion. Use Goal / Context /
Constraints / Done when framing. Persist durable decisions and blockers in
`.pi/memory/`.

### Instruction-artifact protocol

For changes to `AGENTS.md`, skills, prompts, workflows, checklists, templates,
or equivalent instructions, follow `KIT_CHARTER.md` §6: research recognized
references first, adapt the smallest surface, and obtain a fresh-context review
before completion. Never start from a blank page when a satisfactory reference
exists. Keep permanent context compact; use skills, scripts, and CI for detail
and deterministic gates. The charter is the complete protocol and source of
truth; this section is only its pointer and non-negotiable summary.

## Modification policy

Implement documentation, tests, recipes, and non-structural fixes freely. Ask
before changing `KitV2/rules/core/`, adding a dependency or category, changing a published
frontmatter contract, adding a reference project, or changing adapter output.
Never bypass this approval boundary by silently expanding scope.

## Validation

From `KitV2/`, run:

```sh
export PATH="$PATH:$(go env GOPATH)/bin"
python3 ../.agent/validators/validate-instructions.py
python3 ../.agent/validators/validate-cognitive.py
go mod tidy && go mod verify && test -z "$(gofmt -l .)" && go vet ./... && golangci-lint run ./... && go test -race ./... && gosec ./... && govulncheck ./...
```

A module is done only when its relevant checks pass, its sources are recorded,
and its behavior scenario is actually run or explicitly marked `PARTIAL`/
`BLOCKED`. Three identical failures means stop and report; do not loop.

## Memory

Root `.pi/memory/` is metaproject memory. `KitV2/.pi/` ships reusable
settings, prompts, and skills only; no consumer memory is shipped. Consumer
projects initialize their own `.pi/memory/`. Never mix metaproject memory with
consumer memory.
