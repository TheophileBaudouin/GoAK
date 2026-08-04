# Go Dev Kit — Sources et Références

> Base de connaissances pour un kit de développement Go moderne.
>
> Objectif : couvrir API, CLI, microservices, workers, tooling, IA et projets production.

---

# 1. Cœur du langage Go

## Standard Library

### pkg.go.dev

- **Lien :** <https://pkg.go.dev/>
- **Description :** Documentation officielle de tous les packages Go.
- **Utilité potentielle :**
  - Référence primaire pour un agent IA.
  - Validation des APIs disponibles.
  - Génération de code conforme à la stdlib.
- **Priorité :** Critique
- **Catégorie :** Documentation / Référence

## Effective Go

- **Lien :** <https://go.dev/doc/effective_go>
- **Description :** Guide officiel des bonnes pratiques Go.
- **Utilité potentielle :**
  - Règles de style.
  - Patterns idiomatiques.
  - Amélioration du code généré.
- **Priorité :** Critique
- **Catégorie :** Best Practices

## Go Language Specification

- **Lien :** <https://go.dev/ref/spec>
- **Description :** Spécification normative du langage Go : syntaxe, types,
  interfaces, generics, déclarations et sémantique.
- **Utilité potentielle :**
  - Référence d'autorité pour la génération et la revue de code.
  - Vérification des comportements qui ne doivent pas être déduits d'exemples.
- **Priorité :** Critique
- **Catégorie :** Langage / Référence normative

## Go Modules

- **Lien :** <https://go.dev/doc/modules/managing-dependencies>
- **Description :** Documentation officielle de la gestion des modules,
  dépendances, sommes de contrôle, remplacements et workspaces Go.
- **Utilité potentielle :**
  - Initialisation et maintenance déterministes de `go.mod` et `go.sum`.
  - Résolution, mise à jour et vérification des dépendances.
- **Priorité :** Critique
- **Catégorie :** Dépendances / Tooling officiel

## Go Toolchains

- **Lien :** <https://go.dev/doc/toolchain>
- **Description :** Gestion officielle des versions du compilateur et du
  changement automatique de toolchain via `go`, `toolchain` et `GOTOOLCHAIN`.
- **Utilité potentielle :**
  - Reproductibilité locale et CI.
  - Choix explicite de la version Go supportée par un module.
- **Priorité :** Critique
- **Catégorie :** Tooling officiel / Reproductibilité

## Go Release Policy

- **Lien :** <https://go.dev/doc/devel/release>
- **Description :** Politique et historique officiels des versions Go,
  correctifs, cadence de publication et versions supportées.
- **Utilité potentielle :**
  - Définir les versions supportées et les fenêtres de mise à jour.
  - Éviter les décisions de compatibilité fondées sur une version obsolète.
- **Priorité :** Critique
- **Catégorie :** Cycle de vie / Toolchain

## golang.org/x/sync (errgroup)

- **Lien :** <https://pkg.go.dev/golang.org/x/sync/errgroup>
- **Description :** Extension semi-officielle de la stdlib maintenue par
  l'équipe Go : `errgroup` (fan-out borné avec première-erreur via
  `SetLimit`), `singleflight`, `semaphore`. Module : `golang.org/x/sync`.
- **Utilité potentielle :**
  - Workflows concurrents bornés (déjà utilisé par le kit :
    recipe-worker-pool).
  - Parallel agent tasks.
- **Priorité :** Haute
- **Catégorie :** Concurrence / Extended stdlib

## go/ast

- **Lien :** <https://pkg.go.dev/go/ast>
- **Description :** Analyse de code Go native de la stdlib : AST, parser,
  tokens, transformations, génération de code. Zéro-CGO, stdlib-only
  (completé par go/types et golang.org/x/tools/go/packages). Knowledge
  stdlib admis dans le kit.
- **Utilité potentielle :**
  - Analyse sémantique Go (refactoring, dépendances, génération).
- **Priorité :** Haute
- **Catégorie :** Langage / Analyse de code

---

# 2. Outils officiels Go

## gopls

- **Lien :** <https://github.com/golang/tools/tree/master/gopls>
- **Description :** Serveur de langage Go officiel (autocomplete,
  diagnostics, références, symboles, refactoring) — interface LSP pour
  Go. Outil externe (pas une dépendance Go).
- **Utilité potentielle :**
  - Capacités niveau IDE pour agents coding Go.
