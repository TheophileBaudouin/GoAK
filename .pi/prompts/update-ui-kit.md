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
`PIN.md` + `scenarios.json`), rewrites the pin record, runs the structural
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

1. `git diff --stat KitV2/ui-kit` — confirm the change matches the upstream
   jump (added/removed/modified SDK files; `PIN.md` SHA + dates).
2. Inspect the diff for anomalies (unexpected deletions, binaries, secrets).
3. Commit with a message naming the new SHA and summarizing the change, e.g.:
   `feat(ui-kit): re-pin zone to ui-agent-kit <short-sha> — <what changed>`.
4. Do NOT amend silently; keep the commit separate and reviewable.

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
