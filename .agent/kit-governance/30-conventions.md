# N1 — Conventions (naming, formats, boundaries)

- **Metaproject Contract** — cross-cutting rules applying to all Z1–Z10 and A1 contracts.

## 1. Naming

| Object | Rule | Example |
| --- | --- | --- |
| Artifact id | `<kind>:<domain>:<slug>` kebab-case, ASCII | `pattern:go:concrete-returns` |
| SKILL.md module directory | English kebab-case = frontmatter `name` | `recipe-worker-pool/` |
| Graph-YAML file | kebab-case, domain-prefixed | `anti-patterns/go-mutable-global-state.yaml` |
| Recipe | `recipe-<domain>-<subject>` | `recipe-rest-chi` |
| Probe | `<shape>-<subject>` (or `<subject>`) | `worker-shutdown` |
| Template shape | kebab-case, domain | `rest-api` |

Forbidden: uppercase in ids/paths, spaces, non-ASCII characters, French in
ids. **Language rule (fundamental, D-2026-08-05-21): English is the mandatory
language for every skill, instruction, and document in this repository** —
the content language is English, the identifier stays ASCII kebab-case.

## 2. Formats (choice rule — one truth, one format)

| Artifact type | Canonical format | Justification |
| --- | --- | --- |
| Rule, Recipe, vetted Library, Reference project, Template (via its README) | SKILL.md (Pi frontmatter + body, progressive disclosure) | Pi discoverability (description in the system prompt), load on demand |
| Pattern, Anti-pattern, Source (official pointers), domain guidance (security/performance/observability/architecture/debugging), stdlib | Graph-YAML (`id`/`kind`/`relationships`) | Machine-resolvable graph, relations verified by C2 |
| Snippet | SNIPPET.yaml + example.go + check.sh | Executable and linked to a canonical source |
| Probe | main.go + `PASS` verdict + exit code | Executable evaluation |
| Sourced template | MIT project directory + LICENSE + ATTRIBUTION.md + README | Owner policy (Z5) |
| Prompt / workflow skill | `.pi/prompts/*.md` / `.pi/skills/*/SKILL.md` | Roles delimited by Z8 |

Rule: **two formats are never mixed for the same role without a contract**;
any new format requires a written decision (Decisions.md) and an update of
this table.

## 3. Graph-YAML — writing conventions

- Mandatory metadata (C0/Z10): `id`, `title`, `kind`, `version`, `status`,
  `owner`, `tags`, `go_version`, `dependencies`, `last_verified`.
- Relations: `relationships.<relation>: [targets]`; targets are stable ids or
  URLs (only for `references`).
- Body: block scalars (`>-` / `|`); one idea per section; no free nested YAML.
- `go_version`: the minimum **tested** version; never a future version.
- Canonical URLs: **never rewritten** to satisfy a style linter. If a
  `source:` line exceeds ~80 characters (external YAML linter, not configured
  in the repo), use the valid YAML escape `"...\<line break>  continuation"`
  (double-quote + backslash: resolves to a single string without space —
  verify with `yaml.safe_load`).
- Language: ids ASCII; content in **English** (D-2026-08-05-21) — mandatory
  for all skills, instructions, and documents.
- Post-write: every created graph-YAML is re-read (`yaml.safe_load`) and its
  freshness/relations checked before validation; lines > 80 are not a project
  gate (the corpus already contains them — URLs and content).

## 4. SKILL.md — conventions (detailed in A1)

- Immutable frontmatter: `name`, `description`, `category`, `tags`,
  `last-verified` — no new field without a global migration.
- Progressive disclosure: description (L1) = what + when + negative
  constraints; body (L2) ≤ 500 lines; details in referenced files (L3).
- Module-relative paths; never a rot-prone prose link.
- Catalog `libraries/` body: **canonical "fiche" format** — the following
  decision sections are mandatory for every admitted library:
  `## When to use this library`, `## When NOT to use this library`,
  `## Advantages`, `## Disadvantages`, `## Known pitfalls`,
  `## Verified sources` (URL + date + source type; negative claims confirmed
  by ≥ 2 independent sources, or ≥ 1 official project issue/advisory).
  Preexisting sections (Selection, Admission checklist, Minimal use,
  Alternatives, Notes) are kept as-is.
