# Règles comportementales

Ces règles s'appliquent à chaque agent et à chaque phase du workflow
Spec-Driven Develop. Elles sont non négociables.

---

1. **Ne saute jamais de phase.** Même si tu penses qu'une phase est inutile,
   crée au minimum une version allégée de ses sorties.

2. **Confirme toujours avec l'utilisateur** avant de passer à la phase
   suivante. Chaque frontière de phase est un point de contrôle.

3. **Documente tout.** Si tu prends une décision, enregistre-la dans la
   section « Notes » du fichier de progression pertinent.

4. **Les mises à jour de progression sont obligatoires.** Après avoir terminé
   une tâche, enregistre immédiatement sa télémetry et son état
   d'implémentation. Mode LOCAL_ONLY : coche la case dans le fichier de phase
   ET le compteur de complétion dans MASTER.md. L'outil de suivi natif de la
   plateforme (todo) est une couche complémentaire optionnelle.

5. **Nouvelle conversation = lis MASTER.md en premier.** Non négociable. Le
   fichier maître est ta mémoire entre conversations.

6. **Respecte le temps de l'utilisateur.** Garde des résumés concis. Utilise
   des puces et des tableaux, pas des murs de texte.

7. **L'archivage n'est pas optionnel.** Quand toutes les tâches sont
   terminées, entre toujours en phase 6 (Archive). Archive tous les artefacts
   vers `docs/archives/` pour traçabilité — ne les laisse pas éparpillés dans
   les répertoires de travail et ne les supprime pas.

8. **Écriture double des mises à jour de progression.** Quand tu termines une
   tâche, mets à jour la progression à deux endroits pour la redondance :
   l'outil de suivi natif de la plateforme (marquer comme terminé) + les
   fichiers Markdown de progression (cocher la case, mettre à jour les
   comptes). Le principe est le même dans tous les modes : aucun point de
   défaillance unique pour l'état de progression.

9. **Utilise l'outil de questions structuré de la plateforme pour toutes les
   interactions utilisateur.** Chaque fois que tu dois poser une question,
   demander une clarification ou obtenir une confirmation (y compris les
   points de contrôle de frontière de phase), tu DOIS utiliser l'outil de
   questions/choix structuré intégré (par exemple `ask_user_question` dans
   Pi). Ne te fie pas à une sortie texte brut pour poser des questions —
   l'outil garantit que l'utilisateur voit et répond directement. Si la
   plateforme n'a pas cet outil, demande en texte brut et attends une réponse
   explicite.

10. **La télémetry post-tâche est obligatoire.** Après avoir terminé chaque
    tâche, enregistre l'effort réel, le score S.U.P.E.R et le nombre de
    dépendances imprévues AVANT de marquer la tâche comme terminée. Aussi non
    négociable que les mises à jour de progression (règle 4). Voir
    `references/adaptive-control.md` § « Collecte de télémetry » pour quoi
    collecter et § « Stockage de l'état adaptatif » pour où stocker.

11. **Les déclencheurs de seuil de dérive sont automatiques.** Quand
    `drift_score` dépasse un seuil, l'agent DOIT s'arrêter et exécuter
    l'action de réponse correspondante (annoter / replanifier / ré-évaluer)
    sans attendre l'instruction de l'utilisateur. Les seuils sont calculés par
    phase en pourcentage du nombre total de tâches (20 % / 40 % / 60 %). Voir
    `references/adaptive-control.md` § « Actions de réponse automatiques »
    pour le protocole de réponse.

12. **L'état adaptatif est persistant.** Lis et écris toujours `drift_score`
    via le stockage défini : la section « Adaptive Control State » de
    MASTER.md en mode LOCAL_ONLY. Ne stocke jamais l'état adaptatif seulement
    dans la mémoire de conversation — il doit survivre aux sessions.

13. **La résolution de la surface de gouvernance du projet est obligatoire.**
    Chaque run spec-driven doit résoudre les surfaces d'instructions partagées,
    les surfaces d'instructions spécifiques à la plateforme et la surface de
    mémoire durable AVANT le début de l'exécution. Préfère les surfaces
    existantes/natives. Surfaces typiques : `AGENTS.md`, `.cursor/rules/`,
    `.windsurf/`, `.clinerules*`, `.codex/`, ou équivalents projet.

