// Package koanfconfig demonstrates an explicit, testable configuration cascade
// with Koanf. The concrete provider wiring belongs in a consuming application.
package koanfconfig

import (
	"fmt"
	"strings"

	"github.com/knadh/koanf/providers/confmap"
	"github.com/knadh/koanf/v2"
)

// Config is the application configuration produced by Load.
type Config struct {
	Host string `koanf:"host"`
	Port int    `koanf:"port"`
}

// Load applies defaults, then overrides them with the supplied values.
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
