# Z2 — Zone `knowledge/` (sourced decision graph)

- **Metaproject Contract** — governs `KitV2/knowledge/`.
- **Audit report:** §2.2, §2.3. **Decision:** vetted SKILL.md libraries + separate YAML pointers (2026-08-04).

## 1. Mission

The "why / when to choose" layer: the Kit's sourced decision graph. A knowledge artifact answers **one distinct question** that no rule or recipe covers, and cites its primary source. It is never the body of a rule/recipe (charter §4) nor metaproject memory.

## 2. Sub-domains and formats (choice rule)

| Sub-domain | Format | Typical content |
| --- | --- | --- |
| `patterns/` | graph-YAML | reusable solutions (positive schema) |
| `anti-patterns/` | graph-YAML | sourced failures (negative schema) |
| `stdlib/` | graph-YAML | **pointer-only** to official sources |
| `catalogs/libraries/` | **SKILL.md** (vetted, 9-criteria admission) + graph-YAML Level-B Source | admitted selection decisions; Level B = active conditional sources, not yet vetted |
| `catalogs/libraries/pointers/` | graph-YAML Source | `status: proposed` "consider" pointers (created 2026-08-05, 5 pointers) |
| `catalogs/reference-projects/` | SKILL.md | **extract-only** projects |
| `catalogs/*.yaml` (discovery) | graph-YAML Source | discovery indexes (awesome-go, …) |
| `security/`, `performance/`, `observability/`, `architecture/`, `debugging/` | graph-YAML | sourced domain guidance |

## 3. Mandatory schemas

**Pattern (positive)**: `problem` (context), `context` (when), `solution`, `benefits`, `costs`, `related` (+ referenced negative counterparts).

**Anti-pattern (negative)**: `symptom`, `detect` (actionable checks), `problem`, `fix`, `when_ok` (+ referenced positive counterpart when it exists).

**Source / pointer**: `source` (URL), `selection` (when to load), `limits` (what it does not prove), `relationships.references`.

## 4. Rules

1. Admission: primary source + distinct question + complete schema + resolved relations (C2).
2. Pattern/anti-pattern pairs reference each other (rule: every anti-pattern admits a positive counterpart when it exists).
3. **Pointer → vetted module promotion**: 9-criteria admission passed, real usage, verified maintenance, fresh `last_verified` — promotion is a written decision and moves the file to `catalogs/libraries/`.
4. `INDEX.md` is **supposed to be** generated (C2 compares to the tree — contracted C2 §2 check, generator pending); meanwhile, review control (Z2 §9.3) and no phantom domain.
5. An empty domain does not exist: either ≥ 1 active artifact, or a contract README + roadmap (`debugging/` — see §7).
6. `knowledge/` hosts neither metaproject history nor raw evidence.
7. **Catalog freshness**: any creation or update of a catalog module requires fresh web research on primary sources at writing time. Libraries are revalidated within 90 days; reference projects within 180 days. The file carries a `Sources vérifiées` section with real URLs and dates; a living URL alone does not prove the claim's validity.
8. **Internal single source**: a decision, limit, alert, or usage rule is written once per file. Sections are syntheses, not duplicative translations; an optional section is removed if it adds no information.
9. **Consistent examples**: every Go block presented as `Minimal use`, `Example`, or runnable handles its errors, resources, and cancellations according to the loaded rules. An abbreviated block is marked `illustrative` and does not claim to compile or prove behavior.

## 5. Patterns

- Pointer-only for massive official sources (stdlib): zero body copy, resolution via `tools/offline/`.
- Referenced pattern ↔ anti-pattern pairs (already in place — generalize).
- "One question, one artifact": detectable by C2 (search for duplicate titles/questions).

## 6. Anti-patterns

