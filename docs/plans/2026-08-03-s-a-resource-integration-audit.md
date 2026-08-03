# Audit d’intégration des ressources Niveau S et A — Plan d’implémentation

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Vérifier séquentiellement que chaque ressource des listes Niveau S et Niveau A du registre source possède une intégration réelle et traçable dans KitV2, sans modifier ces listes.

**Architecture:** Le registre `.agent/sources/Go-dev-kit-sources-et-references.md` reste la source de classement. L’intégration est recherchée dans les artefacts existants de `KitV2` (règles, recettes, catalogues, templates, probes, documentation et métadonnées). Une ressource déjà couverte est documentée comme telle; une ressource absente n’est ajoutée qu’à l’emplacement canonique approprié, après vérification de la source primaire et avec une validation observable.

**Tech Stack:** Markdown/YAML, Go, scripts Python de validation, KitV2 validators and probes.

---

## Protocole par ressource

1. Lire le libellé exact dans le registre.
2. Chercher l’intégration dans `KitV2` et dans les métadonnées metaprojet.
3. Classer: intégrée, partielle ou absente.
4. Pour une ressource absente/partielle, choisir l’intégration minimale conforme à son rôle: catalogue pour une bibliothèque, règle pour une contrainte, recette pour une procédure, source-cache pour une référence officielle.
5. Implémenter et vérifier avant de passer à la suivante.
6. Mettre à jour la micro-tâche correspondante.

## Décision initiale

Le premier audit montre que le produit contient déjà des intégrations riches pour
Go, Effective Go, `pkg.go.dev`, `slog`, `chi`, `sqlc`, Cobra, Koanf, OpenTelemetry
et les validations. Les autres ressources seront traitées séquentiellement; une
simple mention dans le registre ou une importation accidentelle dans un test ne
sera pas considérée comme une intégration complète.

## Validation finale

- Les sections Niveau S et Niveau A restent textuellement inchangées.
- Chaque ressource reçoit un verdict et un chemin d’intégration.
- Les ajouts ont une source primaire et des métadonnées cohérentes.
- Les validateurs et les probes applicables passent.
- Les limites (`PARTIAL`/`BLOCKED`) sont documentées honnêtement.
