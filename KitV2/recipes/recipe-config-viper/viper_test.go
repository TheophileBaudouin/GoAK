package viperconfig

import (
	"os"
	"path/filepath"
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
