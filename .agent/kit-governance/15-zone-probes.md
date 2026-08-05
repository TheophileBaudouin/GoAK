# Z6 — Zone `probes/` (executable product evaluations)

- **Metaproject Contract** — governs `KitV2/probes/`.
- **Audit report:** §2.7.

## 1. Mission

The charter's "product evaluations" layer (Layer 6): **executable, deterministic, LLM-free and external-service-free** scenarios that prove the Kit does what it claims. Each probe ends with an observable verdict and an exit code.

## 2. Probe structure

```text
probes/<subject>/
└── main.go          # self-contained, final verdict: fmt.Println("...: PASS") + exit 0/1
```

- `probes/run.sh` **discovers** probes (glob `probes/*/main.go`) — a hardcoded list is forbidden (regression detected at audit).
- `probes/README.md` = zone contract (how to add, when, criteria).

## 3. Rules

1. A probe exercises a **core recipe** (import, execution) or a **product capability** (offline, tooling) — traced `validated_by` relation.
2. **Determinism**: no external network, no flaky timing, no shared state between executions; local resources (ephemeral port, temporary database) are cleaned up.
3. **Explicit verdict**: the last output line is `…: PASS` (or a clear failure + non-zero exit code); a probe that asserts nothing is an error.
4. Every new "core" recipe is a probe candidate (the C2 gate does not yet require full coverage — the addition is encouraged at recipe admission).
5. Raw outputs belong to metaproject evidence (`docs/evidence/`), never to the product.

## 4. Maintenance

- **Addition**: scenario + assertion + automatic discovery + green gate.
- **Modification of a referenced recipe**: re-running the affected probes mandatory.
- Known limits (Pi discovery, Wails, TUI): remain declared in `capabilities.yaml` (`known_limits`) — a probe does not claim to cover them.

## 5. Patterns

- Probe = "recipe executed in a consumer scenario" (composition, not duplication).
- One `PASS` line + exit code: machine-readable output for CI.

## 6. Anti-patterns

- Probe that passes without asserting; orphan probe; hardcoded list in run.sh;
- network/timing dependency; unstructured raw output.

## 7. Validation criteria

- [ ] C2: run.sh discovers (no hardcoded list).
- [ ] Every probe has an explicit verdict and an exit code.
- [ ] "Core" recipes have a probe (encouraged; to make mandatory when recipe↔probe coverage is tracked by C2).

## 8. Open questions

- How to probe the 3 limits (Pi discovery, Wails, TUI) without harness dependency? (proposal: "doc + manual smoke" probes documented as PARTIAL, never as covered.)
