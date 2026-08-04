---
name: huh
description: "charm.land/huh/v2 v2.0.3 — interactive terminal forms and prompts built on Bubble Tea. Use for validated multi-field CLI forms; not for non-interactive input, a non-TTY environment, or a custom TUI without accepting the v2 framework."
category: library
tags: [tui, cli, forms, prompts, bubbletea, terminal]
last-verified: 2026-08-05
---

# huh — formulaires terminal

## Selection

[`charm.land/huh/v2`](https://github.com/charmbracelet/huh) v2.0.3,
released 2026-03-10, provides interactive `Form`, `Group`, and field models for
inputs, selects, confirmations, text, spinners, and file pickers. It is admitted
for a focused validated-form boundary, active maintenance, tests, and Charm
ecosystem use; not for popularity. It uses Bubble Tea v2 and Lip Gloss v2.

## Admission checklist

- [x] Current v2.0.3 release and active upstream maintenance.
- [x] Single responsibility: interactive terminal forms and prompts.
- [x] Field-level validation, accessible mode, themes, and sizing are exposed.
- [x] Tests, CI, documentation, and examples exist.
- [x] The major version and TTY dependency are explicit adoption decisions.

## Minimal use

```go
func askName() (string, error) {
    var name string
    form := huh.NewForm(
        huh.NewGroup(huh.NewInput().Title("Name").Value(&name)),
    )
    if err := form.Run(); err != nil {
        return "", fmt.Errorf("run form: %w", err)
    }
    return name, nil
}
```

Use `RunAccessible`/accessible form mode when a terminal UI cannot be relied on
or the user's accessibility workflow requires it. Keep validation at the form
boundary and validate again at the application trust boundary.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Bubble Tea directly | Choose for a custom state machine or form layout that Huh cannot express. |
| stdlib `bufio`/`flag` | Prefer for non-interactive, scriptable, or single-value input. |
| `asky`/`prompt` libraries | Consider for a smaller prompt surface; verify maintenance and TTY behavior independently. |
| Web form | Prefer when the interaction must be browser-accessible or remotely managed. |

## Utiliser cette librairie quand

- A CLI needs a validated wizard, select, multi-select, input, confirmation,
  or multi-group form.
- Bubble Tea v2/Lip Gloss v2 are acceptable transitive boundaries.
- The user interaction is genuinely interactive and terminal-based.

## Ne pas utiliser cette librairie quand

- Input must work non-interactively in pipes, CI, or scripts without an
  accessible-mode design.
- A single flag or line can use stdlib with less ceremony.
- The project needs a custom TUI state machine rather than form primitives.
- The application cannot accept a TTY dependency or the v2 import migration.

## Avantages

- High-level fields, groups, validation, themes, sizing, and accessibility.
- Bubble Tea model integration with much less form boilerplate.
- Current v2 API aligns with the Charm TUI stack and handles common field types.

## Inconvénients

- Interactive forms require a compatible terminal and terminal width.
- v2 is a breaking migration from the old GitHub import path and theme API.
- Dynamic/custom layouts can expose viewport and narrow-terminal edge cases.
- Hidden fields may still trigger TTY behavior; accessible mode is an explicit
  choice, not an automatic replacement.

## Pièges connus

- Check `Form.Run` and preserve its error; do not treat cancelled input as a
  successful configuration.
- Use the v2 import path and `ThemeCharm(isDark)` shape; do not copy v1 themes.
- Test terminals narrower than five columns and resize/select filtering paths.
- Keep domain validation after form submission; terminal validation alone is not
  a trust-boundary guarantee.
- Provide an accessible/non-interactive fallback when CI or automation can run
  the command without a real TTY.

## Sources vérifiées

- [Official huh repository](https://github.com/charmbracelet/huh) — maintenance,
  API, license, checked 2026-08-05.
- [huh v2.0.3 on pkg.go.dev](https://pkg.go.dev/charm.land/huh/v2@v2.0.3) —
  exact version and API, checked 2026-08-05.
- [huh releases](https://github.com/charmbracelet/huh/releases) — v2 changes
  and current tag, checked 2026-08-05.
- [v2.0.0 release](https://github.com/charmbracelet/huh/releases/tag/v2.0.0)
  — breaking import/theme/accessibility changes, checked 2026-08-05.
- [TTY issue #718](https://github.com/charmbracelet/huh/issues/718) — non-TTY
  behavior, checked 2026-08-05.
- [Narrow terminal issue #671](https://github.com/charmbracelet/huh/issues/671)
  — width limitation, checked 2026-08-05.
