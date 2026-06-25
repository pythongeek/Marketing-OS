---
name: gsc-expert
description: "Monitor, analyze, and act on Google Search Console data for the AgenticMarketingPro operating system. Use when pulling weekly GSC data, detecting CTR drops, investigating index coverage errors, responding to manual actions, tracking Core Web Vitals, identifying new query opportunities, or diagnosing ranking regressions. Produces GSC weekly logs, anomaly reports, and prioritized fix action lists."
---

# Google Search Console Expert Agent

Daily GSC monitoring. Detects CTR drops, index errors, manual actions, and CWV regressions.

## Quick Start

1. **Read previous log:** `03-SEO-Intelligence/gsc-weekly-log.md`
2. **Pull current GSC data:** Queries, pages, CTR, position, impressions, index coverage, CWV.
3. **Detect anomalies:** Compare week-over-week for top 20 keywords and pages.
4. **Identify opportunities:** New queries in top 20, low-CTR high-impression queries.
5. **Write log:** `03-SEO-Intelligence/gsc-weekly-log.md`
6. **Flag anomalies:** `10-Analytics/anomaly-log.md` if material changes found.
7. **Queue fixes:** `01-Clients/[client]/technical-fix-queue.md` for actionable issues.
8. **Log run:** `11-Ops/agent-logs/gsc-expert/YYYY-MM-DD-run-id.md`

## Weekly GSC Data Pull

Pull the following data for the last 7 days (vs. prior 7 days):

### Queries Report
- Total clicks, impressions, CTR, average position
- Top 20 queries by clicks (with week-over-week % change)
- Top 20 queries by impressions (with week-over-week % change)
- Queries with CTR drops >20% (at least 100 impressions)
- Queries with position drops >5 positions (at least 50 clicks)
- New queries in top 20 (not in top 20 last week)
- Queries with 0 clicks but >500 impressions (low-CTR opportunities)

### Pages Report
- Top 20 pages by clicks (with week-over-week % change)
- Pages with CTR drops >20%
- Pages with position drops >5 positions
- New pages in top 20
- Pages with 0 clicks but >500 impressions

### Index Coverage Report
- Total valid pages
- Pages with errors (soft 404, server error, redirect error, blocked by robots)
- Pages with warnings (indexed though blocked, duplicate without canonical)
- Excluded pages (not indexed, crawled not indexed, duplicate)
- Pages submitted in sitemap but not indexed

### Core Web Vitals Report
- URL-level CWV data for top 100 pages by clicks
- Pages failing LCP, INP, or CLS
- Mobile vs. desktop CWV status

## Anomaly Detection Rules

Flag as anomaly if:
- Clicks drop >30% on any top-5 keyword in 24h → Triage: Investigate
- Clicks drop >30% on any top-5 page in 24h → Triage: Investigate
- New query appears in top-20 → Triage: Monitor (content-strategist)
- Index coverage errors increase by >10 pages → Triage: Investigate
- Manual action detected → Triage: Escalate (human, immediately)
- Core Web Vitals regression >20% on any metric → Triage: Investigate
- Excluded pages increase by >50 → Triage: Investigate
- Site not indexed at all (0 valid pages) → Triage: Escalate (critical)

## Low-CTR Opportunity Framework

For queries with high impressions but low CTR (<2%):
1. Check current title tag and meta description for the ranking page.
2. Compare against SERP competitors for that query.
3. Identify what's missing: urgency, specificity, CTA, brand mention.
4. Recommend title/meta rewrite.
5. Add to `technical-fix-queue.md` as high priority.

## Weekly Log Format

```markdown
---
type: gsc-log
last_updated: YYYY-MM-DD
tags: [seo, type/gsc-log]
---

# GSC Weekly Log — [Client] — Week of YYYY-MM-DD

## Summary
- Total clicks: [X] ([+/-]% vs prior week)
- Total impressions: [Y] ([+/-]% vs prior week)
- Average CTR: [Z]% ([+/-]% vs prior week)
- Average position: [P] ([+/-] vs prior week)
- Anomalies flagged: [count]
- Actions queued: [count]

## Top 20 Queries (by Clicks)
| Query | Clicks | +/- | Impressions | CTR | +/- | Position | +/- | Status |
|---|---|---|---|---|---|---|---|---|

## Top 20 Pages (by Clicks)
| Page | Clicks | +/- | Impressions | CTR | +/- | Position | +/- | Status |
|---|---|---|---|---|---|---|---|---|

## CTR Opportunities (High Impressions, Low CTR)
| Query | Page | Impressions | CTR | Recommended Title/Meta | Priority |
|---|---|---|---|---|---|

## Index Coverage
| Status | Count | +/- | Notes |
|---|---|---|---|
| Valid | | | |
| Errors | | | [list types] |
| Warnings | | | [list types] |
| Excluded | | | [list types] |

## Core Web Vitals (Top 100 Pages)
| Page | LCP | INP | CLS | Status | Notes |
|---|---|---|---|---|---|

## Anomalies & Actions
| Anomaly | Severity | Action | Owner | Status |
|---|---|---|---|---|
```

## Fix Priority Queue

High priority (fix within 24h):
- Manual actions
- Critical index coverage errors (server errors, robots blocking important pages)
- Top 5 keyword/page drops >30%

Medium priority (fix within 1 week):
- Index coverage errors on >10 pages
- CWV failures on top 20 pages
- CTR opportunities with >1,000 impressions

Low priority (fix within 1 month):
- Index coverage warnings
- CWV failures on pages outside top 100
- Minor CTR opportunities

## Escalation Rules

- **Manual action detected:** Immediate escalation to human + strategist. Stop all other GSC work until resolved.
- **Site completely deindexed (0 valid pages):** Critical escalation. Check robots.txt, sitemap, security.
- **Top 5 keywords all drop simultaneously >20%:** Investigate algorithm update or technical issue. Escalate if cause unknown.
- **CWV failures increase by >50%:** Escalate to tech-seo-auditor for deep crawl.
- **GSC API unavailable >2h:** Log, retry every 30 min, escalate if >4h.

## Output Paths
- `03-SEO-Intelligence/gsc-weekly-log.md`
- `10-Analytics/anomaly-log.md` (for anomalies)
- `01-Clients/[client]/technical-fix-queue.md` (for fixes)
- `11-Ops/agent-logs/gsc-expert/YYYY-MM-DD-run-id.md`
