#!/usr/bin/env python3
"""Generate source-bounded Claim Cards for the LLM-Wiki."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from wiki_claim_utils import (
    CLAIM_REGISTER,
    CLAIMS_DIR,
    GOLDEN_SCENARIOS,
    HIGH_VALUE_TOPIC_OVERRIDES,
    PAPER_REGISTER,
    QUALITY_TIERS,
    ROOT,
    SOURCE_REGISTER,
    SOURCE_TOPIC_OVERRIDES,
    TOPIC_RULES,
    best_sentence,
    claim_card_path,
    claim_statement,
    concise_evidence_summary,
    dedupe,
    detect_topics,
    extract_text,
    is_volatile,
    make_claim_id,
    now,
    paper_fragment_path,
    read_json,
    rel,
    slugify,
    source_ids_for_refs,
    split_sentences,
    write_json,
)


TODAY = date.today().isoformat()
CREATOR = "tools/generate_claim_cards.py"


def q(value) -> str:
    return json.dumps(value, ensure_ascii=False)


def yaml_list(name: str, values: list[str]) -> list[str]:
    if not values:
        return [f"{name}: []\n"]
    return [f"{name}:\n"] + [f"  - {q(value)}\n" for value in values]


def card_markdown(claim: dict) -> str:
    lines: list[str] = [
        "---\n",
        f"title: {q(claim['statement'][:96])}\n",
        'note_type: "claim-card"\n',
        f"status: {q(claim['review_status'])}\n",
        'tags: ["claim-card", "llm-wiki", "code-as-agent-harness"]\n',
        f"claim_id: {q(claim['claim_id'])}\n",
        f"claim_type: {q(claim['claim_type'])}\n",
    ]
    lines.extend(yaml_list("paper_ids", claim.get("paper_ids", [])))
    lines.extend(yaml_list("source_ids", claim.get("source_ids", [])))
    lines.extend(yaml_list("source_refs", claim.get("source_refs", [])))
    lines.extend(yaml_list("related_topics", claim.get("related_topics", [])))
    lines.extend(
        [
            f"evidence_locator: {q(claim['evidence_locator']['locator'])}\n",
            f"extraction_method: {q(claim['extraction_method'])}\n",
            f"review_status: {q(claim['review_status'])}\n",
            f"creator: {q(claim['creator'])}\n",
            f"reviewer: {q(claim.get('reviewer', ''))}\n",
            f"confidence: {claim['confidence']:.2f}\n",
            f"volatility_flag: {str(bool(claim['volatility_flag'])).lower()}\n",
            f"last_reviewed: {q(claim['last_reviewed'])}\n",
            "---\n\n",
            f"# {claim['claim_id']}\n\n",
            "## Statement\n\n",
            f"{claim['statement']}\n\n",
            "## Evidence\n\n",
        ]
    )
    if claim.get("paper_ids"):
        lines.append("- Paper fragment")
        lines.append("s:\n" if len(claim["paper_ids"]) != 1 else ":\n")
        for paper_id in claim["paper_ids"]:
            lines.append(f"  - [{paper_id}](../papers/{paper_id}.md)\n")
    if claim.get("source_ids"):
        lines.append("- Source ID")
        lines.append("s:\n" if len(claim["source_ids"]) != 1 else ":\n")
        for source_id in claim["source_ids"]:
            lines.append(f"  - `{source_id}`\n")
    lines.append("- Source refs:\n")
    for ref in claim.get("source_refs", []):
        lines.append(f"  - `{ref}`\n")
    locator = claim["evidence_locator"]
    lines.extend(
        [
            f"- Locator: {locator['locator']}\n",
            f"- Matched terms: {', '.join(f'`{term}`' for term in locator.get('matched_terms', [])) or 'none recorded'}\n",
            f"- Evidence summary: {claim['evidence_summary']}\n",
            "\n## Review\n\n",
            f"- Review status: `{claim['review_status']}`\n",
            f"- Creator: `{claim['creator']}`\n",
            f"- Reviewer: `{claim.get('reviewer', '') or 'not yet reviewed by a separate agent'}`\n",
            f"- Confidence: `{claim['confidence']:.2f}`\n",
            f"- Volatile source flag: `{str(bool(claim['volatility_flag'])).lower()}`\n",
            "\n## Topics\n\n",
        ]
    )
    for topic in claim.get("related_topics", []):
        if (ROOT / "wiki/topics" / f"{topic}.md").is_file():
            lines.append(f"- [{topic}](../topics/{topic}.md)\n")
        else:
            lines.append(f"- `{topic}`\n")
    return "".join(lines)


def extraction_for_refs(refs: list[str], max_pages: int, timeout: int, max_chars: int) -> tuple[str, str, list[dict]]:
    texts: list[str] = []
    methods: list[str] = []
    source_metadata: list[dict] = []
    for source_ref in refs:
        path = ROOT / source_ref
        if not path.is_file():
            continue
        text, method = extract_text(path, max_pages=max_pages, timeout=timeout, max_chars=max_chars)
        texts.append(text)
        methods.append(method)
        try:
            source_metadata.append({"path": source_ref, "bytes": path.stat().st_size})
        except OSError:
            source_metadata.append({"path": source_ref})
    return "\n\n".join(texts), "+".join(sorted(set(methods))) or "unavailable", source_metadata


def survey_topics(paper: dict) -> list[str]:
    topics: list[str] = []
    for section in paper.get("survey_sections", []) + paper.get("survey_subsections", []):
        lowered = section.lower()
        if "feedback" in lowered:
            topics.append("evaluation")
        if "debug" in lowered or "code" in lowered:
            topics.append("code-execution")
        if "multi-agent" in lowered or "multi agent" in lowered:
            topics.append("multi-agent")
        if "tool" in lowered:
            topics.append("tools")
        if "memory" in lowered or "context" in lowered:
            topics.append("memory")
    return topics


def topic_sequence_for_paper(paper: dict, text: str) -> tuple[list[str], bool]:
    paper_id = paper["paper_id"]
    high_value = paper_id in HIGH_VALUE_TOPIC_OVERRIDES
    signal_topics = []
    signal = paper.get("source_signal") or {}
    signal_topics.extend(signal.get("detected_topics") or [])
    topics = HIGH_VALUE_TOPIC_OVERRIDES.get(paper_id, [])
    topics += detect_topics(paper.get("title", ""), text, existing_topics=signal_topics)
    topics += survey_topics(paper)
    return dedupe([topic for topic in topics if topic in TOPIC_RULES]), high_value


def make_claim(
    *,
    title: str,
    claim_type: str,
    topic: str,
    source_refs: list[str],
    source_ids: list[str],
    paper_ids: list[str],
    extraction_method: str,
    sentence: str,
    matched_terms: list[str],
    locator: str,
    confidence: float,
    is_gap: bool = False,
) -> dict:
    related_topics = TOPIC_RULES.get(topic, {}).get("related_topics", [])
    statement = claim_statement(title, topic, sentence, is_gap=is_gap)
    seed = "|".join([title, topic, locator, statement, ",".join(source_refs), ",".join(paper_ids), ",".join(source_ids)])
    claim_id = make_claim_id(seed)
    review_status = "agent-drafted"
    volatility = is_volatile(statement, source_refs, related_topics + [topic])
    return {
        "claim_id": claim_id,
        "statement": statement,
        "claim_type": claim_type,
        "source_refs": source_refs,
        "paper_ids": paper_ids,
        "source_ids": source_ids,
        "evidence_locator": {
            "source_path": source_refs[0] if source_refs else "",
            "locator": locator,
            "matched_terms": matched_terms,
        },
        "extraction_method": extraction_method,
        "review_status": review_status,
        "creator": CREATOR,
        "reviewer": "",
        "confidence": confidence,
        "related_topics": related_topics,
        "topic_id": topic,
        "volatility_flag": volatility,
        "created_at": now(),
        "last_reviewed": TODAY,
        "card_path": claim_card_path(claim_id),
        "evidence_summary": concise_evidence_summary(sentence, topic, matched_terms),
    }


def claims_for_paper(paper: dict, source_register: list[dict], args: argparse.Namespace) -> list[dict]:
    refs = [ref for ref in paper.get("local_source_paths", []) if ref]
    text, method, _ = extraction_for_refs(refs, max_pages=args.max_pages, timeout=args.timeout, max_chars=args.max_chars)
    sentences = split_sentences(text)
    topics, high_value = topic_sequence_for_paper(paper, text)
    target = args.high_value_target if high_value else args.target_per_paper
    claims: list[dict] = []
    used_topics: set[str] = set()
    title = paper.get("title", paper["paper_id"])
    source_ids = source_ids_for_refs(refs, source_register)

    for topic in topics:
        if len(claims) >= target:
            break
        if topic in used_topics:
            continue
        sentence, matched = best_sentence(sentences, topic, title=title)
        if not sentence and len(text) < args.min_claim_chars:
            continue
        if not sentence:
            matched = TOPIC_RULES[topic]["terms"][:2]
            locator = "paper register and local source metadata; source text did not expose a focused sentence"
            confidence = 0.48
            is_gap = True
            claim_type = "gap"
        else:
            locator = f"{refs[0] if refs else paper_fragment_path(paper['paper_id'])}; extracted sentence match for {topic}"
            confidence = 0.82 if high_value else 0.72
            is_gap = False
            claim_type = TOPIC_RULES[topic]["claim_type"]
        claims.append(
            make_claim(
                title=title,
                claim_type=claim_type,
                topic=topic,
                source_refs=refs or [paper_fragment_path(paper["paper_id"])],
                source_ids=source_ids,
                paper_ids=[paper["paper_id"]],
                extraction_method=method,
                sentence=sentence,
                matched_terms=matched,
                locator=locator,
                confidence=confidence,
                is_gap=is_gap,
            )
        )
        used_topics.add(topic)

    if not claims:
        topic = topics[0] if topics else "code-execution"
        claims.append(
            make_claim(
                title=title,
                claim_type="gap",
                topic=topic,
                source_refs=refs or [paper_fragment_path(paper["paper_id"])],
                source_ids=source_ids,
                paper_ids=[paper["paper_id"]],
                extraction_method=method,
                sentence="",
                matched_terms=[],
                locator="localized source unavailable or too thin for source-level claim extraction",
                confidence=0.35,
                is_gap=True,
            )
        )

    return claims


def claims_for_source(source: dict, source_register: list[dict], args: argparse.Namespace) -> list[dict]:
    source_id = source.get("source_id", "")
    refs = [ref for ref in [source.get("local_path"), source.get("note_path")] if ref]
    text, method, _ = extraction_for_refs([ref for ref in refs if not ref.startswith("wiki/")], max_pages=args.max_pages, timeout=args.timeout, max_chars=args.max_chars)
    if not text and source.get("note_path"):
        note = ROOT / source["note_path"]
        if note.is_file():
            text = note.read_text(encoding="utf-8")
            method = "markdown-note"
    sentences = split_sentences(text)
    title = source.get("title", source_id)
    topics = dedupe(SOURCE_TOPIC_OVERRIDES.get(source_id, []) + detect_topics(title, text))
    target = args.high_value_target if source_id in SOURCE_TOPIC_OVERRIDES else max(2, args.target_per_paper)
    claims: list[dict] = []
    for topic in topics:
        if len(claims) >= target:
            break
        if topic not in TOPIC_RULES:
            continue
        sentence, matched = best_sentence(sentences, topic, title=title)
        is_gap = not sentence
        claim_type = "gap" if is_gap else TOPIC_RULES[topic]["claim_type"]
        locator = f"{refs[0] if refs else source.get('canonical_url', source_id)}; source-note or local-source match for {topic}"
        claims.append(
            make_claim(
                title=title,
                claim_type=claim_type,
                topic=topic,
                source_refs=refs or [source.get("canonical_url", source_id)],
                source_ids=[source_id] if source_id else [],
                paper_ids=[],
                extraction_method=method or "source-register",
                sentence=sentence,
                matched_terms=matched,
                locator=locator,
                confidence=0.78 if sentence else 0.40,
                is_gap=is_gap,
            )
        )
    return claims


def write_claim_cards(claims: list[dict], clean: bool) -> None:
    CLAIMS_DIR.mkdir(parents=True, exist_ok=True)
    if clean:
        for path in CLAIMS_DIR.glob("claim-*.md"):
            path.unlink()
    for claim in claims:
        path = ROOT / claim["card_path"]
        path.write_text(card_markdown(claim), encoding="utf-8")


def write_claim_index(claims: list[dict]) -> None:
    by_topic: dict[str, list[dict]] = defaultdict(list)
    for claim in claims:
        for topic in claim.get("related_topics", []):
            by_topic[topic].append(claim)
    lines = [
        "# Claim Cards\n\n",
        "Claim Cards are atomic, source-bounded wiki evidence records. They are generated from localized source files and reviewed using explicit agent/human review tiers.\n\n",
        "## Review Tiers\n\n",
    ]
    for tier in sorted(QUALITY_TIERS):
        lines.append(f"- `{tier}`\n")
    lines.extend(["\n## Summary\n\n", f"- Claim count: {len(claims)}\n"])
    status_counts = Counter(claim.get("review_status", "unknown") for claim in claims)
    for status, count in sorted(status_counts.items()):
        lines.append(f"- `{status}`: {count}\n")
    lines.append("\n## Golden Topics\n\n")
    for topic, required in GOLDEN_SCENARIOS.items():
        count = sum(1 for claim in claims if topic in claim.get("related_topics", []))
        lines.append(f"- [{topic}](../topics/{topic}.md): {count} claims; required cues: {', '.join(required)}\n")
    lines.append("\n## Cards\n\n")
    for claim in sorted(claims, key=lambda item: item["claim_id"]):
        lines.append(f"- [{claim['claim_id']}]({Path(claim['card_path']).name}) - {claim['statement']}\n")
    (CLAIMS_DIR / "README.md").write_text("".join(lines), encoding="utf-8")


def register_summary(claims: list[dict]) -> dict:
    status_counts = Counter(claim.get("review_status", "unknown") for claim in claims)
    type_counts = Counter(claim.get("claim_type", "unknown") for claim in claims)
    topic_counts: Counter = Counter()
    paper_counts: Counter = Counter()
    source_counts: Counter = Counter()
    for claim in claims:
        for topic in claim.get("related_topics", []):
            topic_counts[topic] += 1
        for paper_id in claim.get("paper_ids", []):
            paper_counts[paper_id] += 1
        for source_id in claim.get("source_ids", []):
            source_counts[source_id] += 1
    return {
        "generated_at": now(),
        "claim_count": len(claims),
        "review_status_counts": dict(sorted(status_counts.items())),
        "claim_type_counts": dict(sorted(type_counts.items())),
        "topic_counts": dict(sorted(topic_counts.items())),
        "paper_coverage_count": len(paper_counts),
        "source_coverage_count": len(source_counts),
        "claims": sorted(claims, key=lambda item: item["claim_id"]),
    }


def update_paper_register_with_claims(paper_register: dict, claims: list[dict]) -> None:
    by_paper: dict[str, list[dict]] = defaultdict(list)
    for claim in claims:
        for paper_id in claim.get("paper_ids", []):
            by_paper[paper_id].append(claim)

    for paper in paper_register.get("papers", []):
        paper_claims = sorted(by_paper.get(paper.get("paper_id", ""), []), key=lambda claim: claim["claim_id"])
        paper["claim_card_ids"] = [claim["claim_id"] for claim in paper_claims]
        paper["claim_card_count"] = len(paper_claims)
        paper["claim_cards"] = [
            {
                "claim_id": claim["claim_id"],
                "claim_type": claim["claim_type"],
                "review_status": claim["review_status"],
                "statement": claim["statement"],
                "card_path": claim["card_path"],
                "related_topics": claim.get("related_topics", []),
            }
            for claim in paper_claims
        ]
        statuses = {claim["review_status"] for claim in paper_claims}
        if "decision-grade" in statuses:
            paper["evidence_quality"] = "decision-grade"
        elif "human-reviewed" in statuses:
            paper["evidence_quality"] = "human-reviewed"
        elif "cross-agent-reviewed" in statuses:
            paper["evidence_quality"] = "cross-agent-reviewed"
        elif "agent-reviewed" in statuses:
            paper["evidence_quality"] = "agent-reviewed"
        elif paper_claims:
            paper["evidence_quality"] = "agent-drafted"
        else:
            paper["evidence_quality"] = paper.get("integration_status") or paper.get("source_status", "metadata-only")

    write_json(PAPER_REGISTER, paper_register)


def write_topic_page(topic_id: str, title: str, intro: str, claims: list[dict]) -> None:
    topic_path = ROOT / "wiki/topics" / f"{topic_id}.md"
    relevant = [claim for claim in claims if topic_id in claim.get("related_topics", [])]
    lines = [
        "---\n",
        f"title: {q(title)}\n",
        'note_type: "topic"\n',
        'status: "agent-reviewed"\n',
        'tags: ["topic", "claim-backed", "code-as-agent-harness"]\n',
        f"updated: {q(TODAY)}\n",
        "---\n\n",
        f"# {title}\n\n",
        intro.strip() + "\n\n",
        "## Claim-Backed Evidence\n\n",
    ]
    for claim in sorted(relevant, key=lambda item: (-item["confidence"], item["claim_id"]))[:30]:
        path = Path(claim["card_path"]).name
        lines.append(f"- [{claim['claim_id']}](../claims/{path}) - {claim['statement']} (`{claim['review_status']}`)\n")
    lines.extend(
        [
            "\n## Gaps And Recheck Notes\n\n",
            "- Claim Cards marked `volatile` need official-source recheck before policy or procurement use.\n",
            "- `agent-drafted` and `agent-reviewed` cards are not human-reviewed; use `human-reviewed` only when a named human reviewer is recorded.\n",
            "- Gap cards identify weak local extraction or insufficient claim-level evidence.\n",
        ]
    )
    topic_path.write_text("".join(lines), encoding="utf-8")


def write_theme_pages(claims: list[dict]) -> None:
    write_topic_page(
        "mcp-governance",
        "MCP Governance",
        "This synthesis page uses Claim Cards to track MCP protocol, authorization, registry, gateway, threat, and procurement-conformance evidence.",
        claims,
    )
    write_topic_page(
        "agent-safety-and-sandboxing",
        "Agent Safety And Sandboxing",
        "This synthesis page uses Claim Cards to track rollback, isolation, capability governance, safe execution, threat, and safeguard evidence for agent harnesses.",
        claims,
    )
    write_topic_page(
        "evidence-observability-and-redress",
        "Evidence, Observability, And Redress",
        "This synthesis page uses Claim Cards to track approval, traceability, redress, evaluation, evidence-store, and auditability evidence.",
        claims,
    )
    write_topic_page(
        "procurement-and-conformance",
        "Procurement And Conformance",
        "This synthesis page uses Claim Cards to track conformance evidence, review tiers, official-source volatility, and procurement-facing controls.",
        claims,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-per-paper", type=int, default=3)
    parser.add_argument("--high-value-target", type=int, default=10)
    parser.add_argument("--max-pages", type=int, default=6)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-chars", type=int, default=60000)
    parser.add_argument("--min-claim-chars", type=int, default=500)
    parser.add_argument("--clean", action="store_true", help="Remove previously generated claim card markdown files before writing.")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit for development runs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paper_register = read_json(PAPER_REGISTER, {})
    source_register = read_json(SOURCE_REGISTER, [])
    papers = paper_register.get("papers", [])
    if args.limit:
        papers = papers[: args.limit]

    claims: list[dict] = []
    for index, paper in enumerate(papers, start=1):
        claims.extend(claims_for_paper(paper, source_register, args))
        if index % 50 == 0:
            print(f"Generated claims for {index} papers...", flush=True)

    for source in source_register:
        if source.get("source_id") in SOURCE_TOPIC_OVERRIDES:
            claims.extend(claims_for_source(source, source_register, args))

    unique: dict[str, dict] = {}
    for claim in claims:
        unique[claim["claim_id"]] = claim
    claims = list(unique.values())

    write_claim_cards(claims, clean=args.clean)
    write_claim_index(claims)
    write_json(CLAIM_REGISTER, register_summary(claims))
    update_paper_register_with_claims(paper_register, claims)
    write_theme_pages(claims)

    subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)
    print(f"Generated {len(claims)} Claim Cards.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
