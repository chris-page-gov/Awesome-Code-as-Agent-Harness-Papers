---
title: "Harness Interface"
note_type: "topic"
status: "active"
tags: ["topic", "harness-interface", "reasoning", "acting", "environment-modeling"]
source_ids: ["SOURCE-README-ORIGINAL-2026-06-02"]
related: ["code-as-agent-harness.md", "../maps/taxonomy-map.md"]
last_reviewed: "2026-06-02"
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

- Per-paper fragments need generation and source localization.

