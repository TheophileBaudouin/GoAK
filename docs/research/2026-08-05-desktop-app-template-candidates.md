# Admission dossier — desktop-app template (Wails)

Date: 2026-08-05. Author: metaproject governance-hardening pass (Rodin
finding D), research delegated to Web-Research (fresh-context sub-agent,
read-only). Status: **dossier preparation only** — admission itself (copy,
pinning, attribution, gate) belongs to the next pass in `KitV2/templates/`.

## 1. Context

`recipes/recipe-desktop-app/SKILL.md` (Wails v3, rejects Tauri "Rust, out of
scope of a Go kit") and `probes/desktop-app/main.go` exist. The rest of the
graph therefore covers the desktop capability, but `templates/TEMPLATES.md`
does not list desktop-app anywhere (roadmap = grpc, microservice, monolith,
cloud-service). Per Z5 §2 policy, a template must be a real open-source
project, MIT, maintained, tested, **ultra-specific** (almost exclusively the
template's technology), small, single-responsibility — never an agent-written
scaffold.

## 2. Wails ecosystem state (verified 2026-08-05)

| Version | Status | Latest | Install |
| --- | --- | --- | --- |
| v2 | stable | v2.13.0 (2026-07) | `go install github.com/wailsapp/wails/v2/cmd/wails@latest` |
| v3 | beta (pre-release) | latest pre-release as of 2026-08-05 | `go install github.com/wailsapp/wails/v3/cmd/wails3@latest` |

- Wails v3 has been in alpha since January 2023, reached beta mid-2026: the
  desktop API is stable but the release stays pre-release (verified via the
  GitHub API on 2026-08-05: latest stable = v2.13.0, tags v3.0.0-beta.*). The
  kit recipe documents "Beta-to-GA transition".
- Sources: <https://v3.wails.io/blog/wails-v3-beta/> and
  <https://github.com/wailsapp/wails/releases> (verified by the sub-agent and
  confirmed read-only by the fresh-context review via the GitHub API).

## 3. Candidates evaluated against Z5 §2 (none passes)

| Candidate | License | Activity | Ancillary stack | Tests/CI | Verdict |
| --- | --- | --- | --- | --- | --- |
| JinGongX/SuiDemo | MIT (API-verified) | push 2026-04-12, 86★ | Vue 3 + vue-i18n + SQLite + Tailwind | no | FAIL — a template/starter, not an app; heavy stack; no tests |
| kazuph/obails | MIT (verified) | push 2026-06-12, 2★ | TypeScript + Node.js | no | FAIL — too small, single contributor, no tests/CI |
| JessonChan/captain-api | MIT (verified) | push 2025-10-20, 3★ | Vue 3 + TypeScript | no | FAIL — too small, inactive 9+ months, no tests/CI |
| ehsanpo/Fakering | — | 0★, abandoned | — | — | FAIL |
| gofurry/wails-v3-vue-starter | MIT | 4★ | Vue 3 | — | FAIL — a starter, not an app |

**Official examples** (`wailsapp/examples`): a collection of demonstration
projects (file-association, updater, events, binding, systray-menu,
drag-n-drop, window, wml) — feature demos, not a real single-responsibility
application. Excluded (and now explicitly excluded by the Z5 §2 policy,
precision D-2026-08-05-14: a source = real application, not starter/demo).

## 4. Honest conclusion

**No candidate satisfies the Z5 §2 policy as of 2026-08-05.** The Wails v3
ecosystem is too young (beta) and too small to produce a real, MIT,
mono-technology, tested, browsable project. The criteria are not softened to
find a candidate: the template policy is a hard portal (Z5 §2), and admitting
a starter or a demo would create exactly the defect Z5 §2.4 forbids
(grab-bag, not functional in the product sense).

Consequences:

1. **Roadmap line** desktop-app = `planned` with the note "no conforming MIT
   source as of 2026-08-05" (text ready in the metaproject plan, annex D; to
   apply in `KitV2/templates/TEMPLATES.md` at the next pass) — the capability
   stays recognized (recipe + probe), the template waits for a conforming
   source.
2. **Re-evaluation trigger**: the Wails v3 GA (and its ecosystem maturation,
   ~6-12 months); the roadmap line mentions it.
3. **Transferable lesson**: the Z5 §2 policy now explicitly excludes
   third-party starters/templates and demo collections as a source
   (D-2026-08-05-14) — avoids re-evaluating false candidates.

## 5. Verification commands to run at the real admission

To re-run on any future candidate (not executed in 2026-08-05 — no candidate
reached this stage):

```sh
git clone <repo-url> && cd <repo-dir>
cat LICENSE | head -5                        # MIT mandatory
go build ./... && go test ./... && go vet ./...
test -z "$(gofmt -l .)"
find . -name "*.go" | wc -l                  # smallness
find . -name "*.go" -exec wc -l {} + | tail -1
grep -r "gorilla\|gorm\|echo\|gin\|chi\|sqlx\|zap\|logrus\|observ\|auth" go.mod 2>/dev/null \
  || echo "No auxiliary stack detected"
```

The final verification also includes: executed observable scenario
(document PASS/PARTIAL/BLOCKED), ATTRIBUTION.md (source, pinned version,
adaptations, technical scope), template.yaml, README.md with structure
justification (D-2026-08-05-13).
