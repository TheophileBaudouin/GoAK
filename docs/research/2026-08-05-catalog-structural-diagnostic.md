# Diagnostic structurel du catalogue GoAK

**Date de diagnostic :** 2026-08-05  
**Périmètre :** `KitV2/knowledge/catalogs/` (42 `SKILL.md`) et les `SKILL.md` de recipes contenant des exemples Go.  
**Méthode :** lecture directe du tree, analyse lexicale des sections et blocs Go, recherche fraîche des sources officielles (repos, documentations, pkg.go.dev, issues/advisories) par des lanes de recherche indépendantes, vérification de 109 URL cataloguées (0 URL en erreur HTTP).  
**Statut :** diagnostic seul ; aucune correction de contenu du catalogue dans cette phase.

## Limites et correction des rapports

Les règles sont sous `KitV2/rules/**/SKILL.md`, pas sous les chemins plats mentionnés dans la demande (`rules/core/errors.md`, etc.). Les contrôles ont donc été effectués contre les modules réellement présents :

- `rules/core/errors/SKILL.md` — erreurs, retour et traitement unique ;
- `rules/core/universal/SKILL.md` — erreurs comme valeurs, exemples exécutables ;
- `rules/core/concurrency/SKILL.md` — contextes, sorties, annulation ;
- `rules/core/validation/golangci-lint/SKILL.md` — `errcheck`, fermetures explicites ;
- `rules/core/validation/gosec/SKILL.md` — retours ignorés et justifications ;
- `rules/registry/logging/SKILL.md` — journalisation structurée ;
- `rules/registry/testing/SKILL.md` — exemples testables et ressources fermées.

La gouvernance réellement présente est `.agent/kit-governance/`, contrairement à une observation subagent erronée qui la déclarait absente. Le tree local et les chemins réels font foi.

## Verdicts synthétiques

| Critère | Résultat |
|---|---:|
| Fichiers catalogues audités | 42 |
| Fichiers avec section `Sources vérifiées` | 39/42 (bibliothèques) |
| Références URL catalogues testées | 109, 0 erreur HTTP |
| Duplication interne identifiée | 22 bibliothèques, de gravité variable |
| Extraits Go avec retour ignoré / non traité | 18 bibliothèques |
| Références avec version non exacte ou ambiguë | 12 bibliothèques environ |
| Références de projets de référence sans section de sources formelle | 3 |
| Recipes avec `last-verified` historique (`2025-07-31`) | 6 |
| Recipes avec exemples exécutables présents | 10/10 recipes ciblées ; les rapports signalant des fichiers manquants confondaient `worker.go`/`cmd.go`/`main.go` avec les fichiers réellement présents (`pool.go`, `cobra.go`, `koanf.go`, `viper.go`) |

**Interprétation :** un fichier est `OK` seulement si le critère ne présente pas de défaut diagnostiqué. La source HTTP vivante ne prouve pas que chaque affirmation (version, maintenance, limitation) est correcte ; elle prouve uniquement l'accessibilité de l'URL.

## Phase 1 — diagnostic par fichier

### Catalogue `libraries/`

