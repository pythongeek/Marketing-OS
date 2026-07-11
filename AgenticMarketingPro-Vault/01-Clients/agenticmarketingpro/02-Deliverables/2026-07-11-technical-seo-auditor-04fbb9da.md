---
type: technical-seo-auditor
client: agenticmarketingpro
job_id: 04fbb9da-ad26-460f-ae58-14339f17983a
generated_at: 2026-07-11T18:58:46.91328+00:00
source: sync-from-db
---

# GSC Weekly Audit Checklist — AgenticMarketingPro

**Audit Period:** `_____ / _____ / _____ to _____ / _____ / _____`
**Auditor:** `_________________`
**Property:** `https://agenticmarketingpro.com/`
**Comparison Period:** Previous 7 days (WoW) + Previous 28 days (MoM) + Previous 365 days (YoY)

---

## Section 1: Performance Tab — Core Metrics

> **Date Range Filter:** Last 7 days | **Compare:** Previous 7 days | **Segment:** All + Web + Mobile + Countries (Top 5)

### 1.1 Total Site Performance

| Metric | This Week | Last Week | Δ WoW | 28-Day Avg | Status |
|---|---|---|---|---|---|
| Total Clicks | ___ | ___ | ___% | ___ | 🟢 / 🟡 / 🔴 |
| Total Impressions | ___ | ___ | ___% | ___ | 🟢 / 🟡 / 🔴 |
| Average CTR (%) | ___ | ___ | ___pp | ___ | 🟢 / 🟡 / 🔴 |
| Average Position | ___ | ___ | ___Δ | ___ | 🟢 / 🟡 / 🔴 |

**Flagging Thresholds:**
- 🔴 **Critical:** Clicks ↓ >20% WoW OR Position ↓ >3 positions WoW
- 🟡 **Warning:** Clicks ↓ 10–20% WoW OR CTR ↓ >15% relative
- 🟢 **Healthy:** Within ±10% of previous period

### 1.2 By Device (Mobile vs. Desktop vs. Tablet)

- [ ] Mobile clicks/impressions/position recorded
- [ ] Desktop clicks/impressions/position recorded
- [ ] Mobile vs. desktop CTR gap analysis (target: <30% gap)
- [ ] Tablet trends noted (typically low volume — confirm expected)

**Flag:** Mobile position drops >4 spots while desktop stable = mobile-specific issue (likely CWV or mobile-first indexing).

### 1.3 By Country (Top Traffic Nations)

- [ ] Top 5 countries identified
- [ ] Each country's CTR vs. position benchmarked
- [ ] Anomalies flagged (e.g., high impressions, low CTR country)

### 1.4 Search Appearance Filters

- [ ] Filter by **Rich Results** — track clicks/impressions
- [ ] Filter by **Discover** — track daily trends
- [ ] Filter by **Google News** (if applicable)
- [ ] Filter by **Web Light results** — flag for review (low-quality mobile traffic)

---

## Section 2: Query Analysis

### 2.1 Top Queries (Sort: Clicks DESC)

| Query | Clicks | Impressions | CTR | Position | Δ Position WoW | Action |
|---|---|---|---|---|---|---|
| ___ | ___ | ___ | ___% | ___ | ___ | ___ |
| ___ | ___ | ___ | ___% | ___ | ___ | ___ |
| ___ | ___ | ___ | ___% | ___ | ___ | ___ |

**Action Triggers:**
- Queries in **positions 4–10** with CTR <5% → **Title tag rewrite candidate**
- Queries in **positions 11–20** with high impressions → **Content expansion opportunity**
- Queries with high impressions but CTR <2% → **Snippet/meta description test**

### 2.2 🆕 New Queries (Not in Previous Period)

- [ ] Filter: **Compare mode → New queries**
- [ ] Record top 10 new queries: `_________________`
- [ ] Identify search intent (informational / commercial / transactional)
- [ ] Match each new query to existing landing page (Y/N)
- [ ] Flag orphan queries (no matching page) → **Content gap candidate**

