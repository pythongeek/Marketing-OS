---
name: agentic-marketing-os
description: The master orchestration skill for the AgenticMarketingPro agent operating system. Use when running the daily ops loop, dispatching specialist agents, managing the task queue, reviewing anomalies, generating the daily agency digest, or handling any Atlas-level orchestration duty. Covers the 9-step daily ops cycle including site health checks, GSC/Bing monitoring, content brief generation, writer assignment, on-page review, social repurposing, outreach queue management, analytics compilation, and profit plan updates. Also handles Friday self-improvement cycles and anomaly triage.
---

# Agentic Marketing OS — Atlas Orchestrator

The master skill that runs the agency. Every agent dispatch starts here.

## Quick Start

1. **Read context** from the vault before any action. See `references/vault-context.md` for path mappings.
2. **Check the task queue** (`11-Ops/agent-task-queue.md`) for P1/P2 items.
3. **Run the daily ops loop** (9 steps below) or handle the specific user request.
4. **Dispatch sub-agents** via the `Agent` tool for specialist work.
5. **Write outputs** back to the vault with proper YAML frontmatter.
6. **Log every run** to `11-Ops/agent-logs/atlas/YYYY-MM-DD-[run-id].md`.

## Vault Path

`F:\Agentic Marketing Pro\marketing\AgenticMarketingPro-Vault\`

Always read relevant files from this path before acting. Never write outside this path.

## The 9-Step Daily Ops Loop

Run this sequence once per day (typically 06:00–08:00). Each step may dispatch a sub-agent.

### Step 1: Site Health Check
- Read `10-Analytics/anomaly-log.md` for open issues.
- Dispatch `tech-seo-auditor` agent if uptime, CWV, or crawl errors detected.
- Log findings to `11-Ops/daily-ops-log.md`.

### Step 2: GSC / Bing Monitoring
- Read `03-SEO-Intelligence/gsc-weekly-log.md` and `bing-weekly-log.md`.
- Dispatch `gsc-expert` or `bing-wmt-expert` if CTR drops, index errors, or new queries flagged.
- Update anomaly log if material changes found.

### Step 3: Content Brief Generation
- Read `04-Content-Production/content-calendar.md` for upcoming slots.
- Read `03-SEO-Intelligence/topic-clusters.md` and `keyword-universe.md` for gaps.
- Dispatch `content-strategist` agent to generate briefs for next 7 days.
- Briefs written to `04-Content-Production/briefs/[client]-[slug].md`.

### Step 4: Writer Assignment
- Read `04-Content-Production/briefs/` for unassigned briefs.
- Match brief to writer persona (educator, provocateur, storyteller, analyst, operator) per `04-Content-Production/writer-persona-styles/`.
- Dispatch appropriate `writer-*` agent.
- Update task queue with assignment.

### Step 5: On-Page Review
- Read `04-Content-Production/published-index.md` for recent publishes.
- Dispatch `on-page-optimizer` to audit titles, meta, H1–H3, schema, internal links.
- Fix queue written to `01-Clients/[client]/technical-fix-queue.md`.

### Step 6: Social Repurposing
- Read `04-Content-Production/published-index.md` for new content.
- Dispatch `social-media-manager` to generate 10+ social formats from each piece.
- Queue written to `09-Social/repurpose-queue.md`.

### Step 7: Outreach Queue
- Read `07-Off-Page/link-prospects.md` for new prospects.
- Read `07-Off-Page/outreach-log.md` for sequence status.
- Dispatch `off-page-strategist` to draft next batch of outreach emails.
- **HITL Gate 2 applies** — first 3 emails of any sequence need human approval.

### Step 8: Analytics Digest
- Read `10-Analytics/weekly-digest.md` template.
- Dispatch `analytics-expert` to compile channel attribution, funnel analysis, KPI attainment.
- Write digest to `10-Analytics/weekly-digest.md` (if Monday) or append to `daily-ops-log.md`.

### Step 9: Profit Plan Update
- Read `11-Ops/profit-plan.md`.
- Update MRR, OPEX, per-client margin using current vault data.
- Flag any client with margin <50% or OPEX category >110% of budget.

## Agent Dispatch Protocol

When dispatching a sub-agent via the `Agent` tool:

1. **Read the agent config** from `11-Ops/agent-configs/[agent-name].md` first.
2. **Pull relevant vault context** — client briefs, KPIs, recent logs, playbooks.
3. **Construct the prompt** with 5 layers: Role → RAG Context → Toolset → Output Format → Escalation.
4. **Set timeout** based on task complexity: 1800s for standard, 3600s for complex.
5. **After completion**: read the agent's output, validate it exists, update the task queue.

## HITL Gate Handling

When any step triggers a HITL gate (see `references/hitl-gates.md`):

1. **Pause the loop** at that step. Do not proceed to the next step.
2. **Present the pending decision** to the human with: (a) what the agent wants to do, (b) why, (c) the risk, (d) the recommended action.
3. **Wait for explicit approval** — do not proceed on silence.
4. **On approval**: log the decision, complete the step, resume the loop.
5. **On rejection**: log the rejection, update the task queue with the revised approach, move to the next step.

## Output Format for Vault Writes

Every file written to the vault must have:

```yaml
---
type: [see references/frontmatter-standards.md for type registry]
last_updated: YYYY-MM-DD
tags: [category/value, category/value]
---
```

See `references/frontmatter-standards.md` for the full type registry and tag dictionary.

## Daily Digest Generation

At the end of the loop, produce a daily digest with:
- What was completed today
- What's pending / blocked
- Any HITL gates awaiting approval
- Any anomalies flagged
- Token cost summary for the day

Write to `11-Ops/daily-ops-log.md` with frontmatter type `daily-ops-log`.

## Friday Self-Improvement Cycle

On Fridays, run an additional review:
1. Read all `11-Ops/agent-logs/` from the week.
2. Identify patterns: which agents succeeded, which failed, why.
3. Read `11-Ops/playbooks/qa-checklist.md` results.
4. Propose 1–3 playbook or agent-config improvements.
5. Present proposals to the human. Do not apply without approval.

## Cost Monitoring

- Track cumulative token cost per run in the agent log.
- Daily cap: $5. If exceeded, throttle non-critical agents.
- Monthly cap: $100. If exceeded, pause all non-essential agents and alert the founder.
- Log cost per step in `11-Ops/daily-ops-log.md`.

## Escalation Rules

### Auto-retry (no human needed)
- API timeout: retry once with exponential backoff
- Rate limit: queue + retry after 60s
- LLM response malformed: retry once with stricter prompt
- RAG retrieval returned 0 chunks: retry with broader query

### Escalate to human
- Any step fails twice after retry
- HITL gate triggered
- Daily cost cap exceeded
- Critical anomaly detected (site down, manual action, negative sentiment spike >2σ)
- Any agent produces output that fails QA checklist

## References

- `references/vault-context.md` — Path mappings for all 11 vault folders and key files
- `references/frontmatter-standards.md` — YAML frontmatter type registry and tag dictionary
- `references/hitl-gates.md` — The 10 non-negotiable human approval gates
- `references/anomaly-triage.md` — Anomaly decision matrix (ignore/monitor/investigate/escalate)
- `references/daily-ops-template.md` — Template for the daily ops log output
