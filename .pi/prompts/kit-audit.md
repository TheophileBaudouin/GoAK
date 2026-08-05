---
description: Audit the complete KitV2 product against KIT_CHARTER.md, rules, evidence, and the metaproject/Kit boundary without modifying files.
argument-hint: "[KitV2 zone]"
---

# Audit permanent du produit KitV2

Tu exécutes un audit **diagnostique, non destructif et traçable**. Le produit
à auditer est `KitV2/`, ou la zone `KitV2/<zone>` passée en argument. Le
prompt lui-même est un outil de maintenance du méta-projet et ne fait jamais
partie du produit livré.

## Contrat de sécurité

- Ne modifie, ne crée et ne supprime aucun fichier du dépôt. Ne lance ni
  formatter, ni fixer, ni générateur, ni `go mod tidy`, ni commande de
  migration, ni commande Git qui change l'état.
- N'applique aucune correction pendant l'inspection. Les recommandations sont
  produites uniquement après la fin de l'inventaire et de l'inspection.
- Ne transforme pas une absence de preuve en conformité. Un contrôle non
  exécutable ou une source non vérifiable reçoit `À VÉRIFIER`, jamais `CONFORME`.
- Ne traite pas le nom d'une règle, d'un dossier ou d'un linter comme une
  preuve : lis le fichier et cite le chemin, la ligne ou la section exacte.
- Lors de l'invocation, audite l'arbre réel et non un résumé ou un inventaire
  fourni par l'utilisateur ; ce prompt ne remplace jamais l'inspection du dépôt.

## 1. Cadrage et périmètre

1. Lis d'abord `KIT_CHARTER.md`, puis les règles applicables de `AGENTS.md` et
   les contrats de zone dans `.agent/kit-governance/`. Le charter est
   l'autorité ; ne le réécris pas dans le rapport.
2. Lis avant toute conclusion le code de ces deux validateurs méta-projet :
   - `.agent/validators/validate-instructions.py` ;
   - `.agent/validators/validate-cognitive.py`.
3. Détermine la cible :
   - sans argument : `KitV2/` entier ;
   - avec un argument `KitV2/<zone>` : cette zone, avec le contexte global du
     charter, de l'installeur, des règles, des manifests et des relations ;
   - toute cible hors de `KitV2/` est refusée comme hors périmètre.
4. Distingue toujours :
   - **fichiers audités** : ceux de la cible qui reçoivent un statut pour
     chaque dimension applicable ;
   - **fichiers de contexte** : charter, règles, validateurs, installeur,
     manifests ou sources lus pour interpréter la cible, mais non comptés dans
     l'inventaire de KitV2 ;
   - **fichiers exclus** : uniquement les cas explicitement justifiés dans le
     rapport ; ils restent comptés dans l'inventaire.

## 2. Inventaire complet — première étape obligatoire

L'inventaire doit précéder toute lecture interprétative. Enregistre un
horodatage UTC (`YYYY-MM-DDTHH:MM:SSZ`), la cible absolue, l'argument reçu et,
si disponible sans modifier le dépôt, le commit ou l'état Git observé.

Construis une liste complète et triée de tous les fichiers réguliers et liens
symboliques sous la cible, y compris les fichiers cachés, YAML, Markdown,
JSON, Go, scripts, manifests, tests, probes, fichiers de configuration et
fichiers binaires. N'utilise pas `head`, `tail`, une sortie tronquée ou une
liste manuelle comme inventaire de référence. Une forme acceptable est :

```sh
find -P "$TARGET" \( -type f -o -type l \) -print | LC_ALL=C sort
```

Conserve cette liste dans un fichier temporaire hors du dépôt si la sortie est
trop grande pour le contexte. Ce fichier temporaire n'est pas un livrable et
ne doit pas être confondu avec le produit.

