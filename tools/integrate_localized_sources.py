#!/usr/bin/env python3
"""Promote localized paper sources into lightweight integrated wiki cues."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"

TERM_GROUPS = {
    "agent": ["agent", "agents", "agentic"],
    "code": ["code", "program", "programming", "software"],
    "execution": ["execute", "execution", "runtime", "interpreter"],
    "planning": ["plan", "planning", "planner"],
    "memory": ["memory", "context", "state"],
    "tools": ["tool", "tools", "api"],
    "feedback": ["feedback", "debug", "repair", "verification", "test"],
    "environment": ["environment", "world", "benchmark"],
    "multi-agent": ["multi-agent", "multi agent", "collaboration"],
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def file_metadata(path: Path) -> dict:
    data = path.read_bytes()
    return {
        "path": str(path.relative_to(ROOT)),
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def extract_pdf_text(path: Path, max_pages: int, timeout: int) -> str:
    result = subprocess.run(
        ["pdftotext", "-f", "1", "-l", str(max_pages), str(path), "-"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return result.stdout


def extract_html_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"(?is)<script.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?</style>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def extract_text(path: Path, max_pages: int, timeout: int) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf_text(path, max_pages, timeout), "pdftotext"
    if suffix in {".html", ".htm", ".txt", ".md"}:
        return extract_html_text(path), "html-text"
    return path.read_text(encoding="utf-8", errors="replace"), "plain-text"


def term_cues(text: str) -> tuple[list[dict], list[str]]:
    lowered = text.lower()
    cues: list[dict] = []
    topics: list[str] = []
    for topic, terms in TERM_GROUPS.items():
        count = 0
        for term in terms:
            if " " in term or "-" in term:
                count += lowered.count(term)
            else:
                count += len(re.findall(rf"\b{re.escape(term)}\b", lowered))
        if count:
            cues.append({"term": topic, "count": count})
            topics.append(topic)
    cues.sort(key=lambda cue: (-cue["count"], cue["term"]))
    return cues, topics


def integrate_paper(paper: dict, max_pages: int, timeout: int, max_chars: int) -> bool:
    paths = paper.get("local_source_paths") or []
    if not paths:
        return False

    texts: list[str] = []
    metadata: list[dict] = []
    methods: set[str] = set()
    for rel in paths:
        path = ROOT / rel
        if not path.is_file():
            continue
        metadata.append(file_metadata(path))
        try:
            text, method = extract_text(path, max_pages=max_pages, timeout=timeout)
        except (OSError, subprocess.SubprocessError, UnicodeError) as exc:
            text = f"extraction failed for {rel}: {exc}"
            method = "failed"
        methods.add(method)
        texts.append(text[:max_chars])

    combined = "\n".join(texts)
    if not combined.strip():
        return False

    cues, topics = term_cues(combined)
    paper["source_status"] = "integrated"
    paper["integration_status"] = "auto-extracted"
    paper["integrated_at"] = now()
    paper["source_file_metadata"] = metadata
    paper["source_signal"] = {
        "extraction": {
            "method": "+".join(sorted(methods)),
            "characters": len(combined),
            "max_pages_per_pdf": max_pages,
        },
        "term_cues": cues,
        "detected_topics": topics,
    }
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--max-pages", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--max-chars", type=int, default=30000)
    parser.add_argument("--retry-integrated", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    register = read_json(PAPER_REGISTER)
    changed = 0
    for paper in register.get("papers", []):
        status = paper.get("source_status")
        if status != "localized" and not (args.retry_integrated and status == "integrated"):
            continue
        if integrate_paper(paper, args.max_pages, args.timeout, args.max_chars):
            changed += 1
        if changed >= args.batch_size:
            break

    if changed:
        write_json(PAPER_REGISTER, register)
        subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)
    print(f"Integrated papers={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
