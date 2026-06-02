# Localized Sources

This directory stores source provenance and local source material for the
LLM-Wiki.

- `raw/` contains localized source files as a local evidence cache. It is
  ignored by Git by default; treat files there as read-only after ingestion.
- `raw/redistributable/` is the explicit exception area for source files that
  may be committed, such as repo-owned or AI-generated PDFs that other users
  cannot otherwise retrieve.
- `metadata/` contains fetch manifests, hashes, failures, and derived metadata.

When a raw source cannot be fetched, keep the URL and failure reason in metadata
and continue updating the wiki from available inventory facts.

The current fetch manifest is [metadata/fetch-manifest.json](metadata/fetch-manifest.json).
