# Plan — Metaproject governance hardening (closing 5 Rodin findings)

## Goal

Close the 5 findings identified by the adversarial self-critique "Rodin"
(non-triggered cross-file duplication, premature snippets roadmap, Go
philosophy contradiction, desktop-app without sourced template, MANDATORY
instructions without mechanical gate) **without touching `KitV2/`**:
governance contracts, `.pi/prompts/kit-audit.md`, `.agent/instructions.md`,
decisions, and metaproject research only. The product correction pass
(owner, `.pi/prompts/kit-audit` then corrections) follows; this pass prepares
its pending actions, written and ready, without applying them.

## Context

- Rodin critique verified against the real tree before drafting (reading the
  cited files, no blind trust) — two calibration nuances confirmed as facts:
  1. **Chantier A**: C2 §2 (02-validation-gate.md, "Freshness" block) already
     declares "Semantic duplication remains a human review." The problem is a
     **triggering defect** of this review between two audits, not an absence
     of risk awareness.
  2. **Chantier B**: `KitV2/snippets/` contains exactly 3 real snippets
     (bounded-worker, errors-once, http-json); the 7 roadmap lines are only a
     Markdown table of the README, mandated by 13-zone-snippets.md §3 rule 3
     and 00-charte-d-application.md §7, same pattern as templates/TEMPLATES.md.
