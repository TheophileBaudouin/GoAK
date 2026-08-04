# C0 — Charte d'application (cycle de vie des artefacts)

- **Contrat MetaProjet** — régit `KitV2/` (le produit). Statut : contrats de
  phase 2 (2026-08-04), référencé par C1, C2, Z1–Z10, A1, N1.
- **Autorité** : `KIT_CHARTER.md` (racine) reste l'autorité de processus. Ce
  contrat **opérationnalise** la charte : il ne la remplace ni ne la contredit.

## 1. Mission

Définir le cycle de vie de chaque artefact du Kit (ajout, modification,
dépréciation, retrait) et les règles transverses de travail — pour qu'un agent
ou développeur puisse enrichir le Kit dans 3–5 ans sans dérive.

## 2. Cycle de vie d'un artefact

```text
proposé → actif → déprécié → (retrait, après migration)
```

| Transition | Déclencheur | Conditions de sortie |
| --- | --- | --- |
| proposé → actif | Admission passée (source + question distincte + validation de la catégorie) | Métadonnées complètes, source primaire, relations résolues, gate verte, scénario observable exécuté (`PASS`/`PARTIAL`/`BLOCKED` documenté) |
| actif → déprécié | Source obsolète, doublon détecté, écosystème changé, `last_verified` > 18 mois non renouvelé | Décision écrite (Decision Record metaprojet), `status: deprecated`, note de remplacement, consommateurs identifiés |
| déprécié → retrait | Aucun consommateur actif, migration faite | Suppression **avec** Decision Record et mise à jour des références dans le même commit |

Règle : un artefact `proposed` **ne peut pas** être référencé par un artefact
`active` (le validateur rejette les relations vers du proposé/inexistant).

## 3. Versioning (semver par artefact)

Chaque artefact porte `version:` (entier dans les YAML-graphe existants, à
conserver ; semver à partir de la v2 des artefacts) :

- **major** : rupture de contrat de sortie (schéma, comportement observé,
  signature, frontmatter) ;
- **minor** : ajout compatible (nouvelle section, nouveau champ facultatif) ;
- **patch** : correction (typo, source, reformulation sans changement de
  comportement).

Toute montée **major** exige : décision écrite, migration documentée, mise à
jour des relations `supersedes`/`validated_by` dans le même commit.

## 4. Write-gate (évidence avant inclusion)

1. Le contributeur **propose** (plan ou issue) — jamais d'écriture directe pour
   un contenu nouveau.
2. L'admission exige une **source primaire vérifiée** (docs officielles, RFC,
   implémentation de référence maintenue, échec de production observé, standard
   communautaire prouvé) — pas « semble utile ».
3. L'artefact répond à une **question distincte** : si une règle/recette/pattern
   existant y répond déjà, le contributeur pointe au lieu d'écrire
   (duplication = échec d'admission).
4. La validation de la catégorie est exécutée (voir A1) et la gate passe.

## 5. Fraîcheur (`last_verified`)

- Toute donnée factuelle porte `last_verified: YYYY-MM-DD`.
- **12 mois** → warning validateur ; **18 mois** → statut déprécié proposé.
- La vérification ne consiste pas à bump la date : elle re-vérifie sources,
  versions, API et comportements cités, et met à jour le contenu si besoin.

## 6. Règles transverses de travail (metaprojet)

1. Un seul writer par worktree ; paralléliser uniquement la recherche en
   lecture.
2. Plan dans `docs/plans/` pour tout travail non trivial ; décision dans
   `.pi/memory/Decisions.md` ; évidence brute dans `docs/evidence/<date>/`.
3. Revue fresh-context (subagent read-only) avant déclaration de fin ; les
   remarques sont intégrées ou tranchées avec raison.
4. Trois échecs identiques d'affilée → stop et rapport, pas de boucle.
5. La gate est la seule preuve mécanique ; le scénario observable est la seule
   preuve comportementale ; jamais l'un pour l'autre.

## 7. Contenu interdit partout dans le Kit

- Mémoire/decisions/évidence/historique du metaprojet.
- Secrets, chemins durs, sorties brutes de commandes.
- Duplication de corps (chaque vérité vit une fois ; le reste pointe).
- Placeholders vides (dossiers `.gitkeep` sans contrat) : les zones planifiées
  vivent en roadmap dans le README de zone, pas en dossiers fantômes.

## 8. Critères de validation (exigibles par C2)

- [ ] Validateur C2 passe (dont fraîcheur et cohérence manifest/capabilities).
- [ ] Gate Go verte (gofmt, vet, lint, tests, race, gosec, govulncheck — ou
      PARTIAL documenté si outil absent).
- [ ] Probes concernées passées (scénario observable).
- [ ] Aucune duplication introduite (contrôle C2).
- [ ] Relations résolues (aucune référence vers `proposed`/inexistant).
- [ ] Décision écrite pour toute transition de statut.

## 9. Questions ouvertes

- Semver entier (`1`) vs semver string (`1.2.0`) pour les artefacts : aligner
  sur le schéma validé dans Z10.
- Politique des « capabilities » (manifest) : voir C1.
