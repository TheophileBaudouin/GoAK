# Behavioral Rules

These rules apply to every agent and every phase in the Spec-Driven Develop workflow. They are non-negotiable.

---

1. **Never skip phases**. Even if you think a phase is unnecessary, at minimum create a lightweight version of its outputs.

2. **Always confirm with the user** before proceeding to the next phase. Each phase boundary is a checkpoint.

3. **Document everything**. If you make a decision, record it in the relevant progress file's "Notes" section.

4. **Progress updates are mandatory**. After completing any task, record its telemetry and implementation state immediately. LOCAL_ONLY mode: check the box in the phase file AND the completion count in MASTER.md. The platform's native task tool (todo) is an optional complementary layer.

5. **New conversation = read MASTER.md first**. This is non-negotiable. The master file is your memory across conversations.

6. **Respect the user's time**. Keep summaries concise. Use bullet points and tables, not walls of text.

7. **Archiving is not optional**. When all tasks are done, always enter Phase 6 (Archive). Archive all artifacts to `docs/archives/` for traceability — don't leave them scattered in working directories or delete them.

8. **Dual-write progress updates**. When completing a task, update progress in two places for redundancy: the platform's native task tool (mark as completed) + the Markdown progress files (check the box, update counts). The principle is the same in all modes: no single point of failure for progress state.

9. **Use the platform's structured question tool for all user interactions**. Whenever you need to ask the user a question, request clarification, or get confirmation (including phase boundary checkpoints), you MUST use the platform's built-in structured question/choice tool (for example `ask_user_question` in Pi). Do not rely on plain text output to ask questions — the tool ensures the user sees and responds to your question directly. If the platform has no such tool, ask in plain text and wait for an explicit reply.

10. **Post-task telemetry is mandatory**. After completing every task, record actual effort, S.U.P.E.R score, and unplanned dependency count BEFORE marking the task as done. This is as non-negotiable as progress updates (rule 4). See `references/adaptive-control.md` § "Telemetry Collection" for what to collect and § "Adaptive State Storage" for where to store it.

11. **Drift threshold triggers are automatic**. When `drift_score` exceeds a threshold, the agent MUST halt and execute the corresponding response action (annotate / replan / rescope) without waiting for user instruction. The thresholds are computed per-phase as percentages of total task count (20 % / 40 % / 60 %). See `references/adaptive-control.md` § "Automatic Response Actions" for the response protocol.

12. **Adaptive state is persistent**. Always read and write `drift_score` via the defined storage: the "Adaptive Control State" section of MASTER.md in LOCAL_ONLY mode. Never store adaptive state only in conversation memory — it must survive across sessions.

13. **Project governance surface resolution is mandatory**. Every spec-driven run must resolve shared instruction surfaces, platform-specific instruction surfaces, and the durable memory surface before execution begins. Prefer existing/native surfaces. Typical instruction surfaces include `AGENTS.md`, `.cursor/rules/`, `.windsurf/`, `.clinerules*`, `.codex/`, or project equivalents.

14. **Do not create competing truth sources**. If a project already has equivalent instruction or memory surfaces, update the canonical surfaces in place and record the resolution in MASTER.md. Use native memory (`.pi/memory/`) when available. Do not silently create a repo-local memory file; only use one when the project already declares it or the user explicitly selects it. **Verify which memory files actually exist — the Pi bootstrap may not create `Decisions.md`; never assume the standard set.**

15. **Feature work requires tests by default**. Any task that adds or changes user-visible features, business behavior, API contracts, schemas, migrations, parsing, routing, permissions, caching, or persistence must add or update relevant automated tests. If tests are not applicable or the project lacks a test surface, the task must state the reason and run the closest static/syntax validation available.

16. **Stable learnings go to the resolved memory surface**. When execution reveals a reusable command, invariant, project convention, recurring gotcha, or future-agent rule, record it in the resolved native memory surface (`.pi/memory/`) or the explicitly chosen fallback. If it changes how agents should work in the repository, also update the resolved instruction surfaces.

17. **Tasks and batches have different cardinalities**. Tasks are atomic planning, acceptance, and telemetry units; delivery batches are implementation, integration-validation units. Before editing a phase, review all of its tasks and form the smallest coherent set of phase-local batches. Default to one reviewable batch per phase, not one batch per task. Split only for a documented reviewability, release/rollback, ownership, risk-isolation, dependency, or repository-policy boundary. A single-task batch requires an explicit rationale unless it is the only task in the phase.

18. **Reviewer commit-ownership and authority boundaries**. In the execution review loop, the per-lane reviewer may commit fixes only to its lane's branch (append-only, `fix:` commits referencing but never closing tasks). Reviewers never edit MASTER.md, nor drift/adaptive state, nor instruction or memory surfaces — their review reports return to the orchestrator. The orchestrator remains the acceptance-verification authority and the single writer for all shared state.

19. **Sub-agent dispatch is an economic decision, not a default**. Dispatch only when parallelism gain and context-isolation value exceed the sub-agent cold-start tax and orchestration overhead. Orchestrator-direct execution (Tier 0) is the default; single-coder delegation (Tier 1) is for L/XL or context-heavy work; parallel lanes (Tier 2) require disjoint file sets, ≥ L effort per lane, independent verifiability, and ≤ 4 lanes. Review is likewise tiered: machine validation (L1) and orchestrator diff review (L2) are the default; independent reviewer agents (L3) are reserved for Tier 2 lanes and high-risk changes. Admission criteria live in `references/parallel-protocol.md`.
