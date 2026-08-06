# Template catalog contract

```yaml
name: go-agent-template-catalog
status: catalog
purpose: Define project shapes as sourced, MIT-licensed, functional templates — never agent-authored.
validation: Each sourced template ships a real open-source MIT project (pinned version), LICENSE, ATTRIBUTION.md (source + adaptations + technical scope), a runnable scenario, and passing tests. Planned shapes ship no scaffold.
policy: Templates are forks of reliable open-source projects, minimally adapted, documented, functional. Selection bar: ultra-specific and minimal — almost only the template's technology, no auxiliary stack, small browsable codebase, clear modular structure. Agent-authored scaffolds are retired and must not be recreated (see TEMPLATES.md).
```

## structure.md mechanism (charter Layer 5.1)

Every sourced template ships a `structure.md` at its root (reading map for a
non-developer) whose tree side is machine-checked:

- `template.yaml` declares the mechanism (`structure.md:
  generated-with-semantic-review` or `validated`).
- Generation is the default: `tools/generators/structure_md.py generate`
  derives the tree side from the real tree; a human fills the semantic
  sections (role lines, reading path, boundary, evidence).
- The drift gate runs in `validate-kitv2.py` (tree-facts exactness +
  completeness of the roles section); semantic prose is exempt and never
  claimed machine-verifiable.
- Forbidden content: exhaustive file inventory, API documentation,
  architectural decision history (single source of truth, §4).
- `template.yaml` also records `usage-evidence` (charter §16.1.3): documented
  real usage — observed consumer demand or a real, maintained project — never
  theoretical utility. A new category without the field is non-conformant.
