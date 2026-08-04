# Z11 — Zone `router/` (index de routage sémantique)

- **Contrat MetaProjet** — régit `KitV2/router/` (index + README de
  consommation). Le builder vit dans le méta-projet (`.agent/router/`).
- **Origine :** décisions utilisateur 2026-08-05 (BM25, JSON versionné,
  recherche obligatoire, extension Pi native) — plan
  `docs/plans/2026-08-05-resource-router.md`.

## 1. Mission

L'index de routage embarqué du kit : un **artefact généré** qui permet à un
agent Pi de trouver les ressources pertinentes sans charger le kit dans le
contexte. L'index route vers les fichiers sources ; il ne les remplace jamais.

## 2. Rôles et frontières (inviolables)

| Élément | Rôle | Propriétaire |
| --- | --- | --- |
| `router/index.json` | Artefact généré : ressources (id, kind, path, description, tags, terms) | méta-projet (builder) |
| `router/meta.json` | Version, sha256 de l'index, compteurs, stopwords | méta-projet (builder) |
| `router/README.md` | Doc de consommation : lecture seule, jamais édité à la main | méta-projet (revue) |
| `.agent/router/build_index.py` | Builder (build / --check) — hors kit | méta-projet |
| `.pi/extensions/kit-resource-router.ts` | Outil Pi natif, lecture seule | kit (runtime) |
| `.pi/skills/kit-resource-routing/SKILL.md` | Skill d'usage (quand/comment) | kit (runtime) |

## 3. Règles

1. **Artefact généré** : `index.json` et `meta.json` ne sont JAMAIS édités à la
   main. Toute modification de ressource indexable (rules/, recipes/,
   knowledge/, snippets/, .pi/prompts/, .pi/skills/) impose une régénération
   par le builder puis la gate complète.
2. **Read-only au runtime** : l'outil d'extension ne fait que lire l'index. Il
   ne modifie ni l'index, ni le kit, ni l'environnement.
3. **Index = routeur uniquement** : chaque entrée pointe vers un fichier réel ;
   le contenu de vérité reste le fichier source.
4. **Déterminisme** : builder stdlib Python, aucun réseau, sortie stable
   (tri par id) ; `--check` compare et sort non-zéro en cas de dérive.
5. **Volume borné** : descriptions courtes (source : frontmatter), terms
   pré-calculés, index ~< 200 Ko. Le runtime ne charge jamais le contenu des
   fichiers du kit, seulement l'index.
6. **Protection du contexte** : top-K ≤ 5 (max 8), seuil de score, zéro
   résultat propre plutôt que du bruit (règle « vide > bruit »).

## 4. Maintenance

- **Ajouter une ressource indexable** : la gate (couverture) échouera tant que
  l'index n'est pas régénéré → lancer `python3 .agent/router/build_index.py`
  depuis la racine du méta-projet, vérifier `git diff` sur router/.
- **Modifier le système** : builder (méta-projet, tests + README) OU runtime
  (kit, scénario end-to-end) ; jamais les deux dans la même responsabilité.
- **Tester** : fixtures du builder + scénarios end-to-end pi (évident, vague,
  vide, multiples proches) + gate complète.
- **Ne pas dégrader le routage** : toute nouvelle ressource doit avoir une
  description frontmatter réelle (1..1024 caractères, vocabulaire technique) ;
  pas de description générique (« utile pour Go »).

## 5. Patterns

- Builder déterministe + gate qui vérifie (même schéma que tools/offline).
- Stopwords dans meta.json (source unique, pas de duplication builder/runtime).
- Synonymes uniquement côté runtime (expansion de requête), jamais côté build.

## 6. Anti-patterns

- Index édité à la main ; runtime qui écrit ; index qui contient le contenu des
  fichiers (au lieu des descriptions) ; résultats non filtrés injectés dans le
  contexte ; dépendances réseau dans le builder.

## 7. Critères de validation

- [ ] `validate-kitv2.py` : index.json valide, meta.sha256 conforme, couverture
      complète des ressources indexables, chemins existants.
- [ ] `python3 .agent/router/build_index.py --check` : sortie propre.
- [ ] Scénarios end-to-end : 4 types, aucun faux positif dans les assertions.

## 8. Questions ouvertes

- Aucune : le périmètre a été arbitré avec l'utilisateur (2026-08-05).
