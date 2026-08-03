# Charter-aligned memory update

## Goal

Align root `.pi/memory/` with the current `KIT_CHARTER.md` after v1 retirement.
The memory must describe KitV2 as a typed knowledge graph, preserve durable
history without treating it as active instruction, and expose the exact gates
and ownership boundaries an agent must follow.

## Authoritative current state

- Product: `KitV2/` (`go-agent-kit-v2`, Go 1.25.6).
- Metaproject: root `AGENTS.md`, `KIT_CHARTER.md`, `.agent/`, `.pi/memory/`,
  `docs/`, and `.github/`.
- Product validator: `KitV2/tools/validators/validate-kitv2.py`.
- Metaproject validator: `.agent/validators/validate-instructions.py`.
- Product Pi resources: `KitV2/AGENTS.md`, `KitV2/.pi/settings.json`,
  `KitV2/.pi/prompts/`, and `KitV2/.pi/skills/`.
- Former v1 product: deleted; external archive is the only rollback referent.

## Charter-derived operational contract

Memory is updated to reflect the charter's typed artifact kinds, required
metadata, explicit relationships, composition hierarchy, evidence lifecycle,
progressive knowledge lifecycle, deterministic gate, and Definition of Done.
Historical v1 references remain only where they explain a recorded failure or
migration decision; they are not active paths or commands.

## Validation

- `python3 .agent/validators/validate-instructions.py`
- `cd KitV2 && python3 tools/validators/validate-kitv2.py`
- `cd KitV2 && go mod tidy && go mod verify`
- `cd KitV2 && test -z "$(gofmt -l .)" && go vet ./...`
- `cd KitV2 && golangci-lint run ./... && go test -race ./...`
- `cd KitV2 && gosec ./... && govulncheck ./... && bash probes/run.sh`
- fresh-context review of memory against the complete charter
