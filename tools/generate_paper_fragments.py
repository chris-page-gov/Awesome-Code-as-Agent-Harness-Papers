#!/usr/bin/env python3
"""Generate paper wiki fragments from README table rows."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
PAPERS_DIR = ROOT / "wiki/papers"
REGISTER = ROOT / "wiki/data/paper-register.json"
PAPER_INDEX = PAPERS_DIR / "README.md"
TODAY = date.today().isoformat()
LOCALIZED_STATUSES = {"localized", "integrated"}
REDISTRIBUTABLE_RAW_PREFIX = "sources/raw/redistributable/"
PRESERVED_FIELDS = {
    "blocked_reason",
    "blocked_url",
    "claim_card_count",
    "claim_card_ids",
    "claim_cards",
    "evidence_quality",
    "integrated_at",
    "integration_status",
    "local_source_paths",
    "source_family",
    "source_file_metadata",
    "source_signal",
    "source_status",
}

PAPER_ROW_RE = re.compile(r"^(\|\s*)\[([^\]]+)\]\(([^)]+)\)([^|]*)(\|\s*)([^|]+?)(\s*\|.*)$")
LOCAL_PAPER_RE = re.compile(r"^wiki/papers/([^/]+\.md)$")


def clean_heading(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^[^A-Za-z0-9]+", "", text).strip()
    return text


def normalize_title(title: str) -> str:
    title = title.replace("\\$", "$").replace("\\.", ".")
    title = unicodedata.normalize("NFKC", title)
    title = re.sub(r"\s+", " ", title).strip().lower()
    title = re.sub(r"[^a-z0-9]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def slug_base(title: str) -> str:
    text = unicodedata.normalize("NFKD", title)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return text[:72].strip("-") or "paper"


def paper_id_for(title: str) -> str:
    norm = normalize_title(title)
    digest = hashlib.sha1(norm.encode("utf-8")).hexdigest()[:8]
    return f"{slug_base(title)}-{digest}"


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(values: list[str]) -> str:
    if not values:
        return "[]"
    return "\n" + "\n".join(f"  - {q(value)}" for value in values)


def yaml_field(name: str, values: list[str]) -> str:
    if not values:
        return f"{name}: []\n"
    return f"{name}:\n" + "\n".join(f"  - {q(value)}" for value in values) + "\n"


def load_existing_register() -> dict[str, dict]:
    if not REGISTER.is_file():
        return {}
    data = json.loads(REGISTER.read_text(encoding="utf-8"))
    papers = data.get("papers", []) if isinstance(data, dict) else []
    return {paper.get("paper_id", ""): paper for paper in papers if isinstance(paper, dict)}


def parse_readme(existing: dict[str, dict]) -> tuple[list[str], dict[str, dict], int]:
    lines = README.read_text(encoding="utf-8").splitlines(keepends=True)
    current_layer = ""
    current_section = ""
    current_subsection = ""
    papers: dict[str, dict] = {}
    row_count = 0

    for idx, line in enumerate(lines):
        line_ending = "\n" if line.endswith("\n") else ""
        stripped = line.strip()
        if stripped.startswith("## "):
            current_layer = clean_heading(stripped[3:])
            current_section = ""
            current_subsection = ""
        elif stripped.startswith("### "):
            current_section = clean_heading(stripped[4:])
            current_subsection = ""
        elif stripped.startswith("#### "):
            current_subsection = clean_heading(stripped[5:])

        match = PAPER_ROW_RE.match(line)
        if not match:
            continue

        prefix, title, url, suffix, venue_prefix, venue, tail = match.groups()
        local_match = LOCAL_PAPER_RE.match(url)
        paper_id = local_match.group(1)[:-3] if local_match else paper_id_for(title)
        paper = papers.setdefault(
            paper_id,
            {
                "paper_id": paper_id,
                "title": title,
                "canonical_urls": [],
                "venues": [],
                "row_suffixes": [],
                "placements": [],
                "source_status": "pending",
                "local_source_paths": [],
            },
        )

        prior = existing.get(paper_id, {})
        for field in PRESERVED_FIELDS:
            if field in prior:
                paper[field] = prior[field]
        for canonical_url in prior.get("canonical_urls", []):
            if canonical_url not in paper["canonical_urls"]:
                paper["canonical_urls"].append(canonical_url)
        for local_source_path in prior.get("local_source_paths", []):
            if local_source_path not in paper["local_source_paths"]:
                paper["local_source_paths"].append(local_source_path)
        if prior.get("source_status") and prior["source_status"] != "pending":
            paper["source_status"] = prior["source_status"]

        if not local_match and url not in paper["canonical_urls"]:
            paper["canonical_urls"].append(url)
        if venue.strip() not in paper["venues"]:
            paper["venues"].append(venue.strip())
        clean_suffix = suffix.strip()
        if clean_suffix and clean_suffix not in paper["row_suffixes"]:
            paper["row_suffixes"].append(clean_suffix)
        placement = {
            "layer": current_layer,
            "section": current_section,
            "subsection": current_subsection,
            "venue": venue.strip(),
            "readme_line": idx + 1,
        }
        paper["placements"].append(placement)

        local_url = f"wiki/papers/{paper_id}.md"
        lines[idx] = f"{prefix}[{title}]({local_url}){suffix}{venue_prefix}{venue}{tail}{line_ending}"
        row_count += 1

    return lines, papers, row_count


def markdown_table_row(values: list[str]) -> str:
    escaped = [value.replace("|", "\\|") for value in values]
    return "| " + " | ".join(escaped) + " |"


def is_local_only_raw_path(source_path: str) -> bool:
    return source_path.startswith("sources/raw/") and not source_path.startswith(REDISTRIBUTABLE_RAW_PREFIX)


def write_fragment(paper: dict) -> None:
    paper_path = PAPERS_DIR / f"{paper['paper_id']}.md"
    canonical_urls = paper["canonical_urls"]
    layers = sorted({p["layer"] for p in paper["placements"] if p["layer"]})
    sections = sorted({p["section"] for p in paper["placements"] if p["section"]})
    subsections = sorted({p["subsection"] for p in paper["placements"] if p["subsection"]})
    venues = paper["venues"]
    source_status = paper.get("source_status", "pending")
    is_localized = source_status in LOCALIZED_STATUSES or bool(paper.get("local_source_paths"))
    is_integrated = source_status == "integrated"
    fragment_status = "source-integrated" if is_integrated else "metadata-only"
    signal = paper.get("source_signal") or {}
    metadata = paper.get("source_file_metadata") or []
    claim_cards = paper.get("claim_cards") or []
    evidence_quality = paper.get("evidence_quality") or paper.get("integration_status") or fragment_status

    lines: list[str] = [
        "---\n",
        f"title: {q(paper['title'])}\n",
        'note_type: "paper"\n',
        f"status: {q(fragment_status)}\n",
        'tags: ["paper", "code-as-agent-harness"]\n',
        f"paper_id: {q(paper['paper_id'])}\n",
        yaml_field("canonical_urls", canonical_urls),
        yaml_field("local_source_paths", paper["local_source_paths"]),
        f"source_status: {q(source_status)}\n",
        f"evidence_quality: {q(evidence_quality)}\n",
        yaml_field("claim_card_ids", paper.get("claim_card_ids", [])),
        yaml_field("survey_layers", layers),
        yaml_field("survey_sections", sections),
        yaml_field("survey_subsections", subsections),
        f'last_reviewed: "{TODAY}"\n',
        "---\n\n",
        f"# {paper['title']}\n\n",
        "## Inventory Metadata\n\n",
        f"- Paper ID: `{paper['paper_id']}`\n",
        f"- Venue labels: {', '.join(venues) if venues else 'not recorded'}\n",
        f"- Source status: `{source_status}`\n",
        "- Canonical URL",
        "s:\n" if len(canonical_urls) != 1 else ":\n",
    ]
    if canonical_urls:
        for url in canonical_urls:
            lines.append(f"  - [{url}]({url})\n")
    else:
        lines.append("  - not recorded in the current README row\n")

    lines.extend(["\n## Survey Placement\n\n"])
    lines.append(markdown_table_row(["Layer", "Section", "Subsection", "Venue"]) + "\n")
    lines.append(markdown_table_row(["---", "---", "---", "---"]) + "\n")
    for placement in paper["placements"]:
        lines.append(
            markdown_table_row(
                [
                    placement.get("layer") or "",
                    placement.get("section") or "",
                    placement.get("subsection") or "",
                    placement.get("venue") or "",
                ]
            )
            + "\n"
        )

    lines.extend(
        [
            "\n## Localized Sources\n\n",
        ]
    )
    if paper["local_source_paths"]:
        for source_path in paper["local_source_paths"]:
            if is_local_only_raw_path(source_path):
                lines.append(f"- `{source_path}` (local evidence cache; not committed by default)\n")
            else:
                lines.append(f"- [{source_path}](../../{source_path})\n")
        if metadata:
            lines.append("\n### Local File Metadata\n\n")
            for entry in metadata:
                bits = [f"path `{entry.get('path', 'unknown')}`"]
                if entry.get("bytes") is not None:
                    bits.append(f"{entry['bytes']} bytes")
                if entry.get("sha256"):
                    bits.append(f"SHA-256 `{entry['sha256']}`")
                lines.append(f"- {', '.join(bits)}\n")
    else:
        lines.append("- No localized source file registered yet.\n")

    lines.extend(
        [
            "\n## Source-Backed Notes\n\n",
            "- Inventory fact: this reference appears in the README paper table with the placement above.\n",
        ]
    )
    if is_integrated and signal:
        extraction = signal.get("extraction") or {}
        lines.append("- Source fact: a localized source file is available in this repository.\n")
        if extraction:
            lines.append(
                "- Source fact: automated local text extraction recorded "
                f"{extraction.get('characters', 0)} characters using `{extraction.get('method', 'unknown')}`.\n"
            )
        term_cues = signal.get("term_cues") or []
        if term_cues:
            rendered = ", ".join(f"`{cue['term']}` ({cue['count']})" for cue in term_cues[:10])
            lines.append(f"- Source cue: localized text contains harness-relevant terms: {rendered}.\n")
        detected = signal.get("detected_topics") or []
        if detected:
            lines.append(f"- Source cue: automated topic tags: {', '.join(f'`{topic}`' for topic in detected)}.\n")
        lines.append("- Integration note: these notes are automated extraction cues; Claim Cards below are agent-created evidence records unless separately reviewed.\n")
    elif is_localized:
        lines.append("- Source fact: a localized source file is available in this repository.\n")
        lines.append("- Content claims are pending claim-card extraction or review of the localized source.\n")
    elif source_status == "blocked":
        lines.append("- Gap: source localization is currently blocked; see the registered blocker below.\n")
    else:
        lines.append("- Content claims are pending source localization and review.\n")

    lines.extend(["\n## Claim Cards\n\n"])
    if claim_cards:
        for claim in claim_cards[:12]:
            card_path = claim.get("card_path", "")
            if card_path.startswith("wiki/claims/"):
                card_link = f"../claims/{Path(card_path).name}"
            else:
                card_link = card_path or "../claims/README.md"
            lines.append(
                f"- [{claim.get('claim_id', 'claim')}]"
                f"({card_link}) - {claim.get('statement', 'Claim Card')} "
                f"(`{claim.get('review_status', 'unknown')}`)\n"
            )
        if len(claim_cards) > 12:
            lines.append(f"- Additional Claim Cards are listed in [the claim register](../claims/README.md); total for this fragment: {len(claim_cards)}.\n")
    else:
        lines.append("- No Claim Cards are registered for this fragment yet.\n")

    lines.extend(
        [
            "\n## Cross-References\n\n",
            "- [Paper index](README.md)\n",
            "- [Taxonomy map](../maps/taxonomy-map.md)\n",
            "\n## Gaps\n\n",
        ]
    )
    if is_integrated:
        if claim_cards:
            lines.append("- Promote high-value agent-reviewed cards to cross-agent-reviewed or decision-grade where warranted.\n")
        else:
            lines.append("- Promote automated extraction cues into agent-reviewed Claim Cards; reserve `human-reviewed` for named human review.\n")
    elif is_localized:
        lines.append("- Review the localized source.\n")
    elif source_status == "blocked":
        reason = paper.get("blocked_reason") or "source could not be localized by automation"
        blocked_url = paper.get("blocked_url") or (canonical_urls[0] if canonical_urls else "")
        lines.append(f"- Source localization blocked for `{blocked_url}`: {reason}.\n")
    else:
        lines.append("- Fetch and review the canonical source.\n")
    lines.append("- Add concise source-backed contribution notes.\n")
    paper_path.write_text("".join(lines), encoding="utf-8")


def write_register(papers: dict[str, dict], row_count: int) -> None:
    ordered = sorted(papers.values(), key=lambda p: normalize_title(p["title"]))
    data = {
        "generated_at": TODAY,
        "source": "README.md",
        "paper_count": len(ordered),
        "readme_row_count": row_count,
        "papers": ordered,
    }
    REGISTER.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_index(papers: dict[str, dict], row_count: int) -> None:
    ordered = sorted(papers.values(), key=lambda p: normalize_title(p["title"]))
    localized = sum(1 for paper in ordered if paper.get("source_status") == "localized")
    by_layer: Counter[str] = Counter()
    for paper in ordered:
        for layer in {p["layer"] for p in paper["placements"] if p["layer"]}:
            by_layer[layer] += 1

    lines = [
        "# Paper Fragments\n\n",
        "This directory stores one reusable wiki fragment per paper or external\n",
        "reference. Fragments are generated from README rows first, then enriched as\n",
        "raw sources are localized and reviewed.\n\n",
        "## Generation Summary\n\n",
        f"- Generated at: {TODAY}\n",
        f"- README table rows parsed: {row_count}\n",
        f"- Unique paper/reference fragments: {len(ordered)}\n",
        f"- Fragments with localized source files: {localized}\n\n",
        "## Counts By Top-Level Layer\n\n",
    ]
    for layer, count in sorted(by_layer.items()):
        lines.append(f"- {layer}: {count}\n")
    lines.extend(["\n## Fragments\n\n"])
    for paper in ordered:
        lines.append(f"- [{paper['title']}]({paper['paper_id']}.md)\n")
    PAPER_INDEX.write_text("".join(lines), encoding="utf-8")


def main() -> int:
    PAPERS_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_existing_register()
    lines, papers, row_count = parse_readme(existing)
    README.write_text("".join(lines), encoding="utf-8")
    for paper in papers.values():
        write_fragment(paper)
    write_register(papers, row_count)
    write_index(papers, row_count)
    print(f"Generated {len(papers)} paper fragments from {row_count} README rows.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
