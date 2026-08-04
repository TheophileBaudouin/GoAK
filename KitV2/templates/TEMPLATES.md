# Project template catalog

## Politique (directive propriétaire, 2026-08-04)

Les templates du Kit ne sont **jamais écrits par un agent**. Chaque template
est une copie légèrement adaptée d'un **projet open source réel** :

- licence **MIT** (totalement ouverte) — obligatoire ;
- projet fiable : maintenu, testé, CI, communauté active ;
- **ultra-spécifique et minimal** : presque exclusivement la technologie du
  template — une seule stack, aucune technologie annexe hors périmètre ;
  codebase petit, parcourable de bout en bout, structure claire et modulaire
  (intégration par copie de modules bien délimités, modification simple) ;
- **une responsabilité unique**, directement réutilisable avec très peu de
  modifications ;
- conforme aux règles du Kit (idiomatique, stdlib-first, pas de framework
  imposé) ;
- **fonctionnel** : compile et passe ses tests — un template non fonctionnel
  est interdit ;
- adaptations minimales au Kit **documentées** (diff + raisons) ;
- attribution : source, version épinglée, licence, adaptations (dont le
  périmètre technique : une seule technologie, aucune technologie annexe).

L'agent documente et adapte ; il ne développe pas le template. Il vaut mieux
**moins de templates, très qualitatifs**, améliorés par la communauté, que des
squelettes maison.

## Statut actuel

Les squelettes ci-dessous sont des **scaffolds agent-générés hérités de la
v1** (runnable minimal bases). Ils ne satisfont pas la politique MIT/sourcing :
ils sont marqués `legacy` et **candidats au remplacement** par des templates
sourcés. Aucun nouveau scaffold n'est accepté.

| Template | Statut | Promotion / remplacement |
|---|---|---|
| rest-api | legacy (scaffold) | remplacer par un projet open source MIT REST |
| grpc | legacy (scaffold) | remplacer par un projet open source MIT gRPC |
| cli | legacy (scaffold) | remplacer par un projet open source MIT CLI |
| worker | legacy (scaffold) | remplacer par un projet open source MIT worker |
| microservice | legacy (scaffold) | remplacer par un projet open source MIT service |
| monolith | legacy (scaffold) | remplacer par un projet open source MIT monolith |
| cloud-service | legacy (scaffold) | remplacer par un projet open source MIT déployable |

## Admission d'un nouveau template (sourcé)

1. Identifier un projet open source MIT, fiable, **ultra-spécifique** (une
   seule technologie, pas de stack annexe), **minimal** (codebase petit et
   parcourable, structure claire et modulaire), à responsabilité unique,
   conforme aux règles du Kit.
2. Épinguer la version (commit/release) et vérifier la licence MIT.
3. Copier le projet dans `templates/<shape>/` avec `LICENSE`, `ATTRIBUTION.md`
   (source, version, adaptations) et `README.md` (statut, source, scénario
   observable).
4. Adapter **minimalement** au Kit ; chaque adaptation est documentée dans
   `ATTRIBUTION.md` avec sa raison.
5. Vérifier : compile, tests, scénario observable exécuté et enregistré
   (`PASS`/`PARTIAL`/`BLOCKED`).
6. Mettre à jour ce catalogue et le validateur (forme attendue du template).

Les recettes existantes restent la preuve d'implémentation canonique jusqu'au
remplacement effectif d'un scaffold legacy.
