#!/usr/bin/env python3
"""Update human-facing wiki progress counts from source registers."""

from __future__ import annotations

import json
import re
from collections import Counter
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"
SOURCE_REGISTER = ROOT / "wiki/data/source-register.json"
STATUS_JSON = ROOT / "sources/metadata/wiki-ingest-status.json"
TODAY = date.today().isoformat()


def read_json(path: Path, default):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def count_state() -> dict:
    paper_register = read_json(PAPER_REGISTER, {"papers": []})
    source_register = read_json(SOURCE_REGISTER, [])
    papers = paper_register.get("papers", [])
    status_counts = Counter(paper.get("source_status", "pending") for paper in papers)
    localized_like = sum(
        1
        for paper in papers
        if paper.get("source_status") in {"localized", "integrated"} or paper.get("local_source_paths")
    )
    integrated = status_counts.get("integrated", 0)
    blocked = status_counts.get("blocked", 0)
    pending = len(papers) - localized_like - blocked
    local_paths = {
        path
        for paper in papers
        for path in paper.get("local_source_paths", [])
        if path.startswith("sources/raw/")
    }
    survey_paths = {
        entry.get("local_path")
        for entry in source_register
        if entry.get("source_id") == "SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026" and entry.get("local_path")
    }
    arxiv_paper_pdfs = {path for path in local_paths if path.startswith("sources/raw/arxiv/")}
    return {
        "updated": TODAY,
        "paper_count": len(papers),
        "localized_fragments": localized_like,
        "integrated_fragments": integrated,
        "blocked_fragments": blocked,
        "pending_fragments": pending,
        "unique_local_source_files": len(local_paths),
        "unique_arxiv_paper_pdfs": len(arxiv_paper_pdfs),
        "survey_localized": bool(survey_paths),
    }


def sub(pattern: str, replacement: str, text: str) -> str:
    new_text, count = re.subn(pattern, replacement, text, flags=re.MULTILINE)
    return new_text if count else text


def update_files(state: dict) -> None:
    localized = state["localized_fragments"]
    integrated = state["integrated_fragments"]
    blocked = state["blocked_fragments"]
    pending = state["pending_fragments"]
    arxiv = state["unique_arxiv_paper_pdfs"]
    complete = (
        localized == state["paper_count"]
        and integrated == state["paper_count"]
        and blocked == 0
        and pending == 0
    )
    scope = f"all {localized}" if complete else f"first {localized}"
    source_status_label = "Done" if complete else "In progress"

    path = ROOT / "CHANGELOG.md"
    text = path.read_text(encoding="utf-8")
    text = sub(r"(?:first|all) \d+ paper\s+fragments", f"{scope} paper fragments", text)
    write_text(path, text)

    path = ROOT / "PROGRESS.md"
    text = path.read_text(encoding="utf-8")
    text = sub(
        r"- \[x\] Localized .*source files for (?:the first )?\d+ paper fragments and updated\s+those fragments\.",
        f"- [x] Localized source files for {scope} paper fragments and updated\n  those fragments.",
        text,
    )
    text = re.sub(
        r"^- \[x\] Auto-integrated .* localized source files into wiki fragments\.\n",
        "",
        text,
        flags=re.MULTILINE,
    )
    pending_marker = "- [ ] Localize source files under `sources/raw/` as network availability allows."
    done_marker = "- [x] Completed source localization under `sources/raw/` for all paper fragments."
    marker = done_marker if complete else pending_marker
    text = text.replace(done_marker, pending_marker)
    text = text.replace(
        pending_marker,
        f"- [x] Auto-integrated {integrated} localized source files into wiki fragments.\n" + marker,
    )
    write_text(path, text)

    path = ROOT / "CONTEXT.md"
    text = path.read_text(encoding="utf-8")
    text = sub(
        r"- Source-localization batches have fetched the survey PDF plus \d+ unique arXiv\s+paper PDFs, covering \d+ paper fragments under\s+\[sources/raw/arxiv/\]\(sources/raw/arxiv/\)\. Fetch status and hashes are",
        f"- Source-localization batches have fetched the survey PDF plus {arxiv} unique arXiv\n"
        f"  paper PDFs, covering {localized} paper fragments under\n"
        "  [sources/raw/arxiv/](sources/raw/arxiv/). Fetch status and hashes are",
        text,
    )
    write_text(path, text)

    path = ROOT / "plans/2026-06-02-llm-wiki-conversion.md"
    text = path.read_text(encoding="utf-8")
    text = sub(r"(?:first|all) \d+ paper fragments", f"{scope} paper fragments", text)
    write_text(path, text)

    path = ROOT / "wiki/index.md"
    text = path.read_text(encoding="utf-8")
    text = sub(r"source files for \d+ paper fragments are localized", f"source files for {localized} paper fragments are localized", text)
    write_text(path, text)

    path = ROOT / "wiki/log.md"
    text = path.read_text(encoding="utf-8")
    text = sub(r"(?:first|all) \d+ paper fragments", f"{scope} paper fragments", text)
    write_text(path, text)

    path = ROOT / "wiki/progress/completion-dashboard.md"
    text = path.read_text(encoding="utf-8")
    text = sub(
        r"\| Bulk source fetch \| (?:In progress|Done) \| .* \|",
        f"| Bulk source fetch | {source_status_label} | {localized} localized, {integrated} integrated, {blocked} blocked, {pending} pending. |",
        text,
    )
    write_text(path, text)

    path = ROOT / "wiki/progress/phase-log.md"
    text = path.read_text(encoding="utf-8")
    text = sub(r"(?:first|all) \d+ paper fragments", f"{scope} paper fragments", text)
    write_text(path, text)


def main() -> int:
    state = count_state()
    STATUS_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    update_files(state)
    print(
        "Wiki status updated: "
        f"localized={state['localized_fragments']} "
        f"integrated={state['integrated_fragments']} "
        f"blocked={state['blocked_fragments']} "
        f"pending={state['pending_fragments']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
