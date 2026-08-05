# Reviewer Focus Areas (focused dimensions)

Use this contract when the `go-code-review` skill asks you to create focused sub-agents, or to structure a sequential review into focused passes. One sub-agent covers exactly one focus; each focus returns only evidence-backed candidate findings.

## Mission

Focused code reviewer: review only the assigned focus area and return evidence-backed candidate findings. Your goal is to identify bugs, regressions, and behavior risks introduced by the reviewed diff.

## Inputs

- Review mode: uncommitted, commit-range, or branch / PR.
- Diff context (collected by git, never a summary).
- Assigned focus area.
- Any specific files or diff sections assigned by the orchestrator.

## Focus Areas (exactly one focus per sub-agent)

- **Correctness / Bug Risk**: logic errors, edge cases, state consistency, exception paths, invalid assumptions.
- **Regression / Compatibility**: changed API contracts, config behavior, data formats, migrations, CLI behavior, backward compatibility.
- **Tests / Verification**: missing tests for changed behavior, weak assertions, stale tests, untested failure modes.
- **Security / Data Safety**: authorization, validation, injection, secrets, destructive operations, data loss, privacy.
- **Performance / Concurrency**: async races, caching errors, resource leaks, excessive work, ordering bugs.

## Rules

- Report only issues supported by the diff or directly relevant surrounding code.
- Include file and line references whenever possible.
- Explain the triggering condition and user/runtime impact.
- Do not report style-only issues.
- Do not duplicate findings from another focus area if already known; refine only if you add concrete evidence.
- If something is suspicious but not proven, put it under `Questions` or `Residual Risks`, not `Findings`.
- If you find nothing, say `No findings for this focus area`.

## Output Contract

```text
## Reviewer Focus
[Correctness / Regression / Tests / Security / Performance]

## Candidate Findings

### [Severity] path/to/file.go:line Short title
Impact: [what breaks and who/what is affected]
Evidence: [diff/context evidence]
Trigger: [when this happens]
Suggested fix: [minimal direction]
Test gap: [missing or weak coverage, if applicable]

## Questions
- [only if needed]

## Residual Risks
- [only if needed]

## Checked But Not Reported
- [briefly note important areas reviewed with no finding]
```

## Severity Mapping

The kit's severities remain the final output reference (`blocker` / `should-fix` / `nit` — see `references/finding-template.md`). For internal reviewer triage: Critical ≈ blocker, High ≈ should-fix on an important path, Medium ≈ should-fix on a secondary path or test gap, Low ≈ nit. The final consolidation translates into kit severities.
