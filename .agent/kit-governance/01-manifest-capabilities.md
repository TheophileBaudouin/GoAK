# C1 — Manifest and capabilities (contract of the two root files)

- **Metaproject Contract** — governs `KitV2/manifest.yaml` and `KitV2/capabilities.yaml`.
- **Audit report:** §2.9.

## 1. Mission

`manifest.yaml` and `capabilities.yaml` describe the product's **identity** and **capabilities**. They are machine metadata, **never** instruction entries for the consumer agent (`metadata_role` field already present — it stays mandatory). Together they answer: "what is this product, which version, what can it do, where does each capability live, what are its known limits?"

## 2. Responsibilities (single source of truth per truth)

| Truth | Single owner | The other file |
| --- | --- | --- |
| Identity (name, version, schema_version, language, principles, avoid) | `manifest.yaml` | does not repeat it |
| Capability list | `manifest.yaml` (`capabilities:`) | details it with source + status |
| Capability → path mapping (`canonical:`) | `manifest.yaml` | `capabilities.yaml` (source + status) — **verified coherent** |
| Coverage counts | **no file** — derived by `tools/generators/` (target state: directory to create, Z7), verified by C2 | never hardcoded |
| Known limits | `capabilities.yaml` (`known_limits`) — `id`/`impact`/`status` structure = **target state** (currently prose, to migrate) | — |

## 3. Actionable rules

1. Every declared path (`canonical:`, `source:`) must exist in the Kit.
2. `manifest.capabilities` and the keys of `capabilities.yaml` are the same vocabulary: same name, same separator (kebab-case), no alias.
3. `coverage.*` is **forbidden hardcoded**: the validator recomputes it from the tree and compares (product_skills = SKILL.md of rules + recipes + knowledge/catalogs; rules = number of rules modules; recipes = number of recipes; probes = number of discovered probes; project_templates = number of shapes).
4. `known_limits` is a structured list (**target state**: the current file is still prose — planned migration): each entry has `id`, `impact`, `status` (`open`/`resolved`/`accepted`); an `open` limit downgrades the corresponding capability to `partial`.
5. Modifying a canonical path = modifying both files **in the same commit**; C2 verifies coherence.
6. `schema_version` increments on any schema break of the two files.

## 4. Patterns

- Explicit `metadata_role` ("product manifest, not a Pi instruction entrypoint") — keep.
- Honest capability status: `complete` / `partial` / `proposed` — never `complete` when a required scenario is missing or a known limit is open.

## 5. Anti-patterns

- Hardcoded counts (measured drift: 33 vs 45 on 2026-08-04).
- Two files describing the same mapping without cross-check.
- Capability declared without capability source or verification criterion.
- `known_limits` as unstructured prose (not trackable).

## 6. Validation criteria (C2)

- [ ] Declared paths exist.
- [ ] Identical manifest↔capabilities vocabulary.
- [ ] Recomputed counts == displayed counts (zero hardcoded count).
- [ ] Every capability has `source` + `status` + verification criterion.
- [ ] `known_limits` structured and coherent with statuses.

## 7. Open questions

- Should the manifest `principles` be verified as a subset of the core rules? (proposal: yes, via Z1/C2.)
