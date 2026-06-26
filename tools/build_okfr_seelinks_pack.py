#!/usr/bin/env python3
"""Build a SeeLinks-compatible OKFR pack from the OKF wiki graph."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from okf_lib import ROOT, add_check_arg, build_okf_graph, check_output, repo_rel, write_json


OUTPUT_DIR = ROOT / "exports/okfr/code-agent-harness-okfr"
PACK_PATH = OUTPUT_DIR / "pack.json"
INTRO_PATH = OUTPUT_DIR / "intro.md"
README_PATH = OUTPUT_DIR / "README.md"
PACK_ICON = "/assets/ai/ai-placeholder.svg"
GENERATED_AT = "2026-06-26T00:00:00Z"

NODE_KIND_BY_OKF_TYPE = {
    "claim-card": "assertion",
    "paper": "document",
    "source": "source",
    "report": "output",
    "topic": "article",
    "map": "article",
    "index": "article",
    "guidance": "article",
    "architecture": "article",
    "progress": "article",
    "log": "article",
    "template": "fragment",
}

PROPERTY_DEFS = [
    {"id": "okf_type", "name": "OKF type", "kind": "multi", "section": "OKF", "order": 0},
    {"id": "okf_section", "name": "OKF section", "kind": "multi", "section": "OKF", "order": 1},
    {"id": "okf_timestamp", "name": "OKF timestamp", "kind": "text", "section": "OKF", "order": 2},
    {"id": "okf_tags", "name": "OKF tags", "kind": "multi", "section": "OKF", "order": 3},
    {"id": "okf_resource", "name": "OKF resource", "kind": "text", "section": "OKF", "order": 4},
    {"id": "okfr_role", "name": "OKFR role", "kind": "multi", "section": "OKFR", "order": 5},
    {"id": "okfr_date", "name": "OKFR date", "kind": "text", "section": "OKFR", "order": 6},
    {"id": "okfr_order", "name": "OKFR order", "kind": "number", "section": "OKFR", "order": 7},
    {"id": "source_document", "name": "Source document", "kind": "multi", "section": "Evidence", "order": 8},
    {"id": "paper_id", "name": "Paper id", "kind": "multi", "section": "Evidence", "order": 9},
    {"id": "source_ref", "name": "Source reference", "kind": "multi", "section": "Evidence", "order": 10},
    {"id": "source_url", "name": "Source URL", "kind": "text", "section": "Evidence", "order": 11},
    {"id": "source_locality", "name": "Source locality", "kind": "multi", "section": "Evidence", "order": 12},
    {"id": "claim_type", "name": "Claim type", "kind": "multi", "section": "Claim Card", "order": 13},
    {"id": "evidence_tier", "name": "Evidence tier", "kind": "multi", "section": "Claim Card", "order": 14},
    {"id": "review_status", "name": "Review status", "kind": "multi", "section": "Claim Card", "order": 15},
    {"id": "confidence", "name": "Confidence", "kind": "number", "section": "Claim Card", "order": 16},
    {"id": "volatility_flag", "name": "Volatile source", "kind": "yes_no", "section": "Claim Card", "order": 17},
    {"id": "relationship_type", "name": "Relationship type", "kind": "multi", "section": "Graph", "order": 18},
    {"id": "wiki_path", "name": "Wiki path", "kind": "text", "section": "OKF", "order": 19},
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"{prefix}:{digest}"


def source_locality(source_ref: str) -> str:
    if source_ref.startswith("sources/raw/redistributable/"):
        return "redistributable-local"
    if source_ref.startswith("sources/raw/"):
        return "local-only-raw-cache"
    if source_ref.startswith(("http://", "https://")):
        return "external-url"
    return "repo-file"


def short_label(title: str, limit: int = 72) -> str:
    title = re.sub(r"\s+", " ", title).strip()
    if len(title) <= limit:
        return title
    return title[: limit - 1].rstrip() + "…"


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def load_registers() -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    paper_data = read_json(ROOT / "wiki/data/paper-register.json")
    claim_data = read_json(ROOT / "wiki/data/claim-register.json")
    source_data = read_json(ROOT / "wiki/data/source-register.json")
    papers = {paper["paper_id"]: paper for paper in paper_data.get("papers", []) if isinstance(paper, dict)}
    claims = {claim["card_path"]: claim for claim in claim_data.get("claims", []) if isinstance(claim, dict)}
    sources = {source["note_path"]: source for source in source_data if isinstance(source, dict)}
    return papers, claims, sources


def paper_by_path(papers: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {f"wiki/papers/{paper_id}.md": paper for paper_id, paper in papers.items()}


def paper_publication_date(paper: dict[str, Any] | None) -> str:
    if not paper:
        return ""
    candidates = [*as_list(paper.get("canonical_urls")), *as_list(paper.get("local_source_paths"))]
    for candidate in candidates:
        text = str(candidate)
        match = re.search(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv/)(\d{2})(\d{2})\.\d+", text, flags=re.IGNORECASE)
        if match:
            return f"{2000 + int(match.group(1)):04d}-{int(match.group(2)):02d}"
    for venue in as_list(paper.get("venues")):
        match = re.search(r"\b(19|20)\d{2}\b", str(venue))
        if match:
            return match.group(0)
    return ""


def item_properties(
    node: dict[str, Any],
    papers_by_path: dict[str, dict[str, Any]],
    claims_by_path: dict[str, dict[str, Any]],
    sources_by_path: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    rel_path = node["path"]
    props: dict[str, Any] = {
        "okf_type": node.get("kind"),
        "okf_section": node.get("section"),
        "okf_timestamp": node.get("timestamp"),
        "okf_tags": node.get("tags") or [],
        "okf_resource": node.get("resource") or "",
        "okfr_role": node.get("okfr_role") or "",
        "okfr_date": node.get("okfr_date") or "",
        "okfr_order": node.get("okfr_order"),
        "wiki_path": rel_path,
    }

    paper = papers_by_path.get(rel_path)
    if paper:
        props.update(
            {
                "source_document": paper.get("title") or node.get("label"),
                "paper_id": paper.get("paper_id"),
                "source_ref": as_list(paper.get("local_source_paths")),
                "source_url": (as_list(paper.get("canonical_urls")) or [""])[0],
                "source_locality": sorted({source_locality(str(ref)) for ref in as_list(paper.get("local_source_paths"))}),
                "evidence_tier": paper.get("evidence_quality"),
                "review_status": paper.get("evidence_quality"),
                "okfr_date": node.get("okfr_date") or paper_publication_date(paper),
            }
        )

    claim = claims_by_path.get(rel_path)
    if claim:
        paper_titles = []
        for paper_id in as_list(claim.get("paper_ids")):
            source_paper = papers_by_path.get(f"wiki/papers/{paper_id}.md")
            if source_paper:
                paper_titles.append(source_paper.get("title") or paper_id)
        props.update(
            {
                "source_document": paper_titles or as_list(claim.get("paper_ids")),
                "paper_id": as_list(claim.get("paper_ids")),
                "source_ref": as_list(claim.get("source_refs")),
                "source_locality": sorted({source_locality(str(ref)) for ref in as_list(claim.get("source_refs"))}),
                "claim_type": claim.get("claim_type"),
                "evidence_tier": claim.get("review_status"),
                "review_status": claim.get("review_status"),
                "confidence": claim.get("confidence"),
                "volatility_flag": bool(claim.get("volatility_flag")),
                "relationship_type": ["qualifies"] if claim.get("claim_type") == "gap" else ["evidences"],
            }
        )

    source = sources_by_path.get(rel_path)
    if source:
        props.update(
            {
                "source_document": source.get("title") or source.get("source_id"),
                "source_ref": [source.get("local_path") or source.get("source_path_or_url") or ""],
                "source_locality": [source_locality(str(source.get("local_path") or ""))],
            }
        )
    return props


def item_for(
    node: dict[str, Any],
    papers_by_path: dict[str, dict[str, Any]],
    claims_by_path: dict[str, dict[str, Any]],
    sources_by_path: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    title = str(node.get("label") or node["id"])
    props = item_properties(node, papers_by_path, claims_by_path, sources_by_path)
    subtitle_bits = [str(props.get("okf_type") or "page")]
    if props.get("okfr_date"):
        subtitle_bits.append(str(props["okfr_date"]))
    if props.get("evidence_tier"):
        subtitle_bits.append(str(props["evidence_tier"]))
    return {
        "id": node["id"],
        "name": title,
        "short_name": short_label(title, 42),
        "icon": PACK_ICON,
        "category_path": f"OKFR/{props.get('okf_section') or 'root'}/{props.get('okf_type') or 'page'}",
        "tile_subtitle": " | ".join(subtitle_bits),
        "info_text": node.get("okfr_summary") or node.get("description") or title,
        "properties": props,
    }


def source_records(claims_by_path: dict[str, dict[str, Any]], papers_by_path: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for claim in claims_by_path.values():
        for ref in as_list(claim.get("source_refs")):
            ref_text = str(ref)
            record_id = stable_id("source", ref_text)
            paper_ids = as_list(claim.get("paper_ids"))
            titles = []
            for paper_id in paper_ids:
                paper = papers_by_path.get(f"wiki/papers/{paper_id}.md")
                if paper:
                    titles.append(paper.get("title") or paper_id)
            records.setdefault(
                record_id,
                {
                    "id": record_id,
                    "title": titles[0] if titles else Path(ref_text).name,
                    "publisher": "Code as Agent Harness LLM-Wiki source register",
                    "metadata": {
                        "source_ref": ref_text,
                        "source_locality": source_locality(ref_text),
                        "paper_ids": paper_ids,
                        "local_raw_blobs_not_redistributed": source_locality(ref_text) == "local-only-raw-cache",
                    },
                },
            )
    return sorted(records.values(), key=lambda source: source["id"])


def graph_for(
    okf_graph: dict[str, Any],
    papers_by_path: dict[str, dict[str, Any]],
    claims_by_path: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    nodes = []
    for node in okf_graph["nodes"]:
        nodes.append(
            {
                "id": node["id"],
                "kind": NODE_KIND_BY_OKF_TYPE.get(str(node.get("kind")), "article"),
                "title": node.get("label"),
                "summary": node.get("okfr_summary") or node.get("description"),
                "metadata": {
                    "okf_type": node.get("kind"),
                    "okf_section": node.get("section"),
                    "wiki_path": node.get("path"),
                    "okfr_role": node.get("okfr_role"),
                    "okfr_date": node.get("okfr_date"),
                    "okfr_order": node.get("okfr_order"),
                },
            }
        )

    edges: list[dict[str, Any]] = []
    seen_edges: set[str] = set()

    def add_edge(edge: dict[str, Any]) -> None:
        if edge["id"] in seen_edges:
            return
        seen_edges.add(edge["id"])
        edges.append(edge)

    for edge in okf_graph["edges"]:
        add_edge(
            {
                "id": edge["id"],
                "kind": edge.get("kind", "links_to"),
                "from": edge["source"],
                "to": edge["target"],
                "source_ids": [],
                "metadata": {
                    **edge.get("metadata", {}),
                    "relationship_label": edge.get("metadata", {}).get("relationship_label", "links to"),
                    "inferred": edge.get("metadata", {}).get("inferred", False),
                },
            }
        )

    for claim_path, claim in claims_by_path.items():
        for paper_id in as_list(claim.get("paper_ids")):
            paper_path = f"wiki/papers/{paper_id}.md"
            if paper_path in papers_by_path:
                add_edge(
                    {
                        "id": stable_id("edge", f"{paper_path}|evidences|{claim_path}"),
                        "kind": "evidences",
                        "from": paper_path,
                        "to": claim_path,
                        "source_ids": [stable_id("source", str(ref)) for ref in as_list(claim.get("source_refs"))],
                        "metadata": {
                            "relationship_label": "paper/source evidence supports Claim Card",
                            "inferred": True,
                            "claim_id": claim.get("claim_id"),
                            "review_status": claim.get("review_status"),
                        },
                    }
                )
        for topic in as_list(claim.get("related_topics")):
            topic_path = f"wiki/topics/{topic}.md"
            if (ROOT / topic_path).is_file():
                add_edge(
                    {
                        "id": stable_id("edge", f"{claim_path}|used_in_output|{topic_path}"),
                        "kind": "used_in_output",
                        "from": claim_path,
                        "to": topic_path,
                        "source_ids": [stable_id("source", str(ref)) for ref in as_list(claim.get("source_refs"))],
                        "metadata": {
                            "relationship_label": "used in topic synthesis",
                            "inferred": True,
                            "claim_id": claim.get("claim_id"),
                            "topic": topic,
                        },
                    }
                )

    return {"nodes": nodes, "edges": sorted(edges, key=lambda edge: edge["id"]), "sources": [], "claims": []}


def collections_for(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_section: defaultdict[str, list[str]] = defaultdict(list)
    by_type: defaultdict[str, list[str]] = defaultdict(list)
    for item in items:
        props = item["properties"]
        by_section[str(props.get("okf_section") or "root")].append(item["id"])
        by_type[str(props.get("okf_type") or "page")].append(item["id"])

    collections = []
    for section, item_ids in sorted(by_section.items()):
        collections.append(
            {
                "id": f"okfr-section-{section}",
                "name": f"OKFR section: {section}",
                "description": f"OKF pages in the {section} section.",
                "item_ids": sorted(item_ids),
                "created_at": GENERATED_AT,
            }
        )
    for item_type, item_ids in sorted(by_type.items()):
        collections.append(
            {
                "id": f"okfr-type-{item_type}",
                "name": f"OKF type: {item_type}",
                "description": f"OKF pages with type `{item_type}`.",
                "item_ids": sorted(item_ids),
                "created_at": GENERATED_AT,
            }
        )
    return collections


def build_pack() -> dict[str, Any]:
    papers, claims_by_path, sources_by_path = load_registers()
    papers_by_path = paper_by_path(papers)
    okf_graph = build_okf_graph()
    items = [
        item_for(node, papers_by_path, claims_by_path, sources_by_path)
        for node in sorted(okf_graph["nodes"], key=lambda row: row["id"])
    ]
    graph = graph_for(okf_graph, papers_by_path, claims_by_path)
    graph["sources"] = source_records(claims_by_path, papers_by_path)
    graph["claims"] = [
        {
            "id": claim.get("claim_id"),
            "text": claim.get("statement"),
            "node_id": path,
            "source_ids": [stable_id("source", str(ref)) for ref in as_list(claim.get("source_refs"))],
            "status": "needs_review",
            "assertion_type": claim.get("claim_type"),
            "fact_status": "unsupported" if claim.get("claim_type") == "gap" else "partially_supported",
            "review_state": "proposed",
            "confidence": claim.get("confidence"),
            "fragment_ids": [path],
            "metadata": {
                "claim_type": claim.get("claim_type"),
                "review_status": claim.get("review_status"),
                "paper_ids": claim.get("paper_ids"),
                "source_refs": claim.get("source_refs"),
                "volatility_flag": claim.get("volatility_flag"),
            },
        }
        for path, claim in sorted(claims_by_path.items())
    ]
    type_counts = Counter(item["properties"].get("okf_type") for item in items)
    section_counts = Counter(item["properties"].get("okf_section") for item in items)
    return {
        "meta": {
            "id": "code-agent-harness-okfr",
            "title": "Code Agent Harness OKFR",
            "source": "Awesome-Code-as-Agent-Harness-Papers LLM-Wiki",
            "version": "0.1.0",
            "kind": "okfr-pack",
            "packKind": "okfr",
            "introPath": "intro.md",
            "generated_at": GENERATED_AT,
            "generator": "tools/build_okfr_seelinks_pack.py",
            "source_repo": "https://github.com/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers",
            "okf": {
                "version": "0.1",
                "profile": "OKF v0.1 + OKFR extensions",
                "required_frontmatter": ["type", "title", "description", "timestamp"],
            },
            "okfr": {
                "display": "graph-reader",
                "reference_design": "api-mcp-wiki/viewer.html",
                "default_layout": "timeline",
                "node_count": len(graph["nodes"]),
                "edge_count": len(graph["edges"]),
            },
            "source_blob_policy": {
                "local_only_raw_excluded": True,
                "redistributable_raw_allowed": True,
                "policy": "Only source paths and metadata are exported; local-only raw blobs are not embedded.",
            },
            "okf_type_distribution": dict(sorted(type_counts.items())),
            "okf_section_distribution": dict(sorted(section_counts.items())),
            "fields": PROPERTY_DEFS,
        },
        "properties": PROPERTY_DEFS,
        "items": items,
        "collections": collections_for(items),
        "graph": graph,
    }


def intro_markdown(pack: dict[str, Any]) -> str:
    meta = pack["meta"]
    return f"""# Code Agent Harness OKFR

