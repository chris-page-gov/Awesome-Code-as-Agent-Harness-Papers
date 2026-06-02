# Progress

Last updated: 2026-06-02

## Current Status

- [x] Repointed `origin` to the user fork.
- [x] Inspected nearby repos for the established LLM-Wiki/control-file pattern.
- [x] Added initial root control files and documentation lockstep rule.
- [x] Added initial Karpathy-style LLM-Wiki structure.
- [x] Added source notes for the LLM-Wiki method, current README inventory, and
  the Code as Agent Harness survey.
- [x] Generated 354 per-paper/per-reference wiki fragments from 458 README rows.
- [x] Updated README paper links to point at local wiki fragments while
  preserving canonical external links inside each fragment.
- [x] Localized the Code as Agent Harness survey PDF.
- [x] Localized source files for all 354 paper fragments and updated
  those fragments.
- [x] Added resumable ingest automation for localization, integration,
  validation, and checkpoint pushes.
- [x] Auto-integrated 354 localized source files into wiki fragments.
- [x] Completed source localization under `sources/raw/` for all paper fragments.
- [x] Added the redistributable Agentic AI Governance UK MCP draft as a source.
- [x] Added governance-review and LLM-Wiki effectiveness reports.
- [x] Added Claim Cards, claim register validation, explicit agent review
  tiers, thematic claim-backed topic pages, evidence-packet tooling,
  bibliography export, and a reusable wiki evaluation suite.
- [x] Evaluated Claim Card/evidence-packet synergy with Assertion SeeLinks and
  generated a SeeLinks `seelinks-assertions` demo pack for human review.

## Open Follow-Ups

- Promote selected high-value Claim Cards from `agent-reviewed` to
  `cross-agent-reviewed` using a separate reviewer-agent manifest where the
  reviewer confirms traceability and absence of overclaiming.
- Keep manual source overrides current when publisher-hosted URLs block direct
  downloads.
- Promote repeatedly used, current, source-specific cards to `decision-grade`
  only after the relevant review criteria are met.
- Copy `exports/seelinks/code-agent-harness-claim-review-demo/` into the
  SeeLinks static data directory and exercise the workbench UI review flow.
- Add a round-trip SeeLinks review manifest importer before applying any
  human-review decisions back to Claim Cards.
- Re-run wiki validation before each meaningful checkpoint.
