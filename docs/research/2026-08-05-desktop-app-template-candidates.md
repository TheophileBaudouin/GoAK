# Dossier d'admission — template desktop-app (Wails)

Date : 2026-08-05. Auteur : passe de durcissement gouvernance méta-projet
(finding Rodin D), recherche déléguée Web-Research (subagent fresh-context,
lecture seule). Statut : **préparation de dossier uniquement** — l'admission
elle-même (copie, épinglage, attribution, gate) appartient à la passe suivante
dans `KitV2/templates/`.

## 1. Contexte

`recipes/recipe-desktop-app/SKILL.md` (Wails v3, rejette Tauri « Rust, hors
périmètre d'un kit Go ») et `probes/desktop-app/main.go` existent. Le reste du
graphe couvre donc la capacité desktop, mais `templates/TEMPLATES.md` ne liste
desktop-app nulle part (roadmap = grpc, microservice, monolith, cloud-service).
Selon la politique Z5 §2, un template doit être un projet open source réel,
MIT, maintenu, testé, **ultra-spécifique** (quasi exclusivement la techno du
template), petit, à responsabilité unique — jamais un scaffold agent-écrit.

## 2. État de l'écosystème Wails (vérifié 2026-08-05)

| Version | Statut | Dernière | Install |
| --- | --- | --- | --- |
| v2 | stable | v2.13.0 (2026-07) | `go install github.com/wailsapp/wails/v2/cmd/wails@latest` |
| v3 | beta (pré-release) | dernière pré-release au 2026-08-05 | `go install github.com/wailsapp/wails/v3/cmd/wails3@latest` |

- Wails v3 est en alpha depuis janvier 2023, passé en beta mi-2026 : l'API
  desktop est stable mais la release reste pré-release (vérifié via l'API
  GitHub le 2026-08-05 : latest stable = v2.13.0, tags v3.0.0-beta.*). La
  recette du Kit documente d'ailleurs « Beta-to-GA transition ».
- Sources : <https://v3.wails.io/blog/wails-v3-beta/> et
  <https://github.com/wailsapp/wails/releases> (vérifiés par le subagent et
  confirmés en lecture seule par la revue fresh-context via l'API GitHub).

## 3. Candidats évalués contre Z5 §2 (aucun ne passe)

| Candidat | Licence | Activité | Stack annexe | Tests/CI | Verdict |
| --- | --- | --- | --- | --- | --- |
| JinGongX/SuiDemo | MIT (vérifiée API) | push 2026-04-12, 86★ | Vue 3 + vue-i18n + SQLite + Tailwind | non | ÉCHEC — c'est un template/starter, pas une app ; stack lourde ; sans tests |
| kazuph/obails | MIT (vérifiée) | push 2026-06-12, 2★ | TypeScript + Node.js | non | ÉCHEC — trop petit, mono-contributeur, sans tests/CI |
| JessonChan/captain-api | MIT (vérifiée) | push 2025-10-20, 3★ | Vue 3 + TypeScript | non | ÉCHEC — trop petit, inactif 9+ mois, sans tests/CI |
| ehsanpo/Fakering | — | 0★, abandonné | — | — | ÉCHEC |
| gofurry/wails-v3-vue-starter | MIT | 4★ | Vue 3 | — | ÉCHEC — starter, pas une app |

**Exemples officiels** (`wailsapp/examples`) : collection de projets de
démonstration (file-association, updater, events, binding, systray-menu,
drag-n-drop, window, wml) — des démos de fonctionnalités, pas une application
réelle à responsabilité unique. Exclus (et désormais explicitement exclus par
la politique Z5 §2, précision D-2026-08-05-14 : une source = application
réelle, pas starter/démo).

## 4. Conclusion honnête

**Aucun candidat ne satisfait la politique Z5 §2 au 2026-08-05.** L'écosystème
Wails v3 est trop jeune (beta) et trop petit pour produire un projet réel,
MIT, mono-techno, testé et parcourable. On n'assouplit pas les critères pour
trouver un candidat : la politique templates est un portail dur (Z5 §2), et
admettre un starter ou une démo créerait exactement le défaut que Z5 §2.4
interdit (fourre-tout, non fonctionnel au sens produit).

Conséquences :

1. **Ligne roadmap** desktop-app = `planned` avec note « aucune source MIT
   conforme au 2026-08-05 » (texte prêt dans le plan méta-projet, annexe D ;
   à appliquer dans `KitV2/templates/TEMPLATES.md` à la passe suivante) —
   la capacité reste reconnue (recette + probe), le template attend une
   source conforme.
2. **Déclencheur de ré-évaluation** : la GA de Wails v3 (et la maturation de
   son écosystème, ~6-12 mois) ; la ligne roadmap le mentionne.
3. **Leçon transférable** : la politique Z5 §2 exclut désormais explicitement
   les starters/templates tiers et les recueils de démos comme source
   (D-2026-08-05-14) — évite de re-évaluer des faux candidats.

## 5. Commandes de vérification à exécuter au moment de l'admission réelle

À relancer sur tout futur candidat (non exécutées en 2026-08-05 — aucun
candidat n'a atteint ce stade) :

```sh
git clone <repo-url> && cd <repo-dir>
cat LICENSE | head -5                        # MIT obligatoire
go build ./... && go test ./... && go vet ./...
test -z "$(gofmt -l .)"
find . -name "*.go" | wc -l                  # petitesse
find . -name "*.go" -exec wc -l {} + | tail -1
grep -r "gorilla\|gorm\|echo\|gin\|chi\|sqlx\|zap\|logrus\|observ\|auth" go.mod 2>/dev/null \
  || echo "No auxiliary stack detected"
```

La vérification finale comprend aussi : scénario observable exécuté
(PASS/PARTIAL/BLOCKED documenté), ATTRIBUTION.md (source, version épinglée,
adaptations, périmètre technique), template.yaml, README.md avec justification
de structure (D-2026-08-05-13).
