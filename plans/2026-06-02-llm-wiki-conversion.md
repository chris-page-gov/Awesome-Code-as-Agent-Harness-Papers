# Plan: LLM-Wiki Conversion

Date: 2026-06-02

## Objective

Transform this fork from a standalone awesome list into a source-backed
Karpathy-style LLM-Wiki for *Code as Agent Harness* while preserving the README
as a usable public index.

## Local Pattern Basis

- Root control files: `AGENTS.md`, `CONTEXT.md`, `PROGRESS.md`,
  `CHANGELOG.md`, `LLM-WIKI.md`.
- Wiki structure: `wiki/sources/`, `wiki/papers/`, `wiki/topics/`,
  `wiki/maps/`, `wiki/guidance/`, `wiki/progress/`, `wiki/data/`.
- Raw source boundary: `sources/raw/` is read-only after source localization.

## Phases

1. Add control files, wiki scaffold, source discipline, and initial survey
   synthesis.
2. Parse the README paper inventory into a machine-readable catalog and one
   wiki fragment per paper/reference.
3. Update README paper rows to point at local wiki fragments, with canonical
   external links preserved inside the fragments.
4. Fetch open sources opportunistically, starting with arXiv PDFs and HTML
   pages that are accessible without credentials.
5. Update each paper fragment with localized source paths, fetch status, and
   source-backed notes.

## Status

- [x] Phase 1 complete.
- [x] Phase 2 complete: 354 fragments generated from 458 README rows.
- [x] Phase 3 complete: README paper rows now point at wiki fragments.
- [ ] Phase 4 in progress: survey PDF plus localized arXiv source files for the
  first 121 paper fragments.
- [ ] Phase 5 in progress: automated source-cue integration has started.
