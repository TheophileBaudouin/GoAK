package main

import (
	"fmt"
	"os"

	koanfconfig "go-agent-kit-v2/recipes/recipe-config-koanf"
)

func main() {
	// Test default loading + override
	cfg, err := koanfconfig.Load(map[string]any{"port": 9090})
	if err != nil {
		fail(fmt.Errorf("koanf load failed: %w", err))
	}

	if cfg.Host != "127.0.0.1" || cfg.Port != 9090 {
		fail(fmt.Errorf("unexpected koanf config: %+v", cfg))
	}

	fmt.Println("config-koanf: PASS")
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, err)
	os.Exit(1)
}
