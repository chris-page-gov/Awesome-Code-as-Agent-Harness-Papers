#!/usr/bin/env python3
"""Build markdown evidence packets from Claim Cards."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path

from wiki_claim_utils import (
    CLAIM_REGISTER,
    EVIDENCE_PACKETS_DIR,
    PAPER_REGISTER,
    ROOT,
    SOURCE_REGISTER,
    claim_counts_by,
    read_json,
    slugify,
)


TODAY = date.today().isoformat()


def matches(claim: dict, args: argparse.Namespace) -> bool:
    if args.topic and args.topic not in claim.get("related_topics", []) and args.topic != claim.get("topic_id"):
        return False
    if args.paper_id and args.paper_id not in claim.get("paper_ids", []):
        return False
    if args.source_id and args.source_id not in claim.get("source_ids", []):
        return False
    if args.keyword:
        haystack = " ".join(
            [
                claim.get("statement", ""),
                claim.get("evidence_summary", ""),
                " ".join(claim.get("related_topics", [])),
                " ".join(claim.get("source_refs", [])),
            ]
        ).lower()
        if args.keyword.lower() not in haystack:
            return False
    return True


def bibliography_for_claims(claims: list[dict], paper_register: dict, source_register: list[dict]) -> list[str]:
    papers = {paper["paper_id"]: paper for paper in paper_register.get("papers", [])}
    sources = {source["source_id"]: source for source in source_register}
    lines: list[str] = []
    seen: set[str] = set()
    for claim in claims:
        for paper_id in claim.get("paper_ids", []):
            if paper_id in seen:
                continue
            seen.add(paper_id)
            paper = papers.get(paper_id, {})
            urls = paper.get("canonical_urls") or []
            url_text = f" {urls[0]}" if urls else ""
            lines.append(f"- `{paper_id}`: {paper.get('title', paper_id)}.{url_text}")
        for source_id in claim.get("source_ids", []):
            if source_id in seen:
                continue
            seen.add(source_id)
            source = sources.get(source_id, {})
            url = source.get("canonical_url") or source.get("local_path") or source.get("note_path") or ""
            lines.append(f"- `{source_id}`: {source.get('title', source_id)}. {url}")
    return lines


def packet_markdown(args: argparse.Namespace) -> tuple[str, list[dict]]:
    claim_register = read_json(CLAIM_REGISTER, {})
    paper_register = read_json(PAPER_REGISTER, {})
    source_register = read_json(SOURCE_REGISTER, [])
    claims = [claim for claim in claim_register.get("claims", []) if matches(claim, args)]
    claims.sort(key=lambda claim: (-claim.get("confidence", 0), claim["claim_id"]))

    title_bits = []
    for attr in ["topic", "paper_id", "source_id", "keyword"]:
        value = getattr(args, attr)
        if value:
            title_bits.append(f"{attr}={value}")
    title = ", ".join(title_bits) or "all-claims"

    status_counts = Counter(claim.get("review_status", "unknown") for claim in claims)
    quality_counts = status_counts
    volatile_count = sum(1 for claim in claims if claim.get("volatility_flag"))
    gap_claims = [claim for claim in claims if claim.get("claim_type") == "gap"]

    lines = [
        "---\n",
        f'title: "Evidence Packet: {title}"\n',
        'note_type: "evidence-packet"\n',
        'status: "agent-reviewed"\n',
        'tags: ["evidence-packet", "claim-card", "llm-wiki"]\n',
        f'generated: "{TODAY}"\n',
        "---\n\n",
        f"# Evidence Packet: {title}\n\n",
        "## Query\n\n",
    ]
    for attr in ["topic", "paper_id", "source_id", "keyword"]:
        value = getattr(args, attr)
        if value:
            lines.append(f"- `{attr}`: `{value}`\n")
    if not title_bits:
        lines.append("- all claims\n")
    lines.extend(
        [
            "\n## Summary\n\n",
            f"- Claim Cards: {len(claims)}\n",
            f"- Gap cards: {len(gap_claims)}\n",
            f"- Volatile official/protocol/legal/vendor recheck flags: {volatile_count}\n",
            "- Source-quality distribution:\n",
        ]
    )
    for status, count in sorted(quality_counts.items()):
        lines.append(f"  - `{status}`: {count}\n")

    lines.append("\n## Claim Cards\n\n")
    for claim in claims[: args.limit]:
        path = Path(claim["card_path"]).name
        topics = ", ".join(f"`{topic}`" for topic in claim.get("related_topics", []))
        lines.extend(
            [
                f"### [{claim['claim_id']}](../../claims/{path})\n\n",
                f"- Statement: {claim['statement']}\n",
                f"- Type: `{claim['claim_type']}`\n",
                f"- Review status: `{claim['review_status']}`\n",
                f"- Confidence: `{claim.get('confidence', 0):.2f}`\n",
                f"- Topics: {topics or 'none'}\n",
                f"- Locator: {claim.get('evidence_locator', {}).get('locator', 'not recorded')}\n",
            ]
        )
        if claim.get("volatility_flag"):
            lines.append("- External check warning: volatile source; recheck official/protocol/legal/vendor source before decision use.\n")
        lines.append("\n")

    lines.append("## Gaps\n\n")
    if gap_claims:
        for claim in gap_claims[:20]:
            path = Path(claim["card_path"]).name
            lines.append(f"- [{claim['claim_id']}](../../claims/{path}) - {claim['statement']}\n")
    else:
        lines.append("- No gap cards matched this packet.\n")

    lines.append("\n## Bibliography\n\n")
    bibliography = bibliography_for_claims(claims, paper_register, source_register)
    lines.extend([line + "\n" for line in bibliography] or ["- No bibliography entries matched.\n"])
    return "".join(lines), claims


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic")
    parser.add_argument("--paper-id")
    parser.add_argument("--source-id")
    parser.add_argument("--keyword")
    parser.add_argument("--limit", type=int, default=40)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stdout", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    markdown, claims = packet_markdown(args)
    output = args.output
    if output is None:
        label = args.topic or args.paper_id or args.source_id or args.keyword or "all-claims"
        output = EVIDENCE_PACKETS_DIR / f"{slugify(label)}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    if args.stdout:
        print(markdown)
    print(f"Wrote {output.relative_to(ROOT)} with {len(claims)} matching Claim Cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