Attribue immédiatement à chaque chemin un état de couverture dans un ledger
interne : `À INSPECTER`, `INSPECTÉ`, `EXCLU (justification)`, ou `BLOQUÉ
(cause)`. À la réconciliation, aucun chemin ne peut rester `À INSPECTER` :
il doit devenir `INSPECTÉ`, `EXCLU` ou `BLOQUÉ`. Aucun chemin ne peut disparaître
du ledger. Pour les fichiers illisibles, binaires ou liens non résolus,
inspecte au moins le type, la cible et les métadonnées disponibles puis marque
les dimensions impossibles `À VÉRIFIER` ; ne les saute pas silencieusement.

## 3. Inspection séparée du rapport

### Phase A — Construire le modèle de règles

Après l'inventaire, établis une matrice des exigences, sans encore rédiger de
recommandation :

- `§2/§3` : types d'objets et couches cognitives ;
- `§4` : Single Source of Truth, duplication = défaut ;
- `§5` : métadonnées minimales ;
- `§6` : sources avant inclusion et sources enregistrées ;
- `§7` : composition sans duplication entre les couches ;
- `§8` : génération déterministe et absence d'hypothèses cachées ;
- `§9` : validation des artefacts exécutables et comportement observable ;
- `§10` : progression de la connaissance fondée sur les preuves ;
- `§11` : indépendance de l'artefact et absence de contexte caché ;
- `§12` : versionnement, migrations et dépréciation ;
- `§13` : relations explicites ;
- `§14` : Quality Gates ;
- `§15` : Definition of Done ;
- `§16` : principes fondamentaux du Kit ;
- tout contrat de zone applicable dans `.agent/kit-governance/` ;
- toute règle universelle ou spécialisée de `KitV2/rules/` applicable au
  fichier.

Ne transforme pas un conseil de style en violation de charte. Chaque finding
ultérieur doit pointer vers la section normative exacte ou être étiqueté comme
observation hors charte.

### Phase B — Typage dynamique, fichier par fichier

Pour chaque chemin de l'inventaire, détermine séparément :

1. le rôle déclaré par ses métadonnées ou son contenu ;
2. le type de charte le plus défendable parmi `Rule`, `Recipe`, `Pattern`,
   `Snippet`, `Template`, `Capability`, `Evaluation`, `Decision Record`,
   `Source`, `Memory` ;
3. le rôle de support éventuel (`manifest`, `index`, test, probe, outil,
   documentation, configuration) ;
4. le dossier auquel il appartient réellement ;
5. le type et le dossier attendus, s'ils sont déterminables.

Ne déduis jamais un type uniquement du nom du dossier. Un `category` Pi ou un
nom de fichier n'est pas automatiquement le `kind` du charter. Si le type est
absent, ambigu ou contradictoire, marque `À VÉRIFIER` et explique quelles
métadonnées ou relations manquent.

Vérifie aussi le mismatch structurel :

- un fichier déclare un type inconnu ou un type incompatible avec son rôle ;
- un fichier réutilisable n'a aucun rattachement à un objet de charte ;
- une couche du charter semble absente de `KitV2/`, ou est représentée par un
  autre mécanisme (manifest, graphe, probe, outil) non documenté ;
- pour toute capacité couverte par une recette ET une probe (ex. desktop-app),
  vérifier qu'une ligne roadmap de template existe dans
  `templates/TEMPLATES.md` ; une capacité couverte partout sauf au niveau
  template, sans reconnaissance roadmap, est une catégorie de finding nommée
  à part entière, pas un cas générique noyé dans la formulation actuelle
  (D-2026-08-05-14) ;
- un dossier existe mais mélange plusieurs responsabilités sans frontière
  explicite.

L'absence d'un dossier portant exactement le nom d'un type n'est pas à elle
seule une erreur : rapporte-la comme `CONFORME`, `NON CONFORME` ou `À VÉRIFIER`
selon la représentation déclarée et la preuve de conception.

### Phase C — Contrôles par fichier et par relation

