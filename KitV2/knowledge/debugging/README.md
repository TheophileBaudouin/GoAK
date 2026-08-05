# Debugging — domaine de connaissance

Ce dossier est le domaine « debugging » du graphe de connaissance du Kit. Il
répond à une question unique :

> Comment diagnostiquer un échec Go observé (panique, blocage, course, fuite,
> lenteur, corruption) ?

C'est un domaine **d'échec observé** (charte : « Observed production failure »),
pas un domaine de bonnes pratiques générales : une procédure n'entre ici que si
elle résout un symptôme concret et reproductible, vérifié contre une source ou
une expérience documentée.

## Format des artefacts

- Un artefact par échec : fichier YAML-graphe `kind: Source` (ou `Pattern` pour
  une procédure de diagnostic réutilisable), id stable
  (`source:go:debugging:<slug>` ou `pattern:go:debugging:<slug>`), métadonnées
  complètes (id, title, kind, version, status, owner, tags, go_version,
  dependencies, last_verified) et `relationships.references` pointant vers la
  source primaire (docs officielles, issue Go, article vérifié).
- Sections obligatoires selon le schéma de la catégorie (voir
  `../patterns/` et `../anti-patterns/` pour les modèles existants).
- Le corps n'est **jamais** copié depuis une source : le YAML route, explique la
  décision et cite ; la source vit hors du Kit (résolue via `tools/offline/` ou
  le lien `references`).

## Critères d'admission

1. Un échec précis et reproductible est décrit (symptôme + détection).
2. Une cause racine vérifiée est établie (source primaire ou reproduction
   documentée) — pas d'hypothèse non étiquetée.
3. La procédure de diagnostic est actionnable (commandes, étapes, sorties
   attendues) et ne duplique aucune règle ou recette existante.
4. `last_verified` ≤ 12 mois (sinon warning, 18 mois → déprécié).

## Contenu interdit

- Conseils généraux « deboguer en Go » sans échec concret (→ hors périmètre).
- Corps de documentation copié ; sorties brutes d'évidence conservées hors du
  produit, dans le journal de maintenance du metaprojet.
- Duplication d'un pattern/anti-pattern existant (`../patterns/`,
  `../anti-patterns/`) ou d'une règle (`../../rules/`) — pointer, ne pas
  dupliquer.
- Hypothèse non vérifiée présentée comme fait.

## Roadmap

Ce dossier est vide volontairement : il ne se remplit que sur échec observé et
vérifié. Candidats typiques (à admettre un par un, avec source) :

- fuite de goroutine / `go test -race` — corrélation avec
  `anti-patterns/go-goroutine-leak.yaml` ;
- course détectée tardivement (flaky CI) ;
- blocage / deadlock (pprof goroutine dump) ;
- lenteur mesurée (pprof CPU) — corrélation avec `performance/`.

Un dossier de domaine ne vit que s'il a ≥ 1 artefact actif ; tant qu'il est
vide, ce README est le contrat et la roadmap.
