# HITL Gates — The 10 Non-Negotiables

Enforced at the orchestration layer. Atlas cannot bypass these, even under direct human instruction.

## Gate 1: Publish Content
- **Trigger:** Any draft marked 'ready' in `04-Content-Production/`
- **Approver:** Strategist + QA Agent pass
- **SLA:** Same business day
- **Why:** Brand safety + factual accuracy + legal exposure

## Gate 2: Send Outreach Email
- **Trigger:** First 3 emails of any new outreach sequence
- **Approver:** Strategist
- **SLA:** <4h
- **Why:** Brand reputation + deliverability + personalization quality

## Gate 3: Change Ad Budget
- **Trigger:** Any daily budget change >$100
- **Approver:** Strategist + Finance
- **SLA:** <2h
- **Why:** Direct financial exposure + platform policy compliance

## Gate 4: Modify Site Technical Structure
- **Trigger:** Redirects, canonicals, robots.txt, server config changes
- **Approver:** Strategist + Developer
- **SLA:** <24h
- **Why:** Can cause deindexation, traffic loss, broken UX

## Gate 5: Publish pSEO Batch
- **Trigger:** Any batch >50 pages
- **Approver:** Strategist
- **SLA:** <4h
- **Why:** Risk of cannibalization, indexation budget waste, quality dilution

## Gate 6: Respond to Negative Review
- **Trigger:** Any review <3 stars
- **Approver:** Strategist
- **SLA:** <24h
- **Why:** Public-facing brand response, legal/PR risk

## Gate 7: Send Client Report
- **Trigger:** Any artifact going to a client (report, deck, email)
- **Approver:** Strategist + Atlas review
- **SLA:** Same business day
- **Why:** Client relationship, accuracy, brand voice

## Gate 8: Approve Agent Prompt Change
- **Trigger:** Any change to an agent's system prompt
- **Approver:** Architect + Strategist
- **SLA:** Weekly Monday review
- **Why:** Prompt changes affect all downstream output quality

## Gate 9: Launch New Client Campaign
- **Trigger:** Any new ad campaign, outreach sequence, or content push
- **Approver:** Strategist
- **SLA:** <24h
- **Why:** First impression with new audience, budget exposure

## Gate 10: Declare Incident
- **Trigger:** Any anomaly Atlas escalates
- **Approver:** Strategist (or Founder if unavailable)
- **SLA:** 1 hour
- **Why:** Rapid response prevents S2 → S1 escalation

## Override Policy
- **NO OVERRIDE.** These gates cannot be bypassed programmatically.
- To temporarily disable a gate (e.g., for testing), the founder must:
  1. Edit this playbook in Git
  2. Set `gate_status: disabled` with expiry date
  3. Commit with `[founder]: disabled Gate X for testing until YYYY-MM-DD`
- MarTech Integration Agent auto-re-enables gates on expiry date

## Audit
- All HITL approvals logged in `11-Ops/agent-logs/atlas/` with approver, timestamp, artifact link
- Quarterly audit by Compliance Agent: were any gates bypassed?
