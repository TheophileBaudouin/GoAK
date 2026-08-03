# Evidence record

Copy this record into the approved task, release, or review artifact.

```markdown
## Criterion: <short name>

- Starting state: `<environment, fixture, or command state>`
- Check: `<exact mechanical command>`
- Check result: `PASS | FAIL | BLOCKED`
- User action: `<exact command or interaction>`
- Expected: `<observable output, response, or persisted state>`
- Observed: `<actual output, response, or persisted state>`
- Behavior verdict: `PASS | PARTIAL | FAIL | BLOCKED`
- Evidence: `<log, response body, screenshot, or artifact path>`
- Residual risk: `<none or precise uncertainty>`
```

## Reporting order

1. Report the first failed mechanical command verbatim.
2. Report behavior criteria independently from mechanical checks.
3. State missing tools, skipped actions, and environment differences.
4. Add a follow-up task for every unresolved blocker; never delete a failed
   criterion or replace it with a claim that the code looks correct.
