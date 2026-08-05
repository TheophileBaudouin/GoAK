# Templates de gouvernance du projet

Templates pour les surfaces d'instructions au niveau projet et la résolution
de la surface mémoire générés en phase 4. Mets à jour les fichiers existants
en place quand ils existent. Préfère la mémoire native `.pi/memory/` ; ne
crée un fichier mémoire de secours repo-local que quand le projet en déclare
déjà un ou que l'utilisateur le choisit explicitement.

---

## AGENTS.md (projet)

```markdown
# Project Agent Instructions

## Scope

These instructions apply to the whole repository.

## Truth Sources

- `<chemin>` — <pourquoi ce fichier est autoritaire>
- `<chemin>` — <pourquoi ce fichier est autoritaire>

## Development Rules

- Follow the existing architecture and naming conventions.
- New features or behavior changes must add or update relevant automated
  tests.
- If no automated test surface exists, run the closest static/syntax
  validation and record the limitation.
- Record durable project facts, commands, invariants, and recurring gotchas
  in the resolved native memory surface (` .pi/memory/` ) when available.
- **Vérifie quels fichiers mémoire existent réellement** : le bootstrap Pi
  peut ne créer que Brief/Progress/Gotchas/Agent, sans `Decisions.md`. Ne
  suppose jamais l'ensemble standard ; crée les fichiers manquants au format
  attendu, sans copier d'historique externe.
- Do not create a repo-local memory file unless the workflow explicitly
  records that fallback decision.
```

---

## Résolution de la surface de gouvernance

```markdown
# Résolution de la surface de gouvernance

## Surfaces d'instructions

| Surface | Statut | Rôle | Notes |
|:--------|:-------|:-----|:------|
| `AGENTS.md` | existant / créé / non utilisé | Règles agent partagées | |
| `.cursor/rules/` | existant / absent / non touché | Règles Cursor | |
| `.windsurf/` | existant / absent / non touché | Règles Windsurf | |
| `.clinerules*` | existant / absent / non touché | Règles Cline | |
| `.codex/` | existant / absent / non touché | Fichiers projet Codex | |

## Surface mémoire

| Champ | Valeur |
|:------|:-------|
| Mémoire native disponible | oui / non |
| Surface mémoire résolue | `.pi/memory/` (fichiers vérifiés : Brief, Progress, Gotchas, Agent, Decisions — marquer ceux absents) / fichier existant / fallback explicite / indisponible |
| Fallback repo approuvé | oui / non / non nécessaire |
| Notes | comment les faits durables doivent être enregistrés |
```

---

## Fichier de secours mémoire repo-local (optionnel)

À utiliser seulement quand aucune surface mémoire native n'est disponible et
que l'utilisateur choisit explicitement un fallback repo-local.

```markdown
# Project Memory

This file stores durable project facts and decisions because no native
project memory surface was available or selected. It is not a progress log;
active workflow state belongs in `docs/progress/MASTER.md` during a
spec-driven run.

## Stable Project Facts

- <fait>

## Durable Engineering Rules

- <règle>

## Recurring Gotchas

- <gotcha et atténuation>
```
