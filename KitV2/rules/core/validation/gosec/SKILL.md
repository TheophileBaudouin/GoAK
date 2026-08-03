---
name: gosec
description: "gosec — static security analyzer for Go (injections, hardcoded secrets, dangerous crypto, command exec). Part of the kit's mandatory validation gate. Use when reviewing for security issues, configuring gosec rules, or justifying a #nosec suppression."
category: rule
tags: [validation, security, gosec, sast]
last-verified: 2026-08-02
---

# gosec — the kit's security scanner

## Role in the kit

`gosec` (securego/gosec, 8.9k★, pushed 2026-07, CI with self-scan + multi-Go
matrix + SBOM/Docker release) is a **mandatory validation tool**: every registry
example must report `Issues: 0` (or have each finding explicitly justified).

## Default behaviour

All rules are enabled by default. Select a subset with `-include=G101,G204` or
exclude with `-exclude=`. Notable rules:

| Rule | Catches |
| --- | --- |
| `G101` | Hardcoded credentials |
| `G204` | Command execution (`exec.Command` with tainted input) |
| `G304` | File path injection (`os.Open` with tainted path) |
| `G401/G402` | Weak crypto / insecure TLS (`InsecureSkipVerify: true`) |

## Suppressing a false positive — `#nosec` with a reason

Never suppress without a justification — a bare `#nosec` is an anti-pattern.

```go
//#nosec G402 -- test server: self-signed cert, TLS verification intentionally disabled
srv.TLSConfig.InsecureSkipVerify = true
```

Format: `#nosec [RuleList] [-- Justification]`. `//gosec:disable` is the
equivalent directive. Empty rule list suppresses everything on that line — avoid
it; name the rule.

## Common false positives (and why they're still worth a glance)

- `G101` on a constant that looks like a token but isn't sensitive.
- `G402` on `InsecureSkipVerify: true` in **test** TLS configs (justified, suppress).
- `G304` on paths built from trusted config (review, then suppress if truly bounded).

## Integration

- Standalone: `gosec ./...` (exits non-zero on findings).
- In CI: fail the build on `Issues != 0`. Emit SARIF (`-fmt sarif`) for GitHub code scanning.
- Redundant with `golangci-lint`'s built-in gosec — pick one surface to avoid double-noise;
  the kit runs gosec standalone for a dedicated security signal.
