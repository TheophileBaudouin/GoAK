# Agent.md — Go Agent Development Kit metaproject

These are durable operating rules for work governed by `KIT_CHARTER.md`.
The charter is the authority; this file is only the compact agent-facing
summary. The standalone product is `KitV2/`.

## Prime directive

- I reduce agent decisions without turning the kit into a framework.
- I treat the kit as a typed knowledge graph, not as a folder of snippets.
- I prefer evidence, explicit relationships, deterministic behavior, and
  observable validation over intuition or volume.

## Ownership

- `AGENTS.md` and `KIT_CHARTER.md` govern the metaproject.
- Root `.pi/memory/` is metaproject memory; `.agent/` is metaproject control.
- `KitV2/` is the only consumable product. It may ship `AGENTS.md` and native
  `.pi/` resources, but never metaproject memory, decisions, or evaluations.
- The future `gak` CLI is the canonical distribution boundary. Do not create a
  second consumer `.agent/` runtime: install `.pi/` and selected agent adapters;
  keep root `.agent/` metaproject-only.
- `docs/` stores plans, research, and raw evidence; raw output never belongs in
  memory.

## Zone contracts (obligatoire)

- Avant toute édition dans `KitV2/<zone>`, lire le contrat de cette zone dans
  `.agent/kit-governance/` (index : `README.md`) et l'appliquer.
- Zone sans contrat → écrire ou auditer son contrat avant d'éditer ; ne jamais
  éditer une zone sans contrat.
- Toute règle nouvelle d'un contrat doit être vérifiable par le validateur
  produit (C2) ou un contrôle de revue ; une règle non vérifiable est une
  hypothèse, pas un contrat.

## Artifact contract

- Artifact kinds are: Rule, Recipe, Pattern, Snippet, Template, Capability,
  Evaluation, Decision Record, Source, and Memory.
- Every reusable artifact needs a stable `id`, `title`, `kind`, `version`,
  `status`, `owner`, `tags`, `go_version`, `dependencies`, and
  `last_verified`, plus explicit relationships where applicable.
- Relationships are declared (`depends_on`, `uses`, `implements`, `references`,
  `requires`, `supersedes`, `validated_by`, `generated_from`); folder names are
  navigation, not the authority.
- One artifact has one responsibility and one canonical body. Cross-reference;
  never duplicate knowledge across layers.

## Evidence-first workflow

For non-trivial work I:

1. create atomic todo tasks;
2. inspect the current graph and relevant artifacts;
3. research official or maintained primary sources;
4. record a plan and decision boundary;
5. keep one writer for a worktree;
6. obtain a fresh-context review;
7. run the applicable structural, mechanical, and observable gates;
8. record only durable status, decisions, gotchas, and evidence pointers.

The knowledge lifecycle is: Problem → Research → Decision → Pattern → Snippet
→ Recipe → Template → Evaluation. Do not skip evidence or silently promote a
hypothesis into an operational rule.

## Library knowledge pipeline

For any catalog library (admission, knowledge completion, or future library
analysis), I run the Z2 §9 pipeline exactly, one library at a time and never
in parallel:

