# Templates des documents d'analyse

Templates des trois documents générés en phase 1 (Analyse profonde du
projet). Sortie vers `docs/analysis/`. Ces documents servent deux buts : ils
alimentent la phase 2 (Raffinement et confirmation de l'intention) pour une
discussion utilisateur ancrée, et la phase 3 (Décomposition de la tâche) pour
la planification.

---

## project-overview.md

```markdown
# Project Overview

## Direction préliminaire
<!-- Résumé en une phrase de la direction de transformation prévue depuis la
phase 0. Elle sera raffinée en définition de tâche confirmée en phase 2 après
revue par l'utilisateur. -->

## Architecture actuelle
<!-- Diagramme d'architecture de haut niveau (Mermaid) et description -->

## Stack technologique
| Couche        | Actuel          | Cible           |
|:--------------|:----------------|:----------------|
| Langage       |                 |                 |
| Framework     |                 |                 |
| Outil de build|                 |                 |
| Gestionnaire  |                 |                 |
| Base de données |               |                 |
| Déploiement   |                 |                 |

## Points d'entrée
<!-- Liste des points d'entrée principaux : commandes CLI, endpoints API,
routes UI, etc. -->

## Build & Run
<!-- Comment builder, tester et exécuter le projet actuellement -->

## Ligne de base de test
<!-- Frameworks de test existants, commandes de test, lacunes de couverture,
et si le nouveau travail de fonctionnalité a actuellement un endroit fiable
pour ajouter des tests -->

## Ligne de base de gouvernance du projet
<!-- Surfaces existantes d'instructions et de mémoire au niveau projet :
AGENTS.md, mémoire native .pi/memory/ (fichiers réellement présents),
fallback mémoire repo-local, règles Cursor/Windsurf/Cline/Codex ou
équivalents. Note les emplacements canoniques, les lacunes et les conflits. -->

## Intégrations externes
<!-- APIs, bases de données, services, systèmes de fichiers avec lesquels le
projet interagit -->
```

---

## module-inventory.md

```markdown
# Module Inventory

| Module | Responsabilité | Dépendances | Fichiers | Lignes | Complexité | Score S.U.P.E.R |
|:-------|:---------------|:------------|--------:|-------:|:-----------|:----------------|
|        |                |             |         |       |            |                 |

> **Score S.U.P.E.R** : évalue chaque module comme 🟢 (conforme), 🟡 (partiel)
> ou 🔴 (violation) sur les cinq principes. Format : `S🟢 U🟡 P🔴 E🟢 R🟡`

## Détails des modules

### <Nom du module>
- **Chemin** : `src/module_name/`
- **Responsabilité** : ce que fait ce module
- **API publique** : fonctions/classes clés exposées aux autres modules
- **Dépendances internes** : quels modules du projet il importe
- **Dépendances externes** : bibliothèques tierces utilisées
- **Complexité** : Faible / Moyenne / Élevée / Critique
- **Notes de transformation** : défis ou considérations spécifiques pour ce
  module
- **Évaluation S.U.P.E.R** :
  - **S (Rôle unique)** : ce module a-t-il exactement une responsabilité ? Si
    non, que faut-il diviser ?
  - **U (Flux unidirectionnel)** : les dépendances sont-elles
    unidirectionnelles ? Y a-t-il des dépendances circulaires ?
  - **P (Ports sur l'implémentation)** : les entrées/sorties sont-elles
    schéma-définies et sérialisables ? Les frontières de modules sont-elles
    basées sur des contrats ?
  - **E (Indépendant de l'environnement)** : y a-t-il des chemins codés en
    dur, de la config embarquée ou des hypothèses spécifiques à la
    plateforme ?
  - **R (Parties remplaçables)** : ce module peut-il être échangé sans
    changements en cascade ? Quel est le coût de remplacement ?
```

---

## risk-assessment.md

```markdown
# Risk Assessment

## Résumé de santé d'architecture S.U.P.E.R

> Évalue le codebase actuel contre les principes S.U.P.E.R pour identifier
> les risques d'architecture et guider la transformation.

| Principe | Statut | Résultats clés | Priorité de transformation |
|:---------|:-------|:---------------|:---------------------------|
| **S** Rôle unique | 🟢/🟡/🔴 | | Élevée / Moyenne / Faible |
| **U** Flux unidirectionnel | 🟢/🟡/🔴 | | Élevée / Moyenne / Faible |
| **P** Ports sur l'implémentation | 🟢/🟡/🔴 | | Élevée / Moyenne / Faible |
| **E** Indépendant de l'environnement | 🟢/🟡/🔴 | | Élevée / Moyenne / Faible |
| **R** Parties remplaçables | 🟢/🟡/🔴 | | Élevée / Moyenne / Faible |

**Santé globale** : _X/5 principes sains_ — [Saine / Refactorisation
nécessaire / Alerte de dette technique]

### Hotspots de violation S.U.P.E.R
<!-- Liste les modules/fichiers principaux qui violent le plus de principes
S.U.P.E.R, classés par sévérité. Ils deviennent des cibles prioritaires du
plan de transformation. -->

## Matrice des risques

| Risque | Impact | Probabilité | Sévérité | Atténuation |
|:-------|:-------|:------------|:---------|:------------|
|        |        |             |          |             |

## Risques de sévérité élevée
<!-- Discussion détaillée de chaque risque de sévérité élevée -->

## Dette technique
<!-- Problèmes préexistants qui peuvent compliquer la transformation. Inclut
les violations S.U.P.E.R comme catégorie de dette technique. -->

## Risques de test
<!-- Harnais de test manquants, couverture de régression faible, tests
lents/flaky, ou zones où le travail de fonctionnalité ne peut pas encore être
validé en sécurité. -->

## Risques de gouvernance du projet
<!-- Surfaces d'instructions/mémoire manquantes ou conflictuelles,
instructions obsolètes, fichiers fallback non natifs utilisés sans
confirmation, ou décisions durables qui n'existent actuellement que dans le
contexte de conversation. -->

## Préoccupations de compatibilité
<!-- Compatibilité d'API, changements de format de données, changements de
déploiement -->
```