Pour chaque fichier, évalue les dimensions suivantes. Utilise `N/A
(justifié)` seulement lorsqu'une dimension est réellement inapplicable.

#### C1. Charte et contrat de zone

Vérifie la conformité aux sections pertinentes de `KIT_CHARTER.md` et au
contrat de zone. Cite la section précise (`§4`, `§5`, etc.) et le chemin du
contrat. Ne remplace pas le charter par une checklist inventée.

#### C2. Métadonnées et rattachement

Pour tout artefact réutilisable, vérifie la présence et la valeur utile de
chaque champ §5 :

```text
id, title, kind, version, status, owner, tags, go_version,
dependencies, last_verified
```

Vérifie aussi les relations explicites lorsque le type les exige :
`depends_on`, `uses`, `implements`, `extends`, `references`, `requires`,
`supersedes`, `validated_by`, `generated_from`. Distingue une métadonnée Pi
nécessaire à la découverte (`name`, `description`, etc.) des métadonnées du
graphe de connaissance du charter : l'une ne remplace pas l'autre. Vérifie
également §12 : version, statut de dépréciation, migration documentée pour les
changements cassants et cohérence des évaluations dépendantes.

#### C3. Sources et fraîcheur réelle

Vérifie que les sources sont enregistrées dans l'artefact ou dans le registre
canonique prévu, qu'elles sont primaires ou justifiées par le charter, et que
la version/date revendiquée correspond à la source. Si l'accès réseau n'est
pas possible, garde la source et marque la vérification de fraîcheur `À
VÉRIFIER`; ne te fie pas au seul champ `last_verified`. Signale les URL
manquantes, mortes, non canoniques, vagues ou les affirmations sans preuve.

#### C4. Single Source of Truth et duplication

Recherche :

- doublons exacts ou quasi exacts entre fichiers ;
- même règle opérationnelle copiée dans plusieurs couches ;
- recette qui recopie un pattern ou un snippet au lieu de le composer ;
- catalogues, indexes, manifests ou README qui contredisent le corps
  canonique ;
- traduction ou seconde version linguistique qui répète le même contenu au
  lieu de le référencer.

Une similarité de vocabulaire ne suffit pas : cite les passages qui répondent
à la même question. Si une duplication peut être détectée mécaniquement
(hash, bloc identique, identifiant répété), indique-le séparément d'une
duplication sémantique qui exige une revue humaine.

Échantillonne en outre explicitement les chaînes de pointeurs
pattern↔recette↔snippet (D-2026-08-05-11) : pour chaque snippet, résoudre
`source:` (SNIPPET.yaml) vers son artefact canonique et comparer la forme du
code ; pour chaque recette, identifier les patterns/snippets référencés et
vérifier qu'elle les compose sans les recopier. La dérive d'une chaîne
(canonique modifié, snippet non re-vérifié) est un finding distinct de la
duplication interne à une cible — indique pour chaque chaîne si elle est
contrôlable mécaniquement par dates (`last_verified` dépendant >= canonique)
ou seulement par revue.

#### C5. Indépendance et dépendances cachées

Un agent qui charge un seul artefact doit pouvoir comprendre son usage sans
conversation antérieure ni mémoire du méta-projet. Vérifie les dépendances
explicites, les cross-références résolubles et l'absence de chemins cachés
vers `.agent/`, `.pi/memory/`, `docs/` ou d'autres fichiers non livrés. Un
fichier KitV2 ne doit pas dépendre de `../.agent` ou d'une source disponible
uniquement dans le méta-projet. Les relations déclarées vers des cibles
manquantes, proposées ou non actives sont des findings distincts.

#### C6. Validation §9 et preuve observable

