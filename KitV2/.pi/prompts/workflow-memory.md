---
description: Initialize and maintain consumer-project memory from scratch, without inheriting external history. Use at the start of a new project and after durable decisions, blockers, or verified milestones.
argument-hint: "[project state or event]"
---

# Memory — initialize locally, record only durable signal

## At project start

Note: `.pi/` resources (settings, prompts, skills) load only after the project
is trusted in Pi. In non-interactive sessions, approve for this run with
`pi --approve` (`-a`) when needed. Trust authorizes loading and executing
project resources; it is not a sandbox and grants no permission isolation.

1. Check whether `.pi/memory/` exists in the consumer project.
2. **Inventory the actual files present.** The native memory extension
   auto-bootstraps the five files (`Brief`, `Progress`, `Gotchas`,
   `Decisions`, `Agent`) on session start when missing and injects their
   full content once, on the first message. Verify which files actually
   exist before relying on them — never assume the standard set is
   complete.
3. Create any missing file via `/memory-init` (explicit initialization) or
   let the auto-bootstrap create it — never copy external history into the
   files. Nothing pre-existing is overwritten.
4. Read the local memory before acting. Never copy a pre-existing source
   ledger, roadmap, or research history into it.
5. Record the project's actual goal, stack, constraints, current progress, and
   known risks. Leave unknown details out until observed.

## What belongs in consumer memory

- `Brief`: stable architecture, public contracts, commands, and decisions that
  future sessions need (≤ 8 KiB).
- `Progress`: current tasks and verified milestones; keep incomplete work
  incomplete and include blockers (≤ 10 KiB).
- `Gotchas`: concrete mistakes, failures, and durable corrections discovered in
  this project (≤ 12 KiB).
- `Decisions`: durable architecture decisions and their rationale — ADR-lite
  entries, newest first (≤ 8 KiB).
- `Agent`: concise behavior rules explicitly established for this project
  (≤ 8 KiB).

## Writing rules

- Edit memory files directly with `edit`/`write`. Before editing any memory
  file, load the `memory-writing` skill — it holds the per-file format,
  style, and budget rules.
- Re-read on demand with `memory_read` — omit `file` to read all memory.
- When a file exceeds its size budget (alert injected at session start),
  run the `memory-refactor` skill: archive to
  `.pi/memory/archive/<file>-YYYY-MM-DD.md`, never delete to fit.

Use a decision/source ledger only when the project has enough research to need
one. Keep it local and cite URLs or commands for durable claims.

## What does not belong

Do not store conversation transcripts, temporary reasoning, raw tool output,
finished-task history, generic Go advice already present in the kit, or
secrets — in particular, never put secrets in `.pi/settings.json`.
Do not copy another project's memory into this consumer project.

## Source refresh

Refresh is explicit and atomic: re-verify every loaded source pin and
`last_verified` field before changing guidance. Update the manifest, source
ledger, and all referencing artifacts together; a partial refresh is a defect.
If a source is stale or unavailable, record `stale` or `blocked` and do not
silently reuse old content.

## Update rule

After each meaningful change, update only the affected memory file. Record:
what changed, why it is durable, and how it was verified. If nothing durable
changed, do not write a memory entry. If a file is over budget or duplicates
accumulate, run the `memory-refactor` skill (archive, never delete) instead
of ad-hoc trimming.

End with `Memory: initialized`, `Memory: updated`, or `Memory: unchanged`, plus
the files touched and any missing host-specific bootstrap capability.
