#!/usr/bin/env python3
"""Basic integrity checks for the Code as Agent Harness LLM-Wiki."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from okf_lib import okf_errors


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md",
    "CONTEXT.md",
    "PROGRESS.md",
    "CHANGELOG.md",
    "LLM-WIKI.md",
    "README.md",
    "wiki/AGENTS.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/claims/README.md",
    "wiki/data/claim-register.json",
    "wiki/data/source-register.json",
    "wiki/data/paper-register.json",
]
REDISTRIBUTABLE_RAW_PREFIX = "sources/raw/redistributable/"
VALID_REVIEW_STATUSES = {
    "metadata-only",
    "localized",
    "auto-extracted",
    "agent-drafted",
    "agent-reviewed",
    "cross-agent-reviewed",
    "human-reviewed",
    "decision-grade",
}
VALID_CLAIM_TYPES = {
    "contribution",
    "source-signal",
    "protocol-capability",
    "governance-control",
    "safety-control",
    "threat-taxonomy",
    "evaluation-result",
    "evidence-practice",
    "procurement-conformance",
    "gap",
}
STALE_PHRASES = [
    "source localization needed",
    "source localisation needed",
    "per-paper fragments need generation and source localization",
    "content notes are automated extraction cues and still need human review",
    "replace automated extraction cues with human-reviewed contribution notes",
    "need human review where the fragment only contains automated extraction cues",
]


def is_local_only_raw_path(path: str) -> bool:
    return path.startswith("sources/raw/") and not path.startswith(REDISTRIBUTABLE_RAW_PREFIX)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def check_source_register(errors: list[str]) -> None:
    register_path = ROOT / "wiki/data/source-register.json"
    if not register_path.is_file():
        return
    try:
        entries = json.loads(read(register_path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid source register JSON: {exc}")
        return
    if not isinstance(entries, list):
        errors.append("source register must be a list")
        return
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("source register contains a non-object entry")
            continue
        source_id = entry.get("source_id")
        note_path = entry.get("note_path")
        if not source_id:
            errors.append("source register entry missing source_id")
            continue
        if source_id in seen:
            errors.append(f"duplicate source_id: {source_id}")
        seen.add(source_id)
        if not note_path:
            errors.append(f"{source_id} missing note_path")
            continue
        note = ROOT / note_path
        if not note.is_file():
            errors.append(f"{source_id} note_path not found: {note_path}")
            continue
        note_text = read(note)
        if f'source_id: "{source_id}"' not in note_text and f"source_id: {source_id}" not in note_text:
            errors.append(f"{note_path} does not declare source_id {source_id}")
        local_path = entry.get("local_path")
        if local_path and not is_local_only_raw_path(local_path) and not (ROOT / local_path).is_file():
            errors.append(f"{source_id} local_path not found: {local_path}")


def check_documentation_lockstep(errors: list[str]) -> None:
    agents_text = read(ROOT / "AGENTS.md") if (ROOT / "AGENTS.md").is_file() else ""
    if "Documentation Lockstep" not in agents_text:
        errors.append("AGENTS.md must contain Documentation Lockstep rules")
    readme_text = read(ROOT / "README.md") if (ROOT / "README.md").is_file() else ""
    if "LLM-WIKI.md" not in readme_text:
        errors.append("README.md should link to LLM-WIKI.md")


def check_wiki_links(errors: list[str]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for md in sorted((ROOT / "wiki").rglob("*.md")):
        text = read(md)
        for match in link_re.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (md.parent / clean).resolve()
            if not str(resolved).startswith(str(ROOT)):
                continue
            if not resolved.exists():
                errors.append(f"broken wiki link in {md.relative_to(ROOT)}: {target}")


def check_paper_register(errors: list[str]) -> None:
    register_path = ROOT / "wiki/data/paper-register.json"
    if not register_path.is_file():
        return
    try:
        data = json.loads(read(register_path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid paper register JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append("paper register must be an object")
        return
    papers = data.get("papers")
    if not isinstance(papers, list):
        errors.append("paper register missing papers list")
        return
    seen: set[str] = set()
    for paper in papers:
        if not isinstance(paper, dict):
            errors.append("paper register contains a non-object entry")
            continue
        paper_id = paper.get("paper_id")
        if not paper_id:
            errors.append("paper register entry missing paper_id")
            continue
        if paper_id in seen:
            errors.append(f"duplicate paper_id: {paper_id}")
        seen.add(paper_id)
        fragment = ROOT / "wiki/papers" / f"{paper_id}.md"
        if not fragment.is_file():
            errors.append(f"paper fragment missing for {paper_id}")
            continue
        text = read(fragment)
        if f"paper_id: \"{paper_id}\"" not in text:
            errors.append(f"paper fragment does not declare paper_id: {paper_id}")
        evidence_quality = paper.get("evidence_quality")
        if evidence_quality and evidence_quality not in VALID_REVIEW_STATUSES:
            errors.append(f"{paper_id} has invalid evidence_quality: {evidence_quality}")
        for claim_id in paper.get("claim_card_ids", []):
            if claim_id not in text:
                errors.append(f"{paper_id} fragment missing claim link for {claim_id}")
        for local_path in paper.get("local_source_paths", []):
            if is_local_only_raw_path(local_path):
                continue
            if not (ROOT / local_path).is_file():
                errors.append(f"{paper_id} local source not found: {local_path}")


def check_claim_register(errors: list[str]) -> None:
    register_path = ROOT / "wiki/data/claim-register.json"
    if not register_path.is_file():
        return
    try:
        data = json.loads(read(register_path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid claim register JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append("claim register must be an object")
        return
    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claim register missing claims list")
        return

    paper_register = {}
    paper_register_path = ROOT / "wiki/data/paper-register.json"
    if paper_register_path.is_file():
        paper_data = json.loads(read(paper_register_path))
        if isinstance(paper_data, dict):
            paper_register = {paper.get("paper_id"): paper for paper in paper_data.get("papers", []) if isinstance(paper, dict)}
    source_register = {}
    source_register_path = ROOT / "wiki/data/source-register.json"
    if source_register_path.is_file():
        source_data = json.loads(read(source_register_path))
        if isinstance(source_data, list):
            source_register = {source.get("source_id"): source for source in source_data if isinstance(source, dict)}

    seen: set[str] = set()
    for claim in claims:
        if not isinstance(claim, dict):
            errors.append("claim register contains a non-object entry")
            continue
        claim_id = claim.get("claim_id")
        if not claim_id:
            errors.append("claim register entry missing claim_id")
            continue
        if claim_id in seen:
            errors.append(f"duplicate claim_id: {claim_id}")
        seen.add(claim_id)

        for field in [
            "statement",
            "claim_type",
            "source_refs",
            "paper_ids",
            "source_ids",
            "evidence_locator",
            "extraction_method",
            "review_status",
            "creator",
            "confidence",
            "related_topics",
            "volatility_flag",
            "card_path",
        ]:
            if field not in claim:
                errors.append(f"{claim_id} missing {field}")

        claim_type = claim.get("claim_type")
        if claim_type not in VALID_CLAIM_TYPES:
            errors.append(f"{claim_id} invalid claim_type: {claim_type}")
        review_status = claim.get("review_status")
        if review_status not in VALID_REVIEW_STATUSES:
            errors.append(f"{claim_id} invalid review_status: {review_status}")
        if review_status == "human-reviewed" and not claim.get("human_reviewer"):
            errors.append(f"{claim_id} is human-reviewed without human_reviewer")
        if not claim.get("source_refs"):
            errors.append(f"{claim_id} has no source_refs")
        if not claim.get("related_topics"):
            errors.append(f"{claim_id} has no related_topics")
        if not isinstance(claim.get("confidence"), (int, float)):
            errors.append(f"{claim_id} confidence is not numeric")

        locator = claim.get("evidence_locator")
        if not isinstance(locator, dict) or not locator.get("locator"):
            errors.append(f"{claim_id} missing evidence locator")

        card_path = claim.get("card_path")
        if card_path:
            card = ROOT / card_path
            if not card.is_file():
                errors.append(f"{claim_id} card_path not found: {card_path}")
            else:
                card_text = read(card)
                if claim_id not in card_text:
                    errors.append(f"{card_path} does not contain {claim_id}")
        for paper_id in claim.get("paper_ids", []):
            if paper_id not in paper_register:
                errors.append(f"{claim_id} references unknown paper_id: {paper_id}")
                continue
            fragment = ROOT / "wiki/papers" / f"{paper_id}.md"
            if fragment.is_file() and claim_id not in read(fragment):
                errors.append(f"{claim_id} missing backlink from paper fragment {paper_id}")
        for source_id in claim.get("source_ids", []):
            if source_id not in source_register:
                errors.append(f"{claim_id} references unknown source_id: {source_id}")
        for source_ref in claim.get("source_refs", []):
            if source_ref.startswith(("http://", "https://")):
                continue
            if is_local_only_raw_path(source_ref):
                continue
            if not (ROOT / source_ref).exists():
                errors.append(f"{claim_id} source_ref not found: {source_ref}")


def check_readme_paper_links(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return
    row_re = re.compile(r"^\|\s*\[[^\]]+\]\(([^)]+)\)")
    for lineno, line in enumerate(read(readme).splitlines(), start=1):
        match = row_re.match(line)
        if not match:
            continue
        target = match.group(1)
        if not target.startswith("wiki/papers/"):
            errors.append(f"README paper row {lineno} should link to wiki/papers/: {target}")
            continue
        if not (ROOT / target).is_file():
            errors.append(f"README paper row {lineno} links to missing fragment: {target}")


def check_stale_phrases(errors: list[str]) -> None:
    ingest_path = ROOT / "sources/metadata/wiki-ingest-status.json"
    localization_complete = False
    if ingest_path.is_file():
        try:
            ingest = json.loads(read(ingest_path))
            localization_complete = (
                ingest.get("localized_fragments") == ingest.get("paper_count")
                and ingest.get("pending_fragments", 0) == 0
                and ingest.get("blocked_fragments", 0) == 0
            )
        except json.JSONDecodeError:
            localization_complete = False
    if not localization_complete:
        return
    paths: list[Path] = []
    for rel in ["AGENTS.md", "CONTEXT.md", "PROGRESS.md", "CHANGELOG.md", "LLM-WIKI.md", "wiki/index.md"]:
        path = ROOT / rel
        if path.is_file():
            paths.append(path)
    for folder in ["wiki/topics", "wiki/maps", "wiki/progress", "wiki/papers"]:
        path = ROOT / folder
        if path.is_dir():
            paths.extend(path.rglob("*.md"))
    for path in sorted(set(paths)):
        text = read(path).lower()
        for phrase in STALE_PHRASES:
            if phrase in text:
                errors.append(f"stale phrase in {path.relative_to(ROOT)}: {phrase}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_source_register(errors)
    check_documentation_lockstep(errors)
    check_paper_register(errors)
    check_claim_register(errors)
    check_readme_paper_links(errors)
    check_stale_phrases(errors)
    if (ROOT / "wiki").is_dir():
        check_wiki_links(errors)
    errors.extend(okf_errors())
    if errors:
        print("Wiki validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Wiki validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
