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
