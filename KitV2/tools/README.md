# Tools

Tools provide product mechanics: deterministic generation, validation, and
offline source resolution. They do not invent or duplicate Kit knowledge.

## Tools

| Tool | Mission | Verification |
| --- | --- | --- |
| `validators/` | Enforce product structure, metadata, relationships, freshness, and packaging gates. | `python3 tools/validators/validate-kitv2.py` and its unittest suite. |
| `offline/` | Resolve the pinned official-source bundle and local Go toolchain without network access. | `go test ./tools/offline/...` and `probes/offline`. |
| `generators/` | Deterministic project-map generator and drift checker (`structure_md.py`, charter Layer 5.1): derives the tree side of a project's `structure.md` and verifies it against the real tree. | `python3 tools/generators/test_structure_md.py`; invoked by `validate-kitv2.py` on every sourced template. |

Tools are read-only with respect to product knowledge during validation. A
mutating generator must document its output, be deterministic, and have a
negative drift check before admission. A new generator is admitted only with
a contract (zone Z7), tests, and a negative drift check.
