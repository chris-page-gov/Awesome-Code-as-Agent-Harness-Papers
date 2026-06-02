---
title: "LLM-Wiki Architecture"
note_type: "architecture"
status: "active"
tags: ["architecture", "llm-wiki", "source-localization"]
source_ids: ["SOURCE-KARPATHY-LLM-WIKI-2026", "SOURCE-README-ORIGINAL-2026-06-02"]
related: ["../index.md", "../guidance/source-discipline.md", "../guidance/ingest-workflow.md"]
last_reviewed: "2026-06-02"
---

# LLM-Wiki Architecture

## Layers

```mermaid
flowchart TD
  README["README.md awesome-list inventory"] --> Register["wiki/data/paper-register.json"]
  Register --> Papers["wiki/papers/ paper fragments"]
  Sources["sources/raw/ localized source files"] --> Papers
  SourceNotes["wiki/sources/ source notes"] --> Papers
  Papers --> Claims["wiki/claims/ Claim Cards"]
  SourceNotes --> Claims
  Claims --> Topics
  Papers --> Topics["wiki/topics/ synthesis notes"]
  Topics --> Maps["wiki/maps/ guided entry points"]
  Guidance["wiki/guidance/ operating rules"] --> Register
  Guidance --> Papers
```

## Responsibilities

- `README.md` remains the public inventory and high-level project surface.
- `sources/raw/` stores localized raw evidence and should be treated as
  immutable after files are added.
- `wiki/sources/` records source status, use boundaries, and source-backed
  claims.
- `wiki/papers/` gives each paper or external reference a stable wiki fragment.
- `wiki/claims/` stores atomic source-bounded Claim Cards with explicit review
  status, source refs, locators, and related topics.
- `wiki/topics/` synthesizes the survey's conceptual structure.
- `wiki/maps/` gives humans and agents entry routes through the graph.
- `wiki/data/` stores registers for validation and scripted updates.

## Local Adaptation

The first practical target is usefulness for the Code as Agent Harness survey,
not perfect download completeness. A paper can have a wiki fragment before its
PDF or page is localized, provided the fragment clearly records fetch status and
does not make unsupported content claims.

After localization, the practical target becomes claim granularity. Generated
cards start as `agent-drafted`, local validation promotes traceable cards to
`agent-reviewed`, and separate reviewer manifests can promote selected cards to
`cross-agent-reviewed`. `human-reviewed` is reserved for named human review.