| Fichier | Duplication interne | Cohérence examples/rules | Sources / fraîcheur | Verdict |
|---|---|---|---|---|
| `age/SKILL.md` | `Security note` répète la frontière réseau/reposée de `Ne pas utiliser` ; les rappels de `Close` sont utiles mais redondants avec `Pièges`. | L41–45 ignorent plusieurs erreurs (`GenerateX25519Identity`, `Encrypt`, `Decrypt`, `io.Copy`, `Close`) ; contradiction directe avec `errors` et `errcheck`. | Sources datées 2026-08-05, URLs vivantes ; claims version/advisory à revalider dans la réécriture. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `bbolt/SKILL.md` | La note sécurité sur l’absence d’advisory recouvre partiellement l’avantage sécurité. | `db, _ := bolt.Open` et `b, _ := tx.CreateBucketIfNotExists` ignorent les erreurs ; valeur `Bucket(...).Get` sans garde nil. | Sources datées 2026-08-05, URLs vivantes ; version v1.5.0 à revalider. | `INCOHÉRENCE-RULE` |
| `bleve/SKILL.md` | `Notes` recouvre le batching de `Pièges connus`; `Alternatives` recouvre des exclusions de `Ne pas utiliser`. | Aucun retour ignoré critique détecté dans le bloc. | `last-verified: 2026-08-04`; URLs vivantes ; version et maintenance à rafraîchir. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `bubbles/SKILL.md` | `Notes` répète composition `tea.Model` et forwarding déjà exposés dans avantages/pièges. | L37 utilise `task(...)` non défini ; la construction `list.New` n'est pas traitée comme exemple complet. | Date 2026-08-04, URLs vivantes ; version `v2.1.x` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |
| `bubbletea/SKILL.md` | `Ecosystem notes` répète les avantages Charm ; `Version note` répète le piège import/renommage. | L39 traite l'erreur de `Run` par `os.Exit` dans l'extrait, sans retour de frontière ; exemple incomplet pour un skill de bibliothèque. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |
| `certmagic/SKILL.md` | `Security note` et `Ne pas utiliser` recouvrent le risque d'état global. | L42 affecte `err` sans montrer son traitement ; acceptable comme amorce mais pas comme exemple conforme complet. | Sources datées 2026-08-05, URL vivante ; à revalider. | `INCOHÉRENCE-RULE` |
| `chi/SKILL.md` | `Security note` et `Pièges` répètent la dépréciation/les advisories RealIP. | `http.ListenAndServe` est appelé sans retour traité dans l'extrait. | Date 2026-08-04, URLs vivantes ; version `v5` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |
| `cobra/SKILL.md` | Pas de duplication significative. | Pas d'extrait Go. | Sources datées 2026-08-04, URLs vivantes ; version exacte v1.10.2. | `OK` sur les trois critères |
| `coder-websocket/SKILL.md` | `Notes` répète transport-only/pinning exposés dans pièges. | Le serveur traite `Accept`; les retours de `Read`/`Write` sont traités. L'extrait est globalement cohérent. | Date 2026-08-04, URLs vivantes ; version `v1.8.x` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `colorprofile/SKILL.md` | `Notes` recouvre l'avantage de conversion. | Pas de violation détectée. | Date 2026-08-04, URL vivante ; version `v0.4.x` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `compress/SKILL.md` | `Security note` recouvre l'exclusion des entrées non bornées. | L39–44 ignorent les erreurs de constructeurs/`Write`/`Close`/`Copy`. | Sources 2026-08-05, URLs vivantes ; advisory et version à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `fyne/SKILL.md` | Aucune duplication substantielle identifiée. | Pas de retour ignoré critique dans l'extrait. | Date 2026-08-04, URLs vivantes ; à rafraîchir. | `OK` |
| `glamour/SKILL.md` | `Notes` répète les avantages de `notty`/styles. | Pas de violation détectée. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `go-git/SKILL.md` | `Notes` recouvre les avertissements v6/issues des pièges. | Pas de violation détectée dans l'extrait. | Date 2026-08-04, URLs vivantes ; à revalider. | `DUPLICATION` |
| `golang-jwt/SKILL.md` | `Security note` et `Ne pas utiliser` répètent le legacy path ; pièges répète la whitelist. | `signed, _ := token.SignedString` ignore l'erreur. | Sources 2026-08-05, URLs vivantes ; advisory à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `goldmark/SKILL.md` | `Security note` recouvre le piège XSS. | `md.Convert` retourne une erreur ignorée. | Sources 2026-08-05, URLs vivantes ; à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `harmonica/SKILL.md` | `Notes` recouvre `tea.Tick`/ressorts courts des pièges. | Pas de violation détectée. | Date 2026-08-04, URLs vivantes ; version `v0.2` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `huh/SKILL.md` | `Notes` répète WithProgram et l'intégration Bubble Tea. | `Run()` n'est pas traité dans l'extrait. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |
| `keygen/SKILL.md` | `Security note` recouvre le piège des secrets en arguments. | L39 ignore l'écriture de clé publique (`_ =` sans justification), tandis que la privée doit être traitée explicitement. | Date 2026-08-04, URLs vivantes ; version `v0.5.x` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |
| `kin-openapi/SKILL.md` | `Security note` et `Pièges` répètent fail-open/amplification/nil pointer. | L37 ignore `LoadFromData`. | Sources 2026-08-05, URLs vivantes ; à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `koanf/SKILL.md` | Pièges reprend les restrictions et avantages de cascade/StrictMerge. | Extrait sans gestion d'erreur (à traiter comme violation si le code est présenté comme minimal runnable). | Sources datées 2026-08-04, URLs vivantes ; version exacte v2.3.5 mais revalidation due. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `lipgloss/SKILL.md` | `Avantages` et `Pièges` répètent `style.Copy().Foreground`. | Extrait correct. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `log/SKILL.md` | `Notes` et `Avantages` répètent l'implémentation `slog.Handler`. | Exemple utilisable ; import alias non problématique, mais à clarifier. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `mcp-go-sdk/SKILL.md` | Pièges recouvre les exclusions hand-rolled/websocket. | Bloc présenté comme minimal use mais essentiellement commentaire ; pas un exemple compilable. | Date 2026-08-04, URLs vivantes ; à revalider. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `minio-go/SKILL.md` | Security note/pièges recouvrent le hardcoding credentials. | `minio.New` ignore l'erreur. | Sources 2026-08-05, URLs vivantes ; à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `modernc-sqlite/SKILL.md` | Notes/Avantages répètent zéro-CGO. | Extrait globalement conforme. | Sources datées 2026-08-04 ; version `v1.55+` ambiguë/à corriger. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `pgx/SKILL.md` | Security note/pièges répètent placeholders/SQLi. | `pgxpool.New`, `Query` ignorent erreurs ; `rows` n'est pas fermé. | Sources 2026-08-05, URLs vivantes ; à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `req/SKILL.md` | MAY extract et Avantages recouvrent retry/hooks. | Pas de code, conforme à extract-only. | Date 2026-08-04, URL vivante ; version non exacte et fiche extract-only à revalider. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `ristretto/SKILL.md` | Notes/pièges recouvrent TTL/issue #43. | Pas de violation détectée. | Date 2026-08-04, URL vivante ; à revalider. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `scs/SKILL.md` | Security note/pièges répètent Secure/HttpOnly/SameSite. | Extrait conforme. | Sources 2026-08-05, URLs vivantes ; à revalider. | `DUPLICATION` |
| `sequin/SKILL.md` | Notes/pièges répètent `len()` et bytes ANSI. | Extrait conforme. | Date 2026-08-04, URL vivante ; version range `v0.3.x`. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `sqlc/SKILL.md` | `Hard limits`, `Ne pas utiliser`, `Pièges` répètent dynamic queries/embed/SQLite ; cas fort. | Aucun bloc Go exécutable ; SQL/commandes non audités comme Go. | Date 2026-08-04, URLs vivantes ; version non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `ssh/SKILL.md` | Security note/pièges recouvrent auth/host key/timeouts. | `log.Fatal(srv.ListenAndServe())` traite au niveau process, mais n'explique pas la distinction erreur/arrêt normal. | Date 2026-08-04, URLs vivantes ; version ambiguë `v0.4.x`. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `templ/SKILL.md` | Notes/pièges répètent `go:generate`. | Extraits globalement conformes, mais intégration de génération doit être vérifiée. | Sources 2026-08-04, URLs vivantes ; version non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `testcontainers-go/SKILL.md` | Security note/pièges recouvrent pinning image/Terminate. | Les erreurs de `GenericContainer` et `MappedPort` sont ignorées. | Sources 2026-08-05, URLs vivantes ; version v0.43.0 à revalider. | `DUPLICATION + INCOHÉRENCE-RULE` |
| `testify/SKILL.md` | Pièges et préférence stdlib répètent les checks triviaux. | Extraits conformes. | Sources 2026-08-04, URLs vivantes ; claim push/release à clarifier. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `validator/SKILL.md` | Security note/pièges répètent Namespace/Value. | Extraits conformes. | Date 2026-08-04, URLs vivantes ; version non exacte. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `viper/SKILL.md` | Avantages/inconvénients/pièges répètent singleton/concurrency/encoding ; cas fort. | Pas de code. | Date 2026-08-04, URLs vivantes ; à revalider. | `DUPLICATION + SOURCE-PÉRIMÉE` |
| `wish/SKILL.md` | Security note/pièges recouvrent host key/middleware/auth. | `wish.NewServer` ignore l'erreur ; `ListenAndServe` est fatal au niveau process. | Date 2026-08-04, URLs vivantes ; version `v2` non exacte. | `DUPLICATION + INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE` |

