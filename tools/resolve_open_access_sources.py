#!/usr/bin/env python3
"""Resolve blocked source records through exact-title OpenAlex OA matches."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import localize_sources


ROOT = Path(__file__).resolve().parents[1]
PAPER_REGISTER = ROOT / "wiki/data/paper-register.json"
SOURCE_OVERRIDES = ROOT / "sources/metadata/source-overrides.json"
RAW = ROOT / "sources/raw"
OPENALEX = "https://api.openalex.org/works"
SKIP_SUFFIXES = {".gif", ".jpg", ".jpeg", ".png", ".svg", ".webp"}


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def slug(value: str, limit: int = 80) -> str:
    value = re.sub(r"^https?://", "", value.lower())
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return (value[:limit].strip("-") or "source")


def read_json(path: Path, default):
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def openalex_query(title: str, max_results: int, timeout: int) -> dict:
    params = urllib.parse.urlencode({"search": title, "per-page": max_results})
    request = urllib.request.Request(
        f"{OPENALEX}?{params}",
        headers={"User-Agent": localize_sources.USER_AGENT},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def collect_urls(work: dict) -> list[str]:
    urls: list[str] = []

    def add(value: str | None) -> None:
        if value and value not in urls:
            urls.append(value)

    primary = work.get("primary_location") or {}
    open_access = work.get("open_access") or {}
    add(primary.get("pdf_url"))
    add(open_access.get("oa_url"))
    add(primary.get("landing_page_url"))
    for location in work.get("locations") or []:
        add((location or {}).get("pdf_url"))
        add((location or {}).get("landing_page_url"))
    return urls


def load_overrides(path: Path) -> dict[str, list[str]]:
    data = read_json(path, {"overrides": []})
    overrides: dict[str, list[str]] = {}
    for entry in data.get("overrides", []):
        paper_id = entry.get("paper_id")
        urls = [url for url in entry.get("urls", []) if isinstance(url, str)]
        if paper_id and urls:
            overrides[paper_id] = urls
    return overrides


def url_score(url: str) -> tuple[int, str]:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.lower()
    if host == "arxiv.org" and path.startswith("/pdf/"):
        return (0, url)
    if host == "aclanthology.org" and path.endswith(".pdf"):
        return (1, url)
    if host == "preprints.org" and "download" in path:
        return (2, url)
    if path.endswith(".pdf"):
        return (3, url)
    return (8, url)


def usable_url(url: str, blocked_url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    suffix = Path(parsed.path).suffix.lower()
    if suffix in SKIP_SUFFIXES:
        return False
    if host == "doi.org":
        return False
    if url == blocked_url:
        return False
    return parsed.scheme in {"http", "https"} and bool(host)


def target_for_url(url: str, title: str) -> Path:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.lower()
    if localize_sources.arxiv_id(url):
        return localize_sources.target_candidates(url, title)[0][1]
    if host == "aclanthology.org" and path.endswith(".pdf"):
        return RAW / "acl" / localize_sources.clean_identifier(Path(parsed.path).name)
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()[:8]
    if path.endswith(".pdf") or (host == "preprints.org" and "download" in path):
        return RAW / "pdf" / f"{slug(title)}-{digest}.pdf"
    return localize_sources.html_target(url, title)[1]


def verify_download(path: Path) -> None:
    if path.suffix.lower() == ".pdf" and not path.read_bytes().startswith(b"%PDF"):
        try:
            path.chmod(path.stat().st_mode | 0o200)
            path.unlink()
        finally:
            raise RuntimeError("downloaded file did not look like a PDF")


def resolve_paper(paper: dict, args: argparse.Namespace, manifest: dict) -> bool:
    source_by_url: dict[str, str] = {}
    candidates: list[str] = []
    for url in args.overrides.get(paper["paper_id"], []):
        if usable_url(url, paper.get("blocked_url", "")) and url not in candidates:
            candidates.append(url)
            source_by_url[url] = "manual-override"

    data = {"results": []}
    if not candidates:
        try:
            data = openalex_query(paper["title"], args.max_results, args.timeout)
        except (OSError, TimeoutError, json.JSONDecodeError) as exc:
            localize_sources.append_attempt(
                manifest,
                {
                    "attempted_at": localize_sources.now(),
                    "kind": "paper",
                    "paper_id": paper["paper_id"],
                    "title": paper["title"],
                    "canonical_url": paper.get("blocked_url", ""),
                    "status": "failed",
                    "resolution_source": "openalex-exact-title",
                    "error": f"OpenAlex lookup failed: {exc}",
                },
            )
            return False

    title_norm = normalize_title(paper["title"])
    for work in data.get("results", []):
        if normalize_title(work.get("display_name") or "") != title_norm:
            continue
        for url in collect_urls(work):
            if usable_url(url, paper.get("blocked_url", "")) and url not in candidates:
                candidates.append(url)
                source_by_url[url] = "openalex-exact-title"

    candidates.sort(key=lambda url: (0 if source_by_url.get(url) == "manual-override" else 1, *url_score(url)))
    for url in candidates:
        local_path = target_for_url(url, paper["title"])
        local_rel = str(local_path.relative_to(ROOT))
        attempt = {
            "attempted_at": localize_sources.now(),
            "kind": "paper",
            "paper_id": paper["paper_id"],
            "title": paper["title"],
            "canonical_url": paper.get("blocked_url", ""),
            "fetch_url": url,
            "local_path": local_rel,
            "source_family": localize_sources.family_for_url(url),
            "resolution_source": source_by_url.get(url, "openalex-exact-title"),
        }
        try:
            if args.dry_run:
                attempt["status"] = "dry-run"
                localize_sources.append_attempt(manifest, attempt)
                print(f"DRY {paper['paper_id']} <- {url}")
                return False
            result = localize_sources.download(url, local_path, args.timeout, args.max_bytes)
            verify_download(local_path)
            attempt.update(result)
            paths = paper.setdefault("local_source_paths", [])
            if local_rel not in paths:
                paths.append(local_rel)
            urls = paper.setdefault("canonical_urls", [])
            if url not in urls:
                urls.append(url)
            paper["source_status"] = "localized"
            paper["source_family"] = localize_sources.family_for_url(url)
            paper.pop("blocked_url", None)
            paper.pop("blocked_reason", None)
            localize_sources.append_attempt(manifest, attempt)
            print(f"localized {paper['paper_id']} <- {url}")
            return True
        except (OSError, TimeoutError, RuntimeError) as exc:
            attempt["status"] = "failed"
            attempt["error"] = str(exc)
            localize_sources.append_attempt(manifest, attempt)
            print(f"failed {paper['paper_id']} <- {url}: {exc}")
    return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch-size", type=int, default=25)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--max-bytes", type=int, default=60 * 1024 * 1024)
    parser.add_argument("--sleep", type=float, default=0.1)
    parser.add_argument("--overrides", default=str(SOURCE_OVERRIDES))
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.overrides = load_overrides(Path(args.overrides))
    socket.setdefaulttimeout(args.timeout)
    register = read_json(PAPER_REGISTER, {})
    manifest = localize_sources.load_manifest()
    changed = 0
    processed = 0
    for paper in register.get("papers", []):
        if paper.get("source_status") != "blocked":
            continue
        if processed >= args.batch_size:
            break
        processed += 1
        if resolve_paper(paper, args, manifest):
            changed += 1
        if args.sleep:
            time.sleep(args.sleep)

    if changed:
        write_json(PAPER_REGISTER, register)
        subprocess.run([sys.executable, "tools/generate_paper_fragments.py"], cwd=ROOT, check=True)
    print(f"Processed blocked={processed} localized={changed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
