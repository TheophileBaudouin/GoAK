# Z5 — Zone `templates/` (sourced MIT templates)

- **Metaproject Contract** — governs `KitV2/templates/`.
- **Audit report:** §2.6. **Owner directive (2026-08-04, major):** templates are **never written by an agent**; they are copies of real, reliable, functional open-source projects under MIT license, directly reusable with minimal documented adaptations.

## 1. Mission

Provide **reproducible, sourced project bases**: an agent or developer starts an application from a real, proven project, not a home-made skeleton. Quality comes from the community, not the agent.

## 2. Policy (absolute obligations)

1. **Never an agent-written template** from scratch. The agent documents, pins, minimally adapts, and verifies; it does not develop.
2. **MIT license mandatory** (fully open). A project under a restrictive license (GPL/AGPL, proprietary, "no commercial use") is rejected whatever its quality.
3. **Real, reliable source**: maintained project (recent commits/releases), tested, CI, active community, **single responsibility**, conformant to the kit rules (idiomatic, stdlib-first, no imposed framework).
4. **Ultra-specific and minimal** (high selection bar): the project implements **almost exclusively** the template's technology — one stack, one domain, no out-of-scope ancillary technology (auth, observability, K8s, ORM, heavy CI…). The codebase is **small and browsable end-to-end**: no mega-repo, no vendored/generated tree, no heavy dependencies. The structure is **clear, well-organized, and modular**: each component is isolated and replaceable, so integration into any project happens by copying well-delimited modules, and modification stays simple.
   **Real application mandatory (2026-08-05, D-2026-08-05-14)**: the source must be a real single-responsibility application, **not a third-party starter/template nor a collection of demonstration examples** — a repository named template/starter/example, or a demo collection, does not satisfy the policy even under MIT (lesson of the 2026-08-05 desktop-app research: no conforming Wails candidate).
5. **Functional mandatory**: compiles and passes its tests in the Kit. A non-functional template is forbidden, whatever the source.
6. **Directly reusable**: very few modifications to adopt; necessary modifications are simple and documented.
7. **Minimal documented adaptations**: every deviation from the source is listed in `ATTRIBUTION.md` with its reason.
8. **Fewer templates, very high quality**: there is no quantity goal; a shape without a sourced MIT template remains a roadmap.

## 3. Template structure

```text
templates/<shape>/
├── <source project>…     # pinned, functional project code
├── LICENSE              # MIT (copy of the project's license)
├── ATTRIBUTION.md       # source, pinned version (commit/release), license,
│                        # adaptations (diff + reasons)
├── README.md            # status, source, observable scenario, modifications,
│                        # project structure and justification (D-2026-08-05-13)
└── template.yaml        # name, status, purpose, source, validation
```

## 4. Statuses

| Status | Meaning | Entry condition |
| --- | --- | --- |
| `planned` | shape on roadmap, no template | decision + roadmap line |
| `sourced` | sourced MIT template, functional, verified | complete §2 policy |
| `legacy` | inherited agent-generated scaffold, replacement candidate | existing as of 2026-08-04; no new scaffold accepted |
| `deprecated` | removed or replaced | written decision + migration |

The current `legacy` scaffolds (rest-api, grpc, cli, worker, microservice, monolith, cloud-service) stay in place until replaced by a sourced template — they are **never** presented as policy-conformant templates.

## 5. Maintenance

- **Admission**: project identified (source + version) → MIT license verified → **technical scope verified** (one technology, no ancillary technology, browsable size — written evidence in `ATTRIBUTION.md`) → copy + LICENSE + ATTRIBUTION.md → minimal adaptations → compile + tests + executed observable scenario (`PASS`/`PARTIAL`/`BLOCKED`) → `sourced` status → update of `TEMPLATES.md` and the validator.
- **Update (community tracking)**: bump pinned version, re-verify the adaptations diff, re-run tests + scenario, bump `last_verified` — the update is an event, not an annual chore.
- **Removal**: written decision (abandoned project, changed license, degraded quality) + consumer migration.

## 6. Patterns

- ATTRIBUTION.md as the diff memory: "why this template differs from its source" — this is what makes adaptations simple to reproduce.
- Tracking the source's releases is the natural maintenance: the community improves, the Kit follows.

## 7. Anti-patterns

- Agent-written template (the legacy scaffolds case — accepted transitively, never admitted again).
- **Grab-bag template**: a broad stack (router + ORM + auth + K8s + CI…) instead of a single technology — rejected whatever the source project.
- Non-MIT license; unmaintained project; non-functional template.
- Clone without attribution or pinned version; undocumented adaptations.
- "Starter" template imposing an architecture (ardanlabs lesson: extract-only, never copied as-is).
- Shape placeholder without roadmap.

## 8. Validation criteria (C2)

- [ ] Every non-legacy template: `LICENSE` (MIT) + `ATTRIBUTION.md` (source, version, adaptations, **technical scope**) + `README.md` + `template.yaml` present.
- [ ] `ATTRIBUTION.md` attests a single technology and the absence of ancillary technology (review control; C2 verifies the section presence).
- [ ] Size bound respected (bounded source file/line count, no heavy vendored/generated tree) — C2.
- [ ] Compile + tests + traced observable scenario.
- [ ] `TEMPLATES.md` coherent with the tree (statuses up to date).
- [ ] No new scaffold (legacy status frozen at 2026-08-04).

## 9. Open questions

- Candidate sources for the 7 legacy shapes (research to launch: real, proven MIT Go REST/gRPC/CLI/worker/service/monolith/cloud projects).
- Should there be a type `ATTRIBUTION.md` template in the Kit (at `templates/` level)? (proposal: yes, in phase 3 at the first replacement.)
