---
description: Update the pinned ui-kit zone (KitV2/ui-kit/) from the upstream ui-agent-kit GitHub repository, cleanly and without breaking the kit — pre-flight, sync, full-gate verification, commit, memory/evidence.
argument-hint: "[new-sha]"
---

# Update ui-kit from upstream

You are executing the **only sanctioned update path** for the pinned
ui-agent-kit SDK zone (Z13 §4). The user asked to update `ui-kit/`; the zone
is a verbatim mirror of upstream `sdk/` at a pinned commit SHA (see
`KitV2/ui-kit/PIN.md`), and this workflow keeps the maintenance clean,
verifiable, and reversible. The prompt is a metaproject maintenance tool and
is never part of the shipped product.

## Goal / Context / Constraints / Done

- **Goal**: refresh `KitV2/ui-kit/` from upstream `ui-agent-kit` at the
  requested commit, with the full validation gate green.
- **Context**: content comes from GitHub (clone/sparse/archive at a pinned
  SHA), NEVER from npm. Local-owned files (`PIN.md`, `scenarios.json`) are
  never overwritten. The zone stays Go-free, English-only, marker-free.
- **Constraints**: nothing outside `KitV2/ui-kit/` is modified by the sync;
  nothing is committed automatically; a failed gate is rolled back; silent
  or automatic updates are forbidden.
- **Done**: gate PASS, `git diff` reviewed, commit created, decision +
  evidence recorded.

## Phase 0 — Pre-flight (guardrails)

1. `git -C . status --short` — the working tree must be clean for
   `KitV2/ui-kit/` (uncommitted zone changes are clobbered by a sync → abort
   and commit/restore first).
2. Determine the target SHA:
   - if the user gave one, it must be a well-formed 40-hex commit;
   - otherwise resolve upstream HEAD:
     `git ls-remote https://github.com/TheophileBaudouin/ui-agent-kit HEAD`
     and report it to the user before syncing (do not sync an unseen SHA).
3. Read `KitV2/ui-kit/PIN.md` — record the current SHA and npm equivalence
   for the changelog.

## Phase 1 — Sync (mechanical, gated)

Run:

```sh
bash .agent/sync-ui-kit-from-upstream.sh <new-sha>
```

The helper performs its own pre-flight (SHA shape, clean zone, upstream
reachable, `sdk/` present), copies only inside `KitV2/ui-kit/` (excluding
the local-owned files `PIN.md`, `scenarios.json`, `copy-rules.json` AND the
dead `.pi/settings.json` — the UI skills' single registration point is the
root `KitV2/.pi/settings.json`, which the helper never touches), rewrites
the pin record, runs the structural
checks (diff clean beyond local-owned files, no `.go`, no metaproject
markers, no zero-byte `.md`, English-only), then runs the FULL gate
(validators, router Go + UI gates, router tests, gofmt/vet/lint/test-race/
gosec/govulncheck, probes).

- Exit 0 + "FULL GATE PASS" → continue.
- Any failure → follow the printed rollback
  (`git restore -- KitV2/ui-kit KitV2/ui-kit/PIN.md`), report the failure,
  and do NOT commit. `--no-verify` exists only for debugging and still
  requires the full gate before any commit.

## Phase 2 — Review and commit (manual, never automatic)

1. `git diff --stat KitV2/ui-kit KitV2/AGENTS.md` — confirm the change
   matches the upstream jump (added/removed/modified SDK files; `PIN.md` SHA
   - dates). Pay attention to `ui-kit/copy-rules.json` (local-owned): it is
   regenerated from the upstream `cli/manifest.json`, so a NEW upstream
   folder appears here and the consumer sync tool will copy it without a
   code change — if the rules changed, review the new mapping explicitly.
2. **Merged root AGENTS.md (owner rule 2026-08-08)**: `KitV2/AGENTS.md`
   carries a "UI work" section that merges the SDK's `ui-kit/AGENTS.md`
   instructions (checksum marker in its HTML comment). If the sync changed
   `ui-kit/AGENTS.md`, the helper refuses to finish until this section is
   updated — adapt the prose to mirror the new SDK instructions (never lose
   an instruction from either file) and refresh the sha256 marker. Review
   the section even on a trivial jump.
3. **Project Foundation guard (Z14)**: `KitV2/AGENTS.md` also carries the
   "Project Foundation" pointer section, delimited by its own markers
   (`<!-- workspace-init section: begin -->` … `<!-- workspace-init
   section: end -->`). Before committing, verify — via
   `validate-kitv2.py` `check_workspace_init_placeholder` (or a quick read
   of the two markers and the `## Project Foundation` title between them) —
   that the section survived this sync intact. If the section or a marker
   is missing or altered, ABORT: `git restore -- KitV2/AGENTS.md`, report
   the failure, and do NOT commit — exactly like any other failed guard in
   this workflow.
4. Inspect the diff for anomalies (unexpected deletions, binaries, secrets).
5. Commit with a message naming the new SHA and summarizing the change, e.g.:
   `feat(ui-kit): re-pin zone to ui-agent-kit <short-sha> — <what changed>`.
   Include `KitV2/AGENTS.md` when its merged section changed.
6. Do NOT amend silently; keep the commit separate and reviewable.

## Phase 3 — Record (durable state)

1. `.pi/memory/Decisions.md`: a dated decision (D-YYYY-MM-DD-NN) with the
   SHA jump, the reason (user request / upstream release), and the gate
   result.
2. `docs/evidence/YYYY-MM-DD/ui-kit-update/`: the helper log (or its key
   lines) — raw output never belongs in memory.
3. `.pi/memory/Gotchas.md`: any upstream surprise (content regressions,
   new file classes, license changes) with the preventive rule.
4. `docs/plans/` only when the update is non-trivial (big jump, structural
   change in upstream `sdk/`).

## Guardrails recap

- Pre-flight: clean zone, valid SHA, upstream reachable, `sdk/` present.
- During: only `KitV2/ui-kit/` written; local-owned files excluded.
- Post: structural checks + FULL gate; failure = rollback, never commit.
- Discipline: manual commit, dated decision, raw evidence, fresh-context
  review for any non-trivial jump (a second agent verifies the diff + gate
  before the user merges).
