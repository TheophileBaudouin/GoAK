---
description: Initialize and maintain consumer-project memory without inheriting kit or metaproject history. Use at the start of a new project and after durable decisions, blockers, or verified milestones.
argument-hint: "[project state or event]"
---

# Memory — initialize locally, record only durable signal

## At project start

Note: `.pi/` resources (settings, prompts, skills) load only after the project
is trusted in Pi. In non-interactive sessions, approve for this run with
`pi --approve` (`-a`) when needed. Trust authorizes loading and executing
project resources; it is not a sandbox and grants no permission isolation.

1. Check whether `.pi/memory/` exists in the consumer project.
2. If it does not exist, initialize the host's standard memory files before
   coding. If the host provides a memory bootstrap command, use it; otherwise
   create only the minimal files the host expects.
3. Read the local memory before acting. Never copy the kit's source ledger,
   roadmap, research history, or metaproject tasks into it.
4. Record the project's actual goal, stack, constraints, current progress, and
   known risks. Leave unknown details out until observed.

## What belongs in consumer memory

- `Brief`: stable architecture, public contracts, commands, and decisions that
  future sessions need.
- `Progress`: current tasks and verified milestones; keep incomplete work
  incomplete and include blockers.
- `Gotchas`: concrete mistakes, failures, and durable corrections discovered in
  this project.
- `Agent`: concise behavior rules explicitly established for this project.

Use a decision/source ledger only when the project has enough research to need
one. Keep it local and cite URLs or commands for durable claims.

## What does not belong

Do not store conversation transcripts, temporary reasoning, raw tool output,
finished-task history, generic Go advice already present in the kit, or
secrets — in particular, never put secrets in `.pi/settings.json`.
Do not copy the metaproject's `.pi/memory/` into a consumer project.

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
