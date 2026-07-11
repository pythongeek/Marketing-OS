# 📊 Google Search Console Operations Playbook

**Client:** AgenticMarketingPro
**Document Type:** Standard Operating Procedure (SOP)
**Version:** 2.1
**Audience:** SEO Operations Team
**Cadence:** Daily + Weekly + Monthly cycles

---

## 🎯 Playbook Purpose & Philosophy

This playbook operationalizes Google Search Console (GSC) as a **systematic monitoring layer**, not a reactive tool. Every metric tracked here ties directly to revenue or technical risk. We treat GSC as the single source of truth for search performance signals that no third-party tool can replicate (because only Google knows what's actually happening on Google's side).

**Three Operating Principles:**
1. **Detect before users do** — anomalies caught in 24h, not 30 days
2. **Threshold-driven action** — no opinions, only rules
3. **Document everything** — every check, every finding, every action

---

# PART 1: DAILY CHECKS (5–10 minutes)

**Owner:** Rotating on-call SEO analyst
**Time:** 09:00 local time (after Google's overnight processing)
**Tool:** GSC + connected Slack alerts

---

## 1.1 Daily Check Procedure

### Step 1 — Open GSC Performance Anomaly Detection (3 min)

**Navigation:** `Performance > Search Results > Compare: Last 7 days vs Previous 7 days`

**What you'll see on screen:** A line chart with two date ranges overlaid, plus a metrics table below showing Clicks, Impressions, CTR, Position.

**Look for:**

| Signal | What to check | Action threshold |
|---|---|---|
| Click drops | Compare Today vs 7-day avg | >15% drop = investigate |
| Impression spikes | Sudden >30% increase | Could be indexing or algo — verify |
| Position shifts | Avg position change | >2 positions movement |
| CTR drops | Per-page CTR vs prior week | >1% absolute drop on key pages |

**Exact actions:**
1. Sort table by **Clicks descending** — verify top 20 pages still have traffic
2. Toggle filter to **"Date: Last 7 days"** and export if anomaly suspected
3. Click any page with >20% deviation → drill into **Pages > Queries** to find cause

### Step 2 — Manual Actions & Security Check (2 min)

**Navigation:** `Security & Manual Actions > Manual Actions` AND `Security & Manual Actions > Security Issues`

**Screenshot expectation:** Green checkmark with "No issues detected" text on white background.

**If anything appears:**
- 🔴 **Manual Actions present** → immediately escalate to SEO Lead + client (see Section 5.3)
- 🟡 **Security Issues** → notify DevOps within 1 hour, treat as P1

### Step 3 — Coverage Spike Check (2 min)

**Navigation:** `Index > Pages > Why pages aren't indexed`

**What to look for on screen:** A grouped list of error types (Server errors, Redirect errors, 404s, Excluded by 'noindex' tag, etc.) with count badges.

**Action threshold:**
- Any single error type > 50 pages increase day-over-day = investigate
- New "Server error (5xx)" entries > 10 = critical, escalate

### Step 4 — Verify URL Inspection (3 min)

**Spot-check:** Take 5 URLs from yesterday's published content and paste into the top-bar URL Inspection tool.

**Expected result:** "URL is on Google" with last crawl date within 7 days.

**If "URL is not on Google":**
- Click **"Request Indexing"**
- Log in the daily tracking sheet with timestamp

---

## 1.2 Daily Alert Configuration (One-time setup)

Connect GSC to email/Slack using these trigger conditions:

| Alert | GSC trigger | Channel |
|---|---|---|
| Manual action | Any manual action notification | Email + Slack #seo-critical |
| Coverage spike | Error count +20% WoW | Slack #seo-monitoring |
| CWV regression | Core Web Vitals report update showing new "Poor" URLs | Email daily digest |

---

# PART 2: WEEKLY ROUTINE

**Owner:** SEO Analyst (rotating) + SEO Lead review
**Time block:** 30–45 min per day, Mon–Fri 10:00–10:45

---

## 📅 MONDAY — Performance Deep Review

**Objective:** Establish weekly performance baseline, identify wins/losses, prioritize page-level interventions.

### Step-by-Step Procedure

**1. Top-line KPI Pull (10 min)**

Navigate: `Performance > Search Results > Date: Last 28 days`

Export the full query+page dataset (CSV) using the **Export** button (top right).

**Build this weekly comparison table:**

| Metric | Last 7d | Prev 7d | Δ % | Status |
|---|---|---|---|---|
| Total Clicks | | | | 🟢/🟡/🔴 |
| Total Impressions | | | | 🟢/🟡/🔴 |
| Avg CTR | | | | 🟢/🟡/🔴 |
| Avg Position | | | | 🟢/🟡/🔴 |
| Indexed Pages | | | | 🟢/🟡/🔴 |

**Threshold colors:**
- 🟢 Clicks ≥ +5% WoW
- 🟡 Clicks -5% to -15% WoW → investigate
- 🔴 Clicks < -15% WoW → escalate Monday AM

**2. Query-Level Winner/Loser Analysis (15 min)**

In the same Performance view:
- Filter by **Queries** tab
- Sort by **Clicks descending**
- Identify top 10 queries with biggest **absolute gain** and top 10 with biggest **absolute loss**

**Action:**
- For losers: Check if position dropped (likely algo/competition) or CTR dropped (likely snippet/title change)
- Document each in weekly tracker with hypothesis column

**3. Page-Level CTR Audit (10 min)**

Navigate: `Performance > Pages tab > Filter: Impressions > 1,000 in last 28 days`

**Find underperforming pages:**
- Filter for **CTR < 2%** AND **Position < 10** (these are striking-distance pages with title/description issues)
- These are your highest-leverage CTR wins

**For each page:** Note URL, current title meta, suggested revision for SEO Lead approval.

**4. Country & Device Filter Check (5 min)**

Toggle through filters:
- **Countries:** Identify any new country with >5% traffic (localization opportunity)
- **Devices:** Compare mobile vs desktop CTR (gap >30% = title/snippet issue)

---

## 📅 TUESDAY — Index Coverage & Sitemap Hygiene

**Objective:** Ensure all valuable pages are indexed, low-value pages are excluded, sitemap is healthy.

### Step-by-Step Procedure

**1. Pages Report Audit (15 min)**

Navigate: `Index > Pages`

**Screenshot description:** A status group breakdown chart at top showing 4 buckets — "Indexed", "Not indexed (with reason)", "Crawled, currently not indexed", "Excluded".

**Action checklist:**

| Status | Healthy count range | Action if outside range |
|---|---|---|
| Indexed | Should match total published pages (minus intentional excludes) | If sudden drop >5%, investigate |
| Discovered, not indexed | <10% of indexed | If >20%, check crawl budget / quality signals |
| Crawled, not indexed | <5% of indexed | If >10%, content quality review needed |
| Excluded by noindex | Expected (intentional) | Verify counts match CMS plan |
| Soft 404 | <20 pages | If spike, audit template/thin pages |
| Redirect error | 0 | Any = investigate immediately |
| 404 | Track low-value | >100 new = audit broken links |

**2. Sitemap Health (10 min)**

Navigate: `Index > Sitemaps`

**What you'll see:** A list of submitted sitemaps with status badges.

**Checks:**
- ✅ All sitemaps show "Success" status
- Last read date within 7 days
- Discovered vs indexed ratio > 80%

**If "Couldn't fetch" appears:**
- Click sitemap → check error message
- Common cause: 403 from WAF, sitemap URL change, encoding error
- Verify directly: `curl -I https://domain.com/sitemap.xml`

**3. Sitemap File Decomposition (10 min)**

For each sitemap in the index file:
1. Open sitemap directly in browser
2. Count URLs
3. Cross-reference with published pages from CMS export
4. Identify any orphan pages in sitemap that no longer exist

**Document in tracker:**
```
Sitemap URL | URLs submitted | URLs indexed | Last fetch | Status
```

---

## 📅 WEDNESDAY — Core Web Vitals & Page Experience

**Objective:** Monitor real-user performance signals; prevent UX-related ranking erosion.

### Step-by-Step Procedure

**1. Core Web Vitals Overview (15 min)**

Navigate: `Experience > Core Web Vitals`

**Screenshot description:** Two charts side-by-side — Mobile and Desktop — each showing percentages of URLs in "Good", "Needs improvement", and "Poor" buckets for LCP, INP, CLS.

**Threshold table:**

| Metric | Good | Needs Improvement | Poor | Action |
|---|---|---|---|---|
| LCP | ≤ 2.5s | 2.5s–4.0s | > 4.0s | Dev sprint task if Poor > 5% |
| INP | ≤ 200ms | 200ms–500ms | > 500ms | JS audit needed |
| CLS | ≤ 0.1 | 0.1–0.25 | > 0.25 | Layout shift investigation |

**Threshold for weekly action:**
- 🔴 Any metric showing >5% of URLs in Poor on mobile → create P1 dev ticket
- 🟡 5–10% Needs Improvement trending toward Poor → flag for next sprint

**2. Drill into Problem URLs (10 min)**

Click on any metric bar showing Poor/NII percentages:

**What you'll see:** A URL group table showing example URLs affected, with sample metric values.

**For each problematic URL group:**
1. Document pattern (e.g., all product pages, all /blog/* paths)
2. Run in PageSpeed Insights with URL
3. Identify top 2 contributing factors (e.g., "Render-blocking JS", "Unoptimized images")
4. Create dev ticket with: URL pattern, current metric value, target metric value, suggested fix

**3. Mobile Usability Quick Check (5 min)**

Navigate: `Experience > Mobile Usability`

**Expected:** "No issues" status.
- If any issues appear (e.g., "Clickable elements too close together", "Content wider than screen") → log and escalate same-day.

---

## 📅 THURSDAY — Manual Actions, Security & Policy Review

**Objective:** Catch compliance, manual action, or security issues before they cause catastrophic traffic loss.

### Step-by-Step Procedure

**1. Manual Actions Deep Review (10 min)**

Navigate: `Security & Manual Actions > Manual Actions`

**What to look for:**
- ✅ "No manual actions" green state
- ⚠️ Any "Issues found" section describing specific violation types (Pure spam, Thin content, Cloaking, etc.)

**If an action is found — escalation procedure:**

```
Hour 0:  Detect in GSC
Hour 1:  Notify SEO Lead + Account Manager
Hour 2:  Open P0 incident ticket
Hour 4:  Begin root cause analysis (which URLs, what violation type)
Hour 24: Submit reconsideration request after fix implemented
```

**2. Security Issues Scan (10 min)**

Navigate: `Security & Manual Actions > Security Issues`

**Watch for these report types:**
- Hacked: URL injection
- Hacked: Malware
- Hacked: Phishing
- Deceptive pages

**If detected:**
- Immediate lockout of affected URLs in robots.txt (temporary)
- Notify security team P0
- Plan full cleanup before requesting review

**3. Policy Review of Indexed Pages (15 min)**

Run URL Inspection on a random sample of 20 pages from the previous week's content:

For each:
- Verify it matches the canonical version
- Verify structured data validates
- Verify no cloaking signals (different content for Googlebot vs user)

**Sample template:**

| URL | Canonical OK | Structured data OK | Cloaking check | Notes |
|---|---|---|---|---|
| /example-1 | ✅ | ✅ | ✅ | None |
| /example-2 | ❌ | ✅ | ✅ | Canonical points to wrong URL |

---

## 📅 FRIDAY — Links, Discover & Weekly Reporting

**Objective:** Track link profile health, content distribution signals, and close out the week with documentation.

### Step-by-Step Procedure

**1. External Links Report (10 min)**

Navigate: `Links > External Links > Top linked external pages`

**What you'll see:** A table of your most-linked-to pages with link counts from external sites.

**Friday focus questions:**
- Are the top 10 most-linked pages still live and serving their target message?
- Any spam-link patterns (multiple links from low-quality domains to same page)?
- New top-linked page appearing? → Understand why (viral content, press mention, etc.)

**2. Internal Links Review (10 min)**

Navigate: `Links > Internal Links > Top internally linked pages`

**Verify:**
- High-priority commercial pages are receiving most internal links
- New content published this week has at least 5 internal links pointing to it
- Orphan pages (zero internal links) are not increasing

**3. Discover & News Performance (10 min)**

Navigate: `Performance > Discover`

**If Discover traffic exists (some sites):**
- Compare CTR for Discover vs Search
- Top performing Discover content informs editorial calendar
- Track: are top Discover URLs also performing well in Search?

**4. Weekly Report Compilation (15 min)**

**Deliverable:** Weekly SEO Health Report (template provided in Section 5.4)

**Structure:**
- KPI snapshot table (from Monday)
- Top 3 wins of the week
- Top 3 concerns
- Manual actions/security: clear status
- Open tickets and owners
- Next week's focus

**Send to:** Client (PDF) + internal Slack channel

---

# PART 3: MONTHLY DEEP DIVES

**Time:** 2–3 days distributed across month-end week
**Owner:** SEO Lead + Senior Analyst
**Output:** Strategic recommendations + prioritized backlog

---

## 🔬 3.1 Keyword Opportunity Mining (Positions 11–30)

**The #1 highest-ROI monthly activity.** Page 2 keywords are 5–10x easier to move to page 1 than page 4→page 1.

### Procedure

**Step 1 — Extract striking-distance queries (45 min)**

Navigate: `Performance > Search Results > Date: Last 90 days > Queries tab > Filter: Position > 10 AND Position < 31`

**Sort by Impressions descending.** These are queries with proven demand but under-leveraged rankings.

**Step 2 — Build opportunity matrix (60 min)**

Create a spreadsheet with the following columns:

| Query | Current Pos | Impressions (90d) | CTR | Competing URL | Search Intent | Content Gap | Priority Score |
|---|---|---|---|---|---|---|---|
| [query] | [pos] | [vol] | [%] | [who ranks #1] | [I/N/C/T] | [what's missing] | [1-100] |

**Priority Score formula:**
```
Priority = (Impressions × 0.6) + ((30 - Current Position) × 0.4)
```
Higher score = bigger opportunity.

**Step 3 — Cluster opportunities by page (30 min)**

Group queries by their target URL. Often, one underperforming page has 20+ queries stuck at position 12–25. Fixing that one page can yield massive gains.

**Step 4 — Action assignments (30 min)**

For each cluster:
- **If content gap exists:** Brief content team for content refresh (target: move to position <10 within 60 days)
- **If on-page SEO gap:** Internal linking + title/meta optimization
- **If authority gap:** Add to link-building campaign list

---

## 🔬 3.2 Query-Page Mismatch Analysis

**Purpose:** Find queries that rank on the wrong page (causing low CTR, high bounce, lost conversions).

### Procedure

**Step 1 — Detect mismatches (45 min)**

In `Performance > Pages`, click each top-performing page → switch to **Queries** tab.

**Mismatch signals:**

| Signal | Interpretation |
|---|---|
| Page ranks for 50+ informational queries but is a commercial page | Intent mismatch — needs intent-aligned content section |
| Page ranks #3 for branded query competitor name | SERP competition for non-owned brand |
| Same query appears for 5+ different pages | Cannibalization — needs canonical or page consolidation |
| Page ranks well but CTR < 1% | Title/description not aligned with query intent |

**Step 2 — Cannibalization resolution (60 min)**

