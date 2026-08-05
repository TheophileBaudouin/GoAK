// Package offline resolves bounded, pinned Go knowledge without network access.
package offline

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// Protocol identifies the retrieval wire contract.
const Protocol = "goretrieval/1"

const (
	maxManifestBytes = 4096
	maxIndexBytes    = 16384
	maxBlobBytes     = 524288
	defaultLimit     = 4
	defaultBudget    = 2000
)

// Status is the result of a retrieval operation.
type Status string

const (
	// StatusHit means the requested knowledge was resolved and verified.
	StatusHit Status = "hit"
	// StatusMiss means an indexed unit or blob failed integrity checks.
	StatusMiss Status = "miss"
	// StatusStale means the request and pinned source versions are incompatible.
	StatusStale Status = "stale"
	// StatusBlocked means a prerequisite is unavailable in the current mode.
	StatusBlocked Status = "blocked"
)

// Mode controls deterministic unit matching.
type Mode string

const (
	// ModeExact matches one unit.
	ModeExact Mode = "exact"
	// ModePrefix matches units beginning with Unit.
	ModePrefix Mode = "prefix"
	// ModeContains matches units containing Unit.
	ModeContains Mode = "contains"
)

// Provenance identifies the verified source used for a result.
type Provenance struct {
	Pin      string `json:"pin"`
	SHA256   string `json:"sha256"`
	Verifier string `json:"verifier"`
}

// Match is one bounded source result.
type Match struct {
	Unit    string `json:"unit"`
	SHA256  string `json:"sha256"`
	Excerpt string `json:"excerpt"`
}

// Query selects a bounded source unit.
type Query struct {
	Source       string `json:"source"`
	Unit         string `json:"unit"`
	Mode         Mode   `json:"mode"`
	Limit        int    `json:"limit"`
	BudgetTokens int    `json:"budget_tokens"`
	GoVersion    string `json:"go_version"`
	Online       bool   `json:"online"`
	Full         bool   `json:"full"`
}

// Result is a deterministic retrieval response.
type Result struct {
	Protocol     string     `json:"protocol"`
	Status       Status     `json:"status"`
	Source       string     `json:"source"`
	Unit         string     `json:"unit"`
	Matches      []Match    `json:"matches"`
	Provenance   Provenance `json:"provenance"`
	Prerequisite string     `json:"prerequisite,omitempty"`
}

type manifest struct {
	Protocol string   `json:"protocol"`
	Schema   int      `json:"schema"`
	Sources  []source `json:"sources"`
	Modules  []module `json:"modules"`
}

type source struct {
	ID          string `json:"id"`
	GoVersion   string `json:"go_version"`
	Pin         string `json:"pin"`
	PinType     string `json:"pin_type"`
	Verifier    string `json:"verifier"`
	Index       string `json:"index"`
	IndexSHA256 string `json:"index_sha256"`
	License     string `json:"license"`
	Attribution string `json:"attribution"`
}

type module struct {
	Path    string `json:"path"`
	Version string `json:"version"`
}

// Resolver is an immutable, offline-first source resolver.
type Resolver struct {
	root     string
	manifest manifest
	sources  map[string]source
	indexes  map[string][]indexRecord
	goBin    string
	env      []string
}

// Open loads and validates a complete source bundle.
func Open(bundlePath string) (*Resolver, error) {
	root, err := filepath.Abs(bundlePath)
	if err != nil {
		return nil, fmt.Errorf("resolve bundle path: %w", err)
	}
	data, err := readFile(filepath.Join(root, "manifest.json")) // #nosec G304 -- manifest path is fixed below the caller-selected bundle root
	if err != nil {
		return nil, fmt.Errorf("read manifest: %w", err)
	}
	if len(data) > maxManifestBytes {
		return nil, fmt.Errorf("manifest exceeds %d bytes", maxManifestBytes)
	}
	var m manifest
	if err := json.Unmarshal(data, &m); err != nil {
		return nil, fmt.Errorf("parse manifest: %w", err)
	}
	if m.Protocol != Protocol || m.Schema != 1 {
		return nil, errors.New("unsupported retrieval manifest")
	}
	r := &Resolver{
		root:     root,
		manifest: m,
		sources:  make(map[string]source),
		indexes:  make(map[string][]indexRecord),
		goBin:    "go",
		env:      os.Environ(),
	}
	for _, s := range m.Sources {
		if err := validateSource(s); err != nil {
			return nil, err
		}
		if _, exists := r.sources[s.ID]; exists {
			return nil, fmt.Errorf("duplicate source %q", s.ID)
		}
		r.sources[s.ID] = s
		if s.Index != "" {
			records, err := r.loadIndex(s)
			if err != nil {
				return nil, err
			}
			r.indexes[s.ID] = records
		}
	}
	return r, nil
}

// SetGoCommand selects the executable used for local toolchain resolution.
func (r *Resolver) SetGoCommand(path string) {
	r.goBin = path
}

