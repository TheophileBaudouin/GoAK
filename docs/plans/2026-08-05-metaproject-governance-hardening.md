# Plan — Durcissement gouvernance méta-projet (fermeture de 5 findings Rodin)

## Goal

Fermer les 5 findings identifiés par la critique auto-adversariale « Rodin »
(duplication inter-fichiers non déclenchée, roadmap snippets prématurée,
contradiction de philosophie Go, desktop-app sans template sourcé, instructions
MANDATORY sans porte mécanique) **sans toucher à `KitV2/`** : contrats de
gouvernance, `.pi/prompts/kit-audit.md`, `.agent/instructions.md`, décisions et
recherches méta-projet seulement. La passe de correction produit (Marie,
`.pi/prompts/kit-audit` puis corrections) suivra ; cette passe prépare ses
actions en attente, écrites et prêtes, sans les appliquer.

## Context

- Critique Rodin vérifiée contre l'arbre réel avant rédaction (lecture des
  fichiers cités, pas de confiance aveugle) — deux nuances de calibration
  confirmées comme faits :
  1. **Chantier A** : C2 §2 (02-validation-gate.md, bloc « Fraîcheur »)
     déclare déjà « La duplication sémantique reste une revue humaine ». Le
     problème est un **défaut de déclenchement** de cette revue entre deux
     audits, pas une absence de conscience du risque.
  2. **Chantier B** : `KitV2/snippets/` contient exactement 3 snippets réels
     (bounded-worker, errors-once, http-json) ; les 7 lignes roadmap ne sont
     qu'une table Markdown du README, mandatée par 13-zone-snippets.md §3 règle
     3 et 00-charte-d-application.md §7, même patron que templates/TEMPLATES.md.
