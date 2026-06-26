---
type: "topic"
title: "Harness Interface"
description: "The README defines the Harness Interface layer as code serving as the basic interface between a model and its task environment. This layer covers code for reasoning, acting, and environment modeling."
timestamp: "2026-06-02T00:00:00Z"
tags: ["topic", "harness-interface", "reasoning", "acting", "environment-modeling"]
okf_version: "0.1"
okfr_role: "topic"
okfr_summary: "The README defines the Harness Interface layer as code serving as the basic interface between a model and its task environment. This layer covers code for reasoning, acting, and environment modeling."
note_type: "topic"
status: "active"
last_reviewed: "2026-06-02"
source_ids: ["SOURCE-README-ORIGINAL-2026-06-02"]
related: ["code-as-agent-harness.md", "../maps/taxonomy-map.md"]
---

# Harness Interface

## Scope

The README defines the Harness Interface layer as code serving as the basic
interface between a model and its task environment. This layer covers code for
reasoning, acting, and environment modeling.

## Subareas

- Code for Reasoning: programs externalize intermediate logic into executable
  or checkable computation.
- Code for Acting: generated programs act as policies, tool calls, behaviour
  trees, or reusable skills.
- Code for Environment Modeling: program states, repositories, traces,
  simulators, and tests represent state, dynamics, and feedback.

## First Reading Route

- Program-delegated reasoning and PAL-style program-aided language models.
- Code as Policies and ReAct for action interfaces.
- SWE-bench, AgentBench, InterCode, and world-model papers for environment and
  evaluation interfaces.

## Gaps

- Paper fragments, local sources, and Claim Cards are available. Promote
  repeatedly used high-value cards from `agent-reviewed` to
  `cross-agent-reviewed` or `decision-grade` when source-specific review
  criteria are met.
