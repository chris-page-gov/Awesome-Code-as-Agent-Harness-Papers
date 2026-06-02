#!/usr/bin/env python3
"""Build a SeeLinks assertion pack from local LLM-Wiki Claim Cards."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAIM_REGISTER = ROOT / "wiki/data/claim-register.json"
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"
DEFAULT_OUTPUT = ROOT / "exports/seelinks/code-agent-harness-claim-review-demo/pack.json"
PACK_ICON = "/assets/ai/ai-placeholder.svg"

DEMO_TOPICS = [
    "mcp-governance",
    "agent-safety-and-sandboxing",
    "evidence-observability-and-redress",
    "procurement-and-conformance",
]

GOLDEN_TOPIC_IDS = {
    "mcp-protocol",
    "authorization",
    "registry",
    "gateway",
    "threat",
    "rollback",
    "sandboxing",
    "capability-governance",
    "safe-execution",
    "approval",
    "traceability",
    "redress",
    "evaluation",
    "evidence-store",
}

CLAIM_TYPE_TO_ASSERTION_TYPE = {
    "contribution": "claim",
    "source-signal": "claim",
    "protocol-capability": "fact",
    "governance-control": "recommendation",
    "safety-control": "risk",
    "threat-taxonomy": "risk",
    "evaluation-result": "metric",
    "evidence-practice": "claim",
    "procurement-conformance": "recommendation",
    "gap": "risk",
}

HIGH_MATERIALITY_TYPES = {
    "governance-control",
    "safety-control",
    "threat-taxonomy",
    "procurement-conformance",
    "gap",
}

PROPERTY_DEFS = [
    {"id": "document_type", "name": "Document type", "kind": "multi", "section": "Source", "order": 0},
    {"id": "source_document", "name": "Source document", "kind": "multi", "section": "Source", "order": 1},
    {"id": "topic", "name": "Wiki topic", "kind": "multi", "section": "Classification", "order": 2},
    {"id": "topic_id", "name": "Extraction topic", "kind": "multi", "section": "Classification", "order": 3},
    {"id": "claim_type", "name": "Claim Card type", "kind": "multi", "section": "Assertion", "order": 4},
    {
        "id": "assertion_type",
        "name": "Assertion type",
        "kind": "multi",
        "section": "Assertion",
        "order": 5,
        "values": [
            "claim",
            "fact",
            "assumption",
            "interpretation",
            "inference",
            "judgement",
            "recommendation",
            "decision",
            "risk",
            "metric",
        ],
    },
    {
        "id": "fact_status",
        "name": "Fact status",
        "kind": "multi",
        "section": "Review",
        "order": 6,
        "values": [
            "unverified",
            "supported",
            "partially_supported",
            "contradicted",
            "unsupported",
            "ambiguous",
            "superseded",
            "out_of_scope",
        ],
    },
    {
        "id": "review_state",
        "name": "Human review state",
        "kind": "multi",
        "section": "Review",
        "order": 7,
        "values": ["proposed", "accepted", "amended", "rejected", "escalated"],
    },
    {
        "id": "evidence_tier",
        "name": "Evidence tier",
        "kind": "multi",
        "section": "Review",
        "order": 8,
        "values": [
            "metadata-only",
            "localized",
            "auto-extracted",
            "agent-drafted",
            "agent-reviewed",
            "cross-agent-reviewed",
            "human-reviewed",
            "decision-grade",
        ],
    },
    {
        "id": "relationship_type",
        "name": "Relationship type",
        "kind": "multi",
        "section": "Relationships",
        "order": 9,
        "values": ["supports", "partially_supports", "contradicts", "qualifies", "duplicates", "supersedes", "depends_on"],
    },
    {"id": "materiality", "name": "Materiality", "kind": "multi", "section": "Review", "order": 10, "values": ["low", "medium", "high"]},
    {
        "id": "source_span_quality",
        "name": "Source span quality",
        "kind": "multi",
        "section": "Source",
        "order": 11,
        "values": ["gap", "cue-match-locator", "registered-source", "unknown"],
    },
    {"id": "external_recheck_required", "name": "External recheck required", "kind": "yes_no", "section": "Governance", "order": 12},
    {"id": "volatility_flag", "name": "Volatile source", "kind": "yes_no", "section": "Governance", "order": 13},
    {"id": "security_marking", "name": "Security marking", "kind": "multi", "section": "Governance", "order": 14, "values": ["OFFICIAL"]},
    {"id": "confidence", "name": "Confidence", "kind": "number", "section": "Review", "order": 15},
    {"id": "paper_id", "name": "Paper id", "kind": "multi", "section": "Source", "order": 16},
    {"id": "source_ref", "name": "Source reference", "kind": "multi", "section": "Source", "order": 17},
    {"id": "source_locality", "name": "Source locality", "kind": "multi", "section": "Source", "order": 18},
    {"id": "extraction_method", "name": "Extraction method", "kind": "multi", "section": "Source", "order": 19},
    {"id": "claim_card_path", "name": "Claim Card path", "kind": "text", "section": "Source", "order": 20},
    {"id": "paper_fragment_path", "name": "Paper fragment path", "kind": "text", "section": "Source", "order": 21},
    {"id": "source_year", "name": "Source year", "kind": "number", "section": "Source", "order": 22},
    {"id": "source_order", "name": "Source order", "kind": "number", "section": "Source", "order": 23},
    {"id": "source_url", "name": "Source URL", "kind": "text", "section": "Source", "order": 24},
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def infer_document_type(source_ref: str) -> str:
    suffix = Path(source_ref).suffix.lower()
    if suffix == ".pdf":
        return "pdf"
    if suffix == ".docx":
        return "docx"
    if suffix in {".html", ".htm"}:
        return "html"
    if suffix in {".md", ".markdown"}:
        return "markdown"
    if suffix in {".csv", ".tsv", ".xlsx"}:
        return "spreadsheet"
    return "text"


def source_locality(source_ref: str) -> str:
    if source_ref.startswith("sources/raw/redistributable/"):
        return "redistributable-local"
    if source_ref.startswith("sources/raw/"):
        return "local-only-raw-cache"
    if source_ref.startswith(("http://", "https://")):
        return "external-url"
    return "repo-file"


def materiality_for(claim: dict[str, Any]) -> str:
    if claim.get("claim_type") in HIGH_MATERIALITY_TYPES:
        return "high"
    if claim.get("confidence", 0) < 0.5:
        return "high"
    return "medium"


def fact_status_for(claim: dict[str, Any]) -> str:
    if claim.get("claim_type") == "gap":
        return "unsupported"
    if claim.get("review_status") == "cross-agent-reviewed":
        return "supported"
    if claim.get("review_status") == "agent-reviewed":
        return "partially_supported"
    return "unverified"


def span_quality_for(claim: dict[str, Any]) -> str:
    if claim.get("claim_type") == "gap":
        return "gap"
    locator = claim.get("evidence_locator", {})
    if isinstance(locator, dict) and locator.get("matched_terms"):
        return "cue-match-locator"
    if claim.get("source_ids"):
        return "registered-source"
    return "unknown"


def source_title(claim: dict[str, Any], paper_by_id: dict[str, dict[str, Any]]) -> str:
    paper_ids = claim.get("paper_ids") or []
    if paper_ids and paper_ids[0] in paper_by_id:
        return str(paper_by_id[paper_ids[0]].get("title") or paper_ids[0])
    source_refs = claim.get("source_refs") or []
    return Path(source_refs[0]).name if source_refs else "Unknown source"


def paper_fragment_path(claim: dict[str, Any]) -> str:
    paper_ids = claim.get("paper_ids") or []
    if not paper_ids:
        return ""
    return f"wiki/papers/{paper_ids[0]}.md"


def paper_for(claim: dict[str, Any], paper_by_id: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    paper_ids = claim.get("paper_ids") or []
    if paper_ids and paper_ids[0] in paper_by_id:
        return paper_by_id[paper_ids[0]]
    return None


def paper_year(paper: dict[str, Any] | None) -> int | None:
    if not paper:
        return None
    for venue in paper.get("venues", []):
        match = re.search(r"\b(19|20)\d{2}\b", str(venue))
        if match:
            return int(match.group(0))
    return None


def paper_url(paper: dict[str, Any] | None) -> str:
    if not paper:
        return ""
    urls = paper.get("canonical_urls") or []
    return str(urls[0]) if urls else ""


def source_key(claim: dict[str, Any], paper_by_id: dict[str, dict[str, Any]]) -> str:
    paper = paper_for(claim, paper_by_id)
    if paper:
        return str(paper.get("paper_id") or paper.get("title") or claim.get("claim_id"))
    source_refs = claim.get("source_refs") or []
    return str(source_refs[0]) if source_refs else str(claim.get("claim_id"))


def source_order_by_claim(selected: list[dict[str, Any]], paper_by_id: dict[str, dict[str, Any]]) -> dict[str, int]:
    counters: defaultdict[str, int] = defaultdict(int)
    order: dict[str, int] = {}
    for claim in selected:
        key = source_key(claim, paper_by_id)
        counters[key] += 1
        order[claim["claim_id"]] = counters[key]
    return order


def select_claims(claims: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    selected: dict[str, dict[str, Any]] = {}

    def add(claim: dict[str, Any]) -> None:
        selected.setdefault(claim["claim_id"], claim)

    for claim in claims:
        if claim.get("review_status") == "cross-agent-reviewed":
            add(claim)
        if claim.get("claim_type") == "gap":
            add(claim)
        if claim.get("topic_id") in GOLDEN_TOPIC_IDS:
            add(claim)

    for topic in DEMO_TOPICS:
        topic_claims = [claim for claim in claims if topic in claim.get("related_topics", [])]
        topic_claims.sort(key=lambda claim: (-float(claim.get("confidence", 0)), claim.get("claim_type") == "gap", claim["claim_id"]))
        for claim in topic_claims[:30]:
            add(claim)

    ordered = list(selected.values())
    ordered.sort(
        key=lambda claim: (
            claim.get("claim_type") != "gap",
            claim.get("review_status") != "cross-agent-reviewed",
            -float(claim.get("confidence", 0)),
            claim["claim_id"],
        )
    )
    return ordered[:limit]


def claim_item(
    claim: dict[str, Any],
    paper_by_id: dict[str, dict[str, Any]],
    source_order: int,
) -> dict[str, Any]:
    claim_id = claim["claim_id"]
    topics = claim.get("related_topics", [])
    topic_id = claim.get("topic_id") or ""
    source_refs = claim.get("source_refs", [])
    paper = paper_for(claim, paper_by_id)
    year = paper_year(paper)
    url = paper_url(paper)
    title = source_title(claim, paper_by_id)
    assertion_type = CLAIM_TYPE_TO_ASSERTION_TYPE.get(claim.get("claim_type"), "claim")
    review_state = "proposed"
    fact_status = fact_status_for(claim)
    source_excerpt = claim.get("evidence_summary") or claim.get("statement")
    relationship_types = ["qualifies"] if claim.get("claim_type") == "gap" else []
    if claim.get("volatility_flag"):
        relationship_types.append("depends_on")
    category_topic = topics[0] if topics else "unclassified"
    return {
        "id": claim_id,
        "name": claim.get("statement", claim_id),
        "short_name": claim_id.replace("CLAIM-", ""),
        "icon": PACK_ICON,
        "category_path": f"Code Agent Harness Claim Cards/{category_topic}/{claim.get('claim_type', 'claim')}",
        "tile_subtitle": f"{claim.get('review_status', 'unknown')} | {fact_status} | {title}",
        "info_text": source_excerpt,
        "properties": {
            "document_type": sorted({infer_document_type(ref) for ref in source_refs}) or ["text"],
            "source_document": title,
            "topic": topics,
            "topic_id": topic_id,
            "claim_type": claim.get("claim_type"),
            "assertion_type": assertion_type,
            "fact_status": fact_status,
            "review_state": review_state,
            "evidence_tier": claim.get("review_status"),
            "relationship_type": sorted(set(relationship_types)),
            "materiality": materiality_for(claim),
            "source_span_quality": span_quality_for(claim),
            "external_recheck_required": bool(claim.get("volatility_flag") or claim.get("claim_type") == "gap"),
            "volatility_flag": bool(claim.get("volatility_flag")),
            "security_marking": "OFFICIAL",
            "confidence": float(claim.get("confidence", 0)),
            "paper_id": claim.get("paper_ids", []),
            "source_ref": source_refs,
            "source_locality": sorted({source_locality(ref) for ref in source_refs}) or ["unknown"],
            "extraction_method": claim.get("extraction_method", "unknown"),
            "claim_card_path": claim.get("card_path", ""),
            "paper_fragment_path": paper_fragment_path(claim),
            "source_year": year,
            "source_order": source_order,
            "source_url": url,
            "source_excerpt": source_excerpt,
            "fragment_ids": [f"fragment:{claim_id}"],
            "reviewer": claim.get("reviewer", ""),
            "creator": claim.get("creator", ""),
        },
    }


def build_graph(
    selected: list[dict[str, Any]],
    paper_by_id: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    graph_claims: list[dict[str, Any]] = []
    source_ids_by_ref: dict[str, str] = {}
    seen_nodes: set[str] = set()
    seen_edges: set[str] = set()

    def add_node(node: dict[str, Any]) -> None:
        if node["id"] in seen_nodes:
            return
        seen_nodes.add(node["id"])
        nodes.append(node)

    def add_edge(edge: dict[str, Any]) -> None:
        edge_id = edge.get("id")
        if edge_id and edge_id in seen_edges:
            return
        if edge_id:
            seen_edges.add(edge_id)
        edges.append(edge)

    for topic in DEMO_TOPICS:
        output_id = f"output:{topic}"
        add_node(
            {
                "id": output_id,
                "kind": "output",
                "title": f"Evidence packet: {topic}",
                "summary": "Claim-backed evidence packet generated from the Code as Agent Harness LLM-Wiki.",
                "metadata": {"wiki_path": f"wiki/reports/evidence-packets/{topic}.md"},
            }
        )

    for claim in selected:
        claim_id = claim["claim_id"]
        source_refs = claim.get("source_refs", [])
        claim_source_ids: list[str] = []
        for ref in source_refs:
            source_id = source_ids_by_ref.setdefault(ref, stable_id("source", ref))
            claim_source_ids.append(source_id)
            if not any(source["id"] == source_id for source in sources):
                title = source_title(claim, paper_by_id)
                sources.append(
                    {
                        "id": source_id,
                        "title": title,
                        "publisher": "Code as Agent Harness LLM-Wiki local source register",
                        "metadata": {
                            "source_ref": ref,
                            "source_locality": source_locality(ref),
                            "document_type": infer_document_type(ref),
                            "paper_ids": claim.get("paper_ids", []),
                            "local_raw_blobs_not_redistributed": source_locality(ref) == "local-only-raw-cache",
                        },
                    }
                )
                add_node(
                    {
                        "id": f"document:{source_id}",
                        "kind": "document",
                        "title": title,
                        "summary": ref,
                        "source_ids": [source_id],
                        "metadata": sources[-1]["metadata"],
                    }
                )

        fragment_id = f"fragment:{claim_id}"
        locator = claim.get("evidence_locator", {})
        locator_text = locator.get("locator") if isinstance(locator, dict) else str(locator)
        matched_terms = locator.get("matched_terms", []) if isinstance(locator, dict) else []
        source_excerpt = claim.get("evidence_summary") or claim.get("statement", "")
        add_node(
            {
                "id": fragment_id,
                "kind": "fragment",
                "title": f"{claim_id} evidence locator",
                "content": source_excerpt,
                "source_ids": claim_source_ids,
                "metadata": {
                    "selector": {
                        "type": span_quality_for(claim),
                        "value": locator_text,
                        "metadata": {"matched_terms": matched_terms},
                    },
                    "claim_card_path": claim.get("card_path"),
                    "source_span_quality": span_quality_for(claim),
                },
            }
        )
        for source_id in claim_source_ids:
            add_edge(
                {
                    "id": f"edge:{source_id}:{fragment_id}:contains",
                    "kind": "contains",
                    "from": f"document:{source_id}",
                    "to": fragment_id,
                    "source_ids": [source_id],
                    "metadata": {"locator": locator_text},
                }
            )

        add_node(
            {
                "id": claim_id,
                "kind": "assertion",
                "title": claim.get("statement", claim_id),
                "summary": source_excerpt,
                "source_ids": claim_source_ids,
                "metadata": {
                    "claim_type": claim.get("claim_type"),
                    "assertion_type": CLAIM_TYPE_TO_ASSERTION_TYPE.get(claim.get("claim_type"), "claim"),
                    "fact_status": fact_status_for(claim),
                    "review_state": "proposed",
                    "evidence_tier": claim.get("review_status"),
                    "confidence": claim.get("confidence"),
                    "materiality": materiality_for(claim),
                    "volatility_flag": claim.get("volatility_flag"),
                },
            }
        )
        add_edge(
            {
                "id": f"edge:{fragment_id}:{claim_id}:evidences",
                "kind": "evidences",
                "from": fragment_id,
                "to": claim_id,
                "source_ids": claim_source_ids,
                "metadata": {
                    "review_state": "proposed",
                    "evidence_tier": claim.get("review_status"),
                    "confidence": claim.get("confidence"),
                    "source_span_quality": span_quality_for(claim),
                },
            }
        )
        for topic in claim.get("related_topics", []):
            if topic in DEMO_TOPICS:
                add_edge(
                    {
                        "id": f"edge:{claim_id}:output:{topic}:used",
                        "kind": "used_in_output",
                        "from": claim_id,
                        "to": f"output:{topic}",
                        "source_ids": claim_source_ids,
                        "metadata": {"review_state": "proposed", "confidence": claim.get("confidence")},
                    }
                )

        graph_claims.append(
            {
                "id": claim_id,
                "text": claim.get("statement", claim_id),
                "node_id": claim_id,
                "source_ids": claim_source_ids,
                "status": "needs_review",
                "assertion_type": CLAIM_TYPE_TO_ASSERTION_TYPE.get(claim.get("claim_type"), "claim"),
                "fact_status": fact_status_for(claim),
                "review_state": "proposed",
                "confidence": claim.get("confidence"),
                "fragment_ids": [fragment_id],
                "metadata": {
                    "claim_type": claim.get("claim_type"),
                    "evidence_tier": claim.get("review_status"),
                    "source_excerpt": source_excerpt,
                    "materiality": materiality_for(claim),
                    "claim_card_path": claim.get("card_path"),
                    "paper_ids": claim.get("paper_ids", []),
                    "volatility_flag": claim.get("volatility_flag"),
                    "reviewer": claim.get("reviewer", ""),
                },
            }
        )

    claims_by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    gaps_by_topic: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for claim in selected:
        for topic in claim.get("related_topics", []):
            claims_by_topic[topic].append(claim)
            if claim.get("claim_type") == "gap":
                gaps_by_topic[topic].append(claim)
    for topic, gaps in gaps_by_topic.items():
        targets = [claim for claim in claims_by_topic[topic] if claim.get("claim_type") != "gap"]
        targets.sort(key=lambda claim: (-float(claim.get("confidence", 0)), claim["claim_id"]))
        if not targets:
            continue
        target = targets[0]
        for gap in gaps[:5]:
            add_edge(
                {
                    "id": f"edge:{gap['claim_id']}:{target['claim_id']}:qualifies",
                    "kind": "qualifies",
                    "from": gap["claim_id"],
                    "to": target["claim_id"],
                    "source_ids": [],
                    "metadata": {
                        "review_state": "proposed",
                        "confidence": 0.55,
                        "notes": "Gap card qualifies reuse of related evidence until source span quality is improved.",
                    },
                }
            )

    return {"nodes": nodes, "edges": edges, "sources": sources, "claims": graph_claims}


def collections_for(selected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    ids = {claim["claim_id"] for claim in selected}
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    def collection(collection_id: str, name: str, claim_ids: list[str], description: str) -> dict[str, Any]:
        filtered = [claim_id for claim_id in claim_ids if claim_id in ids]
        return {
            "id": collection_id,
            "name": name,
            "description": description,
            "item_ids": filtered,
            "created_at": now,
        }

    result = [
        collection(
            "review-queue-gap-cards",
            "Gap Cards",
            [claim["claim_id"] for claim in selected if claim.get("claim_type") == "gap"],
            "Claims where the wiki has an explicit source-span or decision-grade evidence gap.",
        ),
        collection(
            "review-queue-cross-agent-reviewed",
            "Cross-Agent Reviewed Sample",
            [claim["claim_id"] for claim in selected if claim.get("review_status") == "cross-agent-reviewed"],
            "Cards checked by a second agent but still awaiting any human SeeLinks decision.",
        ),
        collection(
            "review-queue-volatile-recheck",
            "Volatile Source Recheck",
            [claim["claim_id"] for claim in selected if claim.get("volatility_flag")],
            "Official, protocol, legal, or vendor sources requiring recheck before decision use.",
        ),
    ]
    for topic in DEMO_TOPICS:
        result.append(
            collection(
                f"evidence-packet-{topic}",
                f"Evidence Packet: {topic}",
                [claim["claim_id"] for claim in selected if topic in claim.get("related_topics", [])],
                f"SeeLinks collection corresponding to wiki/reports/evidence-packets/{topic}.md.",
            )
        )
    return [entry for entry in result if entry["item_ids"]]


def build_pack(limit: int) -> dict[str, Any]:
    claim_data = read_json(CLAIM_REGISTER)
    paper_data = read_json(PAPER_REGISTER)
    claims = claim_data.get("claims", [])
    paper_by_id = {paper["paper_id"]: paper for paper in paper_data.get("papers", [])}
    selected = select_claims(claims, limit)
    source_order = source_order_by_claim(selected, paper_by_id)
    type_counts = Counter(claim.get("claim_type") for claim in selected)
    status_counts = Counter(claim.get("review_status") for claim in selected)
    return {
        "meta": {
            "id": "code-agent-harness-llm-wiki-claim-review-demo",
            "title": "Code Agent Harness LLM-Wiki Claim Review Demo",
            "source": "local",
            "version": "0.1.0",
            "kind": "seelinks-assertions",
            "packKind": "seelinks-assertions",
            "cardLayout": "seelinks-assertions",
            "security_marking": "OFFICIAL",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "generator": "tools/build_seelinks_claim_pack.py",
            "source_repo": "Awesome-Code-as-Agent-Harness-Papers",
            "source_claim_count": len(claims),
            "included_claim_count": len(selected),
            "review_semantics": "All imported wiki Claim Cards start with review_state=proposed for SeeLinks human review. Agent review tiers are preserved separately as evidence_tier.",
            "source_blob_policy": "Local raw source blobs are not redistributed in this pack unless already redistributable in the source repo.",
            "claim_type_distribution": dict(sorted(type_counts.items())),
            "evidence_tier_distribution": dict(sorted(status_counts.items())),
            "fields": [entry["id"] for entry in PROPERTY_DEFS],
        },
        "properties": PROPERTY_DEFS,
        "items": [claim_item(claim, paper_by_id, source_order.get(claim["claim_id"], 0)) for claim in selected],
        "collections": collections_for(selected),
        "graph": build_graph(selected, paper_by_id),
    }


def write_intro(output: Path, pack: dict[str, Any]) -> None:
    intro = output.parent / "intro.md"
    intro.write_text(
        "\n".join(
            [
                "# Code Agent Harness LLM-Wiki Claim Review Demo",
                "",
                "This SeeLinks pack turns the LLM-Wiki Claim Card layer into an assertion review surface.",
                "",
                f"- Included Claim Cards: `{pack['meta']['included_claim_count']}`",
                f"- Source Claim Cards available in the wiki: `{pack['meta']['source_claim_count']}`",
                "- Human review state: every imported card starts as `proposed`.",
                "- Agent evidence tier: preserved separately as `evidence_tier`.",
                "- Local raw source blobs: not redistributed unless already marked redistributable.",
                "",
                "Recommended first filters: `claim_type=gap`, `evidence_tier=cross-agent-reviewed`, and `external_recheck_required=true`.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_readme(output: Path, pack: dict[str, Any]) -> None:
    readme = output.parent / "README.md"
    readme.write_text(
        "\n".join(
            [
                "# Code Agent Harness LLM-Wiki Claim Review Demo Pack",
                "",
                "This directory contains a generated SeeLinks assertion pack built from the local Claim Card register.",
                "",
                "## Files",
                "",
                "- `pack.json`: SeeLinks pack with assertion items, collections, and graph metadata.",
                "- `intro.md`: opening note for the pack.",
                "",
                "## Load In SeeLinks",
                "",
                "Copy this directory to `apps/web/static/data/code-agent-harness-claim-review-demo/` in the SeeLinks repo, then open:",
                "",
                "`http://localhost:5173/?pack=/data/code-agent-harness-claim-review-demo/pack.json`",
                "",
                "## Review Semantics",
                "",
                "All items start with `review_state=proposed`. The wiki's automated review tier is preserved as `evidence_tier`, so `agent-reviewed` and `cross-agent-reviewed` are not treated as human acceptance.",
                "",
                "## Generated Summary",
                "",
                f"- Included Claim Cards: `{pack['meta']['included_claim_count']}`",
                f"- Source Claim Cards available in wiki: `{pack['meta']['source_claim_count']}`",
                f"- Claim type distribution: `{pack['meta']['claim_type_distribution']}`",
                f"- Evidence tier distribution: `{pack['meta']['evidence_tier_distribution']}`",
                "",
            ]
        ),
        encoding="utf-8",
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=160)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pack = build_pack(args.limit)
    output = args.output
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(pack, indent=2, sort_keys=False) + "\n", encoding="utf-8")
    write_intro(output, pack)
    write_readme(output, pack)
    print(f"Wrote {output.relative_to(ROOT)} with {len(pack['items'])} items.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
