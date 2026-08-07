import { useEffect, useState } from "react";

import SettingsPreferences, {
	type PreferencesData,
} from "@/components/hextaui/settings-preferences";
import SettingsNotifications from "@/components/hextaui/settings-notifications";
import SettingsSecurity from "@/components/hextaui/settings-security";
import { CommandMenu02 } from "@/components/command-menu-02";
import {
	SidebarProvider,
	Sidebar,
	SidebarHeader,
	SidebarContent,
	SidebarMenu,
	SidebarMenuItem,
	SidebarMenuButton,
	SidebarInset,
	SidebarTrigger,
} from "@/components/ui/sidebar";
import { Settings2Icon, BellIcon, ShieldCheckIcon } from "lucide-react";

/**
 * Example screen — Preferences (desktop, Wails-ready).
 *
 * Exercises the kit: frozen-base Sidebar + harvested hextaui settings pieces +
 * a blocks-so command menu, laid out per ui-rules/ (spacing 8/20px, semantic
 * tokens, keyboard-first). Category switching is internal state; real app
 * navigation between screens must use HashRouter (ui-rules/09-desktop.md).
 *
 * Keyboard: Cmd+1/2/3 switch category, Cmd+K opens the command menu (registered
 * once per ui-rules/08-keyboard.md — in a real app this goes in ux/shortcuts.md).
 */

type Category = "general" | "notifications" | "security";

const CATEGORIES: { id: Category; label: string; icon: typeof BellIcon }[] = [
	{ id: "general", label: "General", icon: Settings2Icon },
	{ id: "notifications", label: "Notifications", icon: BellIcon },
	{ id: "security", label: "Security", icon: ShieldCheckIcon },
];

const INITIAL_PREFERENCES: PreferencesData = {
	theme: "system",
	fontSize: "medium",
	language: "en",
	timezone: "Europe/Paris",
	dateFormat: "YYYY-MM-DD",
	timeFormat: "24h",
	numberFormat: "en-US",
	density: "comfortable",
	animations: true,
	reducedMotion: false,
	highContrast: false,
	screenReaderAnnouncements: true,
	keyboardShortcuts: true,
};

export function PreferencesScreen() {
	const [category, setCategory] = useState<Category>("general");
	const [preferences, setPreferences] =
		useState<PreferencesData>(INITIAL_PREFERENCES);

	// ui-rules/08-keyboard.md: Cmd+1/2/3 switches category (registered once).
	const switchCategory = (id: Category) => {
		setCategory(id);
		// focus the panel so keyboard users land in the content
		document.getElementById("preferences-panel")?.focus();
	};

	// ui-rules/08-keyboard.md: Cmd+1/2/3 switches category (registered once).
	useEffect(() => {
		const onKey = (e: KeyboardEvent) => {
			if (!e.metaKey || e.altKey || e.ctrlKey) return;
			const idx = Number(e.key);
			if (idx >= 1 && idx <= CATEGORIES.length) {
				e.preventDefault();
				switchCategory(CATEGORIES[idx - 1].id);
			}
		};
		window.addEventListener("keydown", onKey);
		return () => window.removeEventListener("keydown", onKey);
	}, []);

	return (
		<SidebarProvider>
			<Sidebar>
				<SidebarHeader>
					<div className="px-2 py-1">
						<h1 className="text-sm font-semibold">Preferences</h1>
						<p className="text-xs text-muted-foreground">ui-dev-kit example</p>
					</div>
				</SidebarHeader>
				<SidebarContent>
					<SidebarMenu>
						{CATEGORIES.map(({ id, label, icon: Icon }) => (
							<SidebarMenuItem key={id}>
								<SidebarMenuButton
									isActive={category === id}
									onClick={() => switchCategory(id)}
									aria-current={category === id ? "page" : undefined}
								>
									<Icon data-icon="inline-start" />
									<span>{label}</span>
								</SidebarMenuButton>
							</SidebarMenuItem>
						))}
					</SidebarMenu>
				</SidebarContent>
			</Sidebar>

			<SidebarInset>
				<header className="flex h-12 items-center justify-between gap-2 border-b px-5">
					<div className="flex items-center gap-2">
						<SidebarTrigger aria-label="Toggle sidebar" />
						<h2 className="text-sm font-medium">
							{CATEGORIES.find((c) => c.id === category)?.label}
						</h2>
					</div>
					<CommandMenu02 />
				</header>

				<main
					id="preferences-panel"
					tabIndex={-1}
					className="flex-1 space-y-5 overflow-auto p-5 outline-none"
				>
					{category === "general" && (
						<SettingsPreferences
							preferences={preferences}
							onSave={async (data) => setPreferences(data)}
						/>
					)}
					{category === "notifications" && <SettingsNotifications />}
					{category === "security" && <SettingsSecurity />}
				</main>
			</SidebarInset>
		</SidebarProvider>
	);
}
