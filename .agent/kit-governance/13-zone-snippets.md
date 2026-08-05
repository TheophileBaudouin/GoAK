# Z4 — Zone `snippets/` (verified views of canonical implementation)

- **Metaproject Contract** — governs `KitV2/snippets/`.
- **Audit report:** §2.5.

## 1. Mission

**Metadata-bearing, verified code fragments linked to a canonical source** (recipe, rule, or pattern). A snippet is never a second implementation: it is a focused view of code that lives canonically elsewhere.

## 2. Snippet structure

```text
<subject>/
├── SNIPPET.yaml   # metadata
├── example.go     # compiling, self-contained fragment
└── check.sh       # EXECUTING verification (compile + run/assertions)
```

## 3. SNIPPET.yaml — mandatory fields (model: `bounded-worker`)

`id`, `type` (domain), `purpose`, `tags`, `go_version`, `dependencies`,
`when_to_use`, `avoid_when`, `source` (**resolved relative path** to the
canonical recipe/rule/pattern), `complexity`, `files`, `tests`,
`last_verified` (**recommended** since 2026-08-05, D-2026-08-05-11: serves
the cross-file C2 check — the snippet must be re-verified when its canonical
source changes).

## 4. Rules

1. **`source` mandatory and resolved**: C2 verifies that the path exists and points to a canonical artifact; an orphan snippet is a failure.
2. **`check.sh` actually executes**: at minimum compilation + execution of the fragment (or assertions) — a check that only verifies `gofmt` is insufficient (regression detected at audit: `errors-once/check.sh`).
3. Snippets do not replace the taxonomy: the category = graph domain (concurrency, database, http, …). **No empty category**: planned categories live in the roadmap in `snippets/README.md`.
4. A snippet does not introduce new knowledge: if new content is needed, a recipe/pattern hosts it, the snippet points.
5. `go_version` = minimum tested version.

## 5. Maintenance

- **Addition**: compile + executing check.sh green + resolved canonical source + complete metadata + freshness.
- **Modification**: re-run check.sh; verify that the canonical source has not changed shape (otherwise update or remove the snippet).
- **Canonical-source modification**: any change to a recipe/rule/pattern referenced by a snippet `source:` triggers the snippet's re-verification in the same change (bump `last_verified`, update, or removal) — cross-file C2 check by dates (D-2026-08-05-11).

## 6. Patterns

- A snippet = a point of view on an existing artifact, never a new knowledge body.
- Minimal but real check.sh: `go run` + assertions, or `go test` of a throwaway package.

## 7. Anti-patterns

- Orphan snippet; snippet that becomes the reference (drift); check that verifies nothing; empty waiting category; non-compiling code.

## 8. Validation criteria

- [ ] C2: complete SNIPPET.yaml (§3 fields; `last_verified` recommended, not required — the cross-file check ignores missing dates, annexe A of the 2026-08-05-metaproject plan).
- [ ] C2: `source` resolved; `check.sh` compiling **and** executing.
- [ ] Freshness 12/18 months.

## 9. Open questions

- Boundary with `knowledge/stdlib/`: stdlib = doc pointers, snippets = executable code. Is a "question → snippet or stdlib?" routing table useful? (proposal: no — the snippet's L1 description suffices.)
