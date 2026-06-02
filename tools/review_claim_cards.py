#!/usr/bin/env python3
"""Review generated Claim Cards without labelling agent work as human review."""

from __future__ import annotations

import argparse
import subprocess
import sys
from collections import Counter
from datetime import date
from pathlib import Path

from generate_claim_cards import (
    card_markdown,
    register_summary,
    update_paper_register_with_claims,
    write_claim_index,
    write_theme_pages,
)
from wiki_claim_utils import (
    CLAIM_REGISTER,
    CLAIMS_DIR,
    GOLDEN_SCENARIOS,
    HIGH_VALUE_TOPIC_OVERRIDES,
    PAPER_REGISTER,
    REVIEW_STATUSES,
    ROOT,
    SOURCE_TOPIC_OVERRIDES,
    TOPIC_RULES,
    claim_card_path,
    is_volatile,
    now,
    read_json,
    write_json,
)


TODAY = date.today().isoformat()
REVIEWER = "tools/review_claim_cards.py schema-traceability pass"


def local_ref_exists(ref: str) -> bool:
    if ref.startswith(("http://", "https://")):
        return True
    if ref.startswith("sources/raw/") and not ref.startswith("sources/raw/redistributable/"):
        return True
    return (ROOT / ref).exists()


def validate_claim(claim: dict) -> list[str]:
    errors: list[str] = []
    required = [
        "claim_id",
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
    ]
    for field in required:
        if field not in claim:
            errors.append(f"missing {field}")
    if claim.get("claim_type") != "gap" and not claim.get("source_refs"):
        errors.append("non-gap claim has no source_refs")
    for ref in claim.get("source_refs", []):
        if not local_ref_exists(ref):
            errors.append(f"source ref not found: {ref}")
    status = claim.get("review_status")
    if status not in REVIEW_STATUSES:
        errors.append(f"invalid review_status: {status}")
    if status == "human-reviewed" and not claim.get("human_reviewer"):
        errors.append("human-reviewed claim lacks human_reviewer")
    locator = claim.get("evidence_locator") or {}
    if not isinstance(locator, dict) or not locator.get("locator"):
        errors.append("missing evidence locator")
    if not claim.get("related_topics"):
        errors.append("missing related_topics")
    if not isinstance(claim.get("confidence"), (float, int)):
        errors.append("confidence must be numeric")
    return errors


def agent_review_claim(claim: dict) -> dict:
    errors = validate_claim(claim)
    claim = dict(claim)
    claim["review_errors"] = errors
    if errors:
        claim["review_status"] = "agent-drafted"
        claim["reviewer"] = REVIEWER
        claim["review_notes"] = "Schema or traceability review failed: " + "; ".join(errors)
    elif claim.get("review_status") in {"agent-drafted", "auto-extracted", "localized", "metadata-only"}:
        claim["review_status"] = "agent-reviewed"
        claim["reviewer"] = REVIEWER
        claim["review_notes"] = "Schema, source-reference, locator, topic, and non-human-review checks passed."
    claim["last_reviewed"] = TODAY
    claim["volatility_flag"] = bool(
        claim.get("volatility_flag")
        or is_volatile(
            claim.get("statement", ""),
            claim.get("source_refs", []),
            claim.get("related_topics", []),
        )
    )
    return claim


def apply_reviewer_manifest(claims: list[dict], manifest_path: Path) -> list[dict]:
    manifest = read_json(manifest_path, {})
    manifest_entries = manifest.get("claims", manifest.get("entries", []))
    decisions = {entry.get("claim_id"): entry for entry in manifest_entries if entry.get("claim_id")}
    reviewer = manifest.get("reviewer", "external reviewer agent")
    reviewed_at = manifest.get("reviewed_at", now())
    updated: list[dict] = []
    for claim in claims:
        decision = decisions.get(claim["claim_id"])
        if not decision:
            updated.append(claim)
            continue
        claim = dict(claim)
        status = decision.get("review_status", "cross-agent-reviewed")
        if status not in REVIEW_STATUSES:
            status = "agent-reviewed"
        if status == "human-reviewed" and not decision.get("human_reviewer"):
            status = "agent-reviewed"
            claim["review_notes"] = "Manifest requested human-reviewed without human_reviewer; retained agent-reviewed."
        elif decision.get("confirmed", False):
            claim["review_status"] = status
            claim["reviewer"] = reviewer
            claim["reviewed_at"] = reviewed_at
            claim["review_notes"] = decision.get(
                "notes",
                "Separate reviewer confirmed traceability, claim type, source locator, and absence of overclaiming.",
            )
            if decision.get("human_reviewer"):
                claim["human_reviewer"] = decision["human_reviewer"]
        else:
            claim["review_status"] = "agent-reviewed"
            claim["reviewer"] = reviewer
            claim["reviewed_at"] = reviewed_at
            claim["review_notes"] = decision.get(
                "notes",
                "Separate reviewer did not confirm this card for cross-agent-reviewed promotion.",
            )
        updated.append(claim)
    return updated


