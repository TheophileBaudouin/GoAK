# Templates

The catalog is explicit about status. It contains only real MIT-sourced projects
that are pinned, attributed, tested, and narrowly scoped, plus two declared
kit-machinery files (`_kit-ci-workflow.yml`, `_kit-skill-authoring.md` — see
`TEMPLATES.md` § "Kit machinery"). The inherited agent-authored scaffolds were
removed on 2026-08-05. Planned shapes are roadmap entries, not
production-ready project bases.

## Current sourced projects

- `rest-api`: standard-library-first HTTP service foundation.
- `cli`: tested Markdown table-of-contents CLI.
- `worker`: dependency-free bounded worker pool.

Read each template's `README.md` and `ATTRIBUTION.md` before adapting it. The
source tree, license, tests, and observable scenario are part of the template;
Kit metadata must not be mistaken for application implementation.

Each sourced template also ships a `structure.md` (reading map, charter
Layer 5.1): its tree side is machine-checked by the kit's drift gate, the
semantic content is human-reviewed. Regenerate the tree side with
`python3 tools/generators/structure_md.py generate <template-dir>` when the
template's tree changes, then complete the semantic sections.
