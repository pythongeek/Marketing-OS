---
type: technical-seo-auditor
client: agenticmarketingpro
job_id: 24f90a1f-3cfe-4115-9ef3-a75b2ddde5a6
generated_at: 2026-07-11T18:43:38.603581+00:00
source: sync-from-db
---

# GSC Weekly Audit Checklist — AgenticMarketingPro

**Audit Window:** Monday–Sunday | **Comparison Period:** Previous 7 days vs. 13-week rolling average
**Prepared by:** Technical SEO | **Tool:** Google Search Console + Looker Studio (recommended)

---

## 📊 1. Performance Tab — Top-Line Metrics

| Metric | Current Week | vs. Last Week | vs. 13-Wk Avg | 🚨 Flag If |
|---|---|---|---|---|
| Total Clicks | ___ | ___% | ___% | Drop >10% WoW |
| Total Impressions | ___ | ___% | ___% | Drop >15% WoW |
| Average CTR | ___% | ___pp | ___pp | Below 2.5% |
| Average Position | ___ | ___ | ___ | Drops >2.0 spots |

- [ ] Filter by **Web** search type (default) — record all four metrics above
- [ ] Re-check with **Discover** filter enabled (traffic spike = content win)
- [ ] Re-check with **Google News** filter (only if applicable to AMP's content verticals)
- [ ] Compare **branded vs. non-branded** queries (use regex filter: `agenticmarketingpro|agentic marketing pro`)

> **Why it matters for AMP:** Since "agentic marketing" is an emerging term, branded CTR is typically inflated. Non-branded performance is the truer signal of topical authority growth.

---

## 🔍 2. Query Analysis

### 2a. New Queries (last 7 days, not in prior 30)
- [ ] Export **Queries** report, sort by Impressions DESC
- [ ] Identify queries appearing for the first time (cross-reference with prior 6 weeks)
- [ ] Tag each new query: *Informational / Commercial / Navigational*
- [ ] **Action:** Any commercial new query with >100 impressions → prioritize content optimization

### 2b. Lost Queries (had impressions, now zero)
- [ ] Filter: Impressions = 0 in current week, Impressions > 50 in prior 4 weeks
- [ ] Investigate each for: ranking drop, SERP feature cannibalization, or seasonal drop
- [ ] **Action:** For queries lost at positions 8–20 → on-page refresh candidate

### 2c. Position Movement
- [ ] Export full query list, compare position WoW
- [ ] **Winners:** Moved up ≥3 positions AND impressions >200 → flag for internal linking amplification
- [ ] **Losers:** Dropped ≥5 positions AND previously in top 10 → escalate to content team same day
- [ ] **SERP feature shifts:** Check if lost positions coincide with new AI Overview, featured snippet, or People Also Ask blocks

---

## 📄 3. Page-Level Analysis

### 3a. Top 10 Pages by Clicks
- [ ] Document URL, clicks, impressions, CTR, position
- [ ] Verify **title tag** and **meta description** still match landing page intent
- [ ] Check for CTR outliers: if position is 1–3 but CTR <5% → rewrite meta

### 3b. Declining Pages (Pages)
- [ ] Filter Pages report by CTR, compare WoW
- [ ] **Critical threshold:** Any page with >50% click loss WoW AND >500 prior clicks → **P0 investigation**
- [ ] Check for: indexation issues, manual penalties, cannibalization, outdated content
- [ ] **Action template:** Create ticket with URL, prior metrics, suspected cause, recommended fix

### 3c. Cannibalization Check
- [ ] Identify queries where **2+ AMP URLs** appear in top 20
- [ ] Common candidates: "what is agentic marketing," "best AI marketing tools," "[vendor] review"
- [ ] **Action:** Decide canonical, consolidation, or differentiation strategy

---

## 🗂️ 4. Index Coverage — Pages Report

| Status | Count | 🚨 Flag If |
|---|---|---|
| Valid (indexed) | ___ | Drops >5% WoW |
| Excluded | ___ | Sudden spike >20% |
| Errors | ___ | Any new errors |
| Valid with warnings | ___ | Increases >10 |

- [ ] **Errors tab → drill into each:**
  - [ ] `Soft 404` — page returns 200 but content suggests noindex/empty
  - [ ] `Submitted URL not found (404)` — clean up internal links
  - [ ] `Server error (5xx)` — escalate to dev team immediately
  - [ ] `Blocked by robots.txt` — verify intentional vs. accidental
- [ ] **Excluded tab → review:**
  - [ ] `Crawled - currently not indexed` (often quality issue)
  - [ ] `Discovered - currently not indexed` (often crawl budget)
  - [ ] `Duplicate without user-selected canonical`
  - [ ] `Alternate page with proper canonical tag` (verify canonical targets are correct)
- [ ] **Sitemaps:** Confirm submitted sitemaps have expected indexed ratio (target: >90%)

---

## ⚡ 5. Core Web Vitals (Mobile + Desktop)

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP | ≤2.5s | 2.5s–4.0s | >4.0s |
| INP | ≤200ms | 200ms–500ms | >500ms |
| CLS | ≤0.1 | 0.1–0.25 | >0.25 |

- [ ] Review **Mobile** CWV report — flag any URL groups newly moved to "Poor"
- [ ] Review **Desktop** CWV report — separate set of issues
- [ ] Cross-reference with **field data from real users** (CrUX), not just lab
- [ ] **AMP-specific watch list:**
  - [ ] Homepage
  - [ ] Top 5 blog posts (likely entry points)
  - [ ] Pricing / product pages
  - [ ] Any interactive tool or demo pages
- [ ] Export URL list of poor performers → ticket to dev with specific metric

> **Threshold:** More than 5% of evaluated URLs "Poor" = coordinated optimization sprint.

---

## 📱 6. Mobile Usability

- [ ] Confirm **zero new issues** in Mobile Usability report
- [ ] Common flags to watch:
  - [ ] Clickable elements too close together (CTAs in nav/footer)
  - [ ] Text too small to read (audit any newly added 9pt or smaller copy)
  - [ ] Viewport not set (typically only fires on legacy templates)
  - [ ] Content wider than screen (embedded iframes, tables)
- [ ] **Action:** Spot-check 3 random pages on real iOS + Android device (not just emulator)

---

## 🧩 7. Structured Data Validation

- [ ] **Enhancements report → review each detected type:**
  - [ ] `Article` — verify all blog posts parse correctly
  - [ ] `BreadcrumbList` — confirm hierarchy matches site structure
  - [ ] `Organization` — check Knowledge Graph signals
  - [ ] `FAQ` (if used) — confirm still eligible under current Google guidelines
  - [ ] `Product` / `SoftwareApplication` — for any AMP tools or platforms
  - [ ] `VideoObject` — for embedded demos/testimonials
- [ ] **Flag any item with:**
  - [ ] "Some issues" count > 0
  - [ ] "Decrease in valid items" >10% WoW
- [ ] **Live test** 3 sample URLs through [Rich Results Test](https://search.google.com/test/rich-results) for any new template
- [ ] **AI-search readiness:** Ensure `Organization`, `Person` (authors), and `Article` schema all have E-E-A-T relevant fields filled (author credentials, datePublished, dateModified, publisher)

---

## 🔒 8. Security Issues

- [ ] Open **Security & Manual Actions → Security Issues**
- [ ] Verify report shows: *"No issues detected"*
- [ ] **If any alert appears:**
  - [ ] Hacked content → isolate affected URLs immediately
  - [ ] Malware / unwanted software → notify hosting + dev within 1 hour
  - [ ] Phishing → redirect or remove URLs
- [ ] **Monthly cross-check:** Run [Google Safe Browsing diagnostic](https://transparencyreport.google.com/safe-browsing/search) for `agenticmarketingpro.com` (record in audit log)

---

## ⚖️ 9. Manual Actions

- [ ] Open **Security & Manual Actions → Manual Actions**
- [ ] Confirm: *"No manual actions found"*
- [ ] If action present:
  - [ ] Document issue type (pure spam, unnatural links, thin content, cloaking, etc.)
  - [ ] Identify scope (site-wide vs. partial match)
  - [ ] Create remediation plan with owner assigned
  - [ ] Reconsideration request drafted only after **full cleanup verified**
- [ ] **Cross-reference** against any recent Google algorithm update notes (track via [Google Search Status Dashboard](https://status.search.google.com/))

---

## 📈 10. Week-over-Week & Trend Comparison

Build a weekly log (Google Sheet or Looker Studio) tracking:

| Week Ending | Clicks | Impressions | CTR | Avg Pos | Indexed | CWV Poor % | Errors | Schema Issues |
|---|---|---|---|---|---|---|---|---|
| 2026-01-12 | | | | | | | | |
| 2026-01-19 | | | | | | | | |
| ... | | | | | | | | |

- [ ] Calculate **delta** for every metric
- [ ] Note any correlation with: published content, technical changes, Google updates, seasonality
- [ ] Flag **3-week consecutive declines** in clicks or impressions → strategy review meeting
- [ ] Monthly: review 13-week trend lines and share with leadership

---

## ✅ 11. Action Items Template

```
WEEKLY AUDIT — [Week Ending Date]
Auditor: ___________ | GSC Property: sc-domain:agenticmarketingpro.com

PRIORITY ACTIONS
─────────────────────────────────────────────────────────────────

[P0] [CRITICAL — Same Day]
• URL: _______________
• Issue: _______________
• Metric affected: _______________
• Owner: _______________ | Due: _______________
• Fix: _______________

[P1] [HIGH — This Week]
• URL: _______________
• Issue: _______________
• Metric affected: _______________
• Owner: _______________ | Due: _______________
• Fix: _______________

[P2] [MEDIUM — Next 2 Weeks]
• URL: _______________
• Issue: _______________
• Owner: _______________ | Due: _______________

[P3] [LOW — Backlog]
• URL: _______________
• Opportunity: _______________
• Owner: _______________

WINS TO CELEBRATE
─────────────────────────────────────────────────────────────────
• _____________________________
• _____________________________

NOTES / OBSERVATIONS
─────────────────────────────────────────────────────────────────
• _____________________________
```

---

## 🛠️ Recommended Workflow Enhancements

1. **Schedule export:** Use GSC API + Looker Studio for automated daily dashboards
2. **Alerting:** Set up email alerts via [GSC API](https://developers.google.com/webmaster-tools) for index error spikes (>25% increase) and security issues (real-time)
3. **Segmentation discipline:** Always run reports segmented by:
   - Branded vs. non-branded
   - Blog (`/blog/`) vs. money pages
   - Mobile vs. desktop
4. **AI search tracking:** Beginning Q1 2026, dedicate a section to track impressions/clicks from AI Overview-eligible queries separately — these often appear with reduced CTR but high impression volume

---

**Audit Cadence:** ⏱️ ~45 min/week for routine checks, +1–2 hrs for deep dive on flagged issues.

Would you like me to also produce a **Looker Studio dashboard template spec**, a **monthly deep-dive checklist**, or a **specific incident response playbook** for any of the P0 scenarios?