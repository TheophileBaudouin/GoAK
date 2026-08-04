# Z8 — Zone `.pi/` (settings, prompts, skills de workflow)

- **Contrat MetaProjet** — régit `KitV2/.pi/`.
- **Rapport d'audit :** §2.11. **Décision :** les 5 skills de workflow restent
  dans le produit (2026-08-04).

## 1. Mission

La couche d'exécution native Pi du produit : découverte (settings), invocation
(prompts), procédures de workflow (skills). Trois rôles **disjoints**, zéro
recouvrement.

## 2. Les trois rôles (frontière inviolable)

| Surface | Rôle | Exemple |
| --- | --- | --- |
| `.pi/prompts/*.md` | **Orchestrateurs** invoqués manuellement (`/workflow-plan`) | workflow-clarify, workflow-plan, workflow-implement, workflow-verify |
| `.pi/skills/*/SKILL.md` | **Procédures durables** chargées par contexte | go-code-review, go-idiomatic-implementation, go-implementation-plan, go-source-retrieval, go-testing-verification |
| modules `rules/`, `recipes/`, `knowledge/catalogs/` | **Contenu de connaissance** (découvrable par description) | recipe-worker-pool, chi, philosophy |

Règle : si un prompt et une skill répondent à la même question, on en garde un
et l'autre pointe (anti-duplication C0). Une skill de workflow ne contient pas
de connaissance de domaine (celle-ci vit dans les modules).

## 3. Règles

1. **Toute skill a un frontmatter complet** : `name`, `description` (activation
   explicite), `category: workflow`, `tags`, `last-verified`. Une skill sans
   `description` n'est pas chargée par Pi.
2. **Tout prompt a une `description`** d'activation et suit la convention de
   nommage `workflow-*` / `checklist-*`.
3. `settings.json` charge les modules par chemins relatifs au produit
   (`../rules`, `../recipes`, `../knowledge/catalogs`) — le contrat de chemins
   est documenté dans `.pi/README.md` (à créer) et stable quelle que soit la
   méthode d'installation.
4. Une skill de workflow reste générique au processus (revue, plan, source,
   vérification) : toute spécificité de domaine migre vers un module.
5. `category: workflow` est une valeur kit-only (hors jeu validé des modules) :
   elle ne s'applique qu'à `.pi/skills/` ; les modules gardent les catégories
   A1.

## 4. Maintenance

- **Ajout d'un prompt** : nommage + description + référence à la skill/module
  orchestré s'il existe.
- **Ajout d'une skill** : contrat de zone + recherche d'absence de duplicat
  (sémantique) + frontmatter complet.
- **Modification** : bump `last-verified` ; vérifier la frontière rôle.

## 5. Patterns

- Prompts = courts, orchestrateurs ; skills = procédures ; modules = contenu.
- Activation explicite : « Use only after workflow-clarify … » (déjà en place —
  généraliser).

## 6. Anti-patterns

- Skill de workflow qui contient des connaissances de domaine (dérive).
- Prompt et skill qui se dupliquent (recouvrement de rôle).
- Skill sans description ; prompt sans description.
- Contenu metaprojet (décisions, mémoire) dans `.pi/` produit.

## 7. Critères de validation

- [ ] Toutes les skills `.pi/skills/` ont le frontmatter complet §3.1.
- [ ] Tous les prompts ont une description.
- [ ] Aucun duplicat détecté prompts↔skills↔modules (contrôle manuel à la
      revue ; C2 pourra grepper les titres).

## 8. Questions ouvertes

- Aucune ouverte : le frontmatter des 5 skills `.pi/skills/` (category
  `workflow`, tags, last-verified) a été complété le 2026-08-04 — l'extension
  de schéma est enregistrée dans `.pi/memory/Decisions.md`.
