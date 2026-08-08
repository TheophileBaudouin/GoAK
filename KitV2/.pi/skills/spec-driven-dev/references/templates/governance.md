# Project Governance Templates

Templates for project-level instruction surfaces and memory surface resolution generated in Phase 4. Update existing files in place when they already exist. Prefer native memory `.pi/memory/`; create a repo-local fallback memory file only when the project already declares one or the user explicitly selects it.

---

## AGENTS.md (project)

```markdown
# Project Agent Instructions

## Scope

These instructions apply to the whole repository.

## Truth Sources

- `<path>` — <why this file is authoritative>
- `<path>` — <why this file is authoritative>

## Development Rules

- Follow the existing architecture and naming conventions.
- New features or behavior changes must add or update relevant automated
  tests.
- If no automated test surface exists, run the closest static/syntax
  validation and record the limitation.
- Record durable project facts, commands, invariants, and recurring gotchas
  in the resolved native memory surface (` .pi/memory/` ) when available.
- **Verify which memory files actually exist**: the native memory extension
  auto-bootstraps the five files (Brief, Progress, Gotchas, Decisions,
  Agent) when missing. Never assume the standard set is complete; create
  the missing files in the expected format, without copying any external
  history.
- Do not create a repo-local memory file unless the workflow explicitly
  records that fallback decision.
```

---

## Governance Surface Resolution

```markdown
# Governance Surface Resolution

## Instruction Surfaces

| Surface | Status | Role | Notes |
|:--------|:-------|:-----|:------|
| `AGENTS.md` | existing / created / unused | Shared agent rules | |
| `.cursor/rules/` | existing / absent / untouched | Cursor rules | |
| `.windsurf/` | existing / absent / untouched | Windsurf rules | |
| `.clinerules*` | existing / absent / untouched | Cline rules | |
| `.codex/` | existing / absent / untouched | Codex-specific project files | |

## Memory Surface

| Field | Value |
|:------|:------|
| Native memory available | yes / no |
| Resolved memory surface | `.pi/memory/` (files verified: Brief, Progress, Gotchas, Agent, Decisions — mark those absent) / existing file / explicit fallback / unavailable |
| Repo fallback approved | yes / no / not needed |
| Notes | how durable facts should be recorded |
```

---

## Optional Repo Fallback Memory File

Use this only when no native memory surface is available and the user explicitly selects a repo-local fallback.

```markdown
# Project Memory

This file stores durable project facts and decisions because no native
project memory surface was available or selected. It is not a progress log;
active workflow state belongs in `docs/progress/MASTER.md` during a
spec-driven run.

## Stable Project Facts

- <fact>

## Durable Engineering Rules

- <rule>

## Recurring Gotchas

- <gotcha and mitigation>
```
