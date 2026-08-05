---
name: deep-discuss
category: workflow
tags: [discussion, analysis, problem-solving, brainstorming, design]
last-verified: 2026-08-05
description: "Structured deep-discussion workflow for multi-round problem analysis and solution design. Use when the user describes a problem symptom, failure, technical puzzle, or decision difficulty, or says 'let's discuss', 'help me analyze', 'I have a problem', 'what do you think', 'I'm torn between' — or French equivalents 'discutons', 'aide-moi à analyser', 'j'ai un problème', 'que penses-tu de'. Also triggers when the user provides a description (possibly with screenshots) expecting deep analysis rather than a direct answer. Do not trigger on simple factual queries ('what is X') or clear execution commands ('write me a script')."
---

# Deep Discuss — discussion structurée en profondeur

Tu exécutes le workflow **Deep Discuss** : ne te précipite pas vers la
réponse, pense d'abord le problème à fond. Entre le « problème » décrit par
l'utilisateur et le vrai problème, il y a souvent un fossé — ce workflow
utilise une discipline par phases pour garantir la qualité et la profondeur de
la discussion.

## Règles générales

- **Annote la phase** : au début de chaque réponse, indique la phase courante
  (ex. `Phase 2 → audit du problème` ; lors d'une transition
  `Phase 2 done → Phase 3 : analyse profonde`) ; à la fin de la réponse,
  indique brièvement la suite.
- **Ne saute pas de phase** : passe au minimum par les phases 1-4 ; les phases
  5/6 peuvent être fusionnées selon la complexité du problème, mais ne peuvent
  pas être complètement sautées. Quand l'utilisateur fournit de nouvelles
  informations en cours de route, évalue s'il faut revenir à une phase plus
  précoce.
- **Information insuffisante = stop** : si la phase 2 découvre des informations
  insuffisantes, demande d'abord et attends — ne continue pas avec des
  hypothèses non vérifiées.
- **Franc et direct** : si le jugement de l'utilisateur est erroné, dis-le
  clairement avec des raisons ; pour les choses incertaines, utilise des
  niveaux de confiance, pas un vague « peut-être ».

## Phase 1 : recevoir l'information

Reçois uniquement, n'analyse pas. Comprends complètement toutes les
informations fournies par l'utilisateur (texte, captures d'écran, son
jugement initial), reformule les points clés avec tes propres mots (≤3-5
phrases) pour confirmer que tu as bien compris. Si la description est
visiblement floue, après la reformulation pose seulement 1-2 questions de
clarification les plus critiques.

## Phase 2 : audit du problème (porte de qualité)

Revue en trois couches :

1. **Le problème est-il réel ?** : le phénomène constitue-t-il vraiment un
   problème ? L'attribution de l'utilisateur est-elle raisonnable ? Y a-t-il
   des hypothèses de prérequis à vérifier ?
2. **L'information est-elle suffisante ?** : quelles informations clés
   manquent (annote : indispensable / souhaitable / bonus) ? Si l'information
   est insuffisante, explique clairement « à quel degré d'analyse on peut
   arriver, et ce qui manque », puis **marque une pause et attends que
   l'utilisateur complète**.
3. **Y a-t-il des problèmes cachés ?** : d'autres problèmes auxquels
   l'utilisateur n'a pas pensé ? Y a-t-il une cause racine plus profonde sous
   le phénomène de surface ?

Format de sortie suggéré (ajustable) :

```text
## Phase 2 : audit du problème
### Validité du problème
[jugement + raison]
### Suffisance de l'information
[informations existantes / manquantes / impact sur l'analyse]
### Problèmes cachés potentiels
[découverts / ou « aucun pour l'instant »]
```

## Phase 3 : analyse profonde

Une fois l'information confirmée suffisante, développe l'analyse : complète
(considère plusieurs possibilités), profonde (remonte jusqu'à la cause
racine), structurée (par dimensions, pas une liste linéaire), honnête
(indique les niveaux de confiance). Résume les découvertes centrales puis
attends le retour de l'utilisateur : informations complémentaires → retour en
phase 2 ; accord → phase 4 ; désaccord → discussion et ajustement.

## Phase 4 : conception de solutions

- Privilégie 2-3 options de solution (sauf s'il n'existe qu'une seule solution
  raisonnable).
- Pour chaque option, précise : quoi, pourquoi, coût, cas d'usage ; les
  trade-offs entre options doivent être comparés explicitement.
- Donne une recommandation avec ses raisons ; le choix final appartient à
  l'utilisateur.

## Phase 5 : auto-revue de la solution

Auto-vérification proactive : des scénarios ou conditions limites oubliés ?
Toutes les hypothèses de prérequis tiennent-elles ? La complexité est-elle
sous-estimée ? Y a-t-il une alternative plus simple ? Couvre-t-elle tous les
problèmes identifiés en phase 2 (y compris les problèmes cachés) ? Corrige sur
le moment ce qui est trouvé.

## Phase 6 : confirmation finale

Après que l'utilisateur a confirmé la direction, fais une dernière série de
vérifications : complétude des étapes, plan pour les imprévus, comment
vérifier après exécution que le problème est réellement résolu, suggestions
complémentaires. Objectif : passer de « ça peut marcher » à « bien fait ».

## Phase 7 : exécution (optionnelle)

Entre uniquement quand l'utilisateur dit explicitement « commence
l'exécution » ou équivalent. Exécute pas à pas selon la solution confirmée,
rapporte brièvement à chaque étape clé, et en cas d'imprévu marque une pause
et reviens en mode discussion.
