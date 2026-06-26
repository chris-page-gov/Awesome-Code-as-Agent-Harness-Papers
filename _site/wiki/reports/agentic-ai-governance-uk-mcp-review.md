---
type: "report"
title: "Agentic AI Governance UK MCP Review"
description: "This report reviews the redistributable DOCX draft sources/raw/redistributable/unofficial-draft-agentic-ai-governance-uk-mcp.docx against the current Code as Agent Harness wiki and paper corpus. The review is wiki-first: paper fragments,..."
timestamp: "2026-06-02T00:00:00Z"
tags: ["report", "governance", "mcp", "uk-government", "bibliography"]
okf_version: "0.1"
okfr_role: "report"
okfr_summary: "This report reviews the redistributable DOCX draft sources/raw/redistributable/unofficial-draft-agentic-ai-governance-uk-mcp.docx against the current Code as Agent Harness wiki and paper corpus. The review is wiki-first: paper fragments,..."
note_type: "report"
status: "draft"
last_reviewed: "2026-06-02"
source_ids: ["SOURCE-UNOFFICIAL-DRAFT-AGENTIC-AI-GOVERNANCE-UK-MCP-2026", "SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026"]
related: ["../sources/SOURCE-UNOFFICIAL-DRAFT-AGENTIC-AI-GOVERNANCE-UK-MCP-2026.md", "../reports/llm-wiki-primary-source-evaluation.md"]
---

# Agentic AI Governance UK MCP Review

## Review Scope

This report reviews the redistributable DOCX draft
`sources/raw/redistributable/unofficial-draft-agentic-ai-governance-uk-mcp.docx`
against the current Code as Agent Harness wiki and paper corpus. The review is
wiki-first: paper fragments, topic notes, source notes, and the paper index were
used as the research surface rather than reopening the original paper PDFs.

The draft is explicitly unofficial, AI-generated, and not endorsed by any part
of Government. Nothing in this report is legal advice or policy clearance.

## Overall Assessment

The draft is directionally strong. It correctly shifts the governance question
from model quality to action authority: when an agent can update records, invoke
tools, trigger payments, contact citizens, deploy code, or delete data, the
control surface is the harness around the model. That position is well aligned
with the wiki's organizing survey note, which frames code as the operational
substrate for reasoning, acting, environment modeling, and execution-based
verification.

The main amendment is to make that alignment explicit. The draft currently
uses MCP, gateways, identity, policy, audit, and procurement as practical
controls. It should recast those controls as a government-grade agent harness:
an interface layer for action, a mechanism layer for tools, policy, memory,
feedback, and approvals, and a scaling layer for shared state, evidence,
portfolio governance, incident response, and multi-agent attribution.

## Strong Elements

- The decision summary is usable: it asks for a minimum MCP profile, tool
  metadata schema, evidence schema, approvals model, third-party MCP posture,
  and procurement criteria.
- The gateway recommendation is the right architectural center. The wiki corpus
  repeatedly makes the tool boundary visible, and the draft turns that boundary
  into an enforceable inspection point.
- The draft distinguishes protocol from governance. MCP can standardize
  discovery and calls, but it does not by itself decide data classification,
  authority, approvals, retention, redress, or procurement evidence.
- Appendix A and Appendix B are valuable because they make governance testable:
  tool metadata and evidence records are concrete artifacts, not abstract
  principles.
- The legal and redress section is a necessary shift from "can the agent act?"
  to "may the public body lawfully act this way, and can the person affected
  challenge it?"

## Recommended Amendments

### 1. Add a "Government Agent Harness" framing section

Insert a short section after the executive summary:

- Harness Interface: how the agent crosses from language/model reasoning into
  action-bearing tools, resources, records, code, or communications.
- Harness Mechanisms: identity, gateway policy, tool schemas, memory/state
  handles, approval gates, execution sandboxes, feedback, and retries.
- Scaling the Harness: central registry, shared evidence store, portfolio
  inventory, conformance tests, incident response, and cross-agent attribution.

This would connect the paper directly to the Code as Agent Harness taxonomy and
make the governance argument less vendor-specific.

