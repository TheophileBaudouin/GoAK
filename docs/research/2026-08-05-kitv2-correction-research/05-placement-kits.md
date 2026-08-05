# Pratiques observées pour l'organisation de catalogues de skills/règles : candidats, pointeurs « à considérer » et statuts de maturité

**Date de recherche :** 2026-08-05
**Contexte :** Audit post-audit KitV2 — décision (a) organisation du catalogue de bibliothèques Go de Niveau B (21 YAML conditionnels dans `knowledge/catalogs/libraries/` alors que la zone est contractée SKILL.md-only) et (b) représentation du contenu `status: proposed` (5 pointeurs « à considérer ») livré dans le produit et indexé.
**Règles :** sources primaires ou documentation publique vérifiée (URL + date de consultation 20-08-05) ; pas de rappel de connaissance interne ; distinguer pratique officielle de pratique communautaire ; ne PAS imposer de décision, fournir des options avec trade-offs.

---

## 1. Comment les kits/registres comparables organisent les entrées « candidats / non encore admis / à considérer » vs. entrées admises

### Option A — Deux dossiers séparés (candidat vs. admis)

**Pratique observée :** `claude-scaffold-skill` (veekunth217) maintient deux fichiers JSON distincts : `registry/discovered.json` (file d'attente de candidats triés par score de qualité 0–100, jamais auto-promus) et `registry/skills.json` (entrées admises, vérifiées par un mainteneur) [1]. Le scraper ne verse jamais automatiquement un candidat dans `skills.json` — c'est une décision humaine explicite [1]. `skill-hub-registry` (CassianFlorin) utilise le même schéma : `candidates/discovered.json` pour les candidats non validés et `skillhub.index.json` pour le registre installable, avec un script d'ingest séparé (`ingest_candidate.py`) qui promeut un candidat à bas niveau de confiance (`trust.level: community`) [2].

**Trade-offs :**

- ✅ Séparation nette : le consommateur n'est jamais exposé à du contenu non validé.
- ✅ Le fichier de candidats sert de file de revue traçable.
- ❌ Double maintenance : chaque ajout doit être copié/supprimé dans les deux fichiers lors d'une promotion.
- ❌ Risque de désynchronisation si la promotion n'est pas faite immédiatement.

**Applicabilité à KitV2 :** Le contrat Z2 §4.3 prévoit déjà une promotion « pointeur → module vété » avec décision écrite [3]. Un dossier `pointers/` séparé dans `catalogs/libraries/` (comme prévu par Z2 §2) est cohérent avec cette approche.

### Option B — Statut unique dans un fichier unifié (champ `status`)

**Pratique observée :** `awesome-omni-skills` (diegosouzapw) utilise un fichier `REPOSITORY-SOURCES.md` unique avec un champ `status` par ligne (`candidate`, `tracked`, `accepted`) [4]. Les entrées `candidate` et `tracked` peuvent être auto-synchronisées par le runtime privé, mais les entrées publiques passent toujours par une revue humaine [4]. `agentcaps/registry` utilise un pipeline de promotion avec un champ `status` dans le schéma CatalogEntry : `draft → reviewed → published` [5]. L'Agent Registry de Google Cloud expose un champ de statut similaire pour les agents enregistrés [6].

**Trade-offs :**

- ✅ Un seul fichier à maintenir ; la promotion est un changement de champ.
- ✅ Facile à filtrer pour les consommateurs (`status: admitted` vs. `status: proposed`).
- ❌ Risque que le consommateur lise accidentellement du contenu non veté si le filtrage n'est pas implémenté.
- ❌ Le champ `status` doit être explicitement vérifié par le validateur (C2) — ajout de règle.

**Applicabilité à KitV2 :** Le format YAML-graphe Source existe déjà avec un champ `status` (utilisé par les pointeurs `adk-go.yaml` avec `status: proposed`) [7]. Étendre ce champ à tous les pointeurs Niveau B est la voie de moindre friction.

### Option C — Répertoires physiques séparés avec un README de transition

**Pratique observée :** `Cooper3363/ai-agent-skills-candidate-registry` utilise un dépôt séparé pour les candidats (screening + evidence warehouse) et un « stable installable registry » distinct [8]. `textrefs/registry` utilise un cycle de vie `draft → candidate → expert review → published` avec des dossiers distincts et un ADR (Architecture Decision Record) pour chaque transition [9]. `agentoperations/agent-registry` sépare les entrées par type de statut (`active`, `deprecated`, `experimental`) dans un registre unifié avec métadonnées de fédération [10].

**Trade-offs :**

- ✅ Isolation physique forte — impossible de consommer un candidat par accident.
- ✅ Chaque répertoire peut avoir son propre contrat de validation.
- ❌ Plus de complexité d'arborescence ; le consommateur doit savoir chercher dans plusieurs endroits.
- ❌ Risque de fragmentation si les frontières entre « candidat » et « admis » sont floues.

**Applicabilité à KitV2 :** Le contrat Z2 §2 prévoit déjà `catalogs/libraries/pointers/` comme dossier séparé pour les pointeurs « à considérer » [3]. C'est la voie la plus proche de la structure actuelle de KitV2.

---

## 2. Les pointeurs « à considérer » sont-ils indexés/discoverables ou exclus de l'index ?

### Option A — Inclus dans l'index mais marqués `status: proposed` (découvrables)

**Pratique observée :** `claude-scaffold-skill` inclut tous les candidats dans `discovered.json` (index complet de la file de revue) avec un drapeau `verified: false` [1]. Le consommateur peut filtrer `verified: true` pour n'obtenir que les entrés admises, mais l'index complet est public et navigable [1]. `awesome-omni-skills` inclut les lignes `candidate` et `tracked` dans `REPOSITORY-SOURCES.md` avec le champ `status` ; le runtime privé peut auto-activer la synchronisation pour `candidate` et `tracked` [4].

**Trade-offs :**

- ✅ Transparence totale : le consommateur voit ce qui est envisagé.
- ✅ Permet la découverte proactive de futures admissions.
- ❌ Le consommateur risque d'utiliser du contenu non veté s'il ne filtre pas.
- ❌ Le validateur C2 doit vérifier que le status est présent et cohérent.

### Option B — Exclus de l'index public ; accessibles uniquement via le chemin « pointers »

**Pratique observée :** `skill-hub-registry` (CassianFlorin) maintient `candidates/discovered.json` séparé du `skillhub.index.json` installable ; les candidats ne sont pas dans l'index de production tant qu'ils ne sont pas ingérés [2]. `agentcaps/registry` expose uniquement les CatalogEntry `published` dans l'index public `/.well-known/ai-catalog.json` ; les entrées `draft` restent internes au pipeline de revue [5]. `textrefs/registry` ne promeut les records qu'après expert review, et les records `draft` ne sont pas dans l'index public [9].

**Trade-offs :**

- ✅ Le consommateur n'est jamais exposé à du contenu non veté.
- ✅ L'index reste petit et rapide à parcourir.
- ❌ Les pointeurs « à considérer » sont invisibles, ce qui peut frustrer les utilisateurs qui cherchent une bibliothèque spécifique.
- ❌ Nécessite un mécanisme séparé pour consulter les pointeurs (ex. un rapport de revue).

### Option C — Index unifié avec filtre côté consommateur (status comme critère de filtrage)

**Pratique observée :** `agentoperations/agent-registry` indexe toutes les entrées (y compris `experimental`) mais fournit un champ `status` que le consommateur peut utiliser pour filtrer [10]. Le registre Nacos de Google expose un « Skill Registry » avec des niveaux de visibilité (PUB/PRIV) [11]. `portkey.ai` (Skills Registry) sépare les scopes (enterprise, personal, project, plugin) avec des précédences [12].

**Trade-offs :**

- ✅ Flexibilité maximale : le consommateur choisit son niveau de confiance.
- ✅ Un seul index à maintenir.
- ❌ Le consommateur doit implémenter le filtrage (complexité additionnelle).
- ❌ Risque que le filtrage soit ignoré ou mal configuré.

---

## 3. Pratiques de « statut de maturité » (draft/proposed/consider) documentées publiquement

### Pratique officielle : les spec Agentskills.io et AIP-3 ne définissent PAS de champ de statut de maturité

La spécification Agentskills.io (v0.1.0, Draft, 2026-04-01) définit uniquement les champs `name`, `description`, `version`, `author`, `license`, `tags` dans le frontmatter de `SKILL.md` — aucun champ `status` ou `maturity` [13]. L'AIP-3 (Anthropic, 2026-04-26, Final) étend le format avec `type`, `pricingModel`, `endpoints`, etc., mais ne prévoit toujours pas de champ de statut de maturité [14]. La RFC de découverte Cloudflare (agent-skills-discovery-rfc, v0.2.0, 2026-01-17) utilise un index `.well-known/agent-skills/index.json` qui énumère toutes les compétences sans champ de statut [15].

### Pratique communautaire : le statut de maturité est un ajout maison

- **`claude-scaffold-skill`** : utilise `verified: boolean` (true/false) comme unique indicateur de maturité, avec un score de qualité 0–100 pour les candidats [1].
- **`skill-hub-registry`** : utilise `trust.level: community` (basse confiance) pour les candidats ingérés, avec un pipeline de promotion vers `trust.level: official` [2].
- **`agentcaps/registry`** : pipeline `draft → reviewed → published` avec un champ `status` dans le schéma CatalogEntry [5].
- **`textrefs/registry`** : cycle `draft → candidate → expert review → published` avec ADR traçant chaque transition [9].
- **`Cooper3363/ai-agent-skills-candidate-registry`** : utilise un « screening and evidence warehouse » séparé du registre stable, avec des champs `smoke results`, `L2 simulated results`, `packaging queues` [8].
- **`mt-score-up-skill`** (areliw) : implémente une « maturity gate » avec un vocabulaire à 3 niveaux (`draft`, `semi-stable`, `stable`) où `status` ne peut pas dépasser le niveau de preuve disponible [16].
- **`KCP` (Cantara/knowledge-context-protocol)** : utilise un `catalog.yaml` de pointeurs avec des champs `intent` et `loading` pour contrôler quand et comment charger un savoir, mais pas de statut de maturité formel [17].

### Pratique KitV2 actuelle

KitV2 utilise déjà un champ `status` dans les YAML-graphes Source (ex. `adk-go.yaml` avec `status: proposed`) [7]. Le contrat Z2 §2 prévoit `catalogs/libraries/pointers/` pour les pointeurs « à considérer » [3]. Cependant, le contrat ne définit pas de vocabulaire de statut de maturité formalisé (draft/proposed/consider/accepted) ni de transitions contrôlées entre ces statuts.

---

## 4. Synthèse des options pour KitV2

### Question (a) : Comment organiser les entrées Niveau B (candidats non vetés) ?

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **A1 — Dossier `pointers/` séparé** (Z2 §2 existant) | Les pointeurs YAML restent dans `knowledge/catalogs/libraries/pointers/`, les SKILL.md admises dans `knowledge/catalogs/libraries/`. Le router indexe les deux mais les différencie par chemin. | Cohérent avec le contrat existant. Minimal effort. Le consommateur doit savoir chercher dans `pointers/` pour les candidats. |
| **A2 — Champ `status` dans les YAML** | Tous les catalogues (YAML et SKILL.md) utilisent un champ `status` (`proposed`, `admitted`). Le router filtre par statut. Un seul dossier. | Simple, un seul fichier à maintenir. Nécessite une mise à jour du validateur C2 pour vérifier le champ `status`. |
| **A3 — Deux dossiers + README de transition** | `catalogs/libraries/` pour les admises, `catalogs/libraries-candidates/` pour les candidats, avec un README expliquant la différence. | Isolation forte. Plus de complexité d'arborescence. |

### Question (b) : Les pointeurs « à considérer » sont-ils indexés ?

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **B1 — Inclus dans l'index, status comme filtre** | Le router indexe tous les pointeurs (y compris `status: proposed`). Le consommateur filtre par statut. | Découvrable, transparent. Le consommateur peut accidentellement utiliser du contenu non veté. |
| **B2 — Exclus de l'index public** | Seules les entrées `status: admitted` sont dans le router. Les pointeurs sont accessibles via le chemin `pointers/` mais pas indexés. | Le consommateur n'est jamais exposé à du contenu non veté. Les pointeurs sont « cachés ». |
| **B3 — Index unifié avec métadonnée `maturity`** | Tout est indexé, mais chaque entrée porte une maturité explicite (`candidate`, `proposed`, `admitted`). Le consommateur choisit son seuil. | Flexible. Nécessite que le consommateur implémente le filtrage. |

### Question (c) : Statut de maturité formel ?

| Option | Description | Trade-offs |
|--------|-------------|------------|
| **C1 — Pas de statut formel (actuel)** | Les pointeurs YAML utilisent `status: proposed` de manière ad hoc. Pas de vocabulaire formalisé. | Simple, pas de changement. Risque d'incohérence entre les pointeurs. |
| **C2 — Vocabulaire à 3 niveaux** | `draft` (brouillon, pas encore revu) → `proposed` (à considérer, revue en cours) → `admitted` (vété, dans le catalogue principal). Transitions documentées dans le contrat Z2. | Cohérent, traçable. Ajoute de la complexité au processus de revue. |
| **C3 — Vocabulaire à 4 niveaux (inspiré de textrefs)** | `draft` → `candidate` → `reviewing` → `published`. Chaque transition nécessite une décision écrite dans Decisions.md. | Très rigoureux. Peut être trop lourd pour un petit catalogue. |

---

## Sources

1. veekunth217/claude-scaffold-skill — CONTRIBUTING.md — <https://github.com/veekunth217/claude-scaffold-skill/blob/main/CONTRIBUTING.md> (consulté 2026-08-05)
2. CassianFlorin/skill-hub-registry — PR #4 (candidate discovery) et #5 (ingest tooling) — <https://github.com/CassianFlorin/skill-hub-registry/pull/4> (consulté 2026-08-05)
3. KitV2 Z2 — Zone `knowledge/` contrat — `/Users/theophilebaudouin/Documents/devellopement/Go/.agent/kit-governance/11-zone-knowledge.md` (consulté 2026-08-05)
4. diegosouzapw/awesome-omni-skills — REPOSITORY-SOURCES.md — <https://github.com/diegosouzapw/awesome-omni-skills/blob/main/REPOSITORY-SOURCES.md> (consulté 2026-08-05)
5. agentcaps/registry — README.md — <https://github.com/agentcaps/registry/blob/main/README.md> (consulté 2026-08-05)
6. Google Cloud — Agent Registry manual registration — <https://docs.cloud.google.com/agent-registry/manual-registration> (consulté 2026-08-05)
7. KitV2 adk-go.yaml pointer — `/Users/theophilebaudouin/Documents/devellopement/Go/KitV2/knowledge/catalogs/libraries/pointers/adk-go.yaml` (consulté 2026-08-05)
8. Cooper3363/ai-agent-skills-candidate-registry — <https://github.com/Cooper3363/ai-agent-skills-candidate-registry> (consulté 2026-08-05)
9. textrefs/registry — PR #7 (draft lifecycle) — <https://github.com/textrefs/registry/pull/7> (consulté 2026-08-05)
10. agentoperations/agent-registry — <https://github.com/agentoperations/agent-registry> (consulté 2026-08-05)
11. Nacos Skill Registry — <https://nacos.io/en/docs/latest/manual/user/ai/skill-registry/> (consulté 2026-08-05)
12. Portkey Skills Registry — <https://portkey.ai/blog/skills-registry/> (consulté 2026-08-05)
13. agentskills.io Specification — <https://agentskills.io/specification> (consulté 2026-08-05)
14. agentproto/aip-3 — SKILL.md format — <https://github.com/agentproto/agentproto/blob/main/specs/aip-3.mdx> (consulté 2026-08-05)
15. cloudflare/agent-skills-discovery-rfc — <https://github.com/cloudflare/agent-skills-discovery-rfc/blob/main/README.md> (consulté 2026-08-05)
16. areliw/mt-score-up-skill — scripts/check_maturity_gate.py — <https://github.com/areliw/mt-score-up-skill/blob/main/scripts/check_maturity_gate.py> (consulté 2026-08-05)
17. Cantara/knowledge-context-protocol — CATALOG-SPEC.md — <https://github.com/Cantara/knowledge-context-protocol/blob/main/CATALOG-SPEC.md> (consulté 2026-08-05)
18. KitV2 N1 §4 — Conventions SKILL.md — `/Users/theophilebaudouin/Documents/devellopement/Go/.agent/kit-governance/30-conventions.md` (consulté 2026-08-05)
19. KitV2 Z2 §2 — Sous-domaines et formats — `/Users/theophilebaudouin/Documents/devellopement/Go/.agent/kit-governance/11-zone-knowledge.md` (consulté 2026-08-05)

---

*Recherche effectuée le 2026-08-05. Pas de décision imposée — options avec trade-offs uniquement.*
