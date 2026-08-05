# Tools

Tools provide product mechanics: deterministic generation, validation, and
offline source resolution. They do not invent or duplicate Kit knowledge.

## Tools

| Tool | Mission | Verification |
| --- | --- | --- |
| `validators/` | Enforce product structure, metadata, relationships, freshness, and packaging gates. | `python3 tools/validators/validate-kitv2.py` and its unittest suite. |
| `offline/` | Resolve the pinned official-source bundle and local Go toolchain without network access. | `go test ./tools/offline/...` and `probes/offline`. |
| `generators/` | Future home for deterministic index/account generators; no generator is admitted until it has a contract and tests. | Planned; no executable generator is shipped yet. |

Tools are read-only with respect to product knowledge during validation. A
mutating generator must document its output, be deterministic, and have a
negative drift check before admission.
