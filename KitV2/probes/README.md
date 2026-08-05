# Go kit probes

Les probes sont les **évaluations produit exécutables** du Kit (charte,
Layer 6) : des scénarios déterministes, sans LLM ni service externe, qui
prouvent que le Kit fait ce qu'il prétend. Chaque probe termine par un verdict
observable et un exit code.

## Inventaire (15 probes)

| Probe | Recette / capacité exercée | Scénario observable |
| --- | --- | --- |
| `auth-jwt` | recipe-auth-jwt | Émission et vérification HS256 Bearer, rejet des tokens invalides. |
| `auth-session` | recipe-auth-session-scs | Création et lecture de session signée, expiration. |
| `cli-cobra` | recipe-cli-cobra | Sous-commandes Cobra, parsing des flags, sorties attendues. |
| `cli-interactive` | recipe-cli-interactive | Modèle Bubble Tea : état, événements, arrêt propre. |
| `cli-minimal` | recipe-cli-minimal | Parsing d'arguments explicites → config observée. |
| `config-koanf` | recipe-config-koanf | Chargement config, fusion, validation des entrées. |
| `config-viper` | recipe-config-viper | Chargement config, fusion, validation des entrées. |
| `desktop-app` | recipe-desktop-app | Limite de la couche applicative Wails : frontières service/modèle. |
| `graceful-shutdown` | recipe-graceful-shutdown | Arrêt propre sur signal, drain des workers. |
| `observability` | recipe-observability-slog-expvar | slog structuré + métriques expvar observées. |
| `offline` | tools/offline | Résolution hors-ligne des sources épinglées et de la toolchain locale. |
| `openapi-validation` | recipe-openapi-validation | Validation de requêtes/réponses contre le contrat OpenAPI. |
| `rest-chi` | recipe-rest-chi | Requête HTTP en process, statut et corps vérifiés. |
| `sqlite-sqlc` | recipe-sqlite-sqlc | Écriture/lecture d'une ligne dans une base temporaire locale. |
| `worker-pool` | recipe-worker-pool | Lot borné valide + annulation sur première erreur. |

## Règles

1. **Composition, pas duplication** : une probe importe la recette qu'elle
   exerce (`go-agent-kit-v2/recipes/...`) ou la capacité produit
   (`go-agent-kit-v2/tools/offline`).
2. **Déterminisme** : pas de réseau externe, pas de timing flaky, pas d'état
   partagé entre exécutions ; les ressources locales (port éphémère, base
   temporaire) sont nettoyées.
3. **Verdict explicite** : la dernière ligne de sortie est `…: PASS` (ou un
   échec clair + exit code non nul) ; une probe qui n'asserte rien est une
   erreur.
4. **Découverte automatique** : `run.sh` découvre les probes par glob
   (`probes/*/main.go`) — une liste codée en dur est interdite.
5. Les sorties brutes appartiennent à l'évidence du metaprojet
   (`docs/evidence/`), jamais au produit.

## Ajouter une probe

Une probe s'ajoute quand une **recette cœur** ou une **capacité produit** a un
comportement observable à prouver (Z6 §3.4 : toute nouvelle recette cœur est
candidate).

1. Créer `probes/<sujet>/main.go` — autonome, `package main`, verdict `PASS` +
   exit code.
2. Importer la recette exercée ; ne jamais recopier son code.
3. Exécuter `bash probes/run.sh` et vérifier `probes/<sujet>: PASS`.
4. Mettre à jour ce README (inventaire) ; la gate complète doit rester verte.

## Limites connues

La suite ne couvre pas : la découverte Pi individuelle des skills, le rendu
TUI dans un terminal réel, ni le webview GUI Wails — ces limites restent
déclarées dans `capabilities.yaml` (`known_limits`) et ne sont jamais
présentées comme couvertes par une probe.
