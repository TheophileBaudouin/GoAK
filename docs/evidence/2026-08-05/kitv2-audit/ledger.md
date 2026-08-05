# Ledger KitV2 — 398 chemins (audit 2026-08-05)

Colonnes : chemin | rôle/kind | placement | C charte | T type/zone | M métadonnées | S sources/fraîcheur | V validation | D SSOT/dup | I indépendance | L langue | R code/règles | confiance | risque | verdict global

## Zone (racine)

| .DS_Store | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| .gitignore | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✗ (.DS_Store non ignoré) | ✓ | N/A | ÉLEVÉE | FAIBLE | NON CONFORME (hygiène) |
| .golangci.yml | yaml | KIT | ✓ | ✓ | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (config) |

## Zone .pi

| .pi/extensions/kit-resource-router.ts | ts | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (lecture seule vérifiée) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (extension Pi Z11 §3.2) |
| .pi/extensions/tsconfig.json | json | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| .pi/extensions/types/pi-env.d.ts | ts | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (lecture seule vérifiée) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (extension Pi Z11 §3.2) |
| .pi/prompts/checklist-api.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/checklist-release.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-clarify.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-implement.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-memory.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-plan.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-tasks.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/prompts/workflow-verify.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (prompt Z8) |
| .pi/settings.json | json | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| .pi/skills/go-code-review/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |
| .pi/skills/go-code-review/assets/review-template.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-code-review/references/finding-template.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-code-review/references/review-checklist.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-idiomatic-implementation/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |
| .pi/skills/go-idiomatic-implementation/references/modern-go-boundaries.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-idiomatic-implementation/references/official-go.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-implementation-plan/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |
| .pi/skills/go-implementation-plan/references/plan-artifact.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-implementation-plan/references/source-ledger.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-source-retrieval/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |
| .pi/skills/go-source-retrieval/references/retrieval-contract.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-testing-verification/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |
| .pi/skills/go-testing-verification/references/evidence-record.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/go-testing-verification/references/test-strategy.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (L3, liens vérifiés) |
| .pi/skills/kit-resource-routing/SKILL.md | md (workflow) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (skill workflow Z8) |

## Zone (racine)

| AGENTS.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| capabilities.yaml | yaml | KIT | ✓ | ✓ | ✓ (C1) | ✗ (coverage en dur, C1 §3.3) | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (comptes non dérivés) |
| go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| go.sum | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |

## Zone knowledge

