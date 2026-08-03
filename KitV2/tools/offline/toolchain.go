package offline

import (
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"path/filepath"
	"strings"
)

func (r *Resolver) resolveLocal(ctx context.Context, result Result, q Query) Result {
	var data []byte
	var err error
	unit := q.Unit
	switch {
	case strings.HasPrefix(unit, "help:"):
		data, err = r.goOutput(ctx, []string{"help", strings.TrimPrefix(unit, "help:")}, q.Online)
	case strings.HasPrefix(unit, "cmd:"):
		name := strings.TrimPrefix(unit, "cmd:")
		if name != "gofmt" && name != "pprof" && name != "trace" {
			result.Prerequisite = "request cmd:gofmt, cmd:pprof, or cmd:trace"
			return result
		}
		goroot, envErr := r.goOutput(ctx, []string{"env", "GOROOT"}, false)
		if envErr != nil {
			result.Prerequisite = "install a local Go toolchain"
			return result
		}
		path := filepath.Join(strings.TrimSpace(string(goroot)), "src", "cmd", name, "doc.go")
		data, err = readFile(path) // #nosec G304 -- command is a fixed allowlist and GOROOT comes from go env
	default:
		data, err = r.goOutput(ctx, []string{"doc", "-short", unit}, q.Online)
	}
	if err != nil || len(data) == 0 {
		result.Prerequisite = prerequisite(unit, q.Online)
		return result
	}
	version, versionErr := r.goOutput(ctx, []string{"version"}, false)
	if versionErr != nil {
		result.Prerequisite = "install a local Go toolchain"
		return result
	}
	pin := strings.TrimSpace(string(version))
	sourceHash := digest(data)
	if q.GoVersion != "" && !compatibleVersion(pin, q.GoVersion) {
		result.Status = StatusStale
		result.Provenance = Provenance{Pin: pin, SHA256: sourceHash, Verifier: "toolchain-local"}
		return result
	}
	result.Status = StatusHit
	result.Matches = []Match{{Unit: unit, SHA256: sourceHash, Excerpt: excerpt(data, q)}}
	result.Provenance = Provenance{Pin: pin, SHA256: sourceHash, Verifier: "toolchain-local"}
	return result
}

func prerequisite(unit string, online bool) string {
	if strings.HasPrefix(unit, "help:") || strings.HasPrefix(unit, "cmd:") {
		return "install a local Go toolchain"
	}
	if online {
		return fmt.Sprintf("run go doc -short %s with a reachable module/toolchain", unit)
	}
	return fmt.Sprintf("cache the package locally, then run go doc -short %s", unit)
}

func (r *Resolver) goOutput(ctx context.Context, args []string, online bool) ([]byte, error) {
	cmd := exec.CommandContext(ctx, r.goBin, args...) // #nosec G204 -- goBin is configured by the trusted product and args are fixed resolver commands
	cmd.Env = append([]string(nil), r.env...)
	cmd.Env = append(cmd.Env, "GOTOOLCHAIN=local")
	if !online {
		cmd.Env = append(cmd.Env, "GOPROXY=off", "GOSUMDB=off", "GONOSUMDB=*")
	}
	return cmd.Output()
}

func resolveModule(ctx context.Context, r *Resolver, q Query, modules []module) (Result, bool) {
	for _, candidate := range modules {
		if candidate.Path != q.Unit {
			continue
		}
		args := []string{"mod", "download", "-json", candidate.Path + "@" + candidate.Version}
		data, err := r.goOutput(ctx, args, q.Online)
		if err != nil {
			return Result{Protocol: Protocol, Status: StatusBlocked, Source: q.Source, Unit: q.Unit, Prerequisite: fmt.Sprintf("cache module %s@%s", candidate.Path, candidate.Version)}, true
		}
		directory, sum, parseErr := parseDownloadJSON(data)
		if parseErr != nil {
			return Result{Protocol: Protocol, Status: StatusMiss, Source: q.Source, Unit: q.Unit, Prerequisite: parseErr.Error()}, true
		}
		content, readErr := readFile(filepath.Join(directory, "README.md")) // #nosec G304 -- directory is returned by go mod download
		if readErr != nil {
			return Result{Protocol: Protocol, Status: StatusBlocked, Source: q.Source, Unit: q.Unit, Prerequisite: fmt.Sprintf("read cached module documentation at %s", directory)}, true
		}
		result := Result{Protocol: Protocol, Status: StatusHit, Source: q.Source, Unit: q.Unit}
		contentHash := digest(content)
		result.Matches = []Match{{Unit: q.Unit, SHA256: contentHash, Excerpt: excerpt(content, q)}}
		result.Provenance = Provenance{Pin: candidate.Version, SHA256: sum, Verifier: "module-sum"}
		return result, true
	}
	return Result{}, false
}

func parseDownloadJSON(data []byte) (string, string, error) {
	var response struct {
		Dir string `json:"Dir"`
		Sum string `json:"Sum"`
	}
	if err := json.Unmarshal(data, &response); err != nil {
		return "", "", err
	}
	if response.Dir == "" || response.Sum == "" {
		return "", "", fmt.Errorf("module download response lacks Dir or Sum")
	}
	return response.Dir, response.Sum, nil
}
