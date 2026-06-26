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

The wiki is being published through the local
`OKF v0.1 + OKFR extensions` profile documented in
[wiki/guidance/okf-profile.md](wiki/guidance/okf-profile.md). OKF frontmatter,
normal Markdown links, Claim Card traceability, and generated graph metadata
feed the OKFR reader, SeeLinks data package, and static site outputs. The
rollout plan is tracked in
[plans/2026-06-26-okfr-reader-and-okf-compliance.md](plans/2026-06-26-okfr-reader-and-okf-compliance.md).

Reader/publication artifacts are generated rather than hand-maintained:

- OKF graph: `tools/build_okf_graph.py`
- OKFR SeeLinks pack: `tools/build_okfr_seelinks_pack.py`
- Static site: `tools/build_okfr_site.py`
- OKF validation: `tools/check_okf.py`

Generated outputs:

- `exports/okf/code-agent-harness-okf-graph.json`
- `exports/okfr/code-agent-harness-okfr/pack.json`
- `_site/index.html`
- `_site/viewer.html`

Reader guidance:

- `wiki/guidance/okfr-jit-training.md`
- `wiki/guidance/okfr-ui-specification.md`
