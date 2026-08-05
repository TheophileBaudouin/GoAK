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

## Enforcement des instructions absolues

Le principe ci-dessus (« Every rule a kit-governance contract states must be
verifiable… ») est étendu aux artefacts consommateurs du Kit (décision
2026-08-05, D-2026-08-05-15) : toute instruction absolue (`MANDATORY`,
« toujours », « jamais ») écrite dans une skill, un prompt, un AGENTS.md ou
une recette doit soit s'accompagner d'un contrôle mécanique nommé (validateur
C2 ou porte Pi), soit être consignée ici comme « guidance seule, non
appliquée ». Ce registre est lu par l'audit (dimension « instructions
absolues », `.pi/prompts/kit-audit.md` phase C9).

| Instruction absolue | Porteur | Contrôle mécanique | Statut (2026-08-05) |
| --- | --- | --- | --- |
| La skill `kit-resource-routing` exige l'appel de `search_kit_resources` « MANDATORY before technical work » (SKILL.md §When to search) | `KitV2/.pi/skills/kit-resource-routing/SKILL.md` | Aucun (outil appelable, non bloquant) | Guidance seule — porte Pi spécifiée (plan 2026-08-05-métaprojet, annexe B), implémentation en passe suivante ; audit C9 vérifie chaque audit |