- **Priorité :** Haute
- **Catégorie :** LSP / Tooling officiel

## LSP Protocol

- **Lien :** <https://microsoft.github.io/language-server-protocol/>
- **Description :** Protocole universel de communication IDE↔langage
  (spécification) — permet aux agents d'interagir avec Go, Rust, Python,
  TypeScript, C++ via leurs serveurs de langage. Spécification (pas une
  dépendance Go).
- **Utilité potentielle :**
  - Agents coding multi-langages.
- **Priorité :** Haute
- **Catégorie :** Protocole / IDE

## Go Toolchain

- **Lien :** <https://go.dev/>
- **Description :** Outils officiels du langage Go.
- **Inclut :**
  - gofmt
  - go test
  - go vet
  - benchmark
  - fuzzing
  - race detector
  - pprof
  - trace

- **Utilité potentielle :**
  - Automatisation qualité.
  - Validation automatique par agent.
  - Analyse performance.
- **Priorité :** Critique
- **Catégorie :** Tooling

## go command

- **Lien :** <https://pkg.go.dev/cmd/go>
- **Description :** Référence complète de la commande `go`, de ses sous-
  commandes, variables d'environnement, flags et contraintes de build.
- **Utilité potentielle :**
  - Automatisation fiable des opérations de build, test, module et release.
  - Référence pour `GOOS`, `GOARCH`, `CGO_ENABLED` et `//go:build`.
- **Priorité :** Critique
- **Catégorie :** Tooling officiel / Build

## Go Testing

- **Lien :** <https://pkg.go.dev/testing>
- **Description :** Guide officiel du package `testing`, des tests unitaires,
  sous-tests, tests parallèles et benchmarks.
- **Utilité potentielle :**
  - Base commune pour les tests du kit et des projets consommateurs.
  - Référence avant l'emploi d'un framework d'assertions ou de mocks.
- **Priorité :** Critique
- **Catégorie :** Tests / Tooling officiel

## Go Fuzzing

- **Lien :** <https://go.dev/doc/tutorial/fuzz>
- **Description :** Fuzzing natif de Go avec `testing.F`, corpus de graines et
  réutilisation des cas trouvés.
- **Utilité potentielle :**
  - Détection reproductible de cas limites dans parseurs et frontières de confiance.
  - Renforcement des recettes de sécurité et de validation.
- **Priorité :** Critique
- **Catégorie :** Tests / Sécurité

## Go Race Detector

- **Lien :** <https://go.dev/doc/articles/race_detector>
- **Description :** Documentation officielle de l'analyse dynamique des accès
  concurrents avec `go test -race`.
- **Utilité potentielle :**
  - Validation des workers, serveurs et états partagés.
  - Référence pour intégrer le détecteur dans CI.
- **Priorité :** Critique
- **Catégorie :** Concurrence / Validation

## Go Profiling

- **Lien :** <https://go.dev/blog/pprof>
- **Description :** Référence officielle du profiling avec `pprof` pour
  diagnostiquer CPU, mémoire et latence; la commande `go tool trace` complète
  l'analyse des exécutions concurrentes.
- **Utilité potentielle :**
  - Mesurer avant d'optimiser.
  - Relier une hypothèse de performance à une observation reproductible.
- **Priorité :** Critique
- **Catégorie :** Performance / Validation

## govulncheck

- **Lien :** <https://pkg.go.dev/golang.org/x/vuln/cmd/govulncheck>
- **Description :** Outil officiel d'analyse des vulnérabilités connues dans le
  code et les dépendances d'un module Go.
- **Utilité potentielle :**
  - Vérifier les appels vulnérables réellement atteignables.
  - Compléter les tests, le lint et le scan de dépendances dans la gate.
- **Priorité :** Critique
- **Catégorie :** Sécurité / Validation officielle

## Go Security Best Practices

- **Lien :** <https://go.dev/security/best-practices>
- **Description :** Recommandations officielles pour sécuriser les programmes
  Go, maintenir les dépendances et utiliser les outils de validation.
- **Utilité potentielle :**
  - Référence de sécurité transversale pour le code généré.
  - Base des contrôles `govulncheck`, fuzzing, race detector et `go vet`.
- **Priorité :** Critique
- **Catégorie :** Sécurité / Validation officielle

## gosec

- **Lien :** <https://github.com/securego/gosec>
- **Description :** Analyseur statique de sécurité Go utilisé par la gate du
  kit pour détecter des constructions à risque.
