---
title: "Karpathy LLM-Wiki Pattern"
note_type: "source"
status: "active"
tags: ["source", "llm-wiki", "method", "karpathy"]
source_id: "SOURCE-KARPATHY-LLM-WIKI-2026"
source_type: "github-gist"
source_path_or_url: "https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f"
related: ["../architecture/llm-wiki-architecture.md", "../guidance/source-discipline.md"]
last_reviewed: "2026-06-02"
---

# Karpathy LLM-Wiki Pattern

## Source

- ID: `SOURCE-KARPATHY-LLM-WIKI-2026`
- Type: GitHub gist by Andrej Karpathy.
- Location: `https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
- Local review basis: adapted from the time-adjacent `wcc-mapping` wiki source
  note reviewed locally on 2026-06-02.
- Status: method source, not a formal standard.

## Why It Matters

This source defines the method pattern this repository is extending: raw sources
remain the source of truth, the wiki is a persistent Markdown knowledge layer
maintained by agents, and repo instructions tell future agents how to preserve
source discipline.

## Source-Backed Claims

- The pattern responds to repeated answer-time rediscovery over raw chunks.
- The LLM-Wiki approach compiles reusable knowledge into a persistent,
  interlinked Markdown layer.
- The core layers are raw sources, wiki, and schema or operating instructions.
- Core operations include ingest, query, and lint.
- `index.md` is the content-oriented entry point and `log.md` is the
  chronological record.
- Git and Markdown are natural tooling fits because the wiki remains ordinary
  files.

## Local Adaptation

- The README remains the public inventory.
- Source notes precede synthesis.
- Paper fragments are the stable xref targets for README rows.
- Raw paper files are localized under `sources/raw/` and treated as read-only.

## Use Boundaries

- Treat this as a practical operating pattern, not a bibliographic authority.
- Paper-specific claims still require paper-specific sources.

