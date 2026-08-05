# Z11 — Zone `router/` (semantic routing index)

- **Metaproject Contract** — governs `KitV2/router/` (index + consumption README). The builder lives in the metaproject (`.agent/router/`).
- **Origin:** user decisions 2026-08-05 (BM25, versioned JSON, mandatory search, native Pi extension) — plan `docs/plans/2026-08-05-resource-router.md`.

## 1. Mission

The kit's embedded routing index: a **generated artifact** that lets a Pi agent find relevant resources without loading the kit into context. The index routes to source files; it never replaces them.

## 2. Roles and boundaries (inviolable)

| Element | Role | Owner |
| --- | --- | --- |
| `router/index.json` | Generated artifact: resources (id, kind, path, description, tags, terms) | metaproject (builder) |
| `router/meta.json` | Version, index sha256, counts, stopwords | metaproject (builder) |
| `router/README.md` | Consumption doc: read-only, never hand-edited | metaproject (review) |
| `.agent/router/build_index.py` | Builder (build / --check) — outside the kit | metaproject |
| `.pi/extensions/kit-resource-router.ts` | Native Pi tool, read-only | kit (runtime) |
| `.pi/skills/kit-resource-routing/SKILL.md` | Usage skill (when/how) | kit (runtime) |

## 3. Rules

1. **Generated artifact**: `index.json` and `meta.json` are NEVER hand-edited. Any modification of an indexable resource (rules/, recipes/, knowledge/, snippets/, .pi/prompts/, .pi/skills/) requires a builder regeneration then the full gate.
2. **Read-only at runtime**: the extension tool only reads the index. It modifies neither the index, nor the kit, nor the environment.
3. **Index = router only**: every entry points to a real file; the truth content stays the source file.
4. **Determinism**: stdlib Python builder, no network, stable output (sorted by id); `--check` compares and exits non-zero on drift.
5. **Bounded volume**: short descriptions (source: frontmatter), precomputed terms, index ~< 200 KB. The runtime never loads kit file content, only the index.
6. **Context protection**: top-K ≤ 5 (max 8), score threshold, clean zero result rather than noise ("empty > noise" rule).

## 4. Maintenance

- **Add an indexable resource**: the gate (coverage) will fail until the index is regenerated → run `python3 .agent/router/build_index.py` from the metaproject root, verify `git diff` on router/.
- **Modify the system**: builder (metaproject, tests + README) OR runtime (kit, end-to-end scenario); never both in the same responsibility.
- **Test**: builder fixtures + end-to-end pi scenarios (obvious, vague, empty, near-multiple) + full gate.
- **Do not degrade routing**: every new resource must have a real frontmatter description (1..1024 characters, technical vocabulary); no generic description ("useful for Go").

## 5. Patterns

- Deterministic builder + verifying gate (same schema as tools/offline).
- Stopwords in meta.json (single source, no builder/runtime duplication).
- Synonyms only on the runtime side (query expansion), never on the build side.

## 6. Anti-patterns

- Hand-edited index; runtime that writes; index containing file content (instead of descriptions); unfiltered results injected into context; network dependencies in the builder.

## 7. Validation criteria

- [ ] `validate-kitv2.py`: valid index.json, conforming meta.sha256, complete coverage of indexable resources, existing paths.
- [ ] `python3 .agent/router/build_index.py --check`: clean output.
- [ ] End-to-end scenarios: 4 types, no false positive in the assertions.

## 8. Open questions

- None: the scope was arbitrated with the user (2026-08-05).
