#!/usr/bin/env python3
"""Basic integrity checks for the Code as Agent Harness LLM-Wiki."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md",
    "CONTEXT.md",
    "PROGRESS.md",
    "CHANGELOG.md",
    "LLM-WIKI.md",
    "README.md",
    "wiki/AGENTS.md",
    "wiki/index.md",
    "wiki/log.md",
    "wiki/data/source-register.json",
    "wiki/data/paper-register.json",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_required_files(errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")


def check_source_register(errors: list[str]) -> None:
    register_path = ROOT / "wiki/data/source-register.json"
    if not register_path.is_file():
        return
    try:
        entries = json.loads(read(register_path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid source register JSON: {exc}")
        return
    if not isinstance(entries, list):
        errors.append("source register must be a list")
        return
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("source register contains a non-object entry")
            continue
        source_id = entry.get("source_id")
        note_path = entry.get("note_path")
        if not source_id:
            errors.append("source register entry missing source_id")
            continue
        if source_id in seen:
            errors.append(f"duplicate source_id: {source_id}")
        seen.add(source_id)
        if not note_path:
            errors.append(f"{source_id} missing note_path")
            continue
        note = ROOT / note_path
        if not note.is_file():
            errors.append(f"{source_id} note_path not found: {note_path}")
            continue
        note_text = read(note)
        if f'source_id: "{source_id}"' not in note_text and f"source_id: {source_id}" not in note_text:
            errors.append(f"{note_path} does not declare source_id {source_id}")


def check_documentation_lockstep(errors: list[str]) -> None:
    agents_text = read(ROOT / "AGENTS.md") if (ROOT / "AGENTS.md").is_file() else ""
    if "Documentation Lockstep" not in agents_text:
        errors.append("AGENTS.md must contain Documentation Lockstep rules")
    readme_text = read(ROOT / "README.md") if (ROOT / "README.md").is_file() else ""
    if "LLM-WIKI.md" not in readme_text:
        errors.append("README.md should link to LLM-WIKI.md")


def check_wiki_links(errors: list[str]) -> None:
    link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for md in sorted((ROOT / "wiki").rglob("*.md")):
        text = read(md)
        for match in link_re.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (md.parent / clean).resolve()
            if not str(resolved).startswith(str(ROOT)):
                continue
            if not resolved.exists():
                errors.append(f"broken wiki link in {md.relative_to(ROOT)}: {target}")


def check_paper_register(errors: list[str]) -> None:
    register_path = ROOT / "wiki/data/paper-register.json"
    if not register_path.is_file():
        return
    try:
        data = json.loads(read(register_path))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid paper register JSON: {exc}")
        return
    if not isinstance(data, dict):
        errors.append("paper register must be an object")
        return
    papers = data.get("papers")
    if not isinstance(papers, list):
        errors.append("paper register missing papers list")
        return
    seen: set[str] = set()
    for paper in papers:
        if not isinstance(paper, dict):
            errors.append("paper register contains a non-object entry")
            continue
        paper_id = paper.get("paper_id")
        if not paper_id:
            errors.append("paper register entry missing paper_id")
            continue
        if paper_id in seen:
            errors.append(f"duplicate paper_id: {paper_id}")
        seen.add(paper_id)
        fragment = ROOT / "wiki/papers" / f"{paper_id}.md"
        if not fragment.is_file():
            errors.append(f"paper fragment missing for {paper_id}")
            continue
        text = read(fragment)
        if f"paper_id: \"{paper_id}\"" not in text:
            errors.append(f"paper fragment does not declare paper_id: {paper_id}")


def check_readme_paper_links(errors: list[str]) -> None:
    readme = ROOT / "README.md"
    if not readme.is_file():
        return
    row_re = re.compile(r"^\|\s*\[[^\]]+\]\(([^)]+)\)")
    for lineno, line in enumerate(read(readme).splitlines(), start=1):
        match = row_re.match(line)
        if not match:
            continue
        target = match.group(1)
        if not target.startswith("wiki/papers/"):
            errors.append(f"README paper row {lineno} should link to wiki/papers/: {target}")
            continue
        if not (ROOT / target).is_file():
            errors.append(f"README paper row {lineno} links to missing fragment: {target}")


def main() -> int:
    errors: list[str] = []
    check_required_files(errors)
    check_source_register(errors)
    check_documentation_lockstep(errors)
    check_paper_register(errors)
    check_readme_paper_links(errors)
    if (ROOT / "wiki").is_dir():
        check_wiki_links(errors)
    if errors:
        print("Wiki validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Wiki validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
