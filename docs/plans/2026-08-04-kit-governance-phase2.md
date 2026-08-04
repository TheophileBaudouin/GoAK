# Plan — Phase 2 : contrats de gouvernance du Kit + nettoyages approuvés

- **Date :** 2026-08-04
- **Référence :** `docs/research/2026-08-04-kit-audit-governance.md` (audit phase 1)
- **Décisions propriétaire :** `.pi/memory/Decisions.md` (2026-08-04, deux sections)
- **Objectif :** rendre le Kit gouvernable à long terme — chaque zone possède un
  contrat MetaProjet lisible par n'importe quel agent avant d'y travailler.

## Goal

Créer les contrats de construction du Kit (metaprojet uniquement, jamais dans le
produit), exécuter les nettoyages approuvés par le propriétaire, et laisser la
gate du Kit verte.

## Context

L'audit phase 1 a identifié 6 problèmes systémiques : contrats de dossier absents,
manifests dérivants, formats mixtes non contractés, placeholders sans contrat,
index manuels obsolètes, validateur qui vérifie la forme sans le contrat. La
phase 2 corrige la cause racine (contrats écrits + nettoyages actés) sans
réarchitecturer le produit.

## Constraints

- Contrats = MetaProjet uniquement → `.agent/kit-governance/` (control-plane),
  jamais `KitV2/`. Le produit reste autonome (aucune référence au metaprojet
  dans `KitV2/AGENTS.md`).
- Nettoyages limités à ceux **explicitement approuvés** (Decisions.md) :
  suppression `embeddings/`, suppression `tools/analyzers/`, renommage
  `rules/core/rules/universal` → `rules/core/universal`, création du contrat de
  domaine `knowledge/debugging/`, marquage `legacy` des squelettes templates.
- Politique templates (directive propriétaire) : jamais de template écrit par un
  agent ; forks légers de projets open source MIT fonctionnels.
- Gate du Kit doit rester verte après les nettoyages : `validate-kitv2.py`,
  `go test ./...`, `gofmt -l`, `go vet ./...` (golangci-lint/gosec/govulncheck
  si dispo, sinon PARTIAL documenté).
- Un seul writer ; revue fresh-context avant déclaration de fin.

## Done

1. `Decisions.md` et rapport d'audit §4.7 reflètent toutes les décisions
   (dont directive templates MIT).
2. Nettoyages approuvés exécutés et gate verte (ou PARTIAL documenté).
3. 15 contrats créés sous `.agent/kit-governance/` (C0–C2, Z1–Z10, A1, N1),
   gabarit commun (mission / format / règles actionnables / patterns /
   anti-patterns / critères de validation / questions ouvertes), Z5 = politique
   templates MIT.
4. Frontmatter des 5 skills `.pi/skills/` complété (décision 3).
5. Revue fresh-context effectuée ; remarques intégrées ou tranchées.
6. Mémoire mise à jour (Progress, Brief, Gotchas si nécessaire) et évidence
   enregistrée sous `docs/evidence/2026-08-04/kit-governance-phase2/`.

## Étapes

1. Persister décisions + ce plan (fait en tête de fichier).
2. Nettoyages Kit (suppressions, renommage, README debugging, marquage legacy
   templates) + gate.
3. Rédaction des 15 contrats (ordre : C0, C1, C2, N1, Z1–Z10, A1).
4. Frontmatter `.pi/skills/`.
5. Gate complète + revue fresh-context.
6. Mémoire + évidence.

## Risques

- Renommage `universal` : vérifier les références (`grep core/rules`) et le
  validateur (name == parent).
- Templates legacy : aucun template supprimé, seul le statut change (pas de
  destruction de contenu fonctionnel sans remplacement).
- Volumétrie : 15 contrats — densité exigée (règles actionnables, pas de prose
  de remplissage).
