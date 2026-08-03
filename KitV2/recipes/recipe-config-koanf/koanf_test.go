package koanfconfig

import "testing"

func TestLoadAppliesOverrides(t *testing.T) {
	config, err := Load(map[string]any{"port": 9090})
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if config.Host != "127.0.0.1" || config.Port != 9090 {
		t.Fatalf("Load() = %+v, want default host and overridden port", config)
	}
}