Pour les recipes, snippets, templates, probes, outils ou tout autre artefact
exécutable, localise les commandes, tests, scénarios et critères d'acceptation.
Vérifie qu'ils couvrent le comportement central, les erreurs importantes et,
si pertinent, race/security/vulnerability checks. Une compilation ou un test
vert ne remplace pas un scénario observable ; une preuve non exécutée est
`À VÉRIFIER`, jamais `CONFORME`. N'exécute que des commandes sans modification
du dépôt et indique exactement ce qui a ou n'a pas été exécuté.

#### C7. Langue et cohérence éditoriale

Détermine la langue dominante de chaque famille d'artefacts à partir du
contenu réel. Signale :

- un mélange de langues qui rend une même instruction incohérente ;
- une traduction intégrale du même contenu dans un seul fichier ou dans deux
  fichiers ;
- des titres, métadonnées et sections qui changent de langue sans raison
  explicite ;
- une citation, un identifiant, un nom d'API ou un extrait source qui n'est
  pas une violation linguistique.

Ne décrète pas arbitrairement que l'anglais ou le français est la langue
obligatoire. Le défaut est la cohérence d'une famille ; toute politique
explicite du dépôt prime sur une préférence stylistique.

#### C8. Exemples de code et règles universelles

Pour chaque bloc Go d'une recipe, d'un snippet, d'un template ou d'un probe,
lis les règles universelles pertinentes avant de conclure. Vérifie notamment
les erreurs traitées une seule fois, le contexte et l'annulation, logging,
validation aux frontières, interfaces consommateur, fermeture des ressources,
concurrence, sécurité et commandes de validation. Cite le fichier de règle et
la ligne du bloc. Si un contrôle exige une analyse que la lecture Markdown ne
permet pas, marque-le `À VÉRIFIER` plutôt que d'inventer un verdict.

#### C9. Instructions absolues et portes mécaniques

Inventorie chaque instruction absolue du Kit (`MANDATORY`, « toujours »,
« jamais ») dans les artefacts consommateurs (skills, prompts, AGENTS.md,
recettes) et son statut d'application : contrôle mécanique nommé (validateur
C2, porte Pi) ou « guidance seule, non appliquée » consignée dans le registre
des lacunes d'automatisation (`.agent/instructions.md` §Enforcement). Une
absolue sans contrôle ni consignation est un finding (D-2026-08-05-15) —
n'évalue pas seulement la présence de la phrase, mais ce qui l'applique.

### Phase D — Décider « méta-projet ou Kit ? »

Cette dimension est obligatoire pour **chaque fichier**, y compris les fichiers
de support. Le méta-projet crée, gouverne, audite et fait évoluer le Kit ; le
Kit est le produit consommable dont l'unique objectif est d'aider un agent à
générer du code Go propre et des applications Go sans friction.

Classe chaque fichier selon la décision la mieux étayée :

- `KIT — consumer-facing` : connaissance, capacité, règle, recette, snippet,
  template, source embarquée, probe ou outil dont le consommateur a besoin
  pour utiliser, vérifier ou maintenir localement le produit installé ;
- `META-PROJET — maintenance/gouvernance` : charter, contrat de construction,
  mémoire du méta-projet, décision de fabrication, plan, recherche, évidence,
  registre de sources de travail, audit, workflow de création/évolution,
  validateur du méta-projet ou prompt de maintenance ;
- `AMBIGU — décision à prendre` : valeur potentielle pour le consommateur et
  le mainteneur non séparées, ou responsabilité partagée ;
- `HORS PÉRIMÈTRE / EXCLU` : uniquement avec raison explicite et preuve.

Applique ces tests, dans l'ordre :

1. Si le fichier disparaît du dépôt source mais que le Kit installé conserve
   la même capacité consommateur, il est probablement méta-projet.
2. Si un agent consommateur chargé uniquement du Kit doit le lire ou l'exécuter
   pour générer/valider du Go, il est probablement Kit.
3. Un fichier de fabrication, d'audit permanent, de preuve historique ou de
   gouvernance n'est pas rendu produit par le simple fait qu'il parle de
   `KitV2`.
