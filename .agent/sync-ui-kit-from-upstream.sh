#!/bin/sh
# sync-ui-kit-from-upstream.sh — refresh the pinned ui-kit zone (metaproject
# only, never shipped). This is the ONLY sanctioned update path for
# KitV2/ui-kit content (Z13 §4): manual (the maintainer invokes it), gated
# (it RUNS the full validation gate before reporting success), never
# automatic or silent.
#
# Guardrails (the "no damage" contract):
#   PRE  - the new SHA must be a well-formed 40-hex commit;
#          the working tree must be clean for KitV2/ui-kit/ (a dirty zone
#          would be clobbered by the sync — abort instead);
#          the upstream repo must resolve the SHA and expose sdk/.
#   POST - upstream sdk/ vs KitV2/ui-kit/ must differ only in the local-owned
#          files (PIN.md, scenarios.json);
#          no .go file may enter the zone (the Go gate would compile it);
#          no metaproject path markers, no zero-byte .md, English only;
#          the FULL validation gate must pass (validators, router Go + UI
#          gates, router tests, gofmt/vet/lint/test-race/gosec/govulncheck,
#          probes). Any failure exits 1 with rollback instructions.
#
# The helper only ever writes inside KitV2/ui-kit/ (plus the pin record).
# Nothing is committed automatically: the maintainer reviews `git diff` and
# commits; a failed gate is rolled back with `git restore`.
#
# Usage:
#   bash .agent/sync-ui-kit-from-upstream.sh <new-sha>          # sync + full gate
#   bash .agent/sync-ui-kit-from-upstream.sh <new-sha> --no-verify   # sync only
#   bash .agent/sync-ui-kit-from-upstream.sh --check           # pin vs tree
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
UI_KIT="$ROOT/KitV2/ui-kit"
UPSTREAM="https://github.com/TheophileBaudouin/ui-agent-kit"
LOCAL_OWNED="PIN.md scenarios.json copy-rules.json" # never overwritten by a sync
# .pi/settings.json is deliberately ABSENT from the zone: the UI skills are
# registered in the root KitV2/.pi/settings.json (single registration point,
# mission 2026-08-08). Upstream sdk/ still carries .pi/settings.json, so it
# must stay excluded here or every re-sync would resurrect the dead file.
EXCLUDES="--exclude=PIN.md --exclude=scenarios.json --exclude=copy-rules.json --exclude=.pi/settings.json"
GATE_HINT="(cd KitV2 && python3 tools/validators/validate-kitv2.py) && node .agent/router/run_scenarios.mjs && node .agent/router/run_ui_scenarios.mjs && (cd .agent && python3 -m pytest router/ -q) && (cd KitV2 && gofmt/vet/lint/test-race/gosec/govulncheck + bash probes/run.sh)"

rollback() {
	echo
	echo "sync-ui-kit: ROLLBACK (nothing was committed):"
	echo "  git restore -- KitV2/ui-kit KitV2/ui-kit/PIN.md"
	echo "The working tree is back to the last commit."
}

# ---------------------------------------------------------------------------
# --check mode
# ---------------------------------------------------------------------------
if [ "${1:-}" = "--check" ]; then
	pinned=$(grep -m1 'Pinned commit (SHA)' "$UI_KIT/PIN.md" | sed -E 's/.*`([0-9a-f]{40})`.*/\1/')
	echo "PIN.md pinned sha: $pinned"
	[ -n "$pinned" ] || {
		echo "sync-ui-kit: no pinned SHA found in PIN.md" >&2
		exit 1
	}
	if [ -n "$(git -C "$ROOT" status --porcelain -- KitV2/ui-kit)" ]; then
		echo "sync-ui-kit: working tree has ui-kit changes (tracked or untracked) — re-sync pending or local drift" >&2
		git -C "$ROOT" status --short -- KitV2/ui-kit >&2
		exit 1
	fi
	echo "sync-ui-kit: pin check OK (zone committed, tree clean)"
	exit 0
fi

# ---------------------------------------------------------------------------
# parse args
# ---------------------------------------------------------------------------
new_sha=""
verify=1
for arg in "$@"; do
	case "$arg" in
	--no-verify) verify=0 ;;
	--check) : ;; # handled above
	*)
		[ -z "$new_sha" ] || {
			echo "sync-ui-kit: unexpected extra argument: $arg" >&2
			exit 2
		}
		new_sha=$arg
		;;
	esac
done
[ -n "$new_sha" ] || {
	echo "usage: sync-ui-kit-from-upstream.sh <new-sha> [--no-verify] | --check" >&2
	exit 2
}

