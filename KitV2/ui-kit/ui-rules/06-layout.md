# 06 — Layout

## Rule

1. Desktop shell layout: **sidebar (leading edge, collapsible) + content area**, with the
   toolbar/header inside the content area (Apple HIG §4 Sidebars, §3 Toolbars). Use the
   base `Sidebar` + `SidebarProvider` (or `ui-sdk/blocks/blocks-so` sidebar variants).
2. Every window/panel is **resizable with sensible minimums** (e.g. ≥800×600 for a main
   window, ≥400×300 for panels) (Apple HIG Rule 2.1); remember window state (size, position,
   last view) across sessions (Rule 2.5).
3. Use responsive breakpoints so the same screen degrades gracefully: content reflows,
   sidebar collapses to overlay on narrow windows; never horizontal scroll on the main view.
4. One primary action per view, visually dominant (primary button), positioned in the
   toolbar or the view's bottom-right (macOS convention); secondary actions as
   `variant="outline"`/`ghost`.
5. Empty states are designed, not an afterthought: use the base `Empty` component with a
   clear next action.

## Source

- Apple HIG — Windows, Toolbars, Sidebars, via skill `macos-design-guidelines` §2, §3, §4.
- WCAG 2.2 / responsive best practices via skill `web-platform-guidelines` §2
  (Responsive Design).
- shadcn/ui `Sidebar`, `Empty` components — frozen base.

## Example

```tsx
// ✅ desktop shell: sidebar + content
<SidebarProvider>
  <AppSidebar />           {/* leading edge, collapsible */}
  <main className="flex-1 overflow-auto p-5">
    <ScreenContent />
  </main>
</SidebarProvider>
```

```tsx
// ✅ empty state with action
<Empty title="No projects yet" description="Create your first project to get started.">
  <Button>New project</Button>
</Empty>
```