4. `KitV2/probes/`, `KitV2/tools/offline/` et `KitV2/.pi/` ne sont pas
   automatiquement de la pollution : mesure leur contrat consommateur réel,
   leur autonomie et leur présence dans l'installation.
5. À l'inverse, un fichier de maintenance placé dans `KitV2/` est une
   pollution potentielle même s'il compile. Mesure son utilité consommateur,
   son coût de contexte et le risque de livrer l'historique ou le contrôle du
   méta-projet.

Pour toute décision `META-PROJET`, `AMBIGU` ou `NON CONFORME`, fournis la
preuve de frontière : chemin, responsabilité, consommateur visé, et résultat
de l'inventaire de l'installeur. Ne corrige jamais le déplacement dans cet
audit.

## 4. Contrôle de couverture et des validateurs existants

Après l'inspection seulement, réconcilie les résultats. Produis ces comptes,
sans arrondir et sans compter les fichiers de contexte :

```text
trouvés = audités + exclus_justifiés + bloqués
```

- `trouvés` : nombre exact de chemins de l'inventaire ;
- `audités` : chaque chemin ayant reçu un statut par dimension applicable ;
- `exclus_justifiés` : chemins avec raison et catégorie explicites ;
- `bloqués` : chemins non lisibles ou impossibles à évaluer, avec cause et
  prochaine vérification.

