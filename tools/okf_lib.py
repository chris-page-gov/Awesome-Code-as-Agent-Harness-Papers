"""Shared OKF/OKFR helpers for the Code as Agent Harness wiki."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WIKI_ROOT = ROOT / "wiki"
DEFAULT_TIMESTAMP = "2026-06-26T00:00:00Z"
OKF_VERSION = "0.1"
OKF_REQUIRED_FIELDS = ("type", "title", "description", "timestamp")
OKF_OPTIONAL_FIELDS = (
    "resource",
    "tags",
    "aliases",
    "okf_version",
    "okfr_role",
    "okfr_summary",
    "okfr_order",
    "okfr_date",
)
FRONTMATTER_ORDER = (
    "type",
    "title",
    "description",
    "timestamp",
    "resource",
    "tags",
    "aliases",
    "okf_version",
    "okfr_role",
    "okfr_summary",
    "okfr_order",
    "okfr_date",
    "note_type",
    "status",
    "updated",
    "last_reviewed",
)
ROOT_PAGES = (
    "wiki/index.md",
    "wiki/log.md",
    "wiki/claims/README.md",
    "wiki/guidance/okf-profile.md",
)
LOCAL_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")


@dataclass(frozen=True)
class WikiPage:
    path: Path
    rel_path: str
    frontmatter: dict[str, Any]
    body: str


@dataclass(frozen=True)
class LinkRecord:
    source: str
    target: str
    raw_target: str
    text: str
    exists: bool
    is_wiki_page: bool


def repo_rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def wiki_markdown_files() -> list[Path]:
    if not WIKI_ROOT.is_dir():
        return []
    return sorted(path for path in WIKI_ROOT.rglob("*.md") if path.is_file())


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"[]", "{}"}:
        return json.loads(value)
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if value.lower() == "null":
        return None
    if value.startswith('"') and value.endswith('"'):
        try:
            return clean_frontmatter_text(json.loads(value))
        except json.JSONDecodeError:
            return clean_frontmatter_text(value[1:-1])
    if value.startswith("'") and value.endswith("'"):
        return clean_frontmatter_text(value[1:-1])
    if value.startswith("[") and value.endswith("]"):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return [part.strip().strip('"').strip("'") for part in value[1:-1].split(",") if part.strip()]
    if re.fullmatch(r"-?\d+", value):
        try:
            return int(value)
        except ValueError:
            return value
    if re.fullmatch(r"-?\d+\.\d+", value):
        try:
            return float(value)
        except ValueError:
            return value
    return value


def clean_frontmatter_text(value: str) -> str:
    previous = None
    cleaned = value
    while cleaned != previous:
        previous = cleaned
        cleaned = cleaned.replace(r"\"", '"')
        cleaned = cleaned.replace(r"\$", "$")
        cleaned = cleaned.replace(r"\\", "\\")
    return cleaned


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str, bool]:
    if not text.startswith("---\n"):
        return {}, text, False
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, False
    raw = text[4:end].strip("\n")
    body = text[end + 4 :]
    body = body.lstrip("\n")

    frontmatter: dict[str, Any] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line or line.startswith((" ", "\t")):
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value:
            frontmatter[key] = parse_scalar(value)
            i += 1
            continue
        block_values: list[Any] = []
        i += 1
        while i < len(lines):
            item = lines[i]
            if not item.startswith((" ", "\t")):
                break
            stripped = item.strip()
            if stripped.startswith("- "):
                block_values.append(parse_scalar(stripped[2:]))
            i += 1
        frontmatter[key] = block_values
    return frontmatter, body, True


def render_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return json.dumps(value, ensure_ascii=False)
    return json.dumps(str(value), ensure_ascii=False)


def dump_frontmatter(frontmatter: dict[str, Any]) -> str:
    ordered: list[str] = []
    seen: set[str] = set()
    for key in FRONTMATTER_ORDER:
        if key in frontmatter:
            ordered.append(key)
            seen.add(key)
    for key in frontmatter:
        if key not in seen:
            ordered.append(key)

    lines = ["---"]
    for key in ordered:
        value = frontmatter[key]
        if isinstance(value, list) and len(value) > 5:
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {render_scalar(item)}")
        else:
            lines.append(f"{key}: {render_scalar(value)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def load_page(path: Path) -> WikiPage:
    text = path.read_text(encoding="utf-8")
    frontmatter, body, _ = parse_frontmatter(text)
    return WikiPage(path=path, rel_path=repo_rel(path), frontmatter=frontmatter, body=body)


def first_heading(body: str) -> str:
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def clean_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def first_paragraph(body: str) -> str:
    parts: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if parts:
                break
            continue
        if stripped.startswith(("#", "|", "-", "*", ">", "```")):
            if parts:
                break
            continue
        parts.append(stripped)
    return clean_inline(" ".join(parts))


def infer_type(path: Path, frontmatter: dict[str, Any]) -> str:
    explicit = str(frontmatter.get("type") or frontmatter.get("note_type") or "").strip()
    if explicit:
        return explicit
    rel = repo_rel(path)
    if rel == "wiki/index.md":
        return "index"
    if rel == "wiki/log.md":
        return "log"
    parts = path.relative_to(WIKI_ROOT).parts
    section = parts[0] if parts else ""
    if section == "papers":
        return "paper"
    if section == "claims":
        return "claim-card" if path.name != "README.md" else "index"
    if section == "sources":
        return "source"
    if section == "topics":
        return "topic"
    if section == "maps":
        return "map"
    if section == "reports":
        return "report"
    if section == "guidance":
        return "guidance"
    if section == "progress":
        return "progress"
    if section == "architecture":
        return "architecture"
    if section == "templates":
        return "template"
    return "page"


def infer_role(path: Path, page_type: str) -> str:
    rel = repo_rel(path)
    if rel == "wiki/index.md":
        return "home"
    if rel == "wiki/log.md":
        return "log"
    if path.name == "README.md":
        return "index"
    if page_type in {"claim-card", "paper", "source", "topic", "report", "map", "guidance", "template"}:
        return page_type
    return "page"


def infer_timestamp(frontmatter: dict[str, Any]) -> str:
    for key in ("timestamp", "updated", "last_reviewed", "date"):
        value = frontmatter.get(key)
        if value:
            text = str(value)
            if "Y" in text or "M" in text or "D" in text:
                continue
            if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
                return f"{text}T00:00:00Z"
            return text
    return DEFAULT_TIMESTAMP


def generated_description(title: str, page_type: str, path: Path) -> str:
    if page_type == "paper":
        return (
            f"Paper fragment for {title}, including inventory metadata, local "
            "source status, evidence quality, and Claim Card links."
        )
    if page_type == "claim-card":
        return f"Claim Card for {title}, including evidence locator, source references, review status, and topic links."
    if page_type == "source":
        return f"Source note for {title}, including evidence boundaries, use constraints, and follow-up gaps."
    if page_type == "template":
        return f"Template for creating a {path.stem.replace('-', ' ')} wiki page."
    return f"{title} OKF {page_type} page."


def normalize_frontmatter_for(path: Path, frontmatter: dict[str, Any], body: str) -> dict[str, Any]:
    normalized = dict(frontmatter)
    page_type = infer_type(path, normalized)
    title = str(normalized.get("title") or first_heading(body) or path.stem.replace("-", " ").title()).strip()
    current_description = str(normalized.get("description") or "").strip()
    prior_generic = current_description == f"{title} OKF {page_type} page."
    description = str(
        ""
        if prior_generic
        else normalized.get("description") or normalized.get("okfr_summary") or first_paragraph(body)
    ).strip()
    if not description:
        description = generated_description(title, page_type, path)
    if len(description) > 240:
        description = description[:237].rstrip() + "..."

    normalized["type"] = page_type
    normalized["title"] = title
    normalized["description"] = description
    normalized["timestamp"] = infer_timestamp(normalized)
    normalized.setdefault("okf_version", OKF_VERSION)
    normalized.setdefault("okfr_role", infer_role(path, page_type))
    current_summary = str(normalized.get("okfr_summary") or "").strip()
    summary_is_generic = current_summary == f"{title} OKF {page_type} page." or current_summary.endswith(
        f"OKF {page_type} page."
    )
    if not current_summary or summary_is_generic:
        normalized["okfr_summary"] = description
    return normalized


def normalized_text_for(path: Path) -> str:
    original = path.read_text(encoding="utf-8")
    frontmatter, body, _ = parse_frontmatter(original)
    normalized = normalize_frontmatter_for(path, frontmatter, body)
    return dump_frontmatter(normalized) + body.rstrip() + "\n"


def validate_required_frontmatter(page: WikiPage) -> list[str]:
    errors: list[str] = []
    for field in OKF_REQUIRED_FIELDS:
        if field not in page.frontmatter or page.frontmatter.get(field) in ("", [], None):
            errors.append(f"{page.rel_path} missing required OKF frontmatter: {field}")
    version = page.frontmatter.get("okf_version")
    if version and str(version) != OKF_VERSION:
        errors.append(f"{page.rel_path} has unsupported okf_version: {version}")
    return errors


def resolve_markdown_target(source: Path, target: str) -> Path:
    clean = target.split("#", 1)[0].split("?", 1)[0]
    if not clean:
        return source
    candidate = (source.parent / clean).resolve()
    if candidate.is_dir():
        if (candidate / "index.md").is_file():
            candidate = candidate / "index.md"
        elif (candidate / "README.md").is_file():
            candidate = candidate / "README.md"
        else:
            candidate = candidate / "index.md"
    return candidate


def extract_links(page: WikiPage) -> list[LinkRecord]:
    records: list[LinkRecord] = []
    node_paths = {repo_rel(path): path for path in wiki_markdown_files()}
    for match in LOCAL_LINK_RE.finditer(page.body):
        raw_target = match.group(1).strip()
        if raw_target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean_target = raw_target.split("#", 1)[0].split("?", 1)[0]
        if not clean_target:
            continue
        resolved = resolve_markdown_target(page.path, raw_target)
        try:
            rel = repo_rel(resolved)
        except ValueError:
            continue
        exists = resolved.exists()
        is_wiki_page = rel in node_paths
        records.append(
            LinkRecord(
                source=page.rel_path,
                target=rel,
                raw_target=raw_target,
                text=clean_inline(match.group(0)),
                exists=exists,
                is_wiki_page=is_wiki_page,
            )
        )
    return records


def section_for(rel_path: str) -> str:
    parts = Path(rel_path).parts
    if len(parts) < 2:
        return "root"
    if parts[1] == "index.md":
        return "root"
    return parts[1]


def stable_edge_id(source: str, target: str, kind: str) -> str:
    digest = hashlib.sha256(f"{source}|{kind}|{target}".encode("utf-8")).hexdigest()[:16]
    return f"edge:{digest}"


def page_to_node(page: WikiPage) -> dict[str, Any]:
    fm = page.frontmatter
    return {
        "id": page.rel_path,
        "label": fm.get("title") or first_heading(page.body) or Path(page.rel_path).stem,
        "kind": infer_type(page.path, fm),
        "section": section_for(page.rel_path),
        "path": page.rel_path,
        "description": fm.get("description") or first_paragraph(page.body),
        "timestamp": fm.get("timestamp"),
        "tags": fm.get("tags") or [],
        "resource": fm.get("resource"),
        "aliases": fm.get("aliases") or [],
        "okf_version": fm.get("okf_version"),
        "okfr_role": fm.get("okfr_role"),
        "okfr_summary": fm.get("okfr_summary") or fm.get("description") or first_paragraph(page.body),
        "okfr_order": fm.get("okfr_order"),
        "okfr_date": fm.get("okfr_date"),
    }


def build_okf_graph() -> dict[str, Any]:
    pages = [load_page(path) for path in wiki_markdown_files()]
    nodes = [page_to_node(page) for page in pages]
    node_ids = {node["id"] for node in nodes}
    edges: list[dict[str, Any]] = []
    external_links: list[dict[str, Any]] = []
    for page in pages:
        for link in extract_links(page):
            if link.target in node_ids:
                edges.append(
                    {
                        "id": stable_edge_id(link.source, link.target, "links_to"),
                        "source": link.source,
                        "target": link.target,
                        "kind": "links_to",
                        "label": "links to",
                        "metadata": {
                            "raw_target": link.raw_target,
                            "relationship_label": "links to",
                            "inferred": False,
                        },
                    }
                )
            else:
                external_links.append(
                    {
                        "source": link.source,
                        "target": link.target,
                        "raw_target": link.raw_target,
                        "exists": link.exists,
                    }
                )
    return {
        "meta": {
            "kind": "okf-graph",
            "okf_version": OKF_VERSION,
            "root": "wiki/",
            "node_count": len(nodes),
            "edge_count": len(edges),
        },
        "nodes": nodes,
        "edges": sorted(edges, key=lambda edge: edge["id"]),
        "external_links": external_links,
    }


def okf_errors() -> list[str]:
    errors: list[str] = []
    for rel in ROOT_PAGES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required OKF root page: {rel}")
    for path in wiki_markdown_files():
        text = path.read_text(encoding="utf-8")
        frontmatter, body, has_frontmatter = parse_frontmatter(text)
        page = WikiPage(path=path, rel_path=repo_rel(path), frontmatter=frontmatter, body=body)
        if not has_frontmatter:
            errors.append(f"{page.rel_path} missing OKF frontmatter block")
        errors.extend(validate_required_frontmatter(page))
        if WIKILINK_RE.search(text):
            errors.append(f"{page.rel_path} contains Obsidian wikilink syntax")
        for link in extract_links(page):
            if not link.exists:
                errors.append(f"{page.rel_path} has broken Markdown link: {link.raw_target}")
    return errors


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def check_output(path: Path, content: str) -> list[str]:
    if not path.exists():
        return [f"{repo_rel(path)} is missing; regenerate it"]
    existing = path.read_text(encoding="utf-8")
    if existing == content:
        return []
    diff = "\n".join(
        difflib.unified_diff(
            existing.splitlines(),
            content.splitlines(),
            fromfile=f"{repo_rel(path)} (current)",
            tofile=f"{repo_rel(path)} (generated)",
            lineterm="",
            n=3,
        )
    )
    return [f"{repo_rel(path)} is out of date:\n{diff}"]


def add_check_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--check", action="store_true", help="Fail if generated files would change.")