// SetEnvironment replaces the environment used for local toolchain resolution.
func (r *Resolver) SetEnvironment(env []string) {
	r.env = append([]string(nil), env...)
}

// Verify checks every indexed blob and its declared SHA-256 digest.
func (r *Resolver) Verify() error {
	for id, records := range r.indexes {
		for _, record := range records {
			data, err := r.readBlob(record)
			if err != nil {
				return fmt.Errorf("verify %s/%s: %w", id, record.unit, err)
			}
			if digest(data) != record.sha {
				return fmt.Errorf("verify %s/%s: checksum mismatch", id, record.unit)
			}
		}
	}
	return nil
}

// Resolve retrieves only the units required by q. It never fabricates knowledge.
func (r *Resolver) Resolve(ctx context.Context, q Query) Result {
	result := Result{Protocol: Protocol, Status: StatusBlocked, Source: q.Source, Unit: q.Unit}
	id := q.Source
	if id == "stdlib" {
		id = "pkg-doc"
	}
	s, ok := r.sources[id]
	if !ok {
		result.Prerequisite = "add a declared source to manifest.json"
		return result
	}
	result.Source = id
	if q.Mode == "" {
		q.Mode = ModeExact
	}
	if !compatibleVersion(s.GoVersion, q.GoVersion) {
		result.Status = StatusStale
		result.Provenance = Provenance{Pin: s.Pin, Verifier: s.Verifier}
		return result
	}
	if records, indexed := r.indexes[id]; indexed {
		return r.resolveIndexed(result, s, records, q)
	}
	if moduleResult, matched := resolveModule(ctx, r, q, r.manifest.Modules); matched {
		return moduleResult
	}
	return r.resolveLocal(ctx, result, q)
}

func (r *Resolver) resolveIndexed(result Result, s source, records []indexRecord, q Query) Result {
	matches := search(records, q.Unit, q.Mode)
	if len(matches) == 0 {
		result.Status = StatusMiss
		return result
	}
	for _, record := range matches {
		data, err := r.readBlob(record)
		if err != nil || digest(data) != record.sha {
			result.Status = StatusMiss
			return result
		}
		result.Matches = append(result.Matches, Match{
			Unit:    record.unit,
			SHA256:  record.sha,
			Excerpt: excerpt(data, q),
		})
	}
	result.Matches = limitMatches(result.Matches, q)
	if len(result.Matches) == 0 {
		result.Status = StatusMiss
		return result
	}
	result.Status = StatusHit
	provenanceSHA := ""
	if len(matches) > 0 {
		provenanceSHA = matches[0].sha
	}
	result.Provenance = Provenance{Pin: s.Pin, SHA256: provenanceSHA, Verifier: s.Verifier}
	return result
}

func (r *Resolver) readBlob(record indexRecord) ([]byte, error) {
	path, err := safeJoin(r.root, record.ref)
	if err != nil {
		return nil, err
	}
	data, err := readFile(path)
	if err != nil {
		return nil, err
	}
	if len(data) > maxBlobBytes {
		return nil, fmt.Errorf("blob exceeds %d bytes", maxBlobBytes)
	}
	if filepath.Base(path) != record.sha {
		return nil, errors.New("blob filename does not match checksum")
	}
	return data, nil
}

func validateSource(s source) error {
	if s.ID == "" || s.Pin == "" || s.License == "" || s.Attribution == "" {
		return fmt.Errorf("source %q has incomplete provenance", s.ID)
	}
	validPin := map[string]bool{
		"toolchain-version": true,
		"module-version":    true,
		"git-commit":        true,
	}
	validVerifier := map[string]bool{
		"toolchain-local": true,
		"module-sum":      true,
		"git-commit":      true,
		"dl-json":         true,
	}
	if !validPin[s.PinType] || !validVerifier[s.Verifier] {
		return fmt.Errorf("source %q has unsupported pin verifier", s.ID)
	}
	if s.Index != "" && s.IndexSHA256 == "" {
		return fmt.Errorf("source %q has indexed content without index checksum", s.ID)
	}
	return nil
}

func safeJoin(root, name string) (string, error) {
	if filepath.IsAbs(name) {
		return "", errors.New("absolute path is not allowed")
	}
	clean := filepath.Clean(name)
	if clean == "." || clean == ".." || strings.HasPrefix(clean, ".."+string(filepath.Separator)) {
		return "", errors.New("path escapes bundle")
	}
	path := filepath.Join(root, clean)
	rel, err := filepath.Rel(root, path)
	if err != nil || rel == ".." || strings.HasPrefix(rel, ".."+string(filepath.Separator)) {
		return "", errors.New("path escapes bundle")
	}
	return path, nil
}

func readFile(path string) ([]byte, error) {
	return os.ReadFile(path) // #nosec G304 -- paths are constrained before resolver reads; pi-lens-ignore: go-bare-error
}

func digest(data []byte) string {
	sum := sha256.Sum256(data)
	return hex.EncodeToString(sum[:])
}
