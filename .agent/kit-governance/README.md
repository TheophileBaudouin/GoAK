# Kit Governance — Kit construction contracts (Metaproject)

This directory is the **governance control plane** of the `KitV2/` product. Each
contract defines the mission, format, rules, patterns, anti-patterns, and
validation criteria of a zone or kit component. An agent or developer must
read the zone contract **before** working there.

Authority: `KIT_CHARTER.md` (root) > these contracts > kit zone README >
content. These files are **never** installed in the product; the product stays
self-contained (Z9, N1).

## Index

| Contract | Scope | Status |
| --- | --- | --- |
| [00-charte-d-application.md](00-charte-d-application.md) | Lifecycle, semver, write-gate, freshness, cross-cutting rules (C0) | active |
| [01-manifest-capabilities.md](01-manifest-capabilities.md) | manifest.yaml + capabilities.yaml (C1) | active |
| [02-validation-gate.md](02-validation-gate.md) | validate-kitv2.py and the full gate (C2) | active |
| [10-zone-rules.md](10-zone-rules.md) | `rules/` (Z1) | active |
| [11-zone-knowledge.md](11-zone-knowledge.md) | `knowledge/` (Z2) | active |
| [12-zone-recipes.md](12-zone-recipes.md) | `recipes/` (Z3) | active |
| [13-zone-snippets.md](13-zone-snippets.md) | `snippets/` (Z4) | active |
| [14-zone-templates.md](14-zone-templates.md) | `templates/` — MIT policy (Z5) | active |
| [15-zone-probes.md](15-zone-probes.md) | `probes/` (Z6) | active |
| [16-zone-tools.md](16-zone-tools.md) | `tools/` (Z7) | active |
| [17-zone-pi.md](17-zone-pi.md) | `.pi/` prompts/skills/settings (Z8) | active |
| [18-zone-agents.md](18-zone-agents.md) | product `AGENTS.md` (Z9) | active |
| [19-registre-artefacts.md](19-registre-artefacts.md) | Metadata template + relations (Z10) | active |
| [20-auteur-modules.md](20-auteur-modules.md) | SKILL.md writing (A1) | active |
| [21-zone-router.md](21-zone-router.md) | `router/` — semantic routing index (Z11) | active |
| [22-zone-spec-driven-dev.md](22-zone-spec-driven-dev.md) | spec-driven-dev + deep-discuss workflow (Z12) | active |
| [23-zone-ui-kit.md](23-zone-ui-kit.md) | `ui-kit/` — pinned ui-agent-kit SDK zone, UI routing corpus, Wails-only sync (Z13) | active |
| [24-zone-workspace-init.md](24-zone-workspace-init.md) | `.pi/skills/workspace-init/` — kernel-first project foundation protocol, `workspace/` capture + AGENTS.md section (Z14) | active |
| [30-conventions.md](30-conventions.md) | Naming, formats, boundaries (N1) | active |

## Origin

- Audit: `docs/research/2026-08-04-kit-audit-governance.md`.
- Plan: `docs/plans/2026-08-04-kit-governance-phase2.md`.
- Decisions: `.pi/memory/Decisions.md` (2026-08-04).
- Evidence: `docs/evidence/2026-08-04/kit-governance-phase2/`.

## Contract maintenance

- Modifying a contract = written decision if the scope changes (new rule, new
  mandatory field); typo/rewording = direct.
- Every new rule in a contract must be formulated to be verifiable by C2 (the
  validator) — an unverifiable rule is a hypothesis.
- Each contract has an "Open questions" section: resolving a question =
  decision in `.pi/memory/Decisions.md` + contract update.
- Language: English mandatory (fundamental rule D-2026-08-05-21).
