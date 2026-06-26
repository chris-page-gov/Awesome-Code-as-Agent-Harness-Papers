---
type: "guidance"
title: "OKFR UI Specification"
description: "Specification for the reusable OKFR graph, detail panel, tile, and stack-of-cards interaction model."
timestamp: "2026-06-26T00:00:00Z"
okf_version: "0.1"
okfr_role: "specification"
okfr_summary: "Captures the reader behavior to implement in SeeLinks and generated static OKFR views."
tags: ["okfr", "ui", "specification", "seelinks"]
---

# OKFR UI Specification

This specification records the UI requirements for helping readers understand a
complex OKF pack quickly.

The first implementation follows the `api-mcp-wiki` reader pattern:

- A hamburger concept/timeline list for entry and reorientation.
- A central graph with `Force`, `Timeline`, `Type`, and `Narrative` layouts.
- A right detail panel with concise summary, evaluation/status, relationship
  chips, references, and referenced-by links.
- Navigation history for back, forward, and home.
- Tooltip and hover behavior for nodes, edges, and relationship chips.
- Tile fronts limited to high-ink-ratio signals, with fuller source/evidence
  detail on the back.
- Stack-of-cards views for small comparable sets such as related Claim Cards,
  source clusters, timeline event groups, and competing evidence/gap cards.