- Coupling points verified directly (no dedicated scout: the direct reading
  of the cited files covers the "locate real coupling points before
  concluding" need):
  - `KitV2/tools/validators/validate-kitv2.py` `check_internal_duplicates`
    (l.203): intra-file paragraph comparison only; docstring: "leaving
    semantic review to humans".
  - SNIPPET.yaml all declare a resolved `source:` (bounded-worker →
    `recipes/recipe-worker-pool/SKILL.md`, errors-once →
    `rules/core/errors/SKILL.md`, http-json →
    `recipes/recipe-rest-chi/SKILL.md`) — a pattern/recipe/rule → snippet
    pointer chain mechanically verifiable.
  - SNIPPET.yaml does not carry `last_verified` (field absent from the
    `bounded-worker` model) → the cross-file rule must add this field (Z4 §3)
    to be date-verifiable.
  - `recipe-desktop-app/SKILL.md` (Wails v3, rejects Tauri "Rust, out of
    scope of a Go kit") + `probes/desktop-app/main.go` exist;
    `templates/TEMPLATES.md` does not list desktop-app anywhere (roadmap =
    grpc, microservice, monolith, cloud-service only).
  - `.pi/skills/kit-resource-routing/SKILL.md` says "MANDATORY before
    planning or implementing" for `search_kit_resources`; nothing mechanical
    enforces it. Pi docs `docs/extensions.md` (verified): the `tool_call`
    event **can block** (`{ block: true, reason }`), `pi.setActiveTools()`
    enables/disables tools, `before_agent_start` injects messages,
    `pi.appendEntry()` persists session state → a mechanical gate is really
    conceivable.
- Web-Research (Chantier D) done: **no Wails candidate qualifies** the Z5 §2
  policy (Wails v3 in beta v3.0.0-beta, ecosystem too young; v2 stable but no
  real MIT mono-technology tested project found; `wailsapp/examples` = demos,
  excluded). Report:
  `docs/research/2026-08-05-desktop-app-template-candidates.md`.

## Constraints

- **Strict metaproject scope**: `KIT_CHARTER.md` (priority read, not
  modified), root `AGENTS.md` (not modified), `.agent/` (contracts,
  instructions, validators, cognitive), `.pi/memory/`, `.pi/prompts/
  kit-audit.md`, `docs/`. **No edit under `KitV2/`** — any product correction
  is logged as a finding or written in this plan as a pending action for the
  next pass. Never widen the boundary (AGENTS.md Modification policy).
- One writer per worktree; the only parallel execution is read-only research
  (Web-Research Chantier D, done).
- Every new contract rule must be formulated to be verifiable by C2 or a
  review control (kit-governance README) — otherwise it is a hypothesis.
- No code in `KitV2/tools/validators/validate-kitv2.py`: the exact contract
  of the new checks is written in this plan (§ Annexes A/B/C), ready for the
  implementation pass.
- Documented confidence: an unverified hypothesis is never a firm claim in
  the final report.
- Three identical failures → stop and report.
- Metaproject gates after edits: `python3 .agent/validators/
  validate-instructions.py` + `python3 .agent/validators/
  validate-cognitive.py` from the root (no product gate: no KitV2 code
  modified).

## Done when

- Plan written (this file) before any edit ✓.
- Chantier A: options a/b/c evaluated, decision taken, contracts C2/Z3/Z4/Z1
  updated with the verifiable rule, kit-audit phases C4 + §5-E evolved, exact
  check contract written (annex A), no KitV2 code written.
- Chantier B: 13-zone-snippets vs 14-zone-templates comparison done,
  evidence-based verdict, Decision Record recorded (no fabricated work).
- Chantier C: `docs/research/2026-08-05-philosophy-tension.md` written with
  ≥ 3 options, question asked to the owner (blocker: nothing else on C before
  the answer); application after the answer (metaproject → apply; core →
  pending action).
- Chantier D: dossier `docs/research/2026-08-05-desktop-app-template-
  candidates.md` (no conforming candidate, honest); Z5 §2 precision (real
  source ≠ starter/demo) applied; TEMPLATES.md roadmap line written in the
  plan (not applied); kit-audit phase B evolved.
- Chantier E: real Pi capability documented (mechanical gate exists), exact
  mechanism spec written in the plan (annex B), principle extended in
  `.agent/instructions.md` (automation-gaps registry), C2 + Z8 updated,
  kit-audit "absolute instructions" dimension named.
- Metaproject gates green; fresh-context review obtained before declaring
  completion; Decisions.md (D-2026-08-05-11…15), Progress.md, Gotchas.md (if
  durable lesson) updated; final report with untouched KitV2 files.

## Steps

1. (done) Evidence verification against the real tree + coupling-point recon.
2. (done) Web-Research Chantier D (fresh-context sub-agent, read-only).
3. Writing this plan + philosophy note
   (`docs/research/2026-08-05-philosophy-tension.md`) + desktop-app dossier
   (`docs/research/2026-08-05-desktop-app-template-candidates.md`).
4. Question to the owner (Chantier C) — do not advance on C before the answer.
5. Chantier A: decision D-2026-08-05-11; edits C2 §2 (cross-file rule +
   tripwire + absolute instructions), Z4 §3/§5, Z3 §5, Z1 §6; kit-audit
   C4/§5-E.
6. Chantier B: decision D-2026-08-05-12 (verdict: sound, no contractual
   edit).
7. Chantier D: decision D-2026-08-05-14; Z5 §2 precision; kit-audit phase B;
   roadmap line ready in the plan (not applied).
8. Chantier E: decision D-2026-08-05-15; `.agent/instructions.md` (principle
   - registry); C2 §2 + Z8 §3; kit-audit named dimension.
9. Chantier C post-answer (if the owner answers during the pass): apply if
   metaproject only; otherwise pending action.
10. Metaproject gates: `validate-instructions.py`, `validate-cognitive.py`.
11. Fresh-context review (read-only sub-agent, C0 §6.3) — integrate or settle
    the remarks.
12. Memory (Decisions.md D-2026-08-05-11…15, Progress.md, Gotchas.md if
    needed) + commit + final report.

## Pass decisions (summary, details in Decisions.md)

- **A (D-2026-08-05-11)**: combine mechanized (b) + tripwire (a). Verifiable
  rule: declared dependent re-verified when the canonical changes
  (`last_verified(dependent) >= last_verified(canonical)`, date-checkable for
  snippet `source:` and graph-YAML relations); similarity tripwire
  example.go ↔ canonical block as warning (never error, focused view ≠ copy).
  Status quo (c) alone rejected: adds no trigger.
- **B (D-2026-08-05-12)**: the snippets roadmap design is sound — the 7 lines
  each carry an actionable admission criterion, more precise per line than
  the templates' `planned` status ("decision + line"), and the pattern is
  mandated by Z4 §3 + C0 §7; no contract change. Closed without fabricated
  work.
- **C (D-2026-08-05-13)**: tension documented honestly (2 levels: root
  AGENTS.md "Go does not prescribe a universal project tree" +
  rules/core/philosophy "no universal project layout" vs personal goal of
  identical navigation); 3 options posed; owner answer (2026-08-05): Option 3
  "navigate by reason"; application subordinate to the answer.
- **D (D-2026-08-05-14)**: no conforming Wails candidate (v3 beta, immature
  ecosystem); Z5 §2 precision "source = real application, not starter/demo"
  (transferable lesson); desktop-app roadmap line = planned with "no
  conforming source as of 2026-08-05, re-evaluate at GA"; admission = next
  pass (KitV2).
- **E (D-2026-08-05-15)**: Pi exposes a real mechanical gate (`tool_call`
  block, `setActiveTools`) — exact spec of a "soft reminder" extension
  written (annex B, implementation next pass in KitV2/.pi/); principle
  extended to consumer artifacts (MANDATORY ⇒ mechanical control OR "guidance
  only" label in the automation-gaps registry); no hard validator scan
  (false-positive risk on legitimately review-enforced absolutes —
  documented).

## Pending actions for the next pass (KitV2/ — do NOT apply here)

1. **C2 check "cross-file drift"** (validate-kitv2.py): full spec in Annex A
   — SNIPPET.yaml `last_verified` field (recommended), snippet↔source date
   comparison, graph-YAML dependent↔target relation, similarity tripwire
   (warning), +/− tests.
2. **Pi gate "search_kit_resources"** (KitV2/.pi/extensions/): full spec in
   Annex B — session state, soft reminder on `tool_call` of writing tools,
   UI-less degradation, optional hard-block.
3. **TEMPLATES.md**: add the desktop-app roadmap line (text ready in Annex
   D), `planned` status, "no conforming MIT source as of 2026-08-05 (Wails v3
   beta) — re-evaluate at GA" note.
4. **Existing SNIPPET.yaml alignment**: add `last_verified` to the 3 snippets
   when the check is implemented.
5. **Option 3 (D-2026-08-05-13) — KitV2**: add the "Structure (why this
   layout)" section to the recipes concerned by a project layout (application/
   service/CLI/worker/desktop creation) and the structure justification to
   the 3 sourced templates' README (Z5 §3 format).
