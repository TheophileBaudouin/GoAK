# Sourced templates evidence — 2026-08-05

## Admission decisions

Three sources passed the Z5 gate after primary-source review:

| Shape | Source and pin | License | Scope | Verification |
| --- | --- | --- | --- | --- |
| REST API | `leeprovoost/go-rest-api-template@4f2d17f700be3b355ff88986ca37c70ad2145cef` | MIT | stdlib-first HTTP REST | PASS |
| CLI | `danjdewhurst/go-toc@1f93495652ca789a75251f3cd6028b8f3adfc624` (`v0.3.0`) | MIT | Markdown TOC CLI | PASS |
| Worker | `sangianpatrick/go-workerpool@5d5c611c47489dda3b6e97cd277131d05c814bad` (`v1.0.1`) | MIT | bounded worker pool | PASS |

The source repositories were cloned at the pins. Their licenses, module files,
source-tree sizes, tests, and CI files were inspected. The copied projects pass
formatting, `go test -race ./...`, `go vet ./...`, and `govulncheck ./...`.

## Observable scenarios

- REST API: started with `VERSION=./cmd/api-service/VERSION PORT=18080
  ENV=LOCAL go run ./cmd/api-service`; `GET /healthcheck` and `GET /ready`
  returned JSON with HTTP 200. **PASS**.
- CLI: generated a Markdown TOC from a temporary directory containing `api.md`
  and `intro.md`; both files appeared in the output. **PASS**.
- Worker: submitted four jobs to a two-worker bounded pool, called `Stop`, and
  asserted all four handler calls completed. **PASS**.

## Removed legacy shapes

The inherited agent-authored scaffolds for `grpc`, `microservice`, `monolith`,
and `cloud-service` were removed. No candidate was admitted for these broad
shapes because no source was evidenced as simultaneously MIT-licensed,
maintained, tested, CI-backed, ultra-specific, small, and directly adaptable.
They remain roadmap entries; no empty or agent-authored replacement was created.

## Commands

The complete command output for the product gate is kept in
`commands.txt`. Source research reports and rejected candidates remain in the
metaproject evidence chain; each admitted template's `ATTRIBUTION.md` is the
consumer-facing source record.
