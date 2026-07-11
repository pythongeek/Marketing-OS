---
type: content-strategist
client: agenticmarketingpro
job_id: 3bf9dae0-0f76-4051-9516-5e92a87c8b94
generated_at: 2026-07-11T18:58:46.769677+00:00
source: sync-from-db
---

# Content Refresh Standard Operating Procedure (SOP)

**Document ID:** AMP-SOP-CONT-002
**Version:** 1.0
**Effective Date:** Q1 2025
**Owner:** Content Strategy Lead, AgenticMarketingPro
**Review Cycle:** Quarterly
**Approval:** Head of Content & SEO

---

## 1. Purpose & Scope

### 1.1 Purpose
This SOP establishes a standardized, repeatable process for identifying, prioritizing, executing, and measuring content refresh activities to prevent organic content decay, recover lost rankings, and maximize the ROI of existing client content assets.

### 1.2 Scope
Applies to all client-owned blog content, landing pages, pillar pages, and resource articles managed by AgenticMarketingPro under monthly retainer or project-based SEO engagements.

### 1.3 Objectives
- Maintain or improve organic traffic to existing content by ≥ 10% post-refresh
- Recover rankings for target keywords that have slipped (positions 4–20)
- Extend content lifecycle by 12+ months per refresh
- Reduce client CAC by leveraging owned assets before creating new content

---

## 2. Quarterly Content Audit Process

### 2.1 Audit Cadence
| Activity | Frequency | Owner | Duration |
|---|---|---|---|
| Full content inventory export | Quarterly | SEO Analyst | Day 1 |
| Performance data pull | Quarterly | SEO Analyst | Day 1–2 |
| Decay signal analysis | Quarterly | Content Strategist | Day 2–3 |
| Prioritization workshop | Quarterly | Content Lead + AM | Day 3 |
| Refresh queue creation | Quarterly | Content Strategist | Day 4 |
| Client review & approval | Quarterly | Account Manager | Day 5 |

### 2.2 Audit Steps

**Step 1 — Inventory & Data Pull**
- Export all indexed URLs from Google Search Console (last 90 days)
- Pull organic traffic, conversions, and engagement data from GA4
- Cross-reference with target keyword mapping sheet
- Note publication date, last updated date, content type, and target persona

**Step 2 — Performance Tiering**
Classify each URL into one of four tiers:

| Tier | Definition | Action Required |
|---|---|---|
| 🟢 **Healthy** | Traffic stable or growing; ranking position 1–10 | Light monitoring only |
| 🟡 **Watch** | Traffic -10% to -20% OR position 11–20 | Add to watchlist |
| 🟠 **Decaying** | Traffic -20% to -50% OR position dropped 5+ spots | Priority refresh candidate |
| 🔴 **Critical** | Traffic -50%+ OR lost top 20 entirely | Urgent refresh or retirement |

**Step 3 — Qualitative Assessment**
- Check for outdated statistics, broken links, deprecated tools mentioned
- Review E-E-A-T signals (author bios, sources, experience markers)
- Assess content depth vs. current top-ranking competitors
- Identify opportunities for new sections, visuals, or schema

**Step 4 — Audit Report**
Compile findings into the standard audit deck (template in Section 9).

---

## 3. Decay Detection Signals & Metrics

### 3.1 Primary Decay Signals

| Signal | Source | Threshold | Severity |
|---|---|---|---|
| Organic sessions decline | GA4 | > 15% drop over 90 days vs. prior period | High |
| Average position drop | GSC | > 3 positions for primary keyword | High |
| Click-through rate decline | GSC | > 20% drop with stable impressions | Medium |
| Impressions decline | GSC | > 25% drop over 90 days | High |
| Bounce rate increase | GA4 | > 10% absolute increase | Medium |
| Avg. engagement time decrease | GA4 | > 30% drop | Medium |
| Conversions decline | GA4 | > 20% drop | Critical |
| Featured snippet loss | Manual / Ahrefs | Lost within last 60 days | Medium |
| Outranked by new competitor | Ahrefs / SEMrush | New competitor in top 3 within 90 days | Medium |

