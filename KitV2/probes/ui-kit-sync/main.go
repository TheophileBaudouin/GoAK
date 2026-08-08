// Probe ui-kit-sync — observable verification of tools/sync-ui-kit.sh.
//
// Scenarios:
//  1. Wails fixture + real zone: SDK materialized, .pi skills wired, code
//     copied; a second run is idempotent (no adds, no removals).
//  2. Non-Wails fixture: refused with non-zero exit, nothing copied.
//  3. Structure evolution (UI_KIT_SRC seam + copy-rules.json): a NEW folder
//     in the zone is copied purely via the rules; an upstream-removed file
//     is deleted cleanly; a consumer file at a destination path is adopted
//     (first run) and never destroyed.
//  4. Ownership contract: a consumer-modified SDK file is REFUSED (exit 1)
//     and its content preserved.
//
// No network, no external services: everything comes from the kit tree.
package main

import (
	"errors"
	"fmt"
	"io"
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
	realZone := filepath.Join(root, "ui-kit")
	if _, err := os.Stat(syncTool); err != nil {
		fail(fmt.Errorf("sync tool missing at %s: %w", syncTool, err))
	}
	if _, err := os.Stat(filepath.Join(realZone, "AGENTS.md")); err != nil {
		fail(fmt.Errorf("ui-kit zone missing in the kit: %w", err))
	}

	// run the sync tool against target, optionally with a zone override
	run := func(target, zoneSrc string) (string, int) {
		// #nosec G204 -- bash invocation targets os.MkdirTemp dirs created by
		// this probe only; no user-controlled input reaches the command line.
		cmd := exec.Command("bash", syncTool, "--target", target)
		cmd.Dir = target
		cmd.Env = append(os.Environ(), "UI_KIT_SRC="+zoneSrc)
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

	// --- 1. Wails fixture, real zone: materialize + idempotence ------------
	fixA := mustTemp("ui-kit-sync-a-")
	defer clean(fixA)
	mustWrite(filepath.Join(fixA, "wails.json"), `{"name":"probe"}`+"\n")
	mustWrite(filepath.Join(fixA, "frontend", "package.json"), `{"name":"frontend"}`+"\n")

	out, code := run(fixA, realZone)
	if code != 0 {
		fail(fmt.Errorf("sync on Wails fixture exited %d:\n%s", code, out))
	}
	assertFile(filepath.Join(fixA, "frontend", "ui-kit", "AGENTS.md"), "SDK AGENTS.md")
	assertFile(filepath.Join(fixA, "frontend", "ui-kit", "skills", "frontend-design", "SKILL.md"), "SDK skill")
	assertFile(filepath.Join(fixA, "frontend", "ui-kit", ".owned.json"), "ownership manifest")
	settings, err := os.ReadFile(filepath.Join(fixA, "frontend", ".pi", "settings.json")) // #nosec G304 -- fixture path from os.MkdirTemp in this probe
	if err != nil {
		fail(fmt.Errorf("frontend .pi/settings.json not created: %w", err))
	}
	if !strings.Contains(string(settings), "../ui-kit/skills") {
		fail(fmt.Errorf(".pi/settings.json missing the SDK skills wiring: %s", settings))
	}
	if !hasSourceFiles(filepath.Join(fixA, "frontend", "src", "components")) {
		fail(fmt.Errorf("no SDK code copied under frontend/src/components (copy rules)"))
	}

	// idempotence: second run adds nothing and removes nothing
	out, code = run(fixA, realZone)
	if code != 0 || !strings.Contains(out, "+0 added") || !strings.Contains(out, "0 removed") {
		fail(fmt.Errorf("second run not idempotent (exit %d):\n%s", code, out))
	}

	// --- 2. non-Wails fixture: refused, nothing copied ----------------------
	bare := mustTemp("ui-kit-sync-bare-")
	defer clean(bare)
	mustWrite(filepath.Join(bare, "go.mod"), "module bare\n")
	out, code = run(bare, realZone)
	if code == 0 {
		fail(fmt.Errorf("non-Wails target not refused (exit 0):\n%s", out))
	}
	if _, err := os.Stat(filepath.Join(bare, "frontend")); err == nil {
		fail(fmt.Errorf("non-Wails target received SDK files — Wails-only guarantee broken"))
	}

	// --- 3. structure evolution (fake zone via UI_KIT_SRC + copy-rules) ----
	fixB := mustTemp("ui-kit-sync-b-")
	defer clean(fixB)
	mustWrite(filepath.Join(fixB, "wails.json"), `{"name":"probe"}`+"\n")
	mustWrite(filepath.Join(fixB, "frontend", "package.json"), `{"name":"frontend"}`+"\n")
	// consumer file that pre-exists in the SDK-owned destination dir
	mustWrite(filepath.Join(fixB, "frontend", "src", "components", "MyOwn.tsx"), "// mine\n")

	fakeZone := mustTemp("ui-kit-sync-zone-")
	defer clean(fakeZone)
	copyTree(realZone, fakeZone)
	mustWrite(filepath.Join(fakeZone, "ui-sdk", "hooks", "use-thing.ts"), "export const useThing = () => 1;\n")
	mustWrite(filepath.Join(fakeZone, "copy-rules.json"),
		`[{"src":"ui-sdk/components","dst":"src/components"},`+
			`{"src":"ui-sdk/blocks/blocks-so","dst":"src/components"},`+
			`{"src":"ui-sdk/examples/preferences-screen","dst":"src/components/example"},`+
			`{"src":"ui-sdk/hooks","dst":"src/hooks"}]`+"\n")

	out, code = run(fixB, fakeZone)
	if code != 0 {
		fail(fmt.Errorf("evolution sync exited %d:\n%s", code, out))
	}
	assertFile(filepath.Join(fixB, "frontend", "src", "hooks", "use-thing.ts"), "new-folder file (via copy-rules.json)")
	if content := read(filepath.Join(fixB, "frontend", "src", "components", "MyOwn.tsx")); content != "// mine\n" {
		fail(fmt.Errorf("consumer file overwritten on first run: %q", content))
	}
	if !strings.Contains(out, "adopt") {
		fail(fmt.Errorf("first-run adoption not reported:\n%s", out))
	}

	// upstream removes a file -> next sync deletes it cleanly
	if err := os.Remove(filepath.Join(fakeZone, "ui-rules", "01-spacing.md")); err != nil {
		fail(err)
	}
	out, code = run(fixB, fakeZone)
	if code != 0 {
		fail(fmt.Errorf("deletion sync exited %d:\n%s", code, out))
	}
	if _, err := os.Stat(filepath.Join(fixB, "frontend", "ui-kit", "ui-rules", "01-spacing.md")); err == nil {
		fail(fmt.Errorf("upstream-removed SDK file not deleted"))
	}
	assertFile(filepath.Join(fixB, "frontend", "src", "components", "MyOwn.tsx"), "consumer file after deletion sync")

	// --- 4. consumer-modified SDK file: refused + preserved ----------------
	hookFile := filepath.Join(fixB, "frontend", "src", "hooks", "use-thing.ts")
	mustAppend(hookFile, "\n// consumer edit\n")
	out, code = run(fixB, fakeZone)
	if code == 0 {
		fail(fmt.Errorf("modified-file sync not refused (exit 0):\n%s", out))
	}
	if content := read(hookFile); !strings.Contains(content, "consumer edit") {
		fail(fmt.Errorf("consumer-modified SDK file was clobbered: %q", content))
	}

	fmt.Println("ui-kit-sync: PASS (materialize, idempotence, Wails-only, structure evolution, ownership contract)")
}

func mustTemp(pattern string) string {
	dir, err := os.MkdirTemp("", pattern)
	if err != nil {
		fail(err)
	}
	return dir
}

func clean(dir string) { _ = os.RemoveAll(dir) }

func mustWrite(path, content string) {
	if err := os.MkdirAll(filepath.Dir(path), 0o750); err != nil {
		fail(err)
	}
	if err := os.WriteFile(path, []byte(content), 0o600); err != nil {
		fail(err)
	}
}

func mustAppend(path, content string) {
	f, err := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, 0o600) // #nosec G304 -- fixture path from os.MkdirTemp in this probe
	if err != nil {
		fail(err)
	}
	defer func() { _ = f.Close() }()
	if _, err := f.WriteString(content); err != nil {
		fail(err)
	}
}

