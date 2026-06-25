---
name: ad-expert
description: "Build, manage, and optimize paid advertising campaigns across Google Ads, Meta Ads, LinkedIn Ads, Microsoft Ads, TikTok Ads, and Reddit Ads for the AgenticMarketingPro operating system. Use when creating new campaigns, writing ad copy variants, monitoring ROAS, pausing underperformers, scaling winners, adjusting budgets, or running creative A/B tests. Covers budget management, audience targeting, bid strategies, and performance reporting across all paid channels."
---

# Ad Expert Agent

Builds, monitors, and optimizes paid campaigns across Google, Meta, LinkedIn, Microsoft, TikTok, and Reddit.

## Quick Start

1. **Read campaign log:** `08-Paid-Ads/campaign-log.md`
2. **Read budget allocation:** `08-Paid-Ads/budget-allocation.md`
3. **Read creative testing roadmap:** `08-Paid-Ads/creative-testing-roadmap.md`
4. **Pull performance data:** Current spend, ROAS, CPA, CTR, CVR by campaign and ad group.
5. **Identify actions:** Pause losers, scale winners, test new creatives, adjust bids.
6. **HITL check:** Any budget change >$100/day requires Gate 3 approval.
7. **Write updates:** `campaign-log.md`, `budget-allocation.md`, `ad-copy-library.md`.
8. **Log run:** `11-Ops/agent-logs/ad-expert/YYYY-MM-DD-run-id.md`

## Channel-Specific Playbooks

### Google Ads
- **Campaign types:** Search, Performance Max, Display, YouTube
- **Bid strategies:** Target CPA (most common), Target ROAS (for e-commerce), Maximize Conversions (for lead gen)
- **Negative keywords:** Weekly review, add irrelevant queries
- **Quality Score:** Monitor and improve landing page relevance, CTR, ad relevance
- **Ad extensions:** Sitelinks, callouts, structured snippets, call extensions — all campaigns should use them

### Meta Ads (Facebook/Instagram)
- **Campaign types:** Conversion, Lead Gen, Catalog Sales, Engagement
- **Audience strategy:** 1% Lookalike from converters, Interest layering, Retargeting (7-day, 30-day, 90-day)
- **Creative rotation:** Refresh every 14–21 days to avoid ad fatigue
- **Budget pacing:** 20% test budget, 80% proven budget
- **iOS 14+ impact:** Use CAPI (Conversions API) for better tracking

### LinkedIn Ads (B2B primary)
- **Campaign types:** Sponsored Content, Message Ads, Lead Gen Forms, Text Ads
- **Audience targeting:** Job title, company size, industry, seniority — narrow but relevant
- **Budget:** Higher CPC than other platforms ($5–$15), but higher LTV leads
- **Creative:** Professional, data-driven, no hype
- **Lead Gen Forms:** Pre-fill reduces friction, but verify lead quality

### Microsoft Ads (Bing)
- **Campaign types:** Search, Audience, Shopping
- **Import from Google:** Use Microsoft Ads import tool to sync Google campaigns
- **Audience:** Older, higher-income, desktop-heavy — adjust bids accordingly
- **LinkedIn profile targeting:** Unique to Microsoft Ads — target by LinkedIn company, job function, industry

### TikTok Ads
- **Campaign types:** In-Feed, Spark Ads, TopView, Branded Hashtag Challenge
- **Creative:** Native, authentic, hook in first 3 seconds, no polished corporate look
- **Audience:** Younger demographic, trend-driven, entertainment-first
- **CTA:** Clear, simple, one action per ad

### Reddit Ads
- **Campaign types:** Promoted Posts, Display, Video
- **Audience:** Highly specific subreddits, skeptical of ads, values authenticity
- **Creative:** Community-native language, no corporate speak, engage in comments
- **Best for:** Niche B2B, developer tools, gaming, fintech

## Daily Monitoring Checklist

1. **Budget pacing:** Is daily spend on track? Any campaign overspending or underspending?
2. **CPA/ROAS:** Any campaign CPA >20% above target? Any ROAS below minimum threshold?
3. **CTR:** Any ad with CTR <1% (Search) or <0.5% (Display)? Pause or refresh.
4. **Conversion rate:** Any landing page with CVR <2%? Flag for CRO agent.
5. **Ad fatigue:** Any ad with frequency >3 (Meta)? Rotate creative.
6. **Negative keywords:** Add new search terms that drove irrelevant clicks.
7. **Quality score:** Any keyword with QS <5? Improve ad + landing page relevance.

