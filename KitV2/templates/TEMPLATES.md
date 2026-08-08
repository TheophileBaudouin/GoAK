# Project template catalog

## Policy (owner directive, 2026-08-04)

The Kit's templates are **never written by an agent**. Each template is a
slightly adapted copy of a **real open-source project**:

- **MIT** license (fully open) — mandatory;
- reliable project: maintained, tested, CI, active community;
- **ultra-specific and minimal**: almost exclusively the template's
  technology — one stack, no out-of-scope ancillary technology; small,
  browsable-end-to-end codebase, clear and modular structure (integration by
  copying well-delimited modules, simple modification);
- **single responsibility**, directly reusable with very few modifications;
- conformant to the Kit rules (idiomatic, stdlib-first, no imposed
  framework);
- **functional**: compiles and passes its tests — a non-functional template
  is forbidden;
- minimal Kit adaptations **documented** (diff + reasons);
- attribution: source, pinned version, license, adaptations (including the
  technical scope: one technology, no ancillary technology).

The agent documents and adapts; it does not develop the template. Better
**fewer templates, very high quality**, improved by the community, than
home-made skeletons.

## Current status

The inherited agent-generated scaffolds were removed on 2026-08-05. The
catalog keeps only three real, pinned, MIT, verified projects:

| Template | Status | Source | Scope |
| --- | --- | --- | --- |
| rest-api | sourced | leeprovoost/go-rest-api-template | HTTP REST stdlib-first |
| cli | sourced | danjdewhurst/go-toc | Markdown TOC generation CLI |
| worker | sourced | sangianpatrick/go-workerpool | bounded worker pool |

The `grpc`, `microservice`, `monolith`, `cloud-service`, and `desktop-app`
shapes remain a roadmap without an operational template. `desktop-app` is
covered at recipe + probe level (`recipe-desktop-app`, `probes/desktop-app`)
but no conforming MIT source was found in the 2026-08-05 desktop-app research
(no real single-responsibility Wails application). No scaffold must be
recreated to represent them: a shape without a conforming MIT source stays
planned.

## Kit machinery (not sourced templates)

Two `_kit-*` files ship inside `templates/` but are **not** sourced project
templates — they are kit machinery, declared here to keep the catalog honest
(Z5 §8: TEMPLATES.md coherent with the tree):

- `_kit-ci-workflow.yml` — a drop-in CI gate for new Go projects (same
  checks as the kit's validation gate, minus the monorepo working-directory).
- `_kit-skill-authoring.md` — the SKILL.md authoring matrix (self-contained
  contributor aid in the product).

## structure.md (project reading map) — mechanism

Every sourced template ships a `structure.md` at its root (charter Layer 5.1):
a reading map for a non-developer, not an inventory of files. The mechanism
is implemented in `tools/generators/structure_md.py`:

- **Generation is the default.** `python3 tools/generators/structure_md.py
  generate <project-dir>` derives the tree side from the real tree
  (top-level directories, Go package names, entry points, test locations,
  internal/public boundary) and emits the skeleton; a human reviews and
  fills the semantic content (role lines, reading path, boundary
  explanations).
- **Drift gate.** `validate-kitv2.py` runs the checker on every sourced
  template's `structure.md`: the machine-checked `Tree facts` block must
  match the real tree exactly (completeness — every top-level directory has
  an entry — and tree-side conformity), so a drifted map blocks the gate.
  Semantic content is exempt from the check and is never claimed
  machine-verifiable.
- **Validation is the exception.** A hand-written structure.md is accepted
  only when a project uses a non-standard layout and the same drift gate
  still runs (Layer 5.1 conditions).

Forbidden content: exhaustive file inventory, API documentation, and
architectural decision history (they belong in the README, doc comments, and
decision records; §4 single source of truth).

## Admitting a new template (sourced)

1. Identify a real open-source MIT project, **ultra-specific** (one
   technology, no ancillary stack), **minimal** (small, browsable, clear
   modular structure), single-responsibility, conformant to the Kit rules.
2. Pin the version (commit/release) and verify the MIT license.
3. Copy the project into `templates/<shape>/` with `LICENSE`,
   `ATTRIBUTION.md` (source, version, adaptations) and `README.md` (status,
   source, observable scenario).
4. Adapt **minimally** to the Kit; each adaptation is documented in
   `ATTRIBUTION.md` with its reason.
5. Record `usage-evidence` in `template.yaml` (documented real usage —
   observed consumer demand or a real, maintained project, never theoretical
   utility; charter §16.1.3).
6. Generate `structure.md` (tree side) and complete the semantic sections;
   declare the mechanism in `template.yaml`.
7. Verify: compile, tests, executed and recorded observable scenario
   (`PASS`/`PARTIAL`/`BLOCKED`).
8. Update this catalog and the validator (expected template shape).

The existing recipes remain the canonical implementation evidence for the
shapes that do not yet have a conforming MIT source.
