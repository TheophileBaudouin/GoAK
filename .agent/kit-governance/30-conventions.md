# N1 — Conventions (nommage, formats, frontières)

- **Contrat MetaProjet** — règles transverses applicables à tous les contrats
  Z1–Z10 et A1.

## 1. Nommage

| Objet | Règle | Exemple |
| --- | --- | --- |
| id d'artefact | `<kind>:<domaine>:<slug>` kebab-case, ASCII | `pattern:go:concrete-returns` |
| dossier de module SKILL.md | kebab-case anglais = `name` du frontmatter | `recipe-worker-pool/` |
| fichier YAML-graphe | kebab-case, domaine préfixé | `anti-patterns/go-mutable-global-state.yaml` |
| recette | `recipe-<domaine>-<sujet>` | `recipe-rest-chi` |
| probe | `<shape>-<sujet>` (ou `<sujet>`) | `worker-shutdown` |
| template shape | kebab-case, domaine | `rest-api` |

Interdit : majuscules dans les ids/chemins, espaces, caractères non ASCII,
français dans les ids (les descriptions restent en français — la langue du
contenu est libre, l'identifiant est ASCII).

## 2. Formats (règle de choix — une vérité, un format)

| Type d'artefact | Format canonique | Justification |
| --- | --- | --- |
| Règle, Recette, Bibliothèque vétée, Projet de référence, Template (via son README) | SKILL.md (frontmatter Pi + corps, progressive disclosure) | Découvrabilité Pi (description dans le system prompt), chargement à la demande |
| Pattern, Anti-pattern, Source (pointeurs officiels), guidance de domaine (security/performance/observability/architecture/debugging), stdlib | YAML-graphe (`id`/`kind`/`relationships`) | Graphe machine-résoluble, relations vérifiées par C2 |
| Snippet | SNIPPET.yaml + example.go + check.sh | Exécutable et lié à une source canonique |
| Probe | main.go + verdict `PASS` + exit code | Évaluation exécutable |
| Template sourcé | dossier projet MIT + LICENSE + ATTRIBUTION.md + README | Politique propriétaire (Z5) |
| Prompt / skill de workflow | `.pi/prompts/*.md` / `.pi/skills/*/SKILL.md` | Rôles délimités par Z8 |

Règle : **on ne mélange pas deux formats pour le même rôle sans contrat** ; tout
format nouveau passe par une décision écrite (Decisions.md) et une mise à jour
de ce tableau.

## 3. YAML-graphe — conventions d'écriture

- Métadonnées obligatoires (C0/Z10) : `id`, `title`, `kind`, `version`,
  `status`, `owner`, `tags`, `go_version`, `dependencies`, `last_verified`.
- Relations : `relationships.<relation>: [cibles]` ; les cibles sont des ids
  stables ou des URLs (seulement pour `references`).
- Corps : block scalars (`>-` / `|`) ; une idée par section ; pas de YAML
  imbriqué libre.
- `go_version` : la version minimale **testée** ; jamais une version future.
- URLs canoniques : **jamais réécrites** pour satisfaire un lint de style.
  Si une ligne `source:` dépasse ~80 caractères (linter YAML externe, non
  configuré dans le repo), utiliser l'échappement
  YAML valide `"...\<saut de ligne>  suite"` (double-quote + backslash :
  résout en une chaîne sans espace — vérifier avec `yaml.safe_load`).
- Langue : ids ASCII, contenu libre (N1 §1) ; convention du corpus — français
  pour patterns/anti-patterns, anglais pour les pointeurs Source/guidance.
- Post-écriture : tout YAML-graphe créé est re-lu (`yaml.safe_load`) et sa
  fraîcheur/relations contrôlées avant validation ; les lignes > 80 ne sont
  pas une gate projet (le corpus en contient déjà — URLs et contenu).

## 4. SKILL.md — conventions (détaillées dans A1)

- Frontmatter immuable : `name`, `description`, `category`, `tags`,
  `last-verified` — aucun champ nouveau sans migration globale.
- Progressive disclosure : description (L1) = quoi + quand + contraintes
  négatives ; corps (L2) ≤ 500 lignes ; détails en fichiers référencés (L3).
- Chemins relatifs au module ; jamais de lien en prose qui pourrit.
- Corps des catalog `libraries/` : **format « fiche » canonique** — les
  sections décisionnelles suivantes sont obligatoires pour toute bibliothèque
  admise : `## Utiliser cette librairie quand`, `## Ne pas utiliser cette
  librairie quand`, `## Avantages`, `## Inconvénients`, `## Pièges connus`,
  `## Sources vérifiées` (URL + date + type de source ; critiques négatives
  confirmées par ≥ 2 sources indépendantes, ou ≥ 1 issue/advisory officielle
  du projet). Les sections
  préexistantes (Selection, Admission checklist, Minimal use, Alternatives,
  Notes) sont conservées telles quelles. En-têtes de fiche en français
  (spécification utilisateur), contenu libre.

## 5. Frontières Kit / MetaProjet (inviolables)

| Ce qui entre dans `KitV2/` | Ce qui n'y entre JAMAIS |
| --- | --- |
| Contenu de connaissance sourcé, modules, code runnable, probes, outils de gate | Mémoire (`.pi/memory/`), décisions, évaluations du metaprojet, évidence brute (`docs/evidence/`) |
| `AGENTS.md` produit, `.pi/` natif | `.agent/` (control-plane), historique v1, références `../` vers la racine |
| Contrats condensés (README de zone, carte AGENTS.md) | Corps complets des contrats MetaProjet (ils vivent dans `.agent/kit-governance/`) |

Règle : le produit ne pointe jamais vers le metaprojet ; le metaprojet peut
pointer vers le produit. Un consommateur qui installe `KitV2/` seul doit
pouvoir l'utiliser sans la racine.

## 6. Placeholders et roadmaps

- **Aucun dossier `.gitkeep` vide** : les zones planifiées vivent dans le
  README de zone (tableau « roadmap » avec critères de remplissage).
- Un dossier de domaine n'existe que s'il a ≥ 1 artefact actif (ou un README
  contrat quand la décision est d'attendre l'évidence — cas `debugging/`).
- Supprimer un placeholder = acte de gouvernance ordinaire, pas une décision.

## 7. Critères de validation

- [ ] Ids ASCII kebab-case ; name == dossier parent (modules).
- [ ] Un seul format par rôle (tableau §2 respecté).
- [ ] Zéro placeholder vide ; chaque roadmap a des critères.
- [ ] Le produit ne référence aucune racine metaprojet (C2 le vérifie déjà pour
      les YAML ; étendre aux SKILL.md).

## 8. Questions ouvertes

- Langue des ids vs langue du contenu : confirmé (ids ASCII, contenu libre).
- Faut-il un lint des frontières (grep `\.\./` dans les SKILL.md du produit) ?
