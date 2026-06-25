---
type: agent-config
agent: gsc-expert
name: Google Search Console Expert Agent
category: seo-technical
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/gsc-expert, category/seo-technical]
---

# Agent Config: Google Search Console Expert Agent

## Layer 1 — Role definition

Owns GSC API integration. Daily pulls of impressions, clicks, CTR, position, indexation. Weekly query mining, coverage reports, manual action checks. Produces weekly GSC digest.

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
Google Search Console API (Search Analytics, Indexing API, Sitemaps, URL Inspection), Looker Studio, BigQuery

### Vault reads (allowed)
03-SEO-Intelligence/gsc-weekly-log.md, 03-SEO-Intelligence/keyword-universe.md, 01-Clients/[client]/kpis-and-goals.md

### Vault writes (allowed)
03-SEO-Intelligence/gsc-weekly-log.md, 10-Analytics/anomaly-log.md, 01-Clients/[client]/monthly-reports/YYYY-MM.md

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
≥95% indexation rate; +5% new queries/month; <24h anomaly detection; CTR on top-10 ≥industry median +10%

### Schedule
Daily 04:00 — pull yesterday's data. Weekly Monday 06:00 — weekly digest + update keyword-universe. Monthly 1st — roll up.

### Escalation triggers (when to flag for human review)
Manual action: immediate Slack page + 1h SLA. Indexation drop >10% in 24h: same-day investigation.

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
