---
name: age
description: "filippo.io/age v1.3.1 — file and archive encryption with a small, pure-Go authenticated format. Use when encrypting files, backups, or secrets at rest; not for network transport, key management, or replay protection."
category: library
tags: [crypto, encryption, age, x25519, secrets, files]
last-verified: 2026-08-05
---

# age — chiffrement de fichiers

## Selection

[`filippo.io/age`](https://github.com/FiloSottile/age) v1.3.1, released
2025-12-28, is a small pure-Go file-encryption format using authenticated
encryption. The API avoids exposing cipher and mode choices to callers; the
format is stable and interoperable with the `age` CLI. It is admitted for its
focused responsibility, maintained upstream, tests/fuzzing, and auditability,
not for star count.

## Admission checklist

- [x] Maintained upstream; v1.3.1 is the current release.
- [x] Single responsibility: file/archive encryption and the age format.
- [x] Pure Go with tests, fuzzing, CI, and a documented security policy.
- [x] Small enough to inspect and usable from Go through `filippo.io/age`.
- [x] Production use and interoperability through the age ecosystem.
- [x] The need is distinct from transport TLS and application key management.

## Minimal use

```go
func encrypt(in io.Reader, out io.Writer, id *age.X25519Identity) error {
    w, err := age.Encrypt(out, id.Recipient())
    if err != nil {
        return fmt.Errorf("create age writer: %w", err)
    }
    if _, err := io.Copy(w, in); err != nil {
        _ = w.Close() // preserve the original copy error; finalization cannot recover it
        return fmt.Errorf("encrypt: %w", err)
    }
    if err := w.Close(); err != nil {
        return fmt.Errorf("finalize encryption: %w", err)
    }
    return nil
}
```

`age.Encrypt` writes the final authenticated block at `Close`, so that error is
part of the operation. Generate or parse the identity separately and handle its
error at the application boundary.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| TLS | Correct for network transport; age is for files and archives. |
| `golang.org/x/crypto/nacl/box` | Authenticated point-to-point primitive, not a stable interoperable file format. |
| Hand-written AES-GCM | Rejected: callers would own nonce, framing, and key-management mistakes. |
| `age` CLI only | Correct for shell workflows; use the Go package when encryption is embedded in a Go program. |

## Utiliser cette librairie quand

- Encrypting files, archives, backups, or secrets at rest.
- An interoperable format and a small cryptographic decision surface matter.
- The caller can provide and protect identities outside the encryption stream.

## Ne pas utiliser cette librairie quand

- The data is network traffic: use TLS.
- The application needs KMS/HSM integration, key rotation, revocation, or
  multi-tenant key policy: use an appropriate key-management boundary.
- The application needs replay/freshness protection: add authenticated
  application metadata and a freshness policy.

## Avantages

- Minimal API with no caller-selected cipher or mode.
- Pure Go, authenticated format, CLI interoperability, and focused surface.
- Current v1.3 line adds hybrid post-quantum recipients without changing the
  basic file-encryption workflow.

## Inconvénients

- It does not provide key storage, rotation, revocation, or network transport.
- Whole-file replay is not detected by the format alone.
- Identities remain application responsibility; losing the private identity
  makes encrypted data unrecoverable.

## Pièges connus

- Always check the writer's `Close` error; the final authenticated data is
  emitted there.
- Do not pass untrusted plugin or recipient names without applying the package's
  documented validation and trust boundary.
- Protect and persist identities before writing data; do not generate a new
  identity for every read of an existing file.
- Rebuild v1.3.1 binaries with a patched Go toolchain when the upstream binary
  toolchain advisory applies; it does not describe a library-source exploit.

## Sources vérifiées

- [FiloSottile/age repository](https://github.com/FiloSottile/age) — official
  repository and license, checked 2026-08-05.
- [age v1.3.1 release](https://github.com/FiloSottile/age/releases/tag/v1.3.1)
  — current release, checked 2026-08-05.
- [filippo.io/age on pkg.go.dev](https://pkg.go.dev/filippo.io/age) — API,
  checked 2026-08-05.
- [age v1.3.0 release](https://github.com/FiloSottile/age/releases/tag/v1.3.0)
  — hybrid recipient and API changes, checked 2026-08-05.
- [age issue #730](https://github.com/FiloSottile/age/issues/730) — binary
  toolchain advisory scope, checked 2026-08-05.
- [age security advisory](https://github.com/FiloSottile/age/security/advisories/GHSA-32gq-x56h-299c)
  — historical plugin/recipient issue and fixed version, checked 2026-08-05.
