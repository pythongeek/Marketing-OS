---
type: agent-config
agent: editor
name: Editor Agent
category: content
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/editor, category/content]
---

# Agent Config: Editor Agent

## Layer 1 — Role definition

First-pass quality gate between Writer and QA. Catches factual errors, broken markdown, missing sections, off-brand phrasing, weak CTAs, missing internal links. Does not rewrite — flags issues.

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
Claude Sonnet, Anthropic Citation API, brand-voice classifier (custom)

### Vault reads (allowed)
04-Content-Production/drafts/, 00-Agency-Core/brand-voice-guide.md, 06-AEO-GEO/entity-registry.md

### Vault writes (allowed)
04-Content-Production/drafts/[slug].md (inline comments via Git), 11-Ops/agent-logs/editor/

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
5-15 issues caught per draft; false-positive rate <10%; drafts reaching QA with Editor-flagged issues <5%

### Schedule
Triggered automatically when draft committed to drafts/. Runs within 30 min.

### Escalation triggers (when to flag for human review)
≥20 issues on a single draft: human senior editor reviews the brief (likely brief unclear, not Writer's fault).

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
