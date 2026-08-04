---
name: testify
description: "stretchr/testify — assert/require/mock test helpers for Go. Use when writing tests that benefit from fluent assertions, but prefer stdlib testing for simple cases. Covers require vs assert and table-driven composition."
category: library
tags: [testing, assert, require, mock]
last-verified: 2026-08-04
---

# testify — test assertions

## Selection

`stretchr/testify` (26k★, pushed 2026-07, CI multi-Go with race, maintained at v1
— no breaking changes accepted, v2 under discussion). The most widely used Go
test-helper toolkit: `assert`, `require`, `mock`, `suite`.

**Actual reason (not stars):** it removes the boilerplate of
`if got != want { t.Errorf(...) }` with readable, composable assertions, and its
function-typed assertions (`ComparisonAssertionFunc`) are purpose-built for
table-driven tests.

## require vs assert — the one rule

| Package | On failure | Use when |
|---|---|---|
| `require` | calls `t.FailNow()` — **stops the test** | A later assertion DEPENDS on this one (e.g. `require.NoError(err)` before using the result) |
| `assert` | calls `t.Errorf` — **continues** | You want to see ALL failures in one run |

Default to `require` for setup/decoding errors (nothing after is meaningful if
they fail); `assert` for independent checks within one test.

```go
require.NoError(t, err)            // stop if setup failed
assert.Equal(t, want, got, "msg") // collect independent failures
```

## Table-driven composition

```go
tests := []struct {
    name string
    in, want int
    assert assert.ComparisonAssertionFunc
}{
    {"add", 4, 4, assert.Equal},
    {"not five", 4, 5, assert.NotEqual},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        tt.assert(t, tt.want, add(tt.in))
    })
}
```

## Mock limits (issue-mined — the #1 pain point)

`testify`'s assert/require are solid; **`mock` is limited** — know before you reach for it:

- **No dynamic returns based on call args** (#350, the most-upvoted open issue, 59👍).
  You cannot return a value computed from the arguments the mock was called with.
- **`assert.Equal` can OOM on large/protobuf types** (#930, 23👍) — deep comparison
  on heavy types explodes. Use a custom comparator (#1204) or compare only the
  fields you care about.

For dynamic mock behaviour or heavy value types, prefer a **hand-written fake**
(a tiny struct implementing the interface) over `testify.Mock`. Keep assert/require
for simple value checks.

## When to prefer stdlib `testing` alone

- Trivial checks (`if err != nil { t.Fatal(err) }`) — a dependency for one line is overkill.
- Strict dependency policy / minimal external code.
- Benchmarks where reflection/interface-conversion overhead matters.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `testing` only | The correct minimal choice — use it until testify's leverage pays. |
| `stretchr/suite` | Adds xUnit-style setup/teardown; only if you need that structure — most Go code stays with plain functions + table-driven. |
| `matryer/moq` / mockery | Mock generation tools; orthogonal to assertions, compose fine with testify's `mock`. |

## Utiliser cette librairie quand

- Des assertions lisibles et composables réduisent le boilerplate
  (`if got != want { t.Errorf(...) }`).
- Des tests table-driven avec assertions fonctionnelles
  (`assert.ComparisonAssertionFunc`) sont visés.
- La distinction `require` (arrêt) / `assert` (continuation) clarifie la
  sémantique des tests.

## Ne pas utiliser cette librairie quand

- Un contrôle trivial suffit (`if err != nil { t.Fatal(err) }`) : stdlib
  testing seul, sans dépendance pour une ligne.
- Un mock au comportement **dynamique** (retour calculé selon les args) est
  requis : `testify.Mock` ne le supporte pas (#350) — préférer un fake
  manuel.
- Des types lourds/protobuf doivent être comparés en profondeur :
  `assert.Equal` peut OOM (#930) — comparateur custom ou champs ciblés.

## Avantages

- Assertions lisibles et composables, table-driven naturelles.
- `require` vs `assert` : une règle claire (setup → require, checks
  indépendants → assert).
- Le toolkit de test Go le plus utilisé (26k★, v1 stable, CI multi-Go avec
  race).

## Inconvénients

- `mock` limité : pas de retours dynamiques selon les args (#350, top issue
  ouverte 59👍) ; OOM possible sur comparaisons profondes lourdes (#930).
- Dépendance externe : à justifier dès que stdlib suffit.
- `suite` (xUnit-style) : pas adapté à la plupart du code Go (fonctions
  plates + table-driven).

## Pièges connus

- Par défaut `require` pour setup/decoding (rien après n'a de sens si ça
  échoue) ; `assert` pour les vérifications indépendantes.
- Pour du comportement mock dynamique ou des types lourds : fake manuel
  (petit struct implémentant l'interface) plutôt que `testify.Mock`.
- Garder assert/require pour les vérifications de valeurs simples.

## Sources vérifiées

- [stretchr/testify (repo officiel)](https://github.com/stretchr/testify) —
  vérifié 2026-08-02
- [Issue #350 — dynamic mock returns](https://github.com/stretchr/testify/issues/350)
  / [#930 — Equal OOM](https://github.com/stretchr/testify/issues/930) —
  vérifiées 2026-08-04 (issues officielles)
- Artefacts internes : `pattern:testing:table-driven`,
  `pattern:testing:fakes-over-mocks`, `pattern:testing:seam-injection`
