---
description: Audit the complete KitV2 product against KIT_CHARTER.md, rules, evidence, and the metaproject/Kit boundary without modifying files.
argument-hint: "[KitV2 zone]"
---

# Permanent audit of the KitV2 product

You are executing a **diagnostic, non-destructive, traceable** audit. The
product to audit is `KitV2/`, or the zone `KitV2/<zone>` passed as argument.
The prompt itself is a metaproject maintenance tool and is never part of the
shipped product.

## Safety contract

- Do not modify, create, or delete any file in the repository. Do not run a
  formatter, fixer, generator, `go mod tidy`, migration command, or any Git
  command that changes state.
- Do not apply any correction during inspection. Recommendations are produced
  only after the inventory and inspection are complete.
- Do not turn absence of evidence into conformity. A non-executable check or
  an unverifiable source receives `TO VERIFY`, never `CONFORM`.
- Do not treat the name of a rule, directory, or linter as proof: read the
  file and cite the exact path, line, or section.
- When invoked, audit the real tree, not a summary or inventory provided by
  the user; this prompt never replaces inspection of the repository.

## 1. Framing and scope

1. First read `KIT_CHARTER.md`, then the applicable rules of `AGENTS.md` and
   the zone contracts in `.agent/kit-governance/`. The charter is the
   authority; do not rewrite it in the report.
2. Before any conclusion, read the code of these two metaproject validators:
   - `.agent/validators/validate-instructions.py`;
   - `.agent/validators/validate-cognitive.py`.
3. Determine the target:
   - without argument: the whole `KitV2/`;
   - with a `KitV2/<zone>` argument: that zone, with the global context of the
     charter, installer, rules, manifests, and relations;
   - any target outside `KitV2/` is rejected as out of scope.
4. Always distinguish:
   - **audited files**: those of the target that receive a status for each
     applicable dimension;
   - **context files**: charter, rules, validators, installer, manifests, or
     sources read to interpret the target, but not counted in the KitV2
     inventory;
   - **excluded files**: only the cases explicitly justified in the report;
     they remain counted in the inventory.

## 2. Complete inventory — first mandatory step

The inventory must precede any interpretive reading. Record a UTC timestamp
(`YYYY-MM-DDTHH:MM:SSZ`), the absolute target, the received argument and, if
available without modifying the repository, the observed commit or Git state.

Build a complete, sorted list of all regular files and symbolic links under
the target, including hidden files, YAML, Markdown, JSON, Go, scripts,
manifests, tests, probes, configuration files, and binary files. Do not use
`head`, `tail`, a truncated output, or a manual list as the reference
inventory. An acceptable form is:

```sh
find -P "$TARGET" \( -type f -o -type l \) -print | LC_ALL=C sort
```

Keep this list in a temporary file outside the repository if the output is
too large for context. This temporary file is not a deliverable and must not
be confused with the product.

Immediately assign each path a coverage state in an internal ledger:
`TO INSPECT`, `INSPECTED`, `EXCLUDED (justification)`, or `BLOCKED (cause)`.
At reconciliation, no path may remain `TO INSPECT`: it must become
`INSPECTED`, `EXCLUDED`, or `BLOCKED`. No path may disappear from the ledger.
For unreadable files, binaries, or unresolved links, inspect at least the
type, target, and available metadata, then mark the impossible dimensions
`TO VERIFY`; do not skip them silently.

## 3. Inspection separated from the report

### Phase A — Build the rule model

After the inventory, establish a requirements matrix, without yet writing any
recommendation:

- `§2/§3`: object types and cognitive layers;
- `§4`: Single Source of Truth, duplication = defect;
- `§5`: minimal metadata;
- `§6`: sources before inclusion and recorded sources;
- `§7`: composition without duplication between layers;
- `§8`: deterministic generation and absence of hidden assumptions;
- `§9`: validation of executable artifacts and observable behavior;
- `§10`: evidence-based knowledge progression;
- `§11`: artifact independence and absence of hidden context;
- `§12`: versioning, migrations, and deprecation;
- `§13`: explicit relationships;
- `§14`: Quality Gates;
- `§15`: Definition of Done;
- `§16`: fundamental Kit principles;
- `§16.1` + Layer 5.1: verifiable governance constraints (relation
  resolvability, router as sole entry, category justification,
  absolute-instruction validation) and the structure.md project reading-map
  contract;
