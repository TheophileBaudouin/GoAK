---
name: no-internal-duplication
description: "Single-source-of-truth rules for GoAK catalog modules. Load when authoring or reviewing a catalog; keep one canonical statement per fact and use cross-references instead of bilingual or repeated sections."
category: rule
tags: [catalog, duplication, single-source-of-truth, documentation]
last-verified: 2026-08-05
---

# no-internal-duplication — one fact, one home

## Rule

A catalog file contains one canonical statement for each decision, limitation,
security warning, or usage rule. Do not restate the same fact in another
language, section, table, or paraphrase merely to fill the fiche format.
Remove an optional section when it adds no distinct information.

Use one coherent language for the body of a file. The mandatory French decision
headings are labels, not a reason to translate and repeat the preceding English
content.

## Section boundaries

- `Selection`: what the library is and why it is admitted.
- `Minimal use`: the smallest correct example, not a second limitations list.
- `Alternatives considered`: comparative decisions only.
- `When to use` / `When NOT to use`: selection boundaries not already stated.
- `Advantages` / `Disadvantages`: trade-offs, each stated once.
- `Known pitfalls`: actionable misuse warnings not already covered elsewhere.
- `Verified sources`: evidence and dates, not a prose summary.

## Verification

Before commit, compare every paragraph and table row within the file. Exact
and near-verbatim matches are defects. A semantic paraphrase that preserves no
new decision is also a defect and requires human review; do not claim that a
text-only scanner proves semantic uniqueness.

## Boundary

This rule does not prohibit a short cross-reference to another canonical
artifact, a necessary repeated term in a heading, or a new example that adds a
different behavior. It prohibits duplicate information, not shared vocabulary.

## Sources

- [Agent Skills specification](https://agentskills.io/specification) —
  progressive disclosure and bounded skill bodies; verified 2026-08-05.
- [GitHub content instructions](https://github.com/github/docs/blob/main/.github/instructions/content.instructions.md)
  — reusable content and single-purpose guidance; verified 2026-08-05.
