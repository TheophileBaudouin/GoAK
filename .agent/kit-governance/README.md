# Kit Governance — contrats de construction du Kit (MetaProjet)

Ce dossier est le **control-plane de gouvernance** du produit `KitV2/`. Chaque
contrat définit la mission, le format, les règles, les patterns, les
anti-patterns et les critères de validation d'une zone ou d'un composant du
Kit. Un agent ou développeur doit lire le contrat de la zone **avant** d'y
travailler.

Autorité : `KIT_CHARTER.md` (racine) > ces contrats > README de zone du Kit >
contenu. Ces fichiers ne sont **jamais** installés dans le produit ; le
produit reste autonome (Z9, N1).

## Index

| Contrat | Portée | Statut |
| --- | --- | --- |
| [00-charte-d-application.md](00-charte-d-application.md) | Cycle de vie, semver, write-gate, fraîcheur, règles transverses (C0) | actif |
| [01-manifest-capabilities.md](01-manifest-capabilities.md) | manifest.yaml + capabilities.yaml (C1) | actif |
| [02-validation-gate.md](02-validation-gate.md) | validate-kitv2.py et la gate complète (C2) | actif |
| [10-zone-rules.md](10-zone-rules.md) | `rules/` (Z1) | actif |
| [11-zone-knowledge.md](11-zone-knowledge.md) | `knowledge/` (Z2) | actif |
| [12-zone-recipes.md](12-zone-recipes.md) | `recipes/` (Z3) | actif |
| [13-zone-snippets.md](13-zone-snippets.md) | `snippets/` (Z4) | actif |
| [14-zone-templates.md](14-zone-templates.md) | `templates/` — politique MIT (Z5) | actif |
| [15-zone-probes.md](15-zone-probes.md) | `probes/` (Z6) | actif |
| [16-zone-tools.md](16-zone-tools.md) | `tools/` (Z7) | actif |
| [17-zone-pi.md](17-zone-pi.md) | `.pi/` prompts/skills/settings (Z8) | actif |
| [18-zone-agents.md](18-zone-agents.md) | `AGENTS.md` produit (Z9) | actif |
| [19-registre-artefacts.md](19-registre-artefacts.md) | Gabarit de métadonnées + relations (Z10) | actif |
| [20-auteur-modules.md](20-auteur-modules.md) | Écriture des SKILL.md (A1) | actif |
| [21-zone-router.md](21-zone-router.md) | `router/` — index de routage sémantique (Z11) | actif |
| [30-conventions.md](30-conventions.md) | Nommage, formats, frontières (N1) | actif |

## Origine

- Audit : `docs/research/2026-08-04-kit-audit-governance.md`.
- Plan : `docs/plans/2026-08-04-kit-governance-phase2.md`.
- Décisions : `.pi/memory/Decisions.md` (2026-08-04).
- Évidence : `docs/evidence/2026-08-04/kit-governance-phase2/`.

## Maintenance des contrats

- Modifier un contrat = décision écrite si le périmètre change (nouvelle
  règle, nouveau champ obligatoire) ; typo/reformulation = direct.
- Toute règle nouvelle dans un contrat doit être formulée pour être vérifiable
  par C2 (le validateur) — une règle non vérifiable est une hypothèse.
- Chaque contrat a une section « Questions ouvertes » : résoudre une question
  = décision dans `.pi/memory/Decisions.md` + mise à jour du contrat.
