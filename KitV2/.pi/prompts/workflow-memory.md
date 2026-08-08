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
2. **Inventory the actual files present.** The Pi bootstrap initializes a
   minimal default set — `Decisions.md` is NOT created by default. List the
   real files under `.pi/memory/` (`Brief`, `Progress`, `Gotchas`, `Agent`,
   `Decisions`) and never assume the standard set is present.
3. Create the missing files in the host's expected format (use the host's
   memory bootstrap command when it provides one; otherwise create only the
   minimal files the host expects). Never copy external history into them.
4. Read the local memory before acting. Never copy a pre-existing source
   ledger, roadmap, or research history into it.
5. Record the project's actual goal, stack, constraints, current progress, and
   known risks. Leave unknown details out until observed.

## What belongs in consumer memory

- `Brief`: stable architecture, public contracts, commands, and decisions that
  future sessions need.
- `Progress`: current tasks and verified milestones; keep incomplete work
  incomplete and include blockers.
- `Gotchas`: concrete mistakes, failures, and durable corrections discovered in
  this project.
- `Agent`: concise behavior rules explicitly established for this project.
- `Decisions`: durable architecture decisions and their rationale — create it
  explicitly; the Pi bootstrap does not create it by default.

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
changed, do not write a memory entry. Compact duplicates periodically without
deleting unique tasks, gotchas, rules, or project context.

End with `Memory: initialized`, `Memory: updated`, or `Memory: unchanged`, plus
the files touched and any missing host-specific bootstrap capability.
