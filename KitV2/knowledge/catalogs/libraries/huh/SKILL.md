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

## Utiliser cette librairie quand

- Une CLI a besoin de saisie structurée interactive (wizards, confirmations,
  sondages) au lieu de `fmt.Scan` brut.
- Les types de prompts standards suffisent : input, text, select,
  multi-select, confirm, file picker, spinner.
- La validation par champ (`.Validate(func(string) error)`) est souhaitée
  sans boucle maison.

## Ne pas utiliser cette librairie quand

- Une TUI custom avec état persistant est visée : Bubble Tea directement.
- Un prompt trivial one-shot suffit (scripts jetables : fmt.Scan accepté).
- survey (prédécesseur) est archivé : ne pas l'utiliser.

## Avantages

- Successeur maintenu de survey (archivé), construit sur Bubble Tea.
- Types de prompts complets avec validation, help, thèmes, bindings
  accessibles.
- Une dépendance au lieu de boucles de prompt maison.
- `huh.NewForm(huh.NewGroup(...))` composable.

## Inconvénients

- Basé sur Bubble Tea : ne pas l'embarquer dans un `tea.Program` séparé
  (intégration via `WithProgram` si nécessaire).
- Orientation « formulaire dans un script » : pas adapté aux TUIs à état
  persistant.
- Dépendance de la chaîne Charm (bubbletea sous le capot).

## Pièges connus

- Ne pas lancer huh à l'intérieur d'un autre `tea.Program` : utiliser
  `huh.NewForm(...).WithProgram(...)` pour l'intégration.
- Toujours associer `.Validate` aux champs sensibles — la validation est
  par champ, pas globale par défaut.
- Pour une TUI complète avec état, passer à Bubble Tea directement (huh est
  le cas « formulaire dans un script »).

## Sources vérifiées

- [charmbracelet/huh (repo officiel, v2)](https://github.com/charmbracelet/huh)
  — vérifié 2026-08-04
- [pkg.go.dev/charm.land/huh/v2](https://pkg.go.dev/charm.land/huh/v2) —
  vérifié 2026-08-04
- Artefact interne : catalog `bubbletea` (fondation)