# ---------------------------------------------------------------------------
# PRE-FLIGHT guardrails
# ---------------------------------------------------------------------------
case "$new_sha" in
*[!0-9a-f]* | '')
	echo "sync-ui-kit: <new-sha> must be a 40-hex commit SHA (got: $new_sha)" >&2
	exit 2
	;;
esac
if [ "${#new_sha}" -ne 40 ]; then
	echo "sync-ui-kit: <new-sha> must be a 40-hex commit SHA (got: $new_sha)" >&2
	exit 2
fi

if [ -n "$(git -C "$ROOT" status --porcelain -- KitV2/ui-kit)" ]; then
	echo "sync-ui-kit: ABORT — KitV2/ui-kit has uncommitted or untracked changes; commit or restore them first (the sync would clobber local drift)." >&2
	git -C "$ROOT" status --short -- KitV2/ui-kit >&2
	exit 1
fi

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

echo "sync-ui-kit: fetching $UPSTREAM @ $new_sha"
git clone --quiet --no-checkout --filter=blob:none "$UPSTREAM" "$tmp/repo" 2>/dev/null ||
	{
		echo "sync-ui-kit: clone failed — check network/access to $UPSTREAM" >&2
		exit 1
	}
git -C "$tmp/repo" checkout --quiet "$new_sha" ||
	{
		echo "sync-ui-kit: cannot checkout $new_sha (does it exist upstream?)" >&2
		exit 1
	}

src="$tmp/repo/sdk"
[ -d "$src" ] || {
	echo "sync-ui-kit: upstream sdk/ not found at $new_sha" >&2
	exit 1
}

# ---------------------------------------------------------------------------
# SYNC (writes only inside KitV2/ui-kit/)
# ---------------------------------------------------------------------------
echo "sync-ui-kit: diffing upstream sdk/ vs KitV2/ui-kit/ (excluding $LOCAL_OWNED)"
diff -rq $EXCLUDES "$src" "$UI_KIT" || true

echo "sync-ui-kit: copying upstream sdk/ -> KitV2/ui-kit/"
rsync -a $EXCLUDES "$src"/ "$UI_KIT"/

# generate copy-rules.json (local-owned) from the upstream SDK's own manifest
# — structure evolution is handled HERE, the consumer tool never hardcodes a
# path. Rules map zone-relative source -> frontend-relative destination.
manifest="$tmp/repo/cli/manifest.json"
if [ -f "$manifest" ]; then
	python3 - "$manifest" "$UI_KIT/copy-rules.json" <<'PY'
import json, sys
src_manifest, out = sys.argv[1], sys.argv[2]
with open(src_manifest, encoding="utf-8") as f:
    m = json.load(f)
rules = []
for r in m.get("copyRules", []):
    frm = r.get("from", "")
    if frm == "sdk":
        continue  # the zone mirror itself, implicit in the consumer tool
    if not frm.startswith("sdk/"):
        print(f"sync-ui-kit: ERROR unexpected copy rule source {frm!r} (outside sdk/)", file=sys.stderr)
        sys.exit(1)
    rules.append({"src": frm[len("sdk/"):], "dst": r.get("to", "")})
with open(out, "w", encoding="utf-8") as f:
    json.dump(rules, f, indent=1)
    f.write("\n")
print(f"sync-ui-kit: wrote copy-rules.json ({len(rules)} code rules)")
PY
else
	echo "sync-ui-kit: WARNING upstream cli/manifest.json missing — copy-rules.json not regenerated (zone keeps the previous one)" >&2
fi


# update the pin record (single-quoted perl: no shell interpolation/backticks)
today=$(date +%Y-%m-%d)
export NEW_SHA="$new_sha" TODAY="$today"
perl -0pi -e 's/\| Pinned commit \(SHA\) \| `[0-9a-f]{40}` \|/| Pinned commit (SHA) | `$ENV{NEW_SHA}` |/; s/\| Commit date \| \d{4}-\d{2}-\d{2} \|/| Commit date | $ENV{TODAY} |/; s/\| Sync date \| \d{4}-\d{2}-\d{2} \|/| Sync date | $ENV{TODAY} |/' "$UI_KIT/PIN.md"

# ---------------------------------------------------------------------------
# POST-SYNC guardrails (structural, cheap — always run)
# ---------------------------------------------------------------------------
echo
echo "sync-ui-kit: post-sync structural checks"
postfail=0

remaining=$(diff -rq $EXCLUDES "$src" "$UI_KIT" || true)
if [ -n "$remaining" ]; then
	echo "sync-ui-kit: FAIL — upstream sdk/ and KitV2/ui-kit/ differ beyond local-owned files:" >&2
	echo "$remaining" >&2
	postfail=1
fi


