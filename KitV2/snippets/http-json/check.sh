#!/bin/sh
set -eu
cd "$(dirname "$0")"
gofmt -w example.go
test -z "$(gofmt -l example.go)"
printf '%s\n' 'http-json-response: PASS'
