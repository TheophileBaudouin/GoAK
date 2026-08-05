# Z8 — Zone `.pi/` (settings, prompts, workflow skills)

- **Metaproject Contract** — governs `KitV2/.pi/`.
- **Audit report:** §2.11. **Decision:** the 5 workflow skills stay in the product (2026-08-04).

## 1. Mission

The product's native Pi execution layer: discovery (settings), invocation (prompts), workflow procedures (skills). Three **disjoint** roles, zero overlap.

## 2. The three roles (inviolable boundary)

| Surface | Role | Example |
| --- | --- | --- |
| `.pi/prompts/*.md` | **Orchestrators** invoked manually (`/checklist-api`) | workflow-memory, checklist-api, checklist-release |
| `.pi/skills/*/SKILL.md` | **Durable procedures** loaded by context | spec-driven-dev, deep-discuss, go-code-review, go-idiomatic-implementation, go-implementation-plan, go-source-retrieval, go-testing-verification, kit-resource-routing |
| modules `rules/`, `recipes/`, `knowledge/catalogs/` | **Knowledge content** (discoverable by description) | recipe-worker-pool, chi, philosophy |

Rule: if a prompt and a skill answer the same question, keep one and the other points (anti-duplication C0). A workflow skill does not contain domain knowledge (it lives in the modules). Since 2026-08-05 (D-2026-08-05-16), the reference workflow for large-scale transformations is the `spec-driven-dev` skill (contract Z12); the former `workflow-clarify → plan → tasks → implement → verify` prompt chain has been removed and must not be recreated.

## 3. Rules

1. **Every skill has complete frontmatter**: `name`, `description` (explicit activation), `category: workflow`, `tags`, `last-verified`. A skill without `description` is not loaded by Pi.
2. **Every prompt has a `description`** of activation and follows the `workflow-*` / `checklist-*` naming convention.
3. `settings.json` loads modules by product-relative paths (`../rules`, `../recipes`, `../knowledge/catalogs`) — the path contract is documented in `.pi/README.md` and stable whatever the installation method.
4. A workflow skill stays generic to the process (review, plan, source, verification): any domain specificity migrates to a module.
5. `category: workflow` is a kit-only value (outside the validated module set): it applies only to `.pi/skills/`; modules keep the A1 categories.
6. **Absolute instruction = named control** (2026-08-05, D-2026-08-05-15): any `MANDATORY`/"always"/"never" instruction carried by a skill or prompt must name a mechanical control (validator C2 or Pi gate) or be labeled "guidance only, not enforced" and recorded in the automation-gaps registry (`.agent/instructions.md` §Enforcement).

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
