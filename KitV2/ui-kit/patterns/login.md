# Pattern — Login

## When to use

For the authentication entry screen(s): login, signup, password reset, session management.
Desktop apps follow platform auth conventions (macOS: system credentials integration where
available via Wails).

## How to organize the information

1. Single centered card: app name/mark, email + password fields, primary **Sign in** button
   (`Return` activates it), secondary actions below (forgot password, sign up).
2. Error handling: single inline error summary near the fields + `aria-describedby` on the
   invalid field (`ui-rules/05-accessibility.md`); disable the submit while pending and show
   a spinner on the button.
3. Password fields: show/hide toggle (eye icon), never log or display the value; support
   password managers (`autoComplete` attributes).
4. Loading/auth state is explicit; on success, navigate to the app's landing
   (`patterns/dashboard.md` or the app's home).

## Common mistakes

- Errors only as a toast that disappears (no persistent inline message).
- Submit button disabled forever while waiting on network (no feedback).
- Autofill attributes missing — password managers fail.
- Brand accent colors instead of the frozen-base tokens (`ui-rules/02-colors.md`).

## Best practices

- Reuse the harvested auth screens as starting points; verify against the app's real auth
  backend (Wails Go side) before customizing.
- `Cmd+Return` / Enter submits (default action, `ui-rules/08-keyboard.md`).
- Keep it one screen: no multi-step login without a strong reason.

## Components/blocks recommended

- `ui-sdk/blocks/blocks-so/login-03.tsx` (email + password block).
- `ui-sdk/components/hextaui/auth-change-password.tsx`, `auth-session-manager.tsx`.
- Frozen base: `Field`, `Input`, `Button`, `Card`, `Spinner`, `Label`.