- any applicable zone contract in `.agent/kit-governance/`;
- any universal or specialized rule in `KitV2/rules/` applicable to the file.

Do not turn a style suggestion into a charter violation. Each subsequent
finding must point to the exact normative section or be labeled as an
off-charter observation.

### Phase B — Dynamic typing, file by file

For each path of the inventory, determine separately:

1. the role declared by its metadata or content;
2. the most defensible charter type among `Rule`, `Recipe`, `Pattern`,
   `Snippet`, `Template`, `Capability`, `Evaluation`, `Decision Record`,
   `Source`, `Memory`;
3. the possible supporting role (`manifest`, `index`, test, probe, tool,
   documentation, configuration);
4. the directory it actually belongs to;
5. the expected type and directory, if determinable.

Never infer a type only from the directory name. A Pi `category` or a file
name is not automatically the charter `kind`. If the type is absent, ambiguous,
or contradictory, mark `TO VERIFY` and explain which metadata or relations are
missing.

Also verify the structural mismatch:

- a file declares an unknown type or a type incompatible with its role;
- a reusable file has no attachment to a charter object;
- a charter layer seems absent from `KitV2/`, or is represented by another
  mechanism (manifest, graph, probe, tool) not documented;
- for every capability covered by a recipe AND a probe (e.g. desktop-app),
  check that a template roadmap line exists in `templates/TEMPLATES.md`; a
  capability covered everywhere except the template level, without roadmap
  recognition, is a named finding category of its own, not a generic case
  buried in the current wording (D-2026-08-05-14);
- a directory exists but mixes several responsibilities without an explicit
  boundary.

The absence of a directory bearing exactly the name of a type is not by
itself an error: report it as `CONFORM`, `NON CONFORM`, or `TO VERIFY`
according to the declared representation and the design evidence.

### Phase C — Per-file and per-relation checks

For each file, evaluate the following dimensions. Use `N/A (justified)` only
when a dimension is truly inapplicable.

#### C1. Charter and zone contract

Verify conformity to the relevant sections of `KIT_CHARTER.md` and to the
zone contract. Cite the precise section (`§4`, `§5`, etc.) and the contract
path. Do not replace the charter with an invented checklist.

#### C2. Metadata and attachment

For every reusable artifact, verify the presence and useful value of each §5
field:

```text
id, title, kind, version, status, owner, tags, go_version,
dependencies, last_verified
```

Also verify the explicit relations when the type requires them:
`depends_on`, `uses`, `implements`, `extends`, `references`, `requires`,
`supersedes`, `validated_by`, `generated_from`. Distinguish Pi metadata
needed for discovery (`name`, `description`, etc.) from the charter's
knowledge-graph metadata: one does not replace the other. Also verify §12:
version, deprecation status, documented migration for breaking changes, and
consistency of dependent evaluations.

#### C3. Sources and real freshness

Verify that sources are recorded in the artifact or in the canonical registry,
that they are primary or justified by the charter, and that the claimed
version/date matches the source. If network access is not possible, keep the
source and mark the freshness check `TO VERIFY`; do not rely only on the
`last_verified` field. Report missing, dead, non-canonical, vague URLs or
unsupported claims.

#### C4. Single Source of Truth and duplication

Search for:

- exact or near-exact duplicates between files;
- the same operational rule copied across several layers;
- a recipe that copies a pattern or snippet instead of composing it;
- catalogs, indexes, manifests, or READMEs that contradict the canonical
  body;
- a translation or second language version that repeats the same content
  instead of referencing it.

Vocabulary similarity is not enough: cite the passages that answer the same
question. If a duplication can be detected mechanically (hash, identical
block, repeated identifier), state it separately from semantic duplication
that requires human review.

Additionally, explicitly sample the pattern↔recipe↔snippet pointer chains
(D-2026-08-05-11): for each snippet, resolve `source:` (SNIPPET.yaml) to its
canonical artifact and compare the code shape; for each recipe, identify the
referenced patterns/snippets and verify that it composes them without copying
them. Chain drift (canonical modified, snippet not re-verified) is a finding
distinct from intra-target duplication — state for each chain whether it is
mechanically checkable by dates (`last_verified` dependent >= canonical) or
only by review.

