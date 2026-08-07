#!/bin/sh
# sync-ui-kit.sh — materialize the pinned ui-agent-kit SDK zone into a Wails
# project's frontend/ (Go Agent Kit, Z13).
#
# The ui-kit/ zone is a pinned, verbatim mirror of the upstream ui-agent-kit
# sdk/ (see ui-kit/PIN.md). This tool copies it into a real Wails project:
#   - ui-kit/            -> <frontend>/ui-kit/            (rules, patterns,
#                                                        skills, docs, code)
#   - ui-sdk code pieces -> <frontend>/src/components     (per the SDK copy
#                                                        rules)
#   - .pi/settings.json  -> wired with ["../ui-kit/skills"] (merge, never
#                                                        destructive)
#
# Wails detection (the "no trace" guarantee): the target must have wails.json
# AND a frontend/ directory with a package.json. Without both, the tool
# refuses with exit 1 and copies NOTHING — a non-Wails Go project never sees
# any SDK file.
#
# Idempotent: re-running refreshes SDK-owned files (force copy) and never
# deletes consumer files. Existing configs are never overwritten.
#
# Usage:
#   bash tools/sync-ui-kit.sh                 # detect in the current dir
#   bash tools/sync-ui-kit.sh --target <dir>  # explicit project root
#   bash tools/sync-ui-kit.sh --dry-run       # print actions, change nothing
set -eu

# --- locate the kit root (this script lives in <kit>/tools/) ---------------
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
KIT_ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
UI_KIT="$KIT_ROOT/ui-kit"

target=""
dry_run=0
while [ "$#" -gt 0 ]; do
	case "$1" in
	--target)
		target=$2
		shift 2
		;;
	--dry-run)
		dry_run=1
		shift
		;;
	*)
		echo "sync-ui-kit: unknown argument: $1" >&2
		exit 2
		;;
	esac
done

if [ -z "$target" ]; then
	target=$(pwd)
fi
target=$(CDPATH= cd -- "$target" 2>/dev/null && pwd) || {
	echo "sync-ui-kit: cannot resolve target: $target" >&2
	exit 2
}

# --- Wails detection --------------------------------------------------------
if [ ! -f "$target/wails.json" ]; then
	echo "sync-ui-kit: no wails.json in $target — not a Wails project; nothing copied (exit 1)." >&2
	exit 1
fi
frontend="$target/frontend"
if [ ! -f "$frontend/package.json" ]; then
	echo "sync-ui-kit: no frontend/package.json in $target — Wails frontend missing; nothing copied (exit 1)." >&2
	exit 1
fi

pin=$(grep -m1 '^| Pinned commit (SHA)' "$UI_KIT/PIN.md" 2>/dev/null | sed -E 's/.*`([0-9a-f]{7,})`.*/\1/')
[ -n "$pin" ] || pin="unknown"

echo "sync-ui-kit: Wails frontend detected at $frontend (pinned $pin)"
echo "sync-ui-kit: copying SDK from $UI_KIT"

# --- copy the SDK mirror ----------------------------------------------------
copy_dir() {
	# $1 source (kit-relative), $2 destination (frontend-relative)
	src="$KIT_ROOT/$1"
	dst="$frontend/$2"
	if [ ! -d "$src" ]; then
		echo "sync-ui-kit: warning: $1 missing in the kit — skipped"
		return 0
	fi
	if [ "$dry_run" = 1 ]; then
		echo "sync-ui-kit: [dry-run] copy $1 -> $2"
	else
		mkdir -p "$dst"
		cp -R "$src"/. "$dst"/
		echo "sync-ui-kit: copied $1 -> $2"
	fi
}

copy_dir "ui-kit" "ui-kit"
copy_dir "ui-kit/ui-sdk/components" "src/components"
copy_dir "ui-kit/ui-sdk/blocks/blocks-so" "src/components"
copy_dir "ui-kit/ui-sdk/examples/preferences-screen" "src/components/example"

# --- wire .pi/settings.json (merge, never destructive) ----------------------
wire_skills() {
	if [ "$dry_run" = 1 ]; then
		echo "sync-ui-kit: [dry-run] wire ../ui-kit/skills into $frontend/.pi/settings.json"
		return 0
	fi
	mkdir -p "$frontend/.pi"
	settings="$frontend/.pi/settings.json"
	if [ ! -f "$settings" ]; then
		printf '{\n  "skills": ["../ui-kit/skills"]\n}\n' >"$settings"
		echo "sync-ui-kit: created $settings"
		return 0
	fi
	if grep -q 'ui-kit/skills' "$settings"; then
		echo "sync-ui-kit: $settings already declares the SDK skills"
		return 0
	fi
	if command -v python3 >/dev/null 2>&1; then
		python3 - "$settings" <<'PY'
import json, sys
path = sys.argv[1]
try:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
except Exception:
    import shutil
    shutil.copyfile(path, path + ".bak")
    data = {}
skills = data.get("skills")
if not isinstance(skills, list):
    skills = []
if "../ui-kit/skills" not in skills:
    skills.append("../ui-kit/skills")
data["skills"] = skills
with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
    f.write("\n")
print(f"sync-ui-kit: wired ../ui-kit/skills into {path}")
PY
	else
		echo "sync-ui-kit: warning: $settings exists without the SDK skills and python3 is missing — add \"../ui-kit/skills\" to its \"skills\" array manually." >&2
	fi
}
wire_skills

# --- installed marker -------------------------------------------------------
if [ "$dry_run" = 1 ]; then
	echo "sync-ui-kit: [dry-run] write ui-kit/.ui-agent-kit.json"
else
	printf '{\n  "version": "%s",\n  "source": "goak-sync"\n}\n' "$pin" >"$frontend/ui-kit/.ui-agent-kit.json"
	echo "sync-ui-kit: wrote ui-kit/.ui-agent-kit.json (pinned $pin)"
fi

echo "sync-ui-kit: done. Read $frontend/ui-kit/AGENTS.md before UI work; UI skills are active when Pi runs inside $frontend."
