/**
 * Kit Onboarding — tiny project-local extension that shows a GOAK banner
 * at the start of the conversation.
 *
 * PURPOSE: after a fresh install (or a /reload) the user immediately sees
 * three entries: Get Started, new large feature, new small feature — the
 * minimal orientation to start working. It is NOT documentation: it only
 * points; the full guide is `.pi/docs/GOAK.md`, reachable via `/goak-help`.
 *
 * BEHAVIOR:
 * - Fires on `session_start` with reason "startup" or "reload" only.
 * - Appends ONE chat-transcript entry (`.pi/onboarding/banner.md` content)
 *   via `pi.appendEntry` + `pi.registerEntryRenderer`. It is NOT a fixed
 *   widget: it is the first message of the conversation, so it scrolls up
 *   naturally as the user talks. It does not participate in LLM context
 *   (custom entries never do).
 * - Idempotent: if the entry already exists in the session (a /reload of
 *   the same session, or reopening the same session), nothing is appended —
 *   no duplicate banners.
 * - Silent no-op when the banner file is missing (broken install) or when
 *   there is no UI (`ctx.hasUI` is false headless) — no crash, no log spam.
 *
 * Constraints honored: no network, no background process, no state beyond
 * the session itself, no logic beyond reading a file and appending once.
 * Content stays out of code: the displayed text is the data file, which
 * `kit audit` and the product validator can check.
 */

/// <reference lib="es2022" />
/// <reference path="./types/pi-env.d.ts" />

import { readFileSync } from "node:fs";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Box, Text } from "@earendil-works/pi-tui";

const BANNER_URL = new URL("../onboarding/banner.md", import.meta.url);
const ENTRY_TYPE = "goak-onboarding";
const SHOW_REASONS = new Set(["startup", "reload"]);

function readBannerLines(): string[] | undefined {
	try {
		return readFileSync(BANNER_URL, "utf-8")
			.split(/\r?\n/)
			.map((line) => line.trimEnd())
			.filter((line) => line.length > 0);
	} catch {
		return undefined; // banner file missing — degraded install, stay silent
	}
}

function bannerAlreadyShown(ctx: {
	sessionManager: {
		getBranch(): Array<{ type: string; customType?: string }>;
	};
}): boolean {
	return ctx.sessionManager
		.getBranch()
		.some(
			(entry) => entry.type === "custom" && entry.customType === ENTRY_TYPE,
		);
}

export default function (pi: ExtensionAPI) {
	pi.registerEntryRenderer(ENTRY_TYPE, (entry, _options, theme) => {
		const lines = (entry.data as { lines?: string[] } | undefined)?.lines ?? [];
		const box = new Box(1, 1, (text) => theme.bg("customMessageBg", text));
		for (const line of lines) {
			box.addChild(new Text(line, 0, 0));
		}
		return box;
	});

	pi.on("session_start", (event, ctx) => {
		if (!ctx.hasUI || !SHOW_REASONS.has(event.reason)) return;
		if (bannerAlreadyShown(ctx)) return; // same session reloaded — no duplicate
		const lines = readBannerLines();
		if (!lines) return;
		pi.appendEntry(ENTRY_TYPE, { lines });
	});
}
