# Z3 — Zone `recipes/` (runnable recipes)

- **Metaproject Contract** — governs `KitV2/recipes/`.
- **Audit report:** §2.4. **Decision:** single Go module (2026-08-04).

## 1. Mission

The "how to execute this task" layer: **ordered, runnable, tested** procedures. A recipe answers "how to do X properly in Go" and ends with an **executed observable scenario** — never a mere compilation.

## 2. Recipe structure

```text
recipe-<domain>-<subject>/
├── SKILL.md          # Pi frontmatter + body (progressive disclosure)
├── <code>.go         # importable package (module go-agent-kit-v2)
├── <code>_test.go    # targeted tests
└── (possible files: schema.sql, sqlc.yaml…)
```

## 3. Mandatory SKILL.md body (model: `recipe-worker-pool`)

1. **Problem** — the task in one sentence.
2. **Solution** — minimal working code (stdlib or vetted library).
3. **Why not the alternatives** — at least two rejected alternatives with verdict (including stdlib when it suffices).
4. **Verify the behavior (observable)** — command to run, expected outputs, what the observation proves.
5. **Run the tests** — the test command; the test does not replace the scenario.
6. **Limits** — scope boundary.
7. **Sources** — primary.
8. **Structure (why this layout)** — mandatory for every recipe that produces or recommends a project layout (application creation, service, CLI, worker, desktop…): explain in a few lines why the chosen tree is right for this task, so the reason always lives in the same place (owner decision 2026-08-05, D-2026-08-05-13). Recipes with no layout involved mark it `N/A` (an explicit `N/A` is content, not an artificial section — A1 §1.9). Review control: kit-audit C1 (zone-contract conformity) + criterion Z3 §8.

## 4. Rules

1. **No placeholder**: a planned recipe is a roadmap line in `recipes/README.md` (with criteria), not a `.gitkeep` directory.
2. Naming: `recipe-<domain>-<subject>`, ASCII kebab-case (N1). The interactive recipe is published as `recipe-cli-interactive` since the 2026-08-05 post-audit correction.
3. Every dependency used by a recipe must be **vetted** in `catalogs/libraries/` (9-criteria admission) — C2 verifies the correspondence.
4. A recipe references the patterns/snippets it uses (`uses`) and its library; it does not duplicate their code.
5. Recipes live in the single module `go-agent-kit-v2` (decision 2026-08-04); an isolated-module recipe requires a written decision (heavy dependency).
6. Every "core" recipe is exercised by a probe (`probes/`) — `validated_by` relation (Z6).

## 5. Maintenance

- **Addition**: compiling code + test + executed scenario with verdict (`PASS`/`PARTIAL`/`BLOCKED`) + limits + sources + resolved relations.
- **Modification**: re-run test + scenario; re-run the probes that import the recipe; bump `last_verified`/`version` if behavior changed; re-verify the declared dependents (snippets `source:` → recipe, probes `validated_by` → recipe) and bump their `last_verified` in the same change — cross-file C2 check (D-2026-08-05-11).

## 6. Patterns

- "Verify the behavior": the scenario is the proof, not compilation.
- Recipe ↔ probe: composition (the probe imports the recipe), not duplication.
- Stdlib first: the "why not" section eliminates frameworks when stdlib suffices.

## 7. Anti-patterns

- Recipe written without being executed; verdict asserted without execution.
- Recipe duplicating another or a snippet.
- Unvetted dependency; framework chosen for comfort.
- Empty placeholder waiting.

## 8. Validation criteria

- [ ] C2: complete SKILL.md (Problem, Solution, alternatives, scenario, limits, sources) and ≤ 500 lines.
- [ ] C2: targeted `go test` + executed scenario traced (explicit verdict).
- [ ] C2: dependencies ⊆ vetted libraries.
- [ ] Freshness 12/18 months.
- [ ] Reviewed (kit-audit C1): Structure section §3.8 present or `N/A` justified (D-2026-08-05-13).

## 9. Open questions

- Should there be "shape recipes" distinct from task recipes? (today the sourced MIT templates will take this role — see Z5.)
- The rename `recipe-cli-interactif` → `recipe-cli-interactive` was done on 2026-08-05; product references and the router are aligned.
