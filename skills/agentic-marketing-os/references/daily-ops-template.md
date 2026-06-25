# Daily Ops Log Template

Use this template when writing the daily ops log to `11-Ops/daily-ops-log.md`.

```markdown
---
type: daily-ops-log
last_updated: YYYY-MM-DD
tags: [ops, type/daily-ops]
---

# Daily Ops Log — YYYY-MM-DD

## Summary
- [ ] Morning loop completed
- [ ] Afternoon check completed
- [ ] Evening wrap completed
- Anomalies flagged: [count]
- HITL gates pending: [count]
- Total agent runs: [count]
- Total cost (USD): $[amount]

## Step-by-Step Log

### 1. Site Health Check
- Status: [pass / issues found]
- Issues: [list or "none"]
- Agent dispatched: [agent name or "none"]

### 2. GSC / Bing Monitoring
- GSC status: [normal / anomalies]
- Bing status: [normal / anomalies]
- Actions taken: [list]

### 3. Content Brief Generation
- Briefs generated: [count]
- Briefs written to: [file paths]

### 4. Writer Assignment
- Assigned: [count] briefs
- Writers: [persona names]

### 5. On-Page Review
- Pages reviewed: [count]
- Fixes queued: [count]

### 6. Social Repurposing
- Pieces repurposed: [count]
- Formats generated: [list]

### 7. Outreach Queue
- Prospects reviewed: [count]
- Emails drafted: [count]
- HITL Gate 2: [pending / approved / N/A]

### 8. Analytics Digest
- Key metric: [one sentence takeaway]
- Digest written to: [path or "N/A (not Monday)"]

### 9. Profit Plan Update
- MRR: $[amount]
- OPEX: $[amount]
- Margin: [pct]%
- Alerts: [list or "none"]

## Anomalies (Open)
| Severity | Source | Description | Status | Owner |
|---|---|---|---|---|

## HITL Gates (Pending Approval)
| Gate | What | Risk | Recommended Action | Status |
|---|---|---|---|---|

## Tomorrow's Queue
1. [Task 1]
2. [Task 2]
3. [Task 3]

## Notes
[Anything else worth capturing]
```

## Cost Tracking

Log cost per agent run in the step where it occurred. Format:
- Agent: [name]
- Run ID: [YYYY-MM-DD-###]
- Cost: $[amount]
- Tokens: [input] in / [output] out
- Latency: [seconds]
