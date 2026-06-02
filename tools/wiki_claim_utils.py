#!/usr/bin/env python3
"""Shared helpers for LLM-Wiki claim cards and evaluation tooling."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import zipfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"
SOURCE_REGISTER = ROOT / "wiki/data/source-register.json"
CLAIM_REGISTER = ROOT / "wiki/data/claim-register.json"
CLAIMS_DIR = ROOT / "wiki/claims"
REPORTS_DIR = ROOT / "wiki/reports"
EVIDENCE_PACKETS_DIR = REPORTS_DIR / "evidence-packets"

QUALITY_TIERS = {
    "metadata-only",
    "localized",
    "auto-extracted",
    "agent-drafted",
    "agent-reviewed",
    "cross-agent-reviewed",
    "human-reviewed",
    "decision-grade",
}

REVIEW_STATUSES = {
    "metadata-only",
    "localized",
    "auto-extracted",
    "agent-drafted",
    "agent-reviewed",
    "cross-agent-reviewed",
    "human-reviewed",
    "decision-grade",
}

CLAIM_TYPES = {
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

TOPIC_RULES: dict[str, dict] = {
    "mcp-protocol": {
        "label": "MCP protocol",
        "terms": ["model context protocol", "mcp", "protocol", "client", "server", "resource", "prompt"],
        "claim_type": "protocol-capability",
        "related_topics": ["mcp-governance", "harness-interface", "procurement-and-conformance"],
    },
    "tool-discovery": {
        "label": "tool discovery",
        "terms": ["discovery", "discover", "tools", "tool", "schema", "capabilities"],
        "claim_type": "protocol-capability",
        "related_topics": ["mcp-governance", "harness-mechanisms"],
    },
    "authorization": {
        "label": "authorization and identity",
        "terms": ["authorization", "authentication", "oauth", "oidc", "access control", "token", "identity", "permission"],
        "claim_type": "governance-control",
        "related_topics": ["mcp-governance", "procurement-and-conformance"],
    },
    "registry": {
        "label": "registry and curation",
        "terms": ["registry", "catalog", "marketplace", "repository", "curation", "curate", "discovery"],
        "claim_type": "procurement-conformance",
        "related_topics": ["mcp-governance", "procurement-and-conformance"],
    },
    "gateway": {
        "label": "gateway and routing",
        "terms": ["gateway", "proxy", "routing", "remote server", "transport", "http", "sse", "header"],
        "claim_type": "governance-control",
        "related_topics": ["mcp-governance", "procurement-and-conformance"],
    },
    "threat": {
        "label": "threat and attack surface",
        "terms": ["threat", "attack", "vulnerability", "malicious", "spoof", "poison", "unauthorized", "security"],
        "claim_type": "threat-taxonomy",
        "related_topics": ["mcp-governance", "agent-safety-and-sandboxing"],
    },
    "safeguards": {
        "label": "security safeguards",
        "terms": ["safeguard", "mitigate", "mitigation", "defense", "security", "policy", "control"],
        "claim_type": "safety-control",
        "related_topics": ["mcp-governance", "agent-safety-and-sandboxing"],
    },
    "trust-boundary": {
        "label": "trust boundary",
        "terms": ["trust boundary", "boundary", "interoperability", "standardization", "governance", "ecosystem"],
        "claim_type": "governance-control",
        "related_topics": ["mcp-governance", "procurement-and-conformance"],
    },
    "sandboxing": {
        "label": "sandboxing and isolation",
        "terms": ["sandbox", "sandboxing", "isolation", "container", "vm", "virtual machine", "environment"],
        "claim_type": "safety-control",
        "related_topics": ["agent-safety-and-sandboxing", "harness-mechanisms"],
    },
    "rollback": {
        "label": "rollback and state recovery",
        "terms": ["rollback", "rolling back", "snapshot", "transaction", "fault recovery", "restore", "consistent state"],
        "claim_type": "safety-control",
        "related_topics": ["agent-safety-and-sandboxing", "evidence-observability-and-redress"],
    },
    "capability-governance": {
        "label": "capability governance",
        "terms": ["capability", "least privilege", "over-provision", "overprovision", "tool reduction", "governance", "scope"],
        "claim_type": "governance-control",
        "related_topics": ["agent-safety-and-sandboxing", "procurement-and-conformance"],
    },
    "safe-execution": {
        "label": "safe execution",
        "terms": ["safe execution", "unsafe execution", "dangerous command", "interception", "execute", "runtime", "policy-based"],
        "claim_type": "safety-control",
        "related_topics": ["agent-safety-and-sandboxing", "harness-mechanisms"],
    },
    "approval": {
        "label": "approval and human oversight",
        "terms": ["approval", "human", "human-in-the-loop", "oversight", "confirm", "review", "accountability"],
        "claim_type": "governance-control",
        "related_topics": ["evidence-observability-and-redress", "procurement-and-conformance"],
    },
    "traceability": {
        "label": "traceability and audit",
        "terms": ["trace", "traceability", "audit", "auditable", "provenance", "log", "attribution"],
        "claim_type": "evidence-practice",
        "related_topics": ["evidence-observability-and-redress", "procurement-and-conformance"],
    },
    "redress": {
        "label": "redress and accountability",
        "terms": ["redress", "accountability", "incident", "appeal", "remedy", "explainable"],
        "claim_type": "evidence-practice",
        "related_topics": ["evidence-observability-and-redress", "procurement-and-conformance"],
    },
    "evaluation": {
        "label": "evaluation and benchmark evidence",
        "terms": ["evaluation", "benchmark", "experiment", "metric", "accuracy", "success rate", "pass@1", "dataset"],
        "claim_type": "evaluation-result",
        "related_topics": ["evidence-observability-and-redress", "scaling-the-harness"],
    },
    "evidence-store": {
        "label": "evidence store and observability",
        "terms": ["evidence", "observability", "telemetry", "logs", "audit log", "trace", "inspectable"],
        "claim_type": "evidence-practice",
        "related_topics": ["evidence-observability-and-redress", "scaling-the-harness"],
    },
    "memory": {
        "label": "memory and state",
        "terms": ["memory", "state", "context", "experience", "experience card", "long-term"],
        "claim_type": "contribution",
        "related_topics": ["harness-mechanisms", "evidence-observability-and-redress"],
    },
    "multi-agent": {
        "label": "multi-agent coordination",
        "terms": ["multi-agent", "multi agent", "agent to agent", "a2a", "collaboration", "coordination"],
        "claim_type": "protocol-capability",
        "related_topics": ["scaling-the-harness", "mcp-governance"],
    },
    "tools": {
        "label": "tool use",
        "terms": ["tool", "tools", "api", "function calling", "external service"],
        "claim_type": "contribution",
        "related_topics": ["harness-mechanisms", "harness-interface"],
    },
    "planning": {
        "label": "planning and workflow",
        "terms": ["plan", "planning", "workflow", "reasoning", "decompose", "step"],
        "claim_type": "contribution",
        "related_topics": ["harness-interface", "harness-mechanisms"],
    },
    "code-execution": {
        "label": "code execution",
        "terms": ["code", "software", "program", "execution", "shell", "terminal", "debug"],
        "claim_type": "contribution",
        "related_topics": ["harness-interface", "harness-mechanisms"],
    },
    "procurement": {
        "label": "procurement and conformance",
        "terms": ["procurement", "conformance", "version", "profile", "standard", "criteria", "compliance"],
        "claim_type": "procurement-conformance",
        "related_topics": ["procurement-and-conformance", "mcp-governance"],
    },
}

HIGH_VALUE_TOPIC_OVERRIDES = {
    "model-context-protocol-mcp-landscape-security-threats-and-future-researc-a33b66a1": [
        "mcp-protocol",
        "tool-discovery",
        "authorization",
        "registry",
        "gateway",
        "threat",
        "safeguards",
        "trust-boundary",
        "evaluation",
        "procurement",
    ],
    "model-context-protocol-5929925a": [
        "mcp-protocol",
        "tool-discovery",
        "authorization",
        "gateway",
        "registry",
        "procurement",
        "trust-boundary",
        "tools",
    ],
    "a-survey-on-model-context-protocol-architecture-state-of-the-art-challen-51ec4866": [
        "mcp-protocol",
        "tool-discovery",
        "threat",
        "trust-boundary",
        "procurement",
    ],
    "from-glue-code-to-protocols-a-critical-analysis-of-a2a-and-mcp-integrati-6c83ea89": [
        "mcp-protocol",
        "multi-agent",
        "tool-discovery",
        "threat",
        "registry",
        "procurement",
        "trust-boundary",
    ],
    "introducing-the-agent-governance-toolkit-open-source-runtime-security-fo-24b2c1ff": [
        "capability-governance",
        "authorization",
        "safe-execution",
        "traceability",
        "procurement",
        "safeguards",
    ],
    "beyond-static-sandboxing-learned-capability-governance-for-autonomous-ai-a8b8b443": [
        "capability-governance",
        "sandboxing",
        "safe-execution",
        "safeguards",
        "evaluation",
        "threat",
        "tools",
    ],
    "fault-tolerant-sandboxing-for-ai-coding-agents-a-transactional-approach-260e82ac": [
        "sandboxing",
        "rollback",
        "safe-execution",
        "evaluation",
        "code-execution",
        "safeguards",
    ],
    "openagentsafety-a-comprehensive-framework-for-evaluating-real-world-ai-a-d60c0cfd": [
        "safe-execution",
        "evaluation",
        "threat",
        "sandboxing",
        "tools",
        "approval",
    ],
    "agentic-harness-engineering-observability-driven-automatic-evolution-of-32a741f4": [
        "evidence-store",
        "traceability",
        "evaluation",
        "tools",
        "memory",
        "rollback",
    ],
    "normcode-a-semi-formal-language-for-auditable-ai-planning-96b226f7": [
        "traceability",
        "planning",
        "evidence-store",
        "approval",
        "procurement",
        "evaluation",
    ],
    "memgovern-enhancing-code-agents-through-learning-from-governed-human-exp-acb2227b": [
        "approval",
        "memory",
        "traceability",
        "evaluation",
        "evidence-store",
        "code-execution",
    ],
}

SOURCE_TOPIC_OVERRIDES = {
    "SOURCE-UNOFFICIAL-DRAFT-AGENTIC-AI-GOVERNANCE-UK-MCP-2026": [
        "mcp-protocol",
        "authorization",
        "gateway",
        "registry",
        "approval",
        "traceability",
        "procurement",
        "evidence-store",
        "redress",
    ],
    "SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026": [
        "code-execution",
        "tools",
        "planning",
        "memory",
        "evaluation",
        "multi-agent",
    ],
}

GENERIC_TOPIC_FALLBACK = [
    "code-execution",
    "tools",
    "planning",
    "memory",
    "evaluation",
    "multi-agent",
    "safe-execution",
]

GOLDEN_SCENARIOS = {
    "mcp-governance": ["mcp-protocol", "authorization", "registry", "gateway", "threat"],
    "agent-safety-and-sandboxing": ["rollback", "sandboxing", "capability-governance", "safe-execution"],
    "evidence-observability-and-redress": ["approval", "traceability", "redress", "evaluation", "evidence-store"],
}

VOLATILE_TERMS = {
    "government",
    "legal",
    "law",
    "procurement",
    "protocol",
    "specification",
    "release candidate",
    "mcp",
    "oauth",
    "oidc",
}

VOLATILE_DOMAINS = {
    "gov.uk",
    "legislation.gov.uk",
    "modelcontextprotocol.io",
    "docs.anthropic.com",
    "anthropic.com",
    "openai.com",
    "microsoft.com",
    "github.blog",
}

STALE_PHRASES = [
    "source localization needed",
    "source localisation needed",
    "per-paper fragments need generation and source localization",
    "content notes are automated extraction cues and still need human review",
    "replace automated extraction cues with human-reviewed contribution notes",
    "need human review where the fragment only contains automated extraction cues",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path, default):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def slugify(text: str, max_len: int = 80) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    text = re.sub(r"-+", "-", text)
    return text[:max_len].strip("-") or "item"


def clean_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[\u200b-\u200f\ufeff]", "", text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(path: Path, max_pages: int, timeout: int) -> tuple[str, str]:
    result = subprocess.run(
        ["pdftotext", "-f", "1", "-l", str(max_pages), str(path), "-"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout, "pdftotext"


def extract_html_text(path: Path) -> tuple[str, str]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    head_bits: list[str] = []
    title_match = re.search(r"(?is)<title[^>]*>(.*?)</title>", raw)
    if title_match:
        head_bits.append(html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip())
    for match in re.finditer(r"(?is)<meta\s+[^>]*(?:name|property)=[\"'](?:description|og:description|og:title|twitter:title)[\"'][^>]*>", raw):
        tag = match.group(0)
        content = re.search(r"(?is)\bcontent=[\"'](.*?)[\"']", tag)
        if content:
            head_bits.append(html.unescape(content.group(1)).strip())
    raw = re.sub(r"(?is)<script.*?</script>", " ", raw)
    raw = re.sub(r"(?is)<style.*?</style>", " ", raw)
    raw = re.sub(r"(?is)<nav.*?</nav>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    body = html.unescape(raw)
    return "\n".join(head_bits + [body]), "html-text"


def extract_docx_text(path: Path) -> tuple[str, str]:
    paragraphs: list[str] = []
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as archive:
        names = [
            name
            for name in archive.namelist()
            if name.startswith("word/") and name.endswith(".xml") and any(part in name for part in ["document", "header", "footer", "footnotes", "endnotes"])
        ]
        for name in names:
            root = ElementTree.fromstring(archive.read(name))
            for para in root.findall(".//w:p", ns):
                texts = [node.text or "" for node in para.findall(".//w:t", ns)]
                if texts:
                    paragraphs.append("".join(texts))
    return "\n".join(paragraphs), "docx-xml"


def extract_text(path: Path, max_pages: int = 6, timeout: int = 30, max_chars: int = 60000) -> tuple[str, str]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            text, method = extract_pdf_text(path, max_pages=max_pages, timeout=timeout)
        elif suffix in {".html", ".htm"}:
            text, method = extract_html_text(path)
        elif suffix == ".docx":
            text, method = extract_docx_text(path)
        else:
            text, method = path.read_text(encoding="utf-8", errors="replace"), "plain-text"
    except (OSError, subprocess.SubprocessError, UnicodeError, zipfile.BadZipFile, ElementTree.ParseError) as exc:
        return f"extraction failed for {path}: {exc}", "failed"
    return clean_text(text)[:max_chars], method


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    sentences: list[str] = []
    for part in parts:
        sentence = clean_text(part)
        if 35 <= len(sentence) <= 650 and len(sentence.split()) >= 6:
            sentences.append(sentence)
    return sentences


def term_hits(text: str, terms: list[str]) -> list[str]:
    lowered = text.lower()
    hits: list[str] = []
    for term in terms:
        if re.search(rf"\b{re.escape(term.lower())}\b", lowered):
            hits.append(term)
    return hits


def detect_topics(title: str, text: str, existing_topics: list[str] | None = None) -> list[str]:
    haystack = f"{title}\n{text[:25000]}".lower()
    scored: list[tuple[int, str]] = []
    for topic, spec in TOPIC_RULES.items():
        score = 0
        for term in spec["terms"]:
            if term.lower() in haystack:
                score += 2 if term.lower() in title.lower() else 1
        if score:
            scored.append((score, topic))
    if existing_topics:
        for topic in existing_topics:
            mapped = {
                "agent": "tools",
                "code": "code-execution",
                "execution": "code-execution",
                "planning": "planning",
                "memory": "memory",
                "tools": "tools",
                "feedback": "evaluation",
                "environment": "sandboxing",
                "multi-agent": "multi-agent",
            }.get(topic, topic)
            if mapped in TOPIC_RULES:
                scored.append((1, mapped))
    ordered = [topic for _, topic in sorted(scored, key=lambda item: (-item[0], item[1]))]
    return dedupe(ordered + GENERIC_TOPIC_FALLBACK)


def best_sentence(sentences: list[str], topic: str, title: str = "") -> tuple[str, list[str]]:
    spec = TOPIC_RULES[topic]
    best = ""
    best_hits: list[str] = []
    best_score = -1
    for sentence in sentences:
        hits = term_hits(sentence, spec["terms"])
        if not hits:
            continue
        score = len(hits) * 4
        lower = sentence.lower()
        for boost in ["we introduce", "we present", "this paper", "we propose", "evaluation", "results", "threat", "framework"]:
            if boost in lower:
                score += 1
        if title and any(part.lower() in lower for part in title.split()[:3] if len(part) > 4):
            score += 1
        if score > best_score:
            best = sentence
            best_hits = hits
            best_score = score
    return best, best_hits


def concise_evidence_summary(sentence: str, topic: str, hits: list[str]) -> str:
    label = TOPIC_RULES[topic]["label"]
    if sentence:
        cue = ", ".join(hits[:5]) if hits else label
        return f"Source sentence contains {label} evidence with matched cue(s): {cue}."
    return f"Source metadata or extracted text did not expose enough local detail for a full {label} claim."


def claim_statement(title: str, topic: str, sentence: str, is_gap: bool = False) -> str:
    label = TOPIC_RULES.get(topic, {}).get("label", topic.replace("-", " "))
    if is_gap:
        return f"The localized source for {title} is too thin for decision-grade synthesis on {label} without returning to the original or an alternate source."
    return f"{title} provides localized evidence about {label} for the Code as Agent Harness wiki."


def make_claim_id(seed: str) -> str:
    return "CLAIM-" + hashlib.sha1(seed.encode("utf-8")).hexdigest()[:12].upper()


def claim_card_path(claim_id: str) -> str:
    return f"wiki/claims/{claim_id.lower()}.md"


def dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def is_volatile(text: str, refs: list[str], topics: list[str]) -> bool:
    lowered = " ".join([text, " ".join(refs), " ".join(topics)]).lower()
    if any(term in lowered for term in VOLATILE_TERMS):
        return True
    return any(domain in lowered for domain in VOLATILE_DOMAINS)


def source_ids_for_refs(refs: list[str], source_register: list[dict]) -> list[str]:
    found: list[str] = []
    for source in source_register:
        local = source.get("local_path")
        note = source.get("note_path")
        canonical = source.get("canonical_url")
        for ref in refs:
            if ref and ref in {local, note, canonical}:
                found.append(source.get("source_id", ""))
    return dedupe([item for item in found if item])


def paper_fragment_path(paper_id: str) -> str:
    return f"wiki/papers/{paper_id}.md"


def load_claim_register() -> dict:
    return read_json(CLAIM_REGISTER, {"claims": [], "claim_count": 0})


def claim_counts_by(field: str, claims: list[dict]) -> Counter:
    counter: Counter = Counter()
    for claim in claims:
        value = claim.get(field)
        if isinstance(value, list):
            for item in value:
                counter[item] += 1
        else:
            counter[value or "unknown"] += 1
    return counter
