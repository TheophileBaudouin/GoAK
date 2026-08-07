# Reference design systems

> Verified on August 6, 2026. This table is the source of truth for knowing **which rule
> relies on which design system**, and which agent skill covers each. Any rule written in
> `ui-rules/` or `patterns/` must trace its source here (verified skills + this file).

| Design system | Official docs | Agent skill found | Reliability | Status |
| --- | --- | --- | --- | --- |
| macOS (Apple HIG) | <https://developer.apple.com/design/human-interface-guidelines> | ehmo/platform-design-skills → `skills/macos-design-guidelines/` (installed, renamed) | High — sourced repo (HIG 2025), MIT, maintained (480★) | **Kept and installed** |
| iOS / iPadOS / watchOS / visionOS / tvOS (Apple HIG) | <https://developer.apple.com/design/human-interface-guidelines> | ehmo/platform-design-skills → skills `ios`, `ipados`, `watchos`, `visionos`, `tvos` (not installed) | High (same repo) | Available — install if a mobile/tablet project appears |
| Material Design 3 | <https://m3.material.io> | ehmo/platform-design-skills → skill `android` (not installed) | High (same repo) | Available — not installed (desktop project) |
| Web / accessibility (WCAG 2.2) | <https://www.w3.org/WAI/WCAG22/quickref> | ehmo/platform-design-skills → `skills/web-platform-guidelines/` (installed, renamed) + vercel-labs `web-design-guidelines` | High | **Kept and installed** (complementary) |
| Fluent (Microsoft, Windows) | <https://fluent2.microsoft.design> | **No reliable agent skill found** | — | Official doc pointer only. Re-evaluate if a reliable skill appears. (The `microsoft/skills` repo targets Azure SDK/AI Foundry, not Fluent.) |
| Carbon (IBM) | <https://carbondesignsystem.com> | **No reliable agent skill found** | — | Official doc pointer only. Same. |
| Primer (GitHub) | <https://primer.style> | **No reliable agent skill found** | — | Official doc pointer only. Same. |

## Usage rules

1. **For desktop (our target)**: the main reference is Apple HIG via
   `skills/macos-design-guidelines/` (desktop user expectations: keyboard, menus, windows,
   toolbars). Fluent would be the Windows reference if a reliable skill existed; otherwise
   consult fluent2.microsoft.design directly for Windows conventions.
2. **For accessibility**: WCAG 2.2 via `skills/web-platform-guidelines/` (ehmo) is the base;
   the `web-design-guidelines` skill (vercel-labs) serves as the review guard.
3. **For aesthetic direction**: `skills/frontend-design/` (Anthropic) — anti "generic AI
   look", not a set of binding rules.
4. **No rule is written without citing its source.** A `ui-rules/` or `patterns/` file
   without a source = non-compliant with the constitution (principle 3).
5. This table updates if a reliable skill appears for Fluent/Carbon/Primer
   (check on skills.sh, then test), otherwise never without an explicit request.

## History

- 2026-08-06: initial verification.
