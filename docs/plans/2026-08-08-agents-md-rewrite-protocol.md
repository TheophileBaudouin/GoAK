# Plan — Consumer `KitV2/AGENTS.md` rewrite protocol

Date: 2026-08-08 · Owner: metaproject agent · Status: plan

## Goal

1. Put in place metaproject guardrails so every future rewrite of the
   consumer `KitV2/AGENTS.md` follows one protocol derived from the full
   critique of that file.
2. Rewrite `KitV2/AGENTS.md` once, using the critique and the new protocol.

## Context

- `KitV2/AGENTS.md` (12.4 KiB) currently mixes normative, recommendatory,
  informative, descriptive, and procedural content at the same level; embeds
  a complete UI-domain manual (a full mirror of `ui-kit/AGENTS.md`); carries
  historical content (removed prompt chain); buries "routing is mandatory"
  inside a Workflow paragraph; uses loose normative vocabulary; and its
  structure pushes it toward becoming the kit's knowledge repository.
- The critique (40 points) concludes: the content is sound, the architecture
  is not. Fixes are P0 (separate normative levels; delegate UI detail;
  routing as an entry rule), P1 (decompose workflow; stabilize
  MUST/SHOULD/MAY; separate rule/procedure/source/validation), P2 (reduce
  command detail in root; drop history; formalize PASS/PARTIAL/FAIL; atomic
  instructions).
- Authority: `KIT_CHARTER.md` (process), Z9 (zone contract governing
  `KitV2/AGENTS.md`), Z13 (ui-kit zone, merged-section policy), N1 §5.1
  (marker-delimited injected sections), the `agent-instructions` skill
  (recognized reference for writing instruction files), `KIT_CHARTER.md §6`
  instruction-artifact protocol (research first, smallest surface,
  fresh-context review).

## Constraints (mechanical, must keep green)

- `check_consumer_onboarding`: markers + `## User guide` between them.
- `check_workspace_init_placeholder`: markers + `## Project Foundation`
  between them.
- UI section: `<!-- ui-kit/AGENTS.md sha256: <64-hex> -->` marker equal to
  the current `KitV2/ui-kit/AGENTS.md` hash (ae432ca8…).
- `check_no_metaproject_paths`: no `.agent/`, `KIT_CHARTER`, metaproject
  vocabulary, dated decisions `D-20xx-…`, `KVA-…`, `KitV2/`, `Z10`–`Z19`
  references in the product.
- C12 prose-id gate: no unresolved `kind:domain:slug` tokens in AGENTS.md.
- Z9 §2.4: the complete validation gate (all commands + PARTIAL rule) stays
  in the root; Z9 §2.1 zone map stays.
- GOAK.md / `/goak-help` / banner: must remain consistent (no command or
  workflow may change, only the file structure).
- Size budget for the rewrite: target ≤ 12 KiB (current 12.4 KiB, will
  shrink with UI delegation).

## Change scope

Metaproject (guardrails):

1. Z9 — new §9 "Consumer AGENTS.md writing protocol": canonical structure
   (Identity → Normative levels → User guide → Non-Negotiable Rules →
   Repository map → Task Routing → Project Foundation → UI work → Memory →
   Validation → Limits → closing invariants echo), the 15 writing rules
   distilled from the critique, rewrite procedure, Definition of Done.
2. Z13 §4 — change the "merged root AGENTS.md" policy from full mirror to
   condensed delegation: the UI section keeps the activation guard, routing,
   and cross-cutting invariants only; every other UI instruction lives in
   `ui-kit/AGENTS.md` (single source). The checksum marker stays as the
   tripwire (a changed SDK AGENTS.md forces re-verification of the condensed
   section + marker refresh).
3. Root metaproject `AGENTS.md` — compact rule: any rewrite of
   `KitV2/AGENTS.md` MUST follow Z9 §9, preserve the marker sections, stay
   under the size budget, and end with the full gate + fresh-context review.
   Update the "merged agent files never lose instructions" paragraph to the
   delegation policy.
4. `.pi/memory/Agent.md` — same rule, absolute.
5. `.agent/sync-ui-kit-from-upstream.sh` + `.pi/prompts/update-ui-kit.md` —
   wording of the merged-section guardrail follows the delegation policy.
6. `KitV2/tools/validators/validate-kitv2.py` — new `check_agents_md_contract`
   (size budget: error > 16 KiB, warning > 12 KiB; required canonical
   headings; no history markers; no "best practices" substitution) + unit
   tests.

Product (rewrite): `KitV2/AGENTS.md` restructured per the protocol —
normative-level legend, non-negotiable invariants at the top, routing as an
entry rule, workflow selection as guarded bullets, UI condensed to
activation + invariants + delegation, Memory split rule/procedure,
Validation with formalized PASS/PARTIAL/FAIL and kit-vs-consumer scope,
Limits as an out-of-scope table, closing echo of the invariants (the only
sanctioned duplication — recency anchor).

## Gates

- `python3 ../.agent/validators/validate-instructions.py` (metaproject)
- `python3 ../.agent/validators/validate-cognitive.py` (prose-id gate)
- `python3 tools/validators/validate-kitv2.py` + stdlib unittest suites
- `node .agent/router/run_scenarios.mjs` (22 Go scenarios) + UI scenarios
- Go gate (gofmt/vet/golangci-lint/go test -race/gosec/govulncheck) +
  `bash probes/run.sh` — unchanged surface, must stay green
- Fresh-context review (pi-subagents `reviewer`) before completion

## Done

- Guardrails in place (Z9 §9, Z13 §4, root AGENTS.md, Agent.md, helper +
  prompt wording, validator check + tests).
- `KitV2/AGENTS.md` rewritten: canonical structure, all hard rules
  preserved, three marker sections intact, UI delegated, history removed,
  no metaproject markers, gate PASS.
- Dated decision + evidence recorded in `.pi/memory/` and `docs/evidence/`.
