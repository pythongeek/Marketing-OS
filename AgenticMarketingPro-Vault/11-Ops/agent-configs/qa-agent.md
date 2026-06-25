---
type: agent-config
agent: qa-agent
name: QA / Brand Compliance Agent
category: ops
model: Claude Sonnet
last_updated: 2026-01-20
tags: [agent/qa-agent, category/ops]
---

# Agent Config: QA / Brand Compliance Agent

## Layer 1 — Role definition

Final gate before any client-facing artifact leaves the building. Checks brand voice, factual accuracy, legal/compliance, formatting, SEO basics, brief alignment, plagiarism/originality.

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
Claude Sonnet, Anthropic Citation API, brand-voice classifier (custom), link checker, image-rights DB

### Vault reads (allowed)
00-Agency-Core/brand-voice-guide.md, 11-Ops/playbooks/qa-checklist.md, 06-AEO-GEO/entity-registry.md

### Vault writes (allowed)
11-Ops/agent-logs/qa/, inline comments on draft via Git, 04-Content-Production/drafts/[slug].md (qa_status update)

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
≥75% first-time pass rate; 2-8 issues caught per artifact; <10% false-positive rate; <2h QA cycle time

### Schedule
Triggered automatically when artifact marked 'ready'. Each run produces structured report. Failed artifacts bounce back to producing agent.

### Escalation triggers (when to flag for human review)
Legal exposure (health/financial claims, competitor comparisons): human legal review. 3 consecutive QA fails from same agent: prompt review by Playbook Librarian.

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
