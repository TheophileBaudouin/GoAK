#!/bin/sh
set -eu
cd "$(dirname "$0")"
test -z "$(gofmt -l example.go example_test.go)"
go test ./...
printf '%s\n' 'http-json-response: PASS'
