---
type: "page"
title: "Wiki Operating Rules"
description: "This folder is the LLM-Wiki knowledge layer for the Code as Agent Harness fork."
timestamp: "2026-06-26T00:00:00Z"
okf_version: "0.1"
okfr_role: "page"
okfr_summary: "This folder is the LLM-Wiki knowledge layer for the Code as Agent Harness fork."
---

# Wiki Operating Rules

This folder is the LLM-Wiki knowledge layer for the Code as Agent Harness fork.

## Folder Contract

- `index.md` is the main navigation entry point.
- `architecture/` explains how sources, source notes, paper fragments, topics,
  maps, and metadata fit together.
- `data/` stores machine-readable source and paper registers.
- `evals/` stores validation and health notes.
- `guidance/` stores source discipline, ingest, validation, and maintenance
  workflows.
- `implementation/` stores implementation plans derived from source-backed
  notes.
- `maps/` stores guided entry points and cross-reference maps.
- `papers/` stores one reusable fragment per paper or external reference.
- `progress/` stores dashboards, phase logs, and plan summaries.
- `sources/` stores source notes.
- `templates/` stores reusable note templates.
- `topics/` stores synthesis notes.

## Source Rules

- Source notes must record ID, location, review status, and use boundaries.
- Paper fragments must link to their canonical source note or registered source
  gap.
- Topic notes may synthesize, but should cite source notes, paper fragments, or
  explicit gaps.
- Do not copy large chunks of papers into wiki notes.

## Maintenance Workflow

1. Register or update the source.
2. Localize the raw source when possible.
3. Create or update a source note.
4. Create or update the paper fragment.
5. Update relevant topics, maps, and README xrefs.
6. Update `wiki/log.md`, `PROGRESS.md`, and `CHANGELOG.md`.
7. Run `python3 tools/check_wiki.py`.
