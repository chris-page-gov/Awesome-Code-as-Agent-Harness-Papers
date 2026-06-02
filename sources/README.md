# Localized Sources

This directory stores local source material for the LLM-Wiki.

- `raw/` contains localized source files. Treat these as read-only after
  ingestion.
- `metadata/` contains fetch manifests, hashes, failures, and derived metadata.

When a raw source cannot be fetched, keep the URL and failure reason in metadata
and continue updating the wiki from available inventory facts.

