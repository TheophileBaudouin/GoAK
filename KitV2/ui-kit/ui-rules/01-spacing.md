# 01 — Spacing

## Rule

1. Use the Tailwind spacing scale (4px base: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64) for every
   margin, padding and gap. Never use arbitrary values (`px-[13px]`) to "fine-tune".
2. Between **related** controls use 8px; between **groups** of controls use 20px; standard
   window/panel margins are 20px (Apple HIG §Visual Design, Rule 9.6).
3. A group of controls is separated from the next group by at least 2× the intra-group gap —
   the grouping must be legible at a glance.
4. Align controls to a consistent grid (the 4px scale is the grid); do not stack elements at
   arbitrary offsets.

## Source

- Apple HIG — Layout & Spacing, via skill `macos-design-guidelines` §9.6 (Rule: 20pt margins,
  8pt between related controls, 20pt between groups).
- shadcn/ui + Tailwind CSS v4 spacing scale (frozen base tokens).

## Example

```tsx
// ✅
<div className="flex gap-2"> {/* 8px between related controls */}
  <Button>Apply</Button>
  <Button variant="outline">Cancel</Button>
</div>

// ❌
<div className="flex gap-[13px]"> {/* arbitrary value, off-scale */}
```

```tsx
// ✅ 20px between groups
<section className="space-y-5">
  <FieldGroup>…</FieldGroup>   {/* related fields inside, gap-2 */}
  <FieldGroup>…</FieldGroup>
</section>
```

## Related

- `patterns/settings-page.md` and the harvested settings pieces in
  `ui-sdk/components/hextaui/settings-*`.
