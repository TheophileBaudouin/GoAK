---
name: keygen
description: "github.com/charmbracelet/keygen v0.5.4 — Go SSH key-pair generation for Ed25519, RSA, and ECDSA with passphrases and file permissions. Use for programmatic key creation; not for key rotation, agents, authorization, or parsing-only workflows."
category: library
tags: [ssh, keys, crypto, security, cli]
last-verified: 2026-08-05
---

# keygen — génération de clés SSH

## Selection

[`github.com/charmbracelet/keygen`](https://github.com/charmbracelet/keygen) v0.5.4,
released 2025-10-02, wraps Go crypto and `x/crypto/ssh` for generating SSH key
pairs with secure file permissions and optional passphrases. It is admitted for
this small security-sensitive utility boundary, tests, documentation, and Charm
use; not for popularity. A later pseudo-version is not a stable release.

## Admission checklist

- [x] Stable v0.5.4 with active dependency/maintenance updates.
- [x] Single responsibility: SSH key-pair generation and serialization.
- [x] Ed25519, RSA, and ECDSA support with passphrase options.
- [x] Tests, CI, documentation, and explicit private/public file permissions.
- [x] The package avoids repeated crypto marshaling boilerplate but leaves key
      lifecycle policy to the application.

## Minimal use

```go
func writeKeyPair(path string) error {
    pair, err := keygen.New(path, keygen.WithKeyType(keygen.Ed25519))
    if err != nil {
        return fmt.Errorf("generate SSH key: %w", err)
    }
    if err := pair.WriteKeys(); err != nil {
        return fmt.Errorf("write SSH keys: %w", err)
    }
    return nil
}
```

Choose a passphrase option and protect it outside process arguments. Keep private
keys at `0600` and public keys at `0644` only when the deployment policy permits
those modes.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `ssh-keygen` | Prefer for interactive one-shot host tooling when the binary is guaranteed. |
| `crypto/ed25519` + `x/crypto/ssh` | Prefer when the application needs full control over formats or lifecycle policy. |
| `x/crypto/ssh` parsing | Parsing/signing support, not a complete key-generation wrapper. |
| KMS/HSM | Prefer for production key custody, rotation, audit, and non-exportable keys. |

## Utiliser cette librairie quand

- A Go tool must generate host or client SSH keys without shelling out.
- Ed25519/RSA/ECDSA, OpenSSH/PEM serialization, passphrases, and file modes are
  enough for the generation boundary.
- The application owns authorization, rotation, backup, and secure key storage.

## Ne pas utiliser cette librairie quand

- A one-shot interactive command can use a trusted `ssh-keygen` binary.
- Existing keys only need parsing or verification.
- The system needs an SSH agent, KMS/HSM custody, rotation, authorization, or
  audit lifecycle.
- Hardware-backed Ed25519-SK or other unsupported key types are required.

## Avantages

- Small API over standard crypto and SSH marshaling.
- Ed25519, RSA, ECDSA, passphrase support, and explicit file permissions.
- Pure Go generation without a host binary dependency.

## Inconvénients

- Generation only; no key discovery, agent, rotation, revocation, or authorization.
- Passphrases remain application-managed sensitive data.
- Stable v0.5.4 is older than the latest unreleased pseudo-version; pin the tag
  for reproducibility.

## Pièges connus

- Prefer Ed25519; use RSA only for legacy interoperability and select a strong
  key size.
- Keep private files `0600`; never log private material or passphrases.
- Never place a passphrase in command-line arguments; use protected input or a
  secret store.
- Define a recovery/rotation policy before generating keys for a durable service.

## Sources vérifiées

- [Official keygen repository](https://github.com/charmbracelet/keygen) —
  maintenance, API, license, checked 2026-08-05.
- [keygen v0.5.4 releases](https://github.com/charmbracelet/keygen/releases) —
  stable version and release date, checked 2026-08-05.
- [keygen on pkg.go.dev](https://pkg.go.dev/github.com/charmbracelet/keygen)
  — API and options, checked 2026-08-05.
- [keygen implementation](https://github.com/charmbracelet/keygen/blob/v0.5.4/keygen.go)
  — supported key types and file behavior, checked 2026-08-05.
- [OpenBSD ssh-keygen manual](https://man.openbsd.org/OpenBSD-current/man1/ssh-keygen.1)
  — interoperability reference, checked 2026-08-05.
