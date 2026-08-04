# Router — index de routage sémantique (lecture seule)

`router/` embarque l'index de routage du kit : un **artefact généré** qui permet
à un agent d'obtenir la direction vers les ressources pertinentes (règles,
recettes, catalogues, patterns, anti-patterns, sources, snippets, prompts,
skills) sans charger le kit dans le contexte.

## Ce que c'est

- `index.json` — les ressources indexées : `id`, `kind`, `path` (chemin relatif
  au kit), `description` (courte, écrite à la main dans le frontmatter),
  `tags`, `terms` (tokens pré-calculés pour la recherche).
- `meta.json` — provenance : version du kit, `index_sha256` (intégrité),
  compteurs par type, liste des stopwords (source unique partagée avec le
  runtime).

L'index est un **routeur uniquement** : il ne contient pas le contenu des
fichiers du kit. La source de vérité reste toujours les fichiers eux-mêmes —
chaque entrée pointe vers un chemin réel à lire.

## Règles

- **Ne jamais éditer `index.json` ou `meta.json` à la main.** Ce sont des
  artefacts générés ; toute modification est détectée par le validateur
  (`validate-kitv2.py` vérifie le hash et la couverture complète) et bloque la
  release.
- **Lecture seule au runtime** : l'outil `search_kit_resources`
  (`.pi/extensions/kit-resource-router.ts`) lit l'index, ne l'écrit jamais, ne
  modifie jamais le kit.
- **Jamais de reconstruction côté consommateur** : l'index est régénéré avant
  chaque release du kit ; vous n'avez rien à faire.

## Utilisation

L'agent appelle l'outil natif `search_kit_resources` avec une requête technique
(ex. « bounded worker pool with context cancellation »). L'outil retourne un
top-K compact : `kind`, `id`, chemin, termes matchés (la raison du match) et
une courte description. Le skill `kit-resource-routing` (`.pi/skills/`)
explique quand et comment l'utiliser.

## Schéma

```json
{
  "schema": 1,
  "resources": [
    {
      "id": "recipe-worker-pool",
      "kind": "recipe",
      "path": "recipes/recipe-worker-pool/SKILL.md",
      "description": "Bounded concurrent fan-out in Go…",
      "tags": ["concurrency", "errgroup"],
      "terms": ["bounded", "concurrent", "errgroup"]
    }
  ]
}
```