This SeeLinks OKFR package is generated from the Code as Agent Harness
LLM-Wiki. It contains {len(pack['items'])} OKF pages and
{len(pack['graph']['edges'])} graph relationships.

Use it to move between the wiki overview, source-backed paper fragments, Claim
Cards, reports, and topic syntheses without opening local-only raw source blobs.

Raw source policy: {meta['source_blob_policy']['policy']}
"""


def readme_markdown(pack: dict[str, Any]) -> str:
    meta = pack["meta"]
    return f"""# Code Agent Harness OKFR Pack

Generated by `tools/build_okfr_seelinks_pack.py`.

- Pack kind: `{meta['packKind']}`
- OKF profile: `{meta['okf']['profile']}`
- Items: {len(pack['items'])}
- Graph nodes: {len(pack['graph']['nodes'])}
- Graph edges: {len(pack['graph']['edges'])}
- Sources listed in graph metadata: {len(pack['graph']['sources'])}
- Claims listed in graph metadata: {len(pack['graph']['claims'])}

The pack is designed for SeeLinks OKFR reader mode and for the generated static
site under `_site/`. It exports paths, metadata, Claim Card traceability, and
relationship metadata only. Local-only raw blobs under `sources/raw/` remain out
of the pack unless they are explicit redistributable exceptions.
"""


def write_outputs(pack: dict[str, Any]) -> None:
    write_json(PACK_PATH, pack)
    INTRO_PATH.write_text(intro_markdown(pack), encoding="utf-8")
    README_PATH.write_text(readme_markdown(pack), encoding="utf-8")


def check_outputs(pack: dict[str, Any]) -> list[str]:
    pack_content = json.dumps(pack, indent=2, ensure_ascii=False) + "\n"
    return [
        *check_output(PACK_PATH, pack_content),
        *check_output(INTRO_PATH, intro_markdown(pack)),
        *check_output(README_PATH, readme_markdown(pack)),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    add_check_arg(parser)
    args = parser.parse_args()

    pack = build_pack()
    if args.check:
        errors = check_outputs(pack)
        if errors:
            print("OKFR SeeLinks pack check failed:")
            for error in errors:
                print(f"- {error}")
            return 1
        print(f"OKFR SeeLinks pack is up to date: {repo_rel(PACK_PATH)}")
        return 0

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_outputs(pack)
    print(f"Wrote {repo_rel(PACK_PATH)}")
    print(f"Wrote {repo_rel(INTRO_PATH)}")
    print(f"Wrote {repo_rel(README_PATH)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
