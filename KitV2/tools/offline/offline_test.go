package offline

import (
	"context"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func fixture(t *testing.T) string {
	t.Helper()
	return filepath.Join("bundle")
}

func TestVersionCompatibilityUsesNumericParts(t *testing.T) {
	if compatibleVersion("1.25+", "go1.9") {
		t.Fatal("1.9 must not satisfy 1.25+")
	}
	if !compatibleVersion("1.25+", "go1.26.5") {
		t.Fatal("1.26.5 must satisfy 1.25+")
	}
}

func TestBundleHitAndDeterminism(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	if err := r.Verify(); err != nil {
		t.Fatal(err)
	}
	q := Query{Source: "effective-go", Unit: "effective-go", BudgetTokens: 10}
	first, second := r.Resolve(context.Background(), q), r.Resolve(context.Background(), q)
	left, _ := json.Marshal(first)
	right, _ := json.Marshal(second)
	if string(left) != string(right) {
		t.Fatalf("results are not deterministic: %s != %s", left, right)
	}
	if first.Status != StatusHit || len(first.Matches) != 1 {
		t.Fatalf("unexpected result: %+v", first)
	}
	if !strings.Contains(first.Matches[0].Excerpt, "truncated") {
		t.Fatalf("expected bounded excerpt: %q", first.Matches[0].Excerpt)
	}
}

func TestLocalToolchainResolution(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	result := r.Resolve(context.Background(), Query{Source: "pkg-doc", Unit: "fmt"})
	if result.Status != StatusHit {
		t.Fatalf("fmt resolution failed: %+v", result)
	}
	if result.Provenance.Verifier != "toolchain-local" {
		t.Fatalf("unexpected provenance: %+v", result.Provenance)
	}
}

func TestBlockedAndStaleResults(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	blocked := r.Resolve(context.Background(), Query{Source: "pkg-doc", Unit: "not/a/real/package"})
	if blocked.Status != StatusBlocked || blocked.Prerequisite == "" {
		t.Fatalf("unexpected blocked result: %+v", blocked)
	}
	stale := r.Resolve(context.Background(), Query{Source: "pkg-doc", Unit: "fmt", GoVersion: "go9.9.9"})
	if stale.Status != StatusStale {
		t.Fatalf("unexpected stale result: %+v", stale)
	}
}

func TestFullRetrievalRemainsBounded(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	result := r.Resolve(context.Background(), Query{Source: "effective-go", Unit: "effective-go", Full: true})
	if result.Status != StatusHit || len(result.Matches) != 1 {
		t.Fatalf("unexpected full result: %+v", result)
	}
	if len(result.Matches[0].Excerpt) > 8000*bytesPerToken {
		t.Fatalf("full result exceeded context budget: %d", len(result.Matches[0].Excerpt))
	}
	if !strings.Contains(result.Matches[0].Excerpt, "truncated") {
		t.Fatal("bounded full result must identify truncation")
	}
}

func TestModuleResolutionUsesChecksum(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	result := r.Resolve(context.Background(), Query{Source: "pkg-doc", Unit: "github.com/go-chi/chi/v5"})
	if result.Status != StatusHit || result.Provenance.Verifier != "module-sum" {
		t.Fatalf("unexpected module result: %+v", result)
	}
}

func TestCorruptBlobFailsVerification(t *testing.T) {
	source := fixture(t)
	temporary := t.TempDir()
	if err := copyTree(source, temporary); err != nil {
		t.Fatal(err)
	}
	entries, err := os.ReadDir(filepath.Join(temporary, "blobs"))
	if err != nil {
		t.Fatal(err)
	}
	if len(entries) != 1 {
		t.Fatalf("expected one fixture blob, got %d", len(entries))
	}
	blob := filepath.Join(temporary, "blobs", entries[0].Name())
	if err := os.WriteFile(blob, []byte("corrupt"), 0o644); err != nil {
		t.Fatal(err)
	}
	r, err := Open(temporary)
	if err != nil {
		t.Fatal(err)
	}
	if err := r.Verify(); err == nil {
		t.Fatal("expected corrupt blob to fail verification")
	}
}

func copyTree(source, destination string) error {
	return filepath.Walk(source, func(path string, info os.FileInfo, err error) error { // pi-lens-ignore: go-bare-error
		if err != nil {
			return err
		}
		relative, err := filepath.Rel(source, path)
		if err != nil {
			return err
		}
		target := filepath.Join(destination, relative)
		if info.IsDir() {
			return os.MkdirAll(target, 0o755)
		}
		data, err := os.ReadFile(path)
		if err != nil {
			return err
		}
		return os.WriteFile(target, data, 0o644)
	})
}

func TestResolverSetters(t *testing.T) {
	r, err := Open(fixture(t))
	if err != nil {
		t.Fatal(err)
	}
	if r.goBin != "go" {
		t.Fatalf("default goBin = %q, want go", r.goBin)
	}
	r.SetGoCommand("/custom/go")
	if r.goBin != "/custom/go" {
		t.Fatalf("goBin after SetGoCommand = %q", r.goBin)
	}
	before := len(r.env)
	r.SetEnvironment([]string{"A=B"})
	if len(r.env) != 1 || r.env[0] != "A=B" {
		t.Fatalf("env after SetEnvironment = %v", r.env)
	}
	if before == 0 {
		t.Fatal("fixture resolver started with an empty environment")
	}
}

func TestRankOrdering(t *testing.T) {
	records := []indexRecord{
		{unit: "zebra"},
		{unit: "error-handling"},
		{unit: "errors"},
		{unit: "errors-go"},
	}
	// Prefix "err": every matched unit has prefix rank 1, ties broken by
	// unit name; non-matching units are excluded from the result.
	got := search(records, "err", ModePrefix)
	want := []string{"error-handling", "errors", "errors-go"}
	for i := range want {
		if got[i].unit != want[i] {
			t.Fatalf("search order[%d] = %q, want %q (got %v)", i, got[i].unit, want[i], got)
		}
	}
	// Exact mode matches only the exact unit (rank 0).
	exact := search(records, "errors", ModeExact)
	if len(exact) != 1 || exact[0].unit != "errors" {
		t.Fatalf("exact search = %v", exact)
	}
	// Contains mode matches mid-string tokens (non-prefix rank).
	contains := search(records, "handling", ModeContains)
	if len(contains) != 1 || contains[0].unit != "error-handling" {
		t.Fatalf("contains search = %v", contains)
	}
}
