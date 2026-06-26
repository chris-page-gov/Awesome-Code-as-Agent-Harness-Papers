# Changelog

All notable changes to this fork are recorded here.

## [Unreleased]

### Added

- Added root agent control files for fork isolation, source discipline, progress
  tracking, and documentation lockstep.
- Added a Karpathy-style LLM-Wiki scaffold with source notes, topic notes, maps,
  progress tracking, and validation.
- Added initial source notes for the LLM-Wiki method, the current README paper
  inventory, and the Code as Agent Harness survey.
- Added a generated paper register and 354 reusable paper/reference fragments
  under `wiki/papers/`.
- Added a generator and validation checks for paper-register and README xref
  integrity.
- Added a source-localization tool, fetch manifest, the localized Code as Agent
  Harness survey PDF, and localized source files for all 354 paper fragments.
- Added a resumable source-ingest automation driver, source integration pass,
  and generated ingest status metadata.
- Added the redistributable unofficial Agentic AI Governance UK MCP DOCX source
  and source note.
- Added review reports for the governance draft and for using the LLM-Wiki as
  the primary research surface.
- Added a Claim Card evidence layer with `wiki/claims/`,
  `wiki/data/claim-register.json`, explicit review tiers, and claim-card
  templates.
- Added claim generation, review, evidence-packet, bibliography export, and
  LLM-Wiki evaluation tooling.
- Added claim-backed topic pages for MCP governance, agent safety and
  sandboxing, evidence/observability/redress, and procurement/conformance.
- Added reusable evaluation fixtures under `tests/wiki_eval/`.
- Added a SeeLinks Claim Card pack exporter, a curated
  `seelinks-assertions` demo pack, and a synergy evaluation/specification for
  Assertion SeeLinks human review.
- Added the OKF Reader / SeeLinks OKFR rollout plan covering OKF compliance,
  generated OKFR data packages, static publication, SeeLinks reader reuse, and
  JIT training/specification assets.

### Changed

- Added README entry points for the local fork wiki.
- Repointed README paper-table links to local wiki fragments while preserving
  canonical external links inside the fragments.
- Updated localized paper fragments with local source paths and source status.
- Promoted all localized fragments into automated source-cue integration
  notes.
- Updated topic-page gaps to reflect completed source localization, generated
  Claim Cards, and explicit agent/cross-agent/human review tiers.
- Updated paper fragments to link to generated Claim Cards and expose
  `evidence_quality`.
- Updated repository operating guidance to treat `OKF v0.1 + OKFR extensions`,
  generated reader artifacts, and static publication output as part of the
  documentation lockstep workflow.

### Removed

- Rewrote `main` history to remove previously committed raw source blobs under
  `sources/raw/`. Raw captures are now a local-only cache by default; commit
  redistributable exceptions under `sources/raw/redistributable/` only.
