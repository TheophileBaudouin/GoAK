// Package viperconfig demonstrates an instance-scoped Viper configuration
// loader. Prefer this shape over Viper's package-level singleton.
package viperconfig

import (
	"fmt"
	"strings"

	"github.com/spf13/viper"
)

// Config is the application configuration produced by Load.
type Config struct {
	Host string `mapstructure:"host"`
	Port int    `mapstructure:"port"`
}

// Load reads a YAML configuration file and applies explicit defaults.
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
