---
name: age
description: "filippo.io/age v1.3.1 — file/archive encryption with modern primitives (X25519 + ChaCha20-Poly1305), no protocol choices left to the user. Use when choosing a library to encrypt files, backups, or secrets at rest. Not for network protocols or application-layer encryption of streaming traffic."
category: library
tags: [crypto, encryption, age, x25519, secrets, files]
last-verified: 2026-08-05
---

# age — chiffrement de fichiers

## Selection

[`filippo.io/age`](https://github.com/FiloSottile/age) (v1.3.1, Go 1.24+).

**Why it passes the gate** (actual reason, not stars): it is a small,
audit-friendly encryption format (X25519 key agreement + ChaCha20-Poly1305 +
HKDF) whose API exposes **zero protocol choices** to the caller — no ciphers,
modes, or padding to get wrong. The CLI is a separate binary; the library is
self-contained, pure Go, and interoperable with the widely deployed `age`
format. Maintained by Filippo Valsorda with an explicit security policy and
fuzzing.

## Admission checklist

- [x] Actively maintained — v1.3.1 (2025-12-28), v1.3.0 (2025-11) ajout
      post-quantum X25519MLKEM768 ; push 2026-03
- [x] Single responsibility — file/archive encryption format + API
- [x] Idiomatic Go — pure Go, stdlib crypto where possible, no magic
- [x] Tests present + CI — yes, plus fuzzing (scorecard fuzzing 10/10)
- [x] Documentation — README + format spec + audited design (2020 audit by
      TreiLabs/HashCloak)
- [x] Real-world usage — packaged in Go projects, distro archives, backup
      tools; CLI adopted broadly
- [x] Readable end-to-end — small core (~thousands of LOC), layered
- [x] Justified by need — the kit had zero file-encryption decision support;
      NOT popularity

## Minimal use

```go
id, _ := age.GenerateX25519Identity()        // ou ParseX25519Identity(secret)
w, _ := age.Encrypt(out, id.Recipient())
io.Copy(w, reader); w.Close()                // out = *os.File, bytes.Buffer, …
r, _ := age.Decrypt(reader, id)
io.Copy(out, r)
```

Compilé et vérifié (roundtrip encrypt→decrypt) avec v1.3.1 le 2026-08-05.

## Alternatives considered

| Alternative | Verdict |
|---|---|
| `golang.org/x/crypto/nacl/box` | Chiffrement *réseau* authentifié, pas un format de fichier ; n'apporte ni en-tête identité, ni multi-recipients, ni format stable. |
| AES-GCM stdlib « maison » | Nonce/padding/authentification à gérer soi-même : la classe d'erreur la plus dangereuse en crypto. Rejeté — jamais de schéma maison. |
| GnuPG (openpgp) | Format complexe, historique de vulns, API lourde ; age couvre le cas fichier avec moins de surface. |
| age CLI seul | Bien pour l'usage interactif ; la bibliothèque est le choix en Go pour l'embarqué. |

## Security note

- Historique : 1 advisory **GHSA-32gq-x56h-299c** (GO-2024-3344) — exécution
  arbitraire via noms de plugins/recipients/identities malveillants, corrigé en
  **v1.2.1**. Épingler ≥ v1.2.1 ; v1.3.1 sain (vérifié 2026-08-05, OSV).
- age chiffre au repos ; ce n'est **pas** un protocole de transport. Pour du
  trafic réseau, utiliser TLS (ou `nacl/box` pour point-à-point applicatif).
- Le format protège confidentialité + intégrité (AEAD) mais pas la
  **fraîcheur** : un rejeu d'un fichier chiffré entier n'est pas détectable —
  ajouter un contexte applicatif (version, horodatage) si pertinent.
- Toujours `defer` la fermeture de l'écrivain et vérifier `Close()` (l'écriture
  du dernier bloc AEAD y a lieu).

## Utiliser cette librairie quand

- Chiffrer des fichiers, archives, sauvegardes ou secrets au repos en Go.
- Un format de fichier stable et interopérable est requis (réutilisable en CLI,
  autres langages, autres outils).
- La simplicité du format importe : zéro choix de primitives côté appelant,
  surface d'erreur minimale, auditabilité.

## Ne pas utiliser cette librairie quand

- Chiffrer du trafic réseau : TLS est la réponse (et `certmagic` pour
  l'automatisation ACME).
- Besoin de gestion de clés partagées multi-utilisateurs ou de révocation :
  un KMS/HSM ou un schéma applicatif est requis (voir
  `pattern:security:secrets-management`).
- En-têtes de métadonnées exigées (age vise la confidentialité des
  métadonnées) : le format n'expose ni identité chiffrée ni contexte obligatoire.

## Avantages

- API minimale sans choix cryptographiques exposés (anti-footgun par design).
- Pure Go, zéro cgo, petit noyau auditable ; fuzzing + politique de sécurité
  explicite.
- Post-quantum disponible dès v1.3.0 (X25519MLKEM768) sans changement d'API.
- Interopérable : même format que le CLI `age` et l'écosystème.

## Inconvénients

- Uniquement chiffrement de fichiers/paquets : pas de streaming réseau, pas de
  gestion de clés, pas de révocation.
- Pas de support natif multi-identités *rotatives* (un recipient par fichier ;
  le multi-recipient existe mais chaque clé est statique).
- Le versionnage du format est lent (v1 stable) : peu de feature creep, mais
  aussi peu de nouvelles primitives.

## Pièges connus

- Advisory GHSA-32gq-x56h-299c : ne jamais passer de noms de plugins non
  contrôlés (épingler ≥ v1.2.1, voir Security note).
- `Close()` sur l'écrivain chiffré **doit** être vérifié (l'AEAD final y est
  écrit) ; un oubli produit un fichier tronqué silencieusement.
- Ne pas réutiliser une identité X25519 générée par `GenerateX25519Identity`
  sans sauvegarde : sans la clé privée, le fichier est irrécupérable.
- Le rejeu entier de fichiers n'est pas détectable : ajouter un contexte
  applicatif quand la fraîcheur compte.

## Sources vérifiées

- [FiloSottile/age (repo officiel, v1.3.1)](https://github.com/FiloSottile/age)
  — vérifié 2026-08-05
- [pkg.go.dev/filippo.io/age](https://pkg.go.dev/filippo.io/age) — vérifié
  2026-08-05
- [Advisory GHSA-32gq-x56h-299c (plugin RCE, fix v1.2.1)](https://github.com/FiloSottile/age/security/advisories/GHSA-32gq-x56h-299c)
  — vérifié 2026-08-05 (sécurité officielle)
- [age v1.3.0 — post-quantum release notes](https://github.com/FiloSottile/age/releases/tag/v1.3.0)
  — vérifié 2026-08-05
- [Issue #730 — binaire v1.3.1 construit avec toolchain vulnérable](https://github.com/FiloSottile/age/issues/730)
  — vérifié 2026-08-05 (affecte les binaires publiés, pas la bibliothèque)
- Artefacts internes : `source:security:file-encryption`,
  `pattern:security:secrets-management`, `pattern:security:fail-closed-auth`
