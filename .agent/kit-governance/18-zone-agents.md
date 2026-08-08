# Z9 — Zone `AGENTS.md` product (entry point)

- **Metaproject Contract** — governs `KitV2/AGENTS.md`.
- **Audit report:** §2.10.

## 1. Mission

The product's **single entry point** for a consumer agent: what this Kit is, where each zone lives, how to work, how to verify. It **routes** to contracts and artifacts; it never duplicates them.

## 2. Mandatory content

1. **Zone map**: table zone → one-line mission → pointer (zone README / canonical files).
2. **Source of truth**: where each truth lives (rules, knowledge, recipes, snippets, templates, probes, tools, `.pi/`).
3. **Workflow**: the native resources to use for non-trivial work — the `spec-driven-dev` skill for large-scale transformations, `workflow-memory` for memory, `checklist-*` prompts for reviews (updated 2026-08-05: the former `workflow-clarify → plan → tasks → implement → verify` prompt chain is removed, D-2026-08-05-16).
4. **Validation**: the complete, unambiguous gate — all commands (validator, gofmt, vet, lint, tests, gosec, govulncheck, probes) and the PARTIAL rule when a tool is missing.
5. **Limits**: what the Kit does not claim to cover (full desktop-application wiring (Wails), TUI development beyond the interactive Bubble Tea recipe, Pi discovery internals, non-Go domains).

## 3. Rules

1. **Routing, not duplication**: AGENTS.md contains neither contract bodies nor rule bodies; each zone is described in one line + pointer.
2. **Product autonomy**: the product **never** references the metaproject.
   This covers every shipped file, not only `AGENTS.md`: no control-directory
   paths (`.agent/`), no charter mention (`KIT_CHARTER`), no build-repository
   vocabulary ("metaproject"), no dated decision or audit references
   (`D-20xx-xx-xx-NN`, `KVA-…`), no repository-folder paths (`KitV2/`), no
   governance-contract references (`Z1–Z14`, `A1`, `C2`, `N1`), no `../`
   paths. Enforcement is mechanical: `validate-kitv2.py`
   `check_no_metaproject_paths()` scans every shipped file (the ui-kit
   mirror is excluded except its local-owned `PIN.md`/`scenarios.json`;
   the checker and its test are exempt as they name the markers). A
   consumer copy of the kit is a standalone project with no awareness of
   the build repository — a reference to it is noise that must fail the
   gate.
3. Any zone or contract creation updates the map in the same commit.
4. The listed gate is exact: all commands, or explicitly "PARTIAL if a tool is missing".
5. **Marker-delimited injected sections** (N1 §5.1, D-2026-08-08-12/17): every
   section merged into this file carries its own begin/end markers plus a
   dedicated mechanical check. Today: UI work (sha256 marker,
   `check_ui_kit_pin`), Project Foundation (`<!-- workspace-init section:
   begin/end -->`, `check_workspace_init_placeholder`), User guide
   (`<!-- user guide section: begin/end -->`, `check_consumer_onboarding`).
   A new merge mechanism without markers + check is non-conformant.
6. **Rewrites follow §9**: any rewrite (or structural edit) of this file
   MUST follow the writing protocol in §9, enforced mechanically by
   `check_agents_md_contract` in `validate-kitv2.py` (D-2026-08-08-19).

## 4. Maintenance

- Synchronous update with: zone changes, contracts, gate, prompts.
- Annual freshness review (trigger: C0 freshness audit).

## 5. Patterns

- Map + routing: the agent finds the zone then the zone README, never a 300-line manual.
- "If two files answer the same question, keep one" (already present — preserve it).

## 6. Anti-patterns

- AGENTS.md growing into a manual; duplication of the charter or contracts;
- metaproject path in the product; undocumented partial gate.

## 7. Validation criteria

- [ ] C2: AGENTS.md exists (already verified) and referenced zones exist.
- [ ] C2 (extended): no `../` or `.agent/` reference in AGENTS.md.
- [ ] §9 contract: canonical sections present, size ≤ 16 KiB, no history
  markers — `check_agents_md_contract` (D-2026-08-08-19).

## 8. Open questions

- Should a link to the artifact registry (generated, Z7) be added? (proposal: yes, one line — "the artifact registry is generated and referenced in the map".)

## 9. Consumer AGENTS.md writing protocol (every rewrite)

Derived from the full critique of `KitV2/AGENTS.md` (2026-08-08). Every
edit — especially every rewrite — MUST follow this protocol. A rewrite is a
**restructure**, never an append-only edit.