#### C5. Independence and hidden dependencies

An agent loading a single artifact must be able to understand its use without
prior conversation or metaproject memory. Verify explicit dependencies,
resolvable cross-references, and the absence of hidden paths to `.agent/`,
`.pi/memory/`, `docs/`, or other unshipped files. A KitV2 file must not depend
on `../.agent` or a source available only in the metaproject. Declared
relations to missing, proposed, or inactive targets are distinct findings.

#### C6. Validation §9 and observable evidence

For recipes, snippets, templates, probes, tools, or any other executable
artifact, locate the commands, tests, scenarios, and acceptance criteria.
Verify that they cover the central behavior, important errors and, if
relevant, race/security/vulnerability checks. A green compilation or test does
not replace an observable scenario; unexecuted evidence is `TO VERIFY`, never
`CONFORM`. Run only commands that do not modify the repository and state
exactly what was or was not executed.

#### C7. Language and editorial coherence

**The repository's explicit policy (fundamental rule D-2026-08-05-21) is:
English is the mandatory language for every skill, instruction, and
document.** Determine the dominant language of each artifact family from the
actual content. Report:

- a language mix that makes the same instruction incoherent;
- a full translation of the same content in a single file or in two files;
- titles, metadata, and sections that change language without an explicit
  reason;
- a citation, identifier, API name, or source excerpt that is not a language
  violation.

French content in active instruction surfaces is `NON CONFORM` under the
explicit policy, except the historical memory records (`.pi/memory/` history)
which are grandfathered as a registry, not an instruction.

#### C8. Code examples and universal rules

For every Go block of a recipe, snippet, template, or probe, read the relevant
universal rules before concluding. In particular verify errors handled once,
context and cancellation, logging, boundary validation, consumer interfaces,
resource closure, concurrency, security, and validation commands. Cite the
rule file and the block line. If a check requires analysis that Markdown
reading does not allow, mark it `TO VERIFY` rather than inventing a verdict.

#### C9. Absolute instructions and mechanical gates

Inventory every absolute instruction in the Kit (`MANDATORY`, « always »,
« never ») in consumer artifacts (skills, prompts, AGENTS.md, recipes) and its
enforcement status: named mechanical control (validator C2, Pi gate) or
"guidance only, not enforced" recorded in the automation-gaps registry
(`.agent/instructions.md` §Enforcement). An absolute without control or
recording is a finding (D-2026-08-05-15) — evaluate not only the presence of
the phrase, but what enforces it.

#### C10. spec-driven-dev workflow (contract Z12)

Verify the `KitV2/.pi/skills/spec-driven-dev/` and `deep-discuss/` zones
against contract Z12:

- complete frontmatter (name == directory, category: workflow, English
  description, tags, last-verified), SKILL.md ≤ 500 lines, `references/**`
  present and relative links resolved;
- no GitHub leakage (no `github-integration.md`, no gh/Issue/PR reference in
  the skill) — LOCAL_ONLY mode (D-2026-08-05-18);
- S.U.P.E.R present as a health lens with the "sourced kit rules win"
  boundary (D-2026-08-05-16, Z12 §3.2);
- adaptive control (telemetry, drift, thresholds) and Phase 6 archive present;
- the memory rule "verify which .pi/memory files exist, Decisions.md may be
  missing" encoded (KitV2/AGENTS.md + workflow-memory.md);
- **no residual `workflow-{clarify,plan,tasks,implement,verify}` prompt**: a
  residual prompt from the former chain is a named finding category of its
  own (D-2026-08-05-16), not a generic case;
- `go-code-review` carries the findings-first discipline (targets, focus,
  format) without exceeding 500 lines;
- router indexed (skills spec-driven-dev, deep-discuss) and `--check` green.

#### C11. structure.md mechanism (Layer 5.1)