1. Analyse (rôle, écosystème, cas d'usage, pièges) ;
2. Audit de couverture du graphe (grep ids + questions, manques réels) ;
3. Recherche par sources primaires uniquement (docs officielles, spec,
   issues officielles, GHSA/CWE/OWASP), URL vérifiées ;
4. Question utilisateur seulement pour une décision éditoriale non dérivable ;
5. Plan dans docs/plans/ ;
6. Découpage en micro-tâches atomiques ;
7. Exécution — une bibliothèque entièrement finie avant la suivante ;
8. Validation — gate complète + router régénéré + INDEX à jour ;
9. Rapport par bibliothèque + global, évidence brute dans docs/evidence/.

I create exactly one artifact per distinct question — never padding (the
catalog Notes often already cover a library's limits: check them before
writing). `debugging/` stays empty by contract (Z2 §7) unless the failure is
observed, verified, and has an actionable procedure. Every new YAML knowledge
file requires regenerating the router index before the gate passes.

Every catalog library carries the canonical **fiche format** in its SKILL.md
(N1 §4): the six mandatory decision sections (`Utiliser cette librairie
quand`, `Ne pas utiliser cette librairie quand`, `Avantages`, `Inconvénients`,
`Pièges connus`, `Sources vérifiées`), appended after the existing sections;
negative claims are confirmed by ≥2 sources or official issues; the fiche
lives in the SKILL.md body, never in a companion .md (declared Pi skill dirs
reject non-SKILL.md files).

## Validation gate

From `KitV2/` run:

```sh
python3 ../.agent/validators/validate-instructions.py
python3 tools/validators/validate-kitv2.py
go mod tidy && go mod verify
test -z "$(gofmt -l .)"
go vet ./...
golangci-lint run ./...
go test -race ./...
gosec ./...
govulncheck ./...
bash probes/run.sh
```

Also run affected template and snippet checks. Mechanical checks, evaluation
criteria, and user-observable behavior are reported separately. A missing tool,
unrun scenario, incomplete metadata, or missing relationship is `PARTIAL` or
`BLOCKED`, never `PASS`.

## Language (fundamental rule, 2026-08-05, D-2026-08-05-21)

- **English is the mandatory language for every skill, instruction, and
  document in this repository** (kit and metaproject): skills, prompts,
  contracts, plans, research, decisions, and all other written artifacts.
  One unique language across the whole project. This rule supersedes the
  earlier French-body decision (D-2026-08-05-17).
- Any translation must preserve technical terms, the original intention, and
  never transform or reformulate a statement: a translation is faithful to
  the original meaning and as close to it as possible.
- Ids stay ASCII kebab-case (unchanged); code, commands, and technical
  identifiers are never translated.
- This is a fundamental project rule — treat it as absolute.

## Boundaries

- Ask before changing the charter, a published metadata contract, dependencies,
  artifact kinds, or evaluation/probe contracts.
- Never claim a generated template is production-ready without reproducible
  validation and observable evidence.
- Never store secrets, consumer history, transcripts, or raw command output in
  the product or metaproject memory.

## Router & scoring maintenance (metaproject-owned, D-2026-08-06-11)

- The router system has ONE scoring implementation: `.pi/extensions/kit-resource-router-scoring.ts`. I never re-implement scoring in a test language (Python port, duplicate TS); I extend the shared module and re-run the gate.
- The routing-quality contract `router/scenarios.json` is maintained through the metaproject gate (`.agent/router/run_scenarios.mjs`, Node ≥ 23.6): every new scenario is a realistic agent intent, targets an existing indexed id, and MUST be able to fail — decorative expectations are not admitted.
- The gate's tripwire is proven: negative tests assert exit 1 on an unreachable expectation and on a stale id. When I add or re-tag a knowledge artifact, I re-run the gate and check that existing scenarios still pass (a silent ranking shift is a routing regression, not a cosmetic change).
- Two-layer verification: the product validator (node-free) checks scenarios schema + id linkage; the metaproject gate checks ranking under the real scoring. I never move the ranking check into the product validator (node dependency) and never move the contract file out of the product.
- Ownership boundary: builder, gate runner, and router tests live in `.agent/router/`; the product ships index/meta/scenarios + the runtime tool only. Consumers never rebuild or re-gate.
- Domain rejection (off-domain) is computed from the user's RAW query vocabulary, never from synonym-expanded tokens (a recall expansion with zero corpus coverage must not flip an in-domain query off-domain — D-2026-08-08). After any upstream content wave, re-verify that the new vocabulary is actually indexable (term-coverage grep on the built index) — existing scenario suites are narrow tripwires, not coverage proof.

## External content registration (D-2026-08-08)

- Copying a folder that carries its own AGENTS.md and its own `.pi/` does
  NOT integrate it: Pi performs no automatic discovery by directory — a
  skills folder is only loaded when an already-loaded `.pi/settings.json`
  references it.
- Every integration of external content (SDK, kit zone, skill pack) must
  include an explicit registration step — skills config entry
  (`.pi/settings.json`), AGENTS.md pointer section, router entry/tool — and
  that registration must be verified concretely afterwards (validator
  check, runtime discovery smoke, router query), never assumed.
- One registration point per concern: the root `.pi/settings.json` is the
  single skill registration point; a nested settings file that duplicates
  it is dead and must be deleted + excluded from syncs so it is never
  resurrected or mistaken for the source of truth.

## Consumer documentation & onboarding maintenance (D-2026-08-08-14..17)

- The consumer kit ships an embedded onboarding/knowledge system: the user
  guide `KitV2/.pi/docs/GOAK.md`, the `/goak` entry point
  (`KitV2/.pi/prompts/goak.md`), the onboarding banner
  (`KitV2/.pi/extensions/kit-onboarding.ts` + `.pi/onboarding/banner.md`),
  and the marker-delimited "User guide" section of `KitV2/AGENTS.md`.
  These are PART OF THE PRODUCT, shipped with every install, and verified by
  `validate-kitv2.py check_consumer_onboarding` + `kit audit` C18. The guide
  is the shipped source of truth: it must stay usable with no metaproject
  documentation and never reference the build repository.
- **Documentation review is a mandatory step of every consumer-kit change.**
  Before modifying: identify whether the change affects the guide, `/goak`,
  the banner, or the audit. During: update the affected surface in the same
  change. After: verify consistency (code ↔ guide ↔ banner ↔ `/goak` ↔
  `kit audit`) and run the validator. Never ship a kit change that documents
  a nonexistent command, omits an existing command, or describes a workflow
  that no longer matches the tree.
- The banner stays orientation-only (Get Started / large feature / small
  feature) and is never a second documentation; `/goak` stays a small
  pointer that forces reading the guide; the guide is the detailed source.
  Information lives once: code = behavior, guide = explanation, `/goak` =
  access point, banner = immediate orientation, audit = consistency check.
- Any new surface that merges content into `KitV2/AGENTS.md` MUST use
  begin/end markers + a dedicated mechanical check (N1 §5.1, D-2026-08-08-12)
  — today: UI work (sha256), Project Foundation, User guide.

## Sub-agent delegation (pi-subagents only, owner rule 2026-08-08)

- I delegate every task to a sub-agent EXCLUSIVELY through the pi-subagents
  skill — its documented workflows and the `subagent` tool (workflowScript,
  `runs.run` / `runs.all`). I never use intercom, the supervisor channel, or
  any other mechanism to delegate a task to a sub-agent.
- **Delegation is the DEFAULT for context-heavy, parallelizable, or
  read-only exploration work — not an exception.** I actively spawn
  pi-subagents to save time and context instead of doing the work inline:
  - `researcher` (builtin) — autonomous web research (searches, evaluates,
    synthesizes a focused brief): use for any web-research task instead of
    multi-round `web_search` in the main context;
  - `scout` (builtin) — fast codebase recon returning compressed context:
    use to explore an unknown area before touching it;
  - `reviewer` (builtin) — fresh-context review of diffs/plans (the
    agent-instructions skill: review in fresh context, not self-review);
  - `oracle` / `worker` for decision-consistency and implementation when an
    isolated context helps.
  These run **in parallel on independent tasks** (`runs.all`) — multi-query
  research, multi-area recon, independent reviews. Parallelism applies to
  read-and-report work; code WRITES stay on one thread (writer-on-one-thread
  principle, agent-instructions skill).
- EXCEPTION: real Pi session smoke tests (`pi -p -a` headless runs from a
  temp consumer copy) are NOT task delegation — they are environment tests
  inside a real Pi session and remain allowed.
- Any instruction that seems to delegate work but bypasses pi-subagents is a
  signal to stop and re-read this rule before acting.

## Merged agent files never lose instructions (owner rule 2026-08-08)

- The root `KitV2/AGENTS.md` is the single agent file for the kit: it MERGES
  the pinned `ui-kit/AGENTS.md` instructions into its "UI work" section
  (adapted, not deformed; every instruction from both files preserved — no
  instruction may be dropped during a merge).
- The section carries a checksum marker
  (`<!-- ui-kit/AGENTS.md sha256: <64-hex> -->`); at every ui-kit re-sync,
  the helper `.agent/sync-ui-kit-from-upstream.sh` refuses to finish when the
  marker drifts — the merged prose must be updated to mirror the new SDK
  AGENTS.md AND the marker refreshed before the sync can complete (Z13 §4,
  update-ui-kit prompt). Never ship a sync with a stale merged section.
- Writing instruction files for this repository follows the
  `agent-instructions` skill: dense, non-redundant, adapted to the kit's
  reality (the ui-kit zone is a pinned mirror, activation is conditional on
  a detected Wails project).
