# Code Agent Harness LLM-Wiki Claim Review Demo

This SeeLinks pack turns the LLM-Wiki Claim Card layer into an assertion review surface.

- Included Claim Cards: `160`
- Source Claim Cards available in the wiki: `1148`
- Human review state: every imported card starts as `proposed`.
- Agent evidence tier: preserved separately as `evidence_tier`.
- Local raw source blobs: not redistributed unless already marked redistributable.

Recommended first filters: `claim_type=gap`, `evidence_tier=cross-agent-reviewed`, and `external_recheck_required=true`.
