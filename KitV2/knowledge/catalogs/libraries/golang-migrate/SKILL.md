---
name: golang-migrate
description: "github.com/golang-migrate/migrate/v4 v4.19.1 — versioned SQL migrations executed by the deployment CLI. Use for an explicit, single-run migration step; never import it into application replicas or run it automatically at startup."
category: library
tags: [database, migrations, sql, postgresql, deployment, cli]
last-verified: 2026-08-05
---

# golang-migrate — migrations SQL versionnées

## Selection

[`github.com/golang-migrate/migrate/v4`](https://github.com/golang-migrate/migrate)
v4.19.1 est admis pour appliquer, dans le déploiement, des migrations SQL
versionnées sur PostgreSQL. La CLI lit les fichiers dans l'ordre et maintient
l'état de migration. Le kit retient une commande externe unique plutôt qu'un
import Go runtime : chaque réplique de l'application reste indépendante du
protocole de déploiement du schéma.

## Admission checklist

- [x] **Problème distinct** : déployer un schéma versionné, non exécuter les
  requêtes de l'application (pgx couvre cette seconde frontière).
- [x] **Source primaire fraîche** : dépôt, release v4.19.1, documentation CLI
  et politique de sécurité vérifiés le 2026-08-05.
- [x] **Version compatible** : ligne v4 supportée, binaire pinable en
  `v4.19.1` et migrations SQL `up`/`down` sur filesystem.
- [x] **Responsabilité limitée** : migration de base, sans ORM, framework HTTP
  ni orchestration de répliques.
- [x] **Maintenance** : dépôt public actif, CI et historique de releases
  vérifiés ; revalider dans les 90 jours avant une nouvelle adoption.
- [x] **Qualité opérationnelle** : ordre, état et arrêt gracieux sont exposés
  par l'outil ; la procédure de sauvegarde/rollback demeure applicative.
- [x] **Sécurité** : politique `SECURITY.md` et surfaces d'advisories consultées
  le 2026-08-05 ; les secrets de l'URL ne sont ni commités ni journalisés.
- [x] **Alternatives** : un runner maison, `goose`, `tern` et migrations ORM ne
  réduisent pas la décision retenue ou ne sont pas admis dans le catalogue.
- [x] **Usage réel vérifiable** : la recipe PostgreSQL applique cette CLI avant
  le test d'intégration ; elle ne l'importe pas dans le processus Go.

## Minimal use

Installer la CLI dans l'environnement de déploiement puis appliquer une fois
les migrations détenues par le projet :

```sh
go install github.com/golang-migrate/migrate/v4/cmd/migrate@v4.19.1
migrate -path recipes/recipe-postgres-pgx/migrations \
  -database "$DATABASE_URL" up
```

`DATABASE_URL` vient du secret store du déploiement. L'application démarre
seulement après cette étape orchestrée ; elle ne lance jamais `migrate up` à
chaque démarrage de réplique.

## Alternatives considered

| Alternative | Verdict |
| --- | --- |
| Runner SQL maison | Rejeté : réimplique l'état, le verrouillage et les cas d'échec. |
| `pressly/goose` | Non admis : réévaluer séparément si ses choix opérationnels deviennent nécessaires. |
| `jackc/tern` | Non admis : alternative pgx-spécifique à réévaluer, pas une seconde recette. |
| Migrations ORM | Rejetées : le kit garde SQL révisable et une frontière sans ORM. |
| Import Go `migrate/v4` | Rejeté ici : créerait une migration automatique dans les répliques. |

## Utiliser cette librairie quand

- Une base partagée doit recevoir des migrations SQL révisables et versionnées.
- Le pipeline peut fournir une étape unique, privilégiée et observable avant le
  déploiement des instances applicatives.
- Les fichiers `up` et `down` font partie du VCS et ont une stratégie de
  compatibilité/rollback revue.

## Ne pas utiliser cette librairie quand

- Chaque réplique devrait exécuter les migrations au démarrage.
- Une modification de schéma ad hoc ou sans historique versionné est recherchée.
- Le projet ne peut pas fournir un verrouillage opérationnel, une sauvegarde ou
  une procédure de réparation après une migration interrompue.

## Avantages

- CLI simple, version pinable, fichiers SQL portables et migrations ordonnées.
- Support PostgreSQL officiel et convention claire `NNN_name.up.sql` /
  `NNN_name.down.sql`.
- Sépare explicitement les droits de migration des droits runtime.

## Inconvénients

- Une migration reste un changement d'état : les rollbacks destructifs et les
  déploiements multi-versions demandent une planification humaine.
- La CLI ne remplace ni backup, ni revue SQL, ni politique de déploiement.
- Les URLs de base peuvent contenir des secrets et demandent un encodage correct.

## Pièges connus

- Ne pas ajouter `migrate/v4` à `go.mod` pour cette recipe ni lancer la CLI dans
  le serveur HTTP.
- Exécuter une fois avec une identité de déploiement dédiée ; éviter les courses
  entre jobs et toutes les répliques.
- Tester `up` et `down` sur une base jetable, mais préférer les changements
  rétrocompatibles plutôt qu'un rollback destructif en production.
- Ne pas écrire `DATABASE_URL`, mots de passe ou SQL sensible dans les logs.

## Sources vérifiées

- [Dépôt officiel](https://github.com/golang-migrate/migrate) — CLI, drivers,
  usage filesystem et politique de sécurité, vérifié le 2026-08-05.
- [Release v4.19.1](https://github.com/golang-migrate/migrate/releases/tag/v4.19.1)
  — version pin retenue, vérifiée le 2026-08-05.
- [Documentation pkg.go.dev v4](https://pkg.go.dev/github.com/golang-migrate/migrate/v4)
  — API et compatibilité de la ligne v4, vérifiée le 2026-08-05.
- [Guide de migrations officiel](https://github.com/golang-migrate/migrate/blob/master/MIGRATIONS.md)
  — conventions et pratiques de migration, vérifié le 2026-08-05.

