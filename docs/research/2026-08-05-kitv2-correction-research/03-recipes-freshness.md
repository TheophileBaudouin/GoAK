# Recettes KitV2 — Fraîcheur des pratiques Go (audit 2026-08-05)

## Méthodologie

Pour chaque recette, les API et idiomes décrits ont été vérifiés contre des sources primaires (pkg.go.dev, go.dev/doc, v3.wails.io) consultées le 2026-08-05. Aucune affirmation de mémoire n'est utilisée ; chaque source est datée et URL-visible.

---

## Verdict par recette

### 1. recipe-cli-minimal — CONFORME

**Pratiques vérifiées :** `flag.NewFlagSet`, `flag.ContinueOnError`, `fs.SetOutput`, `fs.Parse(args)`, `flag.ErrHelp`.

- `flag.NewFlagSet(name string, errorHandling ErrorHandling) *FlagSet` — inchangé, présent sur pkg.go.dev/flag@go1.26.4 (Go 1.26.5 actuel). [Source](https://pkg.go.dev/flag@go1.26.4)
- `ErrorHandling` type avec constantes `ContinueOnError`, `ExitOnError`, `PanicOnError` — inchangé. [Source](https://github.com/golang/go/blob/go1.26.4/src/flag/flag.go)
- `FlagSet.Parse(arguments []string) error` — signature inchangée, retourne `ErrHelp` pour `-h`/`-help`. [Source](https://pkg.go.dev/flag@go1.26.4)
- `FlagSet.SetOutput(output io.Writer)` — inchangé. [Source](https://pkg.go.dev/flag@go1.26.4)
- Le pattern `*FlagSet` + `ContinueOnError` + `Parse([]string)` comme idiom testable reste la recommandation officielle (le package flag utilise ce pattern dans ses propres tests). [Source](https://pkg.go.dev/flag)

**last-verified :** reconduire au 2026-08-05 (aucun changement).

---

### 2. recipe-desktop-app — À CORRIGER (information partiellement obsolète)

**Pratiques vérifiées :** pattern « service Go pur sans import Wails », `application.New`, `application.Service`, `wails3 generate bindings`, `wails3 dev`, `wails3 build`.

- Le pattern « écrire les méthodes de service en Go pur, sans importer le runtime Wails, pour garder la testabilité » reste valide et est explicitement documenté dans la v3 docs (services = plain Go, bindings générés par analyse statique). [Source](https://v3.wails.io/features/bindings/services)
- `application.New(application.Options{Services: [...]})` — API toujours valide dans la v3 beta. [Source](https://v3.wails.io/reference/application)
- `wails3 generate bindings`, `wails3 dev`, `wails3 build` — commandes toujours documentées. [Source](https://v3.wails.io/)
- **Correction nécessaire :** Le SKILL.md affirme « Mobile is unsupported — Android/iOS are the #1/#2 most-upvoted unimplemented features ». Or la page Status (mise à jour le 3 août 2026) indique qu'iOS et Android sont désormais **expérimentaux** (non bloquants pour le beta desktop). Le texte est partiellement obsolète. [Source](https://v3.wails.io/status/)
- **Correction nécessaire :** Le SKILL.md dit « Wails v3 is Beta-to-GA, not stable » — c'est encore exact (la page Status dit « Current Status: Beta », le blog post confirme « This is a beta release, not the final 3.0 release »). [Source](<https://v3.wails.io/blog/wails-v3-beta/>, <https://v3.wails.io/status/>)
- **Correction nécessaire :** Le SKILL.md dit « v3 is desktop-only ». La page d'accueil v3.wails.io affiche désormais « Your desktop app is already a mobile app » avec des liens vers les guides mobiles. Le desktop reste le focus beta, mais mobile n'est plus « unsupported » — il est expérimental. [Source](https://v3.wails.io/)
- **Correction nécessaire :** La dernière version alpha v3.0.0-alpha2.117 est datée du 8 juillet 2026 (changelog). Le rythme de publication est très rapide (~1 release/jour). Le conseil « Pin the exact wails3 version » reste valide et même plus critique qu'avant. [Source](https://v3.wails.io/changelog/)

**Action :** Mettre à jour la section « ⚠ Wails v3 is Beta-to-GA » pour refléter le statut mobile expérimental (plus « unsupported ») et la disponibilité des guides mobiles. Reconduire last-verified si les corrections sont apportées.

---

### 3. recipe-graceful-shutdown — CONFORME

**Pratiques vérifiées :** `signal.NotifyContext`, `http.Server.Shutdown`, `context.WithTimeout`, `http.ErrServerClosed`.

- `signal.NotifyContext(parent context.Context, sig ...os.Signal) (ctx context.Context, stop func())` — ajouté en Go 1.16, toujours l'idiome canonique recommandé par la documentation Go et les sources primaires. [Source](https://pkg.go.dev/os/signal#NotifyContext)
- `http.Server.Shutdown(ctx context.Context) error` — API inchangée, toujours l'idiome pour drainer les connexions in-flight. [Source](https://pkg.go.dev/net/http#Server.Shutdown)
- `http.ErrServerClosed` — sentinel error toujours retourné par `Serve`/`ListenAndServe` pendant un shutdown gracieux. [Source](https://pkg.go.dev/net/http#ErrServerClosed)
- Le pattern « garder le wiring signal séparé de l'orchestration shutdown, passer un context.Context à Run » reste la meilleure pratique testable. Confirme par plusieurs sources 2025-2026 (DEV Community, Linux Future Tech, Wawandco). [Source](https://dev.to/gabrielanhaia/signalnotifycontext-in-go-clean-ctrl-c-handling-in-one-line-1o16)
- `context.WithTimeout` pour le deadline de drain — inchangé. [Source](https://pkg.go.dev/context#WithTimeout)

**last-verified :** reconduire au 2026-08-05 (aucun changement).

---

### 4. recipe-worker-pool — CONFORME

**Pratiques vérifiées :** `golang.org/x/sync/errgroup`, `errgroup.WithContext`, `g.SetLimit(limit)`, `g.Go`, `g.Wait`.

- `golang.org/x/sync/errgroup` — package toujours maintenu par l'équipe Go. Version courante : **v0.22.0** (publiée le 1 juillet 2026). [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- `SetLimit(n int)` — API inchangée : « limits the number of active goroutines in this group to at most n. A negative value indicates no limit. A limit of zero will prevent any new goroutines from being added. The limit must not be modified while any goroutines in the group are active. » [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- `WithContext(ctx context.Context) (*Group, context.Context)` — inchangé. [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- `Go(f func() error)` — inchangé, bloque si la limite est atteinte. [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- `Wait() error` — inchangé, retourne la première erreur non-nil et annule le contexte du groupe. [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- Le module `golang.org/x/sync/go.mod` indique `go 1.25.0` comme version minimale — compatible avec l'écosystème Go actuel. [Source](https://github.com/golang/sync/blob/master/go.mod)
- Aucune API dépréciée dans errgroup. `TryGo` ajouté comme méthode supplémentaire (non dépréciée). [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)
- Le conseil « SetLimit landed in Go 1.18 » est exact et inchangé. [Source](https://pkg.go.dev/golang.org/x/sync/errgroup)

**last-verified :** reconduire au 2026-08-05 (aucun changement).

---

## Résumé des verdicts

| Recette | Verdict | Action |
|---|---|---|
| recipe-cli-minimal | CONFORME | Reconduire last-verified |
| recipe-desktop-app | À CORRIGER | Mettre à jour le statut mobile (expérimental, plus unsupported) |
| recipe-graceful-shutdown | CONFORME | Reconduire last-verified |
| recipe-worker-pool | CONFORME | Reconduire last-verified |

## Sources consultées (toutes datées 2026-08-05)

1. `pkg.go.dev/flag@go1.26.4` — flag package API reference
2. `github.com/golang/go/blob/go1.26.4/src/flag/flag.go` — source stdlib flag
3. `v3.wails.io/` — Wails v3 homepage (status: Beta)
4. `v3.wails.io/blog/wails-v3-beta/` — Wails v3 Beta announcement
5. `v3.wails.io/status/` — Wails v3 Roadmap/Status (last updated Aug 3, 2026)
6. `v3.wails.io/changelog/` — Wails v3 changelog (alpha2.117 = Jul 8, 2026)
7. `pkg.go.dev/golang.org/x/sync/errgroup` — errgroup API reference (v0.22.0)
8. `github.com/golang/sync/blob/master/go.mod` — sync module go version
9. `dev.to/gabrielanhaia/signalnotifycontext-in-go-clean-ctrl-c-handling-in-one-line-1o16` — 2026 signal.NotifyContext guide
10. `dev.to/young_gao/graceful-shutdown-in-go-patterns-every-production-service-needs-3l9c` — 2026 graceful shutdown patterns