- **Utilité potentielle :**
  - Ajouter un contrôle SAST complémentaire à `govulncheck`.
  - Exiger une justification explicite pour toute suppression ciblée.
- **Priorité :** Critique
- **Catégorie :** Sécurité / Validation tierce

## golangci-lint

- **Lien :** <https://golangci-lint.run/docs/configuration/>
- **Description :** Agrégateur de linters Go utilisé par la gate du kit pour
  centraliser les contrôles de qualité et de correction.
- **Utilité potentielle :**
  - Exécuter une configuration déterministe de linters.
  - Maintenir une configuration compatible avec la version majeure installée.
- **Priorité :** Critique
- **Catégorie :** Qualité / Validation tierce

## Go Vulnerability Database

- **Lien :** <https://pkg.go.dev/vuln/>
- **Description :** Base de vulnérabilités Go maintenue par l'écosystème Go et
  consultable par module et symbole affecté.
- **Utilité potentielle :**
  - Comprendre la portée d'un avis et la version corrigée.
  - Compléter l'analyse automatisée par une source de vulnérabilités tracée.
- **Priorité :** Critique
- **Catégorie :** Sécurité / Référence

## context

- **Lien :** <https://pkg.go.dev/context>
- **Description :** Package standard pour annulation, délais, échéances et
  valeurs liées à une opération.
- **Utilité potentielle :**
  - Contrôler la durée de vie des requêtes et goroutines.
  - Éviter les appels bloquants sans chemin d'annulation.
- **Priorité :** Critique
- **Catégorie :** Standard Library / Concurrence

## errors

- **Lien :** <https://pkg.go.dev/errors>
- **Description :** Package standard pour composer, envelopper et inspecter
  les erreurs avec `Is`, `As` et `Join`.
- **Utilité potentielle :**
  - Préserver la cause tout en exposant un contrat d'erreur stable.
  - Référencer les décisions sentinel, typed ou opaque.
- **Priorité :** Critique
- **Catégorie :** Standard Library / Erreurs

## sync et sync/atomic

- **Lien :** <https://pkg.go.dev/sync>
- **Description :** Primitives standard de synchronisation et d'opérations
  atomiques pour l'état partagé concurrent.
- **Utilité potentielle :**
  - Choisir mutex, wait group, once ou atomics sans réinventer une primitive.
  - Vérifier les invariants de durée de vie et de concurrence.
- **Priorité :** Critique
- **Catégorie :** Standard Library / Concurrence

## net/http

- **Lien :** <https://pkg.go.dev/net/http>
- **Description :** Package standard pour clients, serveurs, handlers, TLS et
  transport HTTP.
- **Utilité potentielle :**
  - Référence primaire avant un framework HTTP.
  - Construire des serveurs testables avec les interfaces standard.
- **Priorité :** Critique
- **Catégorie :** Standard Library / HTTP

## database/sql

- **Lien :** <https://pkg.go.dev/database/sql>
- **Description :** Abstraction standard Go pour pools de connexions,
  transactions, requêtes et annulation via contexte.
- **Utilité potentielle :**
  - Évaluer un driver ou générateur SQL sans confondre abstraction et moteur.
  - Référence des comportements de pool et de transaction.
- **Priorité :** Critique
- **Catégorie :** Standard Library / Base de données

---

# 3. Configuration

## Viper

- **Lien :** <https://github.com/spf13/viper>
- **Description :** Gestionnaire de configuration Go populaire.
- **Supporte :**
  - YAML
  - JSON
  - TOML
  - ENV
  - Flags

- **Utilité potentielle :**
  - Templates de projets.
  - Applications configurables.
- **Priorité :** Haute
- **Catégorie :** Configuration

## Koanf

- **Lien :** <https://github.com/knadh/koanf>
- **Description :** Alternative moderne et légère à Viper.
- **Utilité potentielle :**
  - Configuration modulaire.
  - Services modernes.
- **Priorité :** Haute
- **Catégorie :** Configuration

---

# 4. CLI

## Cobra

- **Lien :** <https://github.com/spf13/cobra>
- **Description :** Framework CLI utilisé par Kubernetes, Docker et Hugo.
- **Utilité potentielle :**
  - Création de CLI professionnelles.
  - Agents de développement.
  - Outils internes.
- **Priorité :** Critique
- **Catégorie :** CLI

