# Z6 — Zone `probes/` (évaluations produit exécutables)

- **Contrat MetaProjet** — régit `KitV2/probes/`.
- **Rapport d'audit :** §2.7.

## 1. Mission

La couche « évaluations produit » de la charte (Layer 6) : des scénarios
**exécutables, déterministes, sans LLM ni service externe**, qui prouvent que
le Kit fait ce qu'il prétend. Chaque probe termine par un verdict observable
et un exit code.

## 2. Structure d'une probe

```text
probes/<sujet>/
└── main.go          # autonome, verdict final : fmt.Println("...: PASS") + exit 0/1
```

- `probes/run.sh` **découvre** les probes (glob `probes/*/main.go`) — la liste
  codée en dur est interdite (régression détectée à l'audit).
- `probes/README.md` = contrat de zone (comment ajouter, quand, critères).

## 3. Règles

1. Une probe exerce une **recette cœur** (import, exécution) ou une **capacité**
   produit (offline, outillage) — relation `validated_by` tracée.
2. **Déterminisme** : pas de réseau externe, pas de timing flaky, pas d'état
   partagé entre exécutions ; les ressources locales (port éphémère, base
   temporaire) sont propres.
3. **Verdict explicite** : la dernière ligne de sortie est `…: PASS` (ou un
   échec clair + exit code non nul) ; une probe qui n'asserte rien est une
   erreur.
4. Toute nouvelle recette « cœur » est candidate à une probe (la gate C2
   n'exige pas encore la couverture complète — l'ajout est encouragé à
   l'admission de la recette).
5. Les sorties brutes appartiennent à l'évidence du metaprojet
   (`docs/evidence/`), jamais au produit.

## 4. Maintenance

- **Ajout** : scénario + assertion + découverte automatique + gate verte.
- **Modification d'une recette référencée** : re-run des probes concernées
  obligatoire.
- Limites connues (Pi discovery, Wails, TUI) : restent déclarées dans
  `capabilities.yaml` (`known_limits`) — une probe ne prétend pas les couvrir.

## 5. Patterns

- Probe = « recette exécutée dans un scénario consommateur » (composition, pas
  duplication).
- Une ligne `PASS` + exit code : sortie machine-lisible pour CI.

## 6. Anti-patterns

- Probe qui passe sans asserter ; probe orpheline ; liste en dur dans run.sh ;
- dépendance réseau/timing ; sortie brute non structurée.

## 7. Critères de validation

- [ ] C2 : run.sh découvre (pas de liste en dur).
- [ ] Chaque probe a un verdict explicite et un exit code.
- [ ] Les recettes « cœur » ont une probe (encouragé ; à rendre obligatoire
      quand la couverture recettes↔probes sera suivie par C2).

## 8. Questions ouvertes

- Comment sonder les 3 limites (Pi discovery, Wails, TUI) sans dépendance
  d'harnais ? (proposition : probes « doc + smoke manuel » documentées comme
  PARTIAL, jamais comme couvertes.)
