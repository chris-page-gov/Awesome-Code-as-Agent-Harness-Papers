# OKF Reader / SeeLinks OKFR Rollout Plan

Date: 2026-06-26

## Objective

Publish the Code as Agent Harness LLM-Wiki as an OKF v0.1 corpus with OKFR
reader extensions, export it as a SeeLinks-compatible data package, and use the
`api-mcp-wiki` reader pattern to improve human understanding of complex wiki,
claim, source, and graph material.

## Scope

- Normalize `wiki/**/*.md` to the local `OKF v0.1 + OKFR extensions` profile.
- Add validation and graph-export tooling that treats Markdown as the source of
  truth and generated reader artifacts as drift-checked outputs.
- Export a SeeLinks OKFR pack under `exports/okfr/code-agent-harness-okfr/`.
- Build a static `_site/` publication with a generated OKFR viewer and GitHub
  Pages workflow.
- Document the reusable OKFR graph, side-panel, timeline, tile, and
  stack-of-cards patterns as JIT training for future OKF packs.
- Implement reusable OKFR support in the adjacent SeeLinks repo on branch
  `codex/okfr-reader`.

## Local OKF Profile

The wiki profile is `OKF v0.1 + OKFR extensions`.

Required frontmatter:

- `type`
- `title`
- `description`
- `timestamp`

Optional frontmatter:

- `resource`
- `tags`
- `aliases`
- `okf_version`
- `okfr_role`
- `okfr_summary`
- `okfr_order`
- `okfr_date`

Links remain normal Markdown links only. Obsidian wikilinks are invalid for this
repo because the generated reader, GitHub Pages site, and SeeLinks pack all use
portable Markdown links as their interchange surface.

## Implementation Sequence

### 1. Plan And Lockstep Docs

- Add this plan artifact.
- Update `AGENTS.md`, `CHANGELOG.md`, `CONTEXT.md`, `PROGRESS.md`,
  `LLM-WIKI.md`, and `wiki/index.md`.
- Commit and push to `origin/main`.

### 2. OKF Profile And Validation Tools

- Add `wiki/guidance/okf-profile.md`.
- Add `tools/okf_lib.py` for shared frontmatter parsing, link extraction, graph
  construction, and deterministic metadata normalization.
- Add `tools/check_okf.py`.
- Add `tools/build_okf_graph.py`.
- Add `tools/normalize_okf_frontmatter.py`.
- Extend `tools/check_wiki.py` so OKF validation is part of normal wiki
  validation.

### 3. Frontmatter Normalization

Normalize wiki Markdown in controlled batches:

- First: `wiki/index.md`, `wiki/log.md`, `wiki/topics/`, `wiki/maps/`,
  `wiki/reports/`, `wiki/guidance/`.
- Then: `wiki/papers/`, `wiki/claims/`, `wiki/sources/`.

Generated values must be deterministic. Existing titles, tags, aliases,
register metadata, Claim Card data, and source notes should be preserved.

### 4. OKF Graph And OKFR Pack Export

- Add `tools/build_okfr_seelinks_pack.py`.
- Generate:
  - `exports/okfr/code-agent-harness-okfr/pack.json`
  - `exports/okfr/code-agent-harness-okfr/intro.md`
  - `exports/okfr/code-agent-harness-okfr/README.md`
- Use stable item and graph IDs derived from repo-relative paths.
- Preserve Claim Card traceability through item properties and graph edges.
- Store inferred relationship labels in `edge.metadata.relationship_label` with
  `edge.metadata.inferred = true`.
- Emit a strict SeeLinks runtime shape: `meta.source` uses the existing
  `local|mcp|file` enum, `meta.fields` lists property IDs, rich property
  definitions stay in `meta.field_defs` / `properties`, and OKFR-specific Claim
  Card taxonomy is preserved in metadata while `graph.claims[].assertion_type`
  maps to the SeeLinks assertion enum.

### 5. Static Publication

- Add `tools/build_okfr_site.py`.
- Generate `_site/index.html`, `_site/viewer.html`,
  `_site/data/code-agent-harness-okfr/pack.json`, public wiki Markdown pages,
  screenshot assets, license, citation, README, changelog, and progress
  summaries.
- Add `.github/workflows/pages.yml`.
- Exclude local-only raw source blobs, caches, Word lock files, `.DS_Store`, and
  private temporary outputs.

### 6. SeeLinks OKFR Reader

In `/Users/crpage/repos/seelinks`:

- Create branch `codex/okfr-reader`.
- If any local SeeLinks demo/UI changes are present, commit them first as a
  baseline checkpoint.
- Add data-model types for `OkfManifest`, `OkfrDisplayHints`, and optional
  `PackMeta.okf` / `PackMeta.okfr`.
- Add reusable OKFR display helpers for short labels, summaries, dates,
  relationship chips, breadcrumbs, side-panel content, and tile fields.
- Add an OKFR view activated by `packKind="okfr"` without changing the default
  behavior of assertion, geography, or ontology packs.
- Model the graph/timeline/detail interaction on `api-mcp-wiki/viewer.html`:
  hamburger concept list, central graph modes, right detail panel, navigation
  history, edge tooltips, relationship chips, references, and referenced-by
  links.

### 7. JIT Training And UI Specification

- Add `wiki/guidance/okfr-jit-training.md`.
- Add `wiki/guidance/okfr-ui-specification.md`.
- Add screenshot assets under `wiki/assets/okfr-jit/`.
- Teach entry paths, graph/timeline/tile/card-stack selection, relationship
  interpretation, source-review limits, and inferred relationship meaning.

## Validation

Current repo:

```sh
git diff --check
python3 tools/check_wiki.py
python3 tools/check_okf.py
python3 tools/build_okf_graph.py --check
python3 tools/build_okfr_seelinks_pack.py --check
python3 tools/build_okfr_site.py --check
```

SeeLinks:

```sh
pnpm --dir /Users/crpage/repos/seelinks --filter @seelinks/data-model test
pnpm --dir /Users/crpage/repos/seelinks --filter @seelinks/web test
pnpm --dir /Users/crpage/repos/seelinks --filter @seelinks/web build
```

Browser verification:

- Load `/?pack=/data/code-agent-harness-okfr/pack.json`.
- Open hamburger timeline/search list.
- Select a timeline event and confirm graph focus.
- Confirm the right panel shows summary, status, relationship chips,
  references, and referenced-by links.
- Confirm relationship chip hover highlights graph edges.
- Confirm tile front/back and stack-of-cards examples are readable on desktop
  and mobile widths.
- Confirm non-OKFR packs still render normally.

## Acceptance Criteria

- OKF validation passes.
- Existing wiki validation passes.
- Local-only raw blobs are not published.
- Generated OKFR pack validates as SeeLinks data.
- `_site/` contains a working `index.html` and `viewer.html`.
- JIT training screenshots are committed and linked from Markdown.
- SeeLinks has a reusable OKFR reader path that remains pack-specific via data,
  not hard-coded Code Agent Harness content.
