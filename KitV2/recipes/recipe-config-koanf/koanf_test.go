package koanfconfig

import (
	"strings"
	"testing"
)

func TestLoadAppliesOverrides(t *testing.T) {
	config, err := Load(map[string]any{"port": 9090})
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if config.Host != "127.0.0.1" || config.Port != 9090 {
		t.Fatalf("Load() = %+v, want default host and overridden port", config)
	}
}

func TestLoadRejectsInvalidValues(t *testing.T) {
	for _, overrides := range []map[string]any{
		{"host": " "},
		{"port": 0},
		{"port": 65536},
	} {
		_, err := Load(overrides)
		if err == nil || !strings.Contains(err.Error(), "validate config") {
			t.Fatalf("Load(%v) error = %v, want validation error", overrides, err)
		}
	}
}

func TestLoadRejectsInvalidType(t *testing.T) {
	if _, err := Load(map[string]any{"port": map[string]any{"bad": true}}); err == nil {
		t.Fatal("Load() error = nil, want unmarshal error")
	}
}
