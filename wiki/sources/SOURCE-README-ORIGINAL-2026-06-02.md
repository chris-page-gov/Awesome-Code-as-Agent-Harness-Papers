---
type: "source"
title: "Current README Paper Inventory"
description: "The README is the current source of the paper list, survey taxonomy, venues, and canonical external URLs. It is the bootstrap source for generating paper fragments and source-fetch metadata."
timestamp: "2026-06-02T00:00:00Z"
tags: ["source", "readme", "paper-inventory", "awesome-list"]
okf_version: "0.1"
okfr_role: "source"
okfr_summary: "The README is the current source of the paper list, survey taxonomy, venues, and canonical external URLs. It is the bootstrap source for generating paper fragments and source-fetch metadata."
note_type: "source"
status: "active"
last_reviewed: "2026-06-02"
source_id: "SOURCE-README-ORIGINAL-2026-06-02"
source_type: "repository-markdown"
source_path_or_url: "../../README.md"
related: ["../maps/taxonomy-map.md", "../topics/code-as-agent-harness.md"]
---

# Current README Paper Inventory

## Source

- ID: `SOURCE-README-ORIGINAL-2026-06-02`
- Type: Repository Markdown inventory.
- Location: [README.md](../../README.md)
- Date reviewed: 2026-06-02.
- Classification: public repository content.
- Review status: used as inventory metadata, not as a substitute for the papers.

## Why It Matters

The README is the current source of the paper list, survey taxonomy, venues, and
canonical external URLs. It is the bootstrap source for generating paper
fragments and source-fetch metadata.

## Source-Backed Claims

- The repository accompanies the survey *Code as Agent Harness: Toward
  Executable, Verifiable, and Stateful Agent Systems*.
- The README organizes the literature around Harness Interface, Harness
  Mechanisms, and Scaling the Harness.
- The README also includes application areas such as code assistants, GUI/OS
  agents, scientific discovery agents, and embodied agents.
- The README contains many duplicate paper appearances across sections where a
  paper is relevant to more than one concept.

## Use Boundaries

- Treat README rows as bibliographic inventory facts.
- Do not infer detailed paper contributions from a title alone.
- Verify paper-specific claims against localized sources or canonical pages.

## Gaps And Follow-Up

- Generate `wiki/data/paper-register.json` from README rows.
- Create per-paper fragments under `wiki/papers/`.
- Localize source files and update fragments with source-backed notes.