- **Language migration note (D-2026-08-05-21)**: the kit is under a mandatory
  English rule. **Wave executed 2026-08-06 (D-2026-08-06-01)**: the residual
  French documented below was converted to English in one pass — 15 recipe
  SKILL.md (bodies + frontmatter descriptions), 39 `knowledge/patterns/` +
  54 `knowledge/anti-patterns/` graph-YAML bodies, 43 catalog fiche files
  (the 6 fiche headers, 37 French H1 titles, and the two French fiche bodies
  `bleve` and `golang-migrate`), `knowledge/architecture/mcp-server-shape.yaml`,
  and the `AGENTS.md` / `rules/registry/` references to the old French section
  names. Zero French remains on the kit instruction surface (accent-scan
  check, 2026-08-06). New content must be written in English at admission;
  kit-audit C7 verifies the instruction surface each audit.

## 5. Kit / Metaproject Boundaries (inviolable)

| What enters `KitV2/` | What NEVER enters it |
| --- | --- |
| Sourced knowledge content, modules, runnable code, probes, gate tools | Memory (`.pi/memory/`), decisions, metaproject evaluations, raw evidence (`docs/evidence/`) |
| Product `AGENTS.md`, native `.pi/` | `.agent/` (control plane), v1 history, `../` references to the root |
| Condensed contracts (zone README, AGENTS.md map) | Full metaproject contract bodies (they live in `.agent/kit-governance/`) |

Rule: the product never points to the metaproject; the metaproject may point
to the product. A consumer installing only `KitV2/` must be able to use it
without the root.

### 5.1 — Merged `AGENTS.md` sections (general convention)

Any zone that merges content into the product `KitV2/AGENTS.md` (Z13 today
with "UI work", Z14 with "Project Foundation", others tomorrow) MUST, by
convention — it is not a UI-kit special case:

1. **Delimited section**: wrap the merged section in explicit markers
   unique to the zone. Two accepted shapes:
   - static pointer content → begin/end markers
     (`<!-- <zone> section: begin -->` … `<!-- <zone> section: end -->`),
     checked by the validator for presence, order, and the expected title
     between them (Z14 model);
   - dynamic content mirrored from a source file → a content hash marker
     (`<!-- <source-path> sha256: <hash> -->`), checked against the source
     (Z13 model).
2. **Dedicated mechanical check**: the zone's contract lists a named
   `check_<zone>_placeholder` / pin check in `validate-kitv2.py`, wired
   into `main()`, with unit tests in `test_validate_kitv2.py`. A section
   without its check is a C9/C15 finding, not a documentation gap.
3. **Section isolation**: one zone's manual re-merge must never touch
   another zone's section; each section is edited through its own workflow
   (update-ui-kit Phase 2 guards the "Project Foundation" section too).
4. **Contract traceability**: the format of the markers and the check name
   are recorded in the zone's governance contract, in this section, and in
   the zone's validation criteria.

## 6. Placeholders and roadmaps

- **No empty `.gitkeep` directory**: planned zones live in the zone README
  (roadmap table with fill criteria).
- A domain directory exists only if it has ≥ 1 active artifact (or a contract
  README when the decision is to wait for evidence — `debugging/` case).
- Deleting a placeholder is ordinary governance, not a decision.

## 7. Validation criteria

- [ ] ASCII kebab-case ids; name == parent directory (modules).
- [ ] One format per role (§2 table respected).
- [ ] Zero empty placeholder; every roadmap has criteria.
- [ ] The product references no metaproject root (C2 already verifies it for
      YAML; extend to SKILL.md).

## 8. Open questions

- Id language vs content language: confirmed (ids ASCII, content English,
  D-2026-08-05-21).
- Should there be a boundary lint (grep `../` in product SKILL.md)?
