---
type: agent-config
agent: competitor-intel
name: Competitor Intelligence Agent
category: intelligence
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/competitor-intel, category/intelligence]
---

# Agent Config: Competitor Intelligence Agent

## Layer 1 — Role definition

Continuously monitors 3-5 named competitors per client. Tracks keyword movements, new content, backlinks, ad changes, team/hiring signals, product/funding announcements. Surface material changes within 24h.

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
Ahrefs API, Semrush API, SpyFu, SimilarWeb, Crunchbase API, LinkedIn Sales Nav (manual), BuiltWith

### Vault reads (allowed)
02-Competitors/[name]/*, 01-Clients/[client]/competitor-watch.md, 03-SEO-Intelligence/keyword-universe.md

### Vault writes (allowed)
02-Competitors/[name]/{keyword-gaps,backlink-profile,content-audit,paid-strategy,team-and-hiring}.md, 10-Analytics/anomaly-log.md

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
Competitor coverage freshness ≤7 days; anomaly false-positive rate <30%; strategist-rated weekly digest ≥4/5

### Schedule
Monday 06:00 — full re-pull. Daily 09:00 — lightweight check for new content + backlinks + hires.

### Escalation triggers (when to flag for human review)
Material competitor move (new product page, funding round, executive hire): page strategist via Slack within 2h. >3 anomalies on single competitor in 24h: same-day review.

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
