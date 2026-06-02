---
title: "LLM-Wiki Ingest Workflow"
note_type: "guidance"
status: "active"
tags: ["ingest", "source-notes", "paper-fragments", "llm-wiki"]
source_ids: ["SOURCE-KARPATHY-LLM-WIKI-2026"]
related: ["source-discipline.md", "../templates/source-note.md", "../templates/paper-fragment.md"]
last_reviewed: "2026-06-02"
---

# LLM-Wiki Ingest Workflow

## Steps

1. Parse README rows into title, canonical URL, venue, layer, section, and
   subsection metadata.
2. Create or update `wiki/data/paper-register.json`.
3. Create or update one `wiki/papers/` fragment per canonical paper or external
   reference.
4. Update README paper links to point at local fragments while keeping the
   canonical external URL inside each fragment.
5. Fetch open raw sources into `sources/raw/` when network and access allow.
6. Record hashes, fetch status, and canonical URL in `sources/metadata/`.
7. Update source notes, topic notes, maps, `wiki/log.md`, `PROGRESS.md`, and
   `CHANGELOG.md`.
8. Run `python3 tools/check_wiki.py`.

## First-Pass Priority

1. Code as Agent Harness survey source.
2. arXiv-hosted papers.
3. OpenReview, ACL Anthology, PMLR, NeurIPS, AAAI, IJCAI and DOI landing pages.
4. Publisher pages and product/blog reports.

