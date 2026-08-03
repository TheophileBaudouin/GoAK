# Kit v1 deletion plan

## Status

Approved by the owner for execution, but implementation is not started. The
plan is intentionally atomic because the workspace has no Git repository.

## Goal

Delete the obsolete `kit/` v1 product, retain the root metaproject and make
`KitV2/` the only consumable kit. Remove all runtime and instruction references
to v1 while preserving historical evidence as historical evidence.

## Hard safety rule

Never delete `kit/` until every preceding phase is green. If any checkpoint
fails, stop with `kit/` intact.

## Phase 0 — authorization and archive

1. Record explicit deletion approval in `.pi/memory/Decisions.md`, including
   the no-VCS rollback waiver and archive requirement.
2. Freeze `kit/`: no edits after this point.
3. Create an archive outside this workspace containing the entire `kit/` tree.
4. Generate a SHA-256 manifest and verify the archive with `tar -tzf`, extract it
   into a temporary directory, and run the v1 validator from the extraction.
5. Record archive path, checksum, restore-drill output, and environment under
   `docs/evidence/2026-08-03/v1-deletion/`.

## Phase 1 — make KitV2 self-contained

1. Move the instruction validator out of v1 into a metaproject-owned path, for
   example `.agent/validators/validate-instructions.py`, and update its root
   calculation and all references.
2. Rewrite `KitV2/tools/validators/validate-kitv2.py` to stop reading `../kit`. It must
   validate KitV2 directly and must fail loudly if a deprecated v1 path is
   supplied or referenced; it must never silently pass with zero migration
   coverage.
3. Add a negative validator check proving that no `kit/` runtime dependency is
   required after deletion.
4. Run the validator and its negative case before touching `kit/`.

## Phase 2 — repoint the metaproject and product

1. Update root `AGENTS.md` to name KitV2 as the only product and run all gates
   from `KitV2/`.
2. Update `KIT_CHARTER.md` paths and approval language from v1 locations to
   KitV2 locations.
3. Update `.agent/instructions.md`, `.agent/capabilities.yaml`, and
   `.agent/evaluations/README.md` to remove `kit/` product references.
4. Reconcile `.pi/memory/{Brief,Progress,Agent,Decisions,Gotchas}.md`:
   remove v1 operational instructions, preserve historical facts only when
   explicitly labelled archival, and point all active commands to KitV2.
5. Update `KitV2/AGENTS.md`, `manifest.yaml`, and `capabilities.yaml` to remove
   v1 backup/migration-era claims and make the module identity final.
6. Update KitV2 validation skill references from `kit/.golangci.yml` to
   `KitV2/.golangci.yml` and consumer memory prompts to current KitV2 paths.

## Phase 3 — CI and dependency configuration

1. Change `.github/workflows/ci.yml` to use `KitV2/` as working directory and
   `KitV2/go.mod` as its Go version file.
2. Change `.github/dependabot.yml` from `/kit` to `/KitV2`.
3. Run the full KitV2 gate, including the 70% coverage floor.
4. Stop if any gate fails; v1 remains intact until fixed.

## Phase 4 — content reconciliation

Before deletion, produce a checklist proving that every v1-only asset is either
replaced or intentionally retired:

- v1 README → KitV2 README or explicit documented retirement;
- v1 validator → metaproject validator;
- v1 CI/skill-authoring templates → KitV2 equivalents;
- v1 adapters → explicitly deferred and archived, not silently lost;
- v1 empty patterns/checklists directories → intentionally absent in KitV2;
- v1 prompts, skills, recipes, rules, libraries, reference projects, probes →
  KitV2 equivalents verified by the current validator.

## Phase 5 — deletion and post-delete verification

1. Re-run the archive checksum and restore drill.
2. Re-run the full KitV2 gate and all probes immediately before deletion.
3. Delete only `kit/`.
4. Re-run the KitV2 validator, negative runtime-reference test, full gate, all
   probes, template checks, and Pi smoke test.
5. Search active files (excluding historical evidence and this plan) for
   dangling `kit/`, `kit/.pi`, `kit/core`, `kit/probes`, and `../kit` references.
6. Verify root metaproject files and KitV2 are the only product surfaces.
7. Record complete raw output under `docs/evidence/2026-08-03/v1-deletion/`.

## Retention policy

Retain historical `docs/evidence/`, plans, research, and the archive reference.
Historical records may mention v1 paths, but active instructions, validators,
CI, manifests, and memory must not direct runtime behavior to deleted v1.

## Stop conditions

Stop and keep `kit/` if:

- archive creation, checksum, or restore drill fails;
- any KitV2 gate, probe, validator, or negative test fails;
- any active runtime reference to v1 remains unresolved;
- the CI/dependabot rewrite is not syntactically valid;
- a required v1 asset has no explicit keep/retire decision;
- deletion would require an unapproved public-contract change.

## Done when

- `kit/` does not exist;
- KitV2 is self-contained and independently validated;
- root metaproject harness points only to KitV2;
- historical evidence is retained and labelled;
- no active v1 references remain;
- fresh review reports no blockers;
- residual risks are recorded, especially no VCS and archive-only rollback.