# required shape + copy-rule sources must exist in the zone (structure
# evolution tripwire: upstream restructured sdk/ -> adapt the GoAK side
# before shipping, never ship a broken zone)
for required in AGENTS.md skills ui-sdk; do
	if [ ! -e "$UI_KIT/$required" ]; then
		echo "sync-ui-kit: FAIL — zone missing '$required' (upstream restructured sdk/); adapt the GoAK side before shipping." >&2
		postfail=1
	fi
done
if [ -f "$UI_KIT/copy-rules.json" ]; then
	if ! python3 - "$UI_KIT/copy-rules.json" <<'PY'
import json, os, sys
rules = json.load(open(sys.argv[1], encoding="utf-8"))
missing = [r["src"] for r in rules if not os.path.isdir(os.path.join(sys.argv[1].rsplit("/", 1)[0], r["src"]))]
if missing:
    print("sync-ui-kit: FAIL — copy-rule sources missing in the zone: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)
PY
	then
		postfail=1
	fi
fi

if find "$UI_KIT" -name '*.go' | grep -q .; then
	echo "sync-ui-kit: FAIL — a .go file entered the zone; the Go gate would compile it (zone must stay Go-free)." >&2
	postfail=1
fi

if grep -rl '\.agent/' "$UI_KIT" --include='*.md' --include='*.yaml' --include='*.yml' --include='*.ts' --include='*.json' --include='*.txt' 2>/dev/null | grep -q .; then
	echo "sync-ui-kit: FAIL — metaproject path markers (.agent/) in shipped files (KVA-102)." >&2
	postfail=1
fi

if find "$UI_KIT" -name '*.md' -size 0 | grep -q .; then
	echo "sync-ui-kit: FAIL — zero-byte .md files in the zone (skill discovery breakage)." >&2
	postfail=1
fi

if grep -rlP '[àâäéèêëîïôöùûüçœæ]' "$UI_KIT" --include='*.md' --include='*.yaml' --include='*.yml' 2>/dev/null | grep -q .; then
	echo "sync-ui-kit: FAIL — accented-French content (language rule D-2026-08-05-21)." >&2
	postfail=1
fi

if [ "$postfail" = 1 ]; then
	rollback
	exit 1
fi
echo "sync-ui-kit: structural checks OK (diff clean, no .go, no markers, no empty .md, English)"

if [ "$verify" = 0 ]; then
	echo "sync-ui-kit: --no-verify given — FULL GATE SKIPPED. Do not commit before running it: $GATE_HINT"
	exit 0
fi

# ---------------------------------------------------------------------------
# FULL GATE (the real guardrail)
# ---------------------------------------------------------------------------
echo
echo "sync-ui-kit: running the FULL validation gate (this takes a few minutes)"
gate_failed=0
run_gate() {
	label=$1
	shift
	if "$@"; then
		echo "  PASS  $label"
	else
		echo "  FAIL  $label" >&2
		gate_failed=1
	fi
}

run_gate "validate-instructions" python3 "$ROOT/.agent/validators/validate-instructions.py"
run_gate "validate-cognitive" python3 "$ROOT/.agent/validators/validate-cognitive.py"
run_gate "validate-kitv2" sh -c "cd '$ROOT/KitV2' && python3 tools/validators/validate-kitv2.py"
run_gate "router index check" python3 "$ROOT/.agent/router/build_index.py" --check
run_gate "Go scenarios 22/22" node --no-warnings "$ROOT/.agent/router/run_scenarios.mjs"
run_gate "UI scenarios 9/9" node --no-warnings "$ROOT/.agent/router/run_ui_scenarios.mjs"
run_gate "router unit tests" sh -c "cd '$ROOT/.agent' && python3 -m pytest router/ -q"
run_gate "gofmt" sh -c "cd '$ROOT/KitV2' && test -z \"\$(gofmt -l .)\""
run_gate "go vet" sh -c "cd '$ROOT/KitV2' && go vet ./..."
run_gate "go test -race" sh -c "cd '$ROOT/KitV2' && go test -race ./..."
run_gate "probes" sh -c "cd '$ROOT/KitV2' && bash probes/run.sh >/dev/null && echo 'probes PASS'"

if [ "$gate_failed" = 1 ]; then
	echo "sync-ui-kit: FULL GATE FAILED — do NOT commit." >&2
	rollback
	exit 1
fi

echo
echo "sync-ui-kit: FULL GATE PASS — the zone is clean and verified."
echo "Next steps (manual):"
echo "  1. git diff --stat KitV2/ui-kit   (review the upstream change)"
echo "  2. git add KitV2/ui-kit && git commit"
echo "  3. Record in .pi/memory/Decisions.md + docs/evidence/ (dated, per charter)"
echo "Silent or automatic updates are forbidden (Z13)."