Verify that the structure.md contract is attached to the template machinery:
every sourced template (Z5) declares it in `template.yaml` or its README
(structure.md generation or validation), and `templates/TEMPLATES.md` or a
template-contract document records the mechanism — generation-first default,
drift gate, semantic exception per Layer 5.1. Absence of any conforming
declaration is `NON CONFORM` and drives the KitV2 implementation pass; no
resource may claim a generated project is complete without the mechanism
declared.

#### C12. Relation resolvability (§16.1.1)

Sample and verify every `related:`/`source:` declared between knowledge
layers: the target must exist and be neither proposed, missing, nor inactive.
The check must be tool-backed — validate-cognitive.py for graph relations and
statuses/targets, the snippet date-chain check (D-2026-08-06-03) for `source:`
chains, router index coverage. A relation verifiable only by prose is
`NON CONFORM`; a relation that fails to resolve is a finding (`KVA-###`).

#### C13. Router as sole entry (§16.1.2)

Verify that every resource in an indexable zone (rules/, recipes/, knowledge/,
snippets/, .pi/prompts/, .pi/skills/) appears in `router/index.json`
(coverage), that `build_index.py --check` is green, and that no parallel
hand-maintained discovery index exists anywhere in KitV2 (Z11). A
bypass — unindexed resource or parallel index — is a `NON CONFORM` finding.

#### C14. Category justification (§16.1.3)

Verify that every template/recipe category present in KitV2 carries documented
real usage — observed consumer demand or a real, maintained project, never
theoretical utility — recorded at admission (Z5 admission record; Z3 recipe
admission) in a machine-readable usage-evidence field. A category admitted
without usage evidence is a finding; absence of the field for a new category
is `NON CONFORM`.

#### C15. Absolute-instruction validation (§16.1.4)

Extends C9: every "always", "never", or "MANDATORY" in consumer instruction
surfaces (skills, prompts, AGENTS.md, recipes) must cite the named mechanical
validator that enforces it, or be recorded "guidance only, not enforced" in
`.agent/instructions.md` §Enforcement. An absolute without citation or
recording is `NON CONFORM` — the D-2026-08-05-15 obligation is normative.

#### C16. ui-kit zone integrity (contract Z13) — read-only, never syncs

The ui-kit zone is a pinned verbatim mirror of upstream ui-agent-kit `sdk/`.
The audit is non-destructive (safety contract) — it DETECTS drift and routes
to the manual update workflow; it never syncs, never rewrites `PIN.md`, never
touches the zone.

1. **Pin record**: `ui-kit/PIN.md` carries a well-formed 40-hex pinned SHA
   and a sync date (validator `check_ui_kit_pin` enforces this — cite it,
   do not rebuild it).
2. **Zone drift (local)**: `git status --porcelain -- KitV2/ui-kit` must be
   empty. A dirty zone is `NON CONFORM` (in-place edits or uncommitted
   syncs are forbidden by Z13 §3.1/§9). If clean, run
   `bash .agent/sync-ui-kit-from-upstream.sh --check` (read-only pin-vs-tree
   check) and report its output.
3. **Upstream drift (network, read-only)**: compare the pinned SHA to
   upstream HEAD via `git ls-remote https://github.com/TheophileBaudouin/ui-agent-kit HEAD`
   (do NOT clone). If HEAD differs from the pin, report the jump
   (`git ls-remote` output, upstream log since the pin via the GitHub API or
   a no-checkout clone is optional) as `TO VERIFY — update pending` and
   instruct: run the `.pi/prompts/update-ui-kit.md` workflow (manual, gated
   by `.agent/sync-ui-kit-from-upstream.sh <new-sha>`). The audit NEVER
   performs the sync itself.
4. **Registration integrity (single point)**: the root
   `KitV2/.pi/settings.json` must declare `../ui-kit/skills` (additive,
   keeping `../rules` + `../recipes`), and the zone must contain NO nested
   `ui-kit/.pi/settings.json` (dead by design, excluded from re-syncs —
   D-2026-08-08-02). A second registration source is `NON CONFORM`.
