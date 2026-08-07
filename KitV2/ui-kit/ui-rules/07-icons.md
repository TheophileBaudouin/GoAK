# 07 — Icons

## Rule

1. Use the project's configured icon library — **lucide** (frozen base, `lucide-react`).
   Never mix icon libraries in a component (no `@tabler/icons-react` inside a lucide UI).
2. Icons inside base components use the component's slot conventions, not manual sizing:
   in `Button`, add `data-icon="inline-start"` / `data-icon="inline-end"` — **no** `size-4`
   / `mr-2` classes on the icon (shadcn skill, `rules/icons.md`).
3. Icon-only controls must be in the base's icon sizes (`size="icon"`) and carry an
   accessible name (see `05-accessibility.md`).
4. Semantic color for status icons (destructive/success) via token utilities, never raw hex.
5. Decorative icons get `aria-hidden="true"`; meaningful icons get a label or accompany text.

## Source

- shadcn/ui skill — `rules/icons.md` (icon library conventions, `data-icon` attribute).
- Lucide React (frozen base icon library).
- Apple HIG — Toolbar icons (simple, filled, 16×16 style guidance) via skill
  `macos-design-guidelines` §3.5.

## Example

```tsx
// ✅ correct per shadcn skill
<Button>
  <SearchIcon data-icon="inline-start" />
  Search
</Button>

// ❌ manual sizing/positioning on the icon
<Button>
  <SearchIcon className="mr-2 size-4" />
  Search
</Button>
```

```tsx
// ✅ status icon with semantic token
<Badge variant="destructive"><XCircleIcon data-icon="inline-start" /> Failed</Badge>
```