| knowledge/INDEX.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME (doc de zone) |
| knowledge/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME (doc de zone) |
| knowledge/anti-patterns/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/anti-patterns/api-no-pagination.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/arch-big-ball-of-mud.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/arch-bloater.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/arch-distributed-monolith.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/arch-god-object.yaml | yaml | KIT | ✓ | ✓ | ✗ (URL morte) | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (Z2 §9.2 URL vivante) |
| knowledge/anti-patterns/arch-nano-services.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/arch-shared-database.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/cache-stale.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/cache-stampede.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/cfg-hardcoded-values.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/cli-flag-and-convention-abuse.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-codegen-dynamic-queries.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-eav.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-function-on-column.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-n-plus-one.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-placeholder-cache-injection.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-pool-misconfig.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-raw-transactions.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/db-select-star.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-context-key-collision.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-context-unused.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-error-string-matching.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-goroutine-leak.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-ignored-error.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-init-misuse.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-interface-everywhere.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-json-omitempty-zero.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-loop-variable-capture.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-mutable-global-state.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-over-structuring.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-panic-as-error.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-shadowing.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/go-string-concat-loop.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/http-no-timeouts.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/msg-offset-commit-misorder.yaml | yaml | KIT | ✓ | ✓ | ✗ (URL morte) | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (Z2 §9.2 URL vivante) |
| knowledge/anti-patterns/msg-poison-pill-no-dlq.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/msg-retry-storm.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/obs-excessive-logging.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/obs-logging-not-observability.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/rest-ignoring-http-semantics.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/rest-tunneling.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-cswsh.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-error-information-leak.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-fail-open.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-hardcoded-credentials.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-ip-trust.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-missing-csrf.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-no-threat-modeling.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-ssh-host-key-reuse.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/sec-unsanitized-rendering.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/test-brittle-tests.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/test-implementation-details.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/anti-patterns/test-over-mocking.yaml | yaml | KIT | ✓ | ✓ | ✗ (URL morte) | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (Z2 §9.2 URL vivante) |
| knowledge/anti-patterns/test-sleep-based.yaml | yaml | KIT | ✓ | ✓ | ✗ (URL morte) | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (Z2 §9.2 URL vivante) |
| knowledge/architecture/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/architecture/bootstrap-cli-runtime.yaml | yaml | AMBIGU | ✗ | ✗ | ✓ | ✓ | N/A | ✓ | ✗ | ✓ | N/A | MOYENNE | MOYEN | À VÉRIFIER (placement + statut proposé) |
| knowledge/architecture/embedded-kv.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/architecture/mcp-server-shape.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/awesome-go.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/cookiecutter.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/github-code-search.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/go-by-example.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/go-cookbook.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/catalogs/libraries/age/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/air.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/amqp091-go.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/bbolt/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/bleve/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/bubbles/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/bubbletea/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/certmagic/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/chi/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/cobra/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/coder-websocket/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/colorprofile/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/compress/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/echo.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/fiber.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/franz-go-kafka.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/fyne/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/gin.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/glamour/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/go-blueprint.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/go-git/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/golang-jwt/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/golang-migrate.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/goldmark/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/google-uuid.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/gorm.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/harmonica/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/huh/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/keygen/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/kin-openapi/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/koanf/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/lipgloss/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/log/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/mcp-go-sdk/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/minio-go/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/mockery.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/modernc-sqlite/SKILL.md | md (library) | KIT | ✓ | ✓ | ✗ (URL morte) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | MOYEN | NON CONFORME (URL morte, N1 §4) |
| knowledge/catalogs/libraries/nats.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/ollama-go.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/openai-go.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/pgx/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/pointers/adk-go.yaml | yaml | AMBIGU | ✓ | ✗ (proposé indexé, Z10 §5.3 vs Z11) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (pointeur proposé livré+indexé) |
| knowledge/catalogs/libraries/pointers/eino.yaml | yaml | AMBIGU | ✓ | ✗ (proposé indexé, Z10 §5.3 vs Z11) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (pointeur proposé livré+indexé) |
| knowledge/catalogs/libraries/pointers/playwright-go.yaml | yaml | AMBIGU | ✓ | ✗ (proposé indexé, Z10 §5.3 vs Z11) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (pointeur proposé livré+indexé) |
| knowledge/catalogs/libraries/pointers/sqlite-vec.yaml | yaml | AMBIGU | ✓ | ✗ (proposé indexé, Z10 §5.3 vs Z11) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (pointeur proposé livré+indexé) |
| knowledge/catalogs/libraries/pointers/tree-sitter.yaml | yaml | AMBIGU | ✓ | ✗ (proposé indexé, Z10 §5.3 vs Z11) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | À VÉRIFIER (pointeur proposé livré+indexé) |
| knowledge/catalogs/libraries/prometheus-client.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/redis.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/req/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/resty.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/ristretto/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/scs/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/sequin/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/sqlc/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/sqlx.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/ssh/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/templ/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/testcontainers-go/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/testify/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/uber-go-mock.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/validator/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/viper/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/wish/SKILL.md | md (library) | KIT | ✓ | ✓ | ✓ (structure+date) | ✓ | ✓ (strict gate PASS) | ✓ | ✓ | ✓ | ✓ | MOYENNE | — | CONFORME (fiche N1 §4) |
| knowledge/catalogs/libraries/zap.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/libraries/zerolog.yaml | yaml | AMBIGU | ✓ | ✗ (format YAML dans zone SKILL.md, N1 §2/Z2 §2) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (mélange de formats non contractualisé) |
| knowledge/catalogs/reference-projects/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/catalogs/reference-projects/ardanlabs-service/SKILL.md | md (reference-project) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | À VÉRIFIER (revue fiche extract-only) |
| knowledge/catalogs/reference-projects/go-starter/SKILL.md | md (reference-project) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | À VÉRIFIER (revue fiche extract-only) |
| knowledge/catalogs/reference-projects/pagoda/SKILL.md | md (reference-project) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | À VÉRIFIER (revue fiche extract-only) |
| knowledge/catalogs/sourcegraph.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/debugging/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/debugging/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | FAIBLE | CONFORME (doc de zone; mention docs/evidence = note) |
| knowledge/observability/otel-go.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/observability/ssh-metrics.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/patterns/architecture-modular-monolith.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/architecture-ports-adapters.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/auth-session-vs-jwt.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/cache-stale-while-revalidate.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/cli-subcommands-conventions.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/concurrency-pipeline.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/concurrency-singleflight.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/concurrency-worker-pool.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/config-twelve-factor-config.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/database-pool-config.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/database-query-batching.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/database-transaction-boundary.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/database-versioned-migrations.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-concrete-returns.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-constructor-injection.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-contextual-worker.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-error-wrapping-chain.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-minimal-layout.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-private-context-keys.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-sentinel-errors.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/go-string-builder.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/http-api-idempotency-keys.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/http-middleware-chain.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/http-rest-cursor-pagination.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/http-rest-resource-modeling.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/messaging-dead-letter-queue.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/messaging-idempotent-consumer.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/messaging-transactional-outbox.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/observability-correlation-ids.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/observability-structured-logging.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/resilience-circuit-breaker.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/resilience-retry-backoff-jitter.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/resilience-timeout-deadlines.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/security-fail-closed-auth.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/security-secrets-management.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/testing-fakes-over-mocks.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/testing-httptest.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/testing-seam-injection.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/patterns/testing-table-driven.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/performance/compression-selection.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/performance/go-profiling.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/performance/search-index-merge.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/performance/template-compiled-rendering.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/file-encryption.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/go-security-best-practices.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/go-vulnerability-database.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/input-validation.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/mcp-tool-security.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/ssh-key-generation.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/ssh-server-security.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/security/websocket-security.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| knowledge/stdlib/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| knowledge/stdlib/effective-go-offline.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-ast.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-command.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-context.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-database-sql.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-errors.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-fuzzing.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-html-template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| knowledge/stdlib/go-language-specification.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-modules.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-net-http.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-race-detector.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-release-policy.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-slog.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-sync.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-testing.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/go-toolchains.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/offline-package-lookup.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/offline-source-retrieval.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/pkg-doc-offline.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/toolchain-offline.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/x-crypto.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| knowledge/stdlib/x-oauth2.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |

