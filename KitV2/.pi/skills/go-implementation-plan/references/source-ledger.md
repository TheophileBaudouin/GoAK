# Source ledger

Record sources for decisions that an agent or reviewer cannot safely infer
from the repository. Prefer primary documentation and the actual tool output.

| Claim or decision | Source | What was checked | Verified | Confidence |
| --- | --- | --- | --- | --- |
| `<Go/API/library claim>` | `<URL or local path>` | `<section, command, or version>` | `YYYY-MM-DD` | `high/medium/low` |

## Rules

- Use Go documentation for language and standard-library behavior.
- Use a library's README, upgrade guide, package docs, and issue history for
  library-specific behavior; do not use stars as evidence.
- Record rejected alternatives and the failing criterion when choosing a
  library, reference project, or architecture.
- Treat a web synthesis as a lead. Reconcile it against the primary source
  before putting the claim in a plan.
