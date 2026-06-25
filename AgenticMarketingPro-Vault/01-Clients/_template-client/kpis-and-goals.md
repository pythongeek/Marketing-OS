---
type: client-kpis
client: TEMPLATE
status: template
last_updated: 2026-01-20
tags: [client/template, type/kpis]
---

# KPIs & Goals — [Client Name]

## North Star metric
[North Star — e.g., "Qualified pipeline generated from organic + paid channels"]

## 90-day targets
| KPI | Baseline | 90-day target | Source | Cadence |
|---|---|---|---|---|
| Organic traffic (sessions/mo) | ___ | +25% | GA4 | Weekly |
| Branded search volume | ___ | +15% | GSC | Weekly |
| Non-branded keyword rankings (top-10) | ___ | +20 | Ahrefs | Weekly |
| AEO citation rate (% of tracked queries) | ___ | +50% | Profound | Weekly |
| Referring domains | ___ | +15% | Ahrefs | Weekly |
| Lead-to-MQL conversion rate | ___ | +10% | HubSpot | Monthly |
| MQLs from organic | ___ | +30% | HubSpot | Monthly |
| Email deliverability (inbox %) | ___ | ≥98% | Postmark | Weekly |
| Paid ROAS (if applicable) | ___ | Per tier | Platform | Weekly |
| NPS (if measured) | ___ | +10 | Client survey | Quarterly |

## KPI definitions
> Every KPI must have an unambiguous definition. Define here, not in Slack threads.

### Organic traffic
GA4 sessions where `sessionDefaultChannelGroup = "Organic Search"`. Excludes branded paid campaigns.

### Branded search volume
GSC impressions on queries containing the brand name (and approved variants). Rolling 28-day average.

### AEO citation rate
% of 50 tracked queries where the client's brand is cited by at least one of: ChatGPT, Perplexity, Claude, Gemini, Copilot. Tracked weekly via Profound.

## KPI owners
| KPI | Owner (agent) | Human reviewer |
|---|---|---|
| Organic traffic | On-Page + Content Strategist | Strategist |
| Branded search | AEO/GEO + Content | Strategist |
| AEO citation rate | AEO/GEO Specialist | Strategist |
| Referring domains | Off-Page Strategist | Strategist |
| Lead conversion | CRO + Analytics Expert | Strategist |
| Email deliverability | Email/Lifecycle | Strategist |
| Paid ROAS | Ad Expert | Strategist + Finance |

## KPI review cadence
- **Weekly (Monday 10:00):** Atlas produces KPI snapshot in `weekly-digest.md`
- **Monthly (1st):** Reporting Agent produces full client report with KPI trend
- **Quarterly:** QBR deck with KPI deep dive + 90-day reforecast
