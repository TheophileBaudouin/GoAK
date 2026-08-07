# Pattern — Wizard

## When to use

For a multi-step task where each step depends on the previous (onboarding, project setup,
import with choices, first-run configuration). Not for simple forms (one screen is enough).

## How to organize the information

1. **Steps list** visible (numbered or labeled, with current state) so the user knows how
   long the journey is and where they are — e.g. `onboarding-03` style progress.
2. One screen = one question/decision. Navigation: **Back** (secondary) and **Continue /
   Finish** (primary, `Return` = default action per `ui-rules/08-keyboard.md`).
3. Validate each step before enabling Continue; show inline errors on the field.
4. Finish leads to the actual next screen (never a dead end), and the journey is
   skippable/escaped via "Skip" or closing the window.

## Common mistakes

- 8+ steps of small questions (merge into one screen per theme).
- Continue enabled with invalid data (let the user click into an error wall).
- No Back, no progress indicator, no way to exit.
- Steps that can't be revisited after going forward.

## Best practices

- Keep the primary action label action-oriented ("Create project", not "Next" on the last step).
- Persist partial state so an accidental close doesn't lose everything (or confirm on close).
- Respect `ui-rules/01-spacing.md` (step content max width, 8/20px rhythm) and
  `05-accessibility.md` (focus moves with the step, `aria-current` on the active step).
- Destructive/irreversible final step gets an explicit confirm (`ui-rules/10-dialogs.md`).

## Components/blocks recommended

- `ui-sdk/blocks/blocks-so/onboarding-03.tsx` (steps with progress) — starting point.
- Frozen base: `Stepper`-like composition via `Tabs` or a custom `PremiumWizardSteps`
  component (new named component per constitution §Naming), `Field`, `Button`,
  `AlertDialog` (final confirm).