5. **Automated checks to cite, not rebuild**: `validate-kitv2.py`
   `check_ui_kit_skills` (frontmatter), `check_ui_kit_copy_rules` (rules
   point at existing zone folders), `check_ui_kit_pin`,
   `check_ui_corpus_disjointness` (Go index has no `ui-kit/` path),
   `check_ui_router_scenarios` (schema + id linkage, node-free); the
   metaproject gate `.agent/router/run_ui_scenarios.mjs` (ranking under the
   real scoring + reverse disjointness + tripwire) and
   `KitV2/probes/ui-kit-sync/` (Wails-only materialization + ownership
   contract). Absence of a green result for any of these is a finding.

#### C17. workspace-init zone integrity (contract Z14) — read-only, never initializes

The workspace-init zone governs the day-0 foundation protocol (`workspace/`
capture + AGENTS.md sections). The audit is non-destructive — it DETECTS
drift and routes to the skill; it never initializes a project, never rewrites
`KitV2/AGENTS.md`, never touches a consumer project.

1. **Kit pointer section**: `KitV2/AGENTS.md` carries the "Project
   Foundation" pointer section, delimited by its markers
   (`<!-- workspace-init section: begin -->` … `<!-- workspace-init
   section: end -->`) with the `## Project Foundation` title between them.
   The validator `check_workspace_init_placeholder` enforces this — cite
   it, do not rebuild it. A missing or altered section is `NON CONFORM`:
   two manual merge mechanisms live in this file (UI work and Project
   Foundation) and neither may silently swallow the other.
2. **Zone contract listed**: `.agent/kit-governance/README.md` lists the
   `24-zone-workspace-init.md` contract (Z14) in its index.
3. **Router indexing**: the router index contains the `workspace-init`
   skill entry (`.pi/skills/workspace-init/SKILL.md`, kind `skill`), and
   the routing-quality scenario "set up project foundation kernel modules
   before feature work" passes under the real scoring
   (`.agent/router/run_scenarios.mjs`).
4. **Automated checks to cite, not rebuild**: `validate-kitv2.py`
   `check_workspace_init_placeholder` (kit pointer section markers +
   title), `check_no_metaproject_paths` (the product never references the
   build repository — Z9 §3.2), plus the skill's frontmatter / size / prose
   gates (validate-instructions, validate-cognitive). Absence of a green
   result for any of these is a finding.

#### C18. Consumer onboarding system (docs + /goak + banner) — the embedded knowledge surface

The kit ships an onboarding/knowledge system for consumers: the user guide
`.pi/docs/GOAK.md`, the `/goak` entry point (`.pi/prompts/goak.md`), the
onboarding banner extension (`.pi/extensions/kit-onboarding.ts` +
`.pi/onboarding/banner.md`), and the "User guide" pointer section of
`KitV2/AGENTS.md`. It is shipped, self-contained, and enforced by the
product validator — the audit verifies consistency, not existence alone.

1. **Guide present and structured**: `.pi/docs/GOAK.md` exists and carries
   the Get Started level plus the deep-usage levels (Commands, Workflows,
   Kit structure, Troubleshooting). Every command, tool, and path it names
   exists in the shipped tree (cross-check `.pi/prompts/`, `.pi/skills/`,
   `rules/`, `recipes/`, `router/`); anything named but absent is a stale
   claim (`NON CONFORM`). The guide must stay usable with no external
   documentation and no build-repository references
   (`check_no_metaproject_paths` covers the latter).
2. **`/goak` correctness**: `.pi/prompts/goak.md` exists, has a
   `description`, and orders the agent to READ the local guide (mentions
   `.pi/docs/GOAK.md`) rather than answer from memory; it must not point at
   a renamed/stale path; it must end by inviting follow-up questions. It is
   router-indexed (C13) and passes validate-instructions (description
   gate).
3. **Banner extension**: `.pi/extensions/kit-onboarding.ts` exists, is
   project-local, subscribes to `session_start`, renders only for
   `reason: startup | reload`, guards on UI availability, and degrades
   silently when the banner file is missing (no network, no background
   process, no state). Its displayed content comes from
   `.pi/onboarding/banner.md` — content must stay out of code.
4. **Banner content**: `.pi/onboarding/banner.md` carries the three
   expected entries — Get Started, new large feature, new small feature —
   and their pointers are consistent with the real workflows (large →
   `spec-driven-dev` skill; small → direct routing + `.pi/` prompts/skills;
   orientation → `/goak`). A banner describing an obsolete workflow or a
   command that no longer exists is a finding.
