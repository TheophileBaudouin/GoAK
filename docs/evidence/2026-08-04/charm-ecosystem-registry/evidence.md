# Evidence — Ajout de l'écosystème Charm au registre des sources (2026-08-04)

## Requête

Ajouter au kit toutes les tech/lib Charm (github.com/charmbracelet) utiles pour
le go-agent-kit, en excluant les outils destinés aux humains et les libs pas
assez matures/documents. Destination : `.agent/sources/Go-dev-kit-sources-et-references.md`.

## Méthode

1. Inventaire de l'organisation via l'API GitHub (`GET /orgs/charmbracelet/repos?per_page=100&sort=pushed&type=source`) : 42 dépôts source.
2. Métadonnées par dépôt candidat (`GET /repos/charmbracelet/<repo>` : created/pushed/archived/stars/lang) + dernière release (`GET /repos/.../releases/latest`).
3. Vérification du module path via le `go.mod` de chaque dépôt retenu (branche par défaut, `main` ou `master`).
4. Admission : librairie Go importable, mature (releases actives, docs), maintenue. Exclusion des apps humaines et des libs pré-1.0/expérimentales.

## Données brutes (2026-08-04, GitHub API)

### Retenues (12)

| Repo | created | pushed | ★ | latest release | module |
|---|---|---|---|---|---|
| bubbletea | 2020-01-10 | 2026-07-20 | 44 143 | v2.0.8 (2026-07-03) | charm.land/bubbletea/v2 |
| bubbles | 2020-01-18 | 2026-08-02 | 8 753 | v2.1.1 (2026-07-04) | charm.land/bubbles/v2 |
| lipgloss | 2021-03-01 | 2026-07-26 | 11 654 | v2.0.5 (2026-07-03) | charm.land/lipgloss/v2 |
| glamour | 2019-12-18 | 2026-06-14 | 3 624 | v2.0.1 (2026-06-12) | charm.land/glamour/v2 |
| huh | 2023-10-11 | 2026-08-03 | 7 073 | v2.0.3 (2026-03-10) | charm.land/huh/v2 |
| log | 2022-12-02 | 2026-07-06 | 3 343 | v2.0.0 (2026-03-09) | charm.land/log/v2 |
| wish | 2019-12-19 | 2026-07-31 | 5 372 | v2.0.3 (2026-07-31) | charm.land/wish/v2 |
| ssh | 2022-11-16 | 2026-08-02 | 50 | v0.4.2 (2026-07-31) | charm.land/ssh |
| harmonica | 2021-07-08 | 2026-05-28 | 1 576 | v0.2.0 (2022-04-15) | github.com/charmbracelet/harmonica |
| sequin | 2024-10-29 | 2026-04-27 | 806 | v0.3.1 (2025-01-27) | github.com/charmbracelet/sequin |
| colorprofile | 2024-09-13 | 2026-07-13 | 122 | v0.4.3 (2026-03-09) | github.com/charmbracelet/colorprofile |
| keygen | 2021-09-13 | 2026-03-16 | 171 | v0.5.4 (2025-10-02) | github.com/charmbracelet/keygen |

### Exclues et raisons

| Repo | ★ | Raison |
|---|---|---|
| crush | 27 065 | app agentic coding — outil destiné aux humains |
| glow | 26 674 | app CLI markdown — outil humain |
| gum | 24 147 | app CLI shell — outil humain |
| vhs | 20 534 | app CLI enregistrement terminal — outil humain |
| freeze | 4 766 | app CLI captures code — outil humain |
| mods | 4 531 | app CLI IA — outil humain |
| pop | 2 879 | app CLI email — outil humain |
| soft-serve | 7 126 | serveur Git — application, pas une lib |
| skate | 1 810 | KV store personnel — daemon/outil humain |
| charm | 2 497 | client Charm Cloud — déprécié (push 2025-03-06) |
| melt | 725 | outil CLI sauvegarde clés SSH — outil humain |
| wishlist | 1 642 | répertoire SSH — outil humain |
| fantasy | 901 | pré-1.0 (créé 2025-08, churn rapide) — pas assez mature |
| catwalk | 772 | pré-1.0 (créé 2025-06) — pas assez mature |
| ultraviolet | 366 | aucune release — pas assez mature |
| x | 306 | packages expérimentaux par définition |
| xunicode | 6 | expérimental |
| termenv | — | dépôt absent de l'org (recherche API : 0 résultat) — absorbé par colorprofile + x/ansi |
| keygen, promwish, git-lfs-transfer, confettysh, hotdiva2000, vhs-action, tree-sitter-vhs, meta, homebrew-tap, nur, scoop-bucket, pi-hyper-provider, .github, runway, inspo, wizard-tutorial, bubbletea-app-template | — | trop niche, outil, toy, infra org ou non-Go |

## Vérification module paths

`go.mod` récupérés sur la branche par défaut de chaque dépôt retenu (12/12) :
tous cohérents avec le tableau ci-dessus (vanity `charm.land/<name>/v2` pour les v2,
`github.com/charmbracelet/<name>` pour les v0).

## Changements

- `.agent/sources/Go-dev-kit-sources-et-references.md` : nouvelle section « # 21.
  Écosystème Charm (TUI, SSH, CLI) » avec 12 entrées au format existant (Lien,
  Description, Utilité potentielle, Priorité, Catégorie), modules et docs charm.sh.
- Niveau A : + Bubble Tea, Bubbles, Lip Gloss.
- Niveau B : + Glamour, Huh, Log, Wish, SSH, Harmonica, Sequin, Colorprofile, Keygen.

## Statut

PASS (inventaire, admission et édition vérifiés).

## Promotion KitV2 (suite à confirmation utilisateur)

Les 12 libs sont promues en **knowledge catalogs** du produit
(`KitV2/knowledge/catalogs/libraries/<name>/SKILL.md`, format chi, frontmatter
immutable : name/description/category/tags/last-verified) :

- Niveau A : bubbletea, bubbles, lipgloss
- Niveau B : glamour, huh, log, wish, ssh, harmonica, sequin, colorprofile, keygen

Chaque catalog : Selection (module vérifié + raison d'admission réelle),
Admission checklist, Minimal use, Alternatives considered, notes/sécurité.
`bubbletea` référence `recipe-cli-interactif` (déjà sur charm.land/bubbletea/v2).

### Changements

- 12 fichiers SKILL.md ajoutés.
- `KitV2/tools/validators/validate-kitv2.py` : `EXPECTED_PRODUCT_SKILLS` 33 → 45.

### Gate (2026-08-04, depuis KitV2/)

- `validate-instructions.py` : PASS
- `validate-kitv2.py` : PASS (45 product skills, 3 snippets, standalone, offline bundle)
- `gofmt -l .` : vide · `go vet ./...` : propre · `golangci-lint run ./...` : 0 issues
- `go test ./...` : propre · `gosec ./...` : 0 issues
- `probes/run.sh` : rest-chi, sqlite-sqlc, worker-shutdown, offline — PASS
- `govulncheck` : 1 vuln d'import non appelée (pré-existante, aucun code Go ajouté)

### Non inclus (décision)

- Recettes/templates complets par lib : non requis pour des catalogs ; le seul
  code de référence (bubbletea v2) existe déjà dans `recipe-cli-interactif`.
- Note pi-lens : MD060 (table-column-style) émet des avis ℹ sur les tableaux
  des nouveaux SKILL.md — quirk du linter, tableaux identiques au format chi
  existant ; la règle n'appartient pas à la gate du projet.
