---
name: go-code-review
category: workflow
tags: [review, code-review, diff, evidence, verification]
last-verified: 2026-08-05
description: "Review a Go diff for correctness, regressions, maintainability, and evidence quality. Use before merging or handing off non-trivial Go changes, especially when a fresh-context reviewer should challenge the implementer's assumptions; do not use it as an automatic approval. Supports three targets: uncommitted changes (default), commits in a date range (default last 3 days), and a branch compared to the main branch or an explicit base."
---

# Go code review

Review the actual diff and repository behavior. Do not review a worker's summary
instead of the files.

## Target modes (mutually exclusive)

Trois cibles, résolues dans cet ordre de priorité : `branch` spécifié → mode
branche ; sinon `since`/`until` → mode plage de commits ; sinon mode
non-commité. `base` ne s'applique qu'au mode branche. Demandes vagues
("review this") → mode non-commité ; "recent commits" sans dates → 3 derniers
jours.

1. **Mode non-commité** (défaut) — working tree + changements stagés.
2. **Mode plage de commits** — commits dans une plage de dates ; pas de plage
   explicite → 3 derniers jours.
3. **Mode branche / PR** — branche vs `origin/main`, `origin/master`, la
   branche par défaut du remote, ou une `base` explicite.

Collecte le contexte du diff avec git uniquement (ne juge jamais depuis un
résumé) :

```sh
git status --short
git diff --stat && git diff          # non-commité
git log --since "3 days ago" --oneline && git diff HEAD~N  # plage de commits
git diff origin/main...HEAD         # mode branche
```

S'il n'y a aucun changement, arrête-toi et dis qu'il n'y a rien à revoir.
N'invente pas de findings.

## Review planning by size

- **Small** (≤ 3 files, diff localisé) : couvrir Correctness + Tests.
- **Medium** (plusieurs fichiers / comportement affecté) : ajouter
  Regression/Compatibility.
- **Large ou à haut risque** (changements larges, auth/permissions,
  persistance, migrations, concurrence, cache, argent, sécurité, APIs
  publiques, code généré, config/déploiement) : ajouter Security/Data Safety +
  Performance/Concurrency.

Priorise le code de comportement, les contrats publics, la gestion de données,
les chemins d'erreur, la configuration, la persistance, les tests. Dépriorise
la documentation, les changements de formatage uniquement, les fichiers
générés, le churn de lockfile sauf s'ils affectent le comportement runtime.

## Focused reviewer dimensions

Quand des sous-agents sont disponibles (ou séquentiellement sinon), répartis
la revue en reviewers focalisés — un focus par sous-agent :

- Correctness / Bug Risk
- Regression / Compatibility
- Tests / Verification
- Security / Data Safety
- Performance / Concurrency

Chaque reviewer renvoie uniquement des findings candidats étayés par des
preuves pour son propre focus. Contrat complet : `references/reviewer-focus.md`.

## Procedure

1. Read project rules, the approved plan or request, and the complete diff.
   Identify the intended behavior, public contracts, trust boundaries, and
   affected callers/tests.
2. Run the cheapest relevant mechanical checks first: formatting, `go vet`,
   focused tests, and the repository's configured lint/security checks.
3. Read changed files end to end and inspect each finding in context. Check
   error flow, cancellation, goroutine termination, resource cleanup, API
   compatibility, input validation, package ownership, tests, and documentation.
4. Report findings with severity, exact file/line, violated contract or source,
   impact, and the smallest safe fix. Use `references/finding-template.md`.
   Findings-first : présente les findings avant tout résumé ; ne jamais enterrer
   un bug sous un résumé. Pas de findings → dis explicitement `No findings` et
   liste les risques résiduels ou lacunes de test.
5. Reread every finding against the current source. Remove anything that cannot
   be justified by a concrete failure, contract, or primary source.
6. Separate blockers from optional suggestions. Do not edit the worktree unless
   the parent explicitly assigns a writer pass.

## Verdicts

- `PASS`: no blocking or worthwhile correctness findings and required evidence
  is present.
- `PARTIAL`: no known blocker, but required behavior or validation evidence is
  missing.
- `FAIL`: a concrete blocker or regression is present.
- `BLOCKED`: the review cannot run because required files/tools are unavailable.

## References

- [Review checklist](references/review-checklist.md)
- [Finding template](references/finding-template.md)
- [Review output template](assets/review-template.md)
- [Focused reviewer dimensions](references/reviewer-focus.md)