### 3.2 Content Quality Signals (Manual Review)

- [ ] Statistics older than 24 months
- [ ] Outdated product/feature references
- [ ] Broken internal or external links
- [ ] Missing or thin author bio
- [ ] No original imagery (all stock)
- [ ] Word count < 75% of current SERP average
- [ ] Lacks FAQ section or schema markup
- [ ] No clear CTA or conversion path
- [ ] Heading structure (H1-H3) is illogical
- [ ] Content does not address People Also Ask queries

### 3.3 Automated Monitoring Setup
Configure **ContentKing** or **Ahrefs Content Audit** to monitor all priority URLs with weekly email alerts for:
- Ranking drops > 3 positions
- Traffic drops > 20%
- New technical errors
- Content changes detected on SERP competitors

---

## 4. Refresh Priority Matrix

### 4.1 Prioritization Framework
Score each decaying URL on **Impact Potential** (1–5) and **Refresh Effort** (1–5).

```
                    HIGH IMPACT
                         |
            QUICK WIN    |    MAJOR PROJECT
        (Do First)       |    (Schedule Carefully)
   ──────────────────────┼───────────────────── EFFORT →
         MAINTAIN        |    DEPRIORITIZE
        (Light Updates)  |    (Sunset or Combine)
                         |
                    LOW IMPACT
```

### 4.2 Scoring Criteria

**Impact Potential (1–5):**
- Historical traffic volume
- Commercial value of target keywords
- Conversion history
- Strategic importance to client funnel

**Effort (1–5):**
- Word count gap to competitors
- Number of new sections required
- Need for new visuals or SME interviews
- Technical fixes required

### 4.3 Priority Queue Output
Maintain a rolling **Refresh Queue** in the project management tool:

| Priority | URL | Decay Signal | Impact | Effort | Owner | Deadline |
|---|---|---|---|---|---|---|
| P1 | /blog/example | Traffic -45% | 5 | 2 | Writer A | 2 weeks |
| P2 | /guide/example | Position drop | 4 | 3 | Writer B | 3 weeks |

**Monthly target:** Complete 4–8 refreshes per active client, balanced between quick wins and major overhauls.

---

## 5. Step-by-Step Refresh Workflow

### 5.1 Phase 1: Pre-Refresh Briefing (Day 1)
1. Content Strategist assigns refresh from priority queue
2. Pull competitive SERP analysis for target keywords (top 5 ranking pages)
3. Identify content gaps using **Surfer SEO** or **MarketMuse**
4. Update the brief with: target keywords, new sections required, link targets, conversion goals
5. Brief writer via standard refresh brief template

### 5.2 Phase 2: Research & Content Update (Days 2–5)
1. Writer conducts fresh research — new stats, examples, expert quotes
2. Update introduction with current year context and stronger hook
3. Add or expand sections addressing new search intent
4. Replace outdated visuals; create new custom imagery
5. Add FAQ section with People Also Ask questions
6. Strengthen internal linking to pillar pages and recent posts
7. Update or add CTAs aligned with current funnel stage
8. Refresh meta title, meta description, and URL slug (if redirecting)

### 5.3 Phase 3: SEO & Technical Polish (Day 6)
1. Run through SEO checklist (see Section 7)
2. Add or update schema markup (Article, FAQ, HowTo, Product as relevant)
3. Compress images and update alt text
4. Verify mobile rendering and Core Web Vitals
5. Set up 301 redirects for any moved URLs
6. Update internal links pointing to old URL

### 5.4 Phase 4: QA & Approval (Day 7)
1. Content Strategist review — quality, brand voice, completeness
2. SEO Analyst review — keyword optimization, technical elements
3. Account Manager submits to client for approval (if required by contract)
4. Final edits incorporated

