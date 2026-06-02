#!/usr/bin/env python3
"""Run resumable source localization and wiki integration cycles."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_JSON = ROOT / "sources/metadata/wiki-ingest-status.json"
DEFAULT_FAMILIES = ["arxiv", "openreview", "acl", "pmlr", "neurips", "aaai", "direct-pdf", "html", "all"]


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+ " + " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=ROOT, check=check, text=True)


def status_state() -> dict:
    if not STATUS_JSON.is_file():
        run([sys.executable, "tools/update_wiki_status.py"])
    return json.loads(STATUS_JSON.read_text(encoding="utf-8"))


def has_worktree_changes() -> bool:
    result = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, check=True, capture_output=True, text=True)
    return bool(result.stdout.strip())


def validate() -> None:
    run(["git", "diff", "--check", "--", ".", ":(exclude)sources/raw/**"])
    run(
        [
            sys.executable,
            "-m",
            "py_compile",
            "tools/localize_sources.py",
            "tools/generate_paper_fragments.py",
            "tools/check_wiki.py",
            "tools/integrate_localized_sources.py",
            "tools/update_wiki_status.py",
            "tools/automate_wiki_ingest.py",
        ]
    )
    run([sys.executable, "tools/check_wiki.py"])


def checkpoint(args: argparse.Namespace, state: dict) -> None:
    if not args.commit or not has_worktree_changes():
        return
    run(["git", "add", "-A"])
    run(["git", "diff", "--cached", "--check", "--", ".", ":(exclude)sources/raw/**"])
    result = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if result.returncode == 0:
        return
    message = (
        "Automate source ingest checkpoint "
        f"({state['localized_fragments']} localized, "
        f"{state['integrated_fragments']} integrated, "
        f"{state['blocked_fragments']} blocked)"
    )
    run(["git", "commit", "-m", message])
    if args.push:
        run(["git", "push", "origin", args.branch])


def run_cycle(args: argparse.Namespace, cycle: int) -> dict:
    print(f"== Cycle {cycle} ==", flush=True)
    families = args.families.split(",") if args.families else DEFAULT_FAMILIES
    for family in families:
        family = family.strip()
        if not family or args.fetch_batch_size <= 0:
            continue
        run(
            [
                sys.executable,
                "tools/localize_sources.py",
                "--family",
                family,
                "--batch-size",
                str(args.fetch_batch_size),
                "--timeout",
                str(args.timeout),
                "--mark-blocked-after",
                str(args.mark_blocked_after),
            ]
        )
        if args.sleep:
            time.sleep(args.sleep)

    if args.integrate_batch_size > 0:
        run(
            [
                sys.executable,
                "tools/integrate_localized_sources.py",
                "--batch-size",
                str(args.integrate_batch_size),
                "--max-pages",
                str(args.max_pages),
                "--timeout",
                str(args.extract_timeout),
            ]
        )

    run([sys.executable, "tools/update_wiki_status.py"])
    validate()
    state = status_state()
    checkpoint(args, state)
    return state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cycles", type=int, default=1)
    parser.add_argument("--until-complete", action="store_true")
    parser.add_argument("--families", default=",".join(DEFAULT_FAMILIES))
    parser.add_argument("--fetch-batch-size", type=int, default=10)
    parser.add_argument("--integrate-batch-size", type=int, default=25)
    parser.add_argument("--timeout", type=int, default=25)
    parser.add_argument("--extract-timeout", type=int, default=30)
    parser.add_argument("--max-pages", type=int, default=3)
    parser.add_argument("--mark-blocked-after", type=int, default=3)
    parser.add_argument("--sleep", type=float, default=0.0)
    parser.add_argument("--commit", action="store_true")
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--no-progress-limit", type=int, default=3)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run([sys.executable, "tools/update_wiki_status.py"])
    previous = status_state()
    no_progress = 0
    cycle = 0
    while True:
        cycle += 1
        state = run_cycle(args, cycle)
        if state["pending_fragments"] <= 0:
            print("Ingest complete: no pending fragments remain.")
            return 0

        progress_tuple = (state["localized_fragments"], state["integrated_fragments"], state["blocked_fragments"])
        previous_tuple = (
            previous["localized_fragments"],
            previous["integrated_fragments"],
            previous["blocked_fragments"],
        )
        no_progress = no_progress + 1 if progress_tuple == previous_tuple else 0
        previous = state

        if not args.until_complete and cycle >= args.cycles:
            return 0
        if args.until_complete and no_progress >= args.no_progress_limit:
            print(f"Stopping after {no_progress} cycles without progress.")
            return 2
        if args.cycles and cycle >= args.cycles and not args.until_complete:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