---

# 5. Logging

## slog

- **Lien :** <https://pkg.go.dev/log/slog>
- **Description :** Logger structuré officiel depuis Go 1.21.
- **Utilité potentielle :**
  - Standard recommandé.
  - Compatible production.
- **Priorité :** Critique
- **Catégorie :** Observabilité

## Zap

- **Lien :** <https://github.com/uber-go/zap>
- **Description :** Logger haute performance Uber.
- **Utilité potentielle :**
  - Services nécessitant beaucoup de logs.
- **Priorité :** Haute
- **Catégorie :** Logging

## Zerolog

- **Lien :** <https://github.com/rs/zerolog>
- **Description :** Logger JSON très rapide.
- **Utilité potentielle :**
  - Microservices.
  - Applications performantes.
- **Priorité :** Haute
- **Catégorie :** Logging

---

# 6. Validation et Identifiants

## Validator

- **Lien :**
<https://github.com/go-playground/validator>

- **Description :**
Validation de structures Go.

- **Utilité potentielle :**
  - API REST.
  - Validation automatique.
- **Priorité :** Haute

## Google UUID

- **Lien :**
<https://github.com/google/uuid>

- **Description :**
Génération UUID standard.

- **Utilité potentielle :**
  - IDs distribués.
  - Microservices.
- **Priorité :** Haute

---

# 7. HTTP

## Resty

- **Lien :**
<https://github.com/go-resty/resty>

- **Description :**
Client HTTP riche.

- **Utilité potentielle :**
  - APIs externes.
  - Intégrations SaaS.
- **Priorité :** Moyenne

---

# 8. Frameworks HTTP

## Chi

- **Lien :**
<https://github.com/go-chi/chi>

- **Description :**
Router HTTP léger basé sur stdlib.

- **Utilité potentielle :**
  - APIs REST modernes.
  - Architecture propre.
- **Priorité :** Critique

## Gin

- **Lien :**
<https://github.com/gin-gonic/gin>

- **Description :**
Framework HTTP populaire.

- **Utilité potentielle :**
  - APIs rapides.
  - Projets existants.
- **Priorité :** Haute

## Fiber

- **Lien :**
<https://github.com/gofiber/fiber>

- **Description :**
Framework haute performance basé sur fasthttp.

- **Utilité potentielle :**
  - APIs nécessitant performance.
- **Priorité :** Haute

## Echo

- **Lien :**
<https://github.com/labstack/echo>

- **Description :**
Framework HTTP complet.

- **Utilité potentielle :**
  - APIs classiques.
- **Priorité :** Moyenne

---

# 9. Base de données

## sqlc

- **Lien :**
<https://sqlc.dev/>

- **Description :**
Génère du code Go depuis SQL.

- **Utilité potentielle :**
  - Alternative moderne aux ORM.
  - Code type-safe.
- **Priorité :** Critique

## sqlx

- **Lien :**
<https://github.com/jmoiron/sqlx>

- **Description :**
Extension de database/sql.

- **Utilité potentielle :**
  - SQL manuel simplifié.
- **Priorité :** Haute

## GORM

- **Lien :**
<https://gorm.io/>

- **Description :**
ORM Go populaire.

- **Utilité potentielle :**
  - CRUD rapide.
  - Prototypes.
- **Priorité :** Moyenne

---

# 10. Migration SQL

## golang-migrate

- **Lien :**
<https://github.com/golang-migrate/migrate>

- **Description :**
Gestionnaire de migrations SQL.

- **Utilité potentielle :**
  - Déploiement production.
- **Priorité :** Haute

---

# 11. Tests

## Testify

- **Lien :**
<https://github.com/stretchr/testify>

- **Description :**
Assertions et mocks pour tests Go.

- **Utilité potentielle :**
  - Tests lisibles.
- **Priorité :** Haute

## GoMock

- **Lien :**
<https://github.com/uber-go/mock>

- **Description :**
Framework officiel de mocks Uber.

- **Utilité potentielle :**
  - Tests unitaires complexes.
- **Priorité :** Haute

---

# 12. Cache

## go-redis

- **Lien :**
<https://github.com/redis/go-redis>

- **Description :**
Client Redis officiel Go.

- **Utilité potentielle :**
  - Cache.
  - Sessions.
  - Queues.
- **Priorité :** Haute

## Ristretto

