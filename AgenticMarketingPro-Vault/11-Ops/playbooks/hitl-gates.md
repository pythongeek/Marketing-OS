---
type: playbook
title: HITL Gates (Human-in-the-Loop)
description: The 10 non-negotiable human approval gates. Atlas cannot bypass these.
last_updated: 2026-01-20
owner: Atlas (Master Orchestrator) + Compliance Agent
tags: [playbook, type/hitl-gates, priority/critical]
---

# HITL Gates — The 10 Non-Negotiables

> These gates are enforced at the n8n orchestration layer. Atlas cannot bypass them, even under direct human instruction. To change a gate, the human must edit this playbook in Git (itself an audited action).

## Gate 1: Publish content
- **Trigger:** Any draft marked 'ready' in 04-Content-Production/
- **Approver:** Strategist + QA Agent pass
- **SLA:** Same business day
- **Why:** Brand safety + factual accuracy + legal exposure

## Gate 2: Send outreach email
- **Trigger:** First 3 emails of any new outreach sequence
- **Approver:** Strategist
- **SLA:** <4h
- **Why:** Brand reputation + deliverability + personalization quality

## Gate 3: Change ad budget
- **Trigger:** Any daily budget change >$100
- **Approver:** Strategist + Finance
- **SLA:** <2h
- **Why:** Direct financial exposure + platform policy compliance

## Gate 4: Modify site technical structure
- **Trigger:** Redirects, canonicals, robots.txt, server config changes
- **Approver:** Strategist + Developer
- **SLA:** <24h
- **Why:** Can cause deindexation, traffic loss, broken UX

## Gate 5: Publish pSEO batch
- **Trigger:** Any batch >50 pages
- **Approver:** Strategist
- **SLA:** <4h
- **Why:** Risk of cannibalization, indexation budget waste, quality dilution

## Gate 6: Respond to negative review
- **Trigger:** Any review <3 stars
- **Approver:** Strategist
- **SLA:** <24h
- **Why:** Public-facing brand response, legal/PR risk

## Gate 7: Send client report
- **Trigger:** Any artifact going to a client (report, deck, email)
- **Approver:** Strategist + Atlas review
- **SLA:** Same business day
- **Why:** Client relationship, accuracy, brand voice

## Gate 8: Approve agent prompt change
- **Trigger:** Any change to an agent's system prompt
- **Approver:** Architect + Strategist
- **SLA:** Weekly Monday review
- **Why:** Prompt changes affect all downstream output quality

## Gate 9: Launch new client campaign
- **Trigger:** Any new ad campaign, outreach sequence, or content push
- **Approver:** Strategist
- **SLA:** <24h
- **Why:** First impression with new audience, budget exposure

## Gate 10: Declare incident
- **Trigger:** Any anomaly Atlas escalates
- **Approver:** Strategist (or Founder if unavailable)
- **SLA:** 1 hour
- **Why:** Rapid response prevents S2 → S1 escalation

## Override policy
- **NO OVERRIDE.** These gates cannot be bypassed programmatically.
- To temporarily disable a gate (e.g., for testing), the founder must:
  1. Edit this playbook in Git
  2. Set `gate_status: disabled` with expiry date
  3. Commit with `[founder]: disabled Gate X for testing until YYYY-MM-DD`
- MarTech Integration Agent auto-re-enables gates on expiry date

## Audit
- All HITL approvals logged in `11-Ops/agent-logs/atlas/` with approver, timestamp, artifact link
- Quarterly audit by Compliance Agent: were any gates bypassed? If yes, incident report.
