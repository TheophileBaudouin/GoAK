#!/bin/sh
# sync-ui-kit-from-upstream.sh — refresh the pinned ui-kit zone (metaproject
# only, never shipped). This is the ONLY sanctioned update path for
# KitV2/ui-kit content (Z13 §4): manual, revalidated, never automatic.
#
# Fetches the ui-agent-kit repository at a pinned commit SHA, diffs upstream
# sdk/ against KitV2/ui-kit/, updates PIN.md, and prints a verification
# checklist. Local-owned files (PIN.md, scenarios.json) are never clobbered.
#
# Usage:
#   bash .agent/sync-ui-kit-from-upstream.sh <new-sha>   # refresh the zone
#   bash .agent/sync-ui-kit-from-upstream.sh --check     # verify pin matches tree
#
# After a refresh, run the FULL validation gate before committing:
#   (cd KitV2 && python3 tools/validators/validate-kitv2.py)
#   node .agent/router/run_scenarios.mjs && node .agent/router/run_ui_scenarios.mjs
#   cd KitV2 && gofmt/vet/lint/test/race/gosec/govulncheck + bash probes/run.sh
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
UI_KIT="$ROOT/KitV2/ui-kit"
UPSTREAM="https://github.com/TheophileBaudouin/ui-agent-kit"
LOCAL_OWNED="PIN.md scenarios.json" # never overwritten by a sync

new_sha=""
if [ "${1:-}" = "--check" ]; then
	pinned=$(grep -m1 'Pinned commit (SHA)' "$UI_KIT/PIN.md" | sed -E 's/.*`([0-9a-f]{40})`.*/\1/')
	echo "PIN.md pinned sha: $pinned"
	[ -n "$pinned" ] || { echo "sync-ui-kit: no pinned SHA found in PIN.md" >&2; exit 1; }
	git -C "$ROOT" diff --quiet -- KitV2/ui-kit || {
		echo "sync-ui-kit: working tree has ui-kit changes — re-sync pending or local drift" >&2
		exit 1
	}
	echo "sync-ui-kit: pin check OK"
	exit 0
fi
new_sha="${1:-}"
if [ -z "$new_sha" ]; then
	echo "usage: sync-ui-kit-from-upstream.sh <new-sha> | --check" >&2
	exit 2
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

echo "sync-ui-kit: fetching $UPSTREAM @ $new_sha"
git clone --quiet --no-checkout --filter=blob:none "$UPSTREAM" "$tmp/repo" 2>/dev/null \
	|| { echo "sync-ui-kit: clone failed" >&2; exit 1; }
git -C "$tmp/repo" checkout --quiet "$new_sha" \
	|| { echo "sync-ui-kit: cannot checkout $new_sha (exists upstream?)" >&2; exit 1; }

src="$tmp/repo/sdk"
[ -d "$src" ] || { echo "sync-ui-kit: upstream sdk/ not found at $new_sha" >&2; exit 1; }

echo "sync-ui-kit: diffing upstream sdk/ vs KitV2/ui-kit/ (excluding $LOCAL_OWNED)"
diff -rq "$src" "$UI_KIT" 2>/dev/null | grep -vE "/(PIN|scenarios)\.md|scenarios\.json" || true

echo "sync-ui-kit: copying upstream sdk/ -> KitV2/ui-kit/"
rsync -a --exclude="PIN.md" --exclude="scenarios.json" "$src"/ "$UI_KIT"/

# update the pin record (single-quoted perl: no shell interpolation/backticks)
today=$(date +%Y-%m-%d)
export NEW_SHA="$new_sha" TODAY="$today"
perl -0pi -e 's/\| Pinned commit \(SHA\) \| `[0-9a-f]{40}` \|/| Pinned commit (SHA) | `$ENV{NEW_SHA}` |/; s/\| Commit date \| \d{4}-\d{2}-\d{2} \|/| Commit date | $ENV{TODAY} |/; s/\| Sync date \| \d{4}-\d{2}-\d{2} \|/| Sync date | $ENV{TODAY} |/' "$UI_KIT/PIN.md"

echo
echo "sync-ui-kit: PIN.md updated. Verify checklist before committing:"
echo "  1. git diff --stat KitV2/ui-kit           (intended upstream change?)"
echo "  2. diff -rq <upstream sdk/> KitV2/ui-kit  (only PIN.md/scenarios.json differ)"
echo "  3. No .go files, no .agent/ markers, no zero-byte .md, English only"
echo "  4. (cd KitV2 && python3 tools/validators/validate-kitv2.py)          # PASS"
echo "  5. node .agent/router/run_scenarios.mjs && node .agent/router/run_ui_scenarios.mjs"
echo "  6. Full Go gate + bash probes/run.sh"
echo "  7. Record the change in .pi/memory/Decisions.md + docs/evidence/"
echo "Silent or automatic updates are forbidden (Z13)."