- **Lien :** <https://github.com/dgraph-io/ristretto>
- **Description :** Cache mémoire haute performance avec politique
  d'admission (TinyLFU) et budget mémoire borné. Module :
  `github.com/dgraph-io/ristretto` (v2.4.x, Apache-2.0, zéro-CGO). Catalog
  admis dans le kit.
- **Utilité potentielle :**
  - Cache de réponses LLM, fichiers parsés, embeddings (avec budget).
- **Priorité :** Haute
- **Catégorie :** Cache / Mémoire

---

# 13. Messaging

## Franz-go Kafka

- **Lien :**
<https://github.com/twmb/franz-go>

- **Description :**
Client Kafka moderne.

- **Utilité potentielle :**
  - Event-driven architecture.
- **Priorité :** Haute

## RabbitMQ AMQP

- **Lien :**
<https://github.com/rabbitmq/amqp091-go>

- **Description :**
Client RabbitMQ officiel.

- **Priorité :** Haute

## NATS

- **Lien :**
<https://github.com/nats-io/nats.go>

- **Description :**
Messaging léger haute performance.

- **Priorité :** Haute

---

# 14. Observabilité

## OpenTelemetry Go

- **Lien :**
<https://opentelemetry.io/docs/languages/go/>

- **Description :**
Standard traces, métriques et logs.

- **Utilité potentielle :**
  - Monitoring microservices.
  - Debug automatique.
- **Priorité :** Critique

## Prometheus Client Go

- **Lien :**
<https://github.com/prometheus/client_golang>

- **Description :**
Client officiel Prometheus.

- **Priorité :** Haute

---

# 15. Docker / Développement local

## Air

- **Lien :**
<https://github.com/air-verse/air>

- **Description :**
Hot reload Go.

- **Utilité potentielle :**
  - Développement rapide.
- **Priorité :** Haute

---

# 16. Génération de code

## Mockery

- **Lien :**
<https://github.com/vektra/mockery>

- **Description :**
Générateur de mocks Go.

- **Priorité :** Haute

---

# 17. Sécurité

## JWT Go

- **Lien :**
<https://github.com/golang-jwt/jwt>

- **Description :**
Implémentation JWT.

- **Utilité potentielle :**
  - Authentification API.
- **Priorité :** Haute

---

# 18. IA / LLM

## Eino

- **Lien :** <https://github.com/cloudwego/eino> — docs <https://www.cloudwego.io/docs/eino/>
- **Description :** Framework d'orchestration d'applications LLM (workflows, graphes, streaming, tools, multi-agents) par CloudWeGo/ByteDance. **Pointeur uniquement** — pré-1.0 (v0.9.x), à étudier pour les patterns, pas à dépendre (kit ≠ framework). Pointeur catalog : `pointers/eino.yaml`.
- **Utilité potentielle :**
  - Étude des patterns d'orchestration pour agents style Claude Code.
- **Priorité :** Moyenne
- **Catégorie :** IA / LLM / Orchestration

## MCP (Model Context Protocol)

- **Lien :** <https://modelcontextprotocol.io> — SDK Go <https://github.com/modelcontextprotocol/go-sdk>
- **Description :** Protocole standard d'interopérabilité agents/outils (tool discovery, resources, prompts). SDK officiel Go v1.7.0 (maintenu avec Google) — catalog admis dans le kit.
- **Utilité potentielle :**
  - Serveurs/outils MCP compatibles Claude Code.
  - Interopérabilité multi-agents.
- **Priorité :** Haute
- **Catégorie :** Protocole / Agents

## OpenAI Go SDK

- **Lien :**
<https://github.com/openai/openai-go>

- **Description :**
SDK officiel Go pour API OpenAI.

- **Utilité potentielle :**
  - Agents IA.
  - Automatisation.
  - Copilotes.
- **Priorité :** Haute

## Ollama API Go

- **Lien :**
<https://github.com/ollama/ollama>

- **Description :**
API Go pour modèles locaux.

- **Utilité potentielle :**
  - IA locale.
  - Agents offline.
- **Priorité :** Haute

---

# 19. Templates projets

## go-blueprint

- **Lien :**
<https://github.com/Melkeydev/go-blueprint>

- **Description :**
Générateur de projets Go.

- **Utilité potentielle :**
  - Bootstrap rapide.
  - Templates agent.
- **Priorité :** Haute

## Cookiecutter

- **Lien :**
<https://cookiecutter.readthedocs.io/>

