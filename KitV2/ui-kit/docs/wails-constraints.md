# Wails interface constraints — research & guardrails

> Verified: August 6, 2026. Sources: official Wails v3 docs (v3.wails.io — live docs; the
> v2 wails.io pages 404'd and the site is restructured, v2 remains the current stable) +
> web research. Every statement below was verified during this session.

## The hard contract (non-negotiable for the SDK)

| Constraint | Detail | Source |
| --- | --- | --- |
| **Static build only** | The frontend MUST build to a static bundle in `frontend/dist/`. `main.go` embeds it with `//go:embed all:frontend/dist` and serves it from the asset server. **No SSR, no server, no Node runtime in production.** | v3.wails.io/guides/dev/frontend-frameworks (§How the frontend directory is used) |
| **Build is driven by the frontend's `build` script** | `wails3 build` runs the frontend `build` script; `wails3 dev` runs `dev` and proxies the Vite dev server. | same |
| **React routing = HashRouter** | Hash-based routing (`#/page`) avoids conflicts with the Wails runtime's internal routing, native window URL handling, and production assets served from non-root paths. React: `react-router-dom` `HashRouter`. Full-URL/history mode risks `ERR_FILE_NOT_FOUND` on reload. | v3.wails.io/guides/routing (React tab + "Why Hash Routing?") |
| **Vite `base: "./"`** | Required so asset paths resolve in the embedded context (relative paths, not root-absolute). | v3.wails.io/guides/routing (Troubleshooting) |
| **Dev server on a fixed port** | `wails3 dev` proxies Vite on `WAILS_VITE_PORT` (default **9245**): `server: { host: "127.0.0.1", port: Number(process.env.WAILS_VITE_PORT) ?? 9245, strictPort: true }`. No Wails Vite plugin is required for the basics. | v3.wails.io/guides/dev/frontend-frameworks (§Scaffold any framework) |
| **Go ↔ JS via generated bindings** | Wails inspects registered Go services and writes a type-safe SDK into `frontend/bindings/`; import it (`import { GreetService } from "./bindings/…"`). The runtime package is **`@wailsio/runtime`** (Events, Browser, dialogs, clipboard, menus, system, screens, window management). | v3.wails.io/guides/dev/frontend-frameworks + v3.wails.io/reference/frontend-runtime |
| **Typed events (optional)** | `@wailsio/runtime/plugins/vite` injects generated event-type definitions; `Events.Emit(TypedEvent({…}))` with autocomplete. | v3.wails.io/reference/frontend-runtime (Vite Plugin for Typed Events) |
| **Wails version status** | **v2 = current stable** (still receiving fixes). **v3 = beta** (desktop API described as stable and in production by some teams — test thoroughly before deploying). v3 is a significant port, not a simple upgrade. | wailsapp/wails releases + v3 beta blog post |

## Implications for ui-agent-kit

1. **Components must be static-only**: no SSR-only APIs, no `next/*` imports (already the case —
   Next-specific blocks were excluded at integration), no assumption of a server. `window` /
   `document` at module scope are fine (the webview is a real browser context).
2. **Navigation in SDK apps must use hash-based routing** (`HashRouter`) — this is a
   constraint for any screen pattern that mentions routing (`ux/user-flows.md`,
   `ux/navigation.md` use "routes"; the app layer must map them to HashRouter routes).
3. **The app shell (Wails) is the integration boundary**: window management, dialogs,
   native menus, system info go through `@wailsio/runtime` / generated Go bindings — SDK
   components must NOT re-implement them; they receive data/actions via props (declared
   interface, per the constitution).
4. **Asset paths**: consumed pieces keep relative imports; the consuming Vite config adds
   `base: "./"`.
5. **Dev parity**: the reference workspace must run with the Wails dev-server config so
   `wails3 dev` hot-reload works (port 9245, strictPort).

## What this changed in the project

- `ui-rules/09-desktop.md`: added a Wails section (static-only, hash routing, bindings
  boundary).
- `ui-sdk/docs/CONSUMPTION.md`: added the Wails integration contract.
- `AGENTS.md`: added the Wails static constraint to the absolute rules + a reference.
- `ui-workspace/vite.config.ts`: adapted to Wails (`base: "./"` + dev-server port config),
  build re-verified green.

## Sources (all fetched this session)

- <https://v3.wails.io/guides/routing/> — React HashRouter recommendation + troubleshooting
- <https://v3.wails.io/guides/dev/frontend-frameworks/> — static dist contract, dev port, bindings
- <https://v3.wails.io/reference/frontend-runtime/> — @wailsio/runtime API, typed events plugin
- <https://github.com/wailsapp/wails/releases> + v3 beta blog — version status
- Web search: routing guidance, Vite base path, community reports (ERR_FILE_NOT_FOUND)