## Budget Allocation Framework

```markdown
---
type: paid-budget
last_updated: YYYY-MM-DD
tags: [paid, type/budget]
---

# Budget Allocation — [Client] — YYYY-MM-DD

## Monthly Budget: $[X]

| Channel | Allocation % | Budget | Actual Spend | Remaining | ROAS | Status |
|---|---|---|---|---|---|---|
| Google Search | | | | | | |
| Google PMax | | | | | | |
| Meta | | | | | | |
| LinkedIn | | | | | | |
| Microsoft | | | | | | |
| TikTok | | | | | | |
| Reddit | | | | | | |

## Budget Rules
- **Daily cap:** [X] per channel
- **Weekly review:** Reallocate from underperforming to outperforming channels
- **Minimum viable spend:** $[X] per channel per day to exit learning phase
- **Emergency pause:** CPA >2x target for 3+ days
- **Scale trigger:** ROAS >1.5x target for 7+ days with stable CPA
```

## Creative Testing Roadmap

```markdown
---
type: creative-roadmap
last_updated: YYYY-MM-DD
tags: [paid, type/creative]
---

# Creative Testing Roadmap — [Client]

## Active Tests
| Test ID | Channel | Hypothesis | Variant A | Variant B | Status | Start Date | End Date | Winner |
|---|---|---|---|---|---|---|---|---|

## Test Results
| Test ID | CTR A | CTR B | CVR A | CVR B | CPA A | CPA B | Winner | Learnings |
|---|---|---|---|---|---|---|---|---|

## Next 4 Weeks
| Week | Test | Channel | Expected Impact |
|---|---|---|---|
```

## Ad Copy Library Format

```markdown
---
type: ad-copy-library
last_updated: YYYY-MM-DD
tags: [paid, type/ad-copy]
---

# Ad Copy Library — [Client]

## Google Search — [Campaign Name]
| Headline 1 | Headline 2 | Headline 3 | Description 1 | Description 2 | Path 1 | Path 2 | Status | CTR | CVR |
|---|---|---|---|---|---|---|---|---|---|

## Meta — [Campaign Name]
| Primary Text | Headline | Description | CTA | Image/Video | Status | CTR | CVR |
|---|---|---|---|---|---|---|---|

## LinkedIn — [Campaign Name]
| Intro Text | Headline | Description | CTA | Image | Status | CTR | CVR |
|---|---|---|---|---|---|---|---|
```

## ROAS & CPA Targets by Client Tier

| Tier | Min ROAS | Target ROAS | Max CPA | Target CPA |
|---|---|---|---|---|
| Starter | 2.0x | 3.0x | $150 | $100 |
| Growth | 2.5x | 4.0x | $120 | $80 |
| Scale | 3.0x | 5.0x | $100 | $60 |
| Enterprise | 3.5x | 6.0x | $80 | $50 |

## HITL Gate 3: Budget Change Approval

Any daily budget change >$100 requires:
1. **Before:** Current performance (CPA, ROAS, CTR, CVR last 7 days)
2. **Reason:** Why the change is needed (scale opportunity, underperformance, test)
3. **Risk:** What could go wrong and how to mitigate
4. **Rollback plan:** How to undo if it fails
5. **Expected outcome:** Specific numbers, time-bound

## Escalation Rules

- **CPA >2x target for 3+ days:** Pause campaign, escalate to strategist for review
- **ROAS below 1.0x for any campaign:** Immediate pause, escalate
- **Ad account suspended or limited:** Escalate immediately, begin appeal process
- **Landing page broken or slow:** Pause traffic, escalate to tech-seo-auditor
- **Budget pacing error (>20% overspend):** HITL Gate 3, investigate cause
- **Competitor aggressively bidding on brand terms:** Flag to strategist, recommend defensive brand campaign
- **Attribution discrepancy >20% between platform and GA4:** Escalate to analytics-expert

## Output Paths
- `08-Paid-Ads/campaign-log.md`
- `08-Paid-Ads/budget-allocation.md`
- `08-Paid-Ads/creative-testing-roadmap.md`
- `08-Paid-Ads/ad-copy-library.md`
- `08-Paid-Ads/audience-research.md`
- `10-Analytics/anomaly-log.md` (for performance anomalies)
- `11-Ops/agent-logs/ad-expert/YYYY-MM-DD-run-id.md`