- **Description :**
Générateur de templates multi-langages.

- **Priorité :** Moyenne

---

# 20. Bases de connaissances / Snippets

## Awesome Go

- **Lien :**
<https://awesome-go.com/>

- **Description :**
Collection communautaire de bibliothèques Go destinée à la découverte.

- **Utilité potentielle :**
  - Source d'index RAG.
  - Découverte initiale avant vérification dans une source primaire.
- **Priorité :** Haute

## Go by Example

- **Lien :**
<https://gobyexample.com/>

- **Description :**
Exemples Go exécutables orientés apprentissage et découverte.

- **Utilité potentielle :**
  - Point de départ pour des snippets.
  - Vérification obligatoire dans la documentation primaire avant admission.
- **Priorité :** Haute

## Go Cookbook

- **Lien :**
<https://go-cookbook.com/>

- **Description :**
Recettes pratiques Go.

- **Utilité potentielle :**
  - Base de patterns.
- **Priorité :** Haute

## GitHub Code Search

- **Lien :**
<https://github.com/search>

- **Description :**
Recherche d'implémentations réelles.

- **Utilité potentielle :**
  - Trouver des patterns production.
- **Priorité :** Haute

## Sourcegraph

- **Lien :**
<https://sourcegraph.com/>

- **Description :**
Recherche intelligente dans des dépôts.

- **Utilité potentielle :**
  - Analyse codebase.
  - Recherche RAG.
- **Priorité :** Haute

---

# 21. Écosystème Charm (TUI, SSH, CLI)

