# Philosophie d'architecture S.U.P.E.R

> Écris du code comme on construit avec des LEGO — chaque brique a un seul
> rôle, une interface standard, une direction claire, fonctionne n'importe où
> et peut être échangée à volonté.

Ce document définit les principes d'architecture qui guident tout le code
écrit pendant les phases de développement d'un workflow Spec-Driven Develop.
Chaque agent exécutant des tâches doit internaliser ces principes.

## Frontière avec les règles du kit (obligatoire)

S.U.P.E.R est la **lentille d'évaluation de santé** du workflow (scoring par
principe dans l'analyse, checklist de revue) — pas une doctrine de conception
Go qui remplacerait les règles sourcées du kit. En cas de conflit, les règles
du kit priment : `rules/core/philosophy` (plus petit design justifié,
stdlib-first, pas de structure universelle), `rules/core/universal` (noms de
packages, contextes, erreurs, interfaces consommateur), et toute règle de
zone applicable. Les lectures compatibles :

| Principe S.U.P.E.R | Lecture kit (sourcée) |
|:---|:---|
| S — Single Purpose | Responsabilité unique (déjà doctrine kit) |
| U — Unidirectional Flow | Dépendances consommateur-possédées, direction des imports (déjà doctrine kit) |
| P — Ports over Implementation | Interfaces consommateur + contrats explicites, I/O sérialisable (déjà doctrine kit) |
| E — Environment-Agnostic | Configuration par environnement, zéro chemin/clé codé en dur (déjà doctrine kit) |
| R — Replaceable Parts | Remplaçabilité sans effet en cascade (déjà doctrine kit) |

Ce que S.U.P.E.R ajoute réellement au kit : le **scoring par principe
(🟢🟡🔴)** dans l'analyse, la **checklist de revue en 10 points**, et
l'identification des **hotspots de violation** comme priorités du plan.

---

## S — Single Purpose (Rôle unique)

De la philosophie Unix.

- Chaque module, fichier et fonction résout exactement un problème.
- Préfère la décomposition ; la puissance vient de la composition.
- Une skill fait une chose, un worker fait une chose, un script fait une
  chose.

**Test décisif** : si tu ne peux pas décrire la responsabilité d'un module en
une phrase, il faut le diviser.

**Anti-pattern** : un script qui récupère des données, calcule des métriques,
rend des graphiques et envoie des notifications.

**Approche correcte** :

```text
fetch_data.py  -> récupération uniquement, sort JSON
compute.py     -> calcul uniquement, lit JSON écrit JSON
render.py      -> rendu uniquement, lit JSON génère HTML
notify.py      -> notification uniquement, lit JSON appelle un webhook
```

---

## U — Flux unidirectionnel

- Les données circulent toujours dans une direction : entrée -> traitement ->
  sortie.
- Les dépendances pointent toujours vers l'intérieur : les couches externes
  dépendent des couches internes, jamais l'inverse.
- Pas de dépendances inverses, pas d'appels circulaires.

**Modèle en couches** :

```text
+-------------------------------+
|  Infrastructure (API, DB, UI) |  <- la plus externe, remplaçable à volonté
+-------------------------------+
|  Adapters (transform, format) |
+-------------------------------+
|  Core business (logique pure) |  <- la plus interne, zéro dépendance externe
+-------------------------------+
```

**Test décisif** : la logique centrale peut-elle passer des tests unitaires
avec zéro service externe ? Si non, la direction des dépendances est fausse.

---

## P — Ports sur l'implémentation

- Définis les contrats d'interface (structures de données, schémas) AVANT
  d'écrire l'implémentation.
- Utilise des formats intermédiaires (fichiers JSON, structures de données
  standard) pour isoler l'amont de l'aval.
- Changer une source de données, une couche de rendu ou un canal de
  notification exige zéro modification de la logique centrale.

**Pratiques** :

1. Les entrées et sorties de chaque module doivent être des structures de
   données sérialisables.
2. Les frontières de modules communiquent via des fichiers JSON ou des
   structures standard ; les objets typés en mémoire sont acceptables, mais
   les interfaces inter-modules doivent être sérialisables.
3. Définis des schémas explicites — pas « lis le code pour deviner le format ».

---

## E — Indépendant de l'environnement

- Configuration injectée via variables d'environnement ou fichiers de config,
   jamais codée en dur.
- Toutes les dépendances explicitement déclarées, pas de dépendance implicite
   aux packages système globaux.
- Processus sans état ; toute persistance déléguée au stockage externe.
- Logs vers stdout, pas vers des fichiers.

**Précédence de configuration (haute à basse)** :

```text
Variables d'environnement > fichier .env > config.json > défauts en code
```

**Checklist** :

- Toutes les clés d'API et URLs de webhooks lues depuis des variables
  d'environnement ?
- Toutes les dépendances explicitement déclarées dans un fichier de
  dépendances ?
- Aucune hypothèse de chemin de fichier codée en dur ?
- Une autre machine peut-elle exécuter ce code avec zéro modification ?

---

## R — Parties remplaçables

La conséquence naturelle et le but ultime de S + U + P + E.

- Toute couche peut être remplacée sans affecter les autres.
- Le coût de remplacement est la métrique centrale de la qualité
  d'architecture.
- Si remplacer un composant déclenche des changements en cascade dans des
  modules sans rapport, l'architecture est cassée.

**Matrice de remplacement** :

| Remplacement | Périmètre d'impact | Approche correcte |
|:---|:---|:---|
| API de source de données | Couche adaptateur seulement | Nouveau fetcher, même sortie JSON |
| Rendu frontend | Couche rendu seulement | Lit le même JSON, échange l'implémentation |
| Canal de notification | Couche notification | Échange l'adaptateur webhook |
| Plateforme de déploiement | Config de déploiement seule | Change wrangler.toml ou Dockerfile |
| Langage de programmation | Implémentation seule | Contrats JSON inchangés, réécriture dans n'importe quel langage |

---

## Carte Quick Check

```text
+------------------------------------------+
|         S.U.P.E.R Quick Check            |
|                                          |
|  S  Ce module ne fait-il qu'une chose ?  |
|  U  Le flux de données est-il unidirectionnel ? |
|  P  Les entrées/sorties sont-elles schéma-définies ? |
|  E  Peut-il fonctionner dans un autre environnement ? |
|  R  Peut-on le remplacer sans effet de bord ? |
|                                          |
|  Tout oui -> Architecture saine         |
|  1-2 non  -> Refactorisation nécessaire |
|  3+ non   -> Alerte de dette technique  |
+------------------------------------------+
```

---

## Checklist de revue de code S.U.P.E.R (10 points)

Exécute cette checklist après chaque tâche avant de la marquer comme terminée.
C'est la copie canonique de la checklist.

| Check | Principe |
|:---|:---|
| Chaque nouveau module/fichier a exactement une responsabilité | S |
| Aucune fonction ne fait plus d'une chose conceptuelle | S |
| Les données circulent entrée → traitement → sortie, pas de dépendances inverses | U |
| Aucun import circulaire introduit | U |
| Les interfaces inter-modules sont schéma-définies | P |
| L'I/O des modules est sérialisable | P |
| Aucun chemin, URL, clé ou valeur de config codé en dur | E |
| Toutes les nouvelles dépendances explicitement déclarées | E |
| Les nouveaux modules peuvent être remplacés sans changer les autres | R |
| Tous les tests passent après le changement | — |

**Règle de score** : tout passe = continuer. 1-2 échecs = corriger avant de
marquer terminé. 3+ échecs = stop et refactoriser.
