#!/bin/sh
# Go Agent Kit — one-command installer (bootstrap, tree-based version).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.1.0/install.sh | sh -s -- [target-dir]
#
# Environment:
#   GAK_REF   git ref to install (default: v2.1.0). Use GAK_REF=main for the
#             latest branch head, or any tag/commit for a pinned install.
#
# This bootstrap installer materializes the standalone KitV2 product (the only
# consumable part of this repository) into a target directory. It never copies
# metaproject material (.agent/, memory, decisions, evaluations). The future
# `gak` CLI remains the canonical distribution entrypoint once a published
# module and release pipeline exist; this script is the interim for the first
# benchmarkable version.
set -eu

repo="TheophileBaudouin/GoAK"
ref="${GAK_REF:-v2.1.0}"
target="${1:-./go-agent-kit}"

for tool in curl tar; do
	if ! command -v "$tool" >/dev/null 2>&1; then
		echo "error: required tool '$tool' is missing" >&2
		exit 1
	fi
done

if [ -e "$target" ] && [ -n "$(ls -A "$target" 2>/dev/null)" ]; then
	echo "error: $target exists and is not empty; pick another directory or empty it" >&2
	exit 1
fi

echo "go-agent-kit: installing ref $ref into $target"

tmp=$(mktemp -d "${TMPDIR:-/tmp}/gak-install.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

url="https://codeload.github.com/$repo/tar.gz/$ref"
if ! curl -fsSL "$url" -o "$tmp/repo.tgz"; then
	echo "error: cannot download $url (check the ref and network)" >&2
	exit 1
fi

top=$(tar -tzf "$tmp/repo.tgz" | sed -n '1s#^\([^/]*/\).*#\1#p')
if [ -z "$top" ]; then
	echo "error: cannot determine archive layout" >&2
	exit 1
fi

mkdir -p "$target"
# Extract only the KitV2/ product subtree, stripping the archive top-level and
# the KitV2 prefix so files land directly in $target (.pi/ included).
tar -xzf "$tmp/repo.tgz" -C "$target" --strip-components=2 "${top}KitV2"

if [ ! -f "$target/manifest.yaml" ]; then
	echo "error: extracted tree has no manifest.yaml — install aborted" >&2
	exit 1
fi

version=$(sed -n 's/^version: //p' "$target/manifest.yaml" | head -n 1)
[ -n "$version" ] || version="unknown"

# Verification. A missing toolchain is reported as PARTIAL, never as PASS.
if command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' >/dev/null 2>&1; then
	if (cd "$target" && python3 tools/validators/validate-kitv2.py); then
		echo "verification: PASS"
	else
		echo "error: product verification failed — install is incomplete" >&2
		exit 1
	fi
else
	echo "warning: python3/PyYAML unavailable — verification PARTIAL (run"
	echo "         'cd $target && python3 tools/validators/validate-kitv2.py' later)"
fi

cat <<EOF

Go Agent Kit installed: $target (ref $ref, manifest version $version)

Next steps:
  cd $target
  pi                    # loads .pi/ prompts, skills and AGENTS.md
  bash probes/run.sh    # runs the product probes (needs a Go toolchain)

This is the tree-based bootstrap install; the future \`gak\` CLI is the
canonical distribution entrypoint once a published module and release
pipeline exist.
EOF