5. **AGENTS.md pointer**: the "User guide" section, delimited by its
   markers (`<!-- user guide section: begin -->` … `<!-- user guide
   section: end -->`) with the `## User guide` title between them (N1
   §5.1, D-2026-08-08-17). The validator `check_consumer_onboarding`
   enforces this — cite it, do not rebuild it. Three manual merge
   mechanisms now live in this file (UI work, Project Foundation, User
   guide) and none may silently swallow another.
6. **Automated checks to cite, not rebuild**: `validate-kitv2.py`
   `check_consumer_onboarding` (guide sections, /goak local-path,
   banner three entries + /goak pointer, extension markers, AGENTS.md
   markers), `check_no_metaproject_paths`, `check_router` (goak.md
   indexed), validate-instructions (prompt description). Absence of a
   green result for any of these is a finding. The CONTENT-consistency
   part (banner ↔ real workflows, guide claims ↔ tree) is a review
   control; report it in Phase E.

### Phase D — Decide "metaproject or Kit?"

This dimension is mandatory for **every file**, including supporting files.
The metaproject creates, governs, audits, and evolves the Kit; the Kit is the
consumable product whose sole purpose is to help an agent generate clean Go
code and frictionless Go applications.

Classify each file according to the best-supported decision:

- `KIT — consumer-facing`: knowledge, capability, rule, recipe, snippet,
  template, embedded source, probe, or tool the consumer needs to use,
  verify, or maintain locally the installed product;
- `META-PROJECT — maintenance/governance`: charter, construction contract,
  metaproject memory, manufacturing decision, plan, research, evidence,
  working source registry, audit, creation/evolution workflow, metaproject
  validator, or maintenance prompt;
- `AMBIGUOUS — decision to take`: consumer and maintainer value not
  separated, or shared responsibility;
- `OUT OF SCOPE / EXCLUDED`: only with explicit reason and evidence.

Apply these tests, in order:

1. If the file disappears from the source repository but the installed Kit
   keeps the same consumer capability, it is probably metaproject.
2. If a consumer agent loaded only with the Kit must read or execute it to
   generate/validate Go, it is probably Kit.
3. A manufacturing, permanent-audit, historical-evidence, or governance file
   is not made product by the mere fact that it talks about `KitV2`.
4. `KitV2/probes/`, `KitV2/tools/offline/`, and `KitV2/.pi/` are not
   automatically pollution: measure their real consumer contract, autonomy,
   and presence in the installation.
5. Conversely, a maintenance file placed in `KitV2/` is potential pollution
   even if it compiles. Measure its consumer usefulness, context cost, and
   the risk of shipping the metaproject's history or control plane.

For every `META-PROJECT`, `AMBIGUOUS`, or `NON CONFORM` decision, provide the
boundary evidence: path, responsibility, intended consumer, and installer
inventory result. Never fix the move in this audit.

## 4. Coverage check and existing validators

After inspection only, reconcile the results. Produce these counts, without
rounding and without counting context files:

```text
found = audited + excluded_justified + blocked
```

- `found`: exact number of inventory paths;
- `audited`: every path that received a status per applicable dimension;
- `excluded_justified`: paths with explicit reason and category;
- `blocked`: paths unreadable or impossible to evaluate, with cause and next
  verification.

