package main

import (
	"fmt"
	"os"
	"path/filepath"

	viperconfig "go-agent-kit-v2/recipes/recipe-config-viper"
)

func main() {
	dir, err := os.MkdirTemp("", "probe-viper-*")
	if err != nil {
		fail(err)
	}
	defer func() { _ = os.RemoveAll(dir) }()

	path := filepath.Join(dir, "config.yaml")
	if err := os.WriteFile(path, []byte("host: 0.0.0.0\nport: 9090\n"), 0o600); err != nil {
		fail(err)
	}

	cfg, err := viperconfig.Load(path)
	if err != nil {
		fail(fmt.Errorf("viper load failed: %w", err))
	}

	if cfg.Host != "0.0.0.0" || cfg.Port != 9090 {
		fail(fmt.Errorf("unexpected viper config: %+v", cfg))
	}

	fmt.Println("config-viper: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
