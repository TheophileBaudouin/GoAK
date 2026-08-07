# 02 — Colors

## Rule

1. Use only the semantic color tokens of the frozen base (`bg-background`, `text-foreground`,
   `bg-primary`, `text-muted-foreground`, `border-border`, `bg-destructive`, …). Never
   hardcode hex values in components.
2. Support **dark mode** through the tokens (CSS variables in `src/index.css`) — a component
   is written once and renders in both schemes (Apple HIG Rule 9.4: support Dark Mode).
3. Respect the system accent color where the platform exposes it (macOS: `AccentColor`) for
   selection and highlight; do not define a brand accent that fights the system
   (Apple HIG Rule 9.3).
4. Do not use color as the **only** information carrier (WCAG 1.4.1): pairs with text, icons
   or patterns (e.g. a status dot must also have a label).
5. On macOS, prefer solid backgrounds over heavy translucency, and fall back to solid when
   Reduce Transparency is enabled (Apple HIG Rule 9.5, Rule 11.4).

## Source

- Apple HIG — Color & Dark Mode, via skill `macos-design-guidelines` §9.3–9.5, §11.4.
- WCAG 2.2 — 1.4.1 Use of Color, via skill `web-platform-guidelines` §1.
- shadcn/ui theming (semantic CSS variables, OKLCH) — frozen base.

## Example

```tsx
// ✅ semantic tokens + dark mode for free
<Badge className="bg-destructive text-destructive-foreground">Failed</Badge>

// ❌ hardcoded hex — breaks dark mode and theming
<Badge style={{ background: "#dc2626" }}>Failed</Badge>
```

```tsx
// ✅ status not conveyed by color alone
<span className="inline-flex items-center gap-2">
  <span className="size-2 rounded-full bg-emerald-500" aria-hidden="true" />
  Online
</span>
```
