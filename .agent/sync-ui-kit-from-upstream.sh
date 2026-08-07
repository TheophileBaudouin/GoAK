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
#          required tools present (git, rsync, python3 + PyYAML, perl, node);
#          the upstream repo must resolve the SHA and expose sdk/.
#   POST - upstream sdk/ vs KitV2/ui-kit/ must differ only in the local-owned
#          files (PIN.md, scenarios.json, copy-rules.json) plus the dead
#          .pi/settings.json exclusion (single registration point,
#          D-2026-08-08-02);
#          the merged UI section of KitV2/AGENTS.md must mirror the pinned
#          ui-kit/AGENTS.md (checksum marker — a changed SDK AGENTS.md blocks
#          the sync until the prose is updated, owner rule 2026-08-08);
#          no .go file may enter the zone (the Go gate would compile it);
#          no metaproject path markers, no zero-byte .md, English only;
#          the FULL validation gate must pass: validators (instructions,
#          cognitive, kitv2), router index check, Go + UI scenario gates,
#          router unit tests (stdlib unittest — pytest is NOT a CI
#          dependency, gotcha 2026-08-07), gofmt, go vet, golangci-lint,
#          go test -race, gosec, govulncheck, probes. Any failure exits 1
#          with rollback instructions.
#
# The helper only ever writes inside KitV2/ui-kit/ (plus the pin record and
# the merged-AGENTS.md checksum marker in KitV2/AGENTS.md).
# Nothing is committed automatically: the maintainer reviews `git diff` and
# commits; a failed gate is rolled back with `git restore`.
#
# Usage:
#   bash .agent/sync-ui-kit-from-upstream.sh <new-sha>               # sync + full gate
#   bash .agent/sync-ui-kit-from-upstream.sh <new-sha> --no-verify  # sync only
#   bash .agent/sync-ui-kit-from-upstream.sh --check                # pin vs tree (+ upstream drift)
set -eu

ROOT=$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)
UI_KIT="$ROOT/KitV2/ui-kit"
UPSTREAM="https://github.com/TheophileBaudouin/ui-agent-kit"
LOCAL_OWNED="PIN.md scenarios.json copy-rules.json" # never overwritten by a sync
# The nested sdk/.pi/ directory is DEAD machinery (D-2026-08-08-02): the UI
# skills are registered in the root KitV2/.pi/settings.json (single
# registration point). Upstream sdk/ still carries .pi/settings.json, so the
# whole .pi dir is excluded from BOTH the diff and the rsync — a nested
# settings file can never be resurrected, and a re-sync never flags it.
# NOTE: diff --exclude matches basenames only (a pattern with a slash would
# never match), hence the bare `.pi` — rsync would accept `.pi/settings.json`
# but the whole-dir exclusion is the consistent contract.
# shellcheck disable=SC2086 # intentional word-splitting into --exclude args
EXCLUDES="--exclude=PIN.md --exclude=scenarios.json --exclude=copy-rules.json --exclude=.pi"

# The lint/security tools (golangci-lint, gosec, govulncheck) install into
# $(go env GOPATH)/bin and are not on PATH by default (gotcha 2025-07-31).
GOPATH_BIN="$(go env GOPATH 2>/dev/null || echo "$HOME/go")/bin"
export PATH="$PATH:$GOPATH_BIN"

GATE_HINT="(cd KitV2 && python3 tools/validators/validate-kitv2.py) && node .agent/router/run_scenarios.mjs && node .agent/router/run_ui_scenarios.mjs && (cd .agent && PYTHONPATH=.. python3 -m unittest discover -s router -q) && (cd KitV2 && gofmt/vet/golangci-lint/test-race/gosec/govulncheck + bash probes/run.sh)"

rollback() {
	echo
	echo "sync-ui-kit: ROLLBACK (nothing was committed):"
	echo "  git restore -- KitV2/ui-kit KitV2/ui-kit/PIN.md"
	echo "The working tree is back to the last commit."
}

# ---------------------------------------------------------------------------
# prerequisite tools (clear error instead of a mid-script command-not-found)
# ---------------------------------------------------------------------------
missing=""
for tool in git rsync python3 perl node; do
	command -v "$tool" >/dev/null 2>&1 || missing="$missing $tool"
