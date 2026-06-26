---
type: "report"
title: "SeeLinks Assertion Package Synergy Evaluation"
description: "The fit is strong. This repo now has the evidence substrate that a SeeLinks human-review interface needs: Claim Cards, source locators, paper/source registers, evidence packets, gap cards, explicit review tiers, topic syntheses, and eval..."
timestamp: "2026-06-02T00:00:00Z"
tags: ["report", "seelinks", "claim-card", "assertion-review", "llm-wiki"]
okf_version: "0.1"
okfr_role: "report"
okfr_summary: "The fit is strong. This repo now has the evidence substrate that a SeeLinks human-review interface needs: Claim Cards, source locators, paper/source registers, evidence packets, gap cards, explicit review tiers, topic syntheses, and eval..."
note_type: "report"
status: "agent-reviewed"
last_reviewed: "2026-06-02"
---

# SeeLinks Assertion Package Synergy Evaluation

## Summary

The fit is strong. This repo now has the evidence substrate that a SeeLinks
human-review interface needs: Claim Cards, source locators, paper/source
registers, evidence packets, gap cards, explicit review tiers, topic syntheses,
and evaluation metrics. The adjacent Assertion SeeLinks repo defines the
reviewable assertion-tile concept, while the live SeeLinks repo already accepts
`seelinks-assertions` packs with graph nodes, evidence fragments, relationship
edges, collections, and review actions.

The best demonstration package is therefore not a document viewer. It is a
Claim Card review pack:

- Claim Cards become SeeLinks assertion tiles.
- Evidence locators become fragment nodes and `evidences` edges.
- Evidence packets become collections and output nodes.
- Gap cards become high-materiality review risks.
- Volatile official/protocol/legal/vendor evidence becomes a recheck queue.
- Wiki agent tiers become `evidence_tier`, while SeeLinks human workflow stays
  at `review_state=proposed`.

Implemented demonstrator:

- Pack directory:
  `exports/seelinks/code-agent-harness-claim-review-demo/`
- Pack:
  `exports/seelinks/code-agent-harness-claim-review-demo/pack.json`
- Generator:
  `tools/build_seelinks_claim_pack.py`

The generated pack parses successfully through the live SeeLinks data model as
`packKind=seelinks-assertions`.

## Repositories Inspected

### This Repo

Relevant assets:

- `wiki/data/claim-register.json`: 1,148 Claim Cards.
- `wiki/claims/`: one Markdown Claim Card per atomic claim.
- `wiki/data/paper-register.json`: 354 paper/reference fragments.
- `wiki/reports/evidence-packets/`: four claim-backed packets.
- `wiki/topics/`: claim-backed synthesis pages for MCP governance, safety,
  evidence/redress, and procurement/conformance.
- `tools/evaluate_llm_wiki.py`: reusable wiki evaluation metrics.
- `tools/build_evidence_packet.py`: markdown packet generation.
- `tools/review_claim_cards.py`: agent/cross-agent review tier support.

Current evidence distribution:

- Claim Cards: 1,148.
- Paper coverage: 354/354.
- Review status: 1,134 `agent-reviewed`, 14 `cross-agent-reviewed`.
- Claim types: contribution, evaluation-result, protocol-capability,
  governance-control, gap, safety-control, evidence-practice,
  procurement-conformance, and threat-taxonomy.
- Volatile recheck flags: 310 across official/protocol/legal/vendor sources.
- Gap cards: 42.

The evidence layer is useful for search and synthesis, but it is currently
Markdown/JSON-first. SeeLinks supplies the missing human review surface:
faceted browsing, review queues, side-by-side evidence, relationship views,
collections, and printable/exportable outputs.

### Assertion SeeLinks Repo

`/Users/crpage/repos/assertion-seelinks` defines the assertion workbench
concept and a starter pack contract:

- `data/schemas/seelinks-pack.schema.json` accepts `meta`, `properties`,
  `items`, and `collections`.
