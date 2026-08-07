# 10 — Dialogs

## Rule

1. Use the base `Dialog` (modal) only when the user must **focus exclusively** on a task or
   confirm a consequential action; prefer non-modal surfaces (`Popover`, `Sheet`,
   inline panel) otherwise (Apple HIG Rule 10.1: popovers for transient context-sensitive
   content).
2. **Esc closes** every dialog/popover/sheet; **Return activates the default button** (the
   safest primary action, visually emphasized); the destructive action is never the default
   (Apple HIG Rules 5.3, 5.4, 10.2).
3. **Focus is trapped** inside the modal and **returned** to the trigger on close
   (WCAG 2.1.1; base Dialog does this — do not disable it).
4. Don't interrupt unnecessarily: no modal for recoverable information; for destructive
   confirmation, offer a **suppression option** ("Don't ask again") when the action repeats
   (Apple HIG Rule 7.3, 7.2).
5. A dialog is small and focused: title + message + 2 actions max (+ optional detail);
   size popovers to their content (Apple HIG Rule 10.3).

## Source

- Apple HIG — Alerts & Popovers, via skill `macos-design-guidelines` §7, §10.
- WCAG 2.2 — 2.1.1 Keyboard (focus trap), via skill `web-platform-guidelines` §1.
- shadcn/ui `Dialog`/`AlertDialog`/`Popover`/`Sheet` (Radix primitives) — frozen base.

## Example

```tsx
// ✅ destructive confirmation, not the default action, Esc/Return handled by base
<AlertDialog>
  <AlertDialogTrigger asChild>
    <Button variant="destructive">Delete project</Button>
  </AlertDialogTrigger>
  <AlertDialogContent>
    <AlertDialogHeader>
      <AlertDialogTitle>Delete “Acme”?</AlertDialogTitle>
      <AlertDialogDescription>
        This permanently removes the project and its history.
      </AlertDialogDescription>
    </AlertDialogHeader>
    <AlertDialogFooter>
      <AlertDialogCancel>Cancel</AlertDialogCancel>
      <AlertDialogAction>Delete</AlertDialogAction>
    </AlertDialogFooter>
  </AlertDialogContent>
</AlertDialog>
```

```tsx
// ❌ modal for something recoverable — use a toast or inline notice instead
```