- Points de couplage vérifiés directement (pas de scout dédié : la recon
  directe des fichiers cités couvre le besoin de « localiser les points de
  couplage réels avant de conclure ») :
  - `KitV2/tools/validators/validate-kitv2.py` `check_internal_duplicates`
    (l.203) : comparaison de paragraphes **intra-fichier** uniquement ;
    docstring : « leaving semantic review to humans ».
  - SNIPPET.yaml déclarent tous une `source:` résolue (bounded-worker →
    `recipes/recipe-worker-pool/SKILL.md`, errors-once →
    `rules/core/errors/SKILL.md`, http-json →
    `recipes/recipe-rest-chi/SKILL.md`) — chaîne de pointeurs
    pattern/recette/règle → snippet vérifiable mécaniquement.
  - SNIPPET.yaml ne porte pas de `last_verified` (champ absent du modèle
    `bounded-worker`) → la règle inter-fichiers doit ajouter ce champ (Z4 §3)
    pour être vérifiable par date.
  - `recipe-desktop-app/SKILL.md` (Wails v3, rejette Tauri « Rust, hors
    périmètre d'un kit Go ») + `probes/desktop-app/main.go` existent ;
    `templates/TEMPLATES.md` ne liste desktop-app nulle part (roadmap =
    grpc, microservice, monolith, cloud-service seulement).
  - `.pi/skills/kit-resource-routing/SKILL.md` dit « MANDATORY before
    planning or implementing » pour `search_kit_resources` ; aucun mécanisme
    ne l'applique. Doc Pi `docs/extensions.md` (vérifiée) : l'événement
    `tool_call` **peut bloquer** (`{ block: true, reason }`),
    `pi.setActiveTools()` active/désactive des outils, `before_agent_start`
    injecte des messages, `pi.appendEntry()` persiste l'état de session →
    une porte mécanique est réellement concevable.
- Recherche Web-Research (chantier D) terminée : **aucun candidat Wails ne
  qualifie** la politique Z5 §2 (Wails v3 en beta v3.0.0-beta.3, écosystème
  trop jeune ; v2 stable mais aucun projet réel MIT mono-techno testé trouvé ;
  `wailsapp/examples` = démos, exclus). Rapport :
  `docs/research/2026-08-05-desktop-app-template-candidates.md`.

## Constraints

- **Périmètre méta-projet strict** : `KIT_CHARTER.md` (lecture prioritaire,
  non modifié), `AGENTS.md` racine (non modifié sauf décision Marie sur C),
  `.agent/` (contrats, instructions, validators, cognitive), `.pi/memory/`,
  `.pi/prompts/kit-audit.md`, `docs/`. **Aucune édition sous `KitV2/`** —
  toute correction produit est loggée comme finding ou écrite dans ce plan
  comme action en attente pour la passe suivante. Ne jamais élargir la
  frontière (AGENTS.md Modification policy).
- Un seul writer sur le worktree ; la seule exécution parallèle est la
  recherche en lecture (Web-Research chantier D, terminée).
- Toute règle nouvelle d'un contrat doit être formulée pour être vérifiable
  par C2 ou un contrôle de revue (README.md kit-governance) — sinon c'est une
  hypothèse.
- Pas de code dans `KitV2/tools/validators/validate-kitv2.py` : le contrat
  exact des nouveaux contrôles est écrit dans ce plan (§ Annexes A/B/C), prêt
  pour la passe d'implémentation.
- Confiance documentée : une hypothèse non vérifiée n'est jamais une
  affirmation ferme dans le rapport final.
- Trois échecs identiques d'affilée → stop et rapport.
- Gates méta-projet après éditions : `python3 .agent/validators/
  validate-instructions.py` + `python3 .agent/validators/
  validate-cognitive.py` depuis la racine (pas de gate produit : aucun code
  KitV2 modifié).

## Done when

- Plan écrit (ce fichier) avant toute édition ✓.
- Chantier A : options a/b/c évaluées, décision prise, contrats C2/Z3/Z4/Z1
  mis à jour avec la règle vérifiable, kit-audit phase C4 + §4-E évolués,
  contrat du contrôle futur écrit (annexe A), aucun code KitV2 écrit.
- Chantier B : comparaison 13-zone-snippets vs 14-zone-templates faite,
  verdict fondé sur la preuve, Decision Record enregistré (aucun travail
  fabriqué).
- Chantier C : `docs/research/2026-08-05-philosophy-tension.md` rédigé avec
  ≥ 3 options, question posée à Marie (bloquant : rien d'autre sur C avant
  réponse) ; application après réponse (méta-projet → appliquer ; core →
  action en attente).
- Chantier D : dossier `docs/research/2026-08-05-desktop-app-template-
  candidates.md` (aucun candidat conforme, honnête) ; précision Z5 §2 (source
  réelle ≠ starter/démo) appliquée ; ligne roadmap TEMPLATES.md rédigée dans
  le plan (non appliquée) ; kit-audit phase B évolué.
- Chantier E : capacité réelle Pi documentée (porte mécanique existe), spec
  exacte du mécanisme écrite dans le plan (annexe B), principe étendu dans
  `.agent/instructions.md` (registre des lacunes d'automatisation), C2 + Z8
  mis à jour, kit-audit dimension « instructions absolues » nommée.
- Gates méta-projet vertes ; revue fresh-context obtenue avant déclaration de
  fin ; Decisions.md (D-2026-08-05-11…15), Progress.md, Gotchas.md (si leçon
  durable) mis à jour ; rapport final avec fichiers KitV2 non touchés.

## Étapes

1. (fait) Vérification des preuves contre l'arbre réel + recon des points de
   couplage.
2. (fait) Recherche Web-Research chantier D (subagent fresh-context,
   read-only).
3. Rédaction de ce plan + note philosophie
   (`docs/research/2026-08-05-philosophy-tension.md`) + dossier desktop-app
   (`docs/research/2026-08-05-desktop-app-template-candidates.md`).
4. Question à Marie (chantier C) — ne pas avancer sur C avant réponse.
5. Chantier A : décision D-2026-08-05-11 ; édits C2 §2 (règle inter-fichiers
   - tripwire + instructions absolues), Z4 §3/§5, Z3 §5, Z1 §6 ; kit-audit
   C4/§4-E.
6. Chantier B : décision D-2026-08-05-12 (verdict : sain, sans édition
   contractuelle).
7. Chantier D : décision D-2026-08-05-14 ; précision Z5 §2 ; kit-audit phase
   B ; ligne roadmap prête dans le plan (non appliquée).
8. Chantier E : décision D-2026-08-05-15 ; `.agent/instructions.md` (principe
   - registre) ; C2 §2 + Z8 §3 ; kit-audit dimension nommée.
9. Chantier C post-réponse (si Marie répond pendant la passe) : appliquer si
   méta-projet seulement ; sinon action en attente.
10. Gates méta-projet : `validate-instructions.py`, `validate-cognitive.py`.
11. Revue fresh-context (subagent read-only, C0 §6.3) — intégrer ou trancher
    les remarques.
12. Mémoire (Decisions.md D-2026-08-05-11…15, Progress.md, Gotchas.md si
    nécessaire) + commit + rapport final.

## Décisions de la passe (résumé, détails dans Decisions.md)

- **A (D-2026-08-05-11)** : combiner (b) mécanisée + (a) tripwire. Règle
  vérifiable : dépendant déclaré re-vérifié quand le canonique change
  (`last_verified(dépendant) >= last_verified(canonique)`, contrôlable par
  date pour snippet `source:` et relations YAML-graphe) ; tripwire de
  similarité exemple.go ↔ bloc canonique en warning (jamais erreur, vue
  focalisée ≠ copie). Statu quo (c) seul écarté : n'ajoute aucun déclencheur.
- **B (D-2026-08-05-12)** : le design roadmap snippets est sain — les 7 lignes
  portent chacune un critère d'admission actionnable, plus précis par ligne
  que le statut `planned` des templates (« décision + ligne »), et le patron
  est mandaté par Z4 §3 + C0 §7 ; aucun changement de contrat. Fermeture sans
  travail fabriqué.
- **C (D-2026-08-05-13)** : tension documentée honnêtement (2 niveaux :
  AGENTS.md racine « Go does not prescribe a universal project tree » +
  rules/core/philosophy « no universal project layout » vs objectif personnel
  de navigation identique partout) ; 3 options posées ; **réponse Marie
  (2026-08-05) : Option 3 « naviguer par la raison »** — liberté de structure
  conservée, mais toute recette qui produit/recommande une disposition doit
  l'expliquer par écrit au même endroit (section « Structure » de la recette,
  justification dans le README template). Aucune modification d'AGENTS.md
  racine ni de rules/core/philosophy nécessaire (l'Option 3 est compatible
  avec la doctrine sourcée) ; éditions des recettes/templates = passe
  suivante (KitV2).
- **D (D-2026-08-05-14)** : aucun candidat Wails conforme (v3 beta,
  écosystème immature) ; précision Z5 §2 « source = application réelle, pas
  starter/démo » (leçon transférable) ; ligne roadmap desktop-app = planned
  avec note « aucune source conforme au 2026-08-05, ré-évaluer à la GA » ;
  admission = passe suivante (KitV2).
- **E (D-2026-08-05-15)** : Pi expose une vraie porte mécanique (`tool_call`
  block, `setActiveTools`) — spec exacte d'une extension « reminder doux »
  écrite (annexe B, implémentation passe suivante dans KitV2/.pi/) ; principe
  étendu aux artefacts consommateurs (MANDATORY ⇒ contrôle mécanique OU
  étiquette « guidance seule » dans le registre des lacunes
  d'automatisation) ; pas de scan validateur dur (risque de faux positifs sur
  des absolus légitimement appliqués par revue — documenté).

## Actions en attente pour la passe suivante (KitV2/ — ne PAS appliquer ici)

1. **Contrôle C2 « dérive inter-fichiers »** (validate-kitv2.py) : spec
   complète en Annexe A — champ SNIPPET.yaml `last_verified` (recommandé),
   comparaison de dates snippet↔source:, relation YAML-graphe
   dépendant↔cible, tripwire de similarité (warning), tests +/−.
2. **Porte Pi « search_kit_resources »** (KitV2/.pi/extensions/) : spec
   complète en Annexe B — état de session, reminder doux sur `tool_call` des
   outils d'écriture, dégradation sans UI, option hard-block.
3. **TEMPLATES.md** : ajouter la ligne roadmap desktop-app (texte prêt en
   Annexe D), statut `planned`, note « aucune source MIT conforme au
   2026-08-05 (Wails v3 beta) — ré-évaluer à la GA ».
4. **Alignement SNIPPET.yaml existants** : ajouter `last_verified` aux 3
   snippets quand le contrôle sera implémenté.
5. **Option 3 (D-2026-08-05-13) — KitV2** : ajouter la section « Structure
   (pourquoi cette disposition) » aux recettes concernées par une disposition
   de projet (création d'application/service/CLI/worker/desktop) et la
   justification de structure au README des 3 templates sourcés (format Z5
   §3).
6. **C2 contrôle « instructions absolues »** (si décidé à l'implémentation) :
   grepper MANDATORY/absolus dans les artefacts consommateurs et vérifier
   contrôle ou étiquette — spec en Annexe C.

## Annexes

### Annexe A — Contrat du contrôle C2 « dérive inter-fichiers » (à implémenter passe suivante)

- **Entrées** : `snippets/*/SNIPPET.yaml` (champ `source:` résolu),
  `snippets/*/example.go`, `snippets/*/check.sh`, SKILL.md cibles,
  `knowledge/**/*.yaml` (relations `references`/`uses`/`depends_on` vers des
  artefacts datés).
- **Règle pass/fail** :
  - Snippet : si SNIPPET.yaml porte `last_verified` ET la cible `source:`
    porte `last-verified` (frontmatter SKILL.md), alors
    `last_verified(snippet) >= last_verified(cible)` — sinon **erreur**
    (« snippet non re-vérifié après modification de sa source canonique »).
  - YAML-graphe : pour toute relation vers une cible datée, `last_verified`
    du dépendant >= celui de la cible — sinon **erreur**.
  - Tripwire (warning, jamais erreur) : similarité de tokens
    (Jaccard/containment normalisé, commentaires ignorés) entre
    `example.go` et le bloc de code Go de la cible `source:` ; sous un seuil
    calibré sur les 3 snippets existants → `warning: « drift suspect … »`.
- **Faux positifs connus** : vue focalisée légitime d'un snippet (≠ copie) —
  d'où warning et non erreur ; dates manquantes → contrôle ignoré (pas de
  failure) ; cibles sans bloc Go → tripwire N/A.
- **Tests** : + snippet ré-verifié (dates OK) ; − snippet obsolète (date
  inférieure) ; − relation graphe obsolète ; +/− tripwire au seuil calibré.

### Annexe B — Contrat de la porte Pi « search_kit_resources » (à implémenter passe suivante)

- **Mécanisme** : extension Pi dans `KitV2/.pi/extensions/` (fusionnée dans
  kit-resource-router.ts ou fichier séparé) — état de session `searched`
  (reset sur `session_start`, set sur `tool_call` de `search_kit_resources`),
  hook `tool_call` sur les outils d'écriture (write/edit/apply_patch/bash) :
  si `searched == false` et l'input ressemble à du travail technique
  (extensions .go/.mod, commandes `go build|test|run|mod`, chemins sous
  rules/recipes/knowledge/snippets/templates), injecter un rappel doux dans
  `tool_result` (« kit-resource-routing : search_kit_resources n'a pas été
  appelé cette session avant cette édition technique — le faire d'abord sauf
  si travail non technique »).
- **Dégradation** : mode sans UI (print/rpc) → rappel seulement (jamais de
  confirm bloquant) ; `hard-block` optionnel par configuration (block +
  reason) réservé aux sessions TUI, avec exemption explicite du cas « travail
  non technique » (la skill elle-même l'exclut).
- **Niveau de confiance honnête** : présence-session ≠ preuve que la *bonne*
  recherche a précédé *cette* édition → la porte est un tripwire de rappel,
  pas une preuve de conformité ; l'audit (dimension instructions absolues)
  reste le juge.
- **Tests** : smoke pi depuis une copie consommateur (rappel déclenché, pas de
  rappel après search, pas de rappel sur édition non technique).

### Annexe C — Contrat du contrôle « instructions absolues » (optionnel, passe suivante)

- Grep déterministe des lexèmes MANDATORY / « must always » / « jamais » /
  « toujours » dans les artefacts consommateurs (AGENTS.md, skills, prompts,
  recipes) ; chaque occurrence doit être rattachée à un contrôle mécanique
  nommé OU à une étiquette « guidance seule » dans le registre
  d'.agent/instructions.md. Statut initial : warning (le registre existe),
  passer en erreur quand le registre est complet.

### Annexe D — Ligne roadmap TEMPLATES.md (texte prêt à coller, passe suivante)

```markdown
| desktop-app | planned | — (aucune source MIT conforme au 2026-08-05 : Wails v3 en beta, écosystème immature ; exemples officiels = démos) | Wails v3 — ré-évaluer à la GA (recherche 2026-08-05) |
```

(à insérer dans la table « Statut actuel » de `KitV2/templates/TEMPLATES.md`,
et la phrase du catalogue : « Les shapes grpc, microservice, monolith,
cloud-service **et desktop-app** restent une roadmap sans template
opérationnel. »)
