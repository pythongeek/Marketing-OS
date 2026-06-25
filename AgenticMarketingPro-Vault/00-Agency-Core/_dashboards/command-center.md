---
type: dashboard
title: Agency Command Center
last_updated: DYNAMIC
tags: [dashboard, ops]
---

# 🎯 Agency Command Center

> Live view of agency state. Refreshes on every vault change.

## Active Clients
```dataview
TABLE WITHOUT ID
  file.link AS "Client",
  mrr AS "MRR",
  status AS "Status",
  last_reviewed AS "Last Review"
FROM "01-Clients"
WHERE type = "client" AND status = "active"
SORT mrr DESC
```

## MRR Summary
```dataview
TABLE
  sum(rows.mrr) AS "Total MRR",
  length(rows) AS "Active Clients",
  round(sum(rows.mrr) / length(rows), 0) AS "Avg Retainer"
FROM "01-Clients"
WHERE type = "client" AND status = "active"
GROUP BY 1
```

## Today's Open Agent Tasks
```dataview
TABLE WITHOUT ID
  agent AS "Agent",
  task AS "Task",
  priority AS "Priority",
  due_date AS "Due"
FROM "11-Ops/agent-task-queue.md"
WHERE status != "done"
SORT priority ASC, due_date ASC
LIMIT 15
```

## Recent Anomalies (last 7 days)
```dataview
TABLE WITHOUT ID
  severity AS "Severity",
  source AS "Source",
  description AS "Anomaly",
  status AS "Status",
  date AS "When"
FROM "10-Analytics/anomaly-log.md"
WHERE date >= date(today) - dur(7 days)
SORT date DESC
LIMIT 10
```

## Agent Performance This Week
```dataview
TABLE WITHOUT ID
  agent AS "Agent",
  count(file) AS "Runs",
  sum(cost_usd) AS "Cost",
  length(filter(file, (x) => x.status = "success")) / count(file) * 100 AS "Success %"
FROM "11-Ops/agent-logs"
WHERE timestamp >= date(today) - dur(7 days)
GROUP BY agent
SORT cost_usd DESC
```
