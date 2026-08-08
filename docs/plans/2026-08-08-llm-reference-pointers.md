# Plan — LLM/ML reference-technology pointers (2026-08-08)

## Goal

Add 5 reference-technology pointers to KitV2's catalog (`knowledge/catalogs/
libraries/pointers/`) for the kit's LLM/agent direction: llama.cpp, MLX
(+ MLX-LM, MLX Swift LM), Outlines, DSPy, Langfuse. Pointer-only admission
(`status: proposed`, `kind: Source`) — none is a Go library, so none passes
the 9-criteria admission gate; they are reference sources for when the kit's
decision order reaches "existing vetted external capability".

## Context

- Owner-supplied reference document (French) listing 5 proven LLM/ML
  technologies and their rationale ("when no Go alternative offers equivalent
  power/stability/ecosystem, rely on these proven solutions"). The document
  itself is NOT admitted verbatim — the language rule (D-2026-08-05-21)
  mandates English for all artifacts; pointer content is translated.
- Precedent: `pointers/adk-go.yaml`, `pointers/eino.yaml` — same shape
  (id `source:<domain>:<slug>`, `status: proposed`, selection + limits +
  references).
- Doctrine (owner clarification 2026-08-08): NO conflict with the kit
  decision order. The order stays Go-native first, smallest effective
  solution first. When stdlib/Go-native cannot satisfy a real need and the
  reference technology is the best in its domain, choosing it IS the
  smallest effective solution — less code to develop, better quality. The
  pointers record when each technology applies (`selection`) and when it
  does not (`limits`); when the why-use conditions hold and no why-not
  blocks, taking the library is the correct decision, consistent with the
  kit philosophy. Decision order unchanged; nothing baked in.
- All 5 repos verified live 2026-08-08 via GitHub API (stars, license,
  latest release, push activity, archived flag).

## Constraints

- English only. One artifact per technology. `id` matches
  `source:llm:<slug>` / `source:observability:langfuse` (GRAPH_ID_RE).
- No catalog SKILL.md, no SKILL format (non-Go, not vetted libraries).
- Every pointer: `status: proposed`, `kind: Source`, `go_version` kept to
  kit minimum (`"1.25+"`) with the technology's own language noted in tags.
- Registry (`metaproject`): add the 5 sources to section 18 (IA / LLM),
  matching existing entry format.
- Gate: regenerate router index, run product + metaproject validators,
  router scenarios must still pass (no ranking shift regression).

## Done

- [ ] 5 pointer YAMLs created (llama-cpp, mlx, outlines, dspy, langfuse)
- [ ] Registry section 18 updated with the 5 sources
- [ ] `build_index.py` regenerated, zone contract count 5→10 updated
- [ ] validate-instructions.py / validate-kitv2.py / validate-cognitive.py PASS
- [ ] router scenarios PASS (22/22 + UI)
- [ ] Fresh-context review notes + memory updated
