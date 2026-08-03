# Go kit probes

These five deterministic consumer-like probes are the initial observable
acceptance suite required by the Go Agent Kit charter:

- `cli-minimal` — parse explicit arguments and observe the resulting config;
- `rest-chi` — send a real in-process HTTP request and inspect status/body;
- `sqlite-sqlc` — write and read a row in a temporary local database;
- `worker-shutdown` — observe bounded work cancellation and graceful shutdown.
- `offline` — resolve pinned source content and local Go toolchain docs without network.

Each probe must run without an LLM or network service and exit non-zero on a
failed expectation. Raw command output belongs in the consuming project's evidence directory;
this standalone product does not ship metaproject evidence. The suite does not claim coverage for
Wails, interactive TUI behavior, or Pi discovery.
