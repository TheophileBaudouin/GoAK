# Z5 — Zone `templates/` (templates sourcés MIT)

- **Contrat MetaProjet** — régit `KitV2/templates/`.
- **Rapport d'audit :** §2.6. **Directive propriétaire (2026-08-04, majeure) :**
  les templates ne sont **jamais écrits par un agent** ; ce sont des copies de
  projets open source réels, fiables, fonctionnels, sous licence MIT,
  réutilisables directement avec des adaptations minimales documentées.

## 1. Mission

Fournir des **bases de projet reproductibles et sourcées** : un agent ou un
développeur démarre une application à partir d'un projet réel éprouvé, pas
d'un squelette maison. La qualité vient de la communauté, pas de l'agent.

## 2. Politique (obligations absolues)

1. **Jamais de template écrit par l'agent** from scratch. L'agent documente,
   épingle, adapte minimalement et vérifie ; il ne développe pas.
2. **Licence MIT obligatoire** (totalement ouverte). Un projet sous licence
   restrictive (GPL/AGPL, licence propriétaire, « no commercial use ») est
   rejeté, quelle que soit sa qualité.
3. **Source réelle, fiable** : projet maintenu (commits/releases récents), testé,
   CI, communauté active, **une responsabilité unique**, conforme aux règles du
   Kit (idiomatique, stdlib-first, pas de framework imposé).
4. **Ultra-spécifique et minimal** (critère de sélection élevé) : le projet
   implémente **presque exclusivement** la technologie du template — une seule
   stack, un seul domaine, aucune technologie annexe hors périmètre (auth,
   observabilité, K8s, ORM, CI lourde…). Le codebase est **petit et parcourable
   de bout en bout** : pas de méga-dépôt, pas d'arbre vendored/généré, pas de
   dépendances lourdes. La structure est **claire, bien organisée et
   modulaire** : chaque composant est isolé et remplaçable, de sorte que
   l'intégration dans un projet quelconque se fait par copie de modules bien
   délimités, et la modification reste simple.
   **Application réelle obligatoire (2026-08-05, D-2026-08-05-14)** : la source
   doit être une application réelle à responsabilité unique, **pas un
   starter/template tiers ni un recueil d'exemples de démonstration** — un
   dépôt nommé template/starter/example, ou une collection de démos, ne
   satisfait pas la politique même sous MIT (leçon recherche 2026-08-05
   desktop-app : aucun candidat Wails conforme).
5. **Fonctionnel obligatoire** : compile et passe ses tests dans le Kit. Un
   template non fonctionnel est interdit, quelle que soit la source.
6. **Réutilisable directement** : très peu de modifications pour l'adopter ;
   les modifications nécessaires sont simples et documentées.
7. **Adaptations minimales documentées** : chaque écart par rapport à la source
   est listé dans `ATTRIBUTION.md` avec sa raison.
8. **Moins de templates, très qualitatifs** : il n'y a pas d'objectif de
   quantité ; une shape sans template sourcé MIT reste une roadmap.

## 3. Structure d'un template

```text
templates/<shape>/
├── <projet source>…     # code du projet épingle, fonctionnel
├── LICENSE              # MIT (copie de la licence du projet)
├── ATTRIBUTION.md       # source, version épinglée (commit/release), licence,
│                        # adaptations (diff + raisons)
├── README.md            # statut, source, scénario observable, modifications,
│                        # structure du projet et justification (D-2026-08-05-13)
└── template.yaml        # name, status, purpose, source, validation
```

## 4. Statuts

| Statut | Signification | Condition d'entrée |
| --- | --- | --- |
| `planned` | shape en roadmap, aucun template | décision + ligne roadmap |
| `sourced` | template sourcé MIT, fonctionnel, vérifié | politique §2 complète |
| `legacy` | scaffold agent-généré hérité, candidat au remplacement | existant au 2026-08-04 ; aucun nouveau scaffold accepté |
| `deprecated` | retiré ou remplacé | décision écrite + migration |

Les scaffolds `legacy` actuels (rest-api, grpc, cli, worker, microservice,
monolith, cloud-service) restent en place jusqu'à leur remplacement par un
template sourcé — ils ne sont **jamais** présentés comme des templates
conformes à la politique.

## 5. Maintenance

- **Admission** : projet identifié (source + version) → licence MIT vérifiée →
  **périmètre technique vérifié** (une seule technologie, pas de technologie
  annexe, taille parcourable — preuve écrite dans `ATTRIBUTION.md`) → copie +
  LICENSE + ATTRIBUTION.md → adaptations minimales → compile + tests +
  scénario observable exécuté (`PASS`/`PARTIAL`/`BLOCKED`) → statut `sourced` →
  mise à jour de `TEMPLATES.md` et du validateur.
- **Mise à jour (suivi communautaire)** : bump de version épinglée, diff des
  adaptations re-vérifié, tests + scénario re-exécutés, `last_verified` bump —
  la mise à jour est un événement, pas une corvée annuelle.
- **Retrait** : décision écrite (project abandonné, licence changée, qualité
  dégradée) + migration des consommateurs.

## 6. Patterns

- ATTRIBUTION.md comme mémoire du diff : « pourquoi ce template diffère de sa
  source » — c'est ce qui rend les adaptations simples à reproduire.
- Le suivi des releases de la source est la maintenance naturelle : la
  communauté améliore, le Kit suit.

## 7. Anti-patterns

- Template écrit par l'agent (le cas des scaffolds legacy — acceptés
  transitoirement, plus jamais admis).
- **Template fourre-tout** : une stack large (router + ORM + auth + K8s + CI…)
  au lieu d'une seule technologie — rejeté quel que soit le projet source.
- Licence non-MIT ; projet non maintenu ; template non fonctionnel.
- Clone sans attribution ni version épinglée ; adaptations non documentées.
- Template « starter » qui impose une architecture (leçon ardanlabs :
  extract-only, jamais copié tel quel).
- Placeholder de shape sans roadmap.

## 8. Critères de validation (C2)

- [ ] Tout template non-legacy : `LICENSE` (MIT) + `ATTRIBUTION.md` (source,
      version, adaptations, **périmètre technique**) + `README.md` +
      `template.yaml` présents.
- [ ] `ATTRIBUTION.md` atteste une seule technologie et l'absence de technologie
      annexe (contrôle de revue ; C2 vérifie la présence de la section).
- [ ] Borne de taille respectée (nb de fichiers source et de lignes bornés, pas
      d'arbre vendored/généré lourd) — C2.
- [ ] Compile + tests + scénario observable tracé.
- [ ] `TEMPLATES.md` cohérent avec l'arborescence (statuts à jour).
- [ ] Aucun nouveau scaffold (statut legacy figé au 2026-08-04).

## 9. Questions ouvertes

- Sources candidates pour les 7 shapes legacy (recherche à lancer : projets
  MIT Go REST/gRPC/CLI/worker/service/monolith/cloud réels, éprouvés).
- Faut-il un gabarit `ATTRIBUTION.md` type dans le Kit (au niveau
  `templates/`) ? (proposition : oui, en phase 3 lors du premier remplacement.)
