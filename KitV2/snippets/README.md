# Snippets

A snippet is a metadata-bearing example, not an unexplained code fragment.
Each entry declares its stable id, purpose, context, dependencies, Go floor,
tags, complexity, source module, complete example, test/check, and limits.

Canonical code remains in `rules/` or `recipes/`; snippets are focused views
that link back to that source and must not become a second implementation.

## Roadmap

The following categories remain planned and intentionally contain no snippet:

| Category | Admission criterion |
| --- | --- |
| `cli/` | Admit a focused CLI fragment with a canonical recipe or rule and an executable check. |
| `cloud/` | Admit only a small cloud boundary with a primary source and an observable check. |
| `concurrency/` | Add only when the existing bounded-worker view does not answer a distinct question. |
| `database/` | Add only for a distinct database operation not covered by the recipes. |
| `networking/` | Add only for a focused network boundary with error and cancellation checks. |
| `security/` | Add only for a distinct security implementation linked to canonical guidance. |
| `testing/` | Add only for a distinct test seam or assertion pattern with executable proof. |
