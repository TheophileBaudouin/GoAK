# Sourced Templates Wave Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remove inherited agent-authored legacy scaffolds and admit only real, MIT-licensed, pinned, tested, narrowly scoped Go project sources that satisfy Z5.

**Architecture:** The template catalog will contain only sourced project trees. Each admitted tree remains recognizable as the upstream project and receives only the required Kit metadata (`template.yaml`, `ATTRIBUTION.md`) plus documentation updates; no new application implementation will be authored. The validator will derive the template set from directories and enforce sourced-template required files without requiring the old scaffold filenames.

**Tech Stack:** Go source projects, GitHub-pinned MIT sources, YAML metadata, Python validator, Go test/race/vet/lint/security gates.

---

## Task 1: Replace the REST legacy scaffold with a sourced project

**Files:**

- Remove: `KitV2/templates/rest-api/` legacy scaffold
- Create: `KitV2/templates/rest-api/` from pinned `leeprovoost/go-rest-api-template` commit `4f2d17f700be3b355ff88986ca37c70ad2145cef`
- Create: `KitV2/templates/rest-api/ATTRIBUTION.md`
- Modify: `KitV2/templates/rest-api/template.yaml`
- Modify: `KitV2/templates/rest-api/README.md`

**Verification:** Run `go test ./...`, `go test -race ./...`, `go vet ./...`, `gofmt -l .`, and the observable HTTP health/hello scenario from the upstream README in a temporary copy. Record exact results in evidence.

### Task 2: Replace the worker legacy scaffold with a sourced project

**Files:**

- Remove: `KitV2/templates/worker/` legacy scaffold
- Create: `KitV2/templates/worker/` from the independently verified MIT source selected by the research report
- Create/modify: `LICENSE`, `ATTRIBUTION.md`, `README.md`, `template.yaml`

**Verification:** Run source tests, race tests, static checks, and a worker execution scenario. Reject the candidate instead of lowering Z5 if exact source/license/test evidence cannot be verified.

### Task 3: Replace the CLI legacy scaffold with a sourced project

**Files:**

- Remove: `KitV2/templates/cli/` legacy scaffold
- Create: `KitV2/templates/cli/` from the independently verified MIT source selected by the research report
- Create/modify: `LICENSE`, `ATTRIBUTION.md`, `README.md`, `template.yaml`

**Verification:** Run source tests, race tests, static checks, and a real CLI invocation against fixture input. Reject the candidate instead of lowering Z5 if source evidence is incomplete.

### Task 4: Retire shapes with no admitted source

**Files:**

- Remove: `KitV2/templates/grpc/`, `microservice/`, `monolith/`, `cloud-service/` if no candidate meets every Z5 hard criterion
- Modify: `KitV2/templates/TEMPLATES.md`
- Modify: `KitV2/templates/README.md`
- Modify: `KitV2/templates/template-contract.md`
- Modify: `KitV2/tools/validators/validate-kitv2.py`

**Verification:** The catalog has no `legacy` template directories; planned shapes are represented only in roadmap prose, and validator checks are derived from actual template directories.

### Task 5: Regenerate product indexes and run the full gate

**Files:**

- Modify generated router files through the repository's router generator
- Modify `KitV2/capabilities.yaml` only if coverage metadata is affected
- Create: `docs/evidence/2026-08-05/sourced-templates/` raw command results and source evidence

**Verification:** Run instruction validation, KitV2 validation, module verification, formatting, vet, lint, race tests, gosec, govulncheck, probes, and every admitted template scenario. Obtain a fresh-context read-only review before completion.
