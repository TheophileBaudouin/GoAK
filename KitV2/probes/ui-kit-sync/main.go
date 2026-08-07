// Probe ui-kit-sync — observable verification of tools/sync-ui-kit.sh (Z13 §6).
//
// Scenario: build a disposable Wails-shaped fixture (wails.json +
// frontend/package.json), run the shipped sync tool against it, and assert
// the SDK materialization (ui-kit/ mirror, src/components code copy, .pi
// skills wiring). Then assert the Wails-only guarantee: a fixture WITHOUT a
// frontend/ is refused with a non-zero exit and copies NOTHING.
//
// No network, no external services: everything comes from the kit tree.
package main

import (
	"errors"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

func main() {
	root, err := os.Getwd() // probes/run.sh runs `go run` from the kit root
	if err != nil {
		fail(fmt.Errorf("getwd: %w", err))
	}
	syncTool := filepath.Join(root, "tools", "sync-ui-kit.sh")
	if _, err := os.Stat(syncTool); err != nil {
		fail(fmt.Errorf("sync tool missing at %s: %w", syncTool, err))
	}
	if _, err := os.Stat(filepath.Join(root, "ui-kit", "AGENTS.md")); err != nil {
		fail(fmt.Errorf("ui-kit zone missing in the kit: %w", err))
	}

	fixture, err := os.MkdirTemp("", "ui-kit-sync-probe-")
	if err != nil {
		fail(err)
	}
	defer func() { _ = os.RemoveAll(fixture) }()

	// --- fixture: a Wails project -----------------------------------------
	mustWrite(filepath.Join(fixture, "wails.json"),
		`{"name":"probe","outputfilename":"probe"}`+"\n")
	mustWrite(filepath.Join(fixture, "frontend", "package.json"),
		`{"name":"frontend","private":true,"version":"0.1.0"}`+"\n")

	run := func(target string) (string, int) {
		// #nosec G204 -- bash invocation targets os.MkdirTemp dirs created by
		// this probe only; no user-controlled input reaches the command line.
		cmd := exec.Command("bash", syncTool, "--target", target)
		cmd.Dir = fixture
		out, err := cmd.CombinedOutput()
		code := 0
		if err != nil {
			var exit *exec.ExitError
			if errors.As(err, &exit) {
				code = exit.ExitCode()
			} else {
				fail(fmt.Errorf("run sync tool: %w", err))
			}
		}
		return string(out), code
	}

	// --- 1. Wails fixture: SDK materialized --------------------------------
	out, code := run(fixture)
	if code != 0 {
		fail(fmt.Errorf("sync on Wails fixture exited %d:\n%s", code, out))
	}
	assertFile(filepath.Join(fixture, "frontend", "ui-kit", "AGENTS.md"), "SDK AGENTS.md")
	assertFile(filepath.Join(fixture, "frontend", "ui-kit", "skills", "frontend-design", "SKILL.md"), "SDK skill")
	settings, err := os.ReadFile(filepath.Join(fixture, "frontend", ".pi", "settings.json")) // #nosec G304 -- fixture path from os.MkdirTemp in this probe
	if err != nil {
		fail(fmt.Errorf("frontend .pi/settings.json not created: %w", err))
	}
	if !strings.Contains(string(settings), "../ui-kit/skills") {
		fail(fmt.Errorf(".pi/settings.json missing the SDK skills wiring: %s", settings))
	}
	if !hasSourceFiles(filepath.Join(fixture, "frontend", "src", "components")) {
		fail(fmt.Errorf("no SDK code copied under frontend/src/components (copy rules)"))
	}

	// --- 2. non-Wails fixture: refused, nothing copied ---------------------
	bare, err := os.MkdirTemp("", "ui-kit-sync-bare-")
	if err != nil {
		fail(err)
	}
	defer func() { _ = os.RemoveAll(bare) }()
	mustWrite(filepath.Join(bare, "go.mod"), "module bare\n")
	out, code = run(bare)
	if code == 0 {
		fail(fmt.Errorf("non-Wails target not refused (exit 0):\n%s", out))
	}
	if _, err := os.Stat(filepath.Join(bare, "frontend")); err == nil {
		fail(fmt.Errorf("non-Wails target received SDK files — Wails-only guarantee broken"))
	}

	fmt.Println("ui-kit-sync: PASS (Wails fixture materialized, non-Wails refused)")
}

func mustWrite(path, content string) {
	if err := os.MkdirAll(filepath.Dir(path), 0o750); err != nil {
		fail(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		fail(err)
	}
}

func assertFile(path, what string) {
	if _, err := os.Stat(path); err != nil {
		fail(fmt.Errorf("%s missing at %s: %w", what, path, err))
	}
}

func hasSourceFiles(dir string) bool {
	entries, err := os.ReadDir(dir)
	if err != nil {
		return false
	}
	for _, entry := range entries {
		if entry.IsDir() {
			if hasSourceFiles(filepath.Join(dir, entry.Name())) {
				return true
			}
		} else if strings.HasSuffix(entry.Name(), ".tsx") || strings.HasSuffix(entry.Name(), ".ts") {
			return true
		}
	}
	return false
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "ui-kit-sync: FAIL:", err)
	os.Exit(1)
}
