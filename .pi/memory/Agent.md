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

## Boundaries

- Ask before changing the charter, a published metadata contract, dependencies,
  artifact kinds, or evaluation/probe contracts.
- Never claim a generated template is production-ready without reproducible
  validation and observable evidence.
- Never store secrets, consumer history, transcripts, or raw command output in
  the product or metaproject memory.
