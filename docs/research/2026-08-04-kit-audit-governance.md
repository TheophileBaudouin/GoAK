# Audit de gouvernance du Kit Go pour agents — phase 1 (audit seul)

- **Date :** 2026-08-04
- **Portée :** audit complet de `KitV2/` (le Kit, produit consommable) — pas du metaprojet.
- **Objet de la mission :** définir les standards d'évolution du Kit. Ce document est un
  livrable du **MetaProjet** (racine du dépôt). Aucune des recommandations n'est écrite
  directement dans le Kit ; elles deviendront, en phase 2, les contrats de construction
  (fichiers d'instructions MetaProjet).
- **Statut :** AUDIT — aucune modification du Kit effectuée.

---

## 0. Méthode et sources

### 0.1 Méthode

1. **Cartographie terrain** : arborescence complète de `KitV2/` (fichier par fichier),
   lecture intégrale des artefacts d'autorité (`KIT_CHARTER.md`, `manifest.yaml`,
   `capabilities.yaml`, `AGENTS.md` produit, `validate-kitv2.py`, contrats de
   templates/snippets/probes, extraits représentatifs de chaque zone).
2. **Mesure de l'écart** : comptage réel vs comptes déclarés ; formats concurrents
   (YAML-graphe vs SKILL.md) ; placeholders `.gitkeep` ; index obsolètes.
3. **Recherche externe** : standards ouverts et pratiques de gouvernance des grands kits
   d'agents open source (voir 0.2), sources croisées et vérifiées à l'exception des
   références secondaires signalées.
4. **Synthèse** : pour chaque dossier, rôle actuel / problèmes / rôle recommandé /
   contenu attendu / contenu interdit / règles de maintenance / patterns / anti-patterns /
   questions ouvertes.

### 0.2 Sources consultées (vérifiées — liens actifs au 2026-08-04)

#### Standards de format (autorité de format)

