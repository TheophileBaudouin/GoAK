# KitV2 boundary correction plan

## Goal

Keep metaproject governance and memory at the repository root while making
KitV2 a consumable, Pi-native kit. The kit may ship a small `AGENTS.md` because
Pi reads it as project context, but it must not ship this metaproject's history.

## Evidence

Local Pi documentation and a fresh research review establish:

- Pi loads `AGENTS.md` from global, ancestor, and current directories.
- Pi loads project `.pi/settings.json` after trust.
- Pi loads direct `.pi/prompts/*.md` and recursively discovers
  `.pi/skills/**/SKILL.md`.
- Pi does not load singular `.agent/` or `.agent/instructions.md`.

Reports: `.pi-subagents/.../pi-compatibility.md`,
`.pi-subagents/.../agent-conventions.md`, and
`.pi-subagents/.../kitv2-boundary-review.md`.

## Ownership

### Metaproject-only: root

- `AGENTS.md`, `KIT_CHARTER.md`
- `.pi/memory/`
- `docs/plans/`, `docs/research/`, `docs/evidence/`
- `.pi-subagents/` research artifacts

### Consumable KitV2

- `AGENTS.md` — compact kit contract read by Pi.
- `.pi/settings.json`, `.pi/prompts/`, `.pi/skills/` — native Pi resources.
- `rules/`, `knowledge/`, `recipes/`, `snippets/`, `templates/`, `probes/`, and
  validation scripts — product content.

Product verification is represented by `probes/` and executable checks. The
metaproject's evaluation methods remain under the root `.agent/evaluations/`
and are not shipped.

The singular `.agent/` is not a Pi-native discovery path. It is removed from
KitV2 rather than presented as if Pi would load it. If a future adapter needs
its own control-plane format, it must be designed and approved separately.

## Changes

Remove from KitV2:

- `.agent/` entirely, because its files are metaproject governance, duplicated
  Pi resources, or unsupported control-plane assumptions.
- top-level `tools.yaml`, whose evidence policy belongs to the metaproject and
  duplicates validation commands elsewhere.

Keep and correct:

- `AGENTS.md` to point consumers to their own `.pi/memory/` and `.pi/prompts/`.
- `.pi/settings.json` to contain only native settings; prompts are discovered
  from `.pi/prompts/` by convention.
- `capabilities.yaml` and `manifest.yaml` as product metadata, explicitly
  documenting that they are not Pi instruction entrypoints.

## Non-goals

- Do not touch `kit/` v1.
- Do not delete root metaproject memory or evidence.
- Do not add `.agents/` or claim singular `.agent/` compatibility.
- Do not add adapters, CI, dependencies, or a workflow runtime.

## Validation

- Verify `find KitV2/.agent` is absent.
- Verify KitV2 contains `AGENTS.md`, `.pi/settings.json`, `.pi/prompts/`, and
  `.pi/skills/`.
- Run the V2 structural validator, Go gate, snippets, templates, and probes.
- Run a trusted temporary-copy Pi discovery check and record exact output.
- Obtain fresh-context review and record remaining PARTIAL risks.
