# 05 — Accessibility

## Rule

1. **Semantic structure first**: use native elements (`<button>`, `<a>`, `<input>`,
   `<select>`, `<label>`) or the base's primitives (Radix) that ship with correct roles.
   Every interactive element must have an accessible name — prefer visible text; use
   `aria-label` only when visible text is insufficient (WCAG 4.1.2).
2. **Full keyboard operability** (WCAG 2.1.1): everything is reachable and operable with Tab
   + arrows + Enter/Space. Modals and dialogs **trap focus** and return focus on close.
   Support Shift+Tab reverse navigation.
3. **Visible focus indicators**: never remove focus outlines without a visible replacement
   (WCAG 2.4.7 / 2.4.11 AA). The focus indicator must be ≥2px with ≥3:1 contrast against
   adjacent colors — use `focus-visible:ring-*` from the frozen base.
4. **Screen-reader announcements**: icon-only buttons get `aria-label`; decorative icons get
   `aria-hidden`; live region updates use `role="status"`/`aria-live`; form errors are
   programmatically associated with their field (`aria-describedby`).
5. **Contrast**: body text ≥4.5:1, large text ≥3:1 (WCAG 1.4.3); do not rely on color alone
   (1.4.1). Support the platform's Increase Contrast / high-contrast variants on macOS
   (Apple HIG Rule 11.7).
6. **Respect system preferences**: Reduce Motion (see `04-animations.md`), Reduce
   Transparency (solid fallbacks), Bold Text.

## Source

+ WCAG 2.2 — SC 2.1.1, 2.4.7, 2.4.11, 4.1.2, 1.4.1, 1.4.3, via skill `web-platform-guidelines` §1.
+ Apple HIG — Accessibility, via skill `macos-design-guidelines` §11 (VoiceOver labels,
  focus order, Increase Contrast, Reduce Motion/Transparency).
+ Vercel Web Interface Guidelines — via skill `web-design-guidelines` (a11y category).

## Example

```tsx
// ✅ icon-only button with accessible name
<Button variant="ghost" size="icon" aria-label="Delete project">
  <Trash2Icon />
</Button>

// ❌ silent icon-only button
<Button variant="ghost" size="icon"><Trash2Icon /></Button>
```

```tsx
// ✅ focus indicator from the base
<Button className="focus-visible:ring-2 focus-visible:ring-ring">Save</Button>
```