- `data/schemas/assertion.schema.json` defines statement, assertion type,
  source spans, facets, verification status, materiality, AI metadata, and
  review history.
- `data/schemas/relationship.schema.json` defines support, contradiction,
  qualification, duplication, update, dependency, derivation, and attribution.
- `examples/assertion-pack/pack.json` demonstrates assertion extension fields
  that legacy SeeLinks importers can ignore while still rendering the tile.

The assertion repo's main insight is that relationships are also reviewable
analytical records. This maps directly to Claim Card gaps and to evidence-packet
membership: both are assertions about how evidence can safely be reused.

### Live SeeLinks Repo

`/Users/crpage/repos/seelinks` already has the runtime needed for the demo:

- `@seelinks/data-model` accepts `Pack` objects with `meta`, `properties`,
  `items`, `collections`, `graph`, and optional hierarchy extensions.
- `packKind=seelinks-assertions` activates assertion-specific card and detail
  behavior.
- Graph extensions support `document`, `fragment`, `assertion`,
  `relationship`, and `output` nodes.
- Edge kinds include `evidences`, `supports`, `partially_supports`,
  `contradicts`, `qualifies`, `duplicates`, `supersedes`, `depends_on`, and
  `used_in_output`.
- `ReviewView.svelte` supports `accepted`, `amended`, `rejected`, and
  `escalated` review actions.
- `AssertionGraphView.svelte` surfaces evidence links and assertion
  relationships.

This means the integration can use a SeeLinks-native package immediately rather
than waiting for a new interface.

## Synergy Model

| LLM-Wiki asset | SeeLinks representation | Human-review value |
| --- | --- | --- |
| Claim Card | Assertion tile plus graph claim | Turns atomic evidence into a reviewable object. |
| Claim statement | Item `name`, graph claim `text` | Gives reviewers one precise proposition to accept, amend, reject, or escalate. |
| Claim type | `claim_type` facet and mapped `assertion_type` | Supports queues for risks, recommendations, metrics, and evidence practices. |
| Paper/source IDs | Source/document facets and graph sources | Preserves provenance and supports source filtering. |
| Evidence locator | Fragment node plus `evidences` edge | Gives the UI a side-by-side evidence target even when exact quote extraction is still weak. |
| Evidence packet | Collection plus output node | Lets reviewers inspect all claims used in a synthesis or report. |
| Gap card | `risk` assertion with `fact_status=unsupported` | Makes missing evidence first-class instead of invisible. |
| Review tier | `evidence_tier` facet | Shows agent/cross-agent status without pretending human review occurred. |
| Volatility flag | `external_recheck_required` and `volatility_flag` facets | Creates review queues for official/protocol/legal/vendor recheck. |
| Related topics | Topic facets and collections | Enables policy-oriented browsing rather than file-oriented browsing. |

The core synergy is that the LLM-Wiki generates a dense evidence graph while
SeeLinks makes that graph inspectable, reviewable, and reusable by people.

## Demonstrator Package

### Location

`exports/seelinks/code-agent-harness-claim-review-demo/`

Files:

- `pack.json`
- `intro.md`
- `README.md`

Generation command:

```bash
python3 tools/build_seelinks_claim_pack.py
```

Load in SeeLinks by copying the directory to:

`/Users/crpage/repos/seelinks/apps/web/static/data/code-agent-harness-claim-review-demo/`

Then open:

`http://localhost:5173/?pack=/data/code-agent-harness-claim-review-demo/pack.json`

### Demo Selection

The curated pack includes 160 Claim Cards:

- All 14 `cross-agent-reviewed` cards.
- All 42 gap cards.
- Golden-scenario coverage for MCP governance, sandboxing/containment, and
  human oversight/evidence.
- High-value cards from MCP governance, agent safety/sandboxing,
  evidence/observability/redress, and procurement/conformance.

Generated distribution:

