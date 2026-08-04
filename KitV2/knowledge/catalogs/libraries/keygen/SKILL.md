---
name: keygen
description: "github.com/charmbracelet/keygen — SSH key pair generation (Ed25519, RSA, ECDSA) with passphrase support and PEM/OpenSSH formats. Use when tooling must create SSH host or client keys programmatically instead of shelling out to ssh-keygen."
category: library
tags: [ssh, keys, crypto, security, cli]
last-verified: 2026-08-04
---

# keygen — SSH key pair generation

## Selection

[`github.com/charmbracelet/keygen`](https://github.com/charmbracelet/keygen).

**Why it passes the gate** (actual reason, not stars): generating SSH keys
correctly (right curve/params, correct PEM encoding, secure permissions) is
security-sensitive boilerplate. Keygen wraps the stdlib crypto stack
(`crypto/ed25519`, `crypto/rsa`, `crypto/ecdsa`, `x/crypto/ssh`) into a small
API with passphrase support and explicit file permissions, used by Charm's own
SSH tooling.

## Admission checklist

- [x] Actively maintained — v0.5.x releases, commits 2026
- [x] Single responsibility — SSH key pair generation
- [x] Idiomatic Go — small constructor + file IO, no globals
- [x] Tests present + CI — yes
- [x] Documentation — README
- [x] Real-world usage — Charm SSH tooling (wish/soft-serve ecosystem)
- [x] Readable end-to-end — yes, tiny
- [x] Justified by need — avoids hand-rolled crypto boilerplate with permissions bugs

## Minimal use

```go
kp, err := keygen.New(keygen.Ed25519)
if err != nil {
    err = kp.WritePrivateKeyToFile("id_ed25519", 0o600) // host/client key
    _ = kp.WritePublicKeyToFile("id_ed25519.pub", 0o644)
}
```

## Alternatives considered

| Alternative | Verdict |
|---|---|
| Shelling out to `ssh-keygen` | Couples the binary to the host's ssh install; harder to test and control formats. |
| Raw `crypto/*` + `x/crypto/ssh` | Correct but ~50 lines of error-prone marshaling per key type. |
| `golang.org/x/crypto/ssh` key parsing | Parsing only, not generation. |

## Security note

- Prefer Ed25519; use RSA only for legacy compat (≥3072-bit).
- Always `0o600` on private keys — keygen enforces explicit perms.
- Passphrases: use `keygen.WithPassphrase` and keep the passphrase out of
  process args (env/secret store).
