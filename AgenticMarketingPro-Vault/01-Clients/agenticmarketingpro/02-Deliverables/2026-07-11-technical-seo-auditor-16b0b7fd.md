---
type: technical-seo-auditor
client: agenticmarketingpro
job_id: 16b0b7fd-2bb4-40b9-b935-af85be136704
generated_at: 2026-07-11T18:43:38.875203+00:00
source: sync-from-db
---

# Technical Health Monitoring SOP
**Client:** AgenticMarketingPro
**Document Type:** Standard Operating Procedure
**Version:** 1.0
**Owner:** Technical SEO Lead
**Review Cadence:** Quarterly
**Last Updated:** [Insert Date]

---

## 1. Purpose & Scope

This SOP establishes a repeatable, tiered monitoring cadence to preserve organic visibility, page experience, and index integrity for AgenticMarketingPro (and scalable to client engagements). The goal is **early detection** of technical degradation before it impacts rankings, traffic, or revenue.

**Scope:** Production websites owned by AgenticMarketingPro. Each client engagement inherits this SOP as a baseline and may add custom focus areas.

---

## 2. Roles & Responsibilities (RACI)

| Activity | SEO Lead | Dev Team | Content Lead | Account Manager |
|----------|----------|----------|--------------|-----------------|
| Daily monitoring | R | I | I | I |
| Weekly CWV review | R | C | I | I |
| Monthly crawl/index audit | R | C | I | I |
| Quarterly architecture review | R/A | C | C | C |
| Fix implementation | C | R | I | I |
| Fix verification | R | C | I | I |
| Stakeholder reporting | R | I | I | A |

*R=Responsible, A=Accountable, C=Consulted, I=Informed*

---

## 3. Monitoring Cadence

### 3.1 Daily Checks (Automated + 15-min manual review)

**Focus:** Uptime, critical errors, indexing health

#### Automation Checks (run 24/7)
- [ ] Uptime monitoring active (HTTP 200 on key templates)
- [ ] SSL certificate validity (auto-renewal confirmed)
- [ ] robots.txt reachable and not blocking critical sections
- [ ] XML sitemap returns valid XML (no parse errors)
- [ ] 5xx server error rate spike detection
- [ ] Search Console: Coverage / Page Indexing anomalies
- [ ] Search Console: Manual Actions alert
- [ ] DNS resolution health

#### Daily Checklist
- [ ] Review uptime report (previous 24h)
- [ ] Check critical error queue (5xx, unhandled exceptions)
- [ ] Verify new manual actions in GSC (if any)
- [ ] Review "crawled - currently not indexed" spike (>10% day-over-day)
- [ ] Confirm scheduled deployments did not break canonical tags on top templates
- [ ] Scan for security incidents (unexpected redirects, malware flags)

> **Note for AgenticMarketingPro:** If you're operating as an agency, also monitor **client-aggregated dashboards** (e.g., Looker Studio pulling from multiple GSC accounts).

---

### 3.2 Weekly Checks (Mondays, ~90 min)

**Focus:** Core Web Vitals, Mobile Usability, Structured Data, Index anomalies

#### Core Web Vitals (CWV)
- [ ] Pull CrUX report for `https://agenticmarketingpro.com` (last 28 days)
  - **LCP (Largest Contentful Paint):** target ≤ 2.5s; alert if > 2.5s on >25% of URLs
  - **INP (Interaction to Next Paint):** target ≤ 200ms; alert if > 200ms
  - **CLS (Cumulative Layout Shift):** target ≤ 0.1
- [ ] Run Lighthouse on top 10 landing pages (mobile + desktop)
- [ ] Compare week-over-week CWV trends in Performance dashboard
- [ ] Identify newly regressed URLs (origin-level + URL-level)

#### Mobile Usability
- [ ] GSC → Mobile Usability report → zero new issues
- [ ] Verify viewport meta tag present on all template types
- [ ] Tap target spacing audit (48px minimum) on top pages
- [ ] Test key flows on actual iOS/Android devices (not just emulators)