- `gap`: 42.
- `evaluation-result`: 34.
- `governance-control`: 27.
- `safety-control`: 16.
- `protocol-capability`: 13.
- `evidence-practice`: 11.
- `procurement-conformance`: 8.
- `threat-taxonomy`: 5.
- `contribution`: 4.

Evidence tiers:

- `agent-reviewed`: 146.
- `cross-agent-reviewed`: 14.
- `human-reviewed`: 0.

Every item is intentionally `review_state=proposed`.

### Pack Shape

The pack follows the live SeeLinks format:

```json
{
  "meta": {},
  "properties": [],
  "items": [],
  "collections": [],
  "graph": {
    "nodes": [],
    "edges": [],
    "sources": [],
    "claims": []
  }
}
```

Runtime validation confirmed:

- Items: 160.
- Properties: 21.
- Collections: 7.
- Graph nodes: 400.
- Graph edges: 606.
- Graph sources: 76.
- Graph claims: 160.
- Pack kind: `seelinks-assertions`.

### Required Facets

The demonstrator defines these SeeLinks property facets:

- Source: `document_type`, `source_document`, `paper_id`, `source_ref`,
  `source_locality`, `extraction_method`, `claim_card_path`.
- Classification: `topic`, `topic_id`.
- Assertion: `claim_type`, `assertion_type`.
- Review: `fact_status`, `review_state`, `evidence_tier`, `materiality`,
  `confidence`, `source_span_quality`.
- Relationships: `relationship_type`.
- Governance: `external_recheck_required`, `volatility_flag`,
  `security_marking`.

This gives reviewers immediate work queues:

- `claim_type=gap`
- `evidence_tier=cross-agent-reviewed`
- `external_recheck_required=true`
- `source_span_quality=cue-match-locator`
- `topic=mcp-governance`
- `topic=procurement-and-conformance`

### Review Semantics

The most important design decision is to keep two review dimensions separate:

- `review_state`: SeeLinks human workflow state. All generated cards start as
  `proposed`.
- `evidence_tier`: LLM-Wiki provenance/review tier. Values such as
  `agent-reviewed` and `cross-agent-reviewed` remain machine/agent review
  signals only.

This avoids the previous ambiguity around "human review". A SeeLinks user may
accept, amend, reject, or escalate a card, but the package itself does not
claim that any generated note is human-reviewed.

### Graph Semantics

The generated graph uses conservative edges:

- `contains`: source document node to evidence fragment node.
- `evidences`: evidence fragment node to Claim Card assertion node.
- `used_in_output`: Claim Card assertion node to evidence-packet output node.
- `qualifies`: selected gap cards to related evidence claims where the gap
  should caveat reuse.

The package does not invent substantive `supports` or `contradicts` edges
between papers. Those should be produced later by a relationship-extraction pass
with its own traceable evidence and review queue.

## Example Workflows

### Example A: MCP Governance

A reviewer filters to `topic=mcp-governance`, then inspects:

- protocol-capability cards for MCP protocol and tool discovery;
- governance-control cards for authorization, gateway, and trust-boundary
  issues;
- procurement-conformance cards for registry and conformance questions;
- threat-taxonomy cards for attack-surface analysis;
- gap cards and volatile-source warnings before policy reuse.

This demonstrates a direct path from wiki evidence packets to a SeeLinks human
review queue.

### Example B: Sandboxing And Containment

Filter to `topic=agent-safety-and-sandboxing`, then inspect:

- rollback and state recovery claims;
- sandboxing/isolation claims;
- capability-governance claims;
- safe-execution claims;
- gap cards that qualify decision-grade reuse.

The SeeLinks graph view can show whether an assertion is backed only by a
cue-match locator or by stronger source-span evidence.

### Example C: Human Oversight And Evidence

Filter to `topic=evidence-observability-and-redress`, then inspect:

- approval and oversight claims;
- traceability/audit claims;
- redress/accountability claims;
- evaluation and benchmark claims;
- evidence-store/observability claims.