**AgenticMarketingPro priority:** New queries containing "AI agents," "agentic marketing," "marketing automation AI," or "autonomous marketing" should be prioritized for content mapping.

### 2.3 📉 Lost Queries (Dropped from Previous Period)

- [ ] Filter: **Compare mode → Queries with ↓ decline**
- [ ] Record queries with >50% click loss
- [ ] For each lost query:
  - [ ] Did the ranking URL change?
  - [ ] Did a competitor outrank us?
  - [ ] Did the SERP feature change (SGE, PAA, Featured Snippet)?
  - [ ] Was the content updated?

**Escalation Rule:** >5 high-volume queries lost in single week = **immediate strategy review**.

### 2.4 Position Movement Audit

| Movement Type | Threshold | Count | Action |
|---|---|---|---|
| Improved >5 positions | High | ___ | Note winning patterns, replicate |
| Declined >5 positions | High | ___ | Investigate SERP changes, content staleness |
| Entered Top 3 | Medium | ___ | Update internal links, protect ranking |
| Exited Top 10 | Critical | ___ | Immediate page-level audit |
| Position = 1 (SERP winner) | Track | ___ | Maintain, monitor SERP features |

---

## Section 3: Page-Level Analysis

### 3.1 Top Performing Pages (Top 10 by Clicks)

| URL | Clicks | Impressions | CTR | Avg Position | Trend |
|---|---|---|---|---|---|
| / | ___ | ___ | ___% | ___ | ↑ / → / ↓ |
| /blog/___ | ___ | ___ | ___% | ___ | ↑ / → / ↓ |
| ___ | ___ | ___ | ___% | ___ | ↑ / → / ↓ |

- [ ] Confirm top pages align with strategic business goals (product, lead-gen, brand)
- [ ] Identify any "wasted" top pages (high traffic, low conversion) → **CRO review**
- [ ] Verify internal linking flow supports these pages

### 3.2 📉 Declining Pages (Click Loss WoW)

**Filter:** Pages tab → Sort by Clicks Δ → Identify bottom 10

| URL | Δ Clicks | Δ Position | Likely Cause | Action Item |
|---|---|---|---|---|
| ___ | ___% | ___ | ___ | ___ |
| ___ | ___% | ___ | ___ | ___ |

**Common Causes Checklist:**
- [ ] Content freshness — last updated date
- [ ] Cannibalization (multiple URLs competing)
- [ ] SERP feature loss (lost snippet to competitor)
- [ ] Technical regression (indexing, CWV)
- [ ] Backlink loss (cross-ref with backlink tool)
- [ ] AI Overview / SGE absorbing clicks

### 3.3 High-Impression, Low-CTR Pages

**Threshold:** Impressions >1,000 AND CTR <2%

- [ ] List URLs: `_________________`
- [ ] Title tag rewrite test
- [ ] Meta description A/B test
- [ ] Schema markup enhancement (FAQ, HowTo)
- [ ] Featured snippet optimization attempt

### 3.4 Cannibalization Check

- [ ] Search GSC for branded + primary keyword terms
- [ ] Identify URLs ranking for same query
- [ ] Cross-reference with Screaming Frog crawl
- [ ] Action: Consolidate, canonicalize, or differentiate intent

---

## Section 4: Index Coverage (Pages Index)

### 4.1 Coverage Status Summary

| Status | Last Week | This Week | Δ | Notes |
|---|---|---|---|---|
| Valid (indexed) | ___ | ___ | ___ | Expected baseline |
| Valid with warnings | ___ | ___ | ___ | Review |
| Excluded | ___ | ___ | ___ | Verify intentional |
| Error | ___ | ___ | ___ | **CRITICAL** |
| Crawled — currently not indexed | ___ | ___ | ___ | Investigate |
| Discovered — currently not indexed | ___ | ___ | ___ | Check crawl budget |

### 4.2 🔴 Critical Errors (Investigate Immediately)

