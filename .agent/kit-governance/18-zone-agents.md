# Z9 — Zone `AGENTS.md` produit (point d'entrée)

- **Contrat MetaProjet** — régit `KitV2/AGENTS.md`.
- **Rapport d'audit :** §2.10.

## 1. Mission

Le **point d'entrée unique** du produit pour un agent consommateur : qu'est-ce
que ce Kit, où vit chaque zone, comment travailler, comment vérifier. Il
**route** vers les contrats et artefacts ; il ne les duplique jamais.

## 2. Contenu obligatoire

1. **Carte des zones** : tableau zone → mission en une ligne → pointeur
   (README de zone / fichiers canoniques).
2. **Source of truth** : où vit chaque vérité (règles, connaissance, recettes,
   snippets, templates, probes, outils, `.pi/`).
3. **Workflow** : les prompts natifs à utiliser dans l'ordre pour un travail
   non trivial (clarifier → planifier → tâches → implémenter → vérifier).
4. **Validation** : la gate complète et non ambiguë — toutes les commandes
   (validateur, gofmt, vet, lint, tests, gosec, govulncheck, probes) et la
   règle PARTIAL quand un outil manque.
5. **Limits** : ce que le Kit ne prétend pas couvrir (Wails, TUI, Pi discovery).

## 3. Règles

1. **Routage, pas duplication** : AGENTS.md ne contient ni corps de contrat ni
   corps de règle ; chaque zone est décrite en une ligne + pointeur.
2. **Autonomie produit** : AGENTS.md ne référence **jamais** le metaprojet
   (`.agent/`, `docs/`, chemins `../`). Les contrats de gouvernance sont pour
   les contributeurs, via le metaprojet.
3. Toute création de zone ou de contrat met à jour la carte dans le même
   commit.
4. La gate listée est exacte : toutes les commandes, ou explicitement
   « PARTIAL si outil absent ».

## 4. Maintenance

- Mise à jour synchrone avec : changements de zones, contrats, gate, prompts.
- Revue fraîcheur annuelle (déclencheur : audit de fraîcheur C0).

## 5. Patterns

- Carte + routage : l'agent trouve la zone puis le README de zone, jamais un
  manuel de 300 lignes.
- « If two files answer the same question, keep one » (déjà présent — le
  préserver).

## 6. Anti-patterns

- AGENTS.md qui grossit en manuel ; duplication de la charte ou des contrats ;
- chemin metaprojet dans le produit ; gate partielle non documentée.

## 7. Critères de validation

- [ ] C2 : AGENTS.md existe (déjà vérifié) et les zones référencées existent.
- [ ] C2 (étendu) : aucune référence `../` ou `.agent/` dans AGENTS.md.

## 8. Questions ouvertes

- Doit-on y ajouter un lien vers le registre d'artefacts (généré, Z7) ?
  (proposition : oui, une ligne — « le registre des artefacts est généré et
  référencé dans la carte ».)
