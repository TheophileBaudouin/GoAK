# Finding template

Report only findings that survive a second read of the current diff.

```text
[severity] path/to/file.go:line
Finding: <what is wrong>
Impact: <observable failure, regression, security, or maintenance cost>
Evidence: <test output, caller, contract, or primary source>
Fix: <smallest safe correction>
```

Use these severities:

- `blocker`: breaks required behavior, safety, compatibility, or the validation
  gate; must be fixed before merge.
- `should-fix`: concrete correctness or maintainability issue inside scope; fix
  now when it is small and unambiguous.
- `nit`: optional clarity or style improvement with no known behavior impact.

If there are no findings, say `No evidence-backed findings.` Do not invent a
finding to fill a section.
