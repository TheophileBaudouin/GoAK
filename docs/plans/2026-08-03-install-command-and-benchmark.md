# Commande unique d'installation, README et première version benchmarkable — Plan

**Goal:** Mettre à disposition sur GitHub une première version du kit installable
par une commande unique, documentée dans le README du dépôt, pour permettre le
benchmark du kit. Mettre à jour la mémoire et pousser l'ensemble du working tree.

**Architecture:** Le pattern `KitV2/knowledge/architecture/bootstrap-cli-runtime.yaml`
(statut `proposed`) reste l'architecture canonique future (`gak` CLI, module
publié, release pipeline). En attendant, la version arborescente du produit
`KitV2/` est le consommable : un installeur bootstrap `install.sh` à la racine
matérialise le produit dans un répertoire cible (tarball codeload, extraction
de `KitV2/` uniquement — jamais `.agent/`, mémoire ou évaluations du
metaprojet, ce que le validateur produit interdit déjà), vérifie l'installation
et affiche le mode d'emploi. Le tag `v2.1.0` (aligné sur `manifest.yaml`) épingle
la première version benchmarkable; `GAK_REF` permet de surcharger la référence.

## Décisions

- Commande unique : `curl -fsSL <raw install.sh> | sh -s -- [cible]`.
- Défaut cible : `./go-agent-kit`; refus d'écraser un dossier non vide.
- L'installeur copie le produit intact (arborescence relative `.pi/` →
  `../rules|recipes|knowledge/catalogs` préservée) et ne touche jamais aux
  chemins metaprojet.
- Pas de tag de release « formel » : `v2.1.0` est un marqueur de première
  version benchmarkable (le pattern reste `proposed`, la politique de release
  complète reste à définir). Le README le dit explicitement.

## Étapes

1. Corriger l'identité git locale (user.name theocode29 → TheophileBaudouin).
2. Écrire `install.sh` (POSIX sh, dépendances : curl + tar + sh).
3. Écrire `README.md` racine (commande en évidence + usage + gate).
4. Synchroniser `bootstrap-cli-runtime.yaml` (contraintes devenues inexactes).
5. Mettre à jour la mémoire (Brief / Progress / Gotchas).
6. Valider (sh -n, gate KitV2), commit, push, tag `v2.1.0` + push.
7. Smoke-test réel de la commande depuis raw.githubusercontent.com.

## Validation finale

- `sh -n install.sh` PASS; gate KitV2 PASS.
- Smoke test : installation dans un répertoire propre, validateur PASS,
  aucun fichier metaprojet présent dans la cible.
- Commit attribué à TheophileBaudouin; push OK sur `main`; tag poussé.
- Mémoire à jour (Brief/Progress/Gotchas).
