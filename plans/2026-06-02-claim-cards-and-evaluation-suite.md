# Claim Cards And Evaluation Suite Rollout

Date: 2026-06-02

## Objective

Implement the LLM-Wiki primary-source evaluation recommendations by turning
localized source cues into explicit Claim Cards, agent review tiers, thematic
synthesis pages, evidence-packet tooling, bibliography export, and a reusable
evaluation suite.

## Review Tiers

- `metadata-only`: Inventory metadata exists, but no localized source signal.
- `localized`: A local source exists.
- `auto-extracted`: Local text extraction produced cues, not reviewed claims.
- `agent-drafted`: An agent generated a Claim Card from local evidence.
- `agent-reviewed`: A local review pass checked schema, traceability, source
  refs, locators, and overclaiming risk.
- `cross-agent-reviewed`: A separate reviewer agent confirmed traceability,
  claim type, locator, and absence of overclaiming.
- `human-reviewed`: A named human reviewer has reviewed the card.
- `decision-grade`: The card has source-specific review, current official-source
  checks where needed, and is suitable for policy/procurement use.

`human-reviewed` is literal and optional. Textual operations such as threat
taxonomy extraction, recommendation drafting, and contribution-note generation
should normally use `agent-reviewed` or `cross-agent-reviewed`.

## Implementation Steps

1. Add `wiki/claims/`, `wiki/data/claim-register.json`, and
   `wiki/templates/claim-card.md`.
2. Generate Claim Cards from localized PDF, HTML, Markdown, text, and DOCX
   sources, prioritising MCP governance, sandboxing/containment, and
   oversight/evidence examples.
3. Add an agent review tool that promotes valid cards to `agent-reviewed` and
   applies `cross-agent-reviewed` only from an explicit reviewer manifest.
4. Update paper fragments so Claim Cards are linked from each fragment.
5. Add thematic synthesis pages that cite Claim Cards directly.
6. Add evidence-packet and bibliography export tooling.
7. Add a reusable evaluation suite and post-upgrade evaluation report.
8. Update root and wiki documentation in lockstep.

## Acceptance Checks

- `python3 tools/check_wiki.py`
- `python3 -m py_compile tools/*.py`
- `python3 tools/evaluate_llm_wiki.py --write-report`
- `python3 tools/build_evidence_packet.py --topic mcp-governance`
- `python3 tools/export_bibliography.py --format markdown`

## Source Boundary

Original raw sources remain local-only except redistributable exceptions under
`sources/raw/redistributable/`. Claim Cards cite local source paths and source
register IDs but do not commit raw local-only blobs.
