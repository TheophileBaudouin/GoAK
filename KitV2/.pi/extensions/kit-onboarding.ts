/**
 * Kit Onboarding — tiny project-local extension that shows a GOAK banner
 * widget at session start.
 *
 * PURPOSE: after a fresh install (or a /reload) the user immediately sees
 * three entries: Get Started, new large feature, new small feature — the
 * minimal orientation to start working. It is NOT documentation: it only
 * points; the full guide is `.pi/docs/GOAK.md`, reachable via `/goak`.
 *
 * BEHAVIOR:
 * - Fires on `session_start` with reason "startup" or "reload" only
 *   (a fresh install or a reload — never on every new/resumed session).
 * - Renders `.pi/onboarding/banner.md` as a TUI widget above the editor
 *   (`ctx.ui.setWidget`), idempotent per key.
 * - Silent no-op when the banner file is missing (broken install) or when
 *   there is no UI (`ctx.hasUI` is false headless) — no crash, no log spam.
 *
 * Constraints honored: no network, no background process, no state, no
 * logic beyond reading a file and rendering lines. Content stays out of
 * code: the displayed text is the data file, which `kit audit` and the
 * product validator can check.
 */

/// <reference lib="es2022" />
/// <reference path="./types/pi-env.d.ts" />

import { readFileSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

const BANNER_URL = new URL("../onboarding/banner.md", import.meta.url);
const WIDGET_KEY = "goak-onboarding";
const SHOW_REASONS = new Set(["startup", "reload"]);

export default function (pi: ExtensionAPI) {
	pi.on("session_start", (event, ctx) => {
		if (!ctx.hasUI || !SHOW_REASONS.has(event.reason)) return;
		let lines: string[];
		try {
			lines = readFileSync(BANNER_URL, "utf-8").split(/\r?\n/);
		} catch {
			return; // banner file missing — degraded install, stay silent
		}
		ctx.ui.setWidget(
			WIDGET_KEY,
			lines.map((line) => line.trimEnd()).filter((line) => line.length > 0),
		);
	});
}
