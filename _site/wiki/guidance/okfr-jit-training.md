---
type: "guidance"
title: "OKFR JIT Training"
description: "Just-in-time reader training for using the OKFR graph, timeline, side panel, tiles, and card stacks."
timestamp: "2026-06-26T00:00:00Z"
tags: ["okfr", "training", "reader", "jit"]
okf_version: "0.1"
okfr_role: "training"
okfr_summary: "Introduces how a reader moves from overview to focused evidence in an OKFR wiki pack."
---

# OKFR JIT Training

This page is the canonical home for short, content-specific reader training for
the Code as Agent Harness OKFR pack. A released wiki should customise this
section to the content it introduces, but the interaction pattern is reusable.

## Reference Pattern

The `api-mcp-wiki` reference reader established the pattern: a hamburger
timeline/concept list, a central graph with layout modes, and a right detail
panel that explains the selected item.

![api-mcp-wiki OKFR reference viewer](../assets/okfr-jit/api-mcp-wiki-reference-okfr-viewer.png)

## Generated Code Agent Harness Viewer

The generated site for this repository applies the same OKFR pattern to the
Claim Card, paper fragment, source note, topic, and report graph.

![Code Agent Harness OKFR overview](../assets/okfr-jit/code-agent-harness-okfr-overview.png)

The right panel is the main reading surface after a user selects a node or list
entry. It should summarise the selected entry, show relationship chips, expose
key evidence metadata, and list references/referenced-by links.

![Code Agent Harness OKFR detail panel](../assets/okfr-jit/code-agent-harness-okfr-detail-panel.png)

## Entry Paths

- Use the hamburger list when you know roughly what you want: a paper title,
  topic, source note, Claim Card, or report.
- Use search when the pack is large and the question starts with a phrase,
  source name, or concept.
- Use timeline mode when sequence matters: publication dates, source clusters,
  and how evidence enters the wiki over time.
- Use type mode when comparing page kinds: topics, papers, claims, reports, and
  source notes.
- Use narrative mode when following the wiki's intended reading path.

## Reading The Graph

- Node colour shows the OKF section, not the claim truth status.
- Direction arrows show link or derived-evidence direction.
- Relationship chips in the right panel name edge groups; hover a chip to
  highlight matching edges.
- `inferred` relationship labels mean the edge was generated from Markdown
  links or register structure. They help navigation but are not independent
  proof of a substantive claim.
- Volatile official, protocol, legal, and vendor sources need current recheck
  before policy or procurement use.

## Moving From Overview To Evidence

1. Start in timeline mode to identify a source cluster or topic area.
2. Select a topic, report, paper fragment, or Claim Card.
3. Read the right-panel summary first.
4. Use relationship chips to isolate how the selected entry connects to the
   rest of the wiki.
5. Follow references to Claim Cards, paper fragments, source notes, and reports.
6. If a card is a gap, treat it as a warning to return to the source or improve
   source localization before making decision-grade use.

## View Choice

- Graph: best for understanding relationship structure, evidence reuse, and
  what a selected item depends on.
- Timeline: best for publication chronology and source clustering.
- Tile: best for rapid triage when each record has a concise front and a fuller
  evidence back.
- Stack of cards: best for small comparable sets, such as related Claim Cards,
  competing evidence/gap cards, timeline event groups, or source clusters.

## Tile And Card-Stack Rules

- Tile front: concise title, type/date badge, one-line summary, and one
  high-value status such as evidence tier or confidence.
- Tile back: evidence summary, source refs, relationship counts, and actions.
- Do not put every available field on the tile front. Low-density metadata
  belongs in the back, right panel, or a stack comparison.
- Use card stacks when the user needs side-by-side comparison across a small
  set rather than a single overloaded tile.

## Current Pack Caveats

- The current generated static viewer is a publication/readability layer. The
  reusable interactive OKFR implementation belongs in SeeLinks.
- Local-only raw source blobs are not embedded in the pack or site.
- Agent-created summaries and inferred edges are not human review.
- Human review is literal and must be recorded separately when it occurs.
