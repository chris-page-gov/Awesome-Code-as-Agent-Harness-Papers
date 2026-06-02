---
title: "LLM-Wiki Primary Source Evaluation"
note_type: "report"
status: "draft"
tags: ["report", "llm-wiki", "evaluation", "method"]
source_ids:
  - "SOURCE-KARPATHY-LLM-WIKI-2026"
  - "SOURCE-UNOFFICIAL-DRAFT-AGENTIC-AI-GOVERNANCE-UK-MCP-2026"
related:
  - "../architecture/llm-wiki-architecture.md"
  - "../reports/agentic-ai-governance-uk-mcp-review.md"
last_reviewed: "2026-06-02"
---

# LLM-Wiki Primary Source Evaluation

## Aim

This evaluation records how effective the current LLM-Wiki implementation was
as the primary research surface for reviewing the Agentic AI Governance UK MCP
draft. The goal is pragmatic: understand where the wiki accelerated the work,
where it created risk, and what implementation changes would make the next
review more reliable.

## Method

The review deliberately used the wiki first:

1. Start from [wiki/index.md](../index.md), [source notes](../sources/README.md),
   and [paper index](../papers/README.md).
2. Search wiki fragments for governance-relevant terms: MCP, governance,
   safety, security, policy, gateway, identity, audit, evidence, approval,
   human, registry, sandbox, trace, observability, accountability, and redress.
3. Read selected wiki fragments and topic pages, not the original paper PDFs.
4. Use the new DOCX source directly because it is the object under review.
5. Use official external links only for time-sensitive government or protocol
   anchors where relying only on the wiki would be irresponsible.

This is therefore a test of the wiki as a research interface, not a full
literature review of every underlying paper.

## What Worked Well

### 1. Discovery was fast

The wiki made it easy to identify a relevant sub-corpus quickly:

- MCP-specific entries:
  [Model Context Protocol](../papers/model-context-protocol-5929925a.md),
  [Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](../papers/model-context-protocol-mcp-landscape-security-threats-and-future-researc-a33b66a1.md),
  [A Survey on Model Context Protocol](../papers/a-survey-on-model-context-protocol-architecture-state-of-the-art-challen-51ec4866.md),
  and [From Glue-Code to Protocols](../papers/from-glue-code-to-protocols-a-critical-analysis-of-a2a-and-mcp-integrati-6c83ea89.md).
- Governance and runtime-security entries:
  [Agent Governance Toolkit](../papers/introducing-the-agent-governance-toolkit-open-source-runtime-security-fo-24b2c1ff.md),
  [Beyond Static Sandboxing](../papers/beyond-static-sandboxing-learned-capability-governance-for-autonomous-ai-a8b8b443.md),
  [Fault-Tolerant Sandboxing](../papers/fault-tolerant-sandboxing-for-ai-coding-agents-a-transactional-approach-260e82ac.md),
  and [OpenAgentSafety](../papers/openagentsafety-a-comprehensive-framework-for-evaluating-real-world-ai-a-d60c0cfd.md).
- Evidence and audit-adjacent entries:
  [Agentic Harness Engineering](../papers/agentic-harness-engineering-observability-driven-automatic-evolution-of-32a741f4.md),
  [NormCode](../papers/normcode-a-semi-formal-language-for-auditable-ai-planning-96b226f7.md),
  and [MemGovern](../papers/memgovern-enhancing-code-agents-through-learning-from-governed-human-exp-acb2227b.md).

Without the wiki, this would have required searching the README, opening many
links, and manually deciding which papers were likely relevant.

### 2. Provenance status reduced uncertainty

The status metadata showed that all 354 paper fragments were localized and
integrated. That did not mean all claims were reviewed, but it did mean the
corpus was complete enough to search consistently. The local-source path and
hash metadata also made it clear which items had evidence files.

### 3. The source-discipline model handled the new DOCX cleanly

The raw-local policy and redistributable exception worked as intended. The new
AI-generated DOCX belongs under `sources/raw/redistributable/` because other
users would not have access to the original local path. The source note records
hash, size, review status, and use boundaries.

### 4. The taxonomy helped convert research into amendments

The Code as Agent Harness taxonomy gave a strong reviewing lens:

- Harness Interface mapped to agent-to-tool action boundaries.
- Harness Mechanisms mapped to identity, tools, state, approval, memory,
  policy, feedback, and sandbox controls.
- Scaling the Harness mapped to evidence stores, registry governance,
  cross-agent attribution, incident response, and procurement conformance.

That taxonomy made the review more coherent than a vendor-by-vendor comparison.

## What Did Not Work Well

### 1. Paper fragments are still mostly automated cues

Most paper fragments contain source status, local path, extracted text length,
term counts, and detected topic tags. They do not yet contain reviewed
contribution notes. Example: the MCP threat paper fragment is discoverable and
has useful term cues, but it does not yet summarize its threat taxonomy or
recommendations. The wiki was excellent for finding the paper and weak for
using it as a claim source.

### 2. Some high-value fragments are thin

The "A Survey on Model Context Protocol" fragment records only 281 extracted
characters from its localized HTML source. That is enough to know the item
exists, but not enough for a policy-facing claim. The wiki made this limitation
visible, which is good, but the report still needed caution.

### 3. Topic pages lagged completion state

