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
