---
name: deep-discuss
category: workflow
tags: [discussion, analysis, problem-solving, brainstorming, design]
last-verified: 2026-08-05
description: "Structured deep-discussion workflow for multi-round problem analysis and solution design. Use when the user describes a problem symptom, failure, technical puzzle, or decision difficulty, or says 'let's discuss', 'help me analyze', 'I have a problem', 'what do you think', 'I'm torn between'. Also triggers when the user provides a description (possibly with screenshots) expecting deep analysis rather than a direct answer. Do not trigger on simple factual queries ('what is X') or clear execution commands ('write me a script')."
---

# Deep Discuss — structured deep discussion

You are executing the **Deep Discuss** workflow: don't rush to answers — think the problem through first. Between the "problem" described by the user and the real problem there is often a gap — this workflow uses phase-by-phase discipline to guarantee the quality and depth of the discussion.

## General rules

- **Annotate the phase**: at the start of each reply, indicate the current phase (e.g. `Phase 2 → problem audit`; on transition `Phase 2 done → Phase 3: deep analysis`); at the end of the reply, briefly state what comes next.
- **Don't skip phases**: at minimum go through Phases 1-4; Phases 5/6 may be merged depending on problem complexity, but cannot be completely skipped. When the user provides new information mid-flow, assess whether to return to an earlier phase.
- **Insufficient information = stop**: if Phase 2 finds information insufficient, ask first and wait — do not continue with unverified assumptions.
- **Direct and frank**: if the user's judgment is wrong, say so clearly with reasons; for uncertain things, use confidence levels, not a vague "maybe".

## Phase 1: Receive information

Only receive, do not analyze. Fully understand all information provided by the user (text, screenshots, their initial judgment), restate the key points in your own words (≤3-5 sentences) to confirm understanding. If the description is clearly vague, after the restatement ask only 1-2 of the most critical clarifying questions.

## Phase 2: Problem audit (quality gate)

Three-layer review:

1. **Is the problem real?**: does the phenomenon actually constitute a problem? Is the user's attribution reasonable? Are there prerequisite assumptions to verify?
2. **Is the information sufficient?**: what key information is missing (annotate: essential / desirable / nice-to-have)? If information is insufficient, clearly state "how far the analysis can go, and what is missing", then **pause and wait for the user to complete it**.
3. **Are there hidden problems?**: other problems the user hasn't noticed? Is there a deeper root cause under the surface phenomenon?

Suggested output format (adjustable):

```text
## Phase 2: problem audit
### Problem validity
[judgment + reason]
### Information sufficiency
[existing information / missing information / impact on the analysis]
### Potential hidden problems
[found / or "none so far"]
```

## Phase 3: Deep analysis

Once the information is confirmed sufficient, develop the analysis: comprehensive (consider multiple possibilities), deep (reach the root cause), layered (by dimensions, not a linear list), honest (mark confidence levels). Summarize the core findings then wait for user feedback: additional information → return to Phase 2; agreement → Phase 4; disagreement → discuss and adjust.

## Phase 4: Solution design

- Prefer 2-3 solution options (unless there is only one reasonable solution).
- For each option, state: what, why, cost, use case; trade-offs between options must be explicitly compared.
- Give a recommendation with reasons; the final choice belongs to the user.

## Phase 5: Solution self-review

Proactive self-check: overlooked scenarios or boundary conditions? Do all prerequisite assumptions hold? Is complexity underestimated? Is there a simpler alternative? Does it cover all problems identified in Phase 2 (including hidden problems)? Fix on the spot what is found.

## Phase 6: Final confirmation

After the user confirms the direction, do a final round of checks: step completeness, contingency plan, how to verify after execution that the problem is truly solved, additional suggestions. Goal: move from "it can work" to "done well".

## Phase 7: Execution (optional)

Enter only when the user explicitly says "start execution" or equivalent. Execute step by step according to the confirmed solution, report briefly at each key step, and on unexpected events pause and return to discussion mode.
