---
type: "report"
title: "LLM-Wiki Primary Source Evaluation After Claim Cards"
description: "The prior evaluation found that the wiki was strong for discovery and provenance, but weak for claim granularity: paper fragments were mostly automated cues and reports cited whole fragments rather than atomic claims."
timestamp: "2026-06-02T00:00:00Z"
tags: ["report", "llm-wiki", "evaluation", "claim-card"]
okf_version: "0.1"
okfr_role: "report"
okfr_summary: "The prior evaluation found that the wiki was strong for discovery and provenance, but weak for claim granularity: paper fragments were mostly automated cues and reports cited whole fragments rather than atomic claims."
note_type: "report"
status: "agent-reviewed"
last_reviewed: "2026-06-02"
---

# LLM-Wiki Primary Source Evaluation After Claim Cards

## Baseline

The prior evaluation found that the wiki was strong for discovery and provenance, but weak for claim granularity: paper fragments were mostly automated cues and reports cited whole fragments rather than atomic claims.

- Baseline report: [LLM-Wiki primary-source evaluation](llm-wiki-primary-source-evaluation.md)
- Baseline Claim Cards: `0`
- Baseline report-claim backing: whole-fragment and source-note citations, not claim-card citations.

## Current Run

- Claim Cards: `1148`
- Paper coverage: `354/354` (100.0%)
- Papers with fewer than 3 cards: `2`
- Gap cards: `42`
- Volatile official/protocol/legal/vendor recheck flags: `310`
- Cases requiring original or official source access before decision use: `352`
- Stale-gap phrase count: `0`
- Wiki validation passed: `true`

## Review Status Distribution

- `agent-reviewed`: 1134
- `cross-agent-reviewed`: 14

## Claim Type Distribution

- `contribution`: 548
- `evaluation-result`: 281
- `evidence-practice`: 16
- `gap`: 42
- `governance-control`: 88
- `procurement-conformance`: 14
- `protocol-capability`: 113
- `safety-control`: 37
- `threat-taxonomy`: 9

## Report Claim Backing

### Legacy Reports

- Claim-like report lines: `476`
- Lines directly backed by Claim Cards: `0`
- Backed percentage: `0.0%`

This metric remains conservative because pre-existing reports were intentionally preserved as the baseline comparison. New evidence packets and topic pages cite Claim Cards directly.

### Evidence Packets

- Evidence packets: `4`
- Claim-backed packets: `4`
- Claim-backed packet percentage: `100.0%`
- Direct Claim Card links in packets: `217`

## Golden Scenarios

- `mcp-governance`: passed `true`, claims `205`, missing topics `none`.
- `agent-safety-and-sandboxing`: passed `true`, claims `51`, missing topics `none`.
- `evidence-observability-and-redress`: passed `true`, claims `462`, missing topics `none`.

## Before/After Comparison

| Dimension | Before | After |
| --- | --- | --- |
| Discovery | Fast paper/source discovery | Fast discovery plus atomic Claim Cards |
| Provenance | Local source paths and hashes | Local paths, hashes, claim IDs, source refs, locators, and review status |
| Claim granularity | Automated cues in fragments | Claim Cards linked from fragments and topic pages |
| Review language | Some pages implied human review was pending | Agent review tiers are explicit; `human-reviewed` is literal and requires a human reviewer |
| Evidence packets | Manual report assembly | `tools/build_evidence_packet.py` produces claim-backed packets and bibliography |
| Reusability | One-off evaluation report | Reusable evaluation suite under `tools/evaluate_llm_wiki.py` and `tests/wiki_eval/` |

## Examples

- Example A, MCP governance: the topic now requires MCP protocol, authorization, registry, gateway, and threat Claim Cards.
- Example B, sandboxing and containment: the topic now requires rollback, isolation, capability governance, and safe execution Claim Cards.
- Example C, human oversight and evidence: the topic now requires approval, traceability, redress, evaluation, and evidence-store Claim Cards.

## Recommendations

1. Use evidence packets as the entry point for future policy reports, then promote any recurring gap into a Claim Card task.
2. Use `cross-agent-reviewed` for cards confirmed by a separate agent manifest; reserve `human-reviewed` for named human review.
3. Recheck volatile protocol, official, legal, and vendor sources before procurement or policy use.
4. Expand page/section locators over time for decision-grade cards where PDFs have stable pagination.

## Implementation Plan

1. Run `tools/generate_claim_cards.py` after localization or source-register changes.
2. Run `tools/review_claim_cards.py --emit-review-sample wiki/data/claim-review-sample.json` and send the sample to a separate reviewer agent.
3. Apply confirmed review manifests with `tools/review_claim_cards.py --reviewer-manifest <manifest>`.
4. Run `tools/evaluate_llm_wiki.py --write-report` and commit the report with generated evidence packets.
5. Promote high-confidence, repeatedly used cards to `decision-grade` only after source-specific review criteria are met.