Écosystème cohérent de Charm (<https://github.com/charmbracelet>) : TUIs,
SSH applicatif et CLI. Les modules v2 utilisent le vanity import `charm.land/...`.
Sont exclues ici les applications destinées aux humains (gum, glow, vhs, crush,
soft-serve…) et les bibliothèques pré-1.0 ou expérimentales (fantasy, catwalk,
ultraviolet, x).

## Bubble Tea

- **Lien :** <https://github.com/charmbracelet/bubbletea> — docs <https://charm.sh/bubbletea>
- **Description :** Framework TUI (Text User Interface) en Go, architecture MVU (Model-View-Update). Module : `charm.land/bubbletea/v2`.
- **Utilité potentielle :**
  - CLI interactives et interfaces terminal pour agents et outils internes.
  - Déjà utilisé par le kit (recipe-cli-interactif).
- **Priorité :** Critique
- **Catégorie :** TUI

## Bubbles

- **Lien :** <https://github.com/charmbracelet/bubbles> — docs <https://charm.sh/bubbles>
- **Description :** Bibliothèque de composants TUI pour Bubble Tea (listes, tables, textinput, spinner, paginator…). Module : `charm.land/bubbles/v2`.
- **Utilité potentielle :**
  - Composants réutilisables pour TUIs d'agents (sélection, formulaires, progression).
- **Priorité :** Haute
- **Catégorie :** TUI / Composants

## Lip Gloss

- **Lien :** <https://github.com/charmbracelet/lipgloss> — docs <https://charm.sh/lipgloss>
- **Description :** Définition de styles pour mises en page terminal (couleurs, bordures, alignement, largeurs). Module : `charm.land/lipgloss/v2`.
- **Utilité potentielle :**
  - Styling cohérent des sorties CLI/TUI générées par un agent.
- **Priorité :** Haute
- **Catégorie :** TUI / Style

## Glamour

- **Lien :** <https://github.com/charmbracelet/glamour> — docs <https://charm.sh/glamour>
- **Description :** Rendu Markdown stylé (feuilles de style) dans le terminal. Module : `charm.land/glamour/v2`.
- **Utilité potentielle :**
  - Afficher documentation, sorties LLM ou rapports Markdown dans une CLI.
- **Priorité :** Haute
- **Catégorie :** TUI / Markdown

## Huh

- **Lien :** <https://github.com/charmbracelet/huh> — docs <https://charm.sh/huh>
- **Description :** Construction de formulaires et invites terminal (input, select, confirm, multi-select). Module : `charm.land/huh/v2`.
- **Utilité potentielle :**
  - Saisie interactive structurée pour workflows agents (wizards, confirmations).
- **Priorité :** Haute
- **Catégorie :** TUI / Formulaires

## Log

- **Lien :** <https://github.com/charmbracelet/log> — docs <https://charm.sh/log>
- **Description :** Logger minimal et coloré pour CLI, implémente un handler `log/slog`. Module : `charm.land/log/v2`.
- **Utilité potentielle :**
  - Logs lisibles en terminal pour les outils CLI.
- **Priorité :** Moyenne
- **Catégorie :** Logging

## Wish

- **Lien :** <https://github.com/charmbracelet/wish> — docs <https://charm.sh/wish>
- **Description :** Framework d'applications SSH (serveur, sessions, PTY, middleware). Module : `charm.land/wish/v2`.
- **Utilité potentielle :**
  - Workbenches distants SSH pour agents (architecture H hybride local/remote).
- **Priorité :** Haute
- **Catégorie :** SSH / Applications

## SSH

- **Lien :** <https://github.com/charmbracelet/ssh> — docs <https://charm.sh/ssh>
- **Description :** API SSH serveur moderne fondée sur `golang.org/x/crypto/ssh` (sessions, PTY, signal). Module : `charm.land/ssh`.
- **Utilité potentielle :**
  - Serveurs SSH intégrés ; fondation de Wish.
- **Priorité :** Haute
- **Catégorie :** SSH

## Harmonica

- **Lien :** <https://github.com/charmbracelet/harmonica>
- **Description :** Animation physique (ressorts) pour TUIs. Module : `github.com/charmbracelet/harmonica`.
- **Utilité potentielle :**
  - Transitions et animations fluides dans les interfaces terminal.
- **Priorité :** Moyenne
- **Catégorie :** TUI / Animation

## Sequin

- **Lien :** <https://github.com/charmbracelet/sequin>
- **Description :** Lecture/écriture de séquences ANSI lisibles. Module : `github.com/charmbracelet/sequin`.
- **Utilité potentielle :**
  - Manipulation de texte terminal avec codes ANSI (couleurs, styles).
- **Priorité :** Moyenne
- **Catégorie :** Terminal / ANSI

## Colorprofile

- **Lien :** <https://github.com/charmbracelet/colorprofile>
- **Description :** Détection des capacités couleur du terminal (successeur de termenv). Module : `github.com/charmbracelet/colorprofile`.
- **Utilité potentielle :**
  - Adaptation des couleurs selon le terminal (256, truecolor).
- **Priorité :** Moyenne
- **Catégorie :** Terminal / Couleurs

## Keygen

- **Lien :** <https://github.com/charmbracelet/keygen>
- **Description :** Génération de paires de clés SSH (Ed25519, RSA, ECDSA). Module : `github.com/charmbracelet/keygen`.
- **Utilité potentielle :**
  - Génération de clés pour tooling SSH sécurisé.
- **Priorité :** Moyenne
- **Catégorie :** SSH / Sécurité

---

# 22. Desktop / GUI

## Wails

- **Lien :** <https://github.com/wailsapp/wails> — docs <https://wails.io>
- **Description :** Applications desktop avec backend Go et frontend web.
  v3 en Beta-to-GA (non stable — pinner la version exacte). Déjà utilisé par
  le kit (recipe-desktop-app).
- **Utilité potentielle :**
  - Alternatives à Claude Desktop, IDEs IA, interfaces visuelles d'agents.
  - Logique de service testable en Go pur (bindings documentés).
- **Priorité :** Haute
- **Catégorie :** Desktop / GUI

## Fyne

- **Lien :** <https://github.com/fyne-io/fyne> — docs <https://fyne.io>
- **Description :** GUI toolkit Go pur API (rendu OpenGL via cgo glfw), sans dépendance navigateur. v2.8.0 (BSD-3). **CGO requis** (limite documentée). Catalog admis dans le kit.
- **Utilité potentielle :**
  - Apps desktop sans frontend web (embarqué, léger).
- **Priorité :** Moyenne
- **Catégorie :** Desktop / GUI / Pure Go

# 23. Temps réel / WebSocket

## coder/websocket

- **Lien :** <https://github.com/coder/websocket>
- **Description :** Implémentation WebSocket moderne en Go pur (client +
  serveur, APIs context-aware, concurrency-safe). Successeur maintenu de
  `nhooyr/websocket` (déprécié — voir gotcha). Module :
  `github.com/coder/websocket`.
- **Utilité potentielle :**
  - Streaming de réponses LLM, événements d'agent, feedback d'outils.
  - Couche transport MCP, communication terminal/navigateur.
- **Priorité :** Haute
- **Catégorie :** Réseau / Temps réel / WebSocket

---

# 24. Git / Versionnage

## go-git

- **Lien :** <https://github.com/go-git/go-git>
- **Description :** Implémentation Git en pur Go (clone, fetch, commit,
  branch, diff, log) sans binaire `git` externe. v5.19.x (Apache-2.0), v6
  alpha en cours. Utilisé par Gitea, Pulumi, Keybase. Catalog admis dans le
  kit.
- **Utilité potentielle :**
  - Commits, diffs, analyse de dépôt par des agents.
- **Priorité :** Haute
- **Catégorie :** Git / VCS

# 25. Recherche / Indexation

## Bleve

- **Lien :** <https://github.com/blevesearch/bleve>
- **Description :** Moteur de recherche plein texte Go pur (index scorch,
  ranking BM25, facettes, highlight, géo), embarquable, zéro-CGO, zéro
  serveur. v2.6.0 (Apache-2.0). Catalog admis dans le kit.
- **Utilité potentielle :**
  - Recherche locale sur documents/code (agents).
- **Priorité :** Haute
- **Catégorie :** Recherche / Indexation

# 26. Browser automation / Computer use

## Playwright Go

- **Lien :** <https://github.com/mxschmitt/playwright-go>
- **Description :** Bindings Go pour Playwright (Chromium/Firefox/WebKit) —
  automation navigateur, computer-use agents. **Pointeur uniquement** :
  pré-1.0 par convention (v0.x miroir du driver), binaires navigateur lourds.
  Pointeur catalog : `pointers/playwright-go.yaml`.
- **Utilité potentielle :**
  - Agents web autonomes quand aucune API n'existe (API first).
- **Priorité :** Moyenne
- **Catégorie :** Browser / Automation

# 27. Code intelligence / Parsing

## Tree-sitter (binding officiel)

- **Lien :** <https://github.com/tree-sitter/go-tree-sitter>
- **Description :** Parsing incrémental multi-langages (AST, navigation,
  indexation) — binding **officiel** Go (le repo smacker est abandonné).
  **Pointeur uniquement** : pré-1.0 (v0.24.0) + CGO obligatoire. Pointeur
  catalog : `pointers/tree-sitter.yaml`.
- **Utilité potentielle :**
  - Indexation de code, chunking sémantique, extraction de symboles.
- **Priorité :** Moyenne
- **Catégorie :** Code intelligence / Parsing

# 28. Vector search

## sqlite-vec

- **Lien :** <https://github.com/asg017/sqlite-vec>
- **Description :** Recherche vectorielle dans SQLite (RAG local). **Pointeur
  uniquement** : pré-1.0 (v0.1.9), docs stale, bindings Go séparés (CGO/WASM).
  Pointeur catalog : `pointers/sqlite-vec.yaml`.
- **Utilité potentielle :**
  - RAG local sur petites machines (si besoin concret).
- **Priorité :** Moyenne
- **Catégorie :** Vector search / RAG

---

# Priorités pour un Agent Coding Go

## Niveau S (indispensable)

- Go Language Specification
- Go Modules
- Go Toolchains
- go command
- Go Testing
- Go Security Best Practices
- pkg.go.dev
- go/ast

## Niveau A (très utile)

- Effective Go
- Go Toolchain
- Go Fuzzing
- Go Race Detector
- Go Profiling
- Go Vulnerability Database
- context
- errors
- sync et sync/atomic
- golang.org/x/sync (errgroup)
- net/http
- database/sql
- slog
- OpenTelemetry
- sqlc
- chi
- Cobra
- Koanf
- Zap
- Validator
- Redis
- NATS
- Testify
- Air
- go-blueprint
- Go by Example
- Awesome Go
- OpenAI Go SDK
- Bubble Tea
- Bubbles
- Lip Gloss
- Wails
- coder/websocket
- go-git
- MCP (Model Context Protocol)
- Bleve
- Ristretto
- gopls
- LSP Protocol

## Niveau B (selon projet)

- GORM
- Fiber
- Kafka
- RabbitMQ
- Resty
- Cookiecutter
- Glamour
- Huh
- Log
- Wish
- SSH
- Harmonica
- Sequin
- Colorprofile
- Keygen
- Fyne
- Eino (pointeur)
- Playwright Go (pointeur)
- Tree-sitter (pointeur)
- sqlite-vec (pointeur)
