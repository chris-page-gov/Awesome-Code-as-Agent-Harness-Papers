---
type: "topic"
title: "Code as Agent Harness"
description: "Code as agent harness treats code as the executable, inspectable, and stateful structure through which agents reason, act, model environments, receive feedback, and coordinate."
timestamp: "2026-06-02T00:00:00Z"
tags: ["topic", "code-as-agent-harness", "survey"]
okf_version: "0.1"
okfr_role: "topic"
okfr_summary: "Code as agent harness treats code as the executable, inspectable, and stateful structure through which agents reason, act, model environments, receive feedback, and coordinate."
note_type: "topic"
status: "active"
last_reviewed: "2026-06-02"
source_ids: ["SOURCE-README-ORIGINAL-2026-06-02", "SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026"]
related: ["harness-interface.md", "harness-mechanisms.md", "scaling-the-harness.md", "applications.md"]
---

# Code as Agent Harness

## Working Definition

Code as agent harness treats code as the executable, inspectable, and stateful
structure through which agents reason, act, model environments, receive
feedback, and coordinate.

## Current Survey Map

- [Harness Interface](harness-interface.md): code as the interface between a
  model and a task environment.
- [Harness Mechanisms](harness-mechanisms.md): planning, memory/context, tool
  use, and debugging mechanisms inside the loop.
- [Scaling the Harness](scaling-the-harness.md): multi-agent structures,
  synchronization, representations, and convergence.
- [Applications](applications.md): code assistants, GUI/OS agents, scientific
  discovery agents, and embodied agents.

## Practical Use

For a coding agent, this wiki should answer three questions quickly:

- What part of the harness taxonomy is relevant?
- Which papers are the canonical starting points?
- Which local source files and fragments support the answer?

## PDF-Backed Structure

The localized survey PDF frames code as the operational substrate for reasoning,
acting, environment modeling, and execution-based verification. It presents the
three-layer taxonomy as a progression: code first enters the agent loop as an
interface, then supports mechanisms for long-horizon reliability, then becomes a
shared artifact for multi-agent coordination and verification.

The survey's stated open challenges are a useful future-work checklist for this
wiki: evaluate beyond final task success, verify under incomplete feedback,
improve harnesses without regressions, maintain consistent shared state, keep
human oversight for safety-critical actions, and extend the harness frame to
multimodal environments.

## Gaps

- Paper-specific contribution notes should be added only after source review.
- Section-level survey notes still need to be split out for each taxonomy layer.
