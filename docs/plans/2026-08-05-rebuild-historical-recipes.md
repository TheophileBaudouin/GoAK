# Plan — reconstruction des recipes historiques KitV2 2.4.0 (2026-08-05)

## Goal

Reconstruire les dix recipes antérieures au lot 2.3.0 selon le contrat A1 :
code Go exploitable, documentation décisionnelle, tests de frontière et probe
déterministe par recette cœur, sans rompre leurs API publiques.

## Context

Le catalogue compte quinze recipes après le lot 2.3.0. Les dix historiques
(CLI flag/Cobra, Koanf/Viper, REST, SQLite/sqlc, workers, shutdown, TUI et
Wails) compilent mais leur maturité est hétérogène : des probes sont combinées
ou absentes, les documents n'ont pas tous les sections A1, et plusieurs
frontières présentent des défauts observables. Les changements 2.3.0 présents
dans le worktree sont une base à préserver, sans reset ni réécriture incidente.

## Constraints

- Préserver les répertoires et API publiques existantes ; seuls les ajouts non
  cassants sont permis. `NewModel` est une façade TUI nouvelle, non cassante.
- Wails reste un adaptateur Go sans import Wails runtime. La documentation v3
  le décrit comme alpha et ne prétend pas couvrir GUI/CGO.
- Aucun nouveau runtime Go : aligner seulement les pins déjà admis Koanf
  v2.3.6 et modernc.org/sqlite v1.56.0 après revue primaire. sqlc v1.31.1 est
  une CLI de génération, pas une dépendance runtime.
- Une probe locale, déterministe et autonome par recipe cœur. La probe combinée
  worker/shutdown disparaît pour éviter une couverture ambiguë.
- Sources primaires fraîches, aucune duplication des catalogues/règles, et
  `SKILL.md` inférieur à 500 lignes. Router généré par builder uniquement.

## Done

- Les dix documents respectent le format de référence, les noms et interfaces
  publiques sont conservés, et les exemples traitent leurs erreurs.
- La génération réelle sqlc v1.31.1 est exécutée et contrôlée sans dérive, ou
  explicitement `BLOCKED` si le binaire ne peut pas être obtenu.
- Les probes sont au nombre de 15 (15 recipes), sans Docker, réseau externe ni
  service persistant ; toutes donnent un verdict `PASS` observé.
- Manifest/capabilities passent en 2.4.0 avec 71 skills, 15 recipes,
  43 catalogues et 15 probes ; le routeur est régénéré.
- Gate complète, evidence et revue fresh-context sont consignées sans déclarer
  réussi un scénario non exécuté.

## Source ledger

| Domaine | Sources primaires à vérifier à l'écriture |
| --- | --- |
| flag / shutdown / HTTP | https://pkg.go.dev/flag ; https://pkg.go.dev/os/signal ; https://pkg.go.dev/net/http |
| Cobra | https://github.com/spf13/cobra ; https://pkg.go.dev/github.com/spf13/cobra |
| Koanf / Viper | https://github.com/knadh/koanf ; https://github.com/spf13/viper |
| REST chi | https://github.com/go-chi/chi ; https://pkg.go.dev/net/http |
| SQLite / sqlc | https://gitlab.com/cznic/sqlite ; https://github.com/sqlc-dev/sqlc |
| Workers | https://pkg.go.dev/golang.org/x/sync/errgroup |
| Bubble Tea | https://github.com/charmbracelet/bubbletea ; https://pkg.go.dev/charm.land/bubbletea/v2 |
| Wails | https://github.com/wailsapp/wails ; https://v3.wails.io/ |

## Acceptance tasks

| ID | État initial | Résultat vérifiable |
| --- | --- | --- |
| HR-01 | PENDING | Plan, tâches, ledger, décision et evidence créés avant code. |
| HR-02 | PENDING | Pins Koanf/SQLite et catalogues alignés sur sources primaires. |
| HR-03 | PENDING | CLI flag/Cobra + configuration réécrites et testées. |
| HR-04 | PENDING | REST/SQLite/workers/shutdown réécrits et testés. |
| HR-05 | PENDING | TUI/Wails réécrits et testés sans runtime Wails. |
| HR-06 | PENDING | Sept probes dédiées remplacent/complètent la couverture historique. |
| HR-07 | PENDING | sqlc v1.31.1 génère réellement les fichiers, ou verdict BLOCKED. |
| HR-08 | PENDING | Manifest 2.4.0, compteurs, routeur et gate complète PASS. |
| HR-09 | PENDING | Revue fresh-context lecture seule et intégration des remarques. |

