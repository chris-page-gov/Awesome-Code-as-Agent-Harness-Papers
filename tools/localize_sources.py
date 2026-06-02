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
LOCALIZED_STATUSES = {"localized", "integrated"}


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


def clean_identifier(value: str) -> str:
    value = urllib.parse.unquote(value)
    value = re.sub(r"[^A-Za-z0-9._-]+", "-", value).strip("-")
    return value or "source"


def parsed_host(url: str) -> str:
    return urllib.parse.urlparse(url).netloc.lower().removeprefix("www.")


def family_for_url(url: str) -> str:
    host = parsed_host(url)
    path = urllib.parse.urlparse(url).path.lower()
    if arxiv_id(url):
        return "arxiv"
    if host == "openreview.net":
        return "openreview"
    if host == "aclanthology.org":
        return "acl"
    if host == "proceedings.mlr.press":
        return "pmlr"
    if host in {"proceedings.neurips.cc", "neurips.cc"}:
        return "neurips"
    if host == "ojs.aaai.org":
        return "aaai"
    if path.endswith(".pdf"):
        return "direct-pdf"
    return "html"


def html_target(url: str, title: str) -> tuple[str, Path]:
    host = clean_identifier(parsed_host(url) or "web")
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    return url, RAW / "html" / host / f"{slug(title)}-{digest}.html"


def target_candidates(url: str, title: str) -> list[tuple[str, Path]]:
    arxiv = arxiv_id(url)
    if arxiv:
        return [(f"https://arxiv.org/pdf/{arxiv}.pdf", RAW / "arxiv" / f"{arxiv}.pdf")]

    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.lower()
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]

    if host == "openreview.net":
        query = urllib.parse.parse_qs(parsed.query)
        forum_id = clean_identifier((query.get("id") or ["openreview"])[0])
        return [
            (f"https://openreview.net/pdf?id={urllib.parse.quote(forum_id)}", RAW / "openreview" / f"{forum_id}.pdf"),
            html_target(url, title),
        ]

    if host == "aclanthology.org":
        acl_id = clean_identifier(parsed.path.strip("/"))
        if acl_id:
            return [
                (f"https://aclanthology.org/{acl_id}.pdf", RAW / "acl" / f"{acl_id}.pdf"),
                html_target(url, title),
            ]

    if host == "proceedings.mlr.press" and path.endswith(".html"):
        pdf_url = urllib.parse.urlunparse(parsed._replace(path=parsed.path[:-5] + ".pdf"))
        pdf_name = clean_identifier(Path(parsed.path).stem)
        return [(pdf_url, RAW / "pmlr" / f"{pdf_name}.pdf"), html_target(url, title)]

    if host in {"proceedings.neurips.cc", "neurips.cc"} and path.endswith(".html"):
        pdf_path = parsed.path.replace("-Abstract-", "-Paper-")[:-5] + ".pdf"
        if pdf_path != parsed.path:
            pdf_url = urllib.parse.urlunparse(parsed._replace(path=pdf_path))
            pdf_name = clean_identifier(Path(pdf_path).name)
            return [(pdf_url, RAW / "neurips" / pdf_name), html_target(url, title)]

    if path.endswith(".pdf"):
        return [(url, RAW / "pdf" / f"{slug(title)}-{digest}.pdf")]

    return [html_target(url, title)]


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
        fetch_url, local_path = target_candidates(url, entry["title"])[0]
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


def family_matches(url: str, requested: str) -> bool:
    if requested == "all":
        return True
    return family_for_url(url) == requested


def failure_counts(manifest: dict) -> dict[tuple[str, str], int]:
    counts: dict[tuple[str, str], int] = {}
    for attempt in manifest.get("attempts", []):
        if attempt.get("kind") != "paper" or attempt.get("status") not in {"failed", "blocked"}:
            continue
        paper_id = attempt.get("paper_id")
        canonical_url = attempt.get("canonical_url")
        if not paper_id or not canonical_url:
            continue
        key = (paper_id, canonical_url)
        counts[key] = counts.get(key, 0) + 1
    return counts


