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
4. **Fonctionnel obligatoire** : compile et passe ses tests dans le Kit. Un
   template non fonctionnel est interdit, quelle que soit la source.
5. **Réutilisable directement** : très peu de modifications pour l'adopter ;
   les modifications nécessaires sont simples et documentées.
6. **Adaptations minimales documentées** : chaque écart par rapport à la source
   est listé dans `ATTRIBUTION.md` avec sa raison.
7. **Moins de templates, très qualitatifs** : il n'y a pas d'objectif de
   quantité ; une shape sans template sourcé MIT reste une roadmap.

## 3. Structure d'un template

```text
templates/<shape>/
├── <projet source>…     # code du projet épingle, fonctionnel
├── LICENSE              # MIT (copie de la licence du projet)
├── ATTRIBUTION.md       # source, version épinglée (commit/release), licence,
│                        # adaptations (diff + raisons)
├── README.md            # statut, source, scénario observable, modifications
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
  copie + LICENSE + ATTRIBUTION.md → adaptations minimales → compile + tests +
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
- Licence non-MIT ; projet non maintenu ; template non fonctionnel.
- Clone sans attribution ni version épinglée ; adaptations non documentées.
- Template « starter » qui impose une architecture (leçon ardanlabs :
  extract-only, jamais copié tel quel).
- Placeholder de shape sans roadmap.

## 8. Critères de validation (C2)

- [ ] Tout template non-legacy : `LICENSE` (MIT) + `ATTRIBUTION.md` (source,
      version, adaptations) + `README.md` + `template.yaml` présents.
- [ ] Compile + tests + scénario observable tracé.
- [ ] `TEMPLATES.md` cohérent avec l'arborescence (statuts à jour).
- [ ] Aucun nouveau scaffold (statut legacy figé au 2026-08-04).

## 9. Questions ouvertes

- Sources candidates pour les 7 shapes legacy (recherche à lancer : projets
  MIT Go REST/gRPC/CLI/worker/service/monolith/cloud réels, éprouvés).
- Faut-il un gabarit `ATTRIBUTION.md` type dans le Kit (au niveau
  `templates/`) ? (proposition : oui, en phase 3 lors du premier remplacement.)