### 2. Separate protocol facts from profile decisions

Several claims in the draft are a blend of MCP release-candidate facts and UK
Government design choices. Add a two-column table:

| MCP or external fact | UK Government profile decision |
| --- | --- |
| MCP defines hosts, clients, servers, tools, resources, prompts, and transport behavior. | Production action-bearing calls must pass through an approved gateway. |
| MCP exposes tool schemas and protocol metadata. | Government requires owner, service, data class, risk tier, approval rule, retention rule, and incident owner. |
| MCP has transport and authorization requirements. | Government bans token passthrough and requires audience-bound tokens plus central trace export. |
| MCP supports tool discovery. | Government permits only private, mirrored, proxied, or curated registries for production use. |

This will reduce the risk that readers treat raw MCP support as equivalent to
public-sector assurance.

### 3. Strengthen the threat model

Add a threat-model subsection before the minimum controls:

- untrusted or malicious public MCP servers;
- prompt injection leading to tool misuse;
- tool-description poisoning or stale cached tool metadata;
- token passthrough and confused-deputy failures;
- state-handle replay, reuse, or cross-user leakage;
- hidden long-running task continuation after authorization has changed;
- evidence gaps where traces remain inside the agent runtime;
- multi-agent failure attribution gaps;
- sandbox escape, irreversible side effects, and rollback failure;
- over-reliance on human approval where the approver lacks context.

This aligns the governance paper with wiki entries on MCP threats, sandboxing,
agent safety, governed memory, and observability-driven harness evolution.

### 4. Define conformance tests, not only procurement criteria

Procurement should require runnable evidence. Add a "minimum conformance pack":

- gateway rejects action-bearing calls without agent identity, human context
  where applicable, trace context, and tool risk metadata;
- destructive or externally visible actions require an approval artifact;
- token audience validation and token-passthrough rejection are tested;
- state handles expire, bind to purpose/caller, and are re-authorized;
- registry changes invalidate cached tool metadata;
- incident kill switch freezes evidence and blocks further calls;
- sandbox tests prove isolation, rollback, and exportable traces;
- evidence records can be reconciled across host, gateway, MCP server, and
  downstream service logs.

### 5. Add evaluation measures for public-sector use

The draft should add metrics beyond "agent success":

- action accuracy: the right tool was called with the right inputs;
- authority accuracy: the agent had the right delegated authority;
- approval quality: humans were asked only when needed and with enough context;
- trace completeness: every action can be reconstructed externally;
- rollback and containment: unsafe actions can be stopped or undone;
- redress readiness: affected users can receive explanation and review;
- regression resistance: profile or model updates do not weaken controls;
- operator load: controls do not create unmanageable approval queues.

This mirrors the survey note's open challenge that evaluation must go beyond
final task success.

### 6. Treat legal duties as control requirements

Keep the legal section, but make every legal point map to a required harness
artifact. For example:

- automated or significant-decision test -> approval and redress policy;
- data protection by design -> data-class fields in tool metadata;
- DPIA gate -> registry status before production;
- algorithmic transparency -> public record linkage in the agent inventory;
- public-law fairness -> reason codes and decision-owner evidence;
- equality impacts -> pre-production assessment and monitoring evidence.

The report should explicitly say that legal currency needs departmental legal
review and current official guidance.

## Proposed Bibliography Additions

Add these to the draft bibliography or a "Related research" appendix. The links
point to the wiki fragments used for this review unless an official external
source is a better fit.

### Core framing

- [Code as Agent Harness Survey](../sources/SOURCE-CODE-AS-AGENT-HARNESS-SURVEY-2026.md).
  Use for the taxonomy: Harness Interface, Harness Mechanisms, Scaling the
  Harness, and the evaluation challenge beyond task success.
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../papers/agentic-harness-engineering-observability-driven-automatic-evolution-of-32a741f4.md).
  Use for the argument that observability and feedback are not optional
  logging extras; they are harness inputs.

### MCP and protocol surface

- [Model Context Protocol](../papers/model-context-protocol-5929925a.md).
  Use as a local corpus entry for MCP as a practical agent-to-tool interface.
