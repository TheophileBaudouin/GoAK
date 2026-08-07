# Go kit probes

Probes are the Kit's **executable product evaluations** (charter, Layer 6):
deterministic scenarios, LLM-free and external-service-free, that prove the
Kit does what it claims. Each probe ends with an observable verdict and an
exit code.

## Inventory (16 probes)

| Probe | Recipe / capability exercised | Observable scenario |
| --- | --- | --- |
| `auth-jwt` | recipe-auth-jwt | HS256 Bearer emission and verification, rejection of invalid tokens. |
| `auth-session` | recipe-auth-session-scs | Signed session creation and reading, expiration. |
| `cli-cobra` | recipe-cli-cobra | Cobra subcommands, flag parsing, expected outputs. |
| `cli-interactive` | recipe-cli-interactive | Bubble Tea model: state, events, clean shutdown. |
| `cli-minimal` | recipe-cli-minimal | Explicit argument parsing → observed config. |
| `config-koanf` | recipe-config-koanf | Config loading, merging, input validation. |
| `config-viper` | recipe-config-viper | Config loading, merging, input validation. |
| `desktop-app` | recipe-desktop-app | Wails application-layer boundary: service/model borders. |
| `graceful-shutdown` | recipe-graceful-shutdown | Clean shutdown on signal, worker drain. |
| `observability` | recipe-observability-slog-expvar | Structured slog + expvar metrics observed. |
| `offline` | tools/offline | Offline resolution of pinned sources and the local toolchain. |
| `openapi-validation` | recipe-openapi-validation | Request/response validation against the OpenAPI contract. |
| `rest-chi` | recipe-rest-chi | In-process HTTP request, status and body verified. |
| `sqlite-sqlc` | recipe-sqlite-sqlc | Write/read of one row in a local temporary database. |
| `ui-kit-sync` | tools/sync-ui-kit.sh | Wails-only materialize/idempotence, structure evolution, ownership refusal. |
| `worker-pool` | recipe-worker-pool | Valid bounded batch + cancellation on first error. |

## Rules

1. **Composition, not duplication**: a probe imports the recipe it exercises
   (`go-agent-kit-v2/recipes/...`) or the product capability
   (`go-agent-kit-v2/tools/offline`).
2. **Determinism**: no external network, no flaky timing, no shared state
   between executions; local resources (ephemeral port, temporary database)
   are cleaned up.
3. **Explicit verdict**: the last output line is `…: PASS` (or a clear
   failure + non-zero exit code); a probe that asserts nothing is an error.
4. **Automatic discovery**: `run.sh` discovers probes by glob
   (`probes/*/main.go`) — a hardcoded list is forbidden.
5. Raw outputs belong to the consumer's own evidence area, never to the
   product.

## Adding a probe

A probe is added when a **core recipe** or a **product capability** has an
observable behavior to prove (Z6 §3.4: every new core recipe is a candidate).

1. Create `probes/<subject>/main.go` — self-contained, `package main`,
   `PASS` verdict + exit code.
2. Import the exercised recipe; never copy its code.
3. Run `bash probes/run.sh` and verify `probes/<subject>: PASS`.
4. Update this README (inventory); the full gate must stay green.

## Known limits

The suite does not cover: individual Pi skill discovery, TUI rendering in a
real terminal, nor the Wails GUI webview — these limits stay declared in
`capabilities.yaml` (`known_limits`) and are never presented as covered by a
probe.
