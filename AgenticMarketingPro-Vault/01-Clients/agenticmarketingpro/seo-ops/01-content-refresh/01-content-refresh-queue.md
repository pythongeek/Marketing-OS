# SEO Ops Content Refresh Queue System
**For AgenticMarketingPro | Internal Operations Playbook**

---

## System Overview

This Content Refresh Queue System transforms reactive content updates into a proactive SEO operations engine. Built specifically for AgenticMarketingPro's AI marketing, SEO, and automation content portfolio, it ensures every asset maintains peak performance through systematic decay detection, priority scoring, and execution workflows.

**System Goals:**
- Detect content decay within 14 days of onset
- Maintain ≥90% of published content in "Healthy" status
- Recover lost traffic/positions within 60 days of refresh
- Establish predictable refresh cadence (no more "set and forget")

---

## 1. Content Decay Identification Methodology

### Detection Framework

Content decay occurs when published content loses organic visibility, traffic, or engagement relative to its baseline performance. AMP uses a **3-Signal Detection System** combining traffic, position, and engagement metrics.

#### Primary Decay Signals

| Signal | Threshold | Comparison Window | Severity Tier |
|--------|-----------|-------------------|---------------|
| **Organic Traffic Drop** | >15% decline vs. 90-day rolling average | Compare trailing 30 days to prior 90 days | Tier 1 (Critical) |
| **Average Position Drop** | >3 positions lost for primary keyword | Compare current month vs. previous 3 months | Tier 2 (High) |
| **CTR Decline** | >20% drop in CTR at maintained position | Compare last 60 days vs. prior 90 days | Tier 3 (Medium) |

#### Detection Schedule

- **Weekly Automated Scan:** Run every Monday 6:00 AM via Search Console + GA4 + Ahrefs/Semrush API
- **Monthly Manual Review:** First Wednesday of each month, 90-minute SEO team session
- **Quarterly Deep Audit:** First week of Q1/Q2/Q3/Q4, full content portfolio review

#### Decay Confirmation Protocol

A content asset enters the refresh queue **only when** it meets one of these conditions:

1. **Single-Signal Critical:** Traffic drop >30% OR position drop >7 spots
2. **Two-Signal Compound:** Any combination of two signals triggered simultaneously
3. **Sustained Pattern:** Same signal triggered across 3 consecutive weekly scans

**Exclusion Criteria:** Content with <1,000 monthly impressions OR content published within last 30 days (too new for meaningful decay data).

---

## 2. Refresh Priority Scoring Matrix

### Scoring Formula

```
Priority Score = (Traffic Value × Decay Severity Multiplier) / Effort Required
```

### Component Breakdown

#### A. Traffic Value (1-10 scale)

| Monthly Organic Traffic | Score |
|-------------------------|-------|
| 10,000+ sessions | 10 |
| 5,000–9,999 sessions | 8 |
| 1,000–4,999 sessions | 6 |
| 500–999 sessions | 4 |
| 100–499 sessions | 2 |
| <100 sessions | 1 |

**Strategic Keyword Bonus:** +2 points if content ranks for a Tier 1 keyword (high-intent, commercial value)

#### B. Decay Severity Multiplier (1.0x – 3.0x)

| Decay Pattern | Multiplier |
|---------------|------------|
| Traffic drop >40% + position drop >7 | 3.0x |
| Traffic drop 25-40% + position drop 5-7 | 2.5x |
| Traffic drop 15-25% OR position drop 3-5 | 2.0x |
| CTR decline >30% at stable position | 1.5x |
| CTR decline 20-30% at stable position | 1.2x |
| Minor/early-stage signals | 1.0x |

#### C. Effort Required (1-10 scale, inverse in formula)

| Refresh Type | Effort Score |
|--------------|--------------|
| Update stats/dates only | 2 |
| Add images/media | 3 |
| Improve CWV/technical fixes | 4 |
| Expand existing sections | 5 |
| Merge thin content (2+ pages) | 7 |
| Major rewrite + redirect obsolete | 9 |