def emit_review_sample(claims: list[dict], output: Path, limit: int) -> None:
    priority_topics = {
        "mcp-governance",
        "agent-safety-and-sandboxing",
        "evidence-observability-and-redress",
        "procurement-and-conformance",
    }
    high_value_papers = set(HIGH_VALUE_TOPIC_OVERRIDES)
    high_value_sources = set(SOURCE_TOPIC_OVERRIDES)
    golden_topics = {topic for topics in GOLDEN_SCENARIOS.values() for topic in topics}
    candidates = [
        claim
        for claim in claims
        if claim.get("volatility_flag")
        or claim.get("claim_type") in {"threat-taxonomy", "governance-control", "procurement-conformance", "safety-control"}
        or priority_topics.intersection(claim.get("related_topics", []))
    ]
    def priority(claim: dict) -> tuple[int, str]:
        score = 0
        if high_value_papers.intersection(claim.get("paper_ids", [])):
            score += 100
        if high_value_sources.intersection(claim.get("source_ids", [])):
            score += 100
        if claim.get("topic_id") in golden_topics:
            score += 50
        if claim.get("claim_type") in {"threat-taxonomy", "governance-control", "procurement-conformance", "safety-control", "evidence-practice"}:
            score += 25
        if claim.get("volatility_flag"):
            score += 10
        return (-score, claim["claim_id"])

    candidates = sorted(candidates, key=priority)[:limit]
    sample = {
        "instructions": (
            "Use a separate agent to confirm traceability, claim type, source locator, and absence of overclaiming. "
            "Return a manifest with confirmed=true only for cards that pass."
        ),
        "review_status_to_apply": "cross-agent-reviewed",
        "claims": [
            {
                "claim_id": claim["claim_id"],
                "statement": claim["statement"],
                "claim_type": claim["claim_type"],
                "source_refs": claim.get("source_refs", []),
                "evidence_locator": claim.get("evidence_locator", {}),
                "review_status": claim.get("review_status"),
                "card_path": claim.get("card_path"),
            }
            for claim in candidates
        ],
    }
    write_json(output, sample)


def write_cards_and_register(claims: list[dict]) -> None:
    for claim in claims:
        path = ROOT / claim["card_path"]
        path.write_text(card_markdown(claim), encoding="utf-8")
    write_claim_index(claims)
    write_theme_pages(claims)
    write_json(CLAIM_REGISTER, register_summary(claims))
    paper_register = read_json(PAPER_REGISTER, {})
    update_paper_register_with_claims(paper_register, claims)
    subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reviewer-manifest", type=Path)
    parser.add_argument("--emit-review-sample", type=Path)
    parser.add_argument("--sample-limit", type=int, default=24)
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    register = read_json(CLAIM_REGISTER, {})
    claims = register.get("claims", [])
    if not claims:
        print("No claims found. Run tools/generate_claim_cards.py first.", file=sys.stderr)
        return 1

    reviewed = [agent_review_claim(claim) for claim in claims]
    if args.reviewer_manifest:
        reviewed = apply_reviewer_manifest(reviewed, args.reviewer_manifest)
    if args.emit_review_sample:
        emit_review_sample(reviewed, args.emit_review_sample, args.sample_limit)
    if not args.no_write:
        write_cards_and_register(reviewed)

    counts = Counter(claim.get("review_status", "unknown") for claim in reviewed)
    print("Review status distribution:")
    for status, count in sorted(counts.items()):
        print(f"- {status}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