- [Model Context Protocol (MCP): Landscape, Security Threats, and Future Research Directions](../papers/model-context-protocol-mcp-landscape-security-threats-and-future-researc-a33b66a1.md).
  Use for the threat-model appendix and future research framing.
- [A Survey on Model Context Protocol: Architecture, State-of-the-art, Challenges and Future Directions](../papers/a-survey-on-model-context-protocol-architecture-state-of-the-art-challen-51ec4866.md).
  Use as a secondary MCP architecture survey, with the caveat that the current
  wiki fragment has little extracted text.
- [From Glue-Code to Protocols: A Critical Analysis of A2A and MCP Integration for Scalable Agent Systems](../papers/from-glue-code-to-protocols-a-critical-analysis-of-a2a-and-mcp-integrati-6c83ea89.md).
  Use for the shift from ad hoc connectors to protocolized agent systems.

### Governance, safety, sandboxing, and evidence

- [Introducing the Agent Governance Toolkit: Open-Source Runtime Security for AI Agents](../papers/introducing-the-agent-governance-toolkit-open-source-runtime-security-fo-24b2c1ff.md).
  Use for runtime governance vocabulary and security controls.
- [Beyond Static Sandboxing: Learned Capability Governance for Autonomous AI Agents](../papers/beyond-static-sandboxing-learned-capability-governance-for-autonomous-ai-a8b8b443.md).
  Use for capability governance beyond coarse sandbox allow/deny controls.
- [Fault-Tolerant Sandboxing for AI Coding Agents: A Transactional Approach to Safe Autonomous Execution](../papers/fault-tolerant-sandboxing-for-ai-coding-agents-a-transactional-approach-260e82ac.md).
  Use for rollback, containment, and safe autonomous execution.
- [Openagentsafety: A comprehensive framework for evaluating real-world ai agent safety](../papers/openagentsafety-a-comprehensive-framework-for-evaluating-real-world-ai-a-d60c0cfd.md).
  Use for real-world agent safety evaluation.
- [NormCode: A Semi-Formal Language for Auditable AI Planning](../papers/normcode-a-semi-formal-language-for-auditable-ai-planning-96b226f7.md).
  Use for auditable planning and policy-expression ideas.
- [MemGovern: Enhancing Code Agents through Learning from Governed Human Experiences](../papers/memgovern-enhancing-code-agents-through-learning-from-governed-human-exp-acb2227b.md).
  Use for governed experiential memory and human-feedback loops.

### Official public-sector anchors to verify before policy use

- [AI Playbook for the UK Government](https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government).
- [Generative AI Framework for HMG](https://www.gov.uk/government/publications/generative-ai-framework-for-hmg).
- [Algorithmic Transparency Recording Standard](https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub).
- [Data Ethics Framework](https://www.gov.uk/government/publications/data-ethics-framework).
- [Model Context Protocol draft specification](https://modelcontextprotocol.io/specification/draft).
- [Model Context Protocol 2026-07-28 release candidate](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/).
- [W3C Trace Context Recommendation](https://www.w3.org/TR/trace-context/).

## Suggested Structural Changes To The Draft

1. Add a one-page "control stack" after the decision summary.
2. Move vendor cards into an appendix and promote architecture controls to the
   main body.
3. Add a "minimum conformance pack" after the procurement criteria.
4. Add a short "failure scenarios" section before the legal section.
5. Add a "human approval is not enough" subsection that defines useful approval
   context, approver authority, timeout, audit, and challenge route.
6. Add a "known limits" box stating that MCP release-candidate claims must be
   revalidated when the final specification ships and that legal claims require
   departmental legal review.

## Bottom Line

The draft is a credible policy-facing bridge between MCP infrastructure and the
Code as Agent Harness research frame. Its strongest contribution is practical:
it turns protocol mechanics into a government control profile. Its main risk is
that readers may read a vendor/protocol comparison as a complete assurance
case. The paper should make the agent harness explicit, add a conformance test
pack, and tie every legal or accountability duty to a concrete artifact in the
harness.
