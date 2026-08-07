# PIN — ui-agent-kit SDK zone (KitV2/ui-kit)

This zone is a **pinned, verbatim mirror** of the consumable SDK of the
ui-agent-kit repository. It is never hand-edited: content changes arrive only
through the metaproject re-sync process (see the kit-governance contract
"Z13 — ui-kit zone" §Update path; the contract is metaproject-only and does
not ship with this product).

## Source

| Field | Value |
| --- | --- |
| Repository | `https://github.com/TheophileBaudouin/ui-agent-kit` |
| Pinned commit (SHA) | `f9bdd9b5237a9154f86050e0f5df583c66e2496e` |
| Commit date | 2026-08-07 |
| Pinned subtree | `sdk/` (the whole folder, hidden files included) |
| npm release equivalence | `ui-agent-kit@0.1.0` — tarball `sdk/` verified byte-identical to the pinned `sdk/` (2026-08-07) |
| License | MIT (upstream `LICENSE` at repo root; `sdk/skills/*` carry their own license fields) |
| Sync date | 2026-08-07 |

## Verification performed at sync time

- `diff -rq <upstream sdk/> <KitV2/ui-kit/>` — empty (before PIN.md was added).
- No `.go` files (the zone adds no Go surface to the module).
- No `.agent/` occurrences (product validator `check_no_metaproject_paths`).
- No zero-byte `.md` files (product validator `check_empty_markdown`).
- No accented-French content (fundamental language rule D-2026-08-05-21).
- Skill frontmatter: all 7 `skills/*/SKILL.md` carry `name` + `description`.

## Update path (manual, gated — never automatic)

1. Run `.agent/sync-ui-kit-from-upstream.sh <new-sha>` from the metaproject root.
2. The script pins the new SHA, diffs `sdk/` vs `KitV2/ui-kit/`, updates this
   file, and prints the verification checklist.
3. Run the FULL validation gate (validators, Go scenarios 22/22, UI scenarios,
   gofmt/vet/lint/test/race/gosec/govulncheck, probes) before committing.
4. Record the change in `.pi/memory/Decisions.md` and `docs/evidence/`.

A silent or automatic update is forbidden (Z13).
