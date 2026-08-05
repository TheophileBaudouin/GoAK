# KitV2 Permanent Audit Prompt Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a metaproject-only Pi prompt template that performs a read-only, complete, charter-grounded audit of the consumable `KitV2/` tree and reports placement pollution between the metaproject and the Kit.

**Architecture:** The prompt uses Pi project prompt-template frontmatter (`description` and `argument-hint`) and a five-pass audit: scope/inventory, typed inspection, cross-artifact checks, coverage reconciliation, and report assembly. It never edits files and keeps inspection separate from recommendations. Existing Python validators are treated as evidence and gap inputs, not reimplemented blindly.

**Tech Stack:** Markdown prompt template, Pi prompt-template substitution, POSIX/read-only repository commands, existing Python validators, `KIT_CHARTER.md`, and KitV2 metadata/artifact conventions.

---

## Task 1: Draft the metaproject prompt template

**Files:**

- Create: `.pi/prompts/kit-audit.md`

### Step 1: Encode invocation and scope

Use Pi-compatible frontmatter, accept an optional target argument, default to `KitV2/`, and explicitly separate the metaproject from the consumable product.

### Step 2: Encode read-only audit phases

Require a dated complete inventory before inspection, per-file coverage status, dynamic artifact typing, charter/rules/source/relationship/language/duplication checks, and explicit `metaproject` versus `Kit` placement classification.

### Step 3: Encode report contract

Require per-dimension verdicts (`CONFORME`, `NON CONFORME`, `À VÉRIFIER`), precise charter citations, confidence/risk labels, inventory reconciliation, validator-gap recommendations, and no automatic remediation.

## Task 2: Validate the artifact without auditing KitV2

**Files:**

- Inspect: `.pi/prompts/kit-audit.md`
- Inspect: `install.sh`

### Step 1: Check prompt format

Confirm frontmatter fields match Pi documentation and the filename maps to `/kit-audit`.

### Step 2: Check boundary placement

Inventory the installer extraction path and prove the new prompt is outside `KitV2/` and is not copied by `install.sh`.

### Step 3: Check changed-file diagnostics

Run only prompt/file-format diagnostics; because the existing metaproject validator only discovers `KitV2/.pi/prompts/*.md`, validate the root prompt manually. Do not invoke the new prompt and do not run the audit against the real `KitV2/` tree.

## Task 3: Independent fresh-context review

Have a read-only reviewer inspect the prompt for source fidelity, completeness, read-only guarantees, coverage reconciliation, and meta-project/Kit pollution analysis. Apply only confirmed corrections in the parent session.
