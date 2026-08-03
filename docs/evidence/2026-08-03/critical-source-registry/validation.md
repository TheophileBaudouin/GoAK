# Validation — registre des sources critiques

Date: 2026-08-03

## Scope

- Registry: `.agent/sources/Go-dev-kit-sources-et-references.md`
- Plan: `docs/plans/2026-08-03-critical-source-registry-enrichment.md`
- Charter: `KIT_CHARTER.md`

## Deterministic structural checks

Command:

```sh
python3 - <<'PY'
from pathlib import Path
import re

p = Path('.agent/sources/Go-dev-kit-sources-et-references.md')
s = p.read_text()
urls = re.findall(r'https?://[^>\\s]+', s)
critical = s.count('**Priorité :** Critique')
print(f'bytes={len(s.encode())}')
print(f'urls={len(urls)} unique_urls={len(set(urls))}')
print(f'critical_entries={critical}')
for title in ('Go Language Specification', 'Go Modules', 'Go Toolchains', 'go command',
              'Go Testing', 'Go Fuzzing', 'Go Race Detector', 'Go Profiling',
              'govulncheck', 'gosec', 'golangci-lint', 'context', 'errors',
              'sync et sync/atomic', 'net/http', 'database/sql'):
    print(f'{title}: {"present" if f"## {title}" in s else "missing"}')
PY
```

Observed:

```text
bytes=18578
urls=59 unique_urls=59
critical_entries=27
Go Language Specification: present
Go Modules: present
Go Toolchains: present
go command: present
Go Testing: present
Go Fuzzing: present
Go Race Detector: present
Go Profiling: present
govulncheck: present
gosec: present
golangci-lint: present
context: present
errors: present
sync et sync/atomic: present
net/http: present
database/sql: present
```

## URL verification

A bounded HTTP check covered 59 unique registry URLs. Fifty-eight returned
HTTP 200 or an accepted redirect. `https://github.com/search` timed out at the
network boundary and remains unresolved; this is not treated as a pass.

The new official URLs corrected after the first review are:

- `https://pkg.go.dev/testing`
- `https://go.dev/doc/articles/race_detector`
- `https://go.dev/blog/pprof`

## Instruction validation

Command:

```sh
python3 .agent/validators/validate-instructions.py
```

Observed:

```text
instruction-artifacts: PASS
```

## Review status

- Fresh reviewers launched: yes.
- Review findings were inspected and corrected: yes.
- Final reviewer process completed: no; it exceeded its turn budget after
  producing substantive findings.
- Independent approval: PARTIAL; no completed approval response was produced.
- VCS-backed diff audit: BLOCKED; this workspace has no Git repository.
- Markdown diagnostics: no error-level findings. Existing heading-style
  warnings in the legacy registry are unchanged and non-blocking.
