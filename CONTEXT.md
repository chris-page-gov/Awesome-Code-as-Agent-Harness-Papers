# Context

Last reviewed: 2026-06-02

## Repository Purpose

This fork localizes and expands the original *Awesome Code as Agent Harness
Papers* list into a source-backed LLM-Wiki for the survey *Code as Agent
Harness: Toward Executable, Verifiable, and Stateful Agent Systems*.

The original README organizes papers around three survey layers:

- Harness Interface: code as reasoning, acting, and environment-modeling
  interface.
- Harness Mechanisms: planning, memory/context, tool use, and feedback-guided
  debugging.
- Scaling the Harness: multi-agent role specialization, interaction,
  workflow topology, feedback, synchronization, representation, and
  convergence.

It also groups application areas such as code assistants, GUI/OS agents,
scientific discovery agents, and embodied agents.

## Current Orientation

- `origin` points to the user fork at
  `https://github.com/chris-page-gov/Awesome-Code-as-Agent-Harness-Papers.git`.
- There is no configured push URL for the original source repository.
- The top-level README remains the visible awesome-list surface.
- The wiki layer starts at [LLM-WIKI.md](LLM-WIKI.md) and [wiki/index.md](wiki/index.md).
- Raw localized source files should be placed under [sources/raw/](sources/raw/)
  and treated as read-only evidence after ingestion.
- The generated paper register at [wiki/data/paper-register.json](wiki/data/paper-register.json)
  currently records 354 unique paper/reference fragments from 458 README rows.
- README paper rows now link to local fragments under [wiki/papers/](wiki/papers/);
  each fragment preserves the canonical external source URL.

## Local Pattern Adopted

This repo follows the recent local LLM-Wiki pattern found in:

- `guidance-for-agentic-data-analyst-using-amazon-bedrock-agentcore-on-aws`:
  lightweight root control files plus `LLM-WIKI.md` and `wiki/`.
- `wcc-mapping`: richer Karpathy-style source discipline, source notes, topic
  notes, maps, progress notes, and validation.

## Durable Decisions

- Keep upstream attribution and citation material intact.
- Do not block wiki usefulness on slow source downloads.
- Register unfetched sources as gaps rather than leaving them invisible.
- Keep the fork isolated from upstream writes.
- Treat bibliographic rows in the README as inventory metadata until the
  corresponding source has been localized or separately verified.
- Use `tools/generate_paper_fragments.py` for README-to-fragment regeneration
  rather than hand-editing hundreds of paper rows.
