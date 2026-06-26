# Repository Operating Rules

These rules apply to the whole repository. More specific `AGENTS.md` files can
add rules for their own folders.

## Mission

Maintain this fork as a source-driven Karpathy-style LLM-Wiki for the Code as
Agent Harness paper and its reference graph. The wiki should make the survey
immediately useful to humans and coding agents while preserving the original
awesome-list inventory.

## Fork Boundary

- `origin` is the user fork:
  `https://github.com/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers.git`.
- Do not add a push path to the original source repository.
- When asked to push, push only to `origin`.
- Preserve upstream attribution, citations, licence notices, and external links.

## Operating Memory

- Start with [CONTEXT.md](CONTEXT.md) for durable repo orientation.
- Use [PROGRESS.md](PROGRESS.md) for current status, blockers, validation, and
  next steps.
- Record user-visible changes in [CHANGELOG.md](CHANGELOG.md).
- Keep multi-step work resumable in [plans/](plans/).
- Use [LLM-WIKI.md](LLM-WIKI.md) before broad taxonomy, source-ingest, or
  documentation changes.

## Knowledge Layer

- [wiki/](wiki/) is the LLM-Wiki layer.
- [wiki/index.md](wiki/index.md) is the main navigation entry point.
- [wiki/sources/](wiki/sources/) stores one source note per source or source
  family.
- [wiki/papers/](wiki/papers/) stores one reusable wiki fragment per paper or
  external reference once ingested.
- [wiki/claims/](wiki/claims/) stores atomic Claim Cards generated from source
  notes, localized sources, or explicit gaps.
- [wiki/topics/](wiki/topics/) stores synthesis notes.
- [wiki/maps/](wiki/maps/) stores guided entry points and cross-reference maps.
- [wiki/guidance/okf-profile.md](wiki/guidance/okf-profile.md) defines the
  local `OKF v0.1 + OKFR extensions` profile used for generated reader and
  SeeLinks exports.
- [exports/okfr/](exports/okfr/) stores generated OKFR SeeLinks data packages.
- [_site/](_site/) is generated static publication output and must be rebuilt
  from wiki/source metadata rather than hand-edited.
- [sources/raw/](sources/raw/) stores localized source files as a local
  evidence cache. Treat these files as read-only after they are added, and do
  not commit them unless they are intentionally placed in
  `sources/raw/redistributable/`.
- [sources/metadata/](sources/metadata/) stores fetch manifests, hashes, and
  derived metadata.

## Source Discipline

- Do not invent paper claims.
- Every generated claim should trace to a source note, localized raw source, or
  an explicit gap.
- Use explicit evidence tiers: `metadata-only`, `localized`,
  `auto-extracted`, `agent-drafted`, `agent-reviewed`,
  `cross-agent-reviewed`, `human-reviewed`, and `decision-grade`.
- Treat `human-reviewed` as literal. Agent-created contribution notes, threat
  taxonomies, recommendations, and Claim Cards must use agent review tiers
  unless a named human reviewer is recorded.
- Keep raw source files immutable. If a source needs transformation, write the
  derivative outside `sources/raw/`, or into `sources/raw/redistributable/`
  only when it is intentionally redistributable.
- Prefer concise paraphrases and source paths over long excerpts.
- When a source cannot be fetched because of network slowness or publisher
  access, add a registered gap and continue with local metadata.
- Use normal Markdown links for repo files and external sources.
- Keep OKF/OKFR reader metadata factual and derived from wiki, register, or
  source material. Do not treat generated summaries or inferred graph
  relationships as human review.
- Use `tools/normalize_okf_frontmatter.py` for deterministic OKF frontmatter
  fill-ins rather than hand-editing large batches of generated fragments.
- Use `tools/build_okf_graph.py`, `tools/build_okfr_seelinks_pack.py`, and
  `tools/build_okfr_site.py` to regenerate reader artifacts. Markdown and JSON
  registers remain the source of truth.

## Documentation Lockstep

Keep documentation in lockstep with structural, source, or taxonomy changes:

- Update [CHANGELOG.md](CHANGELOG.md) for what changed.
- Update [CONTEXT.md](CONTEXT.md) when repo assumptions, source boundaries, or
  architecture change.
- Update [PROGRESS.md](PROGRESS.md) for current status and follow-ups.
- Update [README.md](README.md), [LLM-WIKI.md](LLM-WIKI.md), or
  [wiki/index.md](wiki/index.md) when entry points change.
- Update source registers and wiki fragments in the same commit as source
  localization or xref changes.
- Update OKF guidance, generated OKFR exports, and `_site/` in the same
  checkpoint when reader/publication behavior changes.

## Validation

Run these before committing documentation or wiki structural changes:

```bash
git diff --check
python3 tools/check_wiki.py
python3 tools/check_okf.py
```

When OKFR exports or publication output change, also run:

```bash
python3 tools/build_okf_graph.py --check
python3 tools/build_okfr_seelinks_pack.py --check
python3 tools/build_okfr_site.py --check
```