### 5.5 Phase 5: Publish & Monitor (Day 8+)
1. Publish updates with new "Last Updated" date visible
2. Submit URL to Google Search Console for re-indexing
3. Promote via client channels (email, social) for traffic boost
4. Tag URL in ContentKing for ongoing monitoring
5. Schedule 30/60/90-day performance review

---

## 6. Content Update Checklist

### 6.1 Pre-Publish Checklist

**Content Quality**
- [ ] Headline is compelling and includes primary keyword
- [ ] Introduction hooks reader in first 2 sentences
- [ ] All statistics are from the last 18 months
- [ ] At least 3 original insights, examples, or data points
- [ ] Tone matches brand voice guide
- [ ] Grammar and spelling verified with Grammarly

**SEO Fundamentals**
- [ ] Primary keyword in H1, first 100 words, and meta title
- [ ] 2–3 secondary keywords naturally integrated
- [ ] Meta title ≤ 60 characters; meta description ≤ 155 characters
- [ ] URL slug is clean, short, keyword-rich
- [ ] Image alt text descriptive and keyword-relevant
- [ ] Internal links: 3–5 contextual links to related content
- [ ] External links: 2–3 to authoritative sources

**Technical & Schema**
- [ ] FAQ schema added (if FAQ section present)
- [ ] Article schema verified via Schema.org validator
- [ ] Open Graph and Twitter Card meta tags present
- [ ] Canonical URL set correctly
- [ ] Images compressed (WebP format, lazy-loaded below fold)

**Conversion & UX**
- [ ] CTA present and aligned with funnel stage
- [ ] Mobile layout tested
- [ ] Table of contents for posts > 2,000 words
- [ ] Readability score at grade level appropriate for audience
- [ ] Author bio with credentials and headshot visible

---

## 7. Before/After Measurement Framework

### 7.1 Baseline Metrics (Capture at Refresh Kickoff)
Record in the Refresh Tracking Sheet:

| Metric | Value | Source |
|---|---|---|
| Organic sessions (last 90 days) | ___ | GA4 |
| Primary keyword position | ___ | Ahrefs |
| Backlinks count | ___ | Ahrefs |
| Conversions (last 90 days) | ___ | GA4 |
| Bounce rate | ___ | GA4 |
| Avg. engagement time | ___ | GA4 |
| Word count | ___ | Manual |
| Last updated date | ___ | Manual |

### 7.2 Post-Refresh Measurement Windows
- **Day 30:** Quick sanity check — ensure indexing and no immediate regressions
- **Day 60:** Initial trend assessment — traffic and position changes
- **Day 90:** Full impact evaluation — compare all baseline metrics

### 7.3 Success Criteria
| Outcome | Definition |
|---|---|
| 🟢 **Major Win** | Traffic +25% AND position improved by 3+ spots |
| 🟢 **Win** | Traffic +10% OR position improved by 2+ spots |
| 🟡 **Neutral** | Traffic within ±10%, position stable |
| 🟠 **Underperform** | Traffic -10% to -25% post-refresh |
| 🔴 **Failed** | Traffic -25%+ post-refresh (requires root cause analysis) |

### 7.4 Iteration Protocol
- Failed refreshes trigger a post-mortem within 14 days
- Capture learnings in the Content Refresh Playbook
- If three consecutive refreshes underperform on a specific URL, recommend content retirement and merger into a new comprehensive asset

---

## 8. Tools & Resources

### 8.1 Required Tools

| Category | Primary Tool | Backup Option | Purpose |
|---|---|---|---|
| Analytics | Google Analytics 4 | — | Traffic, engagement, conversions |
| Search Performance | Google Search Console | — | Impressions, CTR, queries |
| SEO Suite | Ahrefs | SEMrush | Rankings, backlinks, content gaps |
| Content Optimization | Surfer SEO | Clearscope | On-page optimization scoring |
| Technical Monitoring | ContentKing | Ahrefs Audit | Real-time decay alerts |
| Project Management | ClickUp | Asana | Refresh queue, workflows |
| Writing Quality | Grammarly | — | Grammar, tone, plagiarism |
| Brief Storage | Notion | Google Drive | SOPs, briefs, research |
| Communication | Slack | — | Internal alerts, client updates |
| Reporting | Google Looker Studio | — | Client dashboards |

