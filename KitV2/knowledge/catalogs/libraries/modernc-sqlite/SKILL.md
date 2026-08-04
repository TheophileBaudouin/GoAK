---
name: modernc-sqlite
description: "modernc.org/sqlite — a pure-Go (cgo-free) SQLite driver that cross-compiles with CGO_ENABLED=0. Use when choosing a SQLite driver for Go or deciding cgo vs pure-Go for SQLite."
category: library
tags: [database, sqlite, driver, pure-go, cgo-free]
last-verified: 2026-08-04
---

# modernc-sqlite — SQLite driver (pure Go)

## Selection

[`modernc.org/sqlite`](https://gitlab.com/cznic/sqlite) (v1.55+, BSD-3-Clause).

**Why it passes the gate** (actual reason, not stars): it is a **cgo-free** port
of SQLite — a transpilation of the C source to Go. The binary cross-compiles
natively with `CGO_ENABLED=0`, needing no C compiler or cross-toolchain at
build time. For a kit that must work on any target platform, build portability
beats the marginal raw-throughput edge of the cgo driver.

## Admission checklist

- [x] Actively maintained — ongoing commits and releases in the canonical GitLab repository (`gitlab.com/cznic/sqlite`)
- [x] Single responsibility — implements the SQLite wire/SQL engine as a `database/sql` driver
- [x] Idiomatic Go — registers a driver, used via stdlib `database/sql`
- [x] Tests present + CI — extensive test matrix upstream
- [x] Documentation — package docs + GitLab project
- [x] Real-world usage — adopted where cross-compile/static builds matter
- [x] Readable end-to-end — driver surface is small; engine is large but opaque-by-design
- [x] Justified by need (cgo-free cross-compile), NOT popularity

## Minimal use

```go
import (
    "database/sql"
    _ "modernc.org/sqlite" // registers the "sqlite" driver
)

db, err := sql.Open("sqlite", "file:app.db")   // or ":memory:"
```

The driver name is `"sqlite"`. See `recipe-sqlite-sqlc` for a runnable example.

## The driver decision (cgo vs pure-Go)

| Driver | Trade-off | Verdict |
|---|---|---|
| `modernc.org/sqlite` (pure Go) | No cgo → cross-compiles & static-builds trivially. Slightly slower on some benchmarks, negligible for most services. | **Chosen** — build portability is the deciding criterion for a universal kit. |
| `mattn/go-sqlite3` (cgo) | Faster raw throughput, but requires `CGO_ENABLED=1` + a C compiler, and a full cross-toolchain for cross-builds. | Rejected for the kit. Acceptable in a project that only ever builds on one native platform and needs max throughput. |

Pick the pure-Go driver unless you have measured that SQLite throughput is your
bottleneck AND you can stomach the cgo build constraints.

## Notes

- No `CGO_ENABLED=1` needed — `GOOS=... GOARCH=... go build` just works.
- Backed by `modernc.org/libc` (a Go libc) — several transitive deps, all pure Go.

## Utiliser cette librairie quand

- SQLite en Go avec cross-compilation simple (`CGO_ENABLED=0`, builds
  statiques, cibles multiples sans toolchain C).
- La portabilité de build prime sur le débit brut (la majorité des services).
- Un driver `database/sql` standard (nom de driver `"sqlite"`).

## Ne pas utiliser cette librairie quand

- Le débit SQLite est MESURÉ comme le goulot d'étranglement ET le projet ne
  build que sur une plateforme native : mattn/go-sqlite3 (cgo) peut alors se
  justifier.
- CGO est déjà requis par ailleurs (le cgo driver n'ajoute alors pas de
  contrainte nouvelle).

## Avantages

- Zéro-CGO : `GOOS=... GOARCH=... go build` fonctionne sans compilateur C ni
  cross-toolchain.
- Driver `database/sql` standard, intégration triviale, compatible sqlc.
- Maintien actif (dépôt GitLab canonique, matrice de tests étendue).

## Inconvénients

- Moteur transpilé opaque (modernc.org/libc, plusieurs deps transitives) —
  débugger les bizarreries internes est difficile.
- Légèrement plus lent que le driver cgo sur certains benchmarks (négligeable
  pour la plupart des services — à mesurer si doute).
- Écarts de fonctionnalités possibles vs SQLite C (ex. `UPDATE FROM`) — à
  vérifier par moteur.

## Pièges connus

- Le nom du driver est `"sqlite"` (importer `_ "modernc.org/sqlite"`).
- Vérifier les limites du moteur pur-Go sur les features avancées SQL avant
  de s'y engager (cf. Gotcha sqlc/SQLite).
- Ne pas choisir sur la réputation : la décision cgo vs pur-Go est une
  décision de build, pas de benchmark théorique (mesurer si doute).

## Sources vérifiées

- [modernc.org/sqlite (dépôt GitLab officiel, v1.55+)](https://gitlab.com/cznic/sqlite)
  — vérifié 2026-08-02
- [pkg.go.dev/modernc.org/sqlite](https://pkg.go.dev/modernc.org/sqlite) —
  vérifié 2026-08-02
- Artefacts internes : `recipe-sqlite-sqlc`, catalog `sqlc`
