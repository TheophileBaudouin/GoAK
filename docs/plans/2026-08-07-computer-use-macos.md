# Plan — macOS Computer Use resources for the kit

Date: 2026-08-07
Status: implementation
Owner: go-agent-kit

## Goal

Give kit consumers (agents implementing autonomous computer use, desktop
automation, or simulated user interaction on macOS Apple Silicon) a routed
decision artifact plus a vetted execution library, so they use the reliable
native Apple APIs instead of fragile pixel-only or pure-Go substitutes.

## Context

The request proposed adding an "exception" to a supposed general kit rule
avoiding CGO / Objective-C / platform-specific native bindings.

**Premise check (verified against the current tree, 2026-08-07): no such rule
exists.** The kit contains:

- `knowledge/stdlib/go-cross-compilation.yaml` — factual guidance
  (`CGO_ENABLED=0` default for cross-compilation), not a prohibition.
- "zero-CGO" as a *library-selection preference* inside catalog fiche
  decision sections — an admission bias, never a ban on writing native code.
- `rules/core/philosophy` decision order: "Prefer the standard library or
  platform capability" — favors native platform APIs.

Conclusion: the "exception" would have no rule to qualify. The intent —
agents must not refuse native Apple APIs for this domain — is served by
explicit positive guidance in the new artifacts, not by modifying existing
ones (user decision, 2026-08-07).

## Primary-source research (2026-08-07)

| Source | Verdict |
| --- | --- |
| Apple Accessibility API (AXUIElement) — developer.apple.com/documentation/accessibility | Live (HTTP 200); primary semantic UI layer |
| Apple AX overview (archive) — developer.apple.com/library/archive/.../cocoaAXOverview.html | Live (HTTP 200) |
| Apple ScreenCaptureKit — developer.apple.com/documentation/screencapturekit | Live (HTTP 200); visual-perception layer |
| github.com/go-vgo/robotgo | Active: v1.0.0 (2025-12-04), v1.0.2 (2026-03-30), v2.0.0-beta2 (2026-07-29); Apache-2.0; 10.7k★; CI `.github/workflows/go.yml`; 9 `_test.go`; 105 `.go`. macOS: cgo by default (`robotgo_mac.go`, CoreGraphics `import "C"`), purego opt-in via `-tags purego` ("no Xcode required", `CGO_ENABLED=0` compatible) |
| progrium/darwinkit (ex-macdriver) | Main Go AXUIElement binding (cgo, .m files, 2,886 files) but **stale**: last release v0.5.0 (2024-07-11), last commit 2024-07-15 → fails "actively maintained"; NOT admitted; referenced in the pattern with the caveat |
| robotn/gohook | Event *listening* only (not input synthesis); v1.0.0-beta1 (2026-07-07) → not the execution layer |

## Decisions (user, 2026-08-07)

1. RobotGo: **vetted fiche** in `catalogs/libraries/robotgo/SKILL.md`.
2. CGO/Objective-C intent: **positive guidance** in the new artifacts; no
   existing artifact modified.
3. Scope: **architecture pattern + library fiche**; no runnable recipe
   (no cgo code enters the kit gate; user asked for official references).
4. darwinkit: mentioned in the pattern only, with stale-maintenance caveat
   (decision derivable by analysis — no user question).

## Constraints

- English mandatory for all kit instruction surfaces (D-2026-08-05-21,
  wave D-2026-08-06-01). Artifacts are written in English.
- No new category: the pattern lives in the existing `architecture/`
  domain; the fiche in `catalogs/libraries/` (both already indexed).
- `knowledge/INDEX.md` needs no change (no new domain).
- `capabilities.yaml` `product_skills` 72 → 73 (one new catalog fiche).

## Done

- [x] `KitV2/knowledge/architecture/macos-computer-use.yaml` (Pattern,
      id `pattern:architecture:macos-computer-use`, Z2 §3 pattern schema,
      Apple + RobotGo references, native-API guidance, darwinkit caveat).
- [x] `KitV2/knowledge/catalogs/libraries/robotgo/SKILL.md` (vetted fiche,
      N1 §4 six mandatory decision sections, 9-criteria admission with
      actual reasons, precise cgo-default / purego-tag facts).
- [x] Router index regenerated (`build_index.py --check` PASS).
- [x] `capabilities.yaml` `product_skills: 73`.
- [x] Full gate: validate-instructions, validate-kitv2, cognitive, Go gate
      (gofmt/vet/lint/test), probes — PASS.
- [x] Fresh-context review before completion.
- [x] Memory: Decisions.md decision + Progress.md + plan pointer.

## Validation evidence

`docs/evidence/2026-08-07/computer-use-macos/` — raw GitHub/Apple API data.
