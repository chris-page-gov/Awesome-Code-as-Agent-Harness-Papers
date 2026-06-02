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
  Harness survey PDF, and localized arXiv source files for the first 261 paper fragments.
- Added a resumable source-ingest automation driver, source integration pass,
  and generated ingest status metadata.

### Changed

- Added README entry points for the local fork wiki.
- Repointed README paper-table links to local wiki fragments while preserving
  canonical external links inside the fragments.
- Updated localized paper fragments with local source paths and source status.
- Promoted the first localized fragments into automated source-cue integration
  notes.
