# LLM-Wiki

Start at [wiki/index.md](wiki/index.md).

This wiki is the tracked agent-readable map for the Code as Agent Harness paper
and reference graph. It separates localized raw sources, source notes, paper
fragments, and synthesis topics so future work can update evidence without
losing the survey structure.

The current evidence layer includes [wiki/claims/](wiki/claims/) and
[wiki/data/claim-register.json](wiki/data/claim-register.json). Claim Cards are
atomic source-bounded records with explicit agent, cross-agent, human, or
decision-grade review status.

The Claim Card layer can also be exported as a SeeLinks human-review surface
with [tools/build_seelinks_claim_pack.py](tools/build_seelinks_claim_pack.py).
The current demo pack lives under
[exports/seelinks/code-agent-harness-claim-review-demo/](exports/seelinks/code-agent-harness-claim-review-demo/).
