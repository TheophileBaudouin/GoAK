# Resource Router — documentation méta-projet

Source de vérité technique du système de routage sémantique du kit. Cette doc
est destinée aux **développeurs du méta-projet**. Le kit utilisateur ne
contient que l'index, l'outil, la skill et un README de consommation —
jamais cette documentation.

## 1. Objectif

Permettre à un agent Pi de répondre à « Quelles ressources du kit m'aident
pour cette tâche ? » sans charger le kit dans le contexte. Le système
retourne : les ressources pertinentes (top-K ≤ 5), pourquoi elles sont
pertinentes (termes matchés), où elles se trouvent (chemin), et quoi lire
ensuite (la skill guide l'agent). **L'index est uniquement un routeur** : il
ne contient pas le contenu des fichiers ; la source de vérité reste le kit
lui-même.

Ce que le système **ne doit pas** faire : remplacer les fichiers sources,
injecter massivement des résultats, polluer le contexte, demander à
l'utilisateur de reconstruire quoi que ce soit, écrire dans l'index.

## 2. Architecture

```
Méta-projet (droit d'écriture)          Kit installé (lecture seule)
─────────────────────────────          ────────────────────────────
.agent/router/build_index.py   ──────▶  router/index.json + meta.json
  scanner les zones indexables           (artefact généré, versionné)
  description + tags + terms              │
  JSON déterministe (tri par id)          ▼
.agent/router/test_build_index.py   .pi/extensions/kit-resource-router.ts
  fixtures + déterminisme + drift        outil Pi natif search_kit_resources
.agent/router/test_validate_kitv2_router.py  BM25 + synonymes + garde hors-domaine
  tests positifs/négatifs du contrôle    .pi/skills/kit-resource-routing/SKILL.md
  de gate                                 quand chercher / comment interpréter
                                          router/README.md (consommation)
Gate : validate-kitv2.py check_router() — schéma, hash, couverture, chemins
```

**Frontière inviolable** : le builder vit dans le méta-projet ; le runtime
vit dans le kit. Le runtime ne reconstruit jamais l'index, ne le modifie
jamais, ne modifie jamais le kit.

## 3. Cycle de vie de l'index

1. **Création** : `python3 .agent/router/build_index.py` depuis la racine du
   méta-projet → écrit `KitV2/router/{index,meta}.json`. Déterministe (aucune
   dépendance réseau ; PyYAML, déjà requis par les validateurs).
2. **Quand régénérer** : après tout changement d'une ressource indexable —
   `rules/`, `recipes/`, `knowledge/` (SKILL.md et YAML), `snippets/`,
   `templates/*/template.yaml`, `.pi/prompts/`, `.pi/skills/`. La gate
   (couverture) échoue tant que l'index est en dérive : impossible d'oublier.
3. **Détection des modifications** : `build_index.py --check` compare le hash
   et les compteurs ; `validate-kitv2.py` vérifie le hash stocké dans
   meta.json + la couverture complète + l'existence des chemins.
4. **Publier** : bump `manifest.yaml`/`capabilities.yaml` (version du kit),
   régénérer l'index (meta.version suit le manifest), gate complète, tag.
   Le consommateur reçoit l'index par l'install standard ; il ne fait rien.

## 4. Choix technologiques

| Choix | Décision | Raison (alternatives évaluées) |
| --- | --- | --- |
| Pas d'embeddings | BM25 (k1=1.2, b=0.75) + synonymes | Corpus ~200 descriptions curées : le BM25 surpasse ou égale les embeddings pour le routage sur petit corpus (recherche web 2026-08-05). L'agent LLM fait le tri final sur le top-K — il EST la couche sémantique. API (OpenAI) : coût + réseau + non-déterministe, et il faudrait encoder la requête côté consommateur. Local (Ollama) : exige un service chez l'utilisateur. Rejetés. |
| Stockage | JSON versionné (index.json + meta.json) | Lisible, diffable, lecture seule triviale, ~200 Ko. SQLite : surdimensionné à ce volume (réévaluer à ×100). |
| Outil agent | Extension Pi native `registerTool` | Schéma contraint (difficile à mal utiliser), zéro dépendance npm (typebox fourni par Pi), auto-découverte. CLI python3 : dépendance d'exécution + risque d'invocation. Rejetée. |
| Déclenchement | Skill imposant la recherche avant tout travail technique | Décision utilisateur (2026-08-05) ; explicite, zéro bruit. |
| Builder | Python stdlib + PyYAML | Même base que les validateurs existants ; déterministe, hors-ligne. |

**Limitations connues** : couverture limitée aux descriptions curées du
frontmatter (un contenu profond non décrit peut être manqué — assumé) ; la
garde hors-domaine (seuil 0.5 sur les tokens étendus) peut rejeter une
requête en domaine avec vocabulaire exotique (l'agent reformule) ; LSP sans
types node pour l'extension (voir Gotchas).

## 5. Règles de maintenance

- **Ajouter une ressource indexable** : lui donner une description frontmatter
  réelle (1..1024, vocabulaire technique, pas de générique) puis régénérer
  l'index ; la gate vérifie la couverture. Ne jamais éditer index.json à la
  main.
- **Modifier le routage** : qualité des synonymes dans l'extension
  (runtime-only, Z11) ; pénalité conditionnelle et poids de kind ; garde
  hors-domaine. Chaque changement = re-exécuter les 7 scénarios
  (raw/ dans l'évidence) + gate.
- **Tester** : `python3 -m unittest .agent/router/test_build_index.py
  .agent/router/test_validate_kitv2_router.py` puis `build_index.py --check`,
  `validate-kitv2.py`, `validate-instructions.py`, gate Go + probes.
- **Ne pas dégrader la qualité** : une description générique ou dupliquée
  noie le routage ; un synonyme qui mappe trop large crée des faux positifs
  (le rejeter et retester) ; ne jamais baisser la barre « vide > bruit ».
- **Frontière méta-projet/kit** : ne pas déplacer le builder dans le kit ni
  l'outil dans le méta-projet ; ne pas référencer `.agent/` depuis le kit.

## 6. Références

- Plan : `docs/plans/2026-08-05-resource-router.md`
- Contrat de zone : `.agent/kit-governance/21-zone-router.md`
- Évidence : `docs/evidence/2026-08-05/resource-router/`
- Décisions : `.pi/memory/Decisions.md`, Brief.md (§ Decisions), Agent.md
  (règles invariants + barre de qualité).
