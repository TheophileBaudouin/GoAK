# 03 — Typography

## Rule

1. Use the preset's type scale via Tailwind utilities (`text-sm`, `text-lg`, `font-semibold`…)
   and the heading scale (`text-2xl` for screen titles). Never set arbitrary font sizes.
2. Use the project font stack (Geist in the frozen-base preset) for UI text; keep a system
   fallback stack. Mono for code/data (`font-mono`) (Apple HIG Rule 9.1: use system fonts).
3. Prefer relative units where sizing matters (Tailwind rem-based scale already does this) so
   the interface respects the user's font-size preference (WCAG 1.4.4 Resize text).
4. Minimum UI text size: `text-sm` (14px) for body controls; do not go below `text-xs` (12px)
   for labels/captions, and only for non-essential content.
5. Use `tabular-nums` for numeric columns and data displays so digits don't jitter when
   values change (Vercel Web Interface Guidelines).

## Source

- Apple HIG — Typography, via skill `macos-design-guidelines` §9.1.
- WCAG 2.2 — 1.4.4 Resize Text, via skill `web-platform-guidelines` §1 and §4 (font stacks,
  relative units).
- Vercel Web Interface Guidelines — via skill `web-design-guidelines` (tabular numbers).
- shadcn/ui typeset (Geist preset) — frozen base.

## Example

```tsx
// ✅ scale + utility
<h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
<p className="text-sm text-muted-foreground">All your workspaces.</p>

// ❌ arbitrary size
<h1 style={{ fontSize: 23 }}>Projects</h1>
```

```tsx
// ✅ tabular numbers for data
<td className="tabular-nums">{formatBytes(size)}</td>
```
