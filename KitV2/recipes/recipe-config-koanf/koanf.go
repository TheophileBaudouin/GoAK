// Package koanfconfig demonstrates an explicit, testable configuration cascade
// with Koanf. The concrete provider wiring belongs in a consuming application.
package koanfconfig

import (
	"fmt"

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
	return config, nil
}
