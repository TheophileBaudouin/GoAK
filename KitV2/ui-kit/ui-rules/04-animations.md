# 04 — Animations

## Rule

1. **Respect `prefers-reduced-motion`** (WCAG 2.3.3, Level AAA): every animation/transition
   must have a reduced-motion alternative (e.g. `@media (prefers-reduced-motion: reduce)`
   collapsing durations to ~0ms). Apple HIG Rule 11.3: respect Reduce Motion.
2. Animate only **`transform` and `opacity`** (compositor-friendly, 60fps). Do not animate
   `width`, `height`, `top`, `left`, or `margin` (layout thrash).
3. Keep durations short and consistent: 150–300ms for micro-interactions, ≤500ms for
   surfaces (dialogs/sheets via the base's animation tokens `tw-animate-css`). No flashing
   or strobing content (WCAG 2.3.1).
4. Use the frozen base's animation utilities (`animate-in`, `animate-out`, `data-open:` /
   `data-closed:` variants) instead of inventing keyframes.
5. Motion is for affordance, not decoration: every animation should explain a state change
   (open/close, appear/disappear, selection). See also `skills/frontend-design` — less is
   more; orchestrated moments beat scattered effects.

## Source

- WCAG 2.2 — 2.3.3 Animation from Interactions, 2.3.1 Three Flashes, via skill
  `web-platform-guidelines` §6.
- Apple HIG — Motion, via skill `macos-design-guidelines` §11.3.
- shadcn/ui animation conventions (`tw-animate-css`, `data-*` variants) — frozen base.
- Anthropic `frontend-design` skill (motion guidance).

## Example

```tsx
// ✅ compositor-only + reduced-motion guard
<div
  className="transition-transform duration-200 ease-out data-[open]:translate-y-0"
  data-open={open ? "" : undefined}
/>

// ❌ animating layout properties
<div className="transition-all duration-300" style={{ width: open ? 300 : 200 }} />
```

```css
/* ✅ reduced-motion alternative */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