#### Structured Data
- [ ] Run [Rich Results Test](https://search.google.com/test/rich-results) on 5 representative URLs per schema type:
  - Organization
  - Article / BlogPosting
  - FAQ / HowTo (when present)
  - BreadcrumbList
  - Service / Product
  - LocalBusiness (if applicable)
- [ ] Validate with [Schema Markup Validator](https://validator.schema.org/)
- [ ] Check GSC → Enhancements report for warnings/errors
- [ ] Monitor drop in rich result impressions (≥ 15% WoW triggers investigation)

#### Crawl & Index Spot-Check
- [ ] GSC → Pages report (indexed vs. excluded breakdown)
- [ ] Review new "Discovered - currently not indexed" URLs (>500/wk = investigation trigger)
- [ ] Check soft 404 cluster for duplicate / thin templates

---

### 3.3 Monthly Checks (First Monday, ~4 hours)

**Focus:** Crawl budget, index bloat, log file analysis, deeper audits

#### Crawl Budget Analysis
- [ ] Pull server log files (sample minimum: 7 days, full month preferred)
- [ ] Segment bot traffic: Googlebot, Bingbot, others (GPTBot, etc.)
- [ ] Identify crawl waste: orphaned URLs, faceted nav, parameter URLs, infinite spaces
- [ ] Compare Googlebot crawl frequency: pre vs. post-fix windows
- [ ] Verify crawl rate matches priority (high-value pages crawled more often)

#### Index Bloat Audit
- [ ] Run `site:` query in Google: count indexed URLs vs. expected
  - **Threshold investigation:** index growth >10% MoM with no planned URL additions
  - **Index contraction alert:** index decline >5% MoM on canonical pages
- [ ] Inspect sample of 50 indexed thin/duplicate URLs
- [ ] Review pagination and faceted navigation indexing
- [ ] Audit pagination tags (`rel=next/prev` deprecated - use `rel=canonical` only)
- [ ] Check `noindex` directives on staging, search results, internal filters

#### Log File Analysis
- [ ] Tool: [Oncrawl](https://www.oncrawl.com/) or [Logz.io](https://logz.io/) or Screaming Frog Log Analyzer
- [ ] Top bot-accessed URLs (sanity check what Google cares about)
- [ ] URLs requested but missing in crawl budget priority (orphan pages)
- [ ] HTTP status code distribution from bot perspective:
  - 200 OK
  - 3xx redirects (chain length acceptable ≤ 1 hop)
  - 4xx client errors
  - 5xx server errors (immediate priority)
- [ ] Detect crawl traps (sessions IDs, calendars, relative URLs)
- [ ] Identify wasted JavaScript/CSS crawling (block non-essential assets if needed)

#### Schema Deep Audit
- [ ] Full schema validation via Screaming Frog custom extraction
- [ ] Coverage check: top services, top blog posts, contact page, about page
- [ ] Required vs. recommended property compliance
- [ ] Nested schema validity (e.g., Article → Person → Organization)

#### Backlink/External Signal Check
- [ ] Toxic backlink spike detection (Ahrefs/Semrush)
- [ ] Anchor text distribution anomalies
- [ ] Referring domain churn >20% MoM

---

### 3.4 Quarterly Checks (First month of quarter, ~8 hours)

**Focus:** Site architecture, internal linking, canonical integrity, large-scale audits

#### Site Architecture Review
- [ ] Visualize current architecture (Screaming Frog tree, Sitebulb, or in-house)
- [ ] Identify pages >3 clicks from homepage (target: any page ≤ 4 clicks)
- [ ] Review silo/topic cluster structure
- [ ] Confirm category hubs link to and from page-level content
- [ ] Audit navigation: HTML nav (not JS-only) for crawlability
- [ ] Mobile vs. desktop navigation parity check

#### Internal Linking Audit
- [ ] Run Screaming Frog crawl → analyze internal link distribution
- [ ] Identify orphan pages (zero internal inbound links)
- [ ] Find over-linked pages (>100 internal outbound to irrelevant targets)
- [ ] Audit anchor text distribution: branded vs. keyword vs. generic
- [ ] Review contextual linking on top 20 pages by traffic
- [ ] Identify missed internal linking opportunities (related content silos)

#### Canonical Strategy Review
- [ ] Audit all canonical declarations: HTML, HTTP header, sitemap
- [ ] Identify canonical chains (Google ignores chained canonicals - should be 1:1)
- [ ] Check for canonical mismatches across signals:
  - HTML canonical
  - Open Graph URL
  - sitemap URL
  - internal link URL
- [ ] Review trailing slash, protocol (http/https), and `www` consistency
- [ ] Cross-domain canonical strategy review (if applicable)

#### Hreflang & International (if applicable)
- [ ] Validate `hreflang` cluster integrity
- [ ] Confirm `x-default` specified
- [ ] No orphan locale versions
- [ ] `lang` attribute on `<html>` tag matches content

#### Comprehensive Schema Refresh
- [ ] Re-evaluate schema types as business evolves (new services, FAQ additions)
- [ ] Audit `sameAs` properties (Knowledge Graph consistency)
- [ ] Test emerging types: `Organization`, `WebSite` with `SearchAction`

#### Security & Compliance
- [ ] HTTPS enforcement (HSTS preloaded, mixed-content check)
- [ ] Cookie consent implementation review (GDPR/CCPA)
- [ ] CSP headers review
- [ ] Confirm `noindex` on dev/staging/preview environments

---

## 4. Recommended Tool Stack

### 4.1 Tier 1 — Free / Essential (Daily Use)

| Tool | Purpose | URL |
|------|---------|-----|
| Google Search Console | Indexing, coverage, CWV, manual actions | search.google.com/search-console |
| Bing Webmaster Tools | Secondary index visibility, mobile usability | bing.com/webmasters |
| Google PageSpeed Insights | Lab + field CWV data | pagespeed.web.dev |
| Google Rich Results Test | Schema validation | search.google.com/test/rich-results |
| Schema Markup Validator | Schema.org validation | validator.schema.org |
| Lighthouse (Chrome DevTools) | Per-URL audits | Chrome built-in |
| WebPageTest | Deep performance waterfall | webpagetest.org |
| UptimeRobot (free tier) | Uptime monitoring + alerts | uptimerobot.com |
| Looker Studio + GSC connector | Custom dashboards | lookerstudio.google.com |

### 4.2 Tier 2 — Mid-Market (Weekly/Monthly)

| Tool | Purpose | Approx. Cost |
|------|---------|--------------|
| Screaming Frog SEO Spider | Crawls, schema extraction, audits | ~$259/yr |
| Ahrefs or Semrush | Backlinks, index, rank tracking | $100–$500/mo |
| Sitebulb | Visual audits, architecture | ~$33/mo |
| ContentKing | Real-time SEO monitoring | ~$49+/mo |
| Oncrawl | Log file + crawl analytics | Enterprise |

### 4.3 Tier 3 — Enterprise (Monthly/Quarterly)

| Tool | Purpose |
|------|---------|
| Lumar (formerly DeepCrawl) | Enterprise technical audits |
| Botify | Log + index + content platform |
| Datadog / New Relic | Synthetic monitoring + APM |
| Logz.io / Splunk | Centralized log analytics |
| Custom Looker Studio dashboards | Multi-property aggregation (for agency scaling) |

### 4.4 Recommended Stack for AgenticMarketingPro

**Phase 1 (Now):** GSC + Bing + PageSpeed Insights + Screaming Frog + UptimeRobot + Looker Studio
**Phase 2 (Growth):** Add Ahrefs + Sitebulb + ContentKing
**Phase 3 (Scale):** Add Lumar or Botify + Datadog

---

## 5. Alert Thresholds & Escalation

### 5.1 Threshold Matrix

| Metric | Healthy | Investigate | Critical |
|--------|---------|-------------|----------|
| Uptime (rolling 30d) | ≥ 99.9% | 99.5–99.9% | < 99.5% |
| 5xx error rate | 0% | > 0.1% | > 1% |
| Soft 404 spike | 0/wk | 10–50/wk | > 50/wk |
| LCP (field, 75p) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| INP (field, 75p) | ≤ 200ms | 200–500ms | > 500ms |
| CLS (field, 75p) | ≤ 0.1 | 0.1–0.25 | > 0.25 |
| Indexed URL growth MoM | -2% to +5% | +5–10% | > 10% or < -5% |
| Manual actions | None | n/a | Any |
| Organic traffic (WoW) | ±10% | -10 to -25% | > -25% |
| CWV URLs "Poor" | ≤ 10% | 10–25% | > 25% |
| New "Discovered-not-indexed" | < 100/wk | 100–500/wk | > 500/wk |
| Rich result drop | < 5% WoW | 5–15% | > 15% |

### 5.2 Escalation Playbook

| Severity | Response Time | Notification Channel | Owner |
|----------|---------------|---------------------|-------|
| **P0 — Critical** | Within 1 hour | Phone + Slack #seo-incident + Email | SEO Lead → Dev Lead → Account Mgr |
| **P1 — High** | Within 4 hours | Slack #seo-alerts + Email | SEO Lead |
| **P2 — Medium** | Within 24 hours | Slack #seo-monitoring | SEO Lead |
| **P3 — Low** | Next sprint | Backlog ticket | SEO analyst |

**P0 Examples:** Complete site deindexing, manual action issued, certificate expired, organic traffic drop >50% in 24h, malware detected.

**P1 Examples:** CWV regression > 25% URLs to Poor, soft 404 spike, structured data invalidation affecting key templates, robots.txt accidentally blocking site.

---

## 6. Issue Prioritization Framework

We score every issue using: **Priority Score = (Impact × Urgency) / Effort**

### Scoring Scale
- **Impact** (1–5): Revenue/ranking/visibility impact
- **Urgency** (1–5): Time-sensitivity to ranking loss or compounding harm
- **Effort** (1–5): Engineering hours required (1 = <1h, 5 = multi-day)

### Decision Matrix

| Score Range | Priority | Action |
|-------------|----------|--------|
| ≥ 10 | **P0** | Fix today, war-room if needed |
| 5–9 | **P1** | Fix within sprint (≤ 2 weeks) |
| 2–4 | **P2** | Backlog for next sprint |
| < 2 | **P3** | Quarterly review |

### Example Scoring

| Issue | Impact | Urgency | Effort | Score | Priority |
|-------|--------|---------|--------|-------|----------|
| Homepage returns 500 | 5 | 5 | 1 | **25** | P0 |
| Schema validation error on blog | 3 | 3 | 1 | **9** | P1 |
| 5,000 thin tag pages indexed | 4 | 3 | 4 | **3** | P2 |
| Image alt text missing on legacy page | 2