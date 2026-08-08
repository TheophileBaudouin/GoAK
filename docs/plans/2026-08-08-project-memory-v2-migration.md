# Plan — Project-memory v2 migration (2026-08-08)

## Goal

The user-level project-memory extension was rewritten (v1 → v2): the four
memory tools (`memory_read`/`memory_update`/`memory_refactor`/
`memory_bootstrap`) collapsed into ONE tool (`memory_read`, omit `file` =
all memory); writing is a direct `edit`/`write` under the `memory-writing`
skill; refactoring is the `memory-refactor` skill only; bootstrap is
automatic (five files — Brief/Progress/Gotchas/Decisions/Agent — plus
AGENTS.md, created when missing) with `/memory` and `/memory-init`.
Update every memory mention in this repository so no surface teaches the
removed v1 API or its stale premise ("Decisions.md is NOT created by the
bootstrap"), and add a deterministic gate that keeps it that way.

## Context

- Audit result: `memory_update` appears only in `.pi/memory/Gotchas.md` +
  `Progress.md` (dated historical records — kept as records per the
  memory-refactor contract). The stale v1 premise "Decisions.md is NOT
  created by default / may be missing from the Pi bootstrap" is the real
  drift, present in 10 instruction surfaces (metaproject + consumer kit).
- No `memory_read`, `memory_bootstrap`, `memory_refactor`,
  `PI_MEMORY_WIDGET`, or `memory_read all` mentions anywhere.
- The home `~/AGENTS.md` (outside this repo) still carries the v1 4-file
  template — out of scope, flagged to the user.

## Constraints

- English only (D-2026-08-05-21). No before/after noise in the kit.
- KitV2 shipped files must not contain metaproject markers
  (`check_no_metaproject_paths`: KIT_CHARTER, metaproject, D-20xx, KVA-,
  Z1x, KitV2/, .agent/).
- Historical dated records of v1 behavior stay untouched (memory-refactor
  contract: never rewrite dated history).
- The memory rule "verify which files exist" stays (defensive), only its
  bootstrap premise changes.

## Changes

### Metaproject instruction surfaces

1. `.pi/memory/Decisions.md` — new decision D-2026-08-08-22 (v2 doctrine,
   supersedes the D-2026-08-05-20 bootstrap premise).
2. `.agent/instructions.md` — §Enforcement row for workflow-memory: quote
   updated to the v2 doctrine, note extended (memory v2, 2026-08-08).
3. `.agent/kit-governance/22-zone-spec-driven-dev.md` — memory rule §5:
   auto-bootstrap premise.
4. `.pi/prompts/kit-audit.md` — C10 memory-rule bullet reworded; new
   dimension C19 (memory-system contract: no v1 residue + v2 facts);
   Phase E row; validate-kitv2.py coverage list mentions
   `check_memory_contract`.

### Consumer kit (KitV2) memory surfaces

1. `KitV2/AGENTS.md` — `## Memory` section: five files, once-per-session
   injection, `memory_read` (omit file), `memory-writing` skill,
   `memory-refactor` skill, `/memory-init`.
2. `KitV2/.pi/prompts/workflow-memory.md` — steps 1–3 + file list +
   writing-rules section rewritten to v2.
3. `KitV2/.pi/docs/GOAK.md` — "Memory is local and verified" bullet.
4. `KitV2/.pi/skills/spec-driven-dev/SKILL.md` (2 spots) +
   `references/behavioral-rules.md` (rule 14) +
   `references/templates/governance.md` + `references/templates/progress.md`.
5. `KitV2/.pi/skills/workspace-init/SKILL.md` — surface-inventory step.

### Deterministic gate

1. `KitV2/tools/validators/validate-kitv2.py` — new `check_memory_contract`:
    forbidden v1 tokens (memory_update, memory_bootstrap, memory_refactor
    tool, PI_MEMORY_WIDGET, "memory_read all", stale bootstrap premises)
    in shipped files (ui-kit mirror + checker/test exempt); required v2
    facts (five files, memory_read, memory-writing, memory-refactor) in
    AGENTS.md `## Memory` and workflow-memory.md. Wired into main().
2. `KitV2/tools/validators/test_validate_kitv2.py` — 5 tests (+/−).

### Memory records

1. `.pi/memory/Gotchas.md` — one new top entry (v1 tools gone, v2
    contract, gate name). `.pi/memory/Progress.md` — one completion entry.

## Done

- Full gate PASS: validators ×3 (kitv2 incl. new check + tests,
  instructions, cognitive), router scenarios + UI scenarios, gofmt/vet/
  lint/test-race/gosec/govulncheck, probes. Router index unchanged
  (frontmatter descriptions untouched — verify with `build_index --check`).
- Fresh-context review before declaring completion.
- Memory updated (Decisions D-2026-08-08-22, Progress, Gotchas).
