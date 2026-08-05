---
name: recipe-config-koanf
description: "Configuration en cascade explicite et typée avec Koanf v2, fusion de sources (valeurs par défaut, carte, environnement, fichier, drapeaux) et validation stricte. Utiliser pour tout service Go combinant plusieurs sources de configuration."
category: recipe
tags: [config, koanf, cascade, env, flags, yaml]
last-verified: 2026-08-05
---

# recipe-config-koanf — Cascade de configuration explicite avec Koanf v2

## Objectif et cas d'utilisation

Charger et fusionner la configuration d'une application Go depuis plusieurs sources selon un ordre de précédence explicite (par exemple : valeurs par défaut < fichier de configuration < variables d'environnement < drapeaux CLI) et un-marchaler le résultat dans une structure typée et validée.

Utiliser Koanf pour les nouvelles applications nécessitant une architecture modulaire et un contrôle total sur l'ordre de fusion des providers.

## Prérequis et architecture

- Go 1.25+
- Dépendances :
  - `github.com/knadh/koanf/v2 v2.3.6`
  - `github.com/knadh/koanf/providers/confmap v1.0.0`
- Architecture :
  - Instancier `koanf.New(".")` localement dans une fonction `Load(overrides map[string]any) (Config, error)`.
  - Éviter toute instance globale mutable.
  - Charger d'abord les valeurs par défaut via `confmap.Provider`.
  - Charger séquentiellement les surcharges (fichiers, env, map) ; chaque `Load` successif écrase les clés précédentes.
  - Décoder via `k.Unmarshal("", &config)` puis exécuter une étape de validation métier explicite.

## Composants et choix

- `github.com/knadh/koanf/v2` — bibliothèque moderne, légère et modulaire (~15x plus légère que Viper sans dépendances inutiles).
- `confmap.Provider` — provider d'objets en mémoire idéal pour injecter des valeurs par défaut et des surcharges de test.

## Alternatives rejetées

- Standard library `os.Getenv` / `flag` seuls : suffisant pour 1 ou 2 variables, mais devient rapidement verbeux et sujet aux erreurs pour les cascades complexes.
- `spf13/viper` : populaire mais monolithique, utilise des singletons globaux par défaut et convertit les clés en minuscules de manière irréversible.
- `kelseyhightower/envconfig` : limité uniquement aux variables d'environnement ; ne permet pas la fusion multi-sources.

## Exemple complet

```go
package koanfconfig

import (
 "fmt"
 "strings"

 "github.com/knadh/koanf/providers/confmap"
 "github.com/knadh/koanf/v2"
)

type Config struct {
 Host string `koanf:"host"`
 Port int    `koanf:"port"`
}

func Load(overrides map[string]any) (Config, error) {
 k := koanf.New(".")
 if err := k.Load(confmap.Provider(map[string]any{
  "host": "127.0.0.1",
  "port": 8080,
 }, "."), nil); err != nil {
  return Config{}, fmt.Errorf("load defaults: %w", err)
 }
 if len(overrides) > 0 {
  if err := k.Load(confmap.Provider(overrides, "."), nil); err != nil {
   return Config{}, fmt.Errorf("load overrides: %w", err)
  }
 }
 var config Config
 if err := k.Unmarshal("", &config); err != nil {
  return Config{}, fmt.Errorf("unmarshal config: %w", err)
 }
 if err := validate(config); err != nil {
  return Config{}, err
 }
 return config, nil
}

func validate(config Config) error {
 if strings.TrimSpace(config.Host) == "" {
  return fmt.Errorf("validate config: host must not be empty")
 }
 if config.Port < 1 || config.Port > 65535 {
  return fmt.Errorf("validate config: port must be between 1 and 65535")
 }
 return nil
}
```

> La fonction `validate` est volontairement partagée avec
> `recipe-config-viper` (packages distincts qui doivent compiler séparément ;
> une copie Go indépendante est conservée dans chaque recette, décision
> D-2026-08-05-09). Les deux recettes répondent à la même question de
> validation d'entrées : consultez la fiche de l'autre bibliothèque pour la
> comparaison koanf ↔ viper.

## Bonnes pratiques et pièges

- Toujours valider la structure `Config` après le `Unmarshal` pour détecter les valeurs hors limites ou manquantes.
- En cas de rechargement dynamique en cours d'exécution, protéger l'instance `*koanf.Koanf` avec un `sync.RWMutex`.
- Ne pas conserver de secrets en clair dans les fichiers de configuration sous contrôle de version.

## Limites et extensions

Koanf ne définit pas d'ordre de cascade par défaut : le développeur doit orchestrer l'ordre des appels `k.Load(...)`. Les parsers (YAML, JSON, TOML) doivent être importés séparément.

## Scénario observable et vérification

```sh
go test ./recipes/recipe-config-koanf/...
go run ./probes/config-koanf
```

La probe charge la configuration avec surcharges, vérifie l'application des valeurs par défaut et des surcharges, puis affiche `config-koanf: PASS`.

## Sources primaires

- [knadh/koanf](https://github.com/knadh/koanf) — dépôt et documentation officielle de Koanf.
- [pkg.go.dev/github.com/knadh/koanf/v2](https://pkg.go.dev/github.com/knadh/koanf/v2) — référence API v2.
