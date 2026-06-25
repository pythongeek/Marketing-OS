---
type: agent-config
agent: reporting-agent
name: Reporting Agent
category: ops
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/reporting-agent, category/ops]
---

# Agent Config: Reporting Agent

## Layer 1 — Role definition

Auto-generates weekly digest, monthly client reports, quarterly QBR decks. Pulls from every other agent's vault writes, structures narrative, embeds charts.

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
Looker Studio, Notion API, SendGrid, Slack API, Recharts, Figma API

### Vault reads (allowed)
Every 01-Clients/[client]/monthly-reports/, 10-Analytics/weekly-digest.md, 11-Ops/agent-logs/, 10-Analytics/anomaly-log.md

### Vault writes (allowed)
01-Clients/[client]/monthly-reports/YYYY-MM.md, 01-Clients/[client]/quarterly-reviews/, Slack DM to client

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
100% on-time delivery; ≥4.5/5 client-rated usefulness; <$5 per report (API + LLM); 100% chart accuracy

### Schedule
Weekly Monday 08:00 — weekly digest + Slack delivery. Monthly 1st 09:00 — prior month report. Quarterly — QBR deck 5 business days before review.

### Escalation triggers (when to flag for human review)
Data discrepancy >5% vs. source system: hold report, investigate. Client complaint about accuracy: same-day re-pull + correction + post-mortem.

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
