package viperconfig

import (
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestLoadReadsYAML(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "config.yaml")
	if err := os.WriteFile(path, []byte("host: 0.0.0.0\nport: 9090\n"), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	config, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if config.Host != "0.0.0.0" || config.Port != 9090 {
		t.Fatalf("Load() = %+v, want YAML values", config)
	}
}

func TestLoadAppliesDefaults(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "config.yaml")
	if err := os.WriteFile(path, []byte("host: 0.0.0.0\n"), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	config, err := Load(path)
	if err != nil {
		t.Fatalf("Load() error = %v", err)
	}
	if config.Port != 8080 {
		t.Fatalf("Load() port = %d, want default 8080", config.Port)
	}
}

func TestLoadRejectsUnreadableOrInvalidConfig(t *testing.T) {
	if _, err := Load(""); err == nil {
		t.Fatal("Load(\"\") error = nil, want error")
	}
	if _, err := Load(filepath.Join(t.TempDir(), "missing.yaml")); err == nil {
		t.Fatal("Load(missing) error = nil, want error")
	}
	dir := t.TempDir()
	path := filepath.Join(dir, "invalid.yaml")
	if err := os.WriteFile(path, []byte("host: [\n"), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	if _, err := Load(path); err == nil {
		t.Fatal("Load(invalid YAML) error = nil, want error")
	}
}

func TestLoadRejectsInvalidValues(t *testing.T) {
	dir := t.TempDir()
	path := filepath.Join(dir, "invalid-values.yaml")
	if err := os.WriteFile(path, []byte("host: ''\nport: 0\n"), 0o600); err != nil {
		t.Fatalf("write config: %v", err)
	}
	_, err := Load(path)
	if err == nil || !strings.Contains(err.Error(), "validate config") {
		t.Fatalf("Load() error = %v, want validation error", err)
	}
}