- [ ] **Server error (5xx)** — any new occurrences → escalate to dev team
- [ ] **Redirect error** — chains, loops, 404s in redirect
- [ ] **404 pages** — high-value pages? → Implement 410 or restore
- [ ] **Soft 404** — Google sees content as not-found despite 200 status
- [ ] **Submitted URL marked noindex** — conflict resolution
- [ ] **Blocked by robots.txt** — verify intent

**Action:** All errors must be fixed or documented within 7 days. Submit updated sitemap after fixes.

### 4.3 ⚠️ Warnings Review

- [ ] Indexed, though blocked by robots.txt — confirm intent
- [ ] Page with redirect — verify canonical handling
- [ ] Soft 404 detection rate
- [ ] Duplicate without user-selected canonical

### 4.4 Sitemap Health

- [ ] Submitted sitemap status: `_________________`
- [ ] Last successful read date: `_________________`
- [ ] Discovered URLs count: ___ | Submitted count: ___ | Indexed count: ___
- [ ] Indexation ratio target: **>90%** of submitted URLs
- [ ] Verify sitemap URL list matches canonical site structure

**Alert:** If indexation ratio drops below 80% → deep crawl audit required.

---

## Section 5: Core Web Vitals (Mobile + Desktop)

### 5.1 Mobile CWV Status

| Metric | Good URLs | Needs Improvement | Poor | % Good (Target: 75%+) |
|---|---|---|---|---|
| LCP | ___ | ___ | ___ | ___% |
| INP | ___ | ___ | ___ | ___% |
| CLS | ___ | ___ | ___ | ___% |

### 5.2 Desktop CWV Status

| Metric | Good URLs | Needs Improvement | Poor | % Good (Target: 75%+) |
|---|---|---|---|---|
| LCP | ___ | ___ | ___ | ___% |
| INP | ___ | ___ | ___ | ___% |
| CLS | ___ | ___ | ___ | ___% |

### 5.3 CWV Investigation

- [ ] Identify URLs in "Poor" status for each metric
- [ ] Group by issue type (e.g., image LCP, JS INP, layout shift CLS)
- [ ] Cross-reference with PageSpeed Insights
- [ ] Compare to previous week — any new URLs failing?

**Critical Thresholds (Core Web Vitals 2024+):**
- LCP: <2.5s (Good) | 2.5–4.0s (Needs Improvement) | >4.0s (Poor)
- INP: <200ms (Good) | 200–500ms (Needs Improvement) | >500ms (Poor)
- CLS: <0.1 (Good) | 0.1–0.25 (Needs Improvement) | >0.25 (Poor)

**AgenticMarketingPro note:** Heavy JS/AI feature embeds may impact INP — flag any third-party scripts on pages failing.

---

## Section 6: Mobile Usability

### 6.1 Mobile Issue Audit

| Issue Type | Affected URLs | Δ WoW | Priority |
|---|---|---|---|
| Clickable elements too close | ___ | ___ | High |
| Content wider than screen | ___ | ___ | Critical |
| Text too small to read | ___ | ___ | High |
| Viewport not configured | ___ | ___ | Critical |
| Flash usage (legacy) | ___ | ___ | Low |

- [ ] Zero mobile usability errors = ✅ target
- [ ] If errors >0: identify pattern (template-level vs. page-specific)
- [ ] Confirm responsive design active across all templates
- [ ] Verify mobile-first indexing compliance

**Action:** Any new mobile error = high-priority fix within 48 hours.

---

## Section 7: Structured Data Validation

### 7.1 Detected Structured Data Types

| Schema Type | Items Detected | Items with Errors | Items with Warnings |
|---|---|---|---|
| Organization | ___ | ___ | ___ |
| WebSite (with Sitelinks Search) | ___ | ___ | ___ |
| BreadcrumbList | ___ | ___ | ___ |
| Article / BlogPosting | ___ | ___ | ___ |
| FAQ | ___ | ___ | ___ |
| HowTo | ___ | ___ | ___ |
| SoftwareApplication | ___ | ___ | ___ |
| Product | ___ | ___ | ___ |
| Person (Author) | ___ | ___ | ___ |
| VideoObject | ___ | ___ | ___ |
| Review / AggregateRating | ___ | ___ | ___ |
| SpeakableSpecification | ___ | ___ | ___ |

