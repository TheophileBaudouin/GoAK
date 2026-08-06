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
