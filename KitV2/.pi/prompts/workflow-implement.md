---
description: Execute an approved Go task list one task at a time with checks, evidence, and explicit stop conditions. Use only after workflow-clarify, workflow-plan, and workflow-tasks.
argument-hint: "[task artifact]"
---

# Implement — execute the approved scope

Before editing, confirm that the clarification, plan, and task artifacts exist,
are approved, and contain no unresolved blocker. If not, stop with `BLOCKED`.

For each task in dependency order:

1. Restate its Goal / Context / Constraints / Done when.
2. Read the relevant existing symbols before editing.
3. Make the smallest change; do not invent adjacent features.
4. Run the task's focused check immediately.
5. Record command, result, changed files, and remaining risk.
6. Change status from `PENDING` only with evidence; leave failures `PARTIAL` or
   `BLOCKED` and add a follow-up task rather than hiding them.

One writer owns a worktree. Parallelize only independent read-only research or
checks. After three identical failures, stop and report instead of looping.
Before completion, run the full mechanical gate and then `/workflow-verify`.

End with a handoff containing completed tasks, evidence, changed behavior,
failed or skipped checks, and the next action. Never report an unexecuted
scenario as passing.