### Final Priority Tiers

| Score Range | Priority Level | SLA |
|-------------|----------------|-----|
| 15.0+ | **P0 — Critical** | Address within 7 days |
| 8.0–14.9 | **P1 — High** | Address within 14 days |
| 4.0–7.9 | **P2 — Medium** | Address within 30 days |
| 1.0–3.9 | **P3 — Low** | Address within 60 days |

### Scoring Example (AMP Content)

**Asset:** "AI Marketing Automation Tools Guide 2025"
- Traffic Value: 8 (3,500 monthly sessions, ranks for "ai marketing tools" Tier 1)
- Decay Severity: 2.5x (28% traffic drop, positions dropped from #4 to #9)
- Effort Required: 5 (expand sections, add new tool comparisons)
- **Priority Score: (8 × 2.5) / 5 = 4.0 → P1 — High**

---

## 3. Six Types of Content Refresh

### Type 1: Update Statistics & Data
**Triggers:** Outdated statistics, broken data references, year mentions in title, >12 months since last data refresh

**Execution Checklist:**
- [ ] Audit all statistics, dates, and data points
- [ ] Source updated data from authoritative sources (2025/2026)
- [ ] Update inline citations and external links
- [ ] Refresh title tag if year-stamped (e.g., "2025" → "2026")
- [ ] Update schema markup with new dates
- [ ] Add "Last Updated: [Date]" visible timestamp

**Time Estimate:** 30–90 minutes per page

### Type 2: Expand Sections
**Triggers:** Competitor content outranks with 2x word count, People Also Ask questions unanswered, thin topical coverage

**Execution Checklist:**
- [ ] Run content gap analysis vs. top 3 SERP competitors
- [ ] Identify missing subtopics from PAA + related searches
- [ ] Add 300-800 words per missing subtopic
- [ ] Include original examples, case studies, or AMP product references
- [ ] Maintain existing keyword density; avoid cannibalization
- [ ] Update internal links to new sections

**Time Estimate:** 2–4 hours per page

### Type 3: Add Media
**Triggers:** Text-heavy pages with <2 images, no video, low dwell time (<90 seconds), competitors using rich media

**Execution Checklist:**
- [ ] Create or source custom graphics (charts, diagrams, screenshots)
- [ ] Add product screenshots for AMP-specific tutorials
- [ ] Embed explainer videos (YouTube, Loom, or native)
- [ ] Optimize all media: descriptive file names, alt text, WebP format
- [ ] Add image schema where appropriate
- [ ] Lazy-load non-critical media

**Time Estimate:** 1–3 hours per page

### Type 4: Improve Core Web Vitals
**Triggers:** LCP >2.5s, INP >200ms, CLS >0.1, mobile usability errors

**Execution Checklist:**
- [ ] Run PageSpeed Insights + CrUX report
- [ ] Optimize LCP: preload hero images, reduce server response time
- [ ] Fix INP: defer non-critical JS, break up long tasks
- [ ] Resolve CLS: set image/video dimensions, reserve ad space
- [ ] Minify CSS/JS, enable Brotli compression
- [ ] Test on mobile (3G throttling) + desktop

**Time Estimate:** 2–6 hours per page (developer collaboration required)

### Type 5: Merge Thin Content
**Triggers:** Multiple URLs competing for same keyword, pages with <300 words and <100 monthly sessions, cannibalization detected

**Execution Checklist:**
- [ ] Identify all competing URLs via keyword overlap analysis
- [ ] Choose primary URL (highest traffic/backlinks/authority)
- [ ] Audit and consolidate best content from all sources
- [ ] Rewrite to eliminate redundancy and improve depth
- [ ] Implement 301 redirects from secondary URLs
- [ ] Update internal links pointing to old URLs
- [ ] Submit updated sitemap

**Time Estimate:** 4–8 hours per merge cluster

### Type 6: Redirect Obsolete Content
**Triggers:** Topic no longer relevant, product discontinued, outdated by >2 years with no recovery path, negative ROI

**Execution Checklist:**
- [ ] Confirm no recovery path (search intent evolved beyond relevance)
- [ ] Identify best replacement URL (most contextually relevant existing page)
- [ ] Implement 301 redirect with preserved anchor text
- [ ] Update or remove all internal links pointing to old URL
- [ ] Document redirect in redirects tracker
- [ ] Monitor for 90 days post-redirect for issues

**Time Estimate:** 30–60 minutes per redirect

---

## 4. Refresh Workflow: 5-Stage Process

### Stage 1: IDENTIFY (Days 1-3)

**Owner:** SEO Analyst

**Activities:**
- Run weekly decay detection scan
- Apply decay confirmation protocol
- Add flagged URLs to refresh queue with raw metrics
- Tag with content topic category (AI Marketing / SEO / Automation)

**Deliverable:** Refresh Queue Spreadsheet with new entries

### Stage 2: AUDIT (Days 3-7)

**Owner:** Content Manager + SEO Analyst

**Activities:**
- Deep-dive analysis of queued content (top 10 by priority)
- SERP competitive analysis (top 5 ranking pages)
- Content gap identification
- Technical audit (CWV, schema, internal links)
- Determine appropriate refresh type (from 6 options)

**Deliverable:** Refresh Brief Document with:
- Current vs. target metrics
- Specific issues identified
- Recommended refresh type
- Estimated effort hours

### Stage 3: PLAN (Days 7-10)

**Owner:** Content Strategist

**Activities:**
- Assign priority tier (P0-P3) using scoring matrix
- Allocate to content team member based on expertise
- Set SLA deadline based on priority tier
- Brief writer/editor with detailed requirements
- Schedule in editorial calendar

**Deliverable:** Assigned task in project management tool with brief link

### Stage 4: EXECUTE (Days 10-40, varies by tier)

**Owner:** Content Writer/Editor + Developer (if technical)

**Activities:**
- Execute refresh per brief specifications
- Internal review (editor + SEO review pass)
- Publish updates (update existing URL, don't change slug)
- Submit sitemap if structural changes made
- Notify team in Slack #seo-refresh channel

**Deliverable:** Updated live content with changelog entry

### Stage 5: MEASURE (Days 60-90 post-refresh)

**Owner:** SEO Analyst

**Activities:**
- Capture baseline metrics (pre-refresh snapshot)
- Track recovery metrics at 30, 60, 90-day intervals
- Compare against pre-refresh baselines
- Document wins/learnings in refresh log
- Adjust future scoring if needed

**Deliverable:** Before/After Performance Report

---

## 5. Content Refresh Calendar Template

### Quarterly Refresh Cadence

| Quarter | Focus | Review Date | Owner |
|---------|-------|-------------|-------|
| **Q1** (Jan-Mar) | Full portfolio audit, prioritize Q4-prior content | Week 2 of January | SEO Lead |
| **Q2** (Apr-Jun) | Mid-year refresh of top-traffic pages | Week 2 of April | Content Manager |
| **Q3** (Jul-Sep) | AI marketing trends update sweep | Week 2 of July | Content Strategist |
| **Q4** (Oct-Dec) | Year-end refresh: stats, dates, annual guides | Week 2 of October | SEO Analyst |

### Monthly Refresh Operations

| Week | Activity | Deliverable |
|------|----------|-------------|
| Week 1 | Decay scan + queue additions | Refresh queue updated |
| Week 2 | Audit top 5 priority items | Refresh briefs created |
| Week 3 | Execute scheduled refreshes | Published updates |
| Week 4 | Measure previous month's refreshes | Performance snapshot |

### Refresh Calendar Spreadsheet Structure

| URL | Topic | Priority | Refresh Type | Owner | Start Date | Due Date | Status | Baseline Traffic | Target Traffic |
|-----|-------|----------|--------------|-------|------------|----------|--------|------------------|----------------|
| /ai-marketing-automation | AI Marketing | P1 | Expand Sections | J. Smith | 2026-01-15 | 2026-01-29 | In Progress | 2,400 | 3,200 |
| /seo-tools-2025 | SEO | P0 | Update Stats | M. Lee | 2026-01-08 | 2026-01-15 | Complete | 850 | 1,200 |

---

## 6. Before/After Tracking Methodology

### Baseline Capture (Pre-Refresh)

Capture these metrics **7 days before refresh** publication:

- Organic sessions (trailing 30 days)
- Average position (primary keyword)
- CTR (search appearance vs. clicks)
- Impressions
- Average engagement time
- Backlink count
- Top 3 ranking keywords + positions

### Post-Refresh Measurement Windows

| Window | Measurement Point | Primary KPIs |
|--------|-------------------|--------------|
| **30-Day** | Day 30 post-publish | Traffic recovery, position recovery |
| **60-Day** | Day 60 post-publish | CTR improvement, impression growth |
| **90-Day** | Day 90 post-publish | Full performance comparison, ROI calculation |

### Success Criteria by Refresh Type

| Refresh Type | Success Metric | Target |
|--------------|----------------|--------|
| Update Stats | Traffic recovery | +20% vs. baseline within 60 days |
| Expand Sections | Position recovery | Return to within 2 positions of peak |
| Add Media | Engagement improvement | +30% avg. engagement time |
| Improve CWV | CWV scores | All metrics in "Good" range |
| Merge Thin | Consolidated traffic | Combined > original individual |
| Redirect Obsolete | Link equity transfer | New URL ranks within 30 days |

### Refresh Performance Report Template

**URL:** [Page URL]
**Refresh Date:** [Date]
**Refresh Type:** [Type]
**Priority Tier:** [P0-P3]

| Metric | Baseline (Pre) | 30-Day | 60-Day | 90-Day | Change |
|--------|----------------|--------|--------|--------|--------|
| Organic Sessions | 2,400 | 2,100 | 2,900 | 3,400 | +41.7% |
| Avg. Position | 8.2 | 9.1 | 6.5 | 5.1 | +3.1 |
| CTR | 3.2% | 2.8% | 4.1% | 4.8% | +1.6pp |
| Engagement Time | 1:42 | 1:38 | 2:05 | 2:18 | +35.3% |

**Outcome:** [Win / Partial Win / Underperformer]
**Learnings:** [Key takeaways for future refreshes]

---

## Implementation Roadmap

### Week 1: Foundation Setup
- Configure automated decay detection (GA4 + Search Console + Ahrefs alerts)
- Build refresh queue spreadsheet with scoring formulas
- Document current content inventory baseline

### Week 2: Team Alignment
- Train SEO team on 3-signal detection protocol
- Brief content team on 6 refresh types
- Establish Slack channel and reporting cadence

### Week 3: Pilot Launch
- Run first decay scan
- Score top 10 flagged URLs
- Execute first 3 refreshes (one of each priority tier)

### Week 4+: Operational Cadence
- Weekly scans begin
- Monthly audit sessions scheduled
- Quarterly deep audits on calendar

---

## Tools & Resources

**Detection & Analytics:**
- Google Search Console (position/CTR data)
- Google Analytics 4 (traffic/engagement)
- Ahrefs or Semrush (ranking tracking, content gaps)
- Screaming Frog (technical audits for CWV candidates)

**Execution:**
- Google Docs / Notion (refresh briefs)
- Asana or ClickUp (task management)
- Canva / Figma (custom graphics)
- PageSpeed Insights / WebPageTest (CWV verification)

**Reporting:**
- Google Sheets (queue tracking + scoring)
- Data Studio / Looker (refresh performance dashboards)

---

## System Maintenance

**Monthly:** Review scoring matrix accuracy; adjust multipliers based on observed patterns
**Quarterly:** Audit refresh type distribution; ensure balanced portfolio attention
**Annually:** Benchmark system performance vs. industry standards; refine SLAs

---

*This system is a living document. Update quarterly based on observed outcomes and team feedback. Last revised: [Current Date] | Owner: SEO Operations Lead, AgenticMarketingPro*