done
if ! python3 -c 'import yaml' >/dev/null 2>&1; then
	missing="$missing PyYAML(python3)"
fi
if [ -n "$missing" ]; then
	echo "sync-ui-kit: missing required tool(s):$missing" >&2
	exit 2
fi

# ---------------------------------------------------------------------------
# --check mode: pin vs tree (local) + upstream drift (network, read-only)
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
	head=$(git ls-remote "$UPSTREAM" HEAD 2>/dev/null | awk '{print $1}')
	if [ -n "$head" ]; then
		if [ "$head" = "$pinned" ]; then
			echo "sync-ui-kit: zone is up to date with upstream HEAD ($pinned)"
		else
			echo "sync-ui-kit: UPSTREAM DRIFT — pinned $pinned, upstream HEAD $head"
			echo "sync-ui-kit: run: bash .agent/sync-ui-kit-from-upstream.sh $head"
		fi
	else
		echo "sync-ui-kit: warning — cannot reach $UPSTREAM (offline?); pin-vs-tree check only" >&2
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
echo "sync-ui-kit: diffing upstream sdk/ vs KitV2/ui-kit/ (excluding $LOCAL_OWNED + dead .pi dir)"
# shellcheck disable=SC2086 # $EXCLUDES splits into --exclude args on purpose
diff -rq $EXCLUDES "$src" "$UI_KIT" || true

# shellcheck disable=SC2086 # $EXCLUDES splits into --exclude args on purpose
echo "sync-ui-kit: copying upstream sdk/ -> KitV2/ui-kit/"
rsync -a $EXCLUDES "$src"/ "$UI_KIT"/

# generate copy-rules.json (local-owned) from the upstream SDK's own manifest
# — structure evolution is handled HERE, the consumer tool never hardcodes a
# path. Rules map zone-relative source -> frontend-relative destination.
# A failure here aborts with rollback: the zone is already modified.
manifest="$tmp/repo/cli/manifest.json"
if [ -f "$manifest" ]; then
	python3 - "$manifest" "$UI_KIT/copy-rules.json" <<'PY' || {
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
		rollback
		exit 1
	}
else
	echo "sync-ui-kit: WARNING upstream cli/manifest.json missing — copy-rules.json not regenerated (zone keeps the previous one)" >&2
fi

# update the pin record (single-quoted perl: no shell interpolation/backticks —
# $ENV is a perl variable, not a shell one)
# shellcheck disable=SC2016
today="$(date +%Y-%m-%d)"
export NEW_SHA="$new_sha" TODAY="$today"
perl -0pi -e 's/\| Pinned commit \(SHA\) \| `[0-9a-f]{40}` \|/| Pinned commit (SHA) | `$ENV{NEW_SHA}` |/; s/\| Commit date \| \d{4}-\d{2}-\d{2} \|/| Commit date | $ENV{TODAY} |/; s/\| Sync date \| \d{4}-\d{2}-\d{2} \|/| Sync date | $ENV{TODAY} |/' "$UI_KIT/PIN.md" || {
	rollback
	exit 1
}
if ! grep -q "$new_sha" "$UI_KIT/PIN.md"; then
	echo "sync-ui-kit: FAIL — PIN.md does not contain the new SHA $new_sha after the update (pin record format changed?)" >&2
	rollback
	exit 1
fi

# ---------------------------------------------------------------------------
# POST-SYNC guardrails (structural, cheap — always run)
# ---------------------------------------------------------------------------
echo
echo "sync-ui-kit: post-sync structural checks"
postfail=0

# shellcheck disable=SC2086 # $EXCLUDES splits into --exclude args on purpose
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
	if ! python3 - "$UI_KIT/copy-rules.json" <<'PY'; then
import json, os, sys
rules = json.load(open(sys.argv[1], encoding="utf-8"))
missing = [r["src"] for r in rules if not os.path.isdir(os.path.join(sys.argv[1].rsplit("/", 1)[0], r["src"]))]
if missing:
    print("sync-ui-kit: FAIL — copy-rule sources missing in the zone: " + ", ".join(missing), file=sys.stderr)
    sys.exit(1)
PY
		postfail=1
	fi
fi

# registration integrity (single registration point, D-2026-08-08-02): the
# root settings.json must keep declaring the UI skills and the dead nested
# file must never be resurrected.
if ! grep -q '"../ui-kit/skills"' "$ROOT/KitV2/.pi/settings.json" 2>/dev/null; then
	echo "sync-ui-kit: FAIL — root .pi/settings.json no longer declares ../ui-kit/skills (registration lost, D-2026-08-08-02)." >&2
	postfail=1
fi
if [ -e "$UI_KIT/.pi/settings.json" ]; then
	echo "sync-ui-kit: FAIL — nested ui-kit/.pi/settings.json present (dead file must stay excluded, D-2026-08-08-02)." >&2
	postfail=1
fi

# merged AGENTS.md freshness (owner rule 2026-08-08): the "UI work" section
# of KitV2/AGENTS.md mirrors the pinned ui-kit/AGENTS.md; the checksum marker
# in its HTML comment must match the synced file. A drift means the SDK
# instructions changed and the merged prose was not updated — the sync
# blocks until the maintainer updates it (the marker refreshes on gate PASS).
AGENTS_ROOT="$ROOT/KitV2/AGENTS.md"
zone_agents_sha=$(shasum -a 256 "$UI_KIT/AGENTS.md" 2>/dev/null | awk '{print $1}')
marker=$(sed -n 's/.*ui-kit\/AGENTS\.md sha256: \([0-9a-f]\{64\}\).*/\1/p' "$AGENTS_ROOT" 2>/dev/null | head -1)
if [ -z "$zone_agents_sha" ]; then
	echo "sync-ui-kit: FAIL — cannot checksum $UI_KIT/AGENTS.md (shasum missing?)" >&2
	postfail=1
elif [ -z "$marker" ]; then
	echo "sync-ui-kit: FAIL — no ui-kit/AGENTS.md sha256 marker found in KitV2/AGENTS.md; add the marker to the merged UI section." >&2
	postfail=1
elif [ "$marker" != "$zone_agents_sha" ]; then
	echo "sync-ui-kit: FAIL — the merged UI section of KitV2/AGENTS.md is STALE: ui-kit/AGENTS.md changed in this sync." >&2
	echo "          Update the section prose to mirror the new SDK instructions (never lose an instruction from either file)" >&2
	echo "          AND refresh its sha256 marker comment, then re-run." >&2
	postfail=1
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
echo "sync-ui-kit: structural checks OK (diff clean, registration intact, merged AGENTS.md fresh, no .go, no markers, no empty .md, English)"

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
run_gate "Go scenarios" node --no-warnings "$ROOT/.agent/router/run_scenarios.mjs"
run_gate "UI scenarios" node --no-warnings "$ROOT/.agent/router/run_ui_scenarios.mjs"
run_gate "router unit tests" sh -c "cd '$ROOT/.agent' && PYTHONPATH=.. python3 -m unittest discover -s router -q"
run_gate "gofmt" sh -c "cd '$ROOT/KitV2' && test -z \"\$(gofmt -l .)\""
run_gate "go vet" sh -c "cd '$ROOT/KitV2' && go vet ./..."
run_gate "golangci-lint" sh -c "cd '$ROOT/KitV2' && golangci-lint run ./..."
run_gate "go test -race" sh -c "cd '$ROOT/KitV2' && go test -race ./..."
run_gate "gosec" sh -c "cd '$ROOT/KitV2' && gosec ./..."
run_gate "govulncheck" sh -c "cd '$ROOT/KitV2' && govulncheck ./..."
run_gate "probes" sh -c "cd '$ROOT/KitV2' && bash probes/run.sh >/dev/null && echo 'probes PASS'"

if [ "$gate_failed" = 1 ]; then
	echo "sync-ui-kit: FULL GATE FAILED — do NOT commit." >&2
	rollback
	exit 1
fi

echo
echo "sync-ui-kit: FULL GATE PASS — the zone is clean and verified."
echo "Next steps (manual):"
echo "  1. git diff --stat KitV2/ui-kit KitV2/AGENTS.md   (review the upstream change + the merged UI section)"
echo "  2. git add KitV2/ui-kit KitV2/AGENTS.md && git commit"
echo "  3. Record in .pi/memory/Decisions.md + docs/evidence/ (dated, per charter)"
echo "Silent or automatic updates are forbidden (Z13)."
