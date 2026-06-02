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
- [wiki/topics/](wiki/topics/) stores synthesis notes.
- [wiki/maps/](wiki/maps/) stores guided entry points and cross-reference maps.
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
- Keep raw source files immutable. If a source needs transformation, write the
  derivative outside `sources/raw/`, or into `sources/raw/redistributable/`
  only when it is intentionally redistributable.
- Prefer concise paraphrases and source paths over long excerpts.
- When a source cannot be fetched because of network slowness or publisher
  access, add a registered gap and continue with local metadata.
- Use normal Markdown links for repo files and external sources.

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

## Validation

Run these before committing documentation or wiki structural changes:

```bash
git diff --check
python3 tools/check_wiki.py
```
