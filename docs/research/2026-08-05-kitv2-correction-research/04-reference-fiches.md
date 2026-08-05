# Rapport de relecture — 3 fiches reference-projects (post-audit 2026-08-05)

Audit des fiches `ardanlabs-service`, `go-starter`, `pagoda` dans
`KitV2/knowledge/catalogs/reference-projects/`.
Contrôle : conformité format extract-only (A1), vivacité des URLs,
actualité des dépôts.

---

## 1. ardanlabs-service

**Fichier :** `KitV2/knowledge/catalogs/reference-projects/ardanlabs-service/SKILL.md`

### Conformité format extract-only (A1)

| Critère | Statut |
|---|---|
| Frontmatter présent (name, description, category, tags, last-verified) | ✅ Conforme |
| Bannière `extract-only: true` explicite | ✅ Conforme |
| Section "What you MAY extract" | ✅ Conforme |
| Section "What you must NEVER copy" | ✅ Conforme |
| Section "How an agent should use this" | ✅ Conforme |
| Section "Verification" | ✅ Conforme |
| Section "Sources vérifiées" | ✅ Conforme |
| Frontière "ne jamais copier" explicite et spécifique | ✅ Conforme — liste K8s/RBAC/deployment assumptions, full tree, vendor/build pipeline |
| Admission appliquée (pas de popularité comme raison) | ✅ Conforme — raison : "starter/template reference, not a Go dependency or a universal architecture" |
| Pas de clonage d'arbre suggéré | ✅ Conforme — "Do not clone the repository wholesale" |

**Verdict : CONFORME**

### URLs + statuts (vérifiés le 2026-08-05)

| URL | Statut HTTP | Vivant ? |
|---|---|---|
| `https://github.com/ardanlabs/service` | 200 | ✅ Vivant |
| `https://github.com/ardanlabs/service/activity` | 200 | ✅ Vivant |
| `https://pkg.go.dev/github.com/ardanlabs/service` | 200 | ✅ Vivant |
| `https://github.com/ardanlabs/service/wiki/Project-Structure` | 200 | ✅ Vivant |

**4 URLs vérifiées — 4 vivantes.**

### Actualité du dépôt

- **Dernier push (API GitHub) :** 2026-07-25T01:16:21Z
- **Dernière mise à jour (API) :** 2026-08-04T15:55:03Z
- **Stars :** 4 103
- **Langage :** Go
- **Licence :** Apache-2.0
- **Créé :** 2017-11-20
- **Dernier commit cité dans la fiche :** `75942ce` (2026-06-22) — cohérent avec l'activité récente
- **Assessment :** Dépôt actif, dernier push il y a 11 jours au moment de l'audit.

### Recommandation

**CONFORME** — La fiche est bien structurée, les URLs sont vivantes, le dépôt est actif. Aucune correction nécessaire.

---

## 2. go-starter

**Fichier :** `KitV2/knowledge/catalogs/reference-projects/go-starter/SKILL.md`

### Conformité format extract-only (A1)

| Critère | Statut |
|---|---|
| Frontmatter présent (name, description, category, tags, last-verified) | ✅ Conforme |
| Bannière `extract-only: true` explicite | ✅ Conforme |
| Section "What you MAY extract" | ✅ Conforme |
| Section "What you must NEVER copy" | ✅ Conforme |
| Section "How an agent should use this" | ✅ Conforme |
| Section "Verification" | ⚠️ Intitulée "Verification outcome" — déviation mineure de nommage, contenu présent |
| Section "Sources vérifiées" | ✅ Conforme |
| Frontière "ne jamais copier" explicite et spécifique | ✅ Conforme — liste Docker/PostgreSQL/SQLBoiler/Swagger stack, generated boilerplate, CI assumptions, generator |
| Admission appliquée (pas de popularité comme raison) | ✅ Conforme — raison : "opinionated Go REST service template", statut "stale reference" |
| Pas de clonage d'arbre suggéré | ✅ Conforme — "consumed as a GitHub template/fork, not as a Go module dependency" |
| Stagnation explicitement signalée | ✅ Conforme — "effectively stagnant" dans la description et les tags |

**Verdict : CONFORME** (déviation mineure de nommage "Verification outcome" vs "Verification", mais le contenu et la frontière "ne jamais copier" sont respectés)

### URLs + statuts (vérifiés le 2026-08-05)

| URL | Statut HTTP | Vivant ? |
|---|---|---|
| `https://github.com/allaboutapps/go-starter` | 200 | ✅ Vivant |
| `https://github.com/allaboutapps/go-starter` (API metadata) | 200 | ✅ Vivant |
| `https://github.com/allaboutapps/go-starter/commits/master` | 200 | ✅ Vivant |
| `https://github.com/allaboutapps/go-starter/issues` | 200 | ✅ Vivant |
| `https://raw.githubusercontent.com/allaboutapps/go-starter/master/CHANGELOG-go-starter.md` | 200 | ✅ Vivant |

**5 URLs vérifiées — 5 vivantes.**

### Actualité du dépôt