If the equation does not close, the workflow's global verdict is `FAIL —
INCOMPLETE COVERAGE`, even if the known findings seem minor. Report the
uninspected paths individually. A zone target must also state how many
context files were read but excluded from the calculation.

In a separate section, compare the observed checks with the two existing
validators:

- state precisely what `validate-instructions.py` already covers (Pi skill
  schema, relative links, size limit, absence of consumer memory, prompt
  descriptions);
- state precisely what `validate-cognitive.py` already covers (metadata and
  relations of supported YAML artifacts, statuses/targets, source units,
  metaproject path leakage, and offline bundle);
- state precisely what `validate-kitv2.py` already covers (product
  structure, router index + scenarios, ui-kit pin/copy-rules/corpus
  disjointness, the Z14 `check_workspace_init_placeholder` for the kit
  AGENTS.md Project Foundation section, and the product-autonomy
  `check_no_metaproject_paths` — Z9 §3.2);
- do not rebuild these checks in the report as if they were absent;
- report the real gaps: all uncovered file types, complete §5, semantic
  duplication, language, effective source freshness, composition,
  independence, and the metaproject/Kit decision;
- for each gap, recommend the best control level:
  `validate-instructions.py` for a deterministic Pi-format constraint,
  `validate-cognitive.py` for the graph/relations, a new deterministic
  validator for an independent structural property, or this agent/review
  workflow for a semantic property. Do not modify any validator.

Caution: do not automatically extend the published Pi schema with the
charter's §5 fields. If these contracts differ, recommend a separate check or
an explicit contract decision rather than a silent change.

## 5. Final report — after inspection only

The report is compact but complete. It must contain, in this order:

### A. Header

- `KitV2 Audit — <UTC date>`;
- exact target and argument;
- non-destructive status;
- observed commit/state if available;
- validator versions and commands actually run.

### B. Inventory and reconciliation

Give the inventory timestamp, the four numbers `found/audited/
excluded/blocked`, the equation, and the coverage verdict. Provide the
complete ledger or an exhaustive per-path table; one line may group several
files only if each file keeps a recoverable individual status and all paths
are enumerated. Context files are listed separately.

### C. Verdict per file and per dimension

Every file of the target must appear in a table or ledger with at least:

```text
path | role/kind | placement (KIT/META/AMBIGUOUS) |
charter | type/zone | metadata | sources/freshness |
SSOT/duplication | validation | independence |
language | code/rules coherence | confidence | risk | global verdict
```

Allowed values are `CONFORM`, `NON CONFORM`, `TO VERIFY`, or `N/A
(justified)`. For each `NON CONFORM` or `TO VERIFY`, reference a stable
finding and precise evidence. The global verdict cannot be `CONFORM` if an
applicable dimension is `NON CONFORM` or `TO VERIFY`.

### D. Classified findings

Number findings stably (`KVA-001`, `KVA-002`, …) and use the format:

```text
ID | category | risk | confidence | file/line | evidence |
KIT_CHARTER or contract section | impact | recommended action (without applying it)
```

Separate `risk` (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`) from `confidence`
(`HIGH`, `MEDIUM`, `LOW`). In particular use:

- `CRITICAL`: §4/§5/§6/§11/§14/§15 violation, metaproject control-plane
  leakage into the Kit, unverifiable essential source, or unclosed coverage;
- `HIGH`: inconsistent type or relation, missing essential metadata,
  executable artifact without validation, operational duplication;
- `MEDIUM`: language drift, freshness to confirm, index inconsistency, or
  applicable rule not proven;
- `LOW`: editorial improvement that changes neither capability nor
  traceability.

An unconfirmed hypothesis does not become a high-confidence finding. Group
identical findings but keep all affected paths.

### E. Automation gaps

Separate table: `dimension | already covered by | gap | recommended check |
reason`. Clearly state what must remain human or agentic semantic analysis and
what can become a repeatable Python assertion.

The table contains at minimum, at each audit:

- the "cross-file drift" row: pattern↔recipe↔snippet chains checkable by
  dates (`last_verified` dependent >= canonical) vs semantic review
  (D-2026-08-05-11);
- the "absolute instructions (MANDATORY)" row: every MANDATORY/"always"/
  "never" occurrence in the Kit and its enforcement status (named mechanical
  control or "guidance only" — D-2026-08-05-15);
- the "spec-driven-dev workflow (Z12)" row: zone conformity to contract
  Z12 — LOCAL_ONLY, S.U.P.E.R boundary, adaptive control, archive, memory
  rule, absence of residual workflow-* prompts (D-2026-08-05-16).
- the "structure.md mechanism (C11)" row: every sourced template and the
  template machinery declare the structure.md contract (template.yaml/README
  reference; TEMPLATES.md or template-contract.md documents generation-first
  default, drift gate, semantic exception) — currently a review control;
  recommended check: a deterministic validator assertion for the presence of
  the declaration, reason: the declaration is a stable structural property;