This is the strongest demonstration of LLM-Wiki plus SeeLinks: the wiki gives
coverage and bibliography; SeeLinks gives review state, amendment, escalation,
and reuse control.

## Full Package Specification

The curated pack is the first fixture. The full package should be generated by
the same exporter with a higher limit or no limit:

```bash
python3 tools/build_seelinks_claim_pack.py --limit 1148 \
  --output exports/seelinks/code-agent-harness-claim-review-full/pack.json
```

Full-package requirements:

1. Include every Claim Card as an item and graph claim.
2. Include every evidence packet as a collection and output node.
3. Include paper fragments as document/source nodes, but do not embed local-only
   raw PDFs or HTML blobs.
4. Preserve source refs and local paths as metadata, with
   `source_locality=local-only-raw-cache` where the source is intentionally not
   redistributed.
5. Preserve `evidence_tier` and keep `review_state=proposed` unless importing
   a named SeeLinks human review log.
6. Generate relationship proposals only when there is a traceable reason:
   duplicate claims, explicit contradiction, explicit dependency, temporal
   update, or gap qualification.
7. Maintain a round-trip review export so SeeLinks decisions can update wiki
   Claim Cards without overwriting agent review provenance.

## Gaps And Risks

- Exact source spans are still weak for many cards. The current Claim Cards
  mostly have source locators and matched cue terms, not literal quoted spans.
  The pack therefore exposes `source_span_quality=cue-match-locator` and keeps
  items in `proposed`.
- Local raw source blobs remain local-only by policy. A reviewer can see paths
  and hashes, but a separate source-opening mechanism is needed in SeeLinks for
  machines that have the raw cache.
- Volatile official/protocol/legal/vendor evidence must be rechecked before
  procurement or policy use.
- The assertion-SeeLinks scaffold uses `verification_status`, while the live
  SeeLinks runtime uses `review_state` and `fact_status`. The package targets
  the live runtime and preserves the scaffold concept through facets.
- Relationship extraction is intentionally conservative. The demo includes
  evidence and gap-qualification edges, but not broad support/contradiction
  claims.
- A full 1,148-card pack will be usable but may need UI performance checks and
  additional collection shortcuts.

## Recommendations

1. Use the generated curated pack as the first human-review fixture in
   SeeLinks.
2. Add a SeeLinks source-opener affordance for local wiki paths:
   `claim_card_path`, `paper_fragment_path`, and `source_ref`.
3. Add a round-trip review exporter that writes SeeLinks decisions as separate
   review manifests rather than mutating original Claim Cards directly.
4. Add a stronger source-span extraction pass for high-materiality cards before
   promoting anything to `decision-grade`.
5. Extend relationship generation only after source-span quality improves.
6. Keep `human-reviewed` reserved for named humans across both repos.

## Implementation Plan

1. Copy the curated demo pack into SeeLinks static data and verify the workbench
   route with the existing assertion UI tests.
2. Add a SeeLinks demo route or catalogue entry for
   `code-agent-harness-claim-review-demo`.
3. Review the gap-card and volatile-source queues first.
4. Capture SeeLinks accept/amend/reject/escalate decisions into a JSON review
   manifest.
5. Add an importer in this repo that applies the review manifest as new
   `human-reviewed` or amended Claim Card metadata only when a named human
   reviewer is present.
6. Generate a full-corpus pack and run UI performance checks.
7. Add relationship extraction and contradiction views as a second package
   iteration.

## Validation

Commands run:

```bash
python3 tools/build_seelinks_claim_pack.py
python3 -m json.tool exports/seelinks/code-agent-harness-claim-review-demo/pack.json
python3 -m py_compile tools/build_seelinks_claim_pack.py
```

Runtime compatibility check against `/Users/crpage/repos/seelinks`:

```json
{
  "items": 160,
  "properties": 21,
  "collections": 7,
  "nodes": 400,
  "edges": 606,
  "claims": 160,
  "packKind": "seelinks-assertions"
}
```
