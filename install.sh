#!/bin/sh
# Go Agent Kit — one-command installer (bootstrap, tree-based version).
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/TheophileBaudouin/GoAK/v2.2.0/install.sh | sh -s -- [target-dir]
#
# Environment:
#   GAK_REF    git ref to install (default: v2.2.0). Use GAK_REF=main for the
#              latest branch head, or any tag/commit for a pinned install.
#   GAK_SKIP_VERIFY   set to 1 to skip the product verification step.
#   NO_COLOR          set to any value to disable colored output.
#
# This bootstrap installer materializes the standalone KitV2 product (the only
# consumable part of this repository) into a target directory. It never copies
# metaproject material (.agent/, memory, decisions, evaluations). The future
# `gak` CLI remains the canonical distribution entrypoint once a published
# module and release pipeline exist; this script is the interim for the first
# benchmarkable version.
set -eu

repo="TheophileBaudouin/GoAK"
ref="${GAK_REF:-v2.2.1}"
target="${1:-./go-agent-kit}"

# --- output helpers: minimal, portable (POSIX sh), auto-disabled ---
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ] && [ "${TERM:-}" != "dumb" ]; then
	C_RESET='\033[0m' C_BOLD='\033[1m' C_CYAN='\033[36m' C_GREEN='\033[32m'
	C_YELLOW='\033[33m' C_RED='\033[31m' C_DIM='\033[2m'
else
	C_RESET='' C_BOLD='' C_CYAN='' C_GREEN='' C_YELLOW='' C_RED='' C_DIM=''
fi

say() { printf '%b\n' "$*"; }
step() { printf '%b\n' "${C_CYAN}→${C_RESET} $*"; }
ok() { printf '%b\n' "${C_GREEN}✓${C_RESET} $*"; }
warn() { printf '%b\n' "${C_YELLOW}!${C_RESET} $*" >&2; }
die() {
	printf '%b\n' "${C_RED}✗${C_RESET} $*" >&2
	exit 1
}

# --- animation: standard rotating-line spinner (TTY only) ---
# Runs <cmd...> with a |/-\ spinner while it executes; returns the cmd rc.
# When stdout is not a TTY it just runs the command (no animation).
animate() {
	label=$1
	shift
	if [ ! -t 1 ]; then
		set +e
		"$@"
		rc=$?
		set -e
		return "$rc"
	fi
	"$@" &
	pid=$!
	i=0
	while kill -0 "$pid" 2>/dev/null; do
		# shellcheck disable=SC1003 # single backslash spinner frame
		case $((i % 4)) in
			0) ch='|' ;;
			1) ch='/' ;;
			2) ch='-' ;;
			3) ch='\' ;;
		esac
		printf '\r  %s %s' "$ch" "$label"
		i=$((i + 1))
		sleep 0.1
	done
	set +e
	wait "$pid"
	rc=$?
	set -e
	printf '\r  \033[K'
	return "$rc"
}

say ""
say "${C_BOLD}${C_CYAN}Go Agent Kit — installer${C_RESET} ${C_DIM}(ref ${ref} → ${target})${C_RESET}"
say ""

# --- prerequisites ---
step "checking prerequisites"
for tool in curl tar sed; do
	if ! command -v "$tool" >/dev/null 2>&1; then
		die "required tool '$tool' is missing (install it first)"
	fi
done
ok "curl, tar, sed available"

if [ -e "$target" ] && [ -n "$(ls -A "$target" 2>/dev/null)" ]; then
	die "target '$target' exists and is not empty — pick another directory or empty it"
fi

# --- download (animated) ---
tmp=$(mktemp -d "${TMPDIR:-/tmp}/gak-install.XXXXXX")
trap 'rm -rf "$tmp"' EXIT HUP INT TERM

url="https://codeload.github.com/$repo/tar.gz/$ref"
if ! animate "downloading ${repo}@${ref}" \
	curl -fsSL --retry 2 --retry-delay 1 "$url" -o "$tmp/repo.tgz"; then
	die "cannot download $url (check the ref and network)"
fi
size=$(wc -c <"$tmp/repo.tgz" | tr -d ' ')
ok "downloaded ${size} bytes"

# --- extract ---
step "extracting the KitV2 product tree"
top=$(tar -tzf "$tmp/repo.tgz" | sed -n '1s#^\([^/]*/\).*#\1#p')
if [ -z "$top" ]; then
	die "cannot determine archive layout"
fi

mkdir -p "$target"
# Extract only the KitV2/ product subtree, stripping the archive top-level and
# the KitV2 prefix so files land directly in $target (.pi/ included).
tar -xzf "$tmp/repo.tgz" -C "$target" --strip-components=2 "${top}KitV2"

if [ ! -f "$target/manifest.yaml" ]; then
	die "extracted tree has no manifest.yaml — install aborted"
fi

version=$(sed -n 's/^version: //p' "$target/manifest.yaml" | head -n 1)
[ -n "$version" ] || version="unknown"
ok "product tree extracted (manifest version ${version})"

# --- verify ---
if [ "${GAK_SKIP_VERIFY:-0}" = "1" ]; then
	warn "verification skipped (GAK_SKIP_VERIFY=1)"
else
	step "verifying product"
	# A missing toolchain is reported as PARTIAL, never as PASS.
	if command -v python3 >/dev/null 2>&1 && python3 -c 'import yaml' >/dev/null 2>&1; then
		if (cd "$target" && python3 tools/validators/validate-kitv2.py); then
			ok "verification: PASS"
		else
			die "product verification failed — install is incomplete"
		fi
	else
		warn "python3/PyYAML unavailable — verification PARTIAL (run"
		warn "  'cd $target && python3 tools/validators/validate-kitv2.py' later)"
	fi
fi

# --- summary ---
say ""
say "${C_GREEN}✓${C_RESET} ${C_BOLD}Go Agent Kit v${version} installed${C_RESET} ${C_DIM}(ref ${ref})${C_RESET}"
say ""
say "  ${C_BOLD}target${C_RESET}   ${target}"
say "  ${C_BOLD}next steps${C_RESET}"
say "    cd ${target}"
say "    pi                  # loads .pi/ prompts, skills and AGENTS.md"
say "    bash probes/run.sh  # runs the product probes (needs a Go toolchain)"
say ""
say "${C_DIM}Tree-based bootstrap install; the future \`gak\` CLI is the canonical"
say "distribution entrypoint once a published module and release pipeline exist.${C_RESET}"
say ""
