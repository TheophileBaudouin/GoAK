# Z8 — Zone `.pi/` (settings, prompts, workflow skills)

- **Metaproject Contract** — governs `KitV2/.pi/`.
- **Audit report:** §2.11. **Decision:** the 5 workflow skills stay in the product (2026-08-04).

## 1. Mission

The product's native Pi execution layer: discovery (settings), invocation (prompts), workflow procedures (skills), runtime behavior (extensions), consumer user guide (docs), and session-start orientation (onboarding). Six **disjoint** roles, zero overlap.

## 2. The roles (inviolable boundary)

| Surface | Role | Example |
| --- | --- | --- |
| `.pi/prompts/*.md` | **Orchestrators** invoked manually (`/checklist-api`, `/goak-help`) | workflow-memory, checklist-api, checklist-release, goak |
| `.pi/skills/*/SKILL.md` | **Durable procedures** loaded by context | spec-driven-dev, deep-discuss, go-code-review, go-idiomatic-implementation, go-implementation-plan, go-source-retrieval, go-testing-verification, kit-resource-routing, workspace-init |
| `.pi/extensions/*.ts` | **Runtime behavior** auto-loaded by Pi after trust | search_kit_resources, search_ui_kit_resources, kit-onboarding (session-start banner) |
| `.pi/docs/GOAK.md` | **Consumer user guide** — shipped source of truth for using the kit; read by `/goak-help` and the onboarding banner, works with no other documentation | — |
| `.pi/onboarding/banner.md` | **Session-start orientation** content (Get Started / large feature / small feature); rendered by `kit-onboarding.ts`, never a second documentation | — |
| modules `rules/`, `recipes/`, `knowledge/catalogs/` | **Knowledge content** (discoverable by description) | recipe-worker-pool, chi, philosophy |

Rule: if a prompt and a skill answer the same question, keep one and the other points (anti-duplication C0). A workflow skill does not contain domain knowledge (it lives in the modules). Since 2026-08-05 (D-2026-08-05-16), the reference workflow for large-scale transformations is the `spec-driven-dev` skill (contract Z12); the former `workflow-clarify → plan → tasks → implement → verify` prompt chain has been removed and must not be recreated.

## 3. Rules

1. **Every skill has complete frontmatter**: `name`, `description` (explicit activation), `category: workflow`, `tags`, `last-verified`. A skill without `description` is not loaded by Pi.
2. **Every prompt has a `description`** of activation. Workflow/checklist orchestrators follow the `workflow-*` / `checklist-*` naming convention; the kit entry-point command `/goak-help` (`.pi/prompts/goak-help.md`) is the single deliberate exception — the filename is the command name, and the entry point is a stable contract (D-2026-08-08-15).
3. `settings.json` loads modules by product-relative paths (`../rules`, `../recipes`, `../knowledge/catalogs`) — the path contract is documented in `.pi/README.md` and stable whatever the installation method.
4. A workflow skill stays generic to the process (review, plan, source, verification): any domain specificity migrates to a module.
5. `category: workflow` is a kit-only value (outside the validated module set): it applies only to `.pi/skills/`; modules keep the A1 categories.
6. **Absolute instruction = named control** (2026-08-05, D-2026-08-05-15): any `MANDATORY`/"always"/"never" instruction carried by a skill or prompt must name a mechanical control (validator C2 or Pi gate) or be labeled "guidance only, not enforced" and recorded in the automation-gaps registry (`.agent/instructions.md` §Enforcement).
7. **Onboarding surface is part of the product** (D-2026-08-08-14..17): the user guide (`.pi/docs/GOAK.md`), the `/goak-help` entry point, the banner (`.pi/onboarding/banner.md`), and the onboarding extension (`kit-onboarding.ts`) are shipped, self-contained, and enforced by `validate-kitv2.py` `check_consumer_onboarding`. Any change to kit commands, workflows, or structure that a user or agent can observe MUST update the guide in the same change; the banner stays orientation-only and must not grow into a second documentation.

## 4. Maintenance

- **Prompt addition**: naming + description + reference to the orchestrated skill/module if it exists.
- **Skill addition**: zone contract + duplicate-absence research (semantic) + complete frontmatter.
- **Modification**: bump `last-verified`; verify the role boundary.

## 5. Patterns

- Prompts = short, orchestrators; skills = procedures; modules = content.
- Explicit activation: the frontmatter description names the activation condition ("Use when …", "Use only after …") — generalize.

## 6. Anti-patterns

- Workflow skill containing domain knowledge (drift).
- Prompt and skill duplicating each other (role overlap).
- Skill without description; prompt without description.
- Metaproject content (decisions, memory) in product `.pi/`.

## 7. Validation criteria

- [ ] All `.pi/skills/` skills have the complete §3.1 frontmatter.
- [ ] All prompts have a description.
- [ ] No detected duplicate prompts↔skills↔modules (manual check at review; C2 may grep titles).

## 8. Open questions

- None open: the frontmatter of the `.pi/skills/` skills (category `workflow`, tags, last-verified) was completed on 2026-08-04 — the schema extension is recorded in `.pi/memory/Decisions.md`.