### `reference-projects/`

| Fichier | Duplication | Rules/examples | Sources | Verdict |
|---|---|---|---|---|
| `ardanlabs-service/SKILL.md` | Pas de duplication interne significative. | Aucun bloc Go exécutable. | Pas de section `Sources vérifiées`; URL primaire absente dans le corps ; claims datés 2026-08-02 mais non traçables dans le fichier. | `SOURCE-ABSENTE` |
| `go-starter/SKILL.md` | Pas de duplication substantielle. | Aucun bloc Go. | Pas de section sources formelle ; claim de last push/maintenance à revalider. | `SOURCE-ABSENTE` |
| `pagoda/SKILL.md` | Pas de duplication substantielle. | Aucun bloc Go. | Pas de section sources formelle ; claim `pushed 2026-07` contredit la vérification du release/repo signalée par la lane fraîche. | `SOURCE-PÉRIMÉE` |

### Recipes contenant des exemples Go

Les recipes sont hors du verdict du tableau « catalogue » mais incluses comme demandé.

| Fichier | Duplication | Exemple/rule | Source/fraîcheur |
|---|---|---|---|
| `recipe-cli-interactif/SKILL.md` | Non diagnostiquée. | Code de démarrage traite `Run` via `fmt.Println`/`os.Exit`, tandis que le modèle de recipe recommande l'erreur explicite ; source date 2025-07-31. | `SOURCE-PÉRIMÉE` (last-verified historique). |
| `recipe-cli-minimal/SKILL.md` | Non diagnostiquée. | Forme `flag` retourne l'erreur ; conforme. | `SOURCE-PÉRIMÉE` (2025-07-31). |
| `recipe-desktop-app/SKILL.md` | Non diagnostiquée. | `panic(err)` au point de démarrage est explicite mais doit rester limité à la frontière process ; source 2025-07-31. | `SOURCE-PÉRIMÉE`. |
| `recipe-graceful-shutdown/SKILL.md` | Non diagnostiquée. | `log.Fatal(err)` à la frontière est cohérent ; source 2025-07-31. | `SOURCE-PÉRIMÉE`. |
| `recipe-rest-chi/SKILL.md` | Non diagnostiquée. | `http.ListenAndServe` ignore l'erreur dans l'extrait court ; le code réel de recipe utilise une implémentation plus complète. | `SOURCE-PÉRIMÉE`. |
| `recipe-sqlite-sqlc/SKILL.md` | Non diagnostiquée. | `sql.Open` et `GetFoo` ignorent des erreurs dans l'extrait ; le code réel traite les retours. | `INCOHÉRENCE-RULE + SOURCE-PÉRIMÉE`. |
| `recipe-worker-pool/SKILL.md` | Non diagnostiquée. | `g.Wait()` est retourné ; conforme. Le code réel est `pool.go` et le test existe. | `SOURCE-PÉRIMÉE`. |
| `recipe-cli-cobra/SKILL.md` | Non diagnostiquée. | Pas de code inline ; `cobra.go`/`cobra_test.go` présents. | Date 2026-08-03, URL à revalider. |
| `recipe-config-koanf/SKILL.md` | Non diagnostiquée. | Pas de code inline ; `koanf.go`/test présents. | Date 2026-08-03, URL à revalider. |
| `recipe-config-viper/SKILL.md` | Non diagnostiquée. | Pas de code inline ; `viper.go`/test présents. | Date 2026-08-03, URL à revalider. |

## Conclusion de Phase 1

Les deux cas de calibration sont systémiques :

1. La fiche bilingue imposée a créé une répétition structurelle dans presque tout le catalogue ; la duplication est souvent entre `Security note`/`Notes`/`Alternatives` et les six sections françaises ajoutées ensuite. Ce n'est pas un défaut isolé de `bubbles`.
2. Les extraits Markdown ne sont pas compilés par la gate Go. Au moins 18 fiches montrent des retours ignorés, et le validateur ne sait pas distinguer un exemple Go de prose ni comparer son comportement aux rules chargées.
3. Les dates et URLs ne suffisent pas à prouver la fraîcheur : les sources sont accessibles mais certaines versions sont ranges, et trois reference-projects n'ont pas de section de sources formelle.

Le diagnostic justifie les trois durcissements demandés. Il ne justifie pas encore une modification du produit : les règles `rules/core/` et le contrat de frontmatter sont des zones protégées, et la modification de `validate-kitv2.py` change la gate publique. Une proposition séparée et une validation explicite sont nécessaires avant Phase 2.