- the "relation resolvability (C12)" row: validate-cognitive.py covers graph
  relations and statuses/targets, the snippet date-chain check
  (D-2026-08-06-03) covers `source:` chains — the gap is cross-layer
  `related:` sampling left to review; recommended check: extend
  validate-cognitive.py with a deterministic cross-layer `related:` scan,
  reason: relations are graph properties a validator can assert;
- the "router coverage (C13)" row: already covered by `build_index.py --check`
  and the coverage check — the gap is "parallel index" detection (a second
  hand-maintained discovery index elsewhere in KitV2); recommended check: a
  deterministic scan of indexable zones for index-like files outside
  `router/`, reason: build_index cannot detect an index it does not build;
- the "absolute instructions (C15)" row: extends the MANDATORY row above — the
  gap is verifying that each cited validator actually exists and enforces the
  claim; recommended check: extend validate-instructions.py to resolve cited
  validator names against real validators/scripts, reason: §16.1.4 makes the
  citation obligation normative.
- the "category justification (C14)" row: no validator asserts the
  usage-evidence field today (§16.1.3) — the gap is presence-checking the
  machine-readable field at admission; recommended check: extend
  validate-kitv2.py with a presence assertion for the usage-evidence field on
  new template/recipe categories, reason: §16.1.3 makes the field normative
  at the first new category admission.
- the "ui-kit integrity (C16)" row: local pin-vs-tree drift is covered by
  `.agent/sync-ui-kit-from-upstream.sh --check` (metaproject script) and the
  product validator (`check_ui_kit_pin`, `check_ui_kit_copy_rules`,
  `check_ui_corpus_disjointness`, `check_ui_router_scenarios`) — the gaps are
  (1) upstream HEAD drift, inherently network-dependent and therefore a
  review control that routes to the manual `update-ui-kit.md` workflow, never
  a silent sync; (2) registration integrity (root settings.json declares
  `../ui-kit/skills`, no nested `ui-kit/.pi/settings.json`); recommended
  check: extend validate-kitv2.py with a settings.json assertion, reason:
  the single-registration-point rule (D-2026-08-08-02) is a stable
  structural property a validator can assert.
- the "workspace-init integrity (C17)" row: the kit pointer section is
  covered by `validate-kitv2.py` `check_workspace_init_placeholder`
  (markers + title); the gap is the CONSUMER-side capture (the per-project
  AGENTS.md section + sha256 marker written by the init session into a
  consumer project) — inherently a runtime artifact outside the kit, a
  review control only; the skill itself self-checks idempotence and
  no-content-loss by procedure (workspace-init SKILL.md §Before you begin /
  §AGENTS.md mechanics).
- the "consumer onboarding (C18)" row: structure is covered by
  `validate-kitv2.py` `check_consumer_onboarding` (guide sections, /goak
  local-path, banner three entries + /goak pointer, extension markers,
  AGENTS.md markers); the gap is CONTENT consistency — the banner's
  workflow pointers and the guide's named commands/paths must match the
  real tree (a renamed command, a removed workflow, a rewritten guide
  section) — inherently semantic, a review control at each kit-audit run;
  recommended check: none (no deterministic assertion can verify that the
  guide describes reality), reason: the mechanical gate guarantees shape,
  the review guarantees truth; the routing-quality scenarios act as a
  narrow tripwire for guide-related vocabulary.

### F. Verdict and next steps

End with:

- `Audit: PASS`, `PARTIAL`, `FAIL`, or `BLOCKED`;
- exact coverage and residual confidence;
- detected metaproject/Kit pollution, with count and paths;
- commands not executed and why;
- proposed next actions, without executing them.

`PASS` requires closed coverage, no unresolved critical/high finding, and no
applicable dimension `TO VERIFY`. An unavailable network source, an unexecuted
scenario, or an unreadable file forces at least `PARTIAL` or `BLOCKED`
depending on its importance.

## Final reminder

This workflow answers two different and mandatory questions:

1. **Is the file conformant to the charter and the applicable rules?**
2. **Does the file belong in the consumable product, or does it pollute
   KitV2 while belonging to the metaproject that builds and maintains it?**

Never merge these questions, never fix during the audit, and never present a
complacent summary in place of the coverage ledger.
