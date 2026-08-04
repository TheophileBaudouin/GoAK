# A1 — Auteur de modules (contrat d'écriture des SKILL.md)

- **Contrat MetaProjet** — régit l'écriture de tout module SKILL.md du Kit
  (rules, recipes, catalogs, .pi/skills). Le document de travail produit
  `KitV2/templates/_kit-skill-authoring.md` reste une aide autonome du
  contributeur **dans le produit** ; le présent contrat est l'**autorité** du
  metaprojet. Il n'est pas copié dans le produit (autonomie, N1) : la version
  produit peut diverger tant qu'elle ne contredit pas les règles ici.
- **Rapport d'audit :** §4.3. **Sources :** spec agentskills.io, best-practices
  Claude, Red Hat ACE, Google Agent Skills.

## 1. Invariants communs (tous les modules)

1. **Frontmatter immuable** : `name`, `description`, `category`, `tags`,
   `last-verified`. Aucun champ nouveau sans migration globale ; `name` =
   dossier parent.
2. **Recherche fraîche** : toute écriture ou mise à jour d'un catalogue est
   précédée d'une recherche web actuelle sur des sources primaires. Chaque
   source utilisée est datée dans `Sources vérifiées` ; la date `last-verified`
   est celle de la relecture complète.
3. **Une information, un emplacement** : une fiche ne répète pas une limite,
   une alerte ou une décision dans une autre langue ou section. Une section
   optionnelle sans contenu nouveau est supprimée.
4. **Exemple vérifiable** : tout bloc Go présenté comme minimal/runnable traite
   les retours et ressources selon les rules applicables. Un extrait abrégé
   porte la mention `illustrative` et n'est pas présenté comme compilable.
5. **Progressive disclosure** : L1 description (seule chose en contexte
   permanent) ; L2 corps ≤ 500 lignes ; L3 détails en fichiers référencés
   (un niveau de profondeur) — jamais dans le corps.
6. **Description = quoi + quand + contraintes négatives** : c'est le goulot de
   découvrabilité (Red Hat : « écrivez vos L1 comme des abstracts optimisés
   pour la recherche »). « Extracts text from PDFs. Use when working with PDF
   documents. Not for images. » — jamais « Helps with PDFs ».
7. **Chemins relatifs** au module ; références croisées taggées (ids stables),
   jamais de lien en prose qui pourrit.
8. **Sources primaires** pour tout fait ; une synthèse est un point de départ,
   jamais la seule base.
9. **Pas de sections artificielles** : une section n'existe que si elle a du
   contenu ; aucun gabarit universel de corps.

## 2. Matrice par catégorie

| Catégorie | Activation | Sections obligatoires | Validation minimale | Anti-patterns spécifiques |
| --- | --- | --- | --- | --- |
| **recipe** | « Use when a consumer project matches this shape » | Problem · Solution (code minimal) · Why not alternatives · Runnable example + test · Observable scenario (actions + sorties attendues) · Limits · Sources | Compile ; tests ; scénario exécuté avec verdict `PASS`/`PARTIAL`/`BLOCKED` — jamais `PASS` sans exécution | Code non runnable ; scénario affirmé au lieu d'exécuté ; framework quand stdlib suffit |
| **rule** | « Load when writing code in this area » | Impératif · Quand appliquer · Frontière (ne couvre PAS) · Contre-exemples · Vérification · Sources | Mécanique verte ; frontière explicite ; sources | Instruction vague ; opinion sans source ; règle sans frontière ; contradiction avec une autre règle |
| **library** | « Use when choosing a library for this responsibility » | Sélection (version + raison d'admission, pas les étoiles) · Admission 9 critères · Alternatives avec verdicts · Minimal use · **Format fiche (N1 §4 : Utiliser/Ne pas utiliser quand, Avantages, Inconvénients, Pièges, Sources vérifiées)** · Sources | Admission répondue avec évidence ; minimal use compile ; alternatives rejetées enregistrées ; fiche complète (6 sections N1 §4) | Étoiles comme raison ; alternative rejetée manquante ; recommandation sans lire les issues ; fiche incomplète |
| **reference-project** | « Use when designing a shape this project demonstrates » | Extract-only : ce que l'on PEUT extraire · ce que l'on ne doit JAMAIS copier · Vérification · Sources | Chaque pattern extrait trace vers le repo ; aucun code/arbre copié ; admission appliquée | Clonage de l'arbre ; architecture imposée du projet ; admission par popularité |
| **core** (rules/core) | « Chargée chaque session » | Principe · Frontière · Exemples courts · Sources | Budget compacité (≤ 6 modules, ≤ 300 lignes) ; pas de référence registry | Contenu de domaine ; croissance « just this once » ; duplication |
| **workflow** (`.pi/skills/`) | « Chargée quand le processus s'applique » | Procédure · Frontière avec modules · Références | Frontmatter complet ; pas de connaissance de domaine | Skill de workflow contenant du domaine ; duplication avec un prompt |

## 3. Budget de lignes et de tokens (Red Hat/Claude)

- L1 : 1–2 phrases, spécifiques, avec contraintes négatives.
- L2 : ≤ 500 lignes ; au-delà → déplacer vers L3 (fichiers référencés).
- L3 : **gated** — ne charger que ce qui est nécessaire à l'invocation ; un
  fichier L3 massif non gated est le plus gros puits de tokens.

## 4. Cycle d'écriture (Google : skills as products)

1. Recherche et sources primaires vérifiées (liens 200, contenu lu).
2. Rédaction selon la matrice ; auto-vérification : la description L1
   déclenche-t-elle le bon chargement ? le corps répond-il à la question ?
3. Éval minimale de la catégorie exécutée (recette : scénario ; library :
   admission + compile).
4. Revue fresh-context (subagent) avant admission.
5. Enregistrement : métadonnées complètes, fraîcheur, relations.

## 5. Anti-patterns généraux (rejeter à vue)

- Description vague (« Helps with … ») ; corps = documentation exhaustive ;
- sections vides ; placeholder ; duplication d'un module existant ;
- un fait sans source ; une URL morte ; `last_verified` bumpé sans re-vérifier.

## 6. Critères de validation

- [ ] C2 : frontmatter complet, name == dossier, ≤ 500 lignes, description avec
      activation + contraintes négatives.
- [ ] Sections obligatoires de la catégorie présentes (C2 par catégorie).
- [ ] Sources présentes ; liens vérifiés à l'admission.
- [ ] Éval minimale exécutée et tracée.

## 7. Questions ouvertes

- Aucune : la relation avec `_kit-skill-authoring.md` est tranchée ci-dessus
  (autorité metaprojet vs aide produit autonome).
- Catégorie `workflow` (`.pi/skills/`) : extension de schéma enregistrée dans
  `.pi/memory/Decisions.md` — les catégories de la matrice ci-dessus restent
  le jeu des modules (A1).
