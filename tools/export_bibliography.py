#!/usr/bin/env python3
"""Export bibliography views from paper, source, and claim registers."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from datetime import date
from pathlib import Path

from wiki_claim_utils import CLAIM_REGISTER, PAPER_REGISTER, REPORTS_DIR, ROOT, SOURCE_REGISTER, read_json, slugify


TODAY = date.today().isoformat()


def bib_key(identifier: str, title: str) -> str:
    words = re.findall(r"[A-Za-z0-9]+", title)
    stem = "".join(words[:3]) or identifier
    return slugify(stem, max_len=32).replace("-", "") + identifier[-4:]


def markdown_export() -> str:
    paper_register = read_json(PAPER_REGISTER, {})
    source_register = read_json(SOURCE_REGISTER, [])
    claim_register = read_json(CLAIM_REGISTER, {})
    claim_counts = Counter()
    for claim in claim_register.get("claims", []):
        for paper_id in claim.get("paper_ids", []):
            claim_counts[paper_id] += 1
        for source_id in claim.get("source_ids", []):
            claim_counts[source_id] += 1

    lines = [
        "---\n",
        'title: "LLM-Wiki Bibliography Export"\n',
        'note_type: "bibliography"\n',
        'status: "agent-reviewed"\n',
        'tags: ["bibliography", "llm-wiki"]\n',
        f'generated: "{TODAY}"\n',
        "---\n\n",
        "# LLM-Wiki Bibliography Export\n\n",
        "## Paper Register\n\n",
    ]
    for paper in paper_register.get("papers", []):
        urls = paper.get("canonical_urls") or []
        url_text = f" {urls[0]}" if urls else ""
        lines.append(
            f"- `{paper['paper_id']}`: {paper.get('title', paper['paper_id'])}. "
            f"Source status: `{paper.get('source_status', 'unknown')}`; "
            f"evidence quality: `{paper.get('evidence_quality', paper.get('integration_status', 'unknown'))}`; "
            f"claim cards: {claim_counts[paper['paper_id']]}.{url_text}\n"
        )
    lines.append("\n## Source Register\n\n")
    for source in source_register:
        source_id = source.get("source_id", "")
        url = source.get("canonical_url") or source.get("local_path") or source.get("note_path") or ""
        lines.append(
            f"- `{source_id}`: {source.get('title', source_id)}. "
            f"Type: `{source.get('source_type', 'unknown')}`; status: `{source.get('status', 'unknown')}`; "
            f"claim cards: {claim_counts[source_id]}. {url}\n"
        )
    return "".join(lines)


def bibtex_export() -> str:
    paper_register = read_json(PAPER_REGISTER, {})
    source_register = read_json(SOURCE_REGISTER, [])
    entries: list[str] = []
    for paper in paper_register.get("papers", []):
        title = paper.get("title", paper["paper_id"])
        urls = paper.get("canonical_urls") or []
        url = urls[0] if urls else ""
        key = bib_key(paper["paper_id"], title)
        entries.append(
            "@misc{"
            + key
            + ",\n"
            + f"  title = {{{title}}},\n"
            + f"  howpublished = {{{url}}},\n"
            + f"  note = {{{paper.get('source_status', 'unknown')} source status; {paper.get('claim_card_count', 0)} LLM-Wiki Claim Cards}},\n"
            + "}\n"
        )
    for source in source_register:
        source_id = source.get("source_id", "")
        title = source.get("title", source_id)
        url = source.get("canonical_url") or source.get("local_path") or source.get("note_path") or ""
        key = bib_key(source_id, title)
        entries.append(
            "@misc{"
            + key
            + ",\n"
            + f"  title = {{{title}}},\n"
            + f"  howpublished = {{{url}}},\n"
            + f"  note = {{{source.get('source_type', 'source')} source; {source.get('status', 'unknown')}}},\n"
            + "}\n"
        )
    return "\n".join(entries)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["markdown", "bibtex"], default="markdown")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--stdout", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.format == "markdown":
        text = markdown_export()
        output = args.output or REPORTS_DIR / "bibliography.md"
    else:
        text = bibtex_export()
        output = args.output or REPORTS_DIR / "bibliography.bib"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    if args.stdout:
        print(text)
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
