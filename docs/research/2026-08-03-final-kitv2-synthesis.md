# Final KitV2 synthesis

## Status

Current metaproject reference after v1 retirement. Historical v1 artifacts were
removed once KitV2 had a standalone validator, module identity, probes, full
gate, external archive, and restore drill.

## Canonical surfaces

- Product: `KitV2/`
- Product context: `KitV2/AGENTS.md`
- Native Pi resources: `KitV2/.pi/`
- Product validator: `KitV2/tools/validators/validate-kitv2.py`
- Metaproject validator: `.agent/validators/validate-instructions.py`
- Metaproject memory: `.pi/memory/`
- Metaproject governance: `AGENTS.md`, `KIT_CHARTER.md`, `.agent/`
- Plans and evidence: `docs/plans/`, `docs/research/`, `docs/evidence/`

## Retired

The former `kit/` product and its v1-only validator, prompts, skills, rules,
recipes, probes, templates, adapters, and module files were retired after the
external archive and restore drill recorded in
`docs/evidence/2026-08-03/v1-deletion-archive.raw.txt`.

Historical v1 evidence was intentionally removed with the obsolete v1 product;
this workspace keeps only current KitV2 evidence and the archive record.

## Required gates

```sh
cd KitV2
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

A missing tool or unexecuted scenario is `PARTIAL`, never `PASS`.
