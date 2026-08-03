# Audit d'intégration des ressources Niveau B (selon projet) — Plan

**Goal:** Vérifier séquentiellement que chaque ressource de la liste « Niveau B
(selon projet) » du registre source possède une intégration réelle et traçable
dans KitV2, puis auditer l'ensemble du registre, sans modifier les listes de
niveaux du document source.

**Architecture:** Le registre `.agent/sources/Go-dev-kit-sources-et-references.md`
reste la source de classement. L'intégration est recherchée dans les artefacts
existants de `KitV2` (règles, recettes, catalogues, templates, probes,
documentation et métadonnées). Le motif d'intégration pour les bibliothèques
tierces « selon projet » est l'entrée Source conditionnelle déjà utilisée par
l'audit Niveau S/A (zap, redis, nats, air, go-blueprint, openai-go) : un YAML
`kind: Source` avec métadonnées graph complètes, critères de sélection, limites
honnêtes et URL de source. Une simple mention dans un fichier partagé n'est pas
une intégration.

**Tech Stack:** Markdown/YAML, Go, scripts Python de validation, probes KitV2.

---

## Ressources Niveau B (selon projet)

1. GORM — `knowledge/catalogs/libraries/gorm.yaml`
2. Fiber — `knowledge/catalogs/libraries/fiber.yaml`
3. Kafka (franz-go) — `knowledge/catalogs/libraries/franz-go-kafka.yaml`
4. RabbitMQ (amqp091-go) — `knowledge/catalogs/libraries/amqp091-go.yaml`
5. Resty — `knowledge/catalogs/libraries/resty.yaml`
6. Cookiecutter — `knowledge/catalogs/cookiecutter.yaml` (générateur
   multi-langages, hors `libraries/` car non-Go, comme awesome-go/go-by-example)

## Protocole par ressource

1. Lire le libellé exact dans le registre (section concernée du document).
2. Chercher l'intégration dans `KitV2` (grep + go.mod + arborescence).
3. Classer: intégrée, partielle ou absente.
4. Pour une ressource absente/partielle, vérifier l'URL de la source primaire
   (requête bornée) puis ajouter l'entrée Source conditionnelle minimale.
5. Exécuter `python3 tools/validators/validate-kitv2.py` avant de passer à la
   suivante.
6. Mettre à jour la micro-tâche correspondante.

## Audit global (après la catégorie Niveau B)

1. Matrice de couverture de chaque entrée des 20 sections du registre
   (Niveau S/A/B + entrées non classées).
2. Classification: intégrée (artefact existant), couverte par règle/recette,
   ajoutée comme référence conditionnelle, hors périmètre avec raison.
3. Correction immédiate des sources importantes non intégrées, avec le même
   motif Source conditionnel.
4. Vérification de la cohérence croisée (doublons, chevauchements, relations).

## Décision initiale

Les 6 ressources Niveau B sont toutes absentes de KitV2 (grep, go.mod,
arborescence); aucune n'est un défaut du kit (chi/sqlc/stdlib restent les choix
canoniques), donc l'entrée Source conditionnelle est l'intégration minimale
conforme, cohérente avec l'audit S/A. Les sources sont vivantes (pushed récent,
non archivées) et leurs URL vérifiées par requête bornée le 2026-08-03.

## Validation finale

- Les listes de niveaux du registre restent textuellement inchangées.
- Chaque ressource reçoit un verdict et un chemin d'intégration.
- Les ajouts ont une source primaire et des métadonnées cohérentes
  (`validate-kitv2.py` : IDs stables uniques, relations résolues, aucun chemin
  metaprojet).
- Les validateurs et les probes applicables passent.
- Les limites (`PARTIAL`/`BLOCKED`) sont documentées honnêtement.
- Evidence dans `docs/evidence/2026-08-03/b-resource-integration-audit.md`.