### 8.2 Required Templates & Documents
- Quarterly Audit Deck Template
- Refresh Brief Template
- Pre-Publish Checklist (Section 6.1)
- Refresh Tracking Sheet
- Client Refresh Report Template (Section 9)

### 8.3 Access Requirements
Each team member must have access to all client GA4, GSC, and SEO tool accounts. Maintain access matrix in shared workspace, reviewed quarterly.

---

## 9. Roles & Responsibilities (RACI)

| Activity | Content Strategist | SEO Analyst | Writer | Account Manager | Client |
|---|---|---|---|---|---|
| Run quarterly audit | A | R | I | I | I |
| Identify decay signals | C | R | I | I | I |
| Prioritize refresh queue | R | C | I | A | I |
| Build refresh brief | R | C | I | I | I |
| Execute content refresh | A | C | R | I | I |
| SEO & technical QA | C | R | I | I | I |
| Client approval | I | I | I | R | A |
| Publish & index | C | R | I | I | I |
| Performance monitoring | A | R | I | C | I |
| Reporting results | R | C | I | A | C |

*R = Responsible, A = Accountable, C = Consulted, I = Informed*

---

## 10. Reporting Template

### 10.1 Monthly Refresh Performance Report

```
═══════════════════════════════════════════════════════
AGENTICMARKETINGPRO — CONTENT REFRESH REPORT
Client: [Client Name]          Reporting Period: [Month Year]
Prepared by: [Strategist]      Approved by: [AM]
═══════════════════════════════════════════════════════

EXECUTIVE SUMMARY
─────────────────────────────────────────────────────
• Refreshes completed this month:    __
• Refreshes in progress:             __
• Refreshes in queue:                __
• Net organic traffic impact (90d):  +__%

PERFORMANCE SCORECARD
─────────────────────────────────────────────────────
URL                       | Baseline | Day 30 | Day 60 | Day 90 | Result
--------------------------|----------|--------|--------|--------|--------
/blog/example             | 1,200    | 1,450  | 1,680  | 1,920  | 🟢 Win
/guide/example           | 850      | 920    | 1,100  | 1,350  | 🟢 Major Win
/resource/example         | 600      | 580    | 590    | 580    | 🟡 Neutral

DECAY ALERTS IDENTIFIED THIS PERIOD
─────────────────────────────────────────────────────
• 3 URLs moved to Decaying tier
• 1 URL moved to Critical tier (added to priority queue)

UPCOMING REFRESH SCHEDULE
─────────────────────────────────────────────────────
URL                       | Owner     | Brief Date | Publish Date
--------------------------|-----------|------------|--------------
/blog/next-1              | Writer A  | 11/05      | 11/15
/blog/next-2              | Writer B  | 11/08      | 11/18

INSIGHTS & RECOMMENDATIONS
─────────────────────────────────────────────────────
1. [Key insight from refresh outcomes]
2. [Recommended strategic adjustment]
3. [New opportunity identified]

═══════════════════════════════════════════════════════
```

### 10.2 Quarterly Strategic Review (every 90 days)
In addition to the monthly report, deliver a strategic review covering:
- Total refreshes completed vs. target
- Aggregate traffic/revenue impact
- Top decay patterns by content category
- Recommended changes to SOP or content strategy
- Next quarter's refresh roadmap

---

## 11. SOP Maintenance

- **Version control:** All updates logged in document footer
- **Annual review:** Lead Content Strategist conducts full SOP review each January
- **Change requests:** Submit via standard change request form; require Head of Content approval
- **Training:** All new team members complete onboarding session within first 30 days

---

*End of Document — AMP-SOP-CONT-002 v1.0*

---

**Implementation tip:** Pilot this SOP with 2–3 clients for one quarter, gather feedback from the team, and refine before agency-wide rollout. The first audit will surface baseline data that makes subsequent cycles significantly faster.