def candidate_papers(register: dict, family: str, retry_blocked: bool = False) -> list[dict]:
    candidates: list[dict] = []
    for paper in register.get("papers", []):
        if paper.get("source_status") in LOCALIZED_STATUSES:
            continue
        if paper.get("source_status") == "blocked" and not retry_blocked:
            continue
        for url in paper.get("canonical_urls", []):
            if not family_matches(url, family):
                continue
            candidates.append({"paper": paper, "url": url})
            break
    return candidates


def fetch_papers(args, manifest: dict) -> int:
    register = read_json(PAPER_REGISTER, {})
    failures = failure_counts(manifest)
    localized = 0
    blocked = 0
    processed = 0
    changed_register = False
    for candidate in candidate_papers(register, args.family, args.retry_blocked):
        if processed >= args.batch_size:
            break
        paper = candidate["paper"]
        url = candidate["url"]
        key = (paper["paper_id"], url)
        if not args.retry_blocked and failures.get(key, 0) >= args.mark_blocked_after:
            paper["source_status"] = "blocked"
            paper["blocked_url"] = url
            paper["blocked_reason"] = f"failed localization attempts reached {args.mark_blocked_after}"
            changed_register = True
            blocked += 1
            processed += 1
            append_attempt(
                manifest,
                {
                    "attempted_at": now(),
                    "kind": "paper",
                    "paper_id": paper["paper_id"],
                    "title": paper["title"],
                    "canonical_url": url,
                    "status": "blocked",
                    "error": paper["blocked_reason"],
                },
            )
            continue

        processed += 1
        last_error = ""
        paper_failed_targets = 0
        for fetch_url, local_path in target_candidates(url, paper["title"]):
            local_rel = str(local_path.relative_to(ROOT))
            attempt = {
                "attempted_at": now(),
                "kind": "paper",
                "paper_id": paper["paper_id"],
                "title": paper["title"],
                "canonical_url": url,
                "fetch_url": fetch_url,
                "local_path": local_rel,
                "source_family": family_for_url(url),
            }
            try:
                result = download(fetch_url, local_path, args.timeout, args.max_bytes)
                attempt.update(result)
                paths = paper.setdefault("local_source_paths", [])
                if local_rel not in paths:
                    paths.append(local_rel)
                paper["source_status"] = "localized"
                paper["source_family"] = family_for_url(url)
                paper.pop("blocked_url", None)
                paper.pop("blocked_reason", None)
                localized += 1
                changed_register = True
                append_attempt(manifest, attempt)
                break
            except (urllib.error.URLError, TimeoutError, RuntimeError, OSError) as exc:
                paper_failed_targets += 1
                last_error = str(exc)
                attempt["status"] = "failed"
                attempt["error"] = last_error
                append_attempt(manifest, attempt)
        else:
            failures[key] = failures.get(key, 0) + paper_failed_targets
            if args.mark_blocked_after and failures[key] >= args.mark_blocked_after:
                paper["source_status"] = "blocked"
                paper["blocked_url"] = url
                paper["blocked_reason"] = last_error or f"failed localization attempts reached {args.mark_blocked_after}"
                changed_register = True
                blocked += 1
        if args.sleep:
            time.sleep(args.sleep)
    if changed_register:
        write_json(PAPER_REGISTER, register)
        subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)
    print(f"Processed papers={processed} localized={localized} blocked={blocked}")
    return localized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--family",
        choices=["arxiv", "openreview", "acl", "pmlr", "neurips", "aaai", "direct-pdf", "html", "all"],
        default="arxiv",
    )
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--max-bytes", type=int, default=60 * 1024 * 1024)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--include-survey", action="store_true")
    parser.add_argument("--mark-blocked-after", type=int, default=3)
    parser.add_argument("--retry-blocked", action="store_true")
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
