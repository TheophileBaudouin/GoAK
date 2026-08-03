---
name: govulncheck
description: "govulncheck — the official Go vulnerability scanner. Part of the kit's mandatory validation gate. Use when checking dependencies for known CVEs, integrating vuln scanning in CI, or interpreting reachability (called vs merely present)."
category: rule
tags: [validation, security, vulnerabilities, govulncheck, ci]
last-verified: 2026-08-02
---

# govulncheck — the kit's vuln scanner

## Role in the kit

`govulncheck` (golang/vuln, official Go security team, ~500★ — admitted on the
**real reason**: it is the official Go tool backed by the curated Go vuln DB, not
on stars) is a **mandatory validation tool**: every registry example must report
`No vulnerabilities found.`

## Called vs merely present (the crucial distinction)

`govulncheck` does **source analysis with a call graph** (SSA + CHA/VTA). It
reports three tiers — read them differently:

| Tier | Meaning | Action |
| --- | --- | --- |
| **Symbol Results** | Your code actually CALLS the vulnerable function (reachable) | Fix immediately — real exposure |
| **Package Results** | Vulnerable package imported but function not called | Lower risk; fix when convenient |
| **Module Results** | Vulnerable module in `go.mod`, not imported | Tracked; usually safe until you import it |

Use `-show verbose` to see package/module tiers; the default focuses on Symbol
Results (the ones that matter). Do **not** panic over every dependency CVE —
reachability is what counts.

## CI integration

```sh
govulncheck ./...                       # exits non-zero if vulns found → fails CI
govulncheck -format json ./... > vuln.json   # machine-readable; exits 0 (for downstream tools)
govulncheck -format sarif ./...              # GitHub code scanning upload
```

Note the exit-code asymmetry: text mode fails CI on findings; `json`/`sarif`/
`openvex` exit 0 so downstream tooling can process results.

## Gotchas

- Run against the **module** (`./...`), not a single binary, for source-mode
  reachability. Binary mode uses the symbol table — less precise.
- Reachability is only as good as static analysis — reflective/dynamic calls may
  be missed. Treat "Package Results" as latent risk, not zero risk.
- The Go vuln DB is curated; private/unlisted advisories won't appear. It is a
  signal, not a guarantee.
