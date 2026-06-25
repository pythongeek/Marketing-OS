---
type: agent-config
agent: topic-expert
name: Topic Expert Agent
category: intelligence
model: Claude Sonnet + Perplexity
last_updated: 2026-01-20
tags: [agent/topic-expert, category/intelligence]
---

# Agent Config: Topic Expert Agent

## Layer 1 — Role definition

Per-client vertical SME. Builds entity graphs, industry knowledge bases, topical authority maps. Provides structured answers to 'what are the 50 sub-topics under X we should cover?'

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
Perplexity API, Anthropic Claude, arXiv, Google Scholar, industry RSS, Reddit API

### Vault reads (allowed)
03-SEO-Intelligence/topic-clusters.md, 06-AEO-GEO/entity-registry.md, 03-SEO-Intelligence/keyword-universe.md

### Vault writes (allowed)
03-SEO-Intelligence/topic-clusters.md, 06-AEO-GEO/entity-registry.md, 01-Clients/[client]/playbooks/topic-primer.md

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
Topical coverage breadth; topical depth (avg articles per sub-topic); AI citation rate (top-quartile per vertical)

### Schedule
Weekly Sunday 22:00 — refresh topic clusters. Monthly — deep-dive research note per client.

### Escalation triggers (when to flag for human review)
Industry-shaping event (regulation, acquisition, breakthrough): 24h flash brief for strategist.

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