func read(path string) string {
	data, err := os.ReadFile(path) // #nosec G304 -- fixture paths from os.MkdirTemp in this probe
	if err != nil {
		fail(err)
	}
	return string(data)
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

func copyTree(src, dst string) {
	err := filepath.WalkDir(src, func(path string, d os.DirEntry, err error) error {
		if err != nil {
			return err
		}
		rel, err := filepath.Rel(src, path)
		if err != nil {
			return err
		}
		target := filepath.Join(dst, rel)
		if d.IsDir() {
			return os.MkdirAll(target, 0o750)
		}
		// #nosec G122, G304 -- tree copy between os.MkdirTemp dirs of this
		// probe only; no symlink traversal or user-controlled paths.
		in, err := os.Open(path)
		if err != nil {
			return err
		}
		defer func() { _ = in.Close() }()
		out, err := os.OpenFile(target, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o600) // #nosec G304 -- temp-dir target of this probe
		if err != nil {
			return err
		}
		defer func() { _ = out.Close() }()
		_, err = io.Copy(out, in)
		return err
	})
	if err != nil {
		fail(fmt.Errorf("copyTree: %w", err))
	}
}

func fail(err error) {
	fmt.Fprintln(os.Stderr, "ui-kit-sync: FAIL:", err)
	os.Exit(1)
}
