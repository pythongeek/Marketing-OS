---
type: agent-config
agent: [kebab-case-name]
name: [Human-Readable Name]
category: [orchestration | intelligence | content | technical | paid | social | ops | analytics]
model: [Claude Sonnet | Claude Opus | Claude Haiku | Kimi 1.5 | Minimax]
last_updated: YYYY-MM-DD
tags: [agent/[name], category/[category]]
---

# Agent Config: [Name]

## Layer 1 — Role Definition

[One-sentence role summary. Be specific about what this agent owns.]

### What this agent owns
- [Responsibility 1]
- [Responsibility 2]
- [Responsibility 3]
- [Responsibility 4]
- [Responsibility 5]

### What this agent NEVER does
- [Out-of-scope activity 1]
- [Out-of-scope activity 2]
- [Out-of-scope activity 3]

## Layer 2 — RAG Context Block

Retrieved chunks always include:
- [Specific vault path 1] — [what information from this path]
- [Specific vault path 2] — [what information from this path]
- Recent agent logs from `11-Ops/agent-logs/[agent-name]/` (episodic memory)
- Current state from working memory (today's anomalies, today's task queue)

Block size: 4K-8K tokens depending on agent role.

## Layer 3 — Toolset Declaration

### APIs this agent can call
- [API 1] — [purpose]
- [API 2] — [purpose]
- [API 3] — [purpose]

### Vault reads (allowed)
- [Specific folder path or file pattern]
- [Specific folder path or file pattern]

### Vault writes (allowed)
- [Specific folder path or file pattern]
- [Specific folder path or file pattern]

> Security note: Any tool call outside this declaration is blocked at the orchestration layer — even if the agent hallucinates a tool call, it will not execute.

## Layer 4 — Output Format Spec

Every output from this agent must be:
1. A structured markdown file with YAML frontmatter (per `11-Ops/playbooks/frontmatter-standards.md`)
2. Written to one of the declared vault write paths above
3. Logged in `11-Ops/agent-logs/AGENT_NAME/YYYY-MM-DD-run-id.md` with full input/output/cost/latency

## Layer 5 — Escalation Rules

### KPIs (this agent is measured against)
- [KPI 1]: [target]
- [KPI 2]: [target]
- [KPI 3]: [target]

### Schedule
- [When this agent runs]
- [Trigger conditions]

### Escalation triggers (when to flag for human review)
- [Specific threshold 1]: [what happens]
- [Specific threshold 2]: [what happens]
- [Specific threshold 3]: [what happens]

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
- v1.0 (YYYY-MM-DD): Initial config from architecture plan
