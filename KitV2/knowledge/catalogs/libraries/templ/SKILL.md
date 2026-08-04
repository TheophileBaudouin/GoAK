---
name: templ
description: "a-h/templ — compiled, type-safe HTML templates for Go (alternative to html/template). Use when rendering HTML server-side and you want compile-time type safety and XSS-safe auto-escaping, with component composition."
category: library
tags: [html, template, type-safe, xss, components]
last-verified: 2026-08-04
---

# templ — type-safe HTML templates

## Selection

`a-h/templ` (10.4k★, pushed 2026-07, CI with `ensure-generated`/`ensure-fmt`,
goreleaser releases).

**Actual reason (not stars):** it compiles `.templ` files to real Go
(`*_templ.go`) so the **compiler** catches type mismatches and bad signatures at
build time — unlike `html/template`'s runtime evaluation. Dynamic content is
auto-HTML-escaped by default (XSS-safe).

## Build integration

`.templ` is NOT runnable Go — it must be generated first.

```sh
templ generate              # parses .templ → emits *_templ.go
templ generate --watch      # dev: regenerate on change
templ generate --proxy=:8080 --watch   # + live reload via SSE
```

Wire `go:generate` so `go generate ./...` stays the single build entry point:

```go
//go:generate templ generate
```

## Component composition

```templ
templ Page(title string, children ...templ.Component) {
    <html><head><title>{title}</title></head>
    @children...
    </html>
}
templ Greeting(name string) {
    <p>Hello, {name}</p>
}
```

Compose via `@Component(...)`, pass children with `children...`, aggregate with
`templ.Join`. Exported (capitalised) components are importable across packages.

## Render to an http.ResponseWriter

```go
templ.Handler(Greeting("world)).ServeHTTP(w, r)
// or, for control:
comp := Greeting("world")
comp.Render(ctx, w)
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| stdlib `html/template` | No dependency, runtime-evaluated (type errors at run time). Fine for small/dynamic templates. |
| `gomarkup`/Jet/etc. | Other engines; templ's compiled-type-safety is its differentiator. |
| Client-side React/Vue | Different deployment model; templ is server-side render only. |

## Utiliser cette librairie quand

- Rendu HTML server-side avec sécurité de type à la compilation et
  auto-escaping XSS par défaut.
- La composition de composants (`@Component`, children, `templ.Join`) est
  souhaitée.
- Le chemin de rendu est chaud (SSR, streaming) : les templates compilés
  exécutent du code Go, sans réflexion runtime (voir
  `source:template:compiled-rendering`).

## Ne pas utiliser cette librairie quand

- Un template petit/dynamique suffit : `html/template` (stdlib) est sans
  dépendance, mais évalué au runtime.
- Le rendu est client-side (React/Vue) : templ est server-side uniquement.
- L'ajout d'une étape de génération (`templ generate`) au build est refusé.

## Avantages

- Compilé : le compilateur attrape les erreurs de type/signature au build.
- Auto-escape HTML par défaut (XSS-safe) — comme html/template mais typé.
- Composants composables et importables entre packages.
- Rendu mesuré plus rapide qu'html/template (benchmarks officiels et
  indépendants, voir `source:template:compiled-rendering`).

## Inconvénients

- `.templ` n'est pas du Go exécutable : étape de génération obligatoire au
  build (`go:generate templ generate`).
- Dépendance + toolchain : un écosystème en plus à maintenir.
- Server-side seulement : pas de rendu client.

## Pièges connus

- Toujours câbler `go:generate templ generate` pour garder `go generate
  ./...` comme point d'entrée unique du build.
- Garder le code généré sous contrôle de version ou le régénérer de façon
  déterministe (CI `ensure-generated`).
- Le rendu type-safe ne dispense pas de valider les entrées à la frontière
  (voir `source:security:input-validation`).

## Sources vérifiées

- [a-h/templ (repo officiel)](https://github.com/a-h/templ) — vérifié
  2026-08-02
- [templ.guide (docs officielles)](https://templ.guide/) — vérifié 2026-08-02
- [a-h/templ benchmarks](https://github.com/a-h/templ/tree/main/benchmarks) —
  vérifié 2026-08-04
- Artefacts internes : `source:template:compiled-rendering`,
  `source:go:html-template` (stdlib), `source:security:input-validation`
