# Localized Sources

This directory stores source provenance and local source material for the
LLM-Wiki.

- `raw/` contains localized source files as a local evidence cache. It is
  ignored by Git by default; treat files there as read-only after ingestion.
- `raw/redistributable/` is the explicit exception area for source files that
  may be committed, such as repo-owned or AI-generated PDFs that other users
  cannot otherwise retrieve.
- `metadata/` contains fetch manifests, hashes, failures, and derived metadata.

Historical raw blobs that were previously committed under `raw/` were removed
from the rewritten `main` history on 2026-06-02. Old commit or blob URLs that
target those files should not be treated as stable references; use the wiki
fragments and metadata records instead.

When a raw source cannot be fetched, keep the URL and failure reason in metadata
and continue updating the wiki from available inventory facts.

The current fetch manifest is [metadata/fetch-manifest.json](metadata/fetch-manifest.json).
