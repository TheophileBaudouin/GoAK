---
name: compress
description: "github.com/klauspost/compress v1.19.1 — pure-Go compression library (zstd, s2, flate, gzip, snappy) with zero dependencies. Use when choosing a compression algorithm or replacing stdlib compress/* on performance grounds. Not for formats it does not implement (brotli, lzma, zlib-variants — check per subpackage)."
category: library
tags: [compression, zstd, s2, gzip, flate, performance]
last-verified: 2026-08-05
---

# compress — compression pure Go

## Selection

[`github.com/klauspost/compress`](https://github.com/klauspost/compress)
(v1.19.1, Go 1.24+).

**Why it passes the gate** (actual reason, not stars): **zero direct
dependencies**, pure Go, fuzzed (scorecard fuzzing 10/10, SAST 10/10,
vulnerabilities 10/10) — the strongest security profile among compression
options — and the reference implementation for zstd/S2 in the Go ecosystem
(used by MinIO, Grafana, VictoriaMetrics). Each subpackage is a single focused
codec; the whole is readable by layer.

## Admission checklist

- [x] Actively maintained — v1.19.1 (2026-07-20), push 2026-08-04
- [x] Single responsibility — compression codecs (zstd, s2, flate, gzip, …)
- [x] Idiomatic Go — pure Go, io.Reader/Writer interfaces, no cgo
- [x] Tests present + CI — extensive; fuzzing 10/10, SAST 10/10 (scorecard 7.4)
- [x] Documentation — README per subpackage + benchmarks
- [x] Real-world usage — MinIO, Grafana, VictoriaMetrics, Caddy
- [x] Readable end-to-end — per-codec packages, layered
- [x] Justified by need — the kit had zero compression decision support and no
      zstd option in stdlib; NOT popularity

## Minimal use

```go
// zstd — compression ratio
zw, _ := zstd.NewWriter(&buf); zw.Write(data); zw.Close()
zr, _ := zstd.NewReader(&r);  io.Copy(&out, zr)

// s2 — speed (Snappy-compatible framing, 2x compression of snappy)
w := s2.NewWriter(&buf); w.Write(data); w.Close()
r := s2.NewReader(&buf); io.Copy(&out, r)
```

Compilé et vérifié (roundtrips zstd + s2) avec v1.19.1 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `compress/gzip`, `compress/flate` | Correct pour l'interopérabilité gzip ; performances et ratio inférieurs (gzip) — préférer compress/gzip pour la compat, klauspost pour la perf mesurée. |
| `github.com/klauspost/pgzip` | Couche parallèle gzip séparée ; intégrée dans klauspost/compress (gzip est parallélisable via `pgzip` subpackage). |
| `compress/brotli` (andybalholm) | Format brotli : klauspost/compress ne l'implémente pas ; bibliothèque séparée si le format est requis (cas rares). |
| `github.com/pierrec/lz4` | Format lz4 : subpackage dédié ; préférer s2 pour le ratio à vitesse comparable. |

## Security note

- Historique : 1 advisory **GO-2026-5841 / GHSA-259r-337f-4rfw** — integer
  overflow + écriture hors bornes dans `s2` (versions 1.16.0 → 1.18.6),
  corrigé en **v1.18.7**. Épingler ≥ v1.18.7 ; v1.19.1 sain (vérifié
  2026-08-05, OSV).
- Toujours décoder depuis une source bornée/limitée : décompresser une entrée
  non contrôlée peut amplifier la mémoire (zip-bomb class) — borner la taille
  de sortie quand la source n'est pas de confiance (voir aussi l'advisory
  data-amplification de kin-openapi).
- Codecs fuzzés + govulncheck dans la gate : suivre les advisories s2/zstd.

## Utiliser cette librairie quand

- Besoin de compression zstd ou S2 en Go (ratio zstd, vitesse s2) — hors stdlib.
- Remplacer `compress/gzip`/`flate` **avec un benchmark à l'appui** (gain
  mesuré en ratio ou en latence sur le workload réel).
- Contrainte zéro dépendance / zéro cgo (binaire autonome, embarqué).

## Ne pas utiliser cette librairie quand

- La compatibilité gzip au sens strict suffit et le workload n'est pas
  mesuré : le stdlib est le choix minimal (voir `source:performance:
  compression-selection`).
- Le format requis est brotli/lzma/lz4 (non implémenté ici — bibliothèque
  dédiée).
- Le décodage doit accepter des entrées arbitraires non bornées : borner la
  sortie à la charge de l'appelant, pas du codec.

## Avantages

- Zéro dépendance directe, pure Go, fuzzé : profil sécurité de tête.
- zstd et S2 de référence dans l'écosystème Go (adoption production massive).
- API `io.Reader`/`io.Writer` familière ; parallelisation gzip incluse
  (`pgzip`-style via le package gzip).
- Perf mesurées et documentées par subpackage (benchmarks publiés).

## Inconvénients

- Couverture de formats incomplète : pas de brotli/lzma/lz4 (subpackages
  séparés à choisir ailleurs).
- Le zstd README évolue vite : suivre les releases pour les correctifs de
  sécurité (1 advisory s2 en 2026).
- La surface d'API est large (10+ codecs) : lisible par subpackage, pas
  d'un seul tenant.

## Pièges connus

- Advisory GO-2026-5841 : épingler ≥ v1.18.7 (integer overflow + écriture
  hors bornes dans `s2` sur entrée non contrôlée). Vérifier les versions
  transitives avec govulncheck.
- `s2.Decode` décode un **bloc** Snappy ; un flux framé (sortie de
  `s2.NewWriter`) se lit avec `s2.NewReader` — l'erreur « corrupt input »
  signale ce mélange.
- Ne pas paralléliser manuellement : chaque codec gère déjà l'état interne ;
  utiliser les writers fournis par package.
- La compression n'est pas du chiffrement : pour des données sensibles,
  combiner avec age (voir `source:security:file-encryption`).

## Sources vérifiées

- [klauspost/compress (repo officiel, v1.19.1)](https://github.com/klauspost/compress)
  — vérifié 2026-08-05
- [pkg.go.dev/github.com/klauspost/compress](https://pkg.go.dev/github.com/klauspost/compress)
  — vérifié 2026-08-05
- [Advisory GO-2026-5841 / GHSA-259r-337f-4rfw (s2 OOB, fix 1.18.7)](https://github.com/klauspost/compress/security/advisories/GHSA-259r-337f-4rfw)
  — vérifié 2026-08-05 (sécurité officielle)
- OSV : `github.com/klauspost/compress` 1 advisory corrigé (requête API
  2026-08-05)
- Artefacts internes : `source:performance:compression-selection`,
  `source:security:file-encryption`