Si l'équation ne ferme pas, le verdict global du workflow est `FAIL —
COUVERTURE INCOMPLÈTE`, même si les findings connus semblent mineurs. Signale
les chemins non inspectés individuellement. Une cible de zone doit aussi
indiquer combien de fichiers de contexte ont été lus mais exclus du calcul.

Dans une section séparée, compare les contrôles observés avec les deux
validateurs existants :

- indique précisément ce que `validate-instructions.py` couvre déjà (schéma
  Pi des skills, liens relatifs, limite de taille, absence de mémoire
  consommateur, description des prompts) ;
- indique précisément ce que `validate-cognitive.py` couvre déjà (métadonnées
  et relations des artefacts YAML pris en charge, statuts/cibles, unités de
  sources, fuite de chemins méta-projet et bundle hors ligne) ;
- ne reconstruis pas ces contrôles dans le rapport comme s'ils étaient absents ;
- signale les trous réels : tous les types de fichiers non couverts, §5
  complet, duplication sémantique, langue, fraîcheur effective des sources,
  composition, indépendance et décision méta-projet/Kit ;
- pour chaque trou, recommande le meilleur niveau de contrôle :
  `validate-instructions.py` pour une contrainte déterministe du format Pi,
  `validate-cognitive.py` pour le graphe/relations, un nouveau validateur
  déterministe pour une propriété de structure indépendante, ou ce workflow
  agent/revue pour une propriété sémantique. Ne modifie aucun validateur.

Attention : n'étends pas automatiquement le schéma Pi publié avec les champs
§5 du charter. Si ces contrats sont différents, recommande un contrôle séparé
ou une décision de contrat explicite plutôt qu'un changement silencieux.

## 5. Rapport final — après l'inspection uniquement

Le rapport est compact mais complet. Il doit contenir, dans cet ordre :

### A. En-tête

- `KitV2 Audit — <date UTC>` ;
- cible exacte et argument ;
- statut non destructif ;
- commit/état observé si disponible ;
- versions des validateurs et commandes réellement exécutées.

### B. Inventaire et réconciliation

Donne l'horodatage de l'inventaire, les quatre nombres `trouvés/audités/
exclus/bloqués`, l'équation et le verdict de couverture. Fournis le ledger
complet ou une table exhaustive par chemin ; une ligne peut regrouper plusieurs
fichiers seulement si chaque fichier garde un statut individuel récupérable et
si les chemins sont tous énumérés. Les fichiers de contexte sont listés à
part séparément.

### C. Verdict par fichier et par dimension

Chaque fichier de la cible doit apparaître dans une table ou un ledger avec au
minimum :

```text
path | rôle/kind | placement (KIT/META/AMBIGU) |
charter | type/zone | metadata | sources/fraîcheur |
SSOT/duplication | validation | indépendance |
langue | cohérence code/règles | confiance | risque | verdict global
```

Les valeurs autorisées sont `CONFORME`, `NON CONFORME`, `À VÉRIFIER` ou `N/A
(justifié)`. Pour chaque `NON CONFORME` ou `À VÉRIFIER`, référence un finding
stable et une preuve précise. Le verdict global ne peut pas être `CONFORME`
si une dimension applicable est `NON CONFORME` ou `À VÉRIFIER`.

### D. Findings classés

Numérote les findings de manière stable (`KVA-001`, `KVA-002`, …) et utilise
le format :

```text
ID | catégorie | risque | confiance | fichier/ligne | preuve |
section KIT_CHARTER ou contrat | impact | action recommandée (sans l'appliquer)
```

Sépare `risque` (`CRITIQUE`, `ÉLEVÉ`, `MOYEN`, `FAIBLE`) de `confiance`
(`ÉLEVÉE`, `MOYENNE`, `FAIBLE`). Utilise notamment :

- `CRITIQUE` : violation §4/§5/§6/§11/§14/§15, fuite de contrôle du
  méta-projet dans le Kit, source essentielle invérifiable, ou couverture non
  fermée ;
- `ÉLEVÉ` : type ou relation incohérente, métadonnées essentielles absentes,
  artefact exécutable sans validation, duplication opérationnelle ;
- `MOYEN` : dérive de langue, fraîcheur à confirmer, incohérence d'index ou
  règle applicable non prouvée ;
- `FAIBLE` : amélioration éditoriale qui ne change pas la capacité ni la
  traçabilité.

Une hypothèse non confirmée ne devient pas un finding à confiance élevée.
Regroupe les findings identiques mais conserve tous les chemins concernés.

### E. Lacunes d'automatisation

Tableau séparé : `dimension | déjà couvert par | trou | contrôle conseillé |
raison`. Indique clairement ce qui doit rester une analyse sémantique humaine
ou agentique et ce qui peut devenir une assertion Python répétable.

Le tableau contient au minimum, à chaque audit :

- la ligne « dérive inter-fichiers » : chaînes pattern↔recette↔snippet
  contrôlables par dates (`last_verified` dépendant >= canonique) vs revue
  sémantique (D-2026-08-05-11) ;
- la ligne « instructions absolues (MANDATORY) » : chaque occurrence
  MANDATORY/« toujours »/« jamais » du Kit et son statut d'application
  (contrôle mécanique nommé ou « guidance seule » — D-2026-08-05-15).

### F. Verdict et suites

Termine par :

- `Audit: PASS`, `PARTIAL`, `FAIL` ou `BLOCKED` ;
- couverture exacte et résiduel de confiance ;
- pollution méta-projet/Kit détectée, avec nombre et chemins ;
- commandes non exécutées et pourquoi ;
- prochaines actions proposées, sans les exécuter.

`PASS` exige une couverture fermée, aucun finding critique/élevé non résolu,
et aucune dimension applicable `À VÉRIFIER`. Une source réseau indisponible,
un scénario non exécuté ou un fichier illisible force au minimum `PARTIAL` ou
`BLOCKED` selon son importance.

## Rappel final

Ce workflow répond à deux questions différentes et obligatoires :

1. **Le fichier est-il conforme au charter et aux règles applicables ?**
2. **Le fichier a-t-il sa place dans le produit consommable, ou pollue-t-il
   KitV2 alors qu'il appartient au méta-projet qui le construit et le
   maintient ?**

Ne fusionne jamais ces questions, ne corrige jamais pendant l'audit et ne
présente jamais un résumé complaisant à la place du ledger de couverture.