6. **C2 check "absolute instructions"** (if decided at implementation):
   grep MANDATORY/absolutes in consumer artifacts and verify control or label
   — spec in Annex C.

## Annexes

### Annex A — Contract of the C2 "cross-file drift" check (to implement next pass)

- **Inputs**: `snippets/*/SNIPPET.yaml` (resolved `source:` field),
  `snippets/*/example.go`, `snippets/*/check.sh`, target SKILL.md,
  `knowledge/**/*.yaml` (`references`/`uses`/`depends_on` relations to dated
  artifacts).
- **Pass/fail rule**:
  - Snippet: if SNIPPET.yaml carries `last_verified` AND the `source:` target
    carries `last-verified` (SKILL.md frontmatter), then
    `last_verified(snippet) >= last_verified(target)` — otherwise **error**
    ("snippet not re-verified after modification of its canonical source").
  - Graph-YAML: for any relation to a dated target,
    `last_verified`(dependent) >= target's — otherwise **error**.
  - Tripwire (warning, never error): token similarity (Jaccard/normalized
    containment, comments ignored) between `example.go` and the target
    `source:` Go block; below a threshold calibrated on the 3 existing
    snippets → `warning: "suspected drift …"`.
- **Known false positives**: legitimate focused view of a snippet (≠ copy) —
  hence warning and not error; missing dates → check ignored (no failure);
  targets without a Go block → tripwire N/A.
- **Tests**: + re-verified snippet (dates OK); − obsolete snippet (lower
  date); − obsolete graph relation; +/− tripwire at the calibrated threshold.

### Annex B — Contract of the Pi "search_kit_resources" gate (to implement next pass)

- **Mechanism**: Pi extension in `KitV2/.pi/extensions/` (merged into
  kit-resource-router.ts or a separate file) — session state `searched`
  (reset on `session_start`, set on `tool_call` of `search_kit_resources`),
  `tool_call` hook on writing tools (write/edit/apply_patch/bash): if
  `searched == false` and the input looks like technical work (.go/.mod
  extensions, `go build|test|run|mod` commands, paths under
  rules/recipes/knowledge/snippets/templates), inject a soft reminder in
  `tool_result` ("kit-resource-routing: search_kit_resources was not called
  this session before this technical edit — do it first unless the work is
  non-technical").
- **Degradation**: UI-less mode (print/rpc) → reminder only (never a blocking
  confirm); optional `hard-block` by configuration (block + reason) reserved
  for TUI sessions, with an explicit exemption for the "non-technical work"
  case (the skill itself excludes it).
- **Honest confidence level**: session presence ≠ proof that the *right*
  search preceded *this* edit → the gate is a reminder tripwire, not a
  conformity proof; the audit (absolute-instructions dimension) remains the
  judge.
- **Tests**: pi smoke from a consumer copy (reminder triggered, no reminder
  after search, no reminder on non-technical edit).

### Annex C — Contract of the "absolute instructions" check (optional, next pass)

- Deterministic grep of MANDATORY / "must always" / "never" lexemes in
  consumer artifacts (AGENTS.md, skills, prompts, recipes); each occurrence
  must be attached to a named mechanical control OR a "guidance only" label
  in the `.agent/instructions.md` registry. Initial status: warning (the
  registry exists), error when the registry is complete.

### Annex D — TEMPLATES.md roadmap line (ready to paste, next pass)

```markdown
| desktop-app | planned | — (no conforming MIT source as of 2026-08-05: Wails v3 in beta, ecosystem immature; official examples = demos) | Wails v3 — re-evaluate at GA (research 2026-08-05) |
```

(to insert in the "Statut actuel" table of `KitV2/templates/TEMPLATES.md`,
and the catalog sentence: "The grpc, microservice, monolith, cloud-service
**and desktop-app** shapes remain a roadmap without an operational
template.")
