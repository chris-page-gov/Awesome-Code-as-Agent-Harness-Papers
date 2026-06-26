#!/usr/bin/env python3
"""Normalize wiki Markdown frontmatter to the local OKF/OKFR profile."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

from okf_lib import ROOT, normalized_text_for, repo_rel, wiki_markdown_files


def selected_paths(raw_paths: list[str]) -> list[Path]:
    if not raw_paths:
        return wiki_markdown_files()
    paths: list[Path] = []
    for raw in raw_paths:
        path = Path(raw)
        if not path.is_absolute():
            path = ROOT / path
        if path.is_dir():
            paths.extend(sorted(path.rglob("*.md")))
        elif path.is_file():
            paths.append(path)
        else:
            raise FileNotFoundError(raw)
    return sorted({path.resolve() for path in paths if path.suffix == ".md"})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional files or directories to normalize.")
    parser.add_argument("--check", action="store_true", help="Fail if files would change.")
    args = parser.parse_args()

    changed: list[Path] = []
    for path in selected_paths(args.paths):
        before = path.read_text(encoding="utf-8")
        after = normalized_text_for(path)
        if before == after:
            continue
        changed.append(path)
        if args.check:
            diff = "\n".join(
                difflib.unified_diff(
                    before.splitlines(),
                    after.splitlines(),
                    fromfile=f"{repo_rel(path)} (current)",
                    tofile=f"{repo_rel(path)} (normalized)",
                    lineterm="",
                    n=3,
                )
            )
            print(diff)
        else:
            path.write_text(after, encoding="utf-8")

    if changed and args.check:
        print(f"OKF frontmatter normalization needed for {len(changed)} files.")
        return 1
    if changed:
        print(f"Normalized OKF frontmatter for {len(changed)} files.")
    else:
        print("OKF frontmatter already normalized.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
