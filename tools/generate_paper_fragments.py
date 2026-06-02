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


def write_fragment(paper: dict) -> None:
    paper_path = PAPERS_DIR / f"{paper['paper_id']}.md"
    canonical_urls = paper["canonical_urls"]
    layers = sorted({p["layer"] for p in paper["placements"] if p["layer"]})
    sections = sorted({p["section"] for p in paper["placements"] if p["section"]})
    subsections = sorted({p["subsection"] for p in paper["placements"] if p["subsection"]})
    venues = paper["venues"]

    lines: list[str] = [
        "---\n",
        f"title: {q(paper['title'])}\n",
        'note_type: "paper"\n',
        'status: "metadata-only"\n',
        'tags: ["paper", "code-as-agent-harness"]\n',
        f"paper_id: {q(paper['paper_id'])}\n",
        yaml_field("canonical_urls", canonical_urls),
        yaml_field("local_source_paths", paper["local_source_paths"]),
        f"source_status: {q(paper['source_status'])}\n",
        yaml_field("survey_layers", layers),
        yaml_field("survey_sections", sections),
        yaml_field("survey_subsections", subsections),
        f'last_reviewed: "{TODAY}"\n',
        "---\n\n",
        f"# {paper['title']}\n\n",
        "## Inventory Metadata\n\n",
        f"- Paper ID: `{paper['paper_id']}`\n",
        f"- Venue labels: {', '.join(venues) if venues else 'not recorded'}\n",
        f"- Source status: `{paper['source_status']}`\n",
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
            lines.append(f"- [{source_path}](../../{source_path})\n")
    else:
        lines.append("- No localized source file registered yet.\n")

    lines.extend(
        [
            "\n## Source-Backed Notes\n\n",
            "- Inventory fact: this reference appears in the README paper table with the placement above.\n",
            "- Content claims are pending source localization and review.\n",
            "\n## Cross-References\n\n",
            "- [Paper index](README.md)\n",
            "- [Taxonomy map](../maps/taxonomy-map.md)\n",
            "\n## Gaps\n\n",
            "- Fetch and review the canonical source.\n",
            "- Add concise source-backed contribution notes.\n",
        ]
    )
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
        f"- Unique paper/reference fragments: {len(ordered)}\n\n",
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
