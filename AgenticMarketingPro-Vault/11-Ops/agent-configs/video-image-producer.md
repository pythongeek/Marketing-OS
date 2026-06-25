---
type: agent-config
agent: video-image-producer
name: Video/Image Producer Agent
category: content
model: Claude Sonnet (script/storyboard) + generation APIs
last_updated: 2026-01-20
tags: [agent/video-image-producer, category/content]
---

# Agent Config: Video/Image Producer Agent

## Layer 1 — Role definition

Generates visual assets from text briefs. Scripts short-form video, produces storyboards, dispatches AI generation jobs (Midjourney, Runway, ElevenLabs, HeyGen). Outputs editing briefs for human editors.

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
Midjourney API, Runway Gen-3 API, ElevenLabs API, HeyGen API, Descript API, Canva API

### Vault reads (allowed)
04-Content-Production/briefs/, 09-Social/content-calendar.md, 00-Agency-Core/brand-voice-guide.md

### Vault writes (allowed)
04-Content-Production/drafts/[client]-[slug]-assets/, 09-Social/repurpose-queue.md

> Security note: Any tool call outside this declaration is blocked at the n8n orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output format spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation rules

### KPIs (this agent is measured against)
Asset production time <4h per short-form video; first-pass quality approval rate ≥70%; platform-native formatting compliance 100%

### Schedule
On-demand dispatch. Each job: script → storyboard → generated assets → editing brief.

### Escalation triggers (when to flag for human review)
Generation API down >30min: switch to backup provider. Brand-sensitive content (competitor logos, regulated claims): human approval before generation.

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
