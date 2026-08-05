# Philosophy tension: Go minimalism vs personal predictability

Date: 2026-08-05. Author: metaproject governance-hardening pass (Rodin
finding C). Status: decision note — the decision belongs to the owner
(product choice), not the agent.

## 1. The contradiction, without softening

Two objectives face each other, and they are **incompatible as stated**:

**Objective A — "the Kit stays idiomatic and without imposed structure"**
(sourced doctrine, already normative):

- `AGENTS.md` (root, Evidence rules section): "Go does not prescribe a
  universal project tree; use official package naming guidance and Go
  Proverbs."
- `KitV2/rules/core/philosophy/SKILL.md` (Boundary section): "it prescribes
  no universal project layout (the official module-layout examples are shapes
  to choose from, not a standard)."
- Cited sources: Effective Go, Go Proverbs, go.dev/doc/modules/layout
  ("Organizing a Go module" — shapes, not a standard).
- Source registry: `golang-standards/project-layout` is not Go authority.

These two texts are **coherent with each other** (verified: they say the same
thing). It is Objective B that contradicts them.

**Objective B — "I want to navigate the same way in any project produced by
the Kit"** (owner's declared personal need): an identical structure to find
the same things in the same place without effort, whatever the project.

If the Kit prescribes "choose the smallest justified structure each time",
two projects produced by the Kit can legitimately have different trees (one a
root `main.go`, another `cmd/` + `internal/` depending on need). Personal
navigation is then not guaranteed identical. Conversely, if the Kit imposes a
single layout, it contradicts the sourced doctrine and stops being "minimal
justified".

This is not an editorial detail: it is a product choice touching
`KitV2/rules/core/` — a zone whose modification requires explicit approval
(AGENTS.md Modification policy). The agent does not decide alone.

## 2. Options with trade-offs

### Option 1 — Keep minimalism, solve elsewhere

The Kit stays idiomatic and without imposed structure (it must also work for
uses other than the owner's). The personal need for predictable navigation is
met by a **separate preset**, clearly labeled "non-canonical", that the owner
activates voluntarily on their projects (e.g. a "fixed personal structure"
recipe/checklist or a prompt applying their preferred layout).

- Advantages: contradicts no source; the core keeps its "sourced, no invented
  opinion" position; the preset stays reversible and personal.
- Costs: the preset must be maintained separately; a third-party Kit consumer
  does not inherit the owner's predictability (it is not their need).
- Risk: if the preset drifts into unsourced doctrine, it must stay labeled
  non-canonical — controllable at review.

### Option 2 — Change the philosophy of the core

`rules/core/philosophy` prescribes a single layout, with documented
case-by-case exceptions.

- Advantages: maximum predictability — the tree is identical everywhere.
- Costs: contradicts frontally Effective Go / Go Proverbs /
  go.dev/doc/modules/layout cited as sources; weakens the kit's "sourced, no
  invented opinion" position; the kit rules would then have to document this
  assumed deviation and its justifications, which is a major doctrine change
  (major version, migration, written decision).
- Risk: a kit imposing a single structure becomes a shape framework —
  contrary to the "typed knowledge graph, not framework" vision (Brief.md).

### Option 3 — Predictability by documentation, not by uniformity

Keep the structure freedom, but make it mandatory that a recipe systematically
produces a "why this layout here" artifact in the same place (e.g. a
`Structure` section in each generated project, or a root `layout.md` produced
by the recipes).

- Advantages: the tree stays free and sourced; navigation becomes predictable
  because the **reason** is always in the same place; low doctrine cost (a
  recipe-shape rule, not a Go structure rule).
- Costs: the real tree can still differ between projects — predictability is
  cognitive (you know where to find the reason), not physical (same paths);
  requires adding an obligation to the production recipes.
- Risk: low; remains compatible with both objectives if the owner accepts
  predictability by reason rather than by uniformity.

## 3. What the decision implies

- **Option 1 or 3**: metaproject scope possible (preset recipe/prompt for 1;
  recipe-shape rule for 3 — but 3 also touches `KitV2/recipes/`, so the next
  pass for existing recipes). If the owner chooses 1 or 3, the agent applies
  what is metaproject and writes the KitV2 edits as pending actions.
- **Option 2**: touches `KitV2/rules/core/philosophy/SKILL.md` (forbidden
  zone this pass) — the exact edit is written in the plan
  (docs/plans/2026-08-05-metaproject-governance-hardening.md) as a pending
  action, never applied here.

## 4. Question asked to the owner

See the question sent via the question tool (template: "The Kit currently
tells the agent: there is no single good Go project structure, choose the
smallest that fits each time. You, you want rather: I always want to navigate
the same, whatever the project. These two rules contradict each other. Three
ways to settle…").

## 5. Owner decision (2026-08-05)

**Option 3 — navigate by reason.** Structure freedom is kept, but every
project produced by the Kit explains in writing, always in the same place, why
it chose its structure; navigation becomes predictable because the reason is
always in the same place.

Application:

- Metaproject (applied in this pass): Z3 §3 — new mandatory section
  "Structure (why this layout)" for every recipe that produces/recommends a
  project layout (N/A otherwise); Z5 §3 — the template README requires the
  structure and its justification.
- KitV2 (pending action, next pass): add the section to the concerned
  recipes; add the structure justification to the 3 sourced templates'
  READMEs.
- No root AGENTS.md or `rules/core/philosophy` modification: Option 3 is
  compatible with the sourced doctrine ("no universal project layout") — it
  adds a recipe-shape obligation, not a Go structure rule.

Confidence: the citations of the two texts are verified directly (root
AGENTS.md §Evidence rules; philosophy SKILL.md §Boundary). The contradictory
character is a judgment established by direct reading of the two passages;
the resolution is a value choice that belongs to the owner.
