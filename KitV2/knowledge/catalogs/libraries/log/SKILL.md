---
name: log
description: "charm.land/log/v2 — minimal, colorful, slog-compatible Go logging library with levels and caller reporting. Use when a CLI/TUI wants human-readable colored logs while keeping the standard log/slog handler interface."
category: library
tags: [logging, slog, tui, cli, terminal]
last-verified: 2026-08-04
---

# log — Colorful slog-compatible logging

## Selection

[`charm.land/log/v2`](https://github.com/charmbracelet/log) (v2).

**Why it passes the gate** (actual reason, not stars): it implements the
standard `log/slog.Handler` interface, so it is a drop-in colored handler for
the kit's mandated `slog` logging story — no logging paradigm change, just a
handler swap. Small, readable, zero magic; the default for Charm CLIs.

## Admission checklist

- [x] Actively maintained — v2.0.x (2026)
- [x] Single responsibility — colored human-readable log handler
- [x] Idiomatic Go — implements `slog.Handler`
- [x] Tests present + CI — yes
- [x] Documentation — README + charm.sh docs
- [x] Real-world usage — Gum, Soft Serve, and other Charm CLIs
- [x] Readable end-to-end — yes, tiny core
- [x] Justified by need — adds color/caller to slog with zero API change

## Minimal use

```go
import slog "log/slog"
import charmLog "charm.land/log/v2"

slog.SetDefault(slog.New(charmLog.New(charmLog.WithTimeFormat(time.Kitchen))))
slog.Info("server started", "port", 8080)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| zap / zerolog | Structured JSON-first; overkill for human-facing CLI logs. Fine when logs feed a pipeline — then keep them instead. |
| Standard slog text handler | Correct default; add charm log only when colored human output matters (CLI/TUI). |

## Notes

- Kit rule `logging` mandates `slog` as the interface: charm log is a handler,
  not a replacement — code keeps using `slog`.
- `WithReportCaller()` adds file:line; keep it off in perf-sensitive paths.

## Utiliser cette librairie quand

- Une CLI/TUI veut des logs colorés lisibles par un humain tout en gardant
  l'interface standard `log/slog.Handler`.
- Le handler slog par défaut est correct mais la sortie colorée/calmer
  compte pour l'expérience utilisateur.

## Ne pas utiliser cette librairie quand

- Les logs alimentent un pipeline JSON : garder zap/zerolog (ou slog JSON
  handler) — pas un handler coloré.
- La sortie doit rester du texte plat non coloré : le handler slog standard
  suffit.

## Avantages

- Implémente `slog.Handler` : drop-in, zéro changement de paradigme de
  logging (la règle kit `logging` reste l'interface).
- Petit, lisible, sans magie — défaut des CLIs Charm.
- `WithReportCaller()` pour file:line.

## Inconvénients

- Orienté humain : pas fait pour des pipelines JSON volumineux.
- Coloration = codes ANSI : à neutraliser quand la sortie est pipée
  (notty/CI).
- Utile seulement quand la lisibilité humaine prime.

## Pièges connus

- Ne pas remplacer slog par charm log : c'est un handler, le code continue
  d'utiliser `slog`.
- Couper `WithReportCaller()` sur les chemins sensibles à la perf (coût
  file:line).
- Sortie pipée : désactiver la couleur (notty) pour éviter les codes
  parasites dans les logs/CI.

## Sources vérifiées

- [charmbracelet/log (repo officiel, v2)](https://github.com/charmbracelet/log)
  — vérifié 2026-08-04
- [pkg.go.dev/charm.land/log/v2](https://pkg.go.dev/charm.land/log/v2) —
  vérifié 2026-08-04
- Artefact interne : règle kit `logging` (slog par défaut)
