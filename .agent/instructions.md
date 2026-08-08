# Metaproject agent instructions

This root directory is the Go Agent Development Kit metaproject. It contains
the constitution, durable memory, research, decisions, and validation methods
used to evolve the standalone consumable `KitV2/` product.

## Ownership

- `AGENTS.md` and `KIT_CHARTER.md` are process authority.
- `.pi/memory/` is the only authoritative metaproject memory.
- `.agent/` contains metaproject-only control-plane artifacts.
- `.agent/kit-governance/` holds the **construction contracts** for KitV2:
  read the contract of a zone (`C0`, `C1`, `C2`, `Z1`–`Z10`, `A1`, `N1` —
  see `.agent/kit-governance/README.md`) **before** working in that zone.
- `KitV2/` is the only consumable product; it must not receive this
  metaproject's history, decisions, or evaluation governance.

## Required behavior

Read `.pi/memory/` before work. For non-trivial changes, research first,
create a plan, use one writer, obtain fresh-context review, run deterministic
checks, and record raw evidence under `docs/evidence/`. Never delete product
content before the approved archive/checkpoint plan passes, and never claim
completion from static checks alone. Every rule a kit-governance contract
states must be verifiable by the product validator (`validate-kitv2.py`) or an
explicit review control; unverifiable rules are hypotheses, not contracts.

## Enforcement of absolute instructions

The principle above ("Every rule a kit-governance contract states must be
verifiable…") is extended to the Kit's consumer artifacts (decision 2026-08-05,
D-2026-08-05-15): any absolute instruction (`MANDATORY`, "always", "never")
written in a skill, prompt, AGENTS.md, or recipe must either be accompanied by
a named mechanical control (validator C2 or Pi gate), or be recorded here as
"guidance only, not enforced". This registry is read by the audit (dimension
"absolute instructions", `.pi/prompts/kit-audit.md` phase C9).

| Absolute instruction | Carrier | Mechanical control | Status (2026-08-05) |
| --- | --- | --- | --- |
| The `kit-resource-routing` skill requires calling `search_kit_resources` "MANDATORY before technical work" (SKILL.md §When to search) | `KitV2/.pi/skills/kit-resource-routing/SKILL.md` | None (callable tool, non-blocking) | Guidance only — Pi gate specified (plan 2026-08-05-metaproject, annexe B), implementation next pass; audit C9 verifies each audit |
| "Read and follow `references/behavioral-rules.md` in every phase" (MUST); "Do NOT restart from Phase 0 when `docs/progress/MASTER.md` exists" (NEVER); "Phase 6 archive always executed" | `KitV2/.pi/skills/spec-driven-dev/SKILL.md` | None (process workflow) | Guidance only — workflow-level discipline, no mechanical gate; recorded 2026-08-06 (KVA-106) |
| "Never write before the user's explicit validation"; "Never re-run over an existing `workspace/` without an explicit revision request"; "Never lose existing `AGENTS.md` content" | `KitV2/.pi/skills/workspace-init/SKILL.md` | None (day-0 workflow; idempotence is a skill-level check) | Guidance only — workflow-level discipline, no mechanical gate; recorded 2026-08-08 (Z14) |
| "NEVER put secrets in `.pi/settings.json`"; "never assume the standard memory set exists — verify which `.pi/memory/` files are present" | `KitV2/.pi/prompts/workflow-memory.md` (memory rule also in `KitV2/AGENTS.md`) | None (consumer-project convention) | Guidance only — encoded as durable text; recorded 2026-08-06 (KVA-106) |
| "Present findings before any summary; never bury a bug under a summary" | `KitV2/.pi/skills/go-code-review/SKILL.md` (§4) | None (review discipline) | Guidance only — findings-first review protocol; recorded 2026-08-06 (KVA-106) |
| "Never claim an unexecuted scenario passed or treat static checks as proof of user intent"; "Always preserve errors, cancellation, input validation, and observable evidence"; "Ask before adding dependencies or changing the manifest contract" | `KitV2/AGENTS.md` (§Limits) | None (product guardrails; kit-audit C6/C15 review control) | Guidance only — review control, no mechanical gate; recorded 2026-08-06 (charter §16.1.4) |
| "**Routing is mandatory, not optional.**" — call `search_kit_resources` before planning or implementing technical work (§Workflow) | `KitV2/AGENTS.md` (§Workflow) | None (callable tool, non-blocking; routing-quality gate enforces the index, not the agent behavior) | Guidance only — Pi gate specified (plan 2026-08-05-metaproject, annexe B), implementation next pass; recorded 2026-08-06 (KVA-103) |
| Tool `promptGuidelines`: "call search_kit_resources … this is mandatory, not optional" | `KitV2/.pi/extensions/kit-resource-router.ts` (promptGuidelines) | None (tool guidance rendered to the agent) | Guidance only — same Pi gate as the AGENTS.md routing mandate; recorded 2026-08-06 (KVA-103) |
| Tool `promptGuidelines`: "call search_ui_kit_resources … this is mandatory, not optional" (UI tasks in Wails projects) | `KitV2/.pi/extensions/kit-ui-router.ts` (promptGuidelines) | None (tool guidance rendered to the agent) | Guidance only — same Pi gate as the routing mandate; the UI ranking itself is gate-enforced (run_ui_scenarios.mjs, Z13); recorded 2026-08-07 (ui-agent-kit integration) |
| Rule bodies ("always wrap with `%w`", "never log the same error twice", …) | `KitV2/rules/**` | Named control: golangci-lint (staticcheck/errcheck) + Z1 "Verification" section + review | Rule-content boundary (Z1 semantic elements), NOT a process absolute — interpretation decision 2026-08-06 (KVA-106): only skills/prompts/AGENTS.md/recipe process instructions enter this registry; rule boundaries carry their own verification path |

## Interpretation note (2026-08-06, KVA-106)

The audit inventoried 31 consumer surfaces carrying `MANDATORY`/`MUST`/
`ALWAYS`/`NEVER` lexemes. Decided: **rule-content boundaries** (a rule stating
what generated code must never do, with its own Z1 `Verification` section) are
not "absolute instructions" for this registry; only **process instructions**
carried by skills/prompts/AGENTS.md/recipes that tell the agent how to behave
are recorded above. The planned deterministic C2 lexeme check (annexe C) will
still be scoped to the process-instruction set, not to rule bodies.
