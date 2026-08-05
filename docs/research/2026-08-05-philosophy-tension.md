# Tension de philosophie : minimalisme Go vs prévisibilité personnelle

Date : 2026-08-05. Auteur : passe de durcissement gouvernance méta-projet
(finding Rodin C). Statut : note de décision — la décision appartient à Marie
(choix de produit), pas à l'agent.

## 1. La contradiction, sans édulcoration

Deux objectifs s'affrontent, et ils sont **incompatibles tels qu'énoncés** :

**Objectif A — « le Kit reste idiomatique et sans structure imposée »**
(doctrine sourcée, déjà normative) :

- `AGENTS.md` (racine, section Evidence rules) : « Go does not prescribe a
  universal project tree; use official package naming guidance and Go
  Proverbs. »
- `KitV2/rules/core/philosophy/SKILL.md` (section Boundary) : « it prescribes
  no universal project layout (the official module-layout examples are shapes
  to choose from, not a standard). »
- Sources citées : Effective Go, Go Proverbs, go.dev/doc/modules/layout
  (« Organizing a Go module » — des formes, pas un standard).
- Registre des sources : `golang-standards/project-layout` n'est pas une
  autorité Go.

Ces deux textes sont **cohérents entre eux** (vérifié : ils disent la même
chose). C'est l'objectif B qui les contredit.

**Objectif B — « je veux naviguer pareil dans n'importe quel projet produit
par le Kit »** (besoin personnel déclaré de Marie) : une structure identique
pour retrouver sans effort les mêmes choses au même endroit, quel que soit le
projet.

Si le Kit prescrit « choisis la plus petite structure justifiée à chaque
fois », deux projets produits par le Kit peuvent légitimement avoir des
arbres différents (l'un `main.go` racine, l'autre `cmd/` + `internal/` selon
le besoin). La navigation personnelle n'est alors pas garantie identique.
Inversement, si le Kit impose une disposition unique, il contredit la
doctrine sourcée et cesse d'être « minimal justifié ».

Ce n'est pas un détail éditorial : c'est un choix de produit qui touche
`KitV2/rules/core/` — zone dont la modification exige une approbation
explicite (AGENTS.md Modification policy). L'agent ne tranche pas seul.

## 2. Options avec compromis

### Option 1 — Garder le minimalisme, résoudre ailleurs (recommandée par défaut)

Le Kit reste idiomatique et sans structure imposée (il doit aussi fonctionner
pour d'autres usages que ceux de Marie). Le besoin personnel de navigation
prévisible est satisfait par un **preset séparé**, clairement étiqueté
« non-canonique », que Marie active volontairement sur ses projets (ex. une
recette/checklist « structure fixe personnelle » ou un prompt qui applique sa
disposition préférée).

- Avantages : ne contredit aucune source ; le cœur garde sa position
  « sourcé, pas d'opinion inventée » ; le preset reste réversible et
  personnel.
- Coûts : le preset doit être maintenu à part ; un consommateur tiers du Kit
  n'hérite pas de la prévisibilité de Marie (ce n'est pas son besoin).
- Risque : si le preset dérive vers de la doctrine non sourcée, il faut le
  garder étiqueté non-canonique — contrôlable à la revue.

### Option 2 — Changer la philosophie du cœur

`rules/core/philosophy` prescrit une disposition unique, avec exceptions
documentées au cas par cas.

- Avantages : prévisibilité maximale — l'arbre est identique partout.
- Coûts : contredit frontalement Effective Go / Go Proverbs /
  go.dev/doc/modules/layout cités en source ; affaiblit la position
  « sourcé, pas d'opinion inventée » du Kit ; les règles du Kit devraient
  alors documenter cette déviation assumée et ses justifications, ce qui est
  un changement de doctrine majeur (version majeure, migration, décision
  écrite).
- Risque : un Kit qui impose une structure unique devient un framework de
  formes — contraire à la vision « typed knowledge graph, pas framework »
  (Brief.md).

### Option 3 — Prévisibilité par documentation, pas par uniformité

Garder la liberté de structure, mais rendre obligatoire qu'une recette
produise systématiquement un artefact « pourquoi cette disposition ici » au
même endroit (ex. section `Structure` dans chaque projet généré, ou
`layout.md` racine produit par les recettes).

- Avantages : l'arbre reste libre et sourcé ; la navigation devient
  prévisible parce que la **raison** est toujours au même endroit ; coût
  faible en doctrine (une règle de forme des recettes, pas une règle de
  structure Go).
- Coûts : l'arbre réel peut quand même différer entre projets — la
  prévisibilité est cognitive (on sait où chercher la raison), pas physique
  (mêmes chemins) ; exige d'ajouter une obligation aux recettes de
  production.
- Risque : faible ; reste compatible avec les deux objectifs si Marie
  accepte la prévisibilité par la raison plutôt que par l'uniformité.

## 3. Ce que la décision implique

- **Option 1 ou 3** : périmètre méta-projet possible (recette/prompt preset
  pour 1 ; règle de forme des recettes pour 3 — mais attention : 3 touche
  aussi les recettes de `KitV2/recipes/`, donc la passe suivante pour les
  recettes existantes). Si Marie choisit 1 ou 3, l'agent applique ce qui est
  méta-projet et écrit les éditions KitV2 comme actions en attente.
- **Option 2** : touche `KitV2/rules/core/philosophy/SKILL.md` (zone
  interdite cette passe) — l'édition exacte est écrite dans le plan
  (docs/plans/2026-08-05-metaproject-governance-hardening.md, annexe à
  compléter après réponse) comme action en attente, jamais appliquée ici.

## 4. Question posée à Marie

Voir la question envoyée via l'outil de questions (gabarit : « Le Kit dit
actuellement à l'agent : il n'y a pas une seule bonne structure de projet Go,
choisis la plus petite qui convient à chaque fois. Toi, tu veux plutôt : je
veux toujours pouvoir naviguer pareil, peu importe le projet. Ces deux règles
se contredisent. Trois façons de trancher… »).

## 5. Décision de Marie (2026-08-05)

**Option 3 — naviguer par la raison.** On garde la liberté de structure, mais
chaque projet produit par le Kit explique par écrit, toujours au même endroit,
pourquoi il a choisi sa structure ; la navigation devient prévisible parce que
la raison est toujours au même endroit.

Application :

- Méta-projet (appliqué dans cette passe) : Z3 §3 — nouvelle section
  obligatoire « Structure (pourquoi cette disposition) » pour toute recette
  qui produit/recommande une disposition de projet (N/A sinon) ; Z5 §3 — le
  README template exige la structure et sa justification.
- KitV2 (action en attente, passe suivante) : ajouter la section aux recettes
  concernées ; ajouter la justification de structure aux README des 3
  templates sourcés.
- Aucune modification d'AGENTS.md racine ni de `rules/core/philosophy` :
  l'Option 3 est compatible avec la doctrine sourcée (« no universal project
  layout ») — elle ajoute une obligation de forme des recettes, pas une règle
  de structure Go.

Confiance : les citations des deux textes sont vérifiées directement
(AGENTS.md racine §Evidence rules ; philosophy SKILL.md §Boundary). Le
caractère contradictoire est un jugement établi par lecture directe des deux
passages ; la résolution est un choix de valeur qui appartient à Marie.
