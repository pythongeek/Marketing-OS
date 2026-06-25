---
name: competitor-intel
description: "Monitor competitors continuously across SEO, content, backlinks, paid ads, team hiring, and product announcements for the AgenticMarketingPro operating system. Use when tracking competitor keyword movements, analyzing new competitor content, auditing competitor backlink profiles, mapping competitor paid strategy, detecting competitor team changes or funding rounds, or updating the competitor intelligence map in the vault. Produces structured competitor reports that feed into the agency's strategic positioning and client recommendations."
---

# Competitor Intelligence Agent

Continuously monitors 3–5 named competitors per client. Tracks keyword movements, new content, backlinks, ad changes, team/hiring signals, product/funding announcements.

## Quick Start

1. **Read competitor list:** `02-Competitors/competitor-map.md`
2. **Read per-client watch:** `01-Clients/[client]/competitor-watch.md`
3. **Select target:** Choose 1–3 competitors for deep analysis this run.
4. **Execute analysis:** Run the appropriate workflow (keyword gaps, content audit, backlink profile, paid strategy, team signals).
5. **Write output:** `02-Competitors/[name]/[analysis-type].md`
6. **Update anomaly log:** If material changes detected, write to `10-Analytics/anomaly-log.md`.
7. **Log run:** `11-Ops/agent-logs/competitor-intel/YYYY-MM-DD-run-id.md`

## Workflows

### Workflow A: Keyword Gap Analysis

**When:** Weekly (Monday) or on-demand for new competitor

**Steps:**
1. Read `03-SEO-Intelligence/keyword-universe.md` for client's target keywords.
2. Read competitor's known ranking keywords from `02-Competitors/[name]/keyword-gaps.md` (previous run).
3. Identify keywords where competitor ranks but client does not (or competitor ranks higher).
4. Categorize gaps by: high volume + low KD, commercial intent, branded vs. non-branded.
5. Write updated `02-Competitors/[name]/keyword-gaps.md` with:
   - New gaps found this week
   - Gaps closed (client now ranking)
   - Priority score (volume × intent × difficulty)
   - Recommended action per gap

**Output format:**
```markdown
---
type: competitor-keyword-gaps
competitor: [name]
last_updated: YYYY-MM-DD
tags: [competitor/[name], priority/[high|medium|low]]
---

# Keyword Gaps — [Competitor]

## New gaps (this run)
| Keyword | Volume | KD | Comp Rank | Client Rank | Gap | Intent | Priority | Action |
|---|---|---|---|---|---|---|---|---|

## Closed gaps (client now ranking)
| Keyword | Previous Gap | Current Client Rank | Notes |
|---|---|---|---|

## Top 10 opportunities
[Ranked list with recommended content type and timeline]
```

### Workflow B: Content Audit

**When:** Weekly or when competitor publishes 3+ new pages in 7 days

**Steps:**
1. Scan competitor's blog/resources for new content in last 7 days.
2. For each new piece: title, publish date, content type, target keyword (if detectable), word count, quality assessment.
3. Compare against client's content on same/similar topics.
4. Identify content opportunities: topics competitor covers that client doesn't, or where client's coverage is thinner.
5. Write `02-Competitors/[name]/content-audit.md`.

**Output format:**
```markdown
---
type: competitor-content
competitor: [name]
last_updated: YYYY-MM-DD
tags: [competitor/[name], type/content-audit]
---

# Content Audit — [Competitor]

## New content (last 7 days)
| Title | URL | Date | Type | Target KW | Words | Quality | Our Response |
|---|---|---|---|---|---|---|---|

## Content gaps vs. our coverage
| Topic | Their Coverage | Our Coverage | Gap | Priority |
|---|---|---|---|---|

## Content velocity
- Their rate: [X pieces/week]
- Our rate: [Y pieces/week]
- Recommendation: [adjustment needed / maintain]
```

### Workflow C: Backlink Profile

**When:** Bi-weekly or monthly depending on competitor tier

**Steps:**
1. Profile competitor's referring domains: total count, DR distribution, anchor text distribution.
2. Identify new backlinks acquired since last run.
3. Identify lost backlinks.
4. Flag high-value links that could be replicated (same source, similar content angle).
5. Write `02-Competitors/[name]/backlink-profile.md`.

**Output format:**
```markdown
---
type: competitor-backlinks
competitor: [name]
last_updated: YYYY-MM-DD
tags: [competitor/[name], type/backlinks]
---

# Backlink Profile — [Competitor]

## Overview
- Total referring domains: [count]
- DR distribution: [breakdown]
- New (last 30 days): [count]
- Lost (last 30 days): [count]

## New links (replicable?)
| Source | DR | URL | Anchor | Replicable? | How |
|---|---|---|---|---|---|

## Lost links
| Source | DR | Reason | Opportunity for us? |
|---|---|---|---|
```

### Workflow D: Paid Strategy Signals

**When:** Monthly or when competitor ad spend changes detected

**Steps:**
1. Collect competitor ad copy, landing page URLs, offers from ad libraries (Meta Ad Library, Google Ads Transparency).
2. Note changes in messaging, offers, CTAs, landing page design.
3. Estimate ad spend trends if data available (SimilarWeb, SpyFu).
4. Write `02-Competitors/[name]/paid-strategy.md`.

### Workflow E: Team & Hiring Signals

**When:** Monthly or when major announcement detected

**Steps:**
1. Monitor LinkedIn, Crunchbase, company careers page for: new hires, departures, funding rounds, product launches.
2. Correlate hiring patterns with strategy shifts (e.g., hiring 5 sales reps = likely entering new market).
3. Write `02-Competitors/[name]/team-and-hiring.md`.

## Anomaly Detection

Flag as anomaly in `10-Analytics/anomaly-log.md` if:
- Competitor publishes 5+ pages in 24h → Monitor
- Competitor raises funding round → Escalate
- Competitor's top-ranking page drops out of top 10 → Investigate
- Competitor launches new product category → Escalate
- Competitor's backlink velocity spikes >2x → Investigate

## Escalation Rules

- **Material competitor move** (new product page, funding round, executive hire): page strategist within 2h
- **>3 anomalies on single competitor in 24h:** same-day review
- **Competitor launches direct attack on client's positioning:** immediate escalation

## Output Paths
- `02-Competitors/[name]/keyword-gaps.md`
- `02-Competitors/[name]/content-audit.md`
- `02-Competitors/[name]/backlink-profile.md`
- `02-Competitors/[name]/paid-strategy.md`
- `02-Competitors/[name]/team-and-hiring.md`
- `10-Analytics/anomaly-log.md` (for anomalies)
- `11-Ops/agent-logs/competitor-intel/YYYY-MM-DD-run-id.md`
