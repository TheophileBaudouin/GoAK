# A1 — Module author (SKILL.md writing contract)

- **Metaproject Contract** — governs the writing of every kit SKILL.md module (rules, recipes, catalogs, .pi/skills). The working document `KitV2/templates/_kit-skill-authoring.md` remains a self-contained contributor aid **in the product**; this contract is the metaproject **authority**. It is not copied into the product (autonomy, N1): the product version may diverge as long as it does not contradict the rules here.
- **Audit report:** §4.3. **Sources:** agentskills.io spec, Claude best-practices, Red Hat ACE, Google Agent Skills.

## 1. Common invariants (all modules)

1. **Immutable frontmatter**: `name`, `description`, `category`, `tags`, `last-verified`. No new field without a global migration; `name` = parent directory.
2. **Fresh research**: any catalog writing or update is preceded by current web research on primary sources. Each used source is dated in `Sources vérifiées`; the `last-verified` date is the date of the full re-read.
3. **One piece of information, one location**: a fiche does not repeat a limit, alert, or decision in another language or section. An optional section without new content is removed.
4. **Verifiable example**: every Go block presented as minimal/runnable handles returns and resources according to the applicable rules. An abbreviated excerpt carries the `illustrative` marker and is not presented as compilable.
5. **Progressive disclosure**: L1 description (the only thing in permanent context); L2 body ≤ 500 lines; L3 details in referenced files (one depth level) — never in the body.
6. **Description = what + when + negative constraints**: this is the discoverability bottleneck (Red Hat: "write your L1s like abstracts optimized for search"). "Extracts text from PDFs. Use when working with PDF documents. Not for images." — never "Helps with PDFs".
7. **Module-relative paths**; tagged cross-references (stable ids), never a rot-prone prose link.
8. **Primary sources** for every fact; a synthesis is a starting point, never the only basis.
9. **No artificial sections**: a section exists only if it has content; no universal body template.

## 2. Per-category matrix

| Category | Activation | Mandatory sections | Minimal validation | Specific anti-patterns |
| --- | --- | --- | --- | --- |
| **recipe** | "Use when a consumer project matches this shape" | Problem · Solution (minimal code) · Why not alternatives · Runnable example + test · Observable scenario (actions + expected outputs) · Limits · Sources | Compiles; tests; executed scenario with `PASS`/`PARTIAL`/`BLOCKED` verdict — never `PASS` without execution | Non-runnable code; asserted instead of executed scenario; framework when stdlib suffices |
| **rule** | "Load when writing code in this area" | Imperative · When to apply · Boundary (does NOT cover) · Counter-examples · Verification · Sources | Green mechanics; explicit boundary; sources | Vague instruction; opinion without source; rule without boundary; contradiction with another rule |
| **library** | "Use when choosing a library for this responsibility" | Selection (version + admission reason, not stars) · Admission 9 criteria · Alternatives with verdicts · Minimal use · **Fiche format (N1 §4: When to use / When NOT to use, Advantages, Disadvantages, Pitfalls, Verified sources)** · Sources | Admission answered with evidence; minimal use compiles; rejected alternatives recorded; complete fiche (6 N1 §4 sections) | Stars as reason; missing rejected alternative; recommendation without reading issues; incomplete fiche |
| **reference-project** | "Use when designing a shape this project demonstrates" | Extract-only: what CAN be extracted · what must NEVER be copied · Verification · Sources | Every extracted pattern traces to the repo; no copied code/tree; admission applied | Tree cloning; project-imposed architecture; admission by popularity |
| **core** (rules/core) | "Loaded every session" | Principle · Boundary · Short examples · Sources | Compactness budget (≤ 6 modules, ≤ 300 lines); no registry reference | Domain content; "just this once" growth; duplication |
| **workflow** (`.pi/skills/`) | "Loaded when the process applies" | Procedure · Boundary with modules · References | Complete frontmatter; no domain knowledge | Workflow skill containing domain; duplication with a prompt |

## 3. Line and token budget (Red Hat/Claude)

- L1: 1–2 sentences, specific, with negative constraints.
- L2: ≤ 500 lines; beyond → move to L3 (referenced files).
- L3: **gated** — load only what is needed for the invocation; a massive ungated L3 file is the biggest token sink.

## 4. Writing cycle (Google: skills as products)

1. Research and verified primary sources (200 links, content read).
2. Writing per the matrix; self-check: does the L1 description trigger the right loading? does the body answer the question?
3. Minimal category eval executed (recipe: scenario; library: admission + compile).
4. Fresh-context review (sub-agent) before admission.
5. Recording: complete metadata, freshness, relations.

## 5. General anti-patterns (reject on sight)

- Vague description ("Helps with …"); body = exhaustive documentation;
- empty sections; placeholder; duplication of an existing module;
- a fact without source; a dead URL; `last-verified` bumped without re-verifying.

## 6. Validation criteria

- [ ] C2: complete frontmatter, name == directory, ≤ 500 lines, description with activation + negative constraints.
- [ ] Category mandatory sections present (per-category C2).
- [ ] Sources present; links verified at admission.
- [ ] Minimal eval executed and traced.

## 7. Open questions

- None: the relationship with `_kit-skill-authoring.md` is settled above (metaproject authority vs self-contained product aid).
- `workflow` category (`.pi/skills/`): schema extension recorded in `.pi/memory/Decisions.md` — the matrix categories above remain the module set (A1).
