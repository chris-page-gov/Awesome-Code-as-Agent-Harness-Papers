#!/usr/bin/env python3
"""Evaluate the LLM-Wiki evidence layer against reusable scenarios."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

from wiki_claim_utils import (
    CLAIM_REGISTER,
    GOLDEN_SCENARIOS,
    PAPER_REGISTER,
    REPORTS_DIR,
    ROOT,
    SOURCE_REGISTER,
    STALE_PHRASES,
    claim_counts_by,
    read_json,
)


TODAY = date.today().isoformat()
POST_REPORT = REPORTS_DIR / "llm-wiki-primary-source-evaluation-post-claim-cards.md"
BASELINE_REPORT = REPORTS_DIR / "llm-wiki-primary-source-evaluation.md"
GOLDEN_PATH = ROOT / "tests/wiki_eval/golden_scenarios.json"


def load_golden_scenarios() -> dict:
    if GOLDEN_PATH.is_file():
        return json.loads(GOLDEN_PATH.read_text(encoding="utf-8"))
    return {
        key: {"required_topic_ids": value}
        for key, value in GOLDEN_SCENARIOS.items()
    }


def report_claim_backing() -> dict:
    claimish = re.compile(r"\b(should|must|requires?|recommends?|threat|governance|protocol|sandbox|approval|audit|evidence|redress|procurement|conformance)\b", re.I)
    backed = 0
    total = 0
    details: dict[str, dict] = {}
    for report in sorted(REPORTS_DIR.glob("*.md")):
        if report.name == POST_REPORT.name:
            continue
        report_backed = 0
        report_total = 0
        for line in report.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "---", "title:", "tags:", "status:", "note_type:", "last_reviewed:")):
                continue
            if claimish.search(stripped):
                report_total += 1
                total += 1
                if "../claims/" in stripped or "CLAIM-" in stripped:
                    report_backed += 1
                    backed += 1
        details[str(report.relative_to(ROOT))] = {"claimish_lines": report_total, "backed_lines": report_backed}
    pct = round((backed / total) * 100, 1) if total else 0.0
    return {"claimish_lines": total, "backed_lines": backed, "backed_percentage": pct, "details": details}


def evidence_packet_backing() -> dict:
    packet_dir = REPORTS_DIR / "evidence-packets"
    packet_paths = sorted(packet_dir.glob("*.md")) if packet_dir.is_dir() else []
    backed_packets = 0
    claim_links = 0
    details: dict[str, dict] = {}
    for packet in packet_paths:
        text = packet.read_text(encoding="utf-8")
        links = len(re.findall(r"\.\./\.\./claims/claim-[a-f0-9]+\.md", text))
        if links:
            backed_packets += 1
        claim_links += links
        details[str(packet.relative_to(ROOT))] = {"claim_links": links, "claim_backed": links > 0}
    pct = round((backed_packets / len(packet_paths)) * 100, 1) if packet_paths else 0.0
    return {
        "packet_count": len(packet_paths),
        "claim_backed_packet_count": backed_packets,
        "claim_backed_packet_percentage": pct,
        "claim_links": claim_links,
        "details": details,
    }


def stale_gap_count() -> dict:
    hits: list[dict] = []
    checked_roots = [ROOT / "AGENTS.md", ROOT / "CONTEXT.md", ROOT / "PROGRESS.md", ROOT / "CHANGELOG.md", ROOT / "LLM-WIKI.md", ROOT / "wiki"]
    for root in checked_roots:
        paths = [root] if root.is_file() else sorted(root.rglob("*.md"))
        for path in paths:
            if path.name == BASELINE_REPORT.name:
                continue
            text = path.read_text(encoding="utf-8")
            lowered = text.lower()
            for phrase in STALE_PHRASES:
                if phrase in lowered:
                    hits.append({"path": str(path.relative_to(ROOT)), "phrase": phrase})
    return {"count": len(hits), "hits": hits[:50]}


def run_check_wiki() -> dict:
    result = subprocess.run(
        ["python3", "tools/check_wiki.py"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return {
        "returncode": result.returncode,
        "passed": result.returncode == 0,
        "stdout": result.stdout.strip(),
        "stderr": result.stderr.strip(),
    }


def golden_results(claims: list[dict], scenarios: dict) -> dict:
    results: dict[str, dict] = {}
    by_related: dict[str, list[dict]] = defaultdict(list)
    for claim in claims:
        for topic in claim.get("related_topics", []):
            by_related[topic].append(claim)
    for scenario_id, spec in scenarios.items():
        required = spec.get("required_topic_ids", spec if isinstance(spec, list) else [])
        scenario_claims = by_related.get(scenario_id, [])
        observed_topic_ids = {claim.get("topic_id") for claim in scenario_claims}
        missing = [topic for topic in required if topic not in observed_topic_ids]
        bibliography_ids = sorted({pid for claim in scenario_claims for pid in claim.get("paper_ids", [])})
        results[scenario_id] = {
            "required_topic_ids": required,
            "claim_count": len(scenario_claims),
            "observed_topic_ids": sorted(topic for topic in observed_topic_ids if topic),
            "missing_topic_ids": missing,
            "passed": not missing and len(scenario_claims) > 0,
            "bibliography_ids": bibliography_ids[:20],
        }
    return results


def collect_metrics() -> dict:
    paper_register = read_json(PAPER_REGISTER, {})
    source_register = read_json(SOURCE_REGISTER, [])
    claim_register = read_json(CLAIM_REGISTER, {})
    claims = claim_register.get("claims", [])
    papers = paper_register.get("papers", [])
    claim_by_paper = claim_counts_by("paper_ids", claims)
    claim_by_source = claim_counts_by("source_ids", claims)
    status_counts = Counter(claim.get("review_status", "unknown") for claim in claims)
    type_counts = Counter(claim.get("claim_type", "unknown") for claim in claims)
    volatile_count = sum(1 for claim in claims if claim.get("volatility_flag"))
    gap_count = sum(1 for claim in claims if claim.get("claim_type") == "gap")
    zero_claim_papers = [paper["paper_id"] for paper in papers if claim_by_paper.get(paper["paper_id"], 0) == 0]
    low_claim_papers = [paper["paper_id"] for paper in papers if 0 < claim_by_paper.get(paper["paper_id"], 0) < 3]
    scenarios = load_golden_scenarios()
    return {
        "generated_at": TODAY,
        "paper_count": len(papers),
        "source_count": len(source_register),
        "claim_count": len(claims),
        "paper_claim_coverage_count": len([paper for paper in papers if claim_by_paper.get(paper["paper_id"], 0) > 0]),
        "paper_claim_coverage_percentage": round((len(papers) - len(zero_claim_papers)) / len(papers) * 100, 1) if papers else 0.0,
        "zero_claim_papers": zero_claim_papers,
        "low_claim_papers_count": len(low_claim_papers),
        "review_status_distribution": dict(sorted(status_counts.items())),
        "claim_type_distribution": dict(sorted(type_counts.items())),
        "volatile_official_protocol_legal_sources_needing_recheck": volatile_count,
        "cases_requiring_original_or_official_source_access": gap_count + volatile_count,
        "gap_claim_count": gap_count,
        "report_claim_backing": report_claim_backing(),
        "evidence_packet_backing": evidence_packet_backing(),
        "stale_gap_count": stale_gap_count(),
        "golden_scenarios": golden_results(claims, scenarios),
        "broken_link_schema_check": run_check_wiki(),
    }


def write_report(metrics: dict) -> None:
    baseline_summary = (
        "The prior evaluation found that the wiki was strong for discovery and provenance, "
        "but weak for claim granularity: paper fragments were mostly automated cues and reports cited whole fragments rather than atomic claims."
    )
    lines = [
        "---\n",
        'title: "LLM-Wiki Primary Source Evaluation After Claim Cards"\n',
        'note_type: "report"\n',
        'status: "agent-reviewed"\n',
        'tags: ["report", "llm-wiki", "evaluation", "claim-card"]\n',
        f'last_reviewed: "{TODAY}"\n',
        "---\n\n",
        "# LLM-Wiki Primary Source Evaluation After Claim Cards\n\n",
        "## Baseline\n\n",
        baseline_summary + "\n\n",
        f"- Baseline report: [LLM-Wiki primary-source evaluation](llm-wiki-primary-source-evaluation.md)\n",
        "- Baseline Claim Cards: `0`\n",
        "- Baseline report-claim backing: whole-fragment and source-note citations, not claim-card citations.\n\n",
        "## Current Run\n\n",
        f"- Claim Cards: `{metrics['claim_count']}`\n",
        f"- Paper coverage: `{metrics['paper_claim_coverage_count']}/{metrics['paper_count']}` ({metrics['paper_claim_coverage_percentage']}%)\n",
        f"- Papers with fewer than 3 cards: `{metrics['low_claim_papers_count']}`\n",
        f"- Gap cards: `{metrics['gap_claim_count']}`\n",
        f"- Volatile official/protocol/legal/vendor recheck flags: `{metrics['volatile_official_protocol_legal_sources_needing_recheck']}`\n",
        f"- Cases requiring original or official source access before decision use: `{metrics['cases_requiring_original_or_official_source_access']}`\n",
        f"- Stale-gap phrase count: `{metrics['stale_gap_count']['count']}`\n",
        f"- Wiki validation passed: `{str(metrics['broken_link_schema_check']['passed']).lower()}`\n",
        "\n## Review Status Distribution\n\n",
    ]
    for status, count in metrics["review_status_distribution"].items():
        lines.append(f"- `{status}`: {count}\n")
    lines.append("\n## Claim Type Distribution\n\n")
    for claim_type, count in metrics["claim_type_distribution"].items():
        lines.append(f"- `{claim_type}`: {count}\n")
    backing = metrics["report_claim_backing"]
    packet_backing = metrics["evidence_packet_backing"]
    lines.extend(
        [
            "\n## Report Claim Backing\n\n",
            "### Legacy Reports\n\n",
            f"- Claim-like report lines: `{backing['claimish_lines']}`\n",
            f"- Lines directly backed by Claim Cards: `{backing['backed_lines']}`\n",
            f"- Backed percentage: `{backing['backed_percentage']}%`\n",
            "\nThis metric remains conservative because pre-existing reports were intentionally preserved as the baseline comparison. New evidence packets and topic pages cite Claim Cards directly.\n\n",
            "### Evidence Packets\n\n",
            f"- Evidence packets: `{packet_backing['packet_count']}`\n",
            f"- Claim-backed packets: `{packet_backing['claim_backed_packet_count']}`\n",
            f"- Claim-backed packet percentage: `{packet_backing['claim_backed_packet_percentage']}%`\n",
            f"- Direct Claim Card links in packets: `{packet_backing['claim_links']}`\n\n",
            "## Golden Scenarios\n\n",
        ]
    )
    for scenario, result in metrics["golden_scenarios"].items():
        lines.append(
            f"- `{scenario}`: passed `{str(result['passed']).lower()}`, "
            f"claims `{result['claim_count']}`, missing topics `{', '.join(result['missing_topic_ids']) or 'none'}`.\n"
        )
    lines.extend(
        [
            "\n## Before/After Comparison\n\n",
            "| Dimension | Before | After |\n",
            "| --- | --- | --- |\n",
            "| Discovery | Fast paper/source discovery | Fast discovery plus atomic Claim Cards |\n",
            "| Provenance | Local source paths and hashes | Local paths, hashes, claim IDs, source refs, locators, and review status |\n",
            "| Claim granularity | Automated cues in fragments | Claim Cards linked from fragments and topic pages |\n",
            "| Review language | Some pages implied human review was pending | Agent review tiers are explicit; `human-reviewed` is literal and requires a human reviewer |\n",
            "| Evidence packets | Manual report assembly | `tools/build_evidence_packet.py` produces claim-backed packets and bibliography |\n",
            "| Reusability | One-off evaluation report | Reusable evaluation suite under `tools/evaluate_llm_wiki.py` and `tests/wiki_eval/` |\n",
            "\n## Examples\n\n",
            "- Example A, MCP governance: the topic now requires MCP protocol, authorization, registry, gateway, and threat Claim Cards.\n",
            "- Example B, sandboxing and containment: the topic now requires rollback, isolation, capability governance, and safe execution Claim Cards.\n",
            "- Example C, human oversight and evidence: the topic now requires approval, traceability, redress, evaluation, and evidence-store Claim Cards.\n",
            "\n## Recommendations\n\n",
            "1. Use evidence packets as the entry point for future policy reports, then promote any recurring gap into a Claim Card task.\n",
            "2. Use `cross-agent-reviewed` for cards confirmed by a separate agent manifest; reserve `human-reviewed` for named human review.\n",
            "3. Recheck volatile protocol, official, legal, and vendor sources before procurement or policy use.\n",
            "4. Expand page/section locators over time for decision-grade cards where PDFs have stable pagination.\n",
            "\n## Implementation Plan\n\n",
            "1. Run `tools/generate_claim_cards.py` after localization or source-register changes.\n",
            "2. Run `tools/review_claim_cards.py --emit-review-sample wiki/data/claim-review-sample.json` and send the sample to a separate reviewer agent.\n",
            "3. Apply confirmed review manifests with `tools/review_claim_cards.py --reviewer-manifest <manifest>`.\n",
            "4. Run `tools/evaluate_llm_wiki.py --write-report` and commit the report with generated evidence packets.\n",
            "5. Promote high-confidence, repeatedly used cards to `decision-grade` only after source-specific review criteria are met.\n",
        ]
    )
    POST_REPORT.write_text("".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metrics = collect_metrics()
    if args.write_report:
        write_report(metrics)
    if args.json:
        print(json.dumps(metrics, indent=2, ensure_ascii=False))
    else:
        print(f"Claim Cards: {metrics['claim_count']}")
        print(f"Paper coverage: {metrics['paper_claim_coverage_count']}/{metrics['paper_count']}")
        print(f"Wiki validation passed: {metrics['broken_link_schema_check']['passed']}")
        for scenario, result in metrics["golden_scenarios"].items():
            print(f"{scenario}: {'PASS' if result['passed'] else 'FAIL'} ({result['claim_count']} claims)")
    return 0 if metrics["broken_link_schema_check"]["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