14. **Ne crée pas de sources de vérité concurrentes.** Si un projet a déjà des
    surfaces d'instructions ou de mémoire équivalentes, mets à jour les
    surfaces canoniques en place et enregistre la résolution dans MASTER.md.
    Utilise la mémoire native (`.pi/memory/`) quand elle est disponible. Ne
    crée pas silencieusement un fichier mémoire repo-local ; ne l'utilise que
    quand le projet le déclare déjà ou que l'utilisateur le choisit
    explicitement. **Vérifie quels fichiers mémoire existent réellement — le
    bootstrap Pi peut ne pas créer `Decisions.md` ; ne suppose jamais
    l'ensemble standard.**

15. **Le travail de fonctionnalité exige des tests par défaut.** Toute tâche
    qui ajoute ou change des fonctionnalités visibles par l'utilisateur, du
    comportement métier, des contrats d'API, des schémas, des migrations, du
    parsing, du routage, des permissions, du cache ou de la persistance doit
    ajouter ou mettre à jour des tests automatisés pertinents. Si les tests ne
    sont pas applicables ou que le projet manque de surface de test, la tâche
    doit en donner la raison et exécuter la validation statique/syntaxique la
    plus proche disponible.

16. **Les apprentissages stables vont à la surface mémoire résolue.** Quand
    l'exécution révèle une commande réutilisable, un invariant, une convention
    de projet, un gotcha récurrent ou une règle pour les futurs agents,
    enregistre-le dans la surface mémoire native résolue (`.pi/memory/`) ou le
    fallback explicitement choisi. Si cela change la façon dont les agents
    doivent travailler dans le dépôt, mets aussi à jour les surfaces
    d'instructions résolues.

17. **Les tâches et les lots ont des cardinalités différentes.** Les tâches
    sont des unités atomiques de planification, d'acceptation et de
    télémetry ; les lots de livraison sont des unités d'implémentation,
    de validation d'intégration. Avant d'éditer une phase, revois toutes ses
    tâches et forme le plus petit ensemble cohérent de lots locaux. Défaut :
    un lot validable par phase, pas un lot par tâche. Ne divise que pour une
    frontière documentée de revueabilité, de release/rollback, de propriété,
    d'isolation de risque, de dépendance ou de politique de dépôt. Un lot à
    tâche unique exige une justification explicite sauf s'il est le seul de la
    phase.

18. **Frontières d'autorité du reviewer.** Dans la boucle de revue
    d'exécution, le reviewer de lane peut commiter des corrections seulement
    sur la branche de sa lane (append-only, commits `fix:` référençant mais ne
    fermant jamais de tâches). Les reviewers n'éditent jamais MASTER.md, ni
    l'état de dérive/adaptatif, ni les surfaces d'instructions ou de mémoire —
    leurs rapports de revue reviennent à l'orchestrateur. L'orchestrateur
    reste l'autorité de vérification des critères d'acceptation et le seul
    writer des états partagés.

19. **Le dispatch de sous-agents est une décision économique, pas un défaut.**
    Ne dispatche que quand le gain de parallélisme et la valeur d'isolation de
    contexte dépassent le coût de démarrage à froid et la surcharge
    d'orchestration. L'exécution orchestrateur-direct (Tier 0) est le défaut ;
    la délégation à un seul codeur (Tier 1) est pour le travail L/XL ou lourd
    en contexte ; les lanes parallèles (Tier 2) exigent des ensembles de
    fichiers disjoints, ≥ L d'effort par lane, une vérifiabilité indépendante
    et ≤ 4 lanes. La revue est elle aussi tiercée : validation machine (L1) et
    revue du diff par l'orchestrateur (L2) sont le défaut ; les reviewers
    indépendants (L3) sont réservés aux lanes Tier 2 et aux changements à haut
    risque. Les critères d'admission vivent dans `references/parallel-protocol.md`.
