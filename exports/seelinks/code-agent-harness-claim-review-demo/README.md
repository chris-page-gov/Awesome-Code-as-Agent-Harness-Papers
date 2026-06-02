# Code Agent Harness LLM-Wiki Claim Review Demo Pack

This directory contains a generated SeeLinks assertion pack built from the local Claim Card register.

## Files

- `pack.json`: SeeLinks pack with assertion items, collections, and graph metadata.
- `intro.md`: opening note for the pack.

## Load In SeeLinks

Copy this directory to `apps/web/static/data/code-agent-harness-claim-review-demo/` in the SeeLinks repo, then open:

`http://localhost:5173/?pack=/data/code-agent-harness-claim-review-demo/pack.json`

## Review Semantics

All items start with `review_state=proposed`. The wiki's automated review tier is preserved as `evidence_tier`, so `agent-reviewed` and `cross-agent-reviewed` are not treated as human acceptance.

## Generated Summary

- Included Claim Cards: `160`
- Source Claim Cards available in wiki: `1148`
- Claim type distribution: `{'contribution': 4, 'evaluation-result': 34, 'evidence-practice': 11, 'gap': 42, 'governance-control': 27, 'procurement-conformance': 8, 'protocol-capability': 13, 'safety-control': 16, 'threat-taxonomy': 5}`
- Evidence tier distribution: `{'agent-reviewed': 146, 'cross-agent-reviewed': 14}`
