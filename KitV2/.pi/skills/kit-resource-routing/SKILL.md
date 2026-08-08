---
name: kit-resource-routing
category: workflow
tags: [router, search, discovery, index, routing]
last-verified: 2026-08-05
description: Route any technical task to the right kit resources with the search_kit_resources tool instead of scanning the kit tree. Use before planning or implementing any Go/architecture/HTTP/database/CLI/TUI work so only the relevant rules, recipes, catalogs, patterns, and snippets are loaded into context. Explains when to search, how to formulate queries, how to read results, when to open source files, and when to ignore a result.
---

# Kit resource routing

The kit ships a read-only routing index (`router/`) and a native tool
`search_kit_resources`. This skill defines the behavior around the tool; the
tool performs the action. Never replace the tool with manual tree scanning.

## When to search — MANDATORY before technical work

Call `search_kit_resources` **before planning or implementing** any technical
task that could map to kit resources, in particular:

- writing, reviewing, or refactoring Go code (errors, concurrency, HTTP,
  database, CLI, TUI, config, security, testing, observability);
- choosing between libraries or approaches;
- creating a project, service, or endpoint;
- answering a question about Go idioms, patterns, or pitfalls.

If the task is purely non-technical (wording, project memory, governance),
do not call the tool.

## How to formulate a query

- One concern per query. Split "I need a REST API with auth and a worker
  pool" into `rest api chi` and `bounded worker pool`.
- 3–8 technical terms, in English — the kit descriptions and index terms are
  English-only (fundamental language rule); a non-English
  query rarely matches.
- Name the concrete artifacts: `sqlc`, `errgroup`, `slog`, `wails`,
  `graceful shutdown`, `chi middleware`.
- Skip filler: `build a service with go` is weak; `chi rest api json` is
  strong.
- Default `limit` (5) protects context. Raise to 8 only for exploration;
  never return more than 8.

## How to interpret results

- The tool returns the top-K resources with a **score**, the **path**, the
  **matched terms** (why it matched), and a short description.
- Read the top 1–3. Treat the score as ordering only, never as an absolute
  truth.
- **Matched terms** tell you why a resource surfaced: if they overlap your
  real intent, read the file; if they only rhyme with it, ignore it.
- The output ends with the index coverage (how many resources of each kind
  exist) — useful to know whether a kind is absent from the kit.
- When you present the answer, use this shape per relevant resource:
  `path` (the result's file path), `matched terms` (matched terms /
  relevance), `description` (short), `recommended action` (what to read or
  run next — for a recipe: SKILL.md then the example and its test).

## When to read the source files

The index only routes; the kit files are the source of truth.

- Before relying on any result, open its `path` and read the resource itself.
- For recipes: read the SKILL.md, then the example and its test; run the
  example if the task depends on behavior.
- For rules/patterns: read the full rule before applying it.
- Never cite a resource from the tool output alone.

## When to ignore a result

- The matched terms are generic (`go`, `service`) and the description does
  not cover the actual need.
- The resource is a conditional catalog entry ("Consider when a consumer
  explicitly requires…") and the library was not requested.
- The query is off-domain: the tool then returns "No kit resource matches" —
  accept it. Do not force a resource to exist; proceed with general Go
  knowledge and say that the kit has no directly relevant resource.
- A single low-score match after a reformulation — prefer an empty answer
  over noise.

## Context protection (absolute)

- Never ask the tool to return full files or dozens of results.
- Never dump the kit tree into the conversation to "check what exists".
- Never load more than the resources you actually use; one resource found =
  one file read, not the whole zone.
- A weak result is dropped, never padded: an empty answer is better than
  context pollution.
