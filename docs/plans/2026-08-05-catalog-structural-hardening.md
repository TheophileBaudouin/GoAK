# Durcissement structurel du catalogue GoAK

**Date :** 2026-08-05  
**Objectif :** éliminer la duplication interne et les exemples Go incohérents avec les rules, puis rendre ces régressions vérifiables par la gate.  
**Périmètre :** `KitV2/knowledge/catalogs/`, `KitV2/recipes/*/SKILL.md` contenant des exemples Go, gouvernance `AGENTS.md`/`.agent/kit-governance/`, et `KitV2/tools/validators/validate-kitv2.py`.  
**Hors périmètre :** CLI `gak`, séparation kit/projet, adapters multi-agents.

## Décisions exécutées

- Une fiche catalogue conserve une langue de contenu cohérente et une seule réponse par information ; les sections ne recopient pas les mêmes limites.
- Une mise à jour de catalogue nécessite une recherche web fraîche ; le validateur bloque une fiche de bibliothèque après 90 jours et un projet de référence après 180 jours.
- Les blocs Go de catalogue/recipe doivent traiter les erreurs et ressources, ou documenter explicitement une suppression justifiée.
- Le validateur ajoute des contrôles déterministes ; la duplication sémantique complexe reste un contrôle de revue obligatoire, car un parseur lexical ne peut pas prouver seul qu'une reformulation n'ajoute rien.

## Séquence

1. Ajouter les règles de gouvernance et le contrôle validator en mode strict opt-in ; ajouter les cas positifs et négatifs du validator.
2. Obtenir une revue fraîche des règles et du mécanisme.
3. Commit unique des règles/validator/tests de Phase 2.
4. Traiter séquentiellement chaque `SKILL.md` de `knowledge/catalogs` : recherche web primaire fraîche, réécriture complète, vérification, commit atomique.
5. Traiter les recipes avec blocs Go si elles sont corrigées par le diagnostic.
6. Activer le mode strict catalogue et régénérer le router si les descriptions/chemins changent.
7. Exécuter la gate complète et produire le journal des recherches et commits.

## Critères de fin

- Chaque fichier catalogue porte des sources URL datées et une date `last-verified` vérifiée.
- Aucun bloc Go ne contient de retour ignoré non justifié par la règle.
- Aucun paragraphe identique ne se répète entre sections du même fichier.
- Les contrôles validator ont un cas positif et négatif.
- Chaque fichier réécrit a un commit atomique et une entrée du journal.
- `validate-kitv2.py`, Go gate et probes passent ; les éventuelles limites sémantiques sont explicitement rapportées.
