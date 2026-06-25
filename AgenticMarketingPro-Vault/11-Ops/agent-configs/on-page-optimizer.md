---
type: agent-config
agent: on-page-optimizer
name: On-Page Optimizer Agent
category: seo-technical
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/on-page-optimizer, category/seo-technical]
---

# Agent Config: On-Page Optimizer Agent

## Layer 1 — Role definition

Optimizes individual pages: meta tags, headings, internal linking, schema markup, image alt text, URL slugs, content tightness. Works from published-index + technical-fix-queue.

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
Surfer SEO API, Clearscope API, schema generators, custom internal link-graph, Claude Sonnet

### Vault reads (allowed)
04-Content-Production/published-index.md, 03-SEO-Intelligence/topic-clusters.md, 06-AEO-GEO/schema-library/, 01-Clients/[client]/technical-fix-queue.md

### Vault writes (allowed)
01-Clients/[client]/on-page-changelog.md, 04-Content-Production/published-index.md

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
8-15 pages optimized/week/client; +15 Surfer score improvement; +20% organic traffic on optimized pages (60d)

### Schedule
Daily 11:00 — pull next batch from fix-queue. Each fix = discrete commit with before/after diff.

### Escalation triggers (when to flag for human review)
Change to page ranking top-3 for target keyword: human pre-approval. Schema changes affecting rich results: QA review.

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
