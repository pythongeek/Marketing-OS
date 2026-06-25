---
type: playbook
title: Anomaly Triage Rules
description: Rules Atlas uses to triage anomalies into ignore/monitor/investigate/escalate.
last_updated: 2026-01-20
owner: Atlas (Master Orchestrator)
tags: [playbook, type/triage-rules]
---

# Anomaly Triage Rules

## Triage decision matrix

| Source | Anomaly example | Default triage | Specialist |
|---|---|---|---|
| GSC Expert | Clicks drop 30% on top-5 keyword in 24h | Investigate | On-Page + AEO/GEO |
| GSC Expert | New query appears in top-20 | Monitor | Content Strategist |
| Site Health | INP regression >100ms | Investigate | Tech SEO Auditor |
| Site Health | Uptime drop (site down) | Escalate | Human (always) |
| Reputation | Negative sentiment spike >2σ | Escalate | Human (always) |
| Reputation | Single negative review | Monitor | Reputation Agent |
| Competitor Intel | Competitor publishes 5+ pages in 24h | Monitor | Content Strategist |
| Competitor Intel | Competitor raises Series B | Escalate | Strategist + Founder |
| Ad Expert | CPA doubles in 6h | Escalate | Human (always) |
| Ad Expert | CPA +20% over 7 days | Investigate | Ad Expert + Strategist |
| AEO/GEO | Citation rate drops 50% across 3 LLMs | Investigate | AEO/GEO + Content |
| Forecasting | 90-day forecast variance >30% | Investigate | Strategist + Forecasting |
| MarTech | Critical API endpoint down >15 min | Escalate | Human (always) |
| MarTech | API rate limit at 80% | Monitor | MarTech Integration |
| Market Signals | Confirmed Google algorithm update | Escalate | Human (always) |
| Market Signals | Suspected algorithm update | Monitor | Atlas (72h window) |
| Email | Deliverability drops >5% in 24h | Investigate | Email/Lifecycle + Strategist |
| Email | Open rate -10% on a single send | Monitor | Email/Lifecycle |

## Triage definitions

### Ignore
- Anomaly is expected (e.g., weekend traffic dip)
- No action, no log entry, no notification

### Monitor
- Log entry in anomaly-log.md
- Watch for 24h
- If worsens → Investigate
- If resolves → close log entry

### Investigate
- Log entry in anomaly-log.md
- Dispatch to specialist agent with scoped task
- Specialist produces investigation report
- If confirmed material → Escalate
- If false positive → close log entry with notes

### Escalate
- Log entry in anomaly-log.md (severity: high or critical)
- Page human via Slack #escalations channel
- Human SLA: 1h (critical), 4h (high)
- Atlas produces incident brief for human

## False-positive rate target
- Target: <30% (i.e., ≥70% of "investigate" anomalies are real)
- If >30% for 2 consecutive weeks: Playbook Librarian refines triage rules

## Override rules
- Atlas may downgrade "escalate" to "investigate" if it has high confidence the anomaly is benign (e.g., known seasonality)
- Atlas may NEVER downgrade "escalate" to "ignore" without human approval
- Atlas may NEVER auto-resolve a "critical" severity without human confirmation
