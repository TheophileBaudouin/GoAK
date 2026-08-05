# Templates d'archive

Templates pour la phase 6 (Archive). Sortie vers `docs/archives/`.

---

## docs/archives/README.md (index des archives)

```markdown
# Project Archives

This directory contains archived artifacts from completed Spec-Driven Develop
workflows. Each subdirectory represents one development project, preserving
its full analysis, plan, and progress history for future reference.

| Project | Description | Period | Mode | Progress |
|:--------|:------------|:-------|:-----|:---------|
| [<nom-du-projet>](./<nom-du-projet>/progress/MASTER.md) | Description en une ligne | YYYY-MM-DD — YYYY-MM-DD | LOCAL_ONLY | Terminé |
```

Quand tu mets à jour ce fichier, ajoute de nouvelles lignes au tableau. Ne
supprime pas les entrées existantes.

---

## Structure du répertoire d'archive

```text
docs/archives/<nom-du-projet>/
├── analysis/
│   ├── project-overview.md
│   ├── module-inventory.md
│   └── risk-assessment.md
├── plan/
│   ├── task-breakdown.md
│   ├── dependency-graph.md
│   └── milestones.md
├── progress/
│   ├── MASTER.md
│   ├── phase-1-<nom-court>.md
│   └── ...
└── governance/
    ├── instruction-surfaces.md
    ├── AGENTS.md              # si résolu et fichier-backé
    └── memory-surface.md      # note d'export ou instantané du fallback, si disponible
```

Archive les surfaces de gouvernance comme instantanés ou notes d'export
uniquement. Garde les surfaces d'instructions et de mémoire actives en place
après l'archivage. Si la mémoire est native et ne peut pas être exportée,
enregistre sa plateforme/nom et les décisions clés qui y ont été écrites.