## Zone (racine)

| manifest.yaml | yaml | KIT | ✓ | ✓ | ✓ (C1) | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (C1) |

## Zone probes

| probes/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| probes/cli-minimal/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (exécutée 5/5 PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (probe Z6) |
| probes/offline/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (exécutée 5/5 PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (probe Z6) |
| probes/rest-chi/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (exécutée 5/5 PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (probe Z6) |
| probes/run.sh | sh | KIT | ✗ | ✗ (liste en dur, Z6 §2/C2 §2) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | ÉLEVÉ | NON CONFORME (découverte probe en dur) |
| probes/sqlite-sqlc/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (exécutée 5/5 PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (probe Z6) |
| probes/worker-shutdown/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (exécutée 5/5 PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (probe Z6) |

## Zone recipes

| recipes/.DS_Store | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| recipes/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/add-authentication/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/add-database/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/add-observability/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/create-grpc-service/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/create-rest-api/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/deploy-container/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| recipes/recipe-cli-cobra/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-cli-cobra/cobra.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-cli-cobra/cobra_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-cli-interactif/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-cli-interactif/tui.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-cli-interactif/tui_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-cli-minimal/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✗ (last_verified 370 j > 12 mois) | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | MOYEN | À VÉRIFIER (fraîcheur 12 mois dépassée, C0 §5) |
| recipes/recipe-cli-minimal/cli.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-cli-minimal/cli_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-config-koanf/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-config-koanf/koanf.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-config-koanf/koanf_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-config-viper/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-config-viper/viper.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-config-viper/viper_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-desktop-app/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✗ (last_verified 370 j > 12 mois) | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | MOYEN | À VÉRIFIER (fraîcheur 12 mois dépassée, C0 §5) |
| recipes/recipe-desktop-app/app.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-desktop-app/app_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-graceful-shutdown/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✗ (last_verified 370 j > 12 mois) | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | MOYEN | À VÉRIFIER (fraîcheur 12 mois dépassée, C0 §5) |
| recipes/recipe-graceful-shutdown/shutdown.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-graceful-shutdown/shutdown_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-rest-chi/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-rest-chi/server.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-rest-chi/server_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-sqlite-sqlc/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (recette Z3) |
| recipes/recipe-sqlite-sqlc/query.sql | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| recipes/recipe-sqlite-sqlc/schema.sql | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| recipes/recipe-sqlite-sqlc/sqlc.yaml | yaml | KIT | ✓ | ✓ | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (config) |
| recipes/recipe-sqlite-sqlc/store.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-sqlite-sqlc/store_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-worker-pool/SKILL.md | md (recipe) | KIT | ✓ | ✓ | ✗ (last_verified 370 j > 12 mois) | ✓ | ✓ (tests+probes PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | MOYEN | À VÉRIFIER (fraîcheur 12 mois dépassée, C0 §5) |
| recipes/recipe-worker-pool/pool.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |
| recipes/recipe-worker-pool/pool_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests -race PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (code recette) |

## Zone router

| router/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| router/index.json | json | KIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| router/meta.json | json | KIT | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |

## Zone rules

| rules/.DS_Store | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| rules/core/.DS_Store | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| rules/core/concurrency/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| rules/core/concurrency/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/errors/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| rules/core/errors/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/philosophy/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| rules/core/philosophy/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/universal/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/validation/.DS_Store | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| rules/core/validation/golangci-lint/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/validation/gosec/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/core/validation/govulncheck/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| rules/registry/catalog-freshness/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/doc-comments/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/example-rule-consistency/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/logging/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/no-internal-duplication/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |
| rules/registry/testing/SKILL.md | md (rule) | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (règle Z1, gate verte) |

## Zone snippets

| snippets/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| snippets/bounded-worker/SNIPPET.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| snippets/bounded-worker/check.sh | sh | KIT | ✗ | ✗ (gofmt-only, Z4 §4.2) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ÉLEVÉE | ÉLEVÉ | NON CONFORME (check ni compile ni execute) |
| snippets/bounded-worker/example.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (compile) | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | CONFORME (compile) — voir finding check.sh |
| snippets/cli/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/cloud/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/concurrency/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/database/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/errors-once/SNIPPET.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| snippets/errors-once/check.sh | sh | KIT | ✗ | ✗ (gofmt-only, Z4 §4.2) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ÉLEVÉE | ÉLEVÉ | NON CONFORME (check ni compile ni execute) |
| snippets/errors-once/example.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (compile) | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | CONFORME (compile) — voir finding check.sh |
| snippets/http-json/SNIPPET.yaml | yaml | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (graphe, validateur PASS) |
| snippets/http-json/check.sh | sh | KIT | ✗ | ✗ (gofmt-only, Z4 §4.2) | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ | ÉLEVÉE | ÉLEVÉ | NON CONFORME (check ni compile ni execute) |
| snippets/http-json/example.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (compile) | ✓ | ✓ | ✓ | ? | MOYENNE | FAIBLE | CONFORME (compile) — voir finding check.sh |
| snippets/networking/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/security/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| snippets/testing/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |

## Zone templates

| templates/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| templates/TEMPLATES.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| templates/_kit-ci-workflow.yml | yaml | KIT | ✓ | ✓ | N/A | N/A | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (config) |
| templates/_kit-skill-authoring.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME (aide A1 produit) |
| templates/cli/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/cli/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/cli/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/cli/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/cli/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/cloud-service/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/cloud-service/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/cloud-service/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/cloud-service/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/cloud-service/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/grpc/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/grpc/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/grpc/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/grpc/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/grpc/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/microservice/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/microservice/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/microservice/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/microservice/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/microservice/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/monolith/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/monolith/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/monolith/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/monolith/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/monolith/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/rest-api/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/rest-api/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/rest-api/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/rest-api/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/rest-api/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |
| templates/template-contract.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (doc de zone) |
| templates/worker/README.md | md | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| templates/worker/go.mod | other | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (mod verify PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME |
| templates/worker/main.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/worker/main_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (build+test OK) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (scaffold legacy fonctionnel) |
| templates/worker/template.yaml | yaml | KIT | ✓ | ✗ (status "partial" hors vocabulaire Z5 §4; TEMPLATES.md dit legacy) | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (statut template incohérent) |

## Zone tools

| tools/generators/.gitkeep | other | KIT (livré) | ✗ | — | — | — | — | — | — | — | — | ÉLEVÉE | MOYEN | NON CONFORME (C0 §7/N1 §6 placeholder vide) |
| tools/offline/bundle/blobs/9c6259ceaec348deabfcef9856955070da5370f3a95cf739b4d9c06b22544e0d | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| tools/offline/bundle/index/effective-go.tsv | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| tools/offline/bundle/licenses/go-website.txt | other | KIT | ✓ | ✓ | ✓ | ✓ | N/A | ✓ | ✓ | ✓ | N/A | MOYENNE | — | CONFORME |
| tools/offline/bundle/manifest.json | json | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (checksums PASS) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | — | CONFORME (Z7) |
| tools/offline/excerpt.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/manifest.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/offline.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/offline_test.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/search.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/toolchain.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/offline/version.go | go | KIT | ✓ | ✓ | ✓ | ✓ | ✓ (tests PASS) | ✓ | ✓ | ✓ | ✓ | ÉLEVÉE | — | CONFORME (outil offline) |
| tools/validators/.ruff_cache/.gitignore | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| tools/validators/.ruff_cache/0.15.12/16970947614363446779 | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| tools/validators/.ruff_cache/CACHEDIR.TAG | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| tools/validators/__pycache__/validate-kitv2.cpython-310.pyc | other | EXCLU | — | — | — | — | — | — | — | — | — | ÉLEVÉE | FAIBLE | EXCLU (artefact machine) |
| tools/validators/validate-kitv2.py | py | KIT | ✓ | ✓ | ✓ | ✓ | ✗ (aucun test, C2 §3) | ✓ | ✓ | ✓ | N/A | ÉLEVÉE | MOYEN | NON CONFORME (C2 §3 exige tests) |
