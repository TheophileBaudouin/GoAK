# Rapport — Fiches de référence des 28 bibliothèques du catalogue

Date : 2026-08-04 · Évidence brute : `docs/evidence/2026-08-04/catalog-fiches/evidence.md`

## Décisions (confirmées par l'utilisateur avant toute modification)

1. **Placement** : la fiche enrichit les SKILL.md existants (source unique) —
   un fichier compagnon est exclu : `knowledge/catalogs` est un répertoire de
   skills Pi déclaré (`../knowledge/catalogs` dans `.pi/settings.json`), tout
   .md non-SKILL.md casserait la découverte (Gotcha 2026-08-03).
2. **Intensité** : vérification ciblée + ré-usage des recherches d'admission
   (sources primaires déjà issue-minées, dates récentes 08-02..04) — pas de
   re-recherche complète de zéro.
3. **Gouvernance** : standard « format fiche » encodé dans N1 §4 + Z2 §9.2.

## Fichiers modifiés (28 SKILL.md enrichis)

Chaque fiche ajoute 6 sections après les sections vétées (Selection,
Admission checklist, Minimal use, Alternatives, Notes/Security note) :

- `## Utiliser cette librairie quand` · `## Ne pas utiliser cette librairie
  quand` · `## Avantages` · `## Inconvénients` · `## Pièges connus` ·
  `## Sources vérifiées` (URL + date + type de source)

28/28 fiches complètes, en-têtes FR (spécification utilisateur), contenu
libre, frontmatter intact, ≤ 500 lignes (max 145 : coder-websocket).

Bibliothèques : bleve, bubbles, bubbletea, chi, cobra, coder-websocket,
colorprofile, fyne, glamour, go-git, harmonica, huh, keygen, koanf, lipgloss,
log, mcp-go-sdk, modernc-sqlite, req, ristretto, sequin, sqlc, ssh, templ,
testify, validator, viper, wish.

## Recherches effectuées (vérification ciblée, ré-usage)

- Ré-usage des recherches d'admission (issues officielles : sqlc #3414/#2061/
  #200/#2348, ristretto #43, wish #325, validator #952, go-git #90/#400/#490,
  coder/websocket #402, mcp-go-sdk #328/#148).
- Ré-usage des artefacts knowledge créés précédemment (sec-ip-trust,
  sec-cswsh, db-codegen-dynamic-queries, sec-ssh-host-key-reuse,
  ssh-server-security, ssh-key-generation, websocket-security,
  mcp-tool-security, input-validation, search-index-merge,
  template-compiled-rendering, ssh-metrics, mcp-server-shape,
  go-html-template).
- Vérification par le reviewer : toutes les URLs échantillonnées → HTTP 200.

## Fichiers de gouvernance modifiés

- `N1 §4` (30-conventions.md) : format fiche canonique (6 sections
  obligatoires, critiques ≥ 2 sources indépendantes ou ≥ 1 issue/advisory
  officielle, en-têtes FR, sections préexistantes conservées).
- `Z2 §9.2` (11-zone-knowledge.md) : « Catalog admis = fiche complète ».
- `A1 §2` (20-auteur-modules.md) : row library enrichie (format fiche).
- `KitV2/templates/_kit-skill-authoring.md` : row library enrichie.

## Mémoire mise à jour

- Agent.md : étape fiche ajoutée à la « Library knowledge pipeline ».
- Brief.md (Decisions) + Decisions.md : « Catalog fiche format (2026-08-04) ».
- Gotchas.md : leçon placement (fiche dans SKILL.md, jamais .md compagnon
  dans un répertoire de skills déclaré).

## Revue fresh-context

Subagent reviewer (run c55cee70) : **APPROVE-WITH-NITS** — aucun bloqueur ;
5 nits intégrés : suppression des `## Sources` legacy dupliquées (cobra,
koanf, viper ; URL confmap migrée), citation CVE validator (issue #899 + PR
# 881), bump `last-verified` → 2026-08-04 (10 fichiers), reformulation N1 §4
(multi-source), cross-références A1 + template.

## Problèmes rencontrés

1. Edit multi rollbacké en entier (Gotcha connu) → appliqué en appels
   séparés, vérifié ligne par ligne sur disque.
2. markdownlint auto-fix sur quelques fichiers → relecture avant chaque edit
   suivant.
3. Legacy `## Sources` dupliquées (3 fichiers) détectées par la revue, pas
   par l'exécution — d'où l'intérêt de la revue fresh-context.

## Validation

Gate complète PASS : validate-kitv2.py (51 skills, router 231), validate-
instructions.py, router `--check` OK (inchangé : éditions de corps,
descriptions frontmatter intactes), 28/28 fiches, zéro `## Sources` legacy.
Aucun code Go touché (CI coverage inchangée, état accepté).

## Éléments restants

- `last-verified` des fiches : les 10 fichiers bumpés portent 08-04 ; le
  cycle 12/18 mois revalidera l'ensemble.
- La vérifiabilité C2 du « format fiche » (grep des 6 en-têtes) pourrait être
  automatisée dans validate-kitv2.py — proposé, non implémenté (question
  ouverte Z2 §10).
