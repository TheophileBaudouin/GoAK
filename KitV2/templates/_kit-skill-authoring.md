# Skill authoring matrix — Go Engineering Kit

Short authoring template/matrix for a `SKILL.md` module (human or agent).
It is a working document — **not a skill, not a Pi prompt, not a new schema**.
It adapts only the established research convergences
(the repository's reviewed Pi-native and kit-practice research, §4.3 contract
per category, R4 category templates) to the existing categories. It does not
introduce new norms.

## Common invariants (every module)

1. **Frontmatter immutable** — the published schema (`name`, `description`,
   `category`, `tags`, `last-verified`) is a contract. Never add, rename, or
   drop a field "for structure"; a schema change requires approval and a
   migration of all modules in the same commit.
2. **Progressive disclosure** — short frontmatter, short procedural body;
   long detail moves to targeted references (one level deep), never into the
   body. A `SKILL.md` is not exhaustive API documentation.
3. **Description = what + when** — `description` is the routing mechanism
   (Pi skips skills without it). State what the module does AND when to load
   it; never keep activation conditions only in the body.
4. **Relative paths** — all references use paths relative to the module or
   tagged cross-references; no rot-prone prose links.
5. **Primary sources** — every factual claim (API facts, security notes,
   library verdicts) traces to a primary, verifiable source; a synthesis is a
   starting point, never the sole basis.
6. **No artificial sections** — a section exists only if it has content.
   Empty, filler, or placeholder sections are forbidden; there is no universal
   template.
7. `name` equals the parent directory, and the module passes the shared
   validation gate (see `../AGENTS.md`) before it is marked done.

## Category matrix

| Category | Objective / activation | Mandatory sections | Conditional sections | Minimal validation | Specific anti-patterns |
| --- | --- | --- | --- | --- | --- |
| **recipe** | Runnable, tested pattern for a concrete project shape. Load when a consumer project matches that shape. | Problem · Solution (minimal code) · Runnable example + test · Observable scenario (actions + expected output) · Limits · Sources | Decision boundary / alternatives · Security note · Migration note | Code compiles; tests pass; the observable scenario is actually run and marked `PASS`, or explicitly marked `PARTIAL`/`BLOCKED` when it cannot run — never `PASS` an unexecuted scenario | Non-runnable or untested code · scenario asserted instead of run · framework reached for when stdlib suffices · recipe copied without adaptation to the project type |
| **rule** | Idiomatic Go rule with an applicability boundary. Load when writing code in that area. | Rule (imperative) · When to apply · Counter-examples · Verification (how to check) · Sources | Minimal code snippet · Relationship to sibling rules | Mechanical checks pass; examples verified; the boundary states what the rule does NOT cover | Vague instruction ("use idiomatic Go") · opinion without a primary source · universal claim with no boundary · contradiction with another rule |
| **library** | Vetted library decision. Load when choosing a library for that responsibility. | Selection (version + stated admission reason, not stars) · Admission checklist (9 criteria) · Alternatives considered with verdicts · Minimal use · **Fiche format (N1 §4: Use when / Don't use when, Advantages, Drawbacks, Known pitfalls, Verified sources)** · Sources | Security note · Upgrade / migration notes | Admission criteria answered with evidence; minimal-use code compiles and passes checks; rejected alternatives recorded; fiche complete (6 sections, N1 §4) | Stars as the reason · missing rejected alternative · recommending without reading the issues · unverified security claims · admission on a single criterion · fiche incomplete |
| **reference-project** | Extract-only source of proven patterns. Load when designing a shape the project demonstrates. | What you MAY extract · What you must NEVER copy · Verification (criteria + evidence) · Sources | How an agent should use it | Each extracted pattern traces to the primary repo; no code or tree copied; admission gate applied with evidence recorded | Cloning the tree or starter shape · importing the project's imposed architecture (K8s-first, RBAC, …) · popularity-only admission · treating issue count as reading the issues |
| **core** | Universal principle, loaded every session; always relevant. | Principle · Applicability boundary · Short examples · Sources | Decision order | Compactness budget respected; cross-referenced, not duplicated; no direct reference to `registry/` content | Project-type-specific content · growing "just this once" · duplicating content that exists elsewhere · direct `registry/` references |

## Minimal output template

Copy this skeleton; delete any section that has no content (invariant 6).
`core/` modules reuse an existing category value (`philosophy` uses `rule`);
never invent a `core` category value.

```markdown
---
name: <kebab-case, equal to the parent directory>
description: "<what it does> Use when <when to load it>."
category: <recipe | rule | library | reference-project>
tags: [<kit search facets>]
last-verified: YYYY-MM-DD
---

# <name> — <one-line title>

## <mandatory section 1>
...

## Sources
- <primary source 1>
- <primary source 2>
```
