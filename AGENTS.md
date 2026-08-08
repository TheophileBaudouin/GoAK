# Go Engineering Kit — metaproject contract

`KIT_CHARTER.md` is the process authority; when an artifact conflicts with it,
the charter wins. This repository develops the standalone `KitV2/` product.
Root `.agent/`, `.pi/memory/`, and `docs/` are metaproject-only. KitV2 is a
compact registry of sourced Go patterns, not a framework.
Every change must reduce decisions, preserve public contracts, and remain
verifiable by observable application behavior as well as code checks.

## Before doing anything

Always check the list of pi-subagents available to you.
To search for files or information in the project, use Scoot.
Pi-subagents are designed to be used together and run in parallel,
allowing you to work faster and maintain a cleaner context.
Always use subagents. You are the orchestrator.
Except for implementations, you are not required.

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

## Absolute rules

You must always check which step of the to-do list you are at and strictly follow this to-do list.
Every task you do, you do by strictly following this to-do list that you created.

## Validation

The Python validators require PyYAML (pinned in
`.agent/validators/requirements.txt`; `python3 -m pip install -r
.agent/validators/requirements.txt` once per environment). From `KitV2/`,
run:

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

## Consumer documentation & onboarding (shipped, never optional)

The consumer kit carries an embedded onboarding/knowledge system — the user
guide `KitV2/.pi/docs/GOAK.md`, the `/goak-help` entry point
(`KitV2/.pi/prompts/goak-help.md`), the onboarding banner
(`KitV2/.pi/extensions/kit-onboarding.ts` + `.pi/onboarding/banner.md`), and
the "User guide" section of `KitV2/AGENTS.md`. These are part of the product:
they ship with every install, must stay usable with no metaproject
documentation, and are verified by `validate-kitv2.py`
`check_consumer_onboarding` plus the `kit audit` dimension C18.

Every change to the consumer kit MUST include the documentation review:
before modifying, identify whether the change affects the guide, `/goak-help`, the
banner, or the audit; during the change, update the affected surface in the
same commit; after the change, verify consistency (code ↔ guide ↔ banner ↔
`/goak-help` ↔ `kit audit`) and run the validator. Never ship a kit change that
documents a command that does not exist, omits a command that exists, or
describes a workflow that no longer matches the tree — the guide is the
shipped source of truth, not an editorial afterthought. A future agent that
modifies the kit must be naturally led to update documentation, banner, and
audits; if a change touches these surfaces and the guide is left untouched,
that is a defect.

## Consumer AGENTS.md writing protocol (D-2026-08-08-19)

- `KitV2/AGENTS.md` is the single agent file for the kit. Any rewrite MUST
  follow Z9 §9: canonical section order, stable MUST/SHOULD/MAY levels, one
  rule per decision, no history, no duplication, ≤ 16 KiB; preserve the
  three marker sections (User guide, Project Foundation, UI work + sha256);
  end with the full gate and a fresh-context review. Enforced by
  `check_agents_md_contract` (validate-kitv2.py).
- Its "UI work" section is a CONDENSED delegation: activation guard, routing
  obligation, cross-cutting invariants only — every other UI instruction
  lives in `ui-kit/AGENTS.md` (single canonical source). The checksum marker
  (`<!-- ui-kit/AGENTS.md sha256: <64-hex> -->`) is the tripwire: at every
  ui-kit re-sync the helper refuses to finish when the marker drifts — the
  section must be re-verified against the new SDK AGENTS.md and the marker
  refreshed before the sync completes (Z13 §4, update-ui-kit prompt). Never
  ship a sync with a stale marker.
- Writing instruction files for this repository follows the
  `agent-instructions` skill: dense, non-redundant, adapted to the kit's
  reality (the ui-kit zone is a pinned mirror, activation is conditional on
  a detected Wails project).
