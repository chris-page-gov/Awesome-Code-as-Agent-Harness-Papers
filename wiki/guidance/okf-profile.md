---
type: "guidance"
title: "OKF Profile"
description: "Local OKF v0.1 plus OKFR extension profile for the Code as Agent Harness LLM-Wiki."
timestamp: "2026-06-26T00:00:00Z"
okf_version: "0.1"
okfr_role: "profile"
okfr_summary: "Defines required frontmatter, portable Markdown link rules, and generated reader/export expectations."
tags: ["okf", "okfr", "profile", "guidance"]
---

# OKF Profile

This repository uses `OKF v0.1 + OKFR extensions` for the wiki layer.

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

Use normal Markdown links only. Do not introduce Obsidian wikilinks, because
the generated OKFR viewer, SeeLinks data package, GitHub Pages publication, and
agent validation tooling all depend on portable Markdown link resolution.

Markdown pages and JSON registers are the source of truth. Generated OKF graph,
OKFR SeeLinks pack, and static site outputs must be regenerated and checked
rather than hand-maintained.
