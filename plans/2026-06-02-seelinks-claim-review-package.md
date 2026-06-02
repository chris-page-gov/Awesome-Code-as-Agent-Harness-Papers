# SeeLinks Claim Review Package Plan

Date: 2026-06-02

Status: implemented

## Goal

Evaluate the fit between this repo's Claim Card/evidence-packet LLM-Wiki layer
and the adjacent Assertion SeeLinks/SeeLinks assertion-review interface, then
produce a concrete SeeLinks data package that demonstrates the synergy without
redistributing local-only raw source blobs.

## Scope

- Inspect this repo's claim register, paper register, evidence packets,
  review-tier semantics, and source-localization boundary.
- Inspect `/Users/crpage/repos/assertion-seelinks` for the assertion pack
  contract, assertion schema, relationship schema, facets, and review workflow.
- Inspect `/Users/crpage/repos/seelinks` for the live `seelinks-assertions`
  pack runtime, graph extension, review view, graph view, and data-model parser.
- Add a reproducible exporter from wiki Claim Cards to a SeeLinks assertion
  pack.
- Generate a curated demo pack that can be copied into the SeeLinks static data
  directory.
- Record a detailed evaluation and data-package specification in the wiki
  reports area.

## Decisions

- Keep every imported Claim Card at SeeLinks `review_state=proposed`.
- Preserve `agent-reviewed` and `cross-agent-reviewed` as an `evidence_tier`
  facet, not as human acceptance.
- Map Claim Cards to assertion items and graph claims.
- Map evidence packets to SeeLinks collections and graph output nodes.
- Map source locators to fragment nodes and `evidences` edges.
- Map gap cards to `risk` assertions with `fact_status=unsupported`.
- Mark volatile official/protocol/legal/vendor evidence with an explicit
  recheck facet and review collection.
- Do not include raw source blobs in the pack unless they are already
  redistributable.

## Outputs

- `tools/build_seelinks_claim_pack.py`
- `exports/seelinks/code-agent-harness-claim-review-demo/pack.json`
- `exports/seelinks/code-agent-harness-claim-review-demo/intro.md`
- `exports/seelinks/code-agent-harness-claim-review-demo/README.md`
- `wiki/reports/seelinks-assertion-package-synergy-evaluation.md`

## Validation

- `python3 tools/build_seelinks_claim_pack.py`
- `python3 -m json.tool exports/seelinks/code-agent-harness-claim-review-demo/pack.json`
- `python3 -m py_compile tools/build_seelinks_claim_pack.py`
- SeeLinks runtime parse via `/Users/crpage/repos/seelinks`:
  `normalizePack` accepted the pack as `packKind=seelinks-assertions` with
  160 items, 21 properties, seven collections, 400 graph nodes, 606 graph
  edges, and 160 graph claims.
