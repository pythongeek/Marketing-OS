---
type: agent-config
agent: pitch-agent
name: Pitch / Proposal Agent
category: ops
model: Claude Opus
last_updated: 2026-01-20
tags: [agent/pitch-agent, category/ops]
---

# Agent Config: Pitch / Proposal Agent

## Layer 1 — Role definition

Builds prospect-specific proposals using competitive intel, historical case studies from vault, prospect's actual site audit. Used by bizdev to convert leads from Revenue Scout.

### What this agent owns
[See role above]

### What this agent NEVER does
[See escalation rules below — these are enforced at orchestration layer]

## Layer 2 — RAG context block (injected at runtime)

Retrieved chunks always include:
- Relevant client brief / KPIs / onboarding
- Relevant playbooks from `11-Ops/playbooks/`
- Recent agent logs (episodic memory — what worked / failed recently)
- Current state from working memory (today's anomalies, today's task queue)

Block size: 4K-8K tokens depending on agent role.

## Layer 3 — Toolset declaration

### APIs this agent can call
Claude Opus, Google Slides API, Beautiful.ai, Loom, Screaming Frog, Ahrefs

### Vault reads (allowed)
11-Ops/deal-pipeline.md, 00-Agency-Core/services-and-pricing.md, 00-Agency-Core/positioning-statements.md, 01-Clients/[similar-client]/onboarding.md, 02-Competitors/[prospect-competitor]/

### Vault writes (allowed)
11-Ops/pitches/[prospect]-YYYY-MM-DD.md, follow-up sequence drafts

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
<48h proposal turnaround; ≥25% pitch-to-close rate; ≥60% case study reuse rate

### Schedule
On-demand trigger from bizdev. Per pitch: prospect audit (4h), competitive positioning (2h), case study selection (1h), proposal draft (3h), exec review (1h).

### Escalation triggers (when to flag for human review)
Prospect audit reveals red flag (penalized site, fake traffic, major technical debt): flag for bizdev before pitching. Active litigation with current client: hard stop.

### Auto-recovery rules (when to retry without escalating)
- API timeout: retry once with exponential backoff
- Rate limit hit: queue + retry after 60s
- LLM response malformed: retry once with stricter prompt
- RAG retrieval returned 0 chunks: retry with broader query, then escalate if still 0

## Cost & token budget
- **Target cost per run:** $0.05-$0.50 (varies by task complexity)
- **Daily budget cap:** $5 (auto-throttle if exceeded)
- **Monthly budget cap:** $100 (auto-pause + alert founder if exceeded)

## Version history
- v1.0 (2026-01-20): Initial config from architecture plan
