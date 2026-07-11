# AgenticMarketingPro — Skill Registry & Process Documentation

## Overview

This document defines every skill in the Marketing OS, its role, the process it follows, and how it integrates with the AgenticMarketingPro client profile.

---

## Skill Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Atlas Orchestrator                        │
│              (agentic-marketing-os skill)                    │
│         Daily 9-step ops loop, dispatches agents             │
└──────────────────────┬──────────────────────────────────────┘
                       │
    ┌──────────────────┼──────────────────┐
    ▼                  ▼                  ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Content │     │  SEO    │     │  Paid   │
│  Team   │     │  Team   │     │  Team   │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     ▼               ▼               ▼
```

---

## Core Skills (30 Total)

### 1. Atlas Orchestrator — `agentic-marketing-os`
**Role:** Master orchestration skill. Runs the daily ops loop, dispatches specialist agents, manages the task queue.

**Process:**
1. Load client context (profile, manifest, KPIs)
2. Site health check → dispatch `tech-seo-auditor`
3. GSC/Bing monitoring → dispatch `gsc-expert` + `bing-wmt-expert`
4. Content brief generation → dispatch `content-strategist`
5. Writer assignment → dispatch `longform-writer`
6. On-page review → dispatch `on-page-optimizer`
7. Social repurposing → dispatch `social-media-manager`
8. Outreach queue → dispatch `off-page-strategist`
9. Analytics digest → dispatch `analytics-expert`
10. Profit plan update

**Output:** Daily ops log, task queue updates, anomaly flags

---

### 2. Content Strategist — `content-strategist`
**Role:** Owns the content factory's intake. Briefs only — never writes.

**Process:**
1. Read topic clusters, keyword universe, content calendar
2. Read client KPIs and goals
3. Identify gaps (high volume, low competition, missing cluster coverage)
4. Match intent to content type and writer persona
5. Generate brief with YAML frontmatter
6. Update content calendar

**Input:** `03-SEO-Intelligence/topic-clusters.md`, `keyword-universe.md`, `04-Content-Production/content-calendar.md`, `01-Clients/[client]/kpis-and-goals.md`
**Output:** `04-Content-Production/briefs/[client]-[slug].md`, updated calendar

---

### 3. On-Page Optimizer — `on-page-optimizer`
**Role:** Audits and rewrites on-page elements for every published page.

**Process:**
1. Read target page URL and content
2. Read brief for target keyword and SEO requirements
3. Audit: title, meta, H1-H3, schema, internal links, alt text, keyword density
4. Write fix queue with before/after recommendations
5. Apply fixes (if approved)

**Input:** `04-Content-Production/published-index.md`, briefs
**Output:** `01-Clients/[client]/technical-fix-queue.md`

---

### 4. Technical SEO Auditor — `tech-seo-auditor`
**Role:** Crawls site architecture, validates structured data, checks speed, mobile, and logs.

**Process:**
1. Read previous audit and anomaly log
2. Crawl site, validate schema, check CWV, mobile test, log analysis
3. Score issues: Impact × Urgency / Effort
4. Write findings with prioritized fix queue

**Input:** `03-SEO-Intelligence/technical-audit-log.md`, `10-Analytics/anomaly-log.md`
**Output:** `03-SEO-Intelligence/technical-audit-log.md`, `01-Clients/[client]/technical-fix-queue.md`

---

### 5. AEO/GEO Specialist — `aeo-geo-specialist`
**Role:** Optimizes for AI search engines (ChatGPT, Gemini, Perplexity).

**Process:**
1. Audit current AEO citations
2. Build entity schema and knowledge graph presence
3. Optimize FAQ/HowTo schema for AI snippets
4. Monitor citation rates weekly

**Input:** Client website, competitor AEO presence
**Output:** AEO optimization report, schema updates

---

### 6. Competitor Intelligence — `competitor-intel`
**Role:** Monitors competitor rankings, backlinks, content, and pricing.

**Process:**
1. Read competitor profiles from vault
2. Pull ranking data, backlink data, content gaps
3. Identify opportunities and threats
4. Update competitor watch file

**Input:** `01-Clients/[client]/competitor-watch.md`, `02-Competitors/`
**Output:** Updated competitor watch, opportunity alerts

---

### 7. Copywriter — `copywriter`
**Role:** Writes conversion-focused copy for ads, landing pages, emails.

**Process:**
1. Read brand voice guide
2. Read brief (audience, angle, CTA)
3. Write copy with A/B variants
4. Self-review against conversion checklist

**Input:** Brand voice, brief, competitor copy
**Output:** Copy variants with performance predictions

---

### 8. CRO Agent — `cro-agent`
**Role:** Designs and analyzes A/B tests, optimizes conversion funnels.

**Process:**
1. Read analytics data and funnel metrics
2. Identify drop-off points
3. Design test variants
4. Run tests, analyze results
5. Implement winners

**Input:** GA4 data, heatmap data, user recordings
**Output:** Test results, implementation recommendations

---

### 9. Email Lifecycle Agent — `email-lifecycle-agent`
**Role:** Builds and optimizes email sequences for nurture, onboarding, retention.

**Process:**
1. Map customer lifecycle stages
2. Design sequences per stage
3. Write emails with personalization
4. A/B test subject lines and CTAs
5. Monitor deliverability and engagement

**Input:** Customer data, lifecycle stage definitions
**Output:** Email sequences, performance reports

---

### 10. Analytics Expert — `analytics-expert`
**Role:** Compiles reports, identifies anomalies, tracks KPIs.

**Process:**
1. Pull data from GA4, GSC, ad platforms
2. Calculate KPIs vs targets
3. Identify anomalies (>2σ deviations)
4. Write digest with recommendations

**Input:** API credentials, KPI definitions
**Output:** Weekly digest, anomaly alerts

---

### 11. Social Media Manager — `social-media-manager`
**Role:** Creates and schedules social content, engages with community.

**Process:**
1. Read published content for repurposing
2. Create platform-native content
3. Schedule posts
4. Monitor engagement and respond

**Input:** `04-Content-Production/published-index.md`, brand voice
**Output:** Social calendar, engagement reports

---

### 12. Paid Ads Manager — `ad-expert`
**Role:** Manages PPC campaigns across Google, Meta, LinkedIn.

**Process:**
1. Review campaign performance
2. Adjust bids and budgets
3. A/B test creatives
4. Optimize targeting
5. Report ROAS and CPA

**Input:** Campaign data, conversion tracking
**Output:** Optimized campaigns, performance reports

---

### 13. Local SEO Agent — `local-seo-agent`
**Role:** Optimizes Google Business Profile, local citations, map pack rankings.

**Process:**
1. Audit GBP completeness
2. Check citation consistency
3. Optimize for local keywords
4. Monitor map pack rankings

**Input:** Business location data, competitor local presence
**Output:** Local SEO report, citation fixes

---

### 14. Off-Page Strategist — `off-page-strategist`
**Role:** Manages link building, digital PR, and outreach campaigns.

**Process:**
1. Read link prospects and outreach log
2. Prioritize prospects by authority and relevance
3. Draft personalized outreach emails
4. Follow up on responses
5. Log acquired links

**Input:** `07-Off-Page/link-prospects.md`, `outreach-log.md`
**Output:** Updated outreach log, acquired links

---

### 15. Programmatic SEO Engineer — `pseo-engineer`
**Role:** Builds automated content at scale for long-tail keywords.

**Process:**
1. Identify pSEO opportunities
2. Build data sources and templates
3. Generate pages programmatically
4. Monitor indexing and rankings

**Input:** Keyword data, data sources
**Output:** Programmatic pages, indexing reports

---

### 16. QA Pipeline — `qa-pipeline`
**Role:** Quality assurance gate for all content and code outputs.

**Process:**
1. Run plagiarism check
2. Run legal/compliance check
3. Score against quality rubric
4. Pass/fail with feedback

**Input:** Content output, quality standards
**Output:** QA report with pass/fail status

---

### 17. Reporting Agent — `reporting-agent`
**Role:** Generates client-ready reports and dashboards.

**Process:**
1. Aggregate data from all sources
2. Build visualizations
3. Write narrative summary
4. Format for client delivery

**Input:** All campaign data, KPIs
**Output:** Client report (PDF/HTML)

---

### 18. Reputation Manager — `reputation-agent`
**Role:** Monitors brand sentiment, reviews, and mentions.

**Process:**
1. Monitor review platforms
2. Track brand mentions
3. Alert on negative sentiment spikes
4. Draft response recommendations

**Input:** Review APIs, social listening data
**Output:** Sentiment reports, response drafts

---

### 19. Revenue Scout — `revenue-scout`
**Role:** Identifies upsell, cross-sell, and expansion opportunities.

**Process:**
1. Analyze client usage data
2. Identify expansion signals
3. Recommend upsell plays
4. Track revenue impact

**Input:** CRM data, usage analytics
**Output:** Opportunity pipeline, revenue forecasts

---

### 20. Video/Image Producer — `video-image-producer`
**Role:** Creates visual content for social, ads, and web.

**Process:**
1. Read brief for visual requirements
2. Generate or source visuals
3. Optimize for platforms
4. Deliver assets

**Input:** Content brief, brand guidelines
**Output:** Visual assets, usage specs

---

### 21. Market Signals — `market-signals`
**Role:** Monitors industry trends, algorithm updates, and market shifts.

**Process:**
1. Monitor news and algorithm updates
2. Track industry trends
3. Alert on relevant changes
4. Recommend strategic pivots

**Input:** News feeds, algorithm trackers
**Output:** Market alerts, strategic recommendations

---

### 22. Martech Integration Agent — `martech-integration-agent`
**Role:** Manages API credentials, integrations, and data pipelines.

**Process:**
1. Maintain integration health
2. Troubleshoot API issues
3. Set up new connections
4. Monitor data flow

**Input:** API credentials, integration requirements
**Output:** Healthy integrations, data pipelines

---

### 23. Onboarding Agent — `onboarding-agent`
**Role:** Handles new client onboarding and vault setup.

**Process:**
1. Collect client information
2. Generate vault folder structure
3. Create client profile, manifest, strategy
4. Set up initial KPIs

**Input:** Onboarding form data
**Output:** Complete client vault

---

### 24. Pitch Agent — `pitch-agent`
**Role:** Generates sales proposals and pitch decks.

**Process:**
1. Read client requirements
2. Research prospect
3. Build proposal with ROI projections
4. Generate pitch deck

**Input:** Prospect data, service catalog
**Output:** Proposal, pitch deck

---

### 25. Playbook Librarian — `playbook-librarian`
**Role:** Maintains SOPs, playbooks, and knowledge base.

**Process:**
1. Document successful processes
2. Update playbooks with learnings
3. Organize knowledge base
4. Train agents on new procedures

**Input:** Agent logs, successful campaigns
**Output:** Updated playbooks, SOPs

---

### 26. Forecasting Agent — `forecasting-agent`
**Role:** Predicts traffic, revenue, and resource needs.

**Process:**
1. Analyze historical data
2. Build forecasting models
3. Predict trends
4. Recommend resource allocation

**Input:** Historical performance data
**Output:** Forecasts, resource recommendations

---

### 27. GSC Expert — `gsc-expert`
**Role:** Monitors Google Search Console data and opportunities.

**Process:**
1. Pull GSC data
2. Identify CTR opportunities
3. Track indexing issues
4. Report on query performance

**Input:** GSC API, website manifest
**Output:** GSC weekly log, CTR opportunities

---

### 28. Bing WMT Expert — `bing-wmt-expert`
**Role:** Monitors Bing Webmaster Tools data.

**Process:**
1. Pull Bing data
2. Identify opportunities
3. Track indexing
4. Report performance

**Input:** Bing API, website manifest
**Output:** Bing weekly log

---

### 29. Influencer Agent — `influencer-agent`
**Role:** Manages influencer outreach and campaigns.

**Process:**
1. Identify relevant influencers
2. Outreach and negotiate
3. Manage campaigns
4. Track ROI

**Input:** Target audience, campaign goals
**Output:** Influencer campaigns, ROI reports

---

### 30. Agent Prompt Engineer — `agent-prompt-engineer`
**Role:** Optimizes prompts for all agents in the system.

**Process:**
1. Review agent performance
2. Identify prompt failures
3. A/B test prompt variants
4. Deploy improved prompts

**Input:** Agent logs, output quality scores
**Output:** Optimized prompts, performance improvements

---

## AgenticMarketingPro-Specific Skill Configuration

### Priority Skills for AMP
Based on the OSINT research, these skills are highest priority for AgenticMarketingPro:

| Priority | Skill | Why |
|----------|-------|-----|
| P0 | `aeo-geo-specialist` | Core differentiator — AEO/GEO is AMP's unique offering |
| P0 | `content-strategist` | Need content engine for n8n thought leadership |
| P0 | `tech-seo-auditor` | Site has technical issues (no case studies, missing pricing) |
| P1 | `competitor-intel` | Track n8n.io, Relevance AI, Make.com agencies |
| P1 | `social-media-manager` | LinkedIn social selling is key channel |
| P1 | `ad-expert` | Paid ads for "n8n automation agency" keywords |
| P2 | `local-seo-agent` | GEO optimization for local landing pages |
| P2 | `email-lifecycle-agent` | Nurture sequence for free audit leads |
| P2 | `cro-agent` | Optimize free audit conversion funnel |
| P2 | `analytics-expert` | Track lead gen metrics |

### AMP Client Profile Integration

When any skill runs for AgenticMarketingPro, it should load:
- **Industry:** AI Automation Agency / B2B SaaS
- **Target Geo:** US, Canada, UK, Australia
- **Primary Keywords:** n8n automation agency, AI agent development, business automation
- **Competitors:** n8n.io (official), Relevance AI, Make.com agencies, Zapier agencies
- **ICP:** 10-200 employee SMEs, COO/VP Operations, $1M-$50M ARR
- **Value Prop:** 70% cost reduction, 24/7 AI operations
- **Pricing:** Starter $5K, Pro $15K-$50K, Enterprise $50K+

### Skill Prompt Override

Every skill now supports a **Prompt Override** field that allows customizing the default skill instructions per run. This is critical for AMP because:

1. **AEO/GEO campaigns** need industry-specific entity optimization
2. **Content briefs** should target n8n-specific keywords
3. **Competitor intel** should track n8n ecosystem competitors
4. **Social content** should use AMP's brand voice (professional but approachable)

---

## Job Execution Flow

```
User clicks "Run" on skill
        │
        ▼
┌───────────────┐
│ Skill Run Modal│
│ - Select client│
│ - Prompt override│
│ - Additional context│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ POST /api/jobs │
│ Creates job in  │
│ Supabase        │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Job appears in │
│ Jobs page with │
│ realtime updates│
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Edge Function  │
│ or Cron Job    │
│ polls pending  │
│ jobs and runs  │
│ skill logic    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ Result stored  │
│ in job.result  │
│ Viewable in    │
│ Jobs page      │
└───────────────┘
```

---

## Integration Points

### Supabase Tables
- `clients` — client profiles with vault_content (JSONB)
- `skills` — skill definitions with instructions and config
- `jobs` — job queue with status, payload, result
- `agent_logs` — structured logging for all operations

### APIs
- `/api/clients` — CRUD for clients
- `/api/skills` — Read skills, update instructions
- `/api/jobs` — Create jobs, view job history
- `/api/clients/[slug]/generate-vault` — Generate vault content

### External Services
- Hermes Agent Desktop — for agent execution
- Supabase — database and realtime
- Vercel — hosting
- Cron-Job.org — scheduled job triggers

---

*Last updated: 2026-07-08*