### 9.1 Canonical structure (order is mandatory)

`# Identity/Scope` → `## Normative levels` (MUST/SHOULD/MAY legend +
vocabulary) → `## User guide` (marker) → `## Non-Negotiable Rules` →
`## Repository map` → `## Task Routing` → `## Project Foundation` (marker)
→ `## UI work — Wails projects` (marker + sha256) → `## Memory` →
`## Validation` → `## Limits` → closing invariants echo.

Rationale (critique §25/§26): the agent first needs the absolute rules, then
the entry procedure (routing), then the conditional rules, then the
references, then the validation. Section titles are canonical: presence and
order of the required headings are mechanically checked by
`check_agents_md_contract`; the three marker sections carry their own checks
(titles + checksums).

### 9.2 Writing rules

1. **Write for execution.** Every line must change or confirm agent
   behavior; descriptive prose belongs in `.pi/docs/GOAK.md`, not here
   (critique §38-R1).
2. **One rule = one decision.** Atomic bullets; never a paragraph carrying
   several independent obligations (critique §31, §38-R2).
3. **Explicit trigger.** "When X is present, MUST do Y", never "For X
   projects, do Y" (critique §38-R3, §10).
4. **Stable normative levels.** Only MUST / MUST NOT / SHOULD / MAY, as
   defined in the file's own legend; do not stack near-synonyms
   ("strongly recommended", "recommended", "should", "prefer") (critique
   §5). The one sanctioned exception is the Project Foundation marker's
   "strongly recommended, never a hard gate", which encodes a deliberate
   gate-vs-recommendation distinction (critique §12).
5. **Prohibitions are explicit.** Dangerous or forbidden behavior is
   written MUST NOT / NEVER (critique §38-R5).
6. **Point, don't duplicate.** The root routes; it never copies a
   specialized rule body. The closing invariants echo is the ONLY
   sanctioned duplication — a deliberate recency anchor (instruction-
   writing research, critique §17, §36).
7. **One canonical source per concept.** If two files answer the same
   question, keep one and replace the other with a pointer (critique §38-R7).
8. **Specialized rules live close to their domain.** UI detail in
   `ui-kit/AGENTS.md`, procedures in recipes, facts in knowledge; the root
   keeps only activation, routing, and cross-cutting invariants
   (critique §33–§36, P0).
9. **Deterministic workflows.** Task → workflow → tool → source →
   validation must be answerable without improvisation (critique §38-R9).
10. **Guards are explicit.** IF condition → rules apply; ELSE → they do
    not. The Wails detection guard is the model (critique §10).
11. **Success claims need proof.** Never claim an unexecuted scenario
    passed; PASS / PARTIAL / FAIL are the only status vocabulary
    (critique §16, §17, §38-R11).
12. **Commands carry context.** The kit validation gate is distinct from a
    consumer project's validation; never present one as the other
    (critique §18, §38-R12).
13. **Instructions are testable.** "How do I know I complied?" must have an
    answer; otherwise the instruction is too vague (critique §38-R13).
14. **No history.** Removed systems, former chains, and dated decisions do
    not belong in operational instructions (critique §20, §14, §38-R14).
15. **No "best practices" substitution.** A precise MUST beats "follow best
    practices" (critique §15, §38-R15).

### 9.3 Rewrite procedure

1. Read this protocol, the current `AGENTS.md`, `ui-kit/AGENTS.md`, and
   `.pi/docs/GOAK.md` (the consistency surface).
2. Preserve every marker-delimited section and its title: User guide,
   Project Foundation, UI work (including the `sha256` checksum comment —
   the hash is the pinned `ui-kit/AGENTS.md` hash, not the section's).
3. Restructure in place; never append new sections at the end of the file.
4. End with the full validation gate and a fresh-context review (charter §6,
   instruction-artifact protocol).

### 9.4 Definition of Done

- All canonical sections present, in the canonical order.
- Size ≤ 16 KiB (Codex truncates at 32 KiB; the budget leaves headroom),
  warning at > 12 KiB.
- No history markers, no "best practices" wording, no metaproject markers.
- Marker sections and the UI checksum intact.
- Gate PASS: validators (instructions, cognitive, kitv2 + unit tests),
  router + UI scenario gates, Go gate, probes.
- Fresh-context review done; GOAK.md / `/goak-help` / banner consistent
  (no command or workflow drift).
- Enforcement: `check_agents_md_contract` (product validator).