- Two formats for the same role without contract (the audit's `libraries/` case — decided 2026-08-04; migration in progress, see §4.3).
- "Useful" artifact without source; source without distinct question.
- Duplication of a recipe/rule body.
- Manual INDEX or counts.

## 7. `debugging/` (special case)

Domain contract already written in `KitV2/knowledge/debugging/README.md`: admission on observed and verified failure only, Source/Pattern schema, candidate roadmap (goroutine leak, flaky race, deadlock, slowness). The directory stays empty until evidence is admitted — it is a choice, not an accidental void.

## 8. Validation criteria

- [ ] C2: per-category schema verified (mandatory sections).
- [ ] C2: relations resolved; pairs referenced.
- [ ] C2: 12/18-month freshness; generated INDEX up to date.
- [ ] Pointer → module promotion: tracked written decision.

## 9. Graph completion pipeline (catalog library)

Trigger: a library admitted in `catalogs/libraries/` (or a promoted pointer) must be covered by the graph; any completion request follows this pipeline — **one library at a time, never in parallel**; a library is done only when the full pipeline is done.

### 9.1 Mandatory steps (in order)

1. **Analysis** — read the existing resource (catalog SKILL.md, linked artifacts); summarize role, features, ecosystem, use cases, pitfalls.
2. **Coverage audit** — compare existing graph coverage (grep of ids and questions per directory); list real gaps, incomplete, duplicates, obsolete.
3. **Documentary research** — by theme (security, performance, observability, architecture, patterns, anti-patterns, stdlib); primary sources only (official docs, spec, official issues, GHSA, CWE, OWASP); verify every added URL.
4. **User question** — only for an editorial decision not derivable from analysis/research; one question at a time; never a question whose answer is findable by analysis.
5. **Planning** — `docs/plans/<date>-<slug>.md`: files to create and modify, resources, dependencies.
6. **Splitting** — atomic, verifiable, independent micro-tasks (todo).
7. **Execution** — one fully finished library before the next; conformity and coherence verified after each artifact.
8. **Validation** — full gate (see 9.3).
9. **Report** — per library + global: files, research, decisions, questions, issues, remaining; raw evidence in `docs/evidence/<date>/<slug>/`.

### 9.2 Admission of a completion artifact (real gaps)

- **Admission C0 §4** (distinct question — no rule, recipe, pattern/anti-pattern, or catalog — and verified primary source, living URL); pipeline-specific: check the catalog Notes, which often cover a library's limits (review control).
- **Complete schema** of the category (Z2 §3) and Z10 metadata.
- **One question = one artifact**: unjustified volume is an admission failure, not an option.
- **`debugging/` stays empty** by contract (Z2 §7): a failure enters only observed, verified, with an actionable procedure.
- **Referenced pairs** when the counterpart exists (Z2 §4.2; corpus convention: the pattern points to its negative counterpart, the anti-pattern references its primary sources).
- **Admitted catalog = complete fiche**: every SKILL.md of `catalogs/libraries/` carries the 6 mandatory decision sections of the fiche format (N1 §4) before admission; preexisting sections (Selection, Admission, Minimal use, Alternatives, Notes) are kept.

### 9.3 Output checks (verifiable)

- [ ] C2: `validate-kitv2.py` PASS — metadata, resolved relations, router (per-category schemas and 12/18-month freshness: contracted checks, pending implementation).
- [ ] C2: router regenerated after any knowledge-YAML addition/removal (`python3 .agent/router/build_index.py --check` PASS).
- [ ] Review control: `knowledge/INDEX.md` up to date (generator pending, Z2 §4); zero phantom domain.
- [ ] Review control: no dead URL in `relationships.references` (spot-check of additions); no question duplication.
- [ ] Gate C0 §8: validators + Go gate + probes.

The write-gate C0 §4, the fresh-context review C0 §6.3, and the written decision (Decisions.md) apply without being duplicated here.

## 10. Open questions

- The 6 discovery YAMLs (awesome-go, go-by-example…) stay Source-YAML — confirmed by the decision (pointers).
- Should there be a real `cloud/` domain (INDEX mentions it)? As long as no cloud artifact is admitted, the domain does not exist (rule 5).
- Is the §9 pipeline automatically verifiable (a C2 "per-library completion" checklist) or does it remain a review control?
