---
name: huh
description: "charm.land/huh/v2 — terminal forms and prompts built on Bubble Tea: input, select, confirm, multi-select, file picker, with validation. Use when a CLI needs interactive structured input (wizards, confirmations, surveys) instead of raw fmt.Scan."
category: library
tags: [tui, forms, prompts, input, bubbletea]
last-verified: 2026-08-04
---

# huh — Terminal forms and prompts

## Selection

[`charm.land/huh/v2`](https://github.com/charmbracelet/huh) (v2).

**Why it passes the gate** (actual reason, not stars): it is the maintained
successor of the archived `AlecAivazis/survey`, built directly on Bubble Tea. It
ships the standard prompt types (input, text, select, multi-select, confirm,
file picker, spinner) with validation, help, themes, and accessibility-friendly
key bindings — as one dependency instead of hand-rolled prompt loops.

## Admission checklist

- [x] Actively maintained — v2.0.x, very active (2026)
- [x] Single responsibility — terminal form/prompt library
- [x] Idiomatic Go — `huh.NewForm(huh.NewGroup(...))`, composable
- [x] Tests present + CI — yes
- [x] Documentation — README + examples + charm.sh docs
- [x] Real-world usage — Gum, Huh CLI, many Charm-based apps
- [x] Readable end-to-end — yes
- [x] Justified by need — survey (predecessor) is archived; this is the modern path

## Minimal use

```go
var name string
err := huh.NewForm(huh.NewGroup(
    huh.NewInput().Title("Name").Value(&name),
    huh.NewConfirm().Title("Continue?").Value(&goOn),
)).Run()
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| AlecAivazis/survey | Archived/unmaintained; survey's fork chzyer/readline is low-level. |
| promptui | Older, smaller feature set, less maintained. |
| Raw fmt.Scan / bufio | No editing, no validation, no cursor handling — only for throwaway scripts. |

## Notes

- Runs on Bubble Tea under the hood — do not embed huh forms inside a separate
  `tea.Program`; use `huh.NewForm(...).WithProgram(...)` integration if needed.
- Every field supports `.Validate(func(string) error)`.
- For a full custom TUI with persistent state, use Bubble Tea directly; huh is
  for the form-in-a-script case.
