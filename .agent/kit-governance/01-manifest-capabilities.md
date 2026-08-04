# C1 — Manifest et capabilities (contrat des deux fichiers racine)

- **Contrat MetaProjet** — régit `KitV2/manifest.yaml` et
  `KitV2/capabilities.yaml`.
- **Rapport d'audit :** §2.9.

## 1. Mission

`manifest.yaml` et `capabilities.yaml` décrivent l'**identité** et les
**capacités** du produit. Ce sont des métadonnées machine, **jamais** des
entrées d'instructions pour l'agent consommateur (champ `metadata_role` déjà
présent — il reste obligatoire). Ensemble, ils répondent à : « qu'est-ce que ce
produit, quelle version, que sait-il faire, où vit chaque capacité, quelles
sont ses limites connues ? »

## 2. Responsabilités (single source of truth par vérité)

| Vérité | Un seul propriétaire | L'autre fichier |
| --- | --- | --- |
| Identité (name, version, schema_version, language, principles, avoid) | `manifest.yaml` | ne la répète pas |
| Liste des capacités | `manifest.yaml` (`capabilities:`) | la décline avec source + status |
| Mapping capacité → chemin (`canonical:`) | `manifest.yaml` | `capabilities.yaml` (source + status) — **vérifié cohérent** |
| Comptes de couverture | **aucun fichier** — dérivés par `tools/generators/` (état cible : dossier à créer, Z7), vérifiés par C2 | jamais codés en dur |
| Limites connues | `capabilities.yaml` (`known_limits`) — structure `id`/`impact`/`status` = **état cible** (actuellement prose, à migrer) | — |

## 3. Règles actionnables

1. Tout chemin déclaré (`canonical:`, `source:`) doit exister dans le Kit.
2. `manifest.capabilities` et les clés de `capabilities.yaml` sont le même
   vocabulaire : même nom, même séparateur (kebab-case), aucun alias.
3. `coverage.*` est **interdit en dur** : le validateur le recalcule depuis
   l'arborescence et compare (product_skills = SKILL.md de rules + recipes +
   knowledge/catalogs ; rules = nb de modules rules ; recipes = nb de recettes ;
   probes = nb de probes découvertes ; project_templates = nb de shapes).
4. `known_limits` est une liste structurée (**état cible** : le fichier actuel
   est encore en prose — migration planifiée) : chaque entrée a `id`,
   `impact`, `status` (`open`/`resolved`/`accepted`) ; une limite `open` fait
   passer la capacité correspondante en `partial`.
5. Modifier un chemin canonique = modifier les deux fichiers **dans le même
   commit** ; C2 vérifie la cohérence.
6. `schema_version` incrémente à toute rupture de schéma des deux fichiers.

## 4. Patterns

- `metadata_role` explicite (« product manifest, not a Pi instruction
  entrypoint ») — conserver.
- Status de capacité honnête : `complete` / `partial` / `proposed` — jamais
  `complete` quand un scénario requis est manquant ou une limite connue ouverte.

## 5. Anti-patterns

- Comptes codés en dur (dérive mesurée : 33 vs 45 le 2026-08-04).
- Deux fichiers qui décrivent le même mapping sans vérification croisée.
- Capacité déclarée sans source de capacité ni critère de vérification.
- `known_limits` en prose non structurée (non suivable).

## 6. Critères de validation (C2)

- [ ] Chemins déclarés existants.
- [ ] Vocabulaire manifest↔capabilities identique.
- [ ] Comptes recalculés == comptes affichés (zéro compte en dur).
- [ ] Chaque capacité a `source` + `status` + critère de vérification.
- [ ] `known_limits` structuré et cohérent avec les status.

## 7. Questions ouvertes

- Le `principles` de manifest doit-il être vérifié comme sous-ensemble des
  règles core ? (proposition : oui, via Z1/C2.)
