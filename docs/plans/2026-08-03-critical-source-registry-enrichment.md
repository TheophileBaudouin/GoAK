# Enrichissement des sources critiques du registre Go — Plan d’implémentation

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Ajouter au registre canonique les références critiques manquantes pour le langage, la toolchain, la qualité et la sécurité Go moderne, sans transformer un index de découverte en doctrine.

**Architecture:** Le fichier `.agent/sources/Go-dev-kit-sources-et-references.md` reste l’unique registre de sources. Les ajouts sont bornés aux références primaires officielles et aux outils directement utilisés par la validation du kit; les bibliothèques tierces spécialisées restent hors de la priorité critique sauf justification explicite. Les sources de découverte existantes sont conservées mais leur priorité sera réalignée pour refléter leur rôle.

**Tech Stack:** Markdown, documentation officielle Go (`go.dev`, `pkg.go.dev`), outils de validation du kit.

---

## Task 1: Établir la matrice de couverture

**Files:**

- Read: `.agent/sources/Go-dev-kit-sources-et-references.md`
- Read: `KIT_CHARTER.md`
- Create: `docs/plans/2026-08-03-critical-source-registry-enrichment.md`

**Steps:**

1. Comparer les entrées `Priorité: Critique` actuelles aux besoins explicitement couverts par le charter et la validation du kit.
2. Classer chaque candidat comme officiel Go, outil de validation, bibliothèque maintenue ou découverte.
3. Exclure les ajouts qui sont seulement des préférences de bibliothèque ou des duplications d’entrées parapluie.
4. Conserver une liste courte et vérifiable: langage/spec, modules/toolchains, testing/fuzz/race/profiling, sécurité, `cmd/go`, stdlib structurante et validation effectivement utilisée.

**Expected:** Matrice critique dédupliquée et décision documentée avant édition.

## Task 2: Ajouter les références officielles fondamentales

**Files:**

- Modify: `.agent/sources/Go-dev-kit-sources-et-references.md`

**Steps:**

1. Ajouter `Go Language Specification`.
2. Ajouter `Go Modules` et `Go Toolchains`.
3. Ajouter `cmd/go`.
4. Ajouter `Go Testing`, `Go Fuzzing`, `Race Detector` et `Profiling`.
5. Ajouter `Go Security Best Practices` et `Go Vulnerability Database`.
6. Ajouter les références stdlib ciblées `context`, `errors`, `sync`, `net/http` et `database/sql` lorsqu'elles apportent une cible de recherche distincte de `pkg.go.dev`; documenter toute extension de cette liste dans l'évidence.
7. Pour chaque entrée, conserver le format existant: lien, description, utilité, priorité, catégorie.

**Expected:** Chaque lacune critique retenue possède une URL canonique, une responsabilité unique et une justification concise.

## Task 3: Ajouter les outils de validation réellement normatifs pour le kit

**Files:**

- Modify: `.agent/sources/Go-dev-kit-sources-et-references.md`

**Steps:**

1. Ajouter `govulncheck` avec la documentation officielle Go vulnérabilités.
2. Ajouter `gosec` comme outil de scan maintenu utilisé par la gate du kit, en le classant comme outil tiers de validation, pas comme règle Go.
3. Ajouter `golangci-lint` comme agrégateur de lint utilisé par la gate, avec sa documentation de configuration v2.
4. Ne pas ajouter automatiquement `mockery`, `Air`, des SDK IA ou des frameworks supplémentaires à la priorité critique: ils sont spécialisés et déjà présents dans les niveaux inférieurs.

**Expected:** Le registre reflète ses propres commandes de validation sans confondre standard officiel et outil tiers.

## Task 4: Réaligner les priorités de découverte

**Files:**

- Modify: `.agent/sources/Go-dev-kit-sources-et-references.md`

**Steps:**

1. Rétrograder `Awesome Go` et `Go by Example` de `Critique` vers `Haute`, car ce sont des index/exemples de découverte et non des autorités normatives.
2. Rétrograder `OpenAI Go SDK` vers `Haute` ou conserver sa priorité actuelle seulement si le kit décide explicitement que l’IA est une capacité cœur; par défaut, appliquer `Haute` car elle est domaine-spécifique.
3. Mettre à jour la section `Niveau S` pour supprimer les doublons et ne garder que les sources réellement indispensables.
4. Ne pas supprimer les références: ce changement est un réalignement de rôle, pas une suppression de connaissance.

**Expected:** Les niveaux de priorité ne contredisent plus la typologie des sources.

## Task 5: Vérifier le registre et obtenir une revue indépendante

**Files:**

- Read/Modify if needed: `.agent/sources/Go-dev-kit-sources-et-references.md`
- Evidence: `docs/evidence/2026-08-03/critical-source-registry/`

**Steps:**

1. Vérifier les titres, URL, priorités et doublons avec un script déterministe.
2. Vérifier les URL officielles et les pages de documentation avec des requêtes réseau bornées.
3. Conserver la sortie brute de validation dans `docs/evidence/2026-08-03/critical-source-registry/`.
4. Demander une revue fraîche en lecture seule sur le diff et la conformité au charter.
5. Corriger uniquement les problèmes confirmés par la revue.
6. Lancer les validateurs d’instructions et les diagnostics disponibles.

**Expected:** Diff minimal, liens vérifiables, registre cohérent, revue indépendante terminée. Toute lacune de recherche ou outil manquant reste explicitement `PARTIAL`/`BLOCKED`.