### 7.2 Validation Drill-Down

- [ ] Run URL inspection on 3 key pages (homepage, top blog, product page)
- [ ] Verify no "Detected structured data → could not parse" errors
- [ ] Confirm rich result preview displays correctly
- [ ] Check for missing recommended fields (e.g., Article: `datePublished`, `author`, `image`)
- [ ] Verify Organization schema on all pages (via template or @id)

**AgenticMarketingPro priority schemas to monitor:**
1. **Organization** — confirm knowledge panel signals
2. **Article** — required for blog content (with author E-E-A-T)
3. **SoftwareApplication** — for product/tool pages
4. **FAQ** — for "what is" / "how does" marketing queries

**Action:** Any new structured data error = document and fix within 7 days.

---

## Section 8: Security Issues

### 8.1 Weekly Security Scan

- [ ] **Hacked content** detection: 0 = ✅ target
- [ ] **Malware** detection: 0 = ✅ target
- [ ] **Deceptive pages** detection: 0 = ✅ target
- [ ] **Unclear billing** issues: 0 = ✅ target
- [ ] **Phishing** detection: 0 = ✅ target

**CRITICAL:** Any security issue detected = immediate escalation to engineering + security team. Document at: `_________________`

- [ ] Cross-verify with Safe Browsing diagnostic page: `https://transparencyreport.google.com/safe-browsing/search`

---

## Section 9: Manual Actions

### 9.1 Manual Actions Status

- [ ] Manual actions panel reviewed
- [ ] Result: ✅ **No manual actions** OR 🔴 **Action(s) detected**

**If action detected:**

| Action Type | Affected Pages | Reason | Disavow Needed? | Status |
|---|---|---|---|---|
| ___ | ___ | ___ | Y / N | Open |
| ___ | ___ | ___ | Y / N | Open |

**Action:** Reconsideration request only after full remediation documented. Track timeline in action log.

- [ ] Review **Security & Manual Actions** report in full
- [ ] Review **Links** report for unnatural link warnings

---

## Section 10: Week-over-Week Comparison Summary

### 10.1 KPI Movement Dashboard

| KPI | This Week | Last Week | 4-Wk Avg | 13-Wk Avg | Trend |
|---|---|---|---|---|---|
| Total Clicks | ___ | ___ | ___ | ___ | ↑ / → / ↓ |
| Total Impressions | ___ | ___ | ___ | ___ | ↑ / → / ↓ |
| Avg CTR | ___% | ___% | ___% | ___% | ↑ / → / ↓ |
| Avg Position | ___ | ___ | ___ | ___ | ↑ / → / ↓ |
| Indexed Pages | ___ | ___ | ___ | ___ | ↑ / → / ↓ |
| Mobile CWV % Good | ___% | ___% | ___% | ___% | ↑ / → / ↓ |
| Structured Data Errors | ___ | ___ | ___ | ___ | ↑ / → / ↓ |

### 10.2 Traffic Distribution Shift

- [ ] **Branded vs. Non-Branded** click ratio: ___% / ___%
- [ ] Top 10 pages account for ___% of total clicks (concentration risk)
- [ ] New page traffic contribution this week: ___%
- [ ] Long-tail (3+ word queries) click share: ___%

### 10.3 SERP Feature Tracking

- [ ] Featured snippets won this week: ___
- [ ] Featured snippets lost this week: ___
- [ ] AI Overview appearances: ___
- [ ] People Also Ask inclusions: ___
- [ ] Image pack appearances: ___
- [ ] Video carousel appearances: ___

### 10.4 Anomaly Detection

- [ ] Days with significant traffic deviation: