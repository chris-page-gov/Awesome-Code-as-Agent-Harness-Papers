#!/usr/bin/env python3
"""Fetch canonical sources into sources/raw and update wiki metadata."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"
SOURCE_REGISTER = ROOT / "wiki/data/source-register.json"
FETCH_MANIFEST = ROOT / "sources/metadata/fetch-manifest.json"
RAW = ROOT / "sources/raw"
USER_AGENT = "code-as-agent-harness-llm-wiki/0.1 (+https://github.com/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers)"


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_json(path: Path, default):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def slug(value: str, limit: int = 80) -> str:
    value = re.sub(r"^https?://", "", value.lower())
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value[:limit].strip("-") or "source")


def arxiv_id(url: str) -> str | None:
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v[0-9]+)?", url)
    return match.group(1) if match else None


def target_for(url: str, title: str) -> tuple[str, Path]:
    arxiv = arxiv_id(url)
    if arxiv:
        return f"https://arxiv.org/pdf/{arxiv}.pdf", RAW / "arxiv" / f"{arxiv}.pdf"
    parsed = urllib.parse.urlparse(url)
    path = parsed.path.lower()
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    base = slug(title)
    if path.endswith(".pdf"):
        return url, RAW / "pdf" / f"{base}-{digest}.pdf"
    return url, RAW / "html" / f"{base}-{digest}.html"


def download(url: str, path: Path, timeout: int, max_bytes: int) -> dict:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.is_file() and path.stat().st_size > 0:
        data = path.read_bytes()
        path.chmod(path.stat().st_mode & ~0o222)
        return {
            "status": "already-local",
            "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        }

    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    hasher = hashlib.sha256()
    total = 0
    tmp = path.with_suffix(path.suffix + ".part")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        with tmp.open("wb") as fh:
            while True:
                chunk = response.read(1024 * 128)
                if not chunk:
                    break
                total += len(chunk)
                if total > max_bytes:
                    raise RuntimeError(f"download exceeded max bytes: {max_bytes}")
                hasher.update(chunk)
                fh.write(chunk)
    tmp.replace(path)
    path.chmod(path.stat().st_mode & ~0o222)
    return {"status": "localized", "bytes": total, "sha256": hasher.hexdigest()}


def load_manifest() -> dict:
    return read_json(FETCH_MANIFEST, {"generated_at": None, "attempts": []})


def append_attempt(manifest: dict, attempt: dict) -> None:
    manifest["generated_at"] = now()
    manifest.setdefault("attempts", []).append(attempt)
    write_json(FETCH_MANIFEST, manifest)


def fetch_survey(args, manifest: dict) -> bool:
    source_register = read_json(SOURCE_REGISTER, [])
    changed = False
    for entry in source_register:
        if entry.get("source_id") != "SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026":
            continue
        url = entry["canonical_url"]
        fetch_url, local_path = target_for(url, entry["title"])
        attempt = {
            "attempted_at": now(),
            "kind": "survey",
            "source_id": entry["source_id"],
            "title": entry["title"],
            "canonical_url": url,
            "fetch_url": fetch_url,
            "local_path": str(local_path.relative_to(ROOT)),
        }
        try:
            result = download(fetch_url, local_path, args.timeout, args.max_bytes)
            attempt.update(result)
            entry["local_path"] = attempt["local_path"]
            entry["status"] = "localized"
            changed = True
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            attempt["status"] = "failed"
            attempt["error"] = str(exc)
        append_attempt(manifest, attempt)
        break
    if changed:
        write_json(SOURCE_REGISTER, source_register)
    return changed


def candidate_papers(register: dict, family: str) -> list[dict]:
    candidates: list[dict] = []
    for paper in register.get("papers", []):
        if paper.get("source_status") == "localized":
            continue
        for url in paper.get("canonical_urls", []):
            if family == "arxiv" and not arxiv_id(url):
                continue
            candidates.append({"paper": paper, "url": url})
            break
    return candidates


def fetch_papers(args, manifest: dict) -> int:
    register = read_json(PAPER_REGISTER, {})
    changed = 0
    for candidate in candidate_papers(register, args.family)[: args.batch_size]:
        paper = candidate["paper"]
        url = candidate["url"]
        fetch_url, local_path = target_for(url, paper["title"])
        local_rel = str(local_path.relative_to(ROOT))
        attempt = {
            "attempted_at": now(),
            "kind": "paper",
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "canonical_url": url,
            "fetch_url": fetch_url,
            "local_path": local_rel,
        }
        try:
            result = download(fetch_url, local_path, args.timeout, args.max_bytes)
            attempt.update(result)
            paths = paper.setdefault("local_source_paths", [])
            if local_rel not in paths:
                paths.append(local_rel)
            paper["source_status"] = "localized"
            changed += 1
        except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
            attempt["status"] = "failed"
            attempt["error"] = str(exc)
        append_attempt(manifest, attempt)
        if args.sleep:
            time.sleep(args.sleep)
    if changed:
        write_json(PAPER_REGISTER, register)
        subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)
    return changed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", choices=["arxiv", "all"], default="arxiv")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--max-bytes", type=int, default=60 * 1024 * 1024)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--include-survey", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest()
    survey_changed = fetch_survey(args, manifest) if args.include_survey else False
    paper_changed = fetch_papers(args, manifest)
    print(f"Localized survey={survey_changed} papers={paper_changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
