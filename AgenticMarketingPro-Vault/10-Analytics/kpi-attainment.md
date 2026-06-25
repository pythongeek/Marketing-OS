---
type: kpi-dashboard
last_updated: DYNAMIC
tags: [analytics, type/kpi-dashboard]
---

# KPI Attainment Dashboard

> Live KPI tracker. Refreshes from individual KPI notes across `01-Clients/`.

## Current month attainment
```dataview
TABLE WITHOUT ID
  client AS "Client",
  kpi AS "KPI",
  target AS "Target",
  actual AS "Actual",
  attainment_pct AS "%",
  status AS "Status"
FROM "01-Clients"
WHERE type = "kpi" AND period = "2026-01"
SORT client ASC, attainment_pct ASC
```

## Below-target KPIs (action needed)
```dataview
TABLE WITHOUT ID
  client AS "Client",
  kpi AS "KPI",
  attainment_pct AS "%",
  notes AS "Notes"
FROM "01-Clients"
WHERE type = "kpi" AND attainment_pct < 90
SORT attainment_pct ASC
```

## KPI trend (last 6 months)
| Client | KPI | M-5 | M-4 | M-3 | M-2 | M-1 | Current | Trend |
|---|---|---|---|---|---|---|---|---|
| | | | | | | | | |
