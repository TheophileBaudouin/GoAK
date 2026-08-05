# Archive Templates

Templates for Phase 6 (Archive). Output to `docs/archives/`.

---

## docs/archives/README.md (Archive Index)

```markdown
# Project Archives

This directory contains archived artifacts from completed Spec-Driven Develop
workflows. Each subdirectory represents one development project, preserving
its full analysis, plan, and progress history for future reference.

| Project | Description | Period | Mode | Progress |
|:--------|:------------|:-------|:-----|:---------|
| [<project-name>](./<project-name>/progress/MASTER.md) | One-line description | YYYY-MM-DD — YYYY-MM-DD | LOCAL_ONLY | Complete |
```

When updating this file, append new rows to the table. Do not remove existing entries.

---

## Archive Directory Structure

```text
docs/archives/<project-name>/
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
│   ├── phase-1-<short-name>.md
│   └── ...
└── governance/
    ├── instruction-surfaces.md
    ├── AGENTS.md              # if resolved and file-backed
    └── memory-surface.md      # export note or fallback snapshot, if available
```

Archive governance surfaces as snapshots or export notes only. Keep active instruction and memory surfaces in place after archiving. If memory is native and cannot be exported, record its platform/name and the key decisions that were written there.
