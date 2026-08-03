// Package viperconfig demonstrates an instance-scoped Viper configuration
// loader. Prefer this shape over Viper's package-level singleton.
package viperconfig

import (
	"fmt"

	"github.com/spf13/viper"
)

// Config is the application configuration produced by Load.
type Config struct {
	Host string `mapstructure:"host"`
	Port int    `mapstructure:"port"`
}

// Load reads a YAML configuration file and applies explicit defaults.
func Load(path string) (Config, error) {
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
	return config, nil
}
