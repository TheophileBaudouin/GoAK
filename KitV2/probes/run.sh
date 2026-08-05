#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
for probe_dir in "$root"/probes/*/; do
	[ -f "$probe_dir/main.go" ] || continue
	probe=${probe_dir%/}
	probe=${probe##*/}
	printf '%s\n' "--- probes/$probe ---"
	(cd "$root" && go run "./probes/$probe")
done