- **Dernier push (API GitHub) :** 2025-10-16T09:54:22Z
- **Dernière mise à jour (API) :** 2026-07-30T08:32:06Z (probable bump de compteur/stars, pas de code)
- **Dernier tag cité :** `go-starter-2025-10-16` / `25.10.0`
- **Stars :** ~3k (non extrait précisément de l'API)
- **Langage :** Go
- **Licence :** MIT (d'après la page)
- **Créé :** 2020-05-08
- **Assessment :** Dépôt stagnant — aucun commit de code depuis octobre 2025 (~10 mois). La fiche le signale explicitement comme "stale reference".

### Recommandation

**CONFORME** — La fiche est conforme au format extract-only. La stagnation est correctement signalée. La section "Verification outcome" devrait être renommée "Verification" pour une cohérence stricte avec le contrat A1, mais ce n'est pas bloquant. Pas de correction structurelle requise.

---

## 3. pagoda

**Fichier :** `KitV2/knowledge/catalogs/reference-projects/pagoda/SKILL.md`

### Conformité format extract-only (A1)

| Critère | Statut |
|---|---|
| Frontmatter présent (name, description, category, tags, last-verified) | ✅ Conforme |
| Bannière `extract-only: true` explicite | ✅ Conforme |
| Section "What you MAY extract" | ✅ Conforme |
| Section "What you must NEVER copy" | ✅ Conforme |
| Section "How an agent should use this" | ✅ Conforme |
| Section "Verification" | ✅ Conforme |
| Section "Sources vérifiées" | ✅ Conforme |
| Frontière "ne jamais copier" explicite et spécifique | ✅ Conforme — liste Echo/Ent/HTMX/Alpine/DaisyUI/SQLite stack, admin panel beta, full scaffold, generated Ent code, deployment defaults, library choice without independent vetting |
| Admission appliquée (pas de popularité comme raison) | ✅ Conforme — raison : "template/starter, not a library or the default architecture for every Go web project" |
| Pas de clonage d'arbre suggéré | ✅ Conforme — "Do not clone the complete project when only one structural idea is required" |
| Beta admin panel signalé | ✅ Conforme — "admin panel explicitly beta" |

**Verdict : CONFORME**

### URLs + statuts (vérifiés le 2026-08-05)

| URL | Statut HTTP | Vivant ? |
|---|---|---|
| `https://github.com/mikestefanello/pagoda` | 200 | ✅ Vivant |
| `https://github.com/mikestefanello/pagoda/releases` | 200 | ✅ Vivant |
| `https://github.com/mikestefanello/pagoda/issues` | 200 | ✅ Vivant |
| `https://pkg.go.dev/github.com/mikestefanello/pagoda` | 200 | ✅ Vivant |
| `https://github.com/mikestefanello/pagoda/blob/main/README.md` | 200 | ✅ Vivant |

**5 URLs vérifiées — 5 vivantes.**

### Actualité du dépôt

- **Dernier push (API GitHub) :** 2026-07-24T00:04:07Z
- **Dernière mise à jour (API) :** 2026-08-05T08:21:22Z
- **Dernier tag cité :** v0.27.0 (publié 2025-08-04)
- **Stars :** ~2k (non extrait précisément de l'API)
- **Langage :** Go
- **Licence :** MIT
- **Créé :** 2021-12-03
- **Assessment :** Dépôt actif (dernier push il y a 12 jours), mais le dernier tag (v0.27.0) date d'un an (2025-08-04). La fiche signale correctement que "current activity must be rechecked before relying on it as a maintained base".

### Recommandation

**CONFORME** — La fiche est bien structurée, les URLs sont vivantes, la frontière "ne jamais copier" est explicite et nuancée (beta admin panel, library choice vetting). Le décalage entre le dernier push (juillet 2026) et le dernier tag (août 2025) est correctement signalé. Aucune correction nécessaire.

---

## Résumé global

| Fiche | Conformité format | URLs vivantes | Dépôt actif | Verdict |
|---|---|---|---|---|
| ardanlabs-service | ✅ Conforme | 4/4 ✅ | ✅ Actif (push 2026-07-25) | **CONFORME** |
| go-starter | ✅ Conforme (⚠️ nommage "Verification outcome") | 5/5 ✅ | ⚠️ Stagnant (push 2025-10-16) | **CONFORME** |
| pagoda | ✅ Conforme | 5/5 ✅ | ✅ Actif (push 2026-07-24) | **CONFORME** |

**Total URLs vérifiées : 14 — 14 vivantes (200/302).**
**Total fiches : 3 — 3 CONFORMES au format extract-only (A1).**

### Points d'attention

1. **go-starter** : la section est intitulée "Verification outcome" au lieu de "Verification" — déviation mineure du contrat A1. À renommer pour cohérence stricte.
2. **go-starter** : le dépôt est stagnant (10 mois sans commit code). La fiche le signale, mais il serait bon de revoir la fréquence de re-vérification pour ce type de référence.
3. **pagoda** : le dernier tag date d'un an, bien que le dépôt ait des pushes récents. La fiche le signale correctement.
4. **Aucune des 3 fiches** n'utilise la popularité (stars) comme raison d'admission — toutes utilisent des critères qualitatifs (rôle, maintenance, usage).
