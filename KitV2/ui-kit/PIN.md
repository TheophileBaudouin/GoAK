# PIN — ui-agent-kit SDK zone (ui-kit)

This zone is a **pinned, verbatim mirror** of the consumable SDK of the
ui-agent-kit repository. It is never hand-edited: content changes arrive only
through the zone's re-sync process (manual, gated — never automatic).

## Source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/TheophileBaudouin/ui-agent-kit` |
| Pinned commit (SHA) | `cd00eb5d92d8044645ff3d6aca1922a473ecb804` |
| Commit date | 2026-08-08 |
| Pinned subtree | `sdk/` (the whole folder, hidden files included) |
| Local-owned files | `PIN.md`, `scenarios.json`, `copy-rules.json` (never overwritten by a sync). `ui-kit/.pi/settings.json` is **dead by design**: the UI skills are registered in the root `.pi/settings.json` (single registration point); the re-sync excludes `.pi/settings.json` |
| npm release equivalence | `ui-agent-kit@0.1.1` — tarball `sdk/` verified byte-identical to the pinned `sdk/` at cd00eb5d (2026-08-08; npm is never the source, GitHub-direct only) |
| License | MIT (upstream `LICENSE` at repo root; `sdk/skills/*` carry their own license fields) |
| Sync date | 2026-08-08 |

## Verification performed at sync time

- `diff -rq <upstream sdk/> <ui-kit/>` — empty (before PIN.md was added).
- No `.go` files (the zone adds no Go surface to the module).
- No control-directory markers (product validator guard).
- No zero-byte `.md` files (product validator `check_empty_markdown`).
- No accented-French content (fundamental language rule — English only).
- Skill frontmatter: all 7 `skills/*/SKILL.md` carry `name` + `description`.
- `copy-rules.json` generated from the upstream `cli/manifest.json` at the pinned SHA (the consumer sync tool never hardcodes a path — structure evolution is handled at re-sync).

## Update path (manual, gated — never automatic)

1. Run the zone's re-sync helper with the new SHA.
2. The script pins the new SHA, diffs `sdk/` vs `ui-kit/`, updates this
   file, and prints the verification checklist.
3. Run the FULL validation gate (validators, routing scenarios, UI scenarios,
   gofmt/vet/lint/test/race/gosec/govulncheck, probes) before committing.
4. Record the change in the decision record and evidence directories.

A silent or automatic update is forbidden.
