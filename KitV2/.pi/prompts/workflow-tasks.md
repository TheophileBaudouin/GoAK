---
description: Decompose an approved Go plan into short dependency-ordered tasks with default-fail acceptance and checks. Use only after workflow-plan.
argument-hint: "[approved plan]"
---

# Tasks — make progress measurable

Do not create or modify application code. Read the approved plan and preserve its
scope. If the plan is missing or ambiguous, stop with `BLOCKED`.

For each task, record:

- stable ID and one outcome;
- exact files or user-visible surface;
- dependencies and whether parallel work is safe;
- a focused mechanical check;
- an observable acceptance check where relevant;
- status, initialized as `PENDING`.

Put the smallest behavior probe or failing check before implementation when
practical. Keep tasks small enough to complete and verify independently. Do not
mark a task `PASS` because code exists; require command output, captured state,
or a reviewer verdict. Add final tasks for the complete mechanical gate and the
user-observable scenario. Add a gap task instead of deleting a failed task.

End with a numbered task list ready for `/workflow-implement`, followed by the
status summary and the exact path of the task artifact.