Several topic pages still said "Per-paper fragments need generation and source
localization" even though localization was complete. This was fixed during this
review, but it shows a weakness: wiki maintenance can drift even when status
JSON is correct. Human-facing synthesis pages need lockstep checks, not only
register checks.

### 4. The wiki has weak claim granularity

Current fragments do not expose page-level, section-level, or quote-bounded
claim cards. This matters for policy review because recommendations should cite
specific claims, not just whole papers. The current wiki supports discovery and
light synthesis, but not high-assurance argumentation.

### 5. External legal and protocol currency still matters

For UK Government governance, the wiki alone is not enough. Official sources
such as the AI Playbook, Generative AI Framework, Algorithmic Transparency
Recording Standard, MCP draft specification, and MCP release-candidate post are
time-sensitive. The wiki can record them, but the review must still check
current official sources before making legal, procurement, or protocol claims.

## Examples

### Example A: MCP governance

The wiki quickly exposed four MCP-related entries. That was enough to suggest a
bibliography expansion and a stronger threat-model section. However, the wiki
fragments did not contain reviewed MCP claims about authorization, token
audience, state handles, or transport headers. Those details should be captured
as claim cards before the wiki can support a decision-ready protocol review.

### Example B: Sandboxing and containment

Searching the paper index for "sandbox" immediately located Beyond Static
Sandboxing and Fault-Tolerant Sandboxing. That supported an amendment to add
rollback, containment, and conformance tests. The wiki gave strong coverage
confidence, but the actual details remain at "source cue" level.

### Example C: Human oversight and evidence

The Code as Agent Harness survey source note explicitly names human oversight,
evaluation beyond final task success, and consistent shared state as open
challenges. That was directly useful. MemGovern and NormCode were also easy to
find, but their fragments did not yet explain how governed human experience or
auditable planning works.

### Example D: Source operations

Adding the DOCX as a redistributable source was straightforward because the repo
already has a tracked exception path and source-register convention. This is a
clear benefit of the implementation: source policy is operational, not just
documented.

## Recommendations

1. Add claim cards for high-value fragments.
   Each reviewed paper should expose 5-10 atomic claims with source path, page
   or section, evidence type, confidence, and related wiki topics.

2. Promote thematic synthesis notes.
   Add dedicated notes for MCP governance, agent safety, sandboxing, evidence
   and observability, human oversight, procurement conformance, and agent
   memory/state governance.

3. Add a report evidence-packet command.
   A script should take keywords or paper IDs and emit a markdown packet with
   selected fragments, source status, local paths, reviewed claims, gaps, and
   bibliography lines.

4. Add stale-gap checks.
   Validation should flag human-facing pages that still contain obsolete
   phrases such as "source localization needed" when status JSON says complete.

5. Add source-quality tiers.
   Distinguish `metadata-only`, `localized`, `auto-extracted`,
   `human-reviewed`, and `decision-grade`. The current `integrated` status is
   useful but too broad for policy work.

6. Add bibliography export.
   A small tool should generate markdown, BibTeX, or CSL JSON from the paper
   register and source register. Reports should not hand-roll bibliography
   entries.

7. Add official-source monitoring for volatile domains.
   Protocol specs, government guidance, legal instruments, and vendor product
   docs should be marked volatile and rechecked before publication.

## Implementation Plan

### Phase 1: Evidence Hygiene

- Add `evidence_quality` to paper fragments and the register.
- Update generators so automated extraction yields `auto-extracted`, not a
  vague integrated state.
- Add stale-phrase validation for topic pages and progress pages.

### Phase 2: Claim Store

- Create `wiki/claims/` with one markdown or JSON record per atomic claim.
- Start with 12 high-value governance papers and source notes:
  Code as Agent Harness Survey, MCP Landscape, MCP architecture survey,
  From Glue-Code to Protocols, Agent Governance Toolkit, Beyond Static
  Sandboxing, Fault-Tolerant Sandboxing, OpenAgentSafety, Agentic Harness
  Engineering, NormCode, MemGovern, and Model Context Protocol.
- Require claim records to cite source path and page/section when available.

### Phase 3: Thematic Synthesis

- Add `wiki/topics/mcp-governance.md`.
- Add `wiki/topics/agent-safety-and-sandboxing.md`.
- Add `wiki/topics/evidence-observability-and-redress.md`.
- Add `wiki/topics/procurement-and-conformance.md`.
- Link each theme to claim cards, not just paper fragments.

### Phase 4: Report Tooling

- Add `tools/build_evidence_packet.py` to assemble reports from topic, paper,
  source, and claim records.
- Add `tools/export_bibliography.py` for markdown and BibTeX output.
- Add a report template requiring an evidence log, wiki-only limitations, and
  external-source checks.

### Phase 5: Governance Review Loop

- For each new policy or governance draft, add it as a source note first.
- Run an evidence packet.
- Write a review report.
- Record where wiki evidence was sufficient and where original or official
  sources were required.
- Promote any recurring gap into either a claim-card task or a source-monitoring
  task.

## Conclusion

This LLM-Wiki implementation is already useful as a navigation and provenance
layer. It dramatically reduces discovery time and gives a disciplined way to add
redistributable sources. It is not yet sufficient as a decision-grade evidence
system because most fragments are automated cues rather than reviewed claims.
The next step is not more raw localization; it is claim-level review, thematic
synthesis, and tooling that turns the wiki into a reliable evidence packet for
each report.
