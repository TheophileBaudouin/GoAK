---
name: recipe-config-viper
description: "Configuration typée et isolée avec Viper instance-scoped (sans singleton global), chargement YAML, valeurs par défaut et validation. Utiliser pour intégrer ou maintenir des projets s'appuyant sur l'écosystème Viper."
category: recipe
tags: [config, viper, yaml, files, env, instance-scoped]
last-verified: 2026-08-05
---

# recipe-config-viper — Configuration instance-scoped avec Viper

## Objectif et cas d'utilisation

Charger un fichier de configuration (YAML/JSON/TOML) et appliquer des valeurs par défaut dans une instance isolée de Viper via `viper.New()`, sans utiliser le singleton global du package.

Utiliser cette recette dans les projets existants standardisés sur Viper ou nécessitant ses intégrations poussées (remote config, etcd/consul, pflag binding).

## Prérequis et architecture

- Go 1.25+
- Dépendance : `github.com/spf13/viper v1.21.0`
- Architecture :
  - Créer une instance locale `v := viper.New()` pour chaque chargement dans une fonction `Load(path string) (Config, error)`.
  - Configurer explicitement `v.SetConfigFile(path)` et les valeurs par défaut via `v.SetDefault()`.
  - Lire le fichier avec `v.ReadInConfig()` puis un-marchaler avec `v.Unmarshal(&config)`.
  - Ne jamais partager l'instance `viper.CommandLine` ou le singleton global dans les tests unitaires.

## Composants et choix

- `github.com/spf13/viper v1.21.0` — version stable épinglée pour la configuration applicative.
- `mapstructure` tags (`mapstructure:"host"`) — tags de structure requis par Viper pour le un-marshaling typé.

## Alternatives rejetées

- Singleton global `viper.Get()` / `viper.SetConfigFile()` : rend les tests dépendants de l'état global et empêche l'exécution en parallèle des tests (`t.Parallel()`).
- `recipe-config-koanf` : recommandé pour les nouveaux projets légers sans dépendance à l'écosystème Viper.
- Standard library `flag` / `os` : trop limité pour la lecture de fichiers YAML structurés.

## Exemple complet

```go
package viperconfig

import (
 "fmt"
 "strings"

 "github.com/spf13/viper"
)

type Config struct {
 Host string `mapstructure:"host"`
 Port int    `mapstructure:"port"`
}

func Load(path string) (Config, error) {
 if strings.TrimSpace(path) == "" {
  return Config{}, fmt.Errorf("read config: path must not be empty")
 }
 v := viper.New()
 v.SetConfigFile(path)
 v.SetDefault("host", "127.0.0.1")
 v.SetDefault("port", 8080)
 if err := v.ReadInConfig(); err != nil {
  return Config{}, fmt.Errorf("read config: %w", err)
 }
 var config Config
 if err := v.Unmarshal(&config); err != nil {
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
> `recipe-config-koanf` (packages distincts qui doivent compiler séparément ;
> une copie Go indépendante est conservée dans chaque recette, décision
> D-2026-08-05-09). Les deux recettes répondent à la même question de
> validation d'entrées : consultez la fiche de l'autre bibliothèque pour la
> comparaison koanf ↔ viper.

## Bonnes pratiques et pièges

- Prêter attention aux clés : Viper convertit automatiquement toutes les clés en minuscules (`lowercase`).
- Vérifier `ReadInConfig()` : distinguer les erreurs de fichier absent des erreurs de syntaxe YAML.
- Toujours utiliser `viper.New()` plutôt que le singleton de package.

## Limites et extensions

Viper v2 n'est pas encore sorti comme cible stable ; garder la version `v1.21.0`. Les instances de Viper ne sont pas sûres pour les accès concurrents sans verrou externe (`sync.RWMutex`).

## Scénario observable et vérification

```sh
go test ./recipes/recipe-config-viper/...
go run ./probes/config-viper
```

La probe crée un fichier temporaire `config.yaml`, le charge via `Load`, vérifie les valeurs lues et affiche `config-viper: PASS`.

## Sources primaires

- [spf13/viper](https://github.com/spf13/viper) — dépôt officiel Viper.
- [Viper UPGRADE.md](https://github.com/spf13/viper/blob/master/UPGRADE.md) — guide de migration et breaking changes.