| Source | Rôle pour l'audit |
| --- | --- |
| [Agent Skills Specification](https://agentskills.io/specification) — spec ouverte, adoptée par Anthropic/OpenAI/Pi/Gemini/Copilot | Définit `SKILL.md`, frontmatter (`name` ≤64, `description` ≤1024, `license`, `compatibility`, `metadata`, `allowed-tools`, `disable-model-invocation`), arborescence skill (`SKILL.md`, `scripts/`, `references/`, `assets/`), **progressive disclosure à 3 niveaux** (L1 frontmatter toujours chargé → L2 corps chargé à la demande → L3 fichiers liés). Le Kit l'implémente déjà (Pi : `docs/skills.md` local). |
| [Skill authoring best practices — Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) | « La fenêtre de contexte est un bien public ». Métadonnées = seul coût permanent. L1 = goulot de découvrabilité : décrire ce que fait la skill + quand la charger. Corps L2 : garder sous ~500 lignes, dépassé → split en fichiers L3. |
| [Agent Skills — Codex (OpenAI)](https://developers.openai.com/codex/skills) | Confirme la convergence inter-harnais du standard. |
| [Pi — docs/skills.md](https://github.com/earendil/pi) (doc locale lue) | Pi implémente la spec, **validation tolérante** (warnings), **description manquante = skill non chargée**, champs frontmatter inconnus ignorés → les extensions du Kit (`category`, `tags`, `last-verified`) sont sûres. |

#### Gouvernance à l'échelle (autorité de processus)

| Source | Leçons extraites |
| --- | --- |
| [Behind the scenes: how we build, test, and scale Google Agent Skills](https://dev.to/googleai/behind-the-scenes-how-we-build-test-and-scale-google-agent-skills-1am5) | Layout skill standardisé (`SKILL.md`, `OWNERS`, `EVAL.yaml`, `reference/`, `scripts/`, `assets/`, `_internal/`). **CI sur chaque contribution** : linters (frontmatter, nb lignes, layout, nommage), vérificateurs de liens (lychee), checklists assistées IA. **Évals continues** (à la soumission + hebdo) : prompts d'éval + rubriques fournies par l'auteur ; comparaison avec/sans la skill ; dimensions précision × efficacité (tokens). **« Skills are products, not snippets »** : propriétaire de skill responsable de la maintenance long terme. |
| [Building skills for AI agents: pitfalls and best practices — Red Hat ACE](https://next.redhat.com/2026/07/28/building-skills-for-ai-agents-pitfalls-and-best-practices/) | **Capability vs preference skills** (éphémères vs durables — les skills qui patchaient un gap de modèle dépérissent quand le modèle s'améliore ; les skills de processus durent). **Hybride script/LLM** : scripts pour le mécanique, LLM pour le subjectif (−26 % coût). **Granularité 1–3 skills par tâche** ; skills trop larges dégradent ; skills hors-sujet **égarent activement** l'agent. Nommage par domaine, contraintes négatives dans la description L1 (« ne PAS utiliser pour X »), router skill. L2 < 500 lignes ; **L3 non-gated = plus grand puits de tokens**. Éval sur 3 piliers : viabilité fonctionnelle, conformité directive, efficacité opérationnelle ; dataset d'éval = actif précieux ; CI de régression avec qualité-gates. Traiter les skills comme des artefacts logiciels (versioning, PR, rollback, sécurité). |
| [Equipping agents for the real world with Agent Skills — Anthropic](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | Fondations du standard ; charge de contexte différentielle ; exemples de structure. |
| [Effective context engineering for AI agents — Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | Contexte = ressource limitée à curer ; tout token ajouté a un coût d'opportunité. |
| [Contributing — Superpowers (obra)](https://obra-superpowers.mintlify.app/development/contributing) | **TDD appliqué à la documentation de processus** : écrire des scénarios de pression (subagents), constater l'échec (baseline), écrire la skill, constater la conformité, refactorer. Kit communautaire éditable, PR requises, repo de skills séparé du plugin. |
| [Building skills for AI agents / kkrlstrm knowledge-graph-governance](https://github.com/kkrlstrm/knowledge-graph-governance) | **Write-gate déterministe** pour graphe de connaissances géré par agents : l'agent propose, seules les écritures validées (versionnées, avec provenance) atteignent le graphe. |

#### Cycle de vie / versioning des artefacts

| Source | Leçons extraites |
| --- | --- |
| [Prompt lifecycle governance — COMPEL](https://www.compelframework.org/articles/prompt-lifecycle-governance) ; [Prompt library governance](https://hiro.solutions/prompting-at-scale-building-a-prompt-library-and-governance-) ; [AWS prescriptive guidance — prompt/agent/model lifecycle](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-serverless/prompt-agent-and-model.html) | Traiter prompt/skill/artefact comme du code : registre versionné, changement = revue + validation, rollout/rollback, retrait propre. |
| [SemVer for agent skills — discussion agentskills #415](https://github.com/agentskills/agentskills/discussions/415) ; [Versioning agent skills: SemVer, compatibility, deprecation](https://aiquinta.ai/blog/versioning-agent-skills-semver-compatibility-deprecation/) | SemVer appliqué aux skills : major = rupture de contrat de sortie, minor = ajout, patch = reformulation. Politique de dépréciation explicite (échéance, migration, retrait). |
| [LLM knowledge base for coding agents — Verdent](https://www.verdent.ai/guides/llm-knowledge-base-coding-agents) | Pipeline raw/ → wiki structuré avec index et backlinks, « compilé » par un LLM — l'index n'est pas un artefact manuel. |

**Note de fiabilité :** les posts d'ingénierie de Google/Red Hat/Anthropic sont des sources
primaires de processus vécus ; les citations arXiv internes (2602.12670, 2603.29919,
2604.04323) citées par Red Hat n'ont pas été vérifiées individuellement — les seuils
chiffrés (500 lignes, 1–3 skills) sont corroborés par la doc officielle Claude pour le
premier. Le registre des sources du metaprojet (`.agent/sources/Go-dev-kit-sources-et-references.md`)
ne couvre pas encore ces sources « gouvernance de kit d'agents » : leur ajout est une
action de phase 2 (jamais au-dessus de `KIT_CHARTER.md` ni des règles du Kit).

---

## 1. Vision globale du Kit

### 1.1 Objectif architectural actuel

`KIT_CHARTER.md` (autorité de processus) définit le Kit comme un **système cognitif
d'exploitation pour agents de code**, organisé en **graphe de connaissances typé**
(10 kinds d'artefacts, 9 relations, métadonnées obligatoires, single source of truth,
évidence avant inclusion, composition plutôt que duplication, validation observable).

Le produit physique `KitV2/` matérialise 8 zones :

| Zone | Contenu mesuré | État |
| --- | --- | --- |
| `rules/` | 10 SKILL.md (core : philosophy, concurrency, errors, universal, validation/* ; registry : doc-comments, logging, testing) | Riche, gouverné |
| `knowledge/` | 137 YAML-graphe + 25 SKILL.md + INDEX (patterns 38, anti-patterns 47, stdlib 20, catalogs ~31, security/performance/observability/architecture) | Riche mais formats mixtes |
| `recipes/` | 10 SKILL.md runnables (+ code + tests) + 6 dossiers placeholder `.gitkeep` | Semi-rempli, placeholders non contractés |
| `snippets/` | 3 vrais snippets (SNIPPET.yaml + example.go + check.sh) + 7 dossiers placeholder | Quasi vide, taxonomie non contractée |
| `templates/` | 7 squelettes runnables marqués PARTIAL + 1 placeholder (api-service) | Contrat de promotion existant, non automatisé |
| `probes/` | 5 probes exécutables + run.sh + README | Fonctionnel, liste codée en dur |
| `tools/` | `offline/` (résolveur + bundle épinglé), `validators/` (validate-kitv2.py) ; `analyzers/`, `generators/` vides | Validateur = seul point d'application des règles |
| `.pi/` | settings.json, 8 prompts de workflow, 5 skills de workflow (.pi/skills) | Deuxième écosystème de skills non gouverné |
| racine | `manifest.yaml`, `capabilities.yaml`, `AGENTS.md`, `embeddings/` (héritage vide) | Deux manifests redondants, comptes dérivés |

### 1.2 Forces du Kit (à préserver et formaliser)

1. **La charte est le bon cadre.** Graphe typé, évidence d'abord, composition, single
   source of truth, validation observable : ces principes sont exactement ceux que la
   recherche externe confirme (write-gate, skills-as-products, évals). Le problème n'est
   pas la vision, c'est l'**écart entre la charte et son application opérationnelle**.
2. **Le format SKILL.md produit est aligné sur le standard ouvert** (agentskills.io) avec
   des extensions kit (`category`, `tags`, `last-verified`) sûres car ignorées par Pi.
3. **Le scénario observable est déjà dans les recettes** (« Verify the behavior ») — c'est
   le concept d'éval le plus coûteux à introduire ailleurs ; il est là, il faut le
   généraliser et le rendre obligatoire.
4. **La séparation probes ↔ recipes ↔ offline est saine** : les probes importent les
   recettes et prouvent qu'elles composent ; le bundle offline prouve la résolution
   déterministe hors-ligne.
5. **Le validateur existe et tourne** — il faut l'élever de « vérificateur de structure »
   à « portail de gouvernance ».

### 1.3 Problèmes systémiques (causes racines de la dérive)

1. **Aucun contrat de dossier.** Aucun dossier ne possède de document MetaProjet définissant
   mission, format, règles, patterns/anti-patterns, critères de validation. La connaissance
   de ces règles est dispersée dans la charte, `_kit-skill-authoring.md` (auto-décrit comme
   « working document »), les READMEs et le validateur. Un agent ne peut pas « lire les
   instructions d'un dossier avant d'y travailler » — c'est l'exigence centrale du mandat.
2. **Deux manifests qui dérivent.** `manifest.yaml` (canonical paths) et `capabilities.yaml`
   (source/status/coverage) décrivent le même mapping avec des comptes **codés en dur et
   faux** : `capabilities.yaml` annonce `product_skills: 33`, le validateur exige 45 ;
   `knowledge_catalogs: 13` ne correspond à rien de mesurable tel quel.
3. **Deux formats pour le même concept.** Les bibliothèques de `knowledge/catalogs/libraries/`
   sont pour moitié des artefacts YAML-graphe (`gin.yaml`, `fiber.yaml`…), pour moitié des
   SKILL.md (`chi/`, `cobra/`, `sqlc/`…). Rien ne documente quand quel format s'applique ;
   le validateur ne peut pas distinguer les deux populations.
4. **Placeholders sans contrat.** 6 recettes, 7 catégories de snippets, `analyzers/`,
   `generators/`, `api-service` : des dossiers `.gitkeep` qui promettent un contenu sans
   dire ce qui y entrera ni quand. C'est le terreau exact de la dérive : un agent voit un
   dossier vide, il l'utilise, personne ne l'empêche.
5. **Index et comptes manuels.** `knowledge/INDEX.md` référence un domaine `cloud/` qui
   n'existe pas ; les comptes de capabilities sont manuels. Tout index maintenu à la main
   finit faux — il doit être **généré**.
6. **Le validateur vérifie la forme, pas le contrat.** Il ne contrôle pas : cohérence
   manifest↔capabilities, fraîcheur des `last_verified`, qualité des descriptions
   (activation explicite « Use when »), présence d'un scénario observable dans les recettes,
   cohérence probes/run.sh↔probes/, validité des liens, sync INDEX.
7. **Deux écosystèmes de skills non délimités.** `.pi/skills/` (5 skills de workflow) cohabitent
   avec les SKILL.md de `rules/`, `recipes/`, `knowledge/catalogs/` (45 modules). Aucun
   contrat ne dit ce qu'est une « skill de workflow » vs un « module de connaissance »,
   où chacun vit, et comment éviter la duplication entre `.pi/prompts/`, `.pi/skills/` et
   les modules.
8. **Héritage mort.** `embeddings/vector-index/.gitkeep` (recherche vectorielle abandonnée)
   est présent sans note de décision — la décision de rejet doit vivre dans une Decision
   Record, pas dans un dossier fantôme.

### 1.4 Ce que disent les références modernes (synthèse applicable)

| Principe externe | Traduction pour le Kit |
| --- | --- |
| Progressive disclosure L1/L2/L3 (spec agentskills, Anthropic, Red Hat) | Déjà partiellement en place. Le rendre **règle écrite** : description L1 = goulot de découvrabilité (quoi + quand + contraintes négatives), corps L2 ≤ 500 lignes, L3 = fichiers référencés, rien d'autre. |
| « Skills are products, not snippets » (Google) | Chaque module a un propriétaire, une date de vérification, un processus de mise à jour, et une éval qui prouve qu'il marche. C'est déjà l'esprit de la charte ; il manque l'opérationnalisation (owner par fichier, échéance `last_verified`, scénario exigé par catégorie). |
| Évals avec/sans + précision × efficacité (Google) ; 3 piliers (Red Hat) | Le Kit a déjà `probes/` (évals produit) et le scénario observable des recettes. Élargir : **chaque catégorie d'artefact définit son éval minimale** (recette = scénario exécuté ; bibliothèque = admission + compile minimale ; règle = contre-exemple + vérification ; template = promotion check ; snippet = check.sh). |
| Capability vs preference (Red Hat) | Distinguer dans les contrats les contenus **durables** (processus, conventions — patterns, règles, recettes de forme) des contenus **sensibles au modèle** (astuces de prompting) et prévoir leur dépréciation. |
| Granularité 1–3 skills par tâche, descriptions à contraintes négatives, nommage par domaine | Règle de nommage et de scopage pour les modules ; description = « quoi + quand + ne PAS utiliser pour ». |
| Write-gate déterministe (kkrlstrm) | C'est déjà le cycle de vie de la charte (Problem→Research→Decision→Pattern→Snippet→Recipe→Template→Evaluation). L'opérationnaliser : **proposé ≠ actif**, validateur qui rejette les relations vers du `proposed`/inexistant, évidence obligatoire à l'admission. |
| SemVer + dépréciation (agentskills #415, aiquinta) | Formaliser la sémantique de `version:` (major = rupture de contrat de sortie) et la politique de retrait (charte §12 le dit, rien ne l'applique). |
| Index généré, pas tenu à la main (Verdent) | Remplacer les index/comptes manuels par un générateur déterministe (candidat pour `tools/generators/`). |
| CI sur contribution (Google : linters, liens, checklists) | Étendre `validate-kitv2.py` et le workflow CI existant (`.github/workflows/ci.yml`) : liens, frontmatter, fraîcheur, cohérence des comptes, scénarios. |

---

## 2. Audit dossier par dossier

Pour chaque dossier : responsabilité actuelle, problèmes observés, responsabilité
recommandée, contenu attendu/interdit, règles de maintenance, patterns, anti-patterns,
questions ouvertes.

---

### 2.1 `rules/`

#### Responsabilité actuelle

Contraintes permanentes chargées par Pi via `.pi/settings.json` (`"../rules"`). Deux
sous-zones : `core/` (philosophy, concurrency, errors, universal, validation/golangci-lint,
gosec, govulncheck) et `registry/` (doc-comments, logging, testing). 10 SKILL.md. La
distinction core/registry n'est documentée que dans `templates/_kit-skill-authoring.md`
(« core = principe universel chargé à chaque session ; registry = règles de domaine »).

#### Problèmes observés

1. **La distinction core/registry est implicite.** Aucun fichier ne dit ce qui doit être
   dans `core/` (coût permanent de session → budget de compacité) vs `registry/` (chargé à
   la demande). Sans contrat, un contributeur mettra n'importe quelle règle dans `core/` —
   et le budget permanent explose (contrainte de la charte déjà violée par croissance).
2. **Anomalie de nommage** : `rules/core/rules/universal/SKILL.md` — imbrication
   `rules/core/rules/...` héritée, confuse.
3. Les règles `core/` sont des SKILL.md (Pi), les patterns/anti-patterns associés sont des
   YAML-graphe dans `knowledge/` — la **relation règle ↔ pattern n'est pas tracée** par le
   validateur (seuls les YAML le sont ; les références croisées dans les SKILL.md ne sont
   pas vérifiées).

#### Responsabilité recommandée

`rules/` = **la couche « doit toujours être vrai » du Kit**, au sens de la charte (Layer 1).
`core/` = règles universelles à coût permanent maîtrisé (budget explicite, ex. ≤ 4–6 modules,
chacun < 300 lignes, jamais de contenu de domaine). `registry/` = règles de domaine chargées
à la demande (par catégorie : testing, logging, doc-comments…), avec une règle de frontière :
**aucune règle registry ne peut être référencée par une règle core** (les universelles ne
dépendent pas du chargé-à-la-demande).

#### Contenu attendu

- `core/philosophy` (existe), `core/concurrency`, `core/errors`, `core/validation/*`
  (existent) : chaque règle = impératif + frontière d'application + contre-exemples +
  vérification + sources (déjà le cas pour les bons exemples : `testing`, `philosophy`).
- Un SKILL.md « méta » dans `core/` exposant le budget de compacité et la règle
  core↔registry (ou un README de zone).
- Rien d'autre. Les règles ne contiennent **jamais** de code d'implémentation (charte §3).

#### Contenu interdit

- Règles de domaine dans `core/` ; code de production ; duplication de contenu de
  `recipes/` ou `knowledge/` ; références directes à `registry/` depuis `core/` ;
  placeholders `.md` vides (régression déjà corrigée — voir Gotchas 2026-08-04).

#### Règles de maintenance

- Ajout d'une règle core : **nécessite une décision** (coût permanent) ; l'admission passe
  par un Decision Record + réévaluation du budget total.
- Ajout d'une règle registry : admission si source primaire + frontière d'application
  explicite + vérification actionnable ; vérifier l'absence de conflit avec les règles
  existantes (contradiction = échec d'admission).
- Modifier une règle : bump `last-verified`, `version` (semver : major si la règle devient
  plus stricte), vérifier les artefacts qui la référencent.

#### Patterns recommandés

- Une règle = un impératif vérifiable + un périmètre « ne couvre PAS » (cf. le bon exemple
  `rules/registry/testing`).
- Les règles core sont les seules à pouvoir citer d'autres règles core (graphe explicite).

#### Anti-patterns

- Règle vague (« use idiomatic Go ») ; règle sans source ; règle sans frontière ; ajout
  « just this once » dans core ; duplication d'un pattern de `knowledge/` dans une règle.

#### Questions ouvertes

- Renommer `rules/core/rules/universal` → `rules/core/universal` (avec migration) ?
- Faut-il une règle core « budget de session » chiffré (nb de modules core × lignes max) ?

---

### 2.2 `knowledge/`

#### Responsabilité actuelle

Couche d'explication et de routage. `INDEX.md` et `README.md` la décrivent : stdlib
(routage pointer-only), architecture, patterns, anti-patterns, debugging, performance,
security, cloud, catalogs. Réalité mesurée : patterns 38 YAML, anti-patterns 47 YAML,
stdlib 20 YAML pointer-only, security 2, performance 1, observability 1, architecture 1,
debugging **vide**, catalogs (libraries ~31 entrées, reference-projects 3, discovery 6),
`INDEX.md` obsolète (ligne `cloud/` fantôme).

#### Problèmes observés

1. **Deux formats pour les catalogues de bibliothèques** : YAML-graphe Source (`gin.yaml`,
   `echo.yaml`, `fiber.yaml`, `gorm.yaml`, …) vs SKILL.md modules (`chi/`, `cobra/`,
   `sqlc/`, `testify/`, …). Les premiers sont des pointeurs fins « à considérer », les
   seconds des décisions vétées avec admission 9 critères. La distinction est probablement
   **intentionnelle** (pointeur vs module) mais **indocumentée et non vérifiée**.
2. `knowledge/INDEX.md` référence `cloud/` qui n'existe pas ; les comptes ne sont nulle part
   (le validateur compte les YAML mais pas par domaine).
3. **Debugging est vide** (`.gitkeep`) ; performance/observability/architecture ont 1 seul
   artefact : la taxonomie promet plus que le contenu.
4. Les patterns/anti-patterns YAML sont **excellents** (id stables, problem/context/solution,
   homologues négatifs référencés, sources) — c'est le modèle à généraliser, mais le
   validateur ne vérifie ni la présence des sections obligatoires du schéma
   (symptom/detect/problem/fix/when_ok pour les anti-patterns), ni la résolution des
   références d'homologues, ni la fraîcheur.

#### Responsabilité recommandée

`knowledge/` = **graphe de décision sourcé** (couche « pourquoi / quand choisir »). Un
artefact YAML-graphe par question distincte : patterns (solutions réutilisables), anti-patterns
(échecs sourcés), stdlib (pointeurs officiels), sources/découvertes (catalogs de
découverte), sécurité/performance/observability/architecture (guidance sourcée par domaine).
Les SKILL.md ne doivent vivre dans `knowledge/` que sous `catalogs/` (modules de
bibliothèque/projet de référence — Pi-native) ; **le choix du format doit être un contrat**
: `catalogs/` = modules SKILL.md, le reste de `knowledge/` = YAML-graphe. Pas de domaine
vide : un dossier de domaine n'existe que s'il a ≥ 1 artefact actif, sinon il est listé dans
une roadmap (pas de `.gitkeep`).

#### Contenu attendu

- Par domaine : un README de domaine (1 page : question type, format, sources d'autorité,
  critères d'admission) + les artefacts YAML-graphe.
- `INDEX.md` **généré** depuis l'arborescence (id, kind, statut, domaine, source) — jamais
  maintenu à la main.
- Patterns : sections obligatoires du schéma positif (problem/context/solution/benefits/
  costs/related) — vérifié par le validateur.
- Anti-patterns : schéma négatif (symptom/detect/problem/fix/when_ok) — vérifié par le
  validateur ; homologue positif référencé quand il existe.

#### Contenu interdit

- Corps dupliqués depuis `rules/` ou `recipes/` (charte §4 ; déjà une règle du README —
  la rendre vérifiable par détection de duplication de code blocks).
- Histoires/évidence du metaprojet (jamais de `docs/evidence` dans le Kit).
- Contenu non sourcé ; recommandation de bibliothèque sans critères d'admission.

#### Règles de maintenance

- Admission d'un artefact knowledge : source primaire + question distincte (aucune règle/
  recette existante n'y répond) + schéma de la catégorie complet + relations résolues.
- Promotion d'un pointeur (`*yaml` Source) vers un module vété (`catalogs/.../SKILL.md`) :
  critères explicites (admission 9 critères passée, usage réel, maintien vérifié).
- Fraîcheur : `last_verified` < 12 mois, sinon statut dégradé (warning validateur).

#### Patterns recommandés

- Pattern ↔ anti-pattern comme paires référencées (déjà en place — généraliser).
- Pointer-only pour les sources officielles massives (stdlib) : pas de copie de corps.
- « Une question, un artefact » : la règle anti-duplication de la charte, rendue
  vérifiable par recherche de titres/questions en double.

#### Anti-patterns

- Deux formats pour le même rôle sans contrat ; dossier de domaine vide sans roadmap ;
  index manuel ; artefact « utile » sans source ; duplication de corps de recette.

#### Questions ouvertes

- Uniformiser `libraries/` : tous SKILL.md (vétées) vs tous YAML ? (recommandation : SKILL.md
  pour les vétées avec admission, YAML Source pour les pointeurs — mais alors renommer les
  pointeurs pour lever l'ambiguïté, ex. sous-dossier `pointers/` ou préfixe `source:`.)
- `debugging/` : remplir (procédures d'échec observé — cf. charte « Observed production
  failure ») ou retirer de la taxonomie ?

---

### 2.3 `knowledge/patterns` et `knowledge/anti-patterns` (zoom)

#### Pourquoi ça fonctionne (à extraire en règles)

1. **Id stables et typés** (`pattern:go:concrete-returns`, `pattern:antipattern:go-…`) —
   le routage par graphe promis par la charte, réellement appliqué.
2. **Schémas positifs et négatifs distincts et complets** — chaque artefact répond à une
   question précise et vérifiable (problem→solution→benefits/costs pour les patterns ;
   symptom→detect→fix→when_ok pour les anti-patterns).
3. **Paires pattern/anti-pattern reliées** (homologues référencés) — un agent qui cherche la
   solution trouve aussi l'échec associé et inversement.
4. **Sources primaires réelles** (100go.co, go.dev/wiki, dave.cheney.net, …) avec URLs
   vérifiées à l'admission (les 2 URLs mortes ont été corrigées le 2026-08-04).
5. **Convergence de sources exigée** avant promotion en « full confidence » (décision du
   2026-08-02 : ≥ 2 dépôts indépendants pour pleine confiance ; mono-source = label
   source-unique).

#### Ce qui manque

- Vérification **automatisée** de ces invariants (le validateur ne contrôle ni les sections
  obligatoires par schéma, ni la fraîcheur, ni la présence d'homologue).
- Règle de **rétention** : que devient un pattern quand son écosystème change (dépréciation,
  remplacement par un pattern plus récent) ?

---

### 2.4 `recipes/`

#### Responsabilité actuelle

Procédures ordonnées et **runnables** : 10 SKILL.md avec code Go + tests + section
« Verify the behavior (observable) » (excellent modèle : `recipe-worker-pool`). Les probes
importent ces recettes — preuve de composition. 6 dossiers placeholder (add-authentication,
add-database, add-observability, create-grpc-service, create-rest-api, deploy-container).

#### Problèmes observés

1. **Placeholders sans contrat** : 6 dossiers `.gitkeep` promettent des recettes sans
   définir leur forme, leurs critères d'admission ni leur échéance.
2. La section « Verify the behavior » est **présente dans les bonnes recettes mais pas
   vérifiée par le validateur** : une recette peut être ajoutée sans scénario observable et
   passer le gate.
3. **Naming** : `recipe-cli-interactif` (français) vs `recipe-cli-minimal` — convention de
   nommage non écrite (kebab-case anglais recommandé).
4. Les recettes dépendent de bibliothèques tierces (cobra, viper, koanf, chi, bubbletea…)
   → la cohérence « bibliothèque vétée dans catalogs ↔ recette qui l'utilise » n'est pas
   vérifiée.

#### Responsabilité recommandée

`recipes/` = **couche « comment exécuter cette tâche »**, entièrement runnable et testée.
Une recette = SKILL.md (Problème / Solution minimale / Exemple runnable + test / Scénario
observable / Limites / Sources) + code compilant + test + scénario. **Aucun placeholder** :
les recettes planifiées vivent dans un README/roadmap de zone avec critères de promotion,
pas dans des dossiers vides.

#### Contenu attendu

- Recette : nom kebab-case anglais (`recipe-<domaine>-<sujet>`), module Go autonome sous le
  module `go-agent-kit-v2` (les recettes partagent le go.mod racine — décision à confirmer
  vs module indépendant), test, scénario observable marqué `PASS`/`PARTIAL`/`BLOCKED`.
- Une recette référence les patterns et snippets qu'elle utilise (relations explicites) et
  la/les bibliothèque(s) vétée(s) correspondante(s).

#### Contenu interdit

- Recette non runnable ; scénario affirmé sans exécution ; duplication d'un snippet ;
  framework choisi quand la stdlib suffit ; dépendance non vétée dans `catalogs/libraries/`.

#### Règles de maintenance

- Admission : compil + test + scénario exécuté + limites + sources + relations résolues.
- Le validateur doit exiger : présence d'une section de scénario, présence d'un test,
  cohérence avec le go.mod, résolution des références croisées.

#### Patterns recommandés

- « Verify the behavior » comme format standard (existant — généraliser).
- Recette ↔ probe : chaque nouvelle recette « cœur » candidate à une probe qui l'exerce.

#### Anti-patterns

- Recette écrite sans avoir été exécutée ; recette qui duplique une autre ; placeholder
  qui reste vide ; dépendance non vétée.

#### Questions ouvertes

- go.mod unique pour tout le Kit (recettes + probes + templates + tools) vs modules
  indépendants par recette ? (impact : isolation des dépendances vs simplicité de la gate)
- Faut-il des « recettes de forme » (shape recipes) distinctes des recettes de tâche ?

---

### 2.5 `snippets/`

#### Responsabilité actuelle

Fragments « production-ready » avec métadonnées. 3 vrais snippets (bounded-worker,
errors-once, http-json) au format SNIPPET.yaml + example.go + check.sh ; 7 dossiers
placeholder (cli, cloud, concurrency, database, networking, security, testing). README
existant mais court.

#### Problèmes observés

1. **3 snippets pour 7 catégories annoncées** — la taxonomie précède le contenu, sans
   contrat de remplissage.
2. Le `check.sh` actuel ne vérifie que `gofmt` (snippet `errors-once`) — pas d'exécution
   réelle du fragment. Un snippet « sans validation est incomplet » (charte §4 Layer 4) ;
   le check minimal doit compiler/exécuter.
3. `source:` pointe vers `../../recipes/…/SKILL.md` — bonne pratique (canonique ailleurs),
   mais non vérifiée (chemin relatif + cible existante + pas de duplication).
4. Pas de lien vérifié entre snippet et recette/règle canonique.

#### Responsabilité recommandée

`snippets/` = **vues focalisées et vérifiables d'implémentation canonique** (jamais une
seconde implémentation). Chaque snippet : SNIPPET.yaml (id, purpose, type, tags, go_version,
dependencies, when_to_use, avoid_when, source canonique, complexity, files, tests) +
example.go **compilant** + check.sh **exécutant** (compile + run ou assertions) + un test
minimal si la logique n'est pas triviale. La taxonomie de catégories = celle du graphe
(domaines existants) ; une catégorie vide n'existe pas, elle est listée en roadmap.

#### Contenu attendu

- Snippets couvrant les patterns/recettes existants (relation `validated_by`/`source`
  vérifiée) ; chacun répond à « comment implémenter ce point précis ».
- README de zone : format exact + lien obligatoire vers une source canonique.

#### Contenu interdit

- Code non compilant ; fragment sans source canonique ; duplication d'un corps de recette ;
  snippet « joli mais jamais vérifié » ; catégorie placeholder.

#### Règles de maintenance

- Admission : compil + check.sh qui passe (compile **et** exécute) + source canonique
  résolue + métadonnées complètes.
- Modifier : bump version + re-run check.sh + vérifier que la source canonique n'a pas
  changé de forme.

#### Patterns recommandés

- Un snippet = un pattern, une recette ou une règle ; jamais un nouveau corps de connaissance.
- check.sh minimaliste mais réel : `go test` sur un package jetable ou `go run` + assertions.

#### Anti-patterns

- Snippet orphelin (aucune source canonique) ; snippet qui devient la référence (dérive) ;
- snippet sans check exécutable ; catégorie vide qui attend.

#### Questions ouvertes

- Faut-il des snippets génériques (net/http, sql, slog) issus de la stdlib en plus de ceux
  liés aux recettes ? (le README de `knowledge/stdlib` joue déjà ce rôle — frontière à
  trancher : stdlib = pointeurs de docs, snippets = code exécutable ; une table de
  routage « question → snippet ou stdlib ? » serait utile.)

---

### 2.6 `templates/`

#### Responsabilité actuelle

Squelettes de projets complets. 7 squelettes runnables (rest-api, grpc, cli, worker,
microservice, monolith, cloud-service), chacun avec go.mod/main.go/main_test.go/README.md/
template.yaml, tous marqués `status: partial` ou `planned` (TEMPLATES.md : « remain planned
until each has an executable, tested, observable example »). `template-contract.md` (4
lignes), `TEMPLATES.md` (tableau de promotion), `_kit-skill-authoring.md` (matrice de
création de modules). `api-service/` = placeholder.

#### Problèmes observés

1. **Excellente honnêteté de statut** (partial ≠ prétendu runnable) — c'est un modèle.
   Mais la **promotion n'est pas automatisée** : le validateur exige des fichiers
   (`template.yaml`, `README.md`, `go.mod`, `main.go`, `main_test.go`) mais ne vérifie pas
   le statut déclaré ni le scénario de promotion.
2. Trois documents de contrat (`template-contract.md`, `TEMPLATES.md`,
   `_kit-skill-authoring.md`) se chevauchent partiellement — le rôle de chacun n'est pas
   explicite.
3. `template.yaml` est minimal (name/status/purpose/validation) — pas de critère
   d'acceptation par shape (le tableau TEMPLATES.md le porte à la place : duplication).
4. Placeholder `api-service/` sans contrat (et absent du tableau TEMPLATES.md — incohérent).

#### Responsabilité recommandée

`templates/` = **bases de projet reproductibles, jamais du code « prêt pour la prod »
prétendu**. Un template : template.yaml (name/status/objectif/**critères de promotion
vérifiables par shape**) + squelette Go compilant + test + README de statut. Le statut est
l'état du graphe (`proposed`/`active`/`deprecated`) ; la promotion `planned→active` exige le
scénario observable de la shape (HTTP request, RPC exchange, command invocation… — déjà
listé dans TEMPLATES.md). Les templates **composent** recettes/patterns/snippets (charte §7)
sans dupliquer leur code.

#### Contenu attendu

- Un template actif = scénario observable exécuté et documenté dans le README.
- Tableau de promotion = généré ou vérifié (statut template.yaml ↔ TEMPLATES.md ↔
  validateur).

#### Contenu interdit

- Template « production-ready » sans preuve ; template qui duplique des recettes ; dossier
  de shape vide ; statut déclaré incohérent avec la réalité (validation).

#### Règles de maintenance

- Admission d'une shape : décision (nouvelle shape = nouvelle catégorie de projet
  consommateur) + squelette + test + scénario ; toute shape listée dans TEMPLATES.md doit
  exister physiquement ou être retirée.

#### Patterns recommandés

- Statut explicite par template (le modèle actuel, généralisé et vérifié).
- Promotion check par shape (règle écrite + exécutable).

#### Anti-patterns

- Prétendre runnable sans scénario ; template « starter kit » imposant une architecture
  (cf. leçon ardanlabs : extract-only) ; placeholder sans roadmap.

#### Questions ouvertes

- Faut-il des templates « library » et « desktop » (wails) — shapes supplémentaires
  demandées par les consommateurs ?
- La matrice `_kit-skill-authoring.md` doit-elle devenir un contrat de zone `templates/` ou
  un contrat transversal `modules` (voir §4) ?

---

### 2.7 `probes/`

#### Responsabilité actuelle

Suite d'acceptation observable « consumér-like » : 5 probes exécutables (cli-minimal,
rest-chi, sqlite-sqlc, worker-shutdown, offline) + `run.sh` + README. Les probes
**importent les recettes** (worker-shutdown importe recipe-graceful-shutdown et
recipe-worker-pool) — preuve que les recettes composent. Aucune dépendance LLM/réseau.

#### Problèmes observés

1. **`run.sh` code la liste des probes en dur** — ajouter une probe sans la mettre dans
   run.sh = probe morte (dérive silencieuse).
2. Chaque probe imprime `PASS`/erreur, mais **aucun critère d'acceptation par probe n'est
   versionné** (le README les décrit en prose) ; une probe qui cesse d'être pertinente peut
   rester verte à tort (ex. assertion trop faible).
3. Pas de mécanisme de **couverture** : rien ne garantit que les nouvelles recettes
   « cœur » reçoivent une probe.
4. `probes/` est le lieu physique des **évaluations** de la charte (Layer 6) mais le nom ne
   le dit pas ; le validateur ne vérifie ni la liste run.sh, ni le nombre de probes.

#### Responsabilité recommandée

`probes/` = **évaluations produit exécutables** (acceptance suite). Une probe = un
scénario observable + critère d'acceptation explicite dans son code/README + enregistrement
dans un manifest de probes (généré ou vérifié) ; `run.sh` **découvre** les probes
(glob `probes/*/main.go`) au lieu de les lister. Le manifest `capabilities.yaml` déclare
la capacité `go-probes` ; la gate exige que toute recette « cœur » ait une probe qui
l'exerce (relation `validated_by`).

#### Contenu attendu

- Probe = `main.go` auto-suffisant (net/réseau OK en local) qui sort une ligne `PASS`
  - exit code ; README de probe décrivant le scénario et le critère.
- `probes/README.md` = contrat de zone (comment ajouter une probe, quand, critères).

#### Contenu interdit

- Probe non déterministe (réseau externe, timing flaky) ; probe qui n'asserte rien ;
  probe listée nulle part ; sortie brute d'évidence metaprojet dans le produit.

#### Règles de maintenance

- Ajout : scénario + assertion + découverte automatique par run.sh + gate verte.
- Modifier une recette référencée par une probe : re-run des probes concernées obligatoire.

#### Patterns recommandés

- Probe = « recette exécutée dans un scénario consommateur » (composition, pas duplication).
- Sortie machine-lisible (une ligne PASS + exit code) — déjà en place.

#### Anti-patterns

- Probe qui passe sans asserter ; probe orpheline ; liste en dur qui dérive ; probe
  dépendante d'un service externe.

#### Questions ouvertes

- Étendre aux 3 limites connues (Pi discovery, Wails, TUI) — comment les sonder sans
  dépendance d'harnais ?

---

### 2.8 `tools/`

#### Responsabilité actuelle

- `tools/offline/` : résolveur stdlib-only + manifest + bundle épinglé content-addressed
  (Effective Go) + attribution — **excellent exemple de capacité déterministe vérifiée**
  (tests, checksums, tailles max vérifiées par le validateur).
- `tools/validators/validate-kitv2.py` : gate produit (frontmatter, snippets, templates,
  métadonnées knowledge, bundle, .md vides, comptes de skills).
- `tools/analyzers/`, `tools/generators/` : **vides** (`.gitkeep`).

#### Problèmes observés

1. `analyzers/` et `generators/` sont des promesses non contractées : quel analyseur ?
   quel générateur ? à quelle fréquence ?
2. Le validateur **n'applique pas la charte** : pas de contrôle de cohérence
   manifest↔capabilities, pas de fraîcheur `last_verified`, pas de qualité des descriptions,
   pas de scénario observable exigé, pas de sync INDEX, pas de sync run.sh.
3. Aucun README de zone pour `tools/` : un contributeur ne sait pas où mettre un outil.

#### Responsabilité recommandée

`tools/` = **mécanique de construction et de gate du Kit** (jamais du contenu). Rôles :

- `tools/validators/` : le portail de gouvernance exécutable (étendu, cf. §3.3) ;
- `tools/generators/` : générateurs d'index/comptes (INDEX.md, registre d'artefacts,
  manifest check) — déterministes, exécutés en CI ;
- `tools/analyzers/` : analyseurs sémantiques optionnels (duplication, liens morts,
  fraîcheur) — ou supprimés si le validateur les absorbe ;
- `tools/offline/` : inchangé (capacité de résolution hors-ligne).
Chaque outil = dossier + README (mission, entrées/sorties, gate associée) + test.

#### Contenu attendu

- Un README `tools/README.md` (contrat de zone : qu'est-ce qu'un outil du Kit, où il vit,
  comment il est testé, quelles gates l'exécutent).
- Un générateur d'index minimum en phase 2 (voir §4).

#### Contenu interdit

- Outil non testé ; outil qui dépend d'un réseau en CI ; logique métier du Kit dans un
  outil ; placeholder sans README.

#### Règles de maintenance

- Ajout d'un outil : mission + test + intégration CI ou exclusion documentée.
- Le validateur reste le seul artefact qui peut échouer la gate.

#### Patterns recommandés

- Un validateur par responsabilité (structure / fraîcheur / cohérence manifest) composables.
- Sortie `PASS`/liste d'erreurs, exit code — aligné sur probes.

#### Anti-patterns

- Outils « à voir plus tard » sans contrat ; validateur qui mute sans test ; comptes codés
  en dur (déjà fautif dans capabilities.yaml).

#### Questions ouvertes

- `analyzers/` : garder (analyse de duplication de corps entre artefacts) ou supprimer ?

---

### 2.9 `manifest.yaml` et `capabilities.yaml`

#### Responsabilité actuelle

`manifest.yaml` = identité produit (name/version/schema_version/language/principles/
capabilities/canonical paths/product_status/avoid). `capabilities.yaml` = catalogue de
capacités (source + status par capacité + `coverage` avec comptes) et `known_limits`.

#### Problèmes observés

1. **Double source du même mapping** (`canonical:` vs `capabilities[].source:`) — aucune
   vérification croisée ; la charte exige « single source of truth », ici deux fichiers
   décrivent la même chose et **dérivent déjà** :
   - `capabilities.yaml` annonce `product_skills: 33` ; le validateur exige 45 (vrai compte) ;
   - `knowledge_catalogs: 13` ne correspond à aucun comptage simple (31 entrées de
     catalogues mesurées) ;
   - `manifest.capabilities` liste 10 capacités, `capabilities.yaml` en déclare 7 —
     vocabulaire divergent (product_verification vs go-probes).
2. Les comptes `coverage` sont **manuels** → faux à chaque évolution (cas d'école de
   dérive déjà survenu).
3. `known_limits` (excellent concept) est en prose non structurée — non vérifiable.

#### Responsabilité recommandée

- `manifest.yaml` = **identité et invariants** (name/version/language/principles/avoid) —
  reste.
- `capabilities.yaml` = **contrat machine des capacités** (id, source, status,
  critère de vérification de la capacité) — les comptes `coverage` deviennent **dérivés**
  (générés par `tools/generators/` et vérifiés par le validateur), plus jamais codés en dur.
- Règle : tout chemin déclaré (canonical/source) doit exister ; tout compte doit être
  recalculé et comparé (validateur).
- `known_limits` : format structuré (id, limite, impact, statut) pour que le statut des
  limites connues (PARTIAL) soit suivable.

#### Contenu interdit

- Comptes en dur ; chemins fantômes ; vocabulaire de capacités divergent ; métadonnées
  d'instruction (ces fichiers sont des manifests, pas des entrées d'instructions — déjà
  déclaré dans `metadata_role`).

#### Règles de maintenance

- Modifier un chemin canonique = changer les deux fichiers **dans le même commit** + le
  validateur l'exige.
- Ajouter une capacité = définition + source + critère de vérification + capacité testée.

#### Patterns recommandés

- Un seul endroit déclare une vérité ; l'autre la référence (canonical → capabilities :
  capabilities généré depuis manifest ou vérifié contre lui).
- `metadata_role` explicite (déjà présent — généraliser).

#### Anti-patterns

- Deux manifests en désaccord ; compte à la main ; champ de capacité inutilisé.

#### Questions ouvertes

- Fusionner en un seul manifest ? (recommandation : non — identité vs contrat machine, mais
  avec vérification croisée obligatoire).

---

### 2.10 `AGENTS.md` (produit)

#### Responsabilité actuelle

Page d'entrée du produit pour un agent consommateur : source of truth (une ligne par zone),
workflow (prompts natifs), validation (gate), limits. **Bien écrit et court** — mais il
répond à « qu'est-ce que c'est », pas à « comment faire évoluer le Kit ».

#### Problèmes observés

1. Il décrit les zones mais **pas les contrats** : un agent qui veut ajouter une recette ne
   trouve nulle part les étapes (format, gate, scénario, sources).
2. La gate listée (validateur + go test + gofmt + vet) omet golangci-lint/gosec/govulncheck/
   probes alors que le texte les mentionne (« le gate local tourne aussi… ») — ambigu.
3. Pas de lien vers les futurs contrats de zone (phase 2).

#### Responsabilité recommandée

`AGENTS.md` produit = **point d'entrée unique** : carte des zones (avec pointeur vers le
contrat de chaque zone), règles de changement transverses (workflow, one-writer, gate,
évidence), et liste des contrats de zone. Il **ne duplique pas** les contrats — il route.

#### Contenu attendu

- Table zone → mission → contrat (référence croisée).
- Workflow de contribution (déjà présent, à compléter par « où sont les contrats »).
- Gate complète et sans ambiguïté (toutes les commandes, y compris probes + lint + gosec +
  govulncheck, avec note PATH GOPATH/bin).

#### Contenu interdit

- Corps de contrat de zone dans AGENTS.md ; histoire du metaprojet ; règles de processus
  du metaprojet (elles vivent dans la racine).

#### Règles de maintenance

- Toute création de zone ou de contrat met à jour AGENTS.md dans le même commit.
- Validateur : vérifier que chaque zone référencée existe et chaque contrat référencé
  existe.

#### Patterns recommandés

- Routage plutôt que duplication (AGENTS.md → contrats → artefacts).

#### Anti-patterns

- AGENTS.md qui grossit en manuel ; AGENTS.md qui duplique la charte ou les contrats.

---

### 2.11 `.pi/` (settings, prompts, skills)

#### Responsabilité actuelle

`settings.json` charge `../rules`, `../recipes`, `../knowledge/catalogs` (découverte Pi).
8 prompts de workflow natifs (`workflow-*`, `checklist-*`) — **excellente qualité**,
modèles d'activation explicites. 5 skills de workflow dans `.pi/skills/` (go-code-review,
go-idiomatic-implementation, go-implementation-plan, go-source-retrieval,
go-testing-verification), avec `references/` — contenu de très bonne facture.

#### Problèmes observés

1. **Deux écosystèmes non délimités** : `.pi/skills/` (skills de workflow, 5) vs modules
   SKILL.md (45) dans rules/recipes/catalogs. Le validateur ne compte que les 45 ; les 5
   skills `.pi/skills/` sont hors contrat (pas de `category`/`tags`/`last-verified`).
2. **Chevauchement de rôle** entre `.pi/prompts/` (workflow-implement, checklist-api) et
   `.pi/skills/` (go-implementation-plan, go-code-review) : un agent ne sait pas lequel
   charger ; la duplication de contenu est latente.
3. `settings.json` charge des chemins relatifs (`../rules`) — implicite sur l'installation
   (valide en produit autonome, mais fragile si un consommateur installe autrement).

#### Responsabilité recommandée

- Contrat de délimitation : **`.pi/skills/` = skills de workflow du processus de
  développement** (revue, plan, vérification — durables, liées au processus) ; **modules
  `rules/recipes/catalogs` = contenu de connaissance du Kit** (découvrables par
  description). Deux populations, deux contrats, frontière anti-duplication explicite.
- Prompts = invocation ponctuelle (`/workflow-implement`) ; skills = chargement contextuel
  durable. La règle « une question, une réponse » s'applique : si un prompt et une skill
  répondent à la même question, en garder un et pointer l'autre.
- `settings.json` : documenter le contrat de chemins (relatifs au produit) et le mode
  d'installation.

#### Contenu attendu

- Un README `.pi/README.md` : qu'est-ce qu'un prompt, qu'est-ce qu'une skill de workflow,
  comment les ajouter, frontière avec les modules.
- Frontmatter complet pour les 5 skills (au minimum `description` — sinon Pi ne les charge
  pas — et idéalement `last-verified`).

#### Contenu interdit

- Skill de workflow qui duplique un module de connaissance ; prompt qui duplique une skill ;
  skill sans `description` ; contenu metaprojet (décisions, mémoire) dans `.pi/` produit.

#### Règles de maintenance

- Ajout d'un prompt : convention de nommage, description d'activation, référence à la
  skill/module qu'il orchestre s'il en existe un.
- Ajout d'une skill : contrat de la zone + absence de duplicat (recherche sémantique).

#### Patterns recommandés

- Prompts comme orchestrateurs courts, skills comme chargeurs de procédure, modules comme
  contenu — trois rôles, zéro recouvrement.
- Activation explicite (« Use only after workflow-clarify… » — déjà le cas).

#### Anti-patterns

- Skill de workflow contenant des connaissances de domaine (dérive) ; double écosystème
  non documenté ; prompt sans description.

#### Questions ouvertes

- Faut-il déplacer les 5 skills de workflow vers le metaprojet (elles gouvernent le
  processus de construction du Kit, pas le produit consommé) ? (Le contenu actuel est
  générique Go — la décision est une vraie question de frontière Kit/metaprojet.)

---

### 2.12 `embeddings/` (héritage)

#### Responsabilité actuelle

`embeddings/vector-index/.gitkeep` — résidu d'une conception antérieure (index vectoriel).

#### Problèmes observés

Dossier fantôme : aucune note de décision, aucun contrat, le graphe + index généré rend la
recherche vectorielle superflue dans l'architecture actuelle.

#### Responsabilité recommandée

Suppression (l'historique Git la conserve) ou, si on veut garder la piste, une Decision
Record « embeddings abandonnés — pourquoi » dans le metaprojet et la suppression du dossier
du produit. **Aucun dossier ne vit sans contrat ni décision.**

---

### 2.13 Racine du Kit (go.mod, .golangci.yml, .gitignore)

#### Observations

- `go.mod` : module `go-agent-kit-v2`, go 1.25.6, dépendances directes = bibliothèques des
  recettes (chi, cobra, viper, koanf, bubbletea, sqlite, x/sync). Cohérent avec les
  recettes — mais **la règle « une dépendance = au moins une recette ou template qui
  l'utilise et une admission dans catalogs » n'est pas vérifiée**.
- `.golangci.yml` : set de linters explicite (bonne pratique v2).
- **Frontière du module Go** : `go test ./...` couvre recettes+templates+probes+tools ;
  le validateur ne vérifie pas que tout package nouveau est atteint par la gate.

---

## 3. Architecture cible recommandée

### 3.1 Organisation idéale (constante : le graphe reste l'autorité, les dossiers naviguent)

```text
KitV2/  (le Kit — produit)
├── AGENTS.md                  → point d'entrée : carte des zones + workflow de changement
├── manifest.yaml              → identité + invariants (version, principes, avoid)
├── capabilities.yaml          → contrat machine des capacités (comptes DÉRIVÉS)
├── rules/                     → couche « doit toujours être vrai » (core = budget permanent,
│                                registry = chargé à la demande)
├── knowledge/                 → graphe de décision sourcé (YAML-graphe) + catalogs (SKILL.md)
│     ├── INDEX.md             → GÉNÉRÉ
│     ├── patterns/  anti-patterns/  stdlib/  security/  performance/  observability/
│     │   architecture/  debugging/   (≥1 artefact actif OU roadmap)
│     └── catalogs/libraries/ + reference-projects/   (modules vétés, admission 9 critères)
├── recipes/                   → procédures runnables (SKILL.md + code + test + scénario)
├── snippets/                  → vues vérifiées d'implémentation canonique (SNIPPET.yaml +
│                                example.go + check.sh exécutant)
├── templates/                 → bases reproductibles (statut graphe, promotion par scénario)
├── probes/                    → évaluations produit exécutables (découvertes par run.sh)
├── tools/
│     ├── validators/          → portail de gouvernance (structure + fraîcheur + cohérence)
│     ├── generators/          → index/comptes dérivés (déterministes, CI)
│     ├── analyzers/           → analyseurs sémantiques (ou supprimés)
│     └── offline/             → capacité de résolution hors-ligne (inchangée)
└── .pi/                       → settings + prompts (orchestrateurs) + skills de workflow
```

### 3.2 Responsabilités et relations entre zones (règles de frontière)

| Relation | Règle |
| --- | --- |
| règle core → registry | **interdite** (les universelles ne dépendent pas du chargé-à-la-demande) |
| règle → pattern/anti-pattern | référencée (homologue négatif/positif) |
| recette → pattern/snippet | référencée via relations (`uses`), jamais dupliquée |
| recette → bibliothèque | la bibliothèque doit être vétée dans `catalogs/libraries/` (admission 9 critères) |
| snippet → source canonique | toujours une recette/règle/pattern existant (chemin résolu) |
| template → recettes/snippets | composition déclarée, zéro code dupliqué |
| probe → recette | toute recette « cœur » a une probe qui l'exerce (`validated_by`) |
| manifest ↔ capabilities | cohérence vérifiée (chemins, comptes dérivés) |
| INDEX / roadmap | générés ou vérifiés contre l'arborescence |

### 3.3 Le flux logique d'utilisation par un agent (cible)

```text
1. Charger le Kit → AGENTS.md (carte) → .pi/settings.json (découverte Pi)
2. Tâche de développement → description L1 des modules (rules/recipes/catalogs)
   → chargement L2 du module pertinent → L3 références si besoin
   (progressive disclosure — 3 niveaux, coût permanent = descriptions seules)
3. Choisir une solution → knowledge/patterns + anti-patterns (paires, sourcés)
4. Implémenter → recipes/ (procédure + code + scénario) + snippets/ (vues vérifiées)
5. Amorcer un projet → templates/ (base reproductible, statut honnête)
6. Vérifier → gate (validateur + go test/gofmt/vet/lint/gosec/govulncheck) + probes/
   (évals produit) + scénario observable de la recette
7. Résoudre hors-ligne → tools/offline/ (bundle épinglé)
```

### 3.4 Les trois « vertèbres » de la gouvernance cible

1. **Un contrat par zone** (phase 2) : chaque dossier possède un document MetaProjet qui
   définit mission/format/contenu interdit/règles/patterns/anti-patterns/critères — c'est
   la réponse directe au mandat (« un agent lit les instructions du dossier avant d'y
   travailler »).
2. **Un portail de gouvernance exécutable** : `validate-kitv2.py` étendu (cohérence
   manifest↔capabilities, comptes dérivés, fraîcheur `last_verified`, qualité des
   descriptions, scénarios exigés par catégorie, résolution des références, liens, sync
   INDEX/run.sh) — la charte cesse d'être déclarative et devient vérifiable.
3. **Un cycle de vie explicite** : proposé → actif → déprécié, avec semver par artefact,
   évidence à l'admission, échéance de vérification, et politesse de retrait (jamais de
   suppression sans Decision Record ni migration).

---

## 4. Plan de création des instructions MetaProjet

Après l'audit — phase 2 — ces fichiers seront créés **dans le metaprojet** (racine, sous
`.agent/` ou `docs/`), jamais dans le Kit. Chaque fichier devient le **contrat de
construction** d'une zone ou d'un composant du Kit : mission, format, règles, patterns,
anti-patterns, critères de validation (actionnables et vérifiables, pas vagues).

### 4.1 Contrats transverses (3)

| # | Fichier | Contenu contractuel |
| --- | --- | --- |
| C0 | `kit-governance/00-charte-d-application.md` | Comment la charte s'applique : cycle de vie des artefacts (proposé→actif→déprécié), semver, politique de dépréciation/retrait, write-gate (évidence à l'admission), règles de one-writer/fresh-context review, définition de « done » par type. |
| C1 | `kit-governance/01-manifest-capabilities.md` | Contrat des deux manifests : rôle de chacun, champs obligatoires, règle de cohérence (chemins, comptes dérivés), `known_limits` structuré. |
| C2 | `kit-governance/02-validation-gate.md` | La gate complète : commandes, outillage (PATH GOPATH/bin), signification de PASS/PARTIAL/BLOCKED, extensions du validateur (liste de contrôles exigés, exemples d'échec), CI. |

### 4.2 Contrats par zone du Kit (10)

| # | Fichier | Zone couverte | Contrat clé |
| --- | --- | --- | --- |
| Z1 | `kit-governance/10-zone-rules.md` | `rules/` | Budget de compacité core, frontière core↔registry, schéma de règle (impératif + frontière + contre-exemples + vérification + sources), admission. |
| Z2 | `kit-governance/11-zone-knowledge.md` | `knowledge/` | Deux formats (YAML-graphe vs SKILL.md catalogs) et leur critère de choix, schémas pattern/anti-pattern obligatoires, paires référencées, fraîcheur, INDEX généré, règle des domaines vides. |
| Z3 | `kit-governance/12-zone-recipes.md` | `recipes/` | Format de recette (SKILL.md + code + test + scénario observable obligatoire), nommage, admission, relations (bibliothèques vétées, patterns utilisés), roadmap au lieu de placeholders. |
| Z4 | `kit-governance/13-zone-snippets.md` | `snippets/` | Format SNIPPET.yaml complet, check.sh exécutant (compile+run), source canonique obligatoire et résolue, catégories = domaines existants, roadmap. |
| Z5 | `kit-governance/14-zone-templates.md` | `templates/` | Statut graphe par template, critères de promotion par shape (scénarios observables), composition sans duplication, promotion automatique du tableau de statut. |
| Z6 | `kit-governance/15-zone-probes.md` | `probes/` | Probe = évaluation exécutable (scénario + critère + PASS + exit code), découverte par run.sh, relation `validated_by` recette cœur, limites (Pi discovery, Wails, TUI). |
| Z7 | `kit-governance/16-zone-tools.md` | `tools/` | Mission des 4 sous-zones (validators/generators/analyzers/offline), format d'outil (README + test + gate), placeholders interdits sans contrat. |
| Z8 | `kit-governance/17-zone-pi.md` | `.pi/` | Délimitation prompts (orchestrateurs) / skills de workflow (procédures) / modules (connaissance) ; frontmatter complet exigé ; règle anti-duplication entre les trois ; contrats de chemins settings.json. |
| Z9 | `kit-governance/18-zone-agents.md` | `AGENTS.md` produit | Rôle de point d'entrée (carte + routage, pas de duplication), contenu minimum, règles de mise à jour synchronisée avec les contrats. |
| Z10 | `kit-governance/19-registre-artefacts.md` | Graphe transversal | Registre des kinds d'artefacts (10), schémas de métadonnées par kind, relations autorisées, format d'id, règles de références croisées — le contrat que `validate-kitv2.py` doit appliquer à chaque artefact. |

### 4.3 Contrat d'auteur de modules (1)

| # | Fichier | Contenu contractuel |
| --- | --- | --- |
| A1 | `kit-governance/20-auteur-modules.md` | Élévation du `_kit-skill-authoring.md` (working document) en contrat : invariants communs (frontmatter immuable, progressive disclosure, description = quoi+quand+contraintes négatives, L2 ≤ 500 lignes, chemins relatifs, sources primaires, pas de sections artificielles) + matrice par catégorie (recipe/rule/library/reference-project/core) avec sections obligatoires/conditionnelles, validation minimale et anti-patterns par catégorie. |

### 4.4 Convention de nommage et de format transverses (1)

| # | Fichier | Contenu contractuel |
| --- | --- | --- |
| N1 | `kit-governance/30-conventions.md` | Kebab-case anglais (ids, dossiers, modules) ; règles d'id par kind (`pattern:go:…`, `source:go:…`) ; conventions YAML (schémas, citations, block scalars) ; frontières Kit/metaprojet (ce qui ne doit jamais entrer dans le Kit : mémoire, décisions, évidence, historique) ; politique des placeholders (interdits, remplacés par roadmap). |

### 4.5 Ce que ces contrats devront contenir (gabarit commun)

Chaque contrat Z*/A1/N1 suit le gabarit (exigence du mandat) :

1. **Mission** — la responsabilité unique de la zone, en une phrase.
2. **Format** — arborescence attendue, fichiers obligatoires, schémas (exemple canonique).
3. **Règles** — actionnables, vérifiables (chaque règle formulée pour être contrôlée par le
   validateur ou un grep).
4. **Patterns** — bonnes pratiques obligatoires (issues de l'audit : les modèles qui
   marchent déjà — `Verify the behavior`, paires pattern/anti-pattern, statut honnête,
   pointer-only, probes-composent-recettes).
5. **Anti-patterns** — erreurs fréquentes avec la sanction (le validateur la détecte ou le
   reviewer la refuse).
6. **Critères de validation** — par opération (ajouter / modifier / déprécier) et par
   catégorie (les « minimal validation » de la matrice A1), alignés sur la gate C2.
7. **Questions ouvertes à trancher** — chaque contrat liste ses décisions en attente.

### 4.6 Dépendances de création (ordre)

1. C0 (charte d'application) et N1 (conventions) — socle commun.
2. C1, C2 (manifests, gate) — le portail de gouvernance qui rendra les contrats vérifiables.
3. Z1–Z10 (contrats de zone) — chacun référence C0/C1/C2/N1.
4. A1 (auteur de modules) — dépend de Z1/Z2/Z3 (formats par catégorie).
5. Mise à jour finale de `AGENTS.md` produit et de `docs/plans/` + évidence — via la
   procédure du metaprojet (plan, one-writer, fresh-context review, gate, evidence).

### 4.7 Décisions du propriétaire (actées le 2026-08-04 — enregistrées dans

`.pi/memory/Decisions.md`)

**Résolues :**

1. `libraries/` : **SKILL.md vétées + pointeurs YAML séparés** (sous-dossier
   `pointers/`) — la distinction pointeur/module devient explicite et
   vérifiable.
2. **Module Go unique** conservé (`go-agent-kit-v2`) ; exceptions à décision
   dédiée.
3. `.pi/skills/` : **restent dans le produit** comme skills de workflow ;
   le contrat Z8 délimite prompts/skills/modules et complète le frontmatter.
4. Nettoyages **tous actés** (à exécuter en phase 2, avant la rédaction) :
   suppression `embeddings/` (avec Decision Record), suppression
   `tools/analyzers/`, renommage `rules/core/rules/universal` →
   `rules/core/universal`, remplissage de `knowledge/debugging/` (objectif de
   phase 2).

**En attente — défauts proposés, à confirmer à la revue des contrats :**

→ **Résolus le 2026-08-04 (phase 2) :**

1. **Seuil de fraîcheur `last_verified` approuvé** : 12 mois → warning,
   18 → déprécié (contrat C2/validateur).
2. **Budget de compacité core approuvé** : ≤ 6 modules core, ≤ 300 lignes
   chacun (contrat Z1).
3. **Politique templates — directive propriétaire** : les templates ne sont
   jamais écrits par un agent ; chaque template est un fork léger d'un projet
   open source réel, fiable, fonctionnel, à responsabilité unique, conforme
   aux règles du Kit et sous licence MIT, réutilisable directement avec des
   adaptations minimales documentées ; les squelettes agent-générés existants
   passent en `legacy` et sont remplacés progressivement (contrat Z5).
4. `rules/core/rules/universal` : renommage de chemin (migration) — acté en 4.
5. go.mod unique (recettes+templates+probes) — acté en 2.
6. `analyzers/` : suppression — acté en 4.

---

## 5. Résumé exécutif (une page)

**Le Kit a une vision excellente et une exécution inégale.** La charte (graphe typé,
évidence, composition, validation) est exactement le cadre que la recherche externe
recommande — Google, Anthropic, Red Hat et le standard agentskills convergent vers :
progressive disclosure 3 niveaux, « skills are products », évals avec/sans, write-gate,
semver, CI de qualité. Le Kit implémente déjà plusieurs de ces idées mieux que beaucoup de
kits publics : recettes runnables avec scénario observable, probes qui composent les
recettes, admission sourcée des bibliothèques, bundle hors-ligne vérifié par checksums,
statuts honnêtes (partial/planned).

**Les faiblesses sont toutes du même type : des règles non écrites ou non appliquées.**
Dossiers sans contrat (rules/registry implicite, catalogs bi-format, placeholders),
manifests qui dérivent (33 vs 45), index manuels obsolètes, validateur qui vérifie la
forme mais pas le contrat, deux écosystèmes de skills non délimités, héritage mort
(embeddings). **Aucune de ces faiblesses n'exige de réarchitecture** : elles exigent des
contrats écrits, un validateur étendu, et des comptes/index générés.

**La cible tient en trois vertèbres :** (1) un contrat MetaProjet par zone du Kit —
mission, format, règles actionnables, anti-patterns, critères de validation — créés en
phase 2 (14 fichiers proposés, §4) ; (2) un portail de gouvernance exécutable
(`validate-kitv2.py` étendu) qui applique la charte de façon vérifiable ; (3) un cycle de
vie explicite (proposé→actif→déprécié, semver, fraîcheur, retrait propre). Avec ces trois
vertèbres, n'importe quel agent ou développeur pourra enrichir le Kit dans 3–5 ans de
façon cohérente — l'objectif du mandat.

---

*Fin du rapport d'audit — phase 1. Aucun fichier d'instruction final n'a été créé ; la
liste de la section 4 est le plan de la phase 2, à valider par le propriétaire avant
rédaction.*
