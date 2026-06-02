---
title: "Source Discipline"
note_type: "guidance"
status: "active"
tags: ["source-discipline", "provenance", "llm-wiki"]
source_ids: ["SOURCE-KARPATHY-LLM-WIKI-2026"]
related: ["ingest-workflow.md", "../templates/source-note.md", "../templates/paper-fragment.md"]
last_reviewed: "2026-06-02"
---

# Source Discipline

## Rules

- Raw sources stay immutable once localized.
- Source notes describe what a source is, why it matters, and how it may be
  used.
- Paper fragments can summarize placement in the survey before source download,
  but must mark content evidence as pending until the source is localized or
  reviewed.
- Topic notes may synthesize, but must link back to paper fragments, source
  notes, or explicit gaps.
- Unsupported claims become gaps or open questions.
- Prefer short paraphrases and source paths over copied excerpts.

## Claim Labels

- `source_fact`: directly stated by a localized or cited source.
- `inventory_fact`: directly present in the README inventory.
- `local_synthesis`: conclusion drawn from several source-backed notes.
- `implementation_decision`: local repo decision.
- `gap`: missing source, missing metadata, or unresolved interpretation.
- `risk`: known or suspected source, licensing, access, or maintenance issue.

## Slow-Network Handling

If source download is slow or unavailable:

- Keep the paper fragment.
- Record the canonical URL and fetch status.
- Add a gap in the fragment.
- Continue with other wiki work.

