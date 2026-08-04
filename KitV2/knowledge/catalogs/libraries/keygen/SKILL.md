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

## Utiliser cette librairie quand

- De l'outillage doit créer des paires de clés SSH (hôte ou client)
  programmatiquement au lieu de sheller vers `ssh-keygen`.
- Les formats PEM/OpenSSH, passphrases et permissions de fichiers sécurisées
  (0o600) doivent être gérés correctement sans boilerplate crypto maison.
- L'environnement n'a pas de binaire ssh-keygen fiable (conteneurs, services).

## Ne pas utiliser cette librairie quand

- Un one-shot interactif suffit (ssh-keygen CLI est disponible).
- Le besoin est de parser des clés existantes (x/crypto/ssh parsing seul).
- La gestion du cycle de vie complet (autorisation, rotation) est requise —
  keygen ne génère que des paires.

## Avantages

- API petite et sûre autour du stack crypto stdlib : moins de marshaling
  erreur-prone par type de clé.
- Support Ed25519, RSA, ECDSA + passphrase + permissions explicites.
- Utilisé par l'outillage SSH de Charm (wish/soft-serve).

## Inconvénients

- Génération seulement : pas de gestion d'autorisation, de rotation ni de
  formatage avancé.
- La sécurité finale dépend de l'usage (algorithme, passphrase, perms) —
  la lib ne décide pas à votre place.

## Pièges connus

- Préférer Ed25519 ; RSA uniquement pour compatibilité legacy (≥ 3072 bits).
- Toujours `0o600` sur les clés privées (keygen l'impose via l'API).
- Passphrase via `WithPassphrase`, jamais dans les args de processus
  (visible dans le process listing / historique) — env ou secret store.
- Voir `source:ssh:key-generation` pour la guidance complète (algorithmes,
  formats, protection).

## Sources vérifiées

- [charmbracelet/keygen (repo officiel, v0.5.x)](https://github.com/charmbracelet/keygen)
  — vérifié 2026-08-04
- [ssh-keygen(1) — OpenBSD manual](https://man.openbsd.org/OpenBSD-current/man1/ssh-keygen.1)
  — vérifié 2026-08-04 (référence officielle)
- Artefact interne : `source:ssh:key-generation` (guidance security)
