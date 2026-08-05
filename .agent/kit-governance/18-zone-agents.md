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
5. **Limits**: what the Kit does not claim to cover (Wails, TUI, Pi discovery).

## 3. Rules

1. **Routing, not duplication**: AGENTS.md contains neither contract bodies nor rule bodies; each zone is described in one line + pointer.
2. **Product autonomy**: AGENTS.md **never** references the metaproject (`.agent/`, `docs/`, `../` paths). Governance contracts are for contributors, via the metaproject.
3. Any zone or contract creation updates the map in the same commit.
4. The listed gate is exact: all commands, or explicitly "PARTIAL if a tool is missing".

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

## 8. Open questions

- Should a link to the artifact registry (generated, Z7) be added? (proposal: yes, one line — "the artifact registry is generated and referenced in the map".)
