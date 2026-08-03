#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
for probe in cli-minimal rest-chi sqlite-sqlc worker-shutdown offline; do
	printf '%s\n' "--- probes/$probe ---"
	(cd "$root" && go run "./probes/$probe")
done
