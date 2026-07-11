---
type: technical-seo-auditor
client: agenticmarketingpro
job_id: 4e9141a1-d3ff-48f8-bbd8-6283816c1af3
generated_at: 2026-07-11T16:47:02.758194+00:00
source: sync-from-db
---

# Technical Health Operations Playbook
## Client: AgenticMarketingPro | Stack: Next.js on Vercel

---

## Executive Summary

This playbook codifies the recurring technical SEO health checks required to maintain AgenticMarketingPro's organic visibility. It is designed for a **two-person operational rhythm**: weekly health sweeps by the Technical SEO lead, monthly deep crawls shared between SEO and Dev, and quarterly reviews that inform the product roadmap.

**Severity Scoring (Impact × Urgency ÷ Effort):**
- **P0** — Traffic or revenue loss occurring *now*. Drop everything.
- **P1** — Risk of ranking loss within 30 days. Fix within sprint.
- **P2** — Technical debt or efficiency issue. Schedule within quarter.
- **P3** — Hygiene / nice-to-have. Backlog.

---

## 1. Weekly Health Sweep (45–60 min)

> **Owner:** Technical SEO Lead
> **Cadence:** Every Monday, before standup
> **Output:** P0/P1 issues logged to #seo-incidents Slack channel; dashboard snapshot archived

### 1.1 Uptime & Synthetic Monitoring

**Tool stack:** Better Uptime or UptimeRobot (free tier covers basic HTTP/keyword checks)

| Check | Method | Pass Criteria | Vercel-Specific Note |
|---|---|---|---|
| Homepage HTTP status | Monitor `https://agenticmarketingpro.com/` every 60s | 200 OK, TTFB < 800ms | Vercel Edge cache should serve from edge POP |
| Key landing pages (5–10 URLs) | Same as above | 200 OK | Use `x-vercel-cache: HIT` header check |
| `/sitemap.xml`, `/robots.txt` | Status + content fingerprint | 200 OK, changed within expected cadence | Vercel serves `app/sitemap.js` and `app/robots.js` from edge |
| SSL handshake | External monitor | Valid cert, >14 days remaining | Vercel auto-provisions Let's Encrypt; renewal is automatic but verify |

**Action:** Configure alerts at 2 consecutive failures from 2 geographic regions to suppress flapping.

### 1.2 Crawl Error Monitoring

**Tool stack:** Google Search Console → Pages → "Why pages aren't indexed"

```
Filter: 4xx (excluding soft 404s), 5xx, Redirect errors, Excluded by robots.txt
```

**Pass criteria:**
- New 404s week-over-week: **≤ baseline + 5**
- Soft 404 detection: any page returning 200 but GSC flagged as soft 404 → immediate investigation (usually thin content or template issue)
- 5xx errors: **zero tolerance** — P0

**Next.js-specific check:** Verify that ISR pages returning dynamic errors (e.g., `notFound()` in app router) actually emit **404 status codes**, not 200 with error UI. This is a common Next.js gotcha.

```typescript
// app/[slug]/page.tsx — correct pattern
import { notFound } from 'next/navigation';

export default async function Page({ params }) {
  const data = await fetchData(params.slug);
  if (!data) notFound(); // emits 404, not 200
}
```

### 1.3 robots.txt Verification

**Tool stack:** Manual fetch + Vercel deployment preview check

```
curl -A "Googlebot" https://agenticmarketingpro.com/robots.txt
```

**Validation checklist:**
- [ ] No accidental `Disallow: /` on production deploy
- [ ] Sitemap directive present and current
- [ ] No staging/internal paths leaked (`/admin`, `/api/*` patterns)
- [ ] Compare against last week's hash — flag unexpected changes immediately

**Next.js note:** In App Router, `app/robots.js` is the source of truth. Any code change to this file should trigger a CI check that diffs the rendered output against the previous deploy.

### 1.4 Sitemap Freshness

**Tool stack:** Direct inspection of `/sitemap.xml` + GSC Sitemap report

| Metric | Expected | Action If Violated |
|---|---|---|
| HTTP status | 200 | P0 if production |
| Last modification date on most recent URLs | Within expected content cadence | P1 if stale >7 days for active blog section |
| URL count delta vs. last week | Matches expected publishes + deletes | Investigate orphan generation |
| GSC "Discovered vs. indexed" gap | < 15% | Investigate crawl budget drain |

**Next.js validation:**
```typescript
// app/sitemap.ts — verify revalidation cadence
export const revalidate = 3600; // 1 hour for ISR sitemap
```

### 1.5 SSL Certificate Status

**Tool stack:** SSL Labs (deep scan, weekly), or Better Stack SSL monitoring

- Expiry **> 30 days**: green
- Expiry **< 30 days**: P1 (Vercel auto-renews, but verify in dashboard)
- Mixed content warnings: P0 (check if any legacy `http://` resources got re-introduced)

### 1.6 Vercel Deployment Health

Quick scan of last 7 deployments in Vercel dashboard:
- Any failed production deployments?
- Any rollbacks executed?
- Build duration creeping up >20%? (early signal of perf debt)

---

## 2. Monthly Site Crawl Audit (3–4 hours)

> **Owner:** Technical SEO Lead + Dev support (1 hour async review)
> **Cadence:** First week of each month
> **Output:** Issue list bucketed by P0/P1/P2 with assigned owners and sprint targets

### 2.1 Crawl Configuration

**Tool:** Screaming Frog SEO Spider (or Sitebulb for visualization-heavy teams)

**Crawl setup for Next.js:**
- **User-Agent:** Googlebot (Smart Mode) — matches Google's modern rendering
- **JavaScript rendering:** Enabled. Set crawl budget to 500 URLs max in initial pass, then full site overnight
- **Respect robots.txt:** Off during audit (we want to see what *could* be crawled)
- **Speed:** 5 req/s for staging previews, 10 req/s for production
- **Custom extraction:** Use XPath/CSS selectors to pull:
  - Next.js page IDs from `__NEXT_DATA__` JSON
  - ISR timestamps from meta tags
  - Image dimensions from `next/image` `srcset`

**Critical config to enable:**
- ✅ Check Images (alt text, oversized files)
- ✅ Check Canonicals
- ✅ Check Hreflang (if applicable)
- ✅ Check Structured Data (validate JSON-LD against Schema.org)
- ✅ XML Sitemap integration (cross-reference)

### 2.2 Page-Level Issues Audit

| Issue | Detection | Severity Heuristic | Next.js Context |
|---|---|---|---|
| Duplicate content (exact) | Hash comparison | P1 if > 1% of indexed pages | Often caused by trailing slash or query param variants |
| Near-duplicate titles/descriptions | Screaming Frog duplicate filter | P2 unless on top 20% traffic pages | Dynamic `[slug]` pages without unique metadata |
| Thin content | Word count < 300 + low internal links | P1 if ranking, P2 otherwise | Check if these are template placeholders |
| Missing alt text | Images filter | P1 if on product/landing pages, P2 for decorative | `next/image` requires `alt` prop — enforce via ESLint rule |
| Broken internal links | Response codes 4xx/5xx | P0 if homepage area, P1 elsewhere | Often from deleted ISR pages without redirects |
| Missing canonicals | Canonical filter | P0 on indexable duplicates | Verify `generateMetadata` returns canonical |
| Missing H1 | Headings filter | P2 (usually multiple H1s in Next.js layouts) | Audit `<h1>` in `app/layout.tsx` and page files |

### 2.3 Site Architecture Issues

**Detection in Screaming Frog:**
1. **Export → Crawl Overview → Site Structure**
2. **Bulk Export → Response Codes, Redirects**

| Issue | Detection Method | Severity |
|---|---|---|
| Redirect chains > 2 hops | Filter: Redirect URL chains | P1 (lose link equity, slow crawls) |
| Redirect loops | Same | P0 (infinite crawl trap) |
| Orphan pages | Filter: Inlinks = 0 | P2 if no inbound links from sitemap/internal |
| Deep pages (clicks from home > 4) | Crawl tree visualization in Sitebulb | P2 |
| Pagination issues | Inspect `?page=N` patterns | P1 if using `noindex` on paginated views incorrectly |
| Faceted nav crawl bloat | URL parameter report | P1 — common in Next.js e-commerce with filter UIs |

**Next.js-specific architecture checks:**

```bash
# Find pages potentially missing ISR revalidation
grep -r "export const revalidate" app/ --include="*.tsx"
```

Pages without `revalidate` constant in App Router may default to static at build time, leading to **stale content** — a common invisible issue. Flag any content-bearing pages missing this.

### 2.4 Sitemap & Indexability Reconciliation

Compare:
- URLs in `/sitemap.xml`
- URLs discovered by Screaming Frog crawl
- URLs in GSC "Indexed pages"

**Expected ratio:** sitemap ≤ crawl ≤ indexed. If indexed > sitemap by >10%, investigate cloaking or unauthorized indexation. If crawl >> indexed, investigate crawl budget waste.

---

## 3. Quarterly Deep Audit (1–2 days, dedicated sprint)

> **Owner:** Technical SEO Lead + Senior Developer (paired work)
> **Cadence:** Q1: January, Q2: April, Q3: July, Q4: October
> **Output:** Quarterly SEO Health Report → Executive summary + prioritized roadmap for next quarter

### 3.1 Log File Analysis

**Tool stack:** Vercel Log Drain (Datadog/Better Stack) + custom queries, or Screaming Frog Log File Analyser

**Vercel setup:**
1. In Vercel dashboard → Project → Settings → Logs → Enable Log Drain to your aggregator
2. Filter logs by `path`, `status_code`, `user_agent`, `response_time_ms`
3. Export last 90 days for analysis

**Key queries to run:**

```
Top 50 URLs by Googlebot hit count → identify crawl budget concentration
URLs hit >1000/day by Googlebot → may indicate soft-404 or thin content trap
URLs returning 5xx to Googlebot → P0 emergency
URLs crawled but not in sitemap → orphan discovery
404 URLs hit by Googlebot → redirect candidates
```

**Decision rules:**
- If Googlebot wastes >30% of crawl on non-canonical URLs → action: tighten `robots.txt` or add canonicals
- If high-priority pages have < 50 daily hits → action: improve internal linking
- If 5xx errors > 0.01% → P0

### 3.2 Core Web Vitals Regression Testing

**Tool stack:** PageSpeed Insights API (automated via CI), CrUX dataset via Data Studio, Vercel Analytics

**Automated regression check (add to CI/CD):**

```yaml
# .github/workflows/cwv-monitor.yml
name: CWV Weekly Check
on:
  schedule:
    - cron: '0 6 * * 1'  # Monday 6am
jobs:
  cwv:
    runs-on: ubuntu-latest
    steps:
      - name: Run PSI API for top 50 URLs
        run: node scripts/psi-audit.js
        env:
          PSI_API_KEY: ${{ secrets.PSI_API_KEY }}
```

**Thresholds (75th percentile, mobile):**

| Metric | Good | Needs Improvement | Poor (P1) |
|---|---|---|---|
| LCP | ≤ 2.5s | ≤ 4.0s | > 4.0s |
| INP | ≤ 200ms | ≤ 500ms | > 500ms |
| CLS | ≤ 0.1 | ≤ 0.25 | > 0.25 |

**Next.js-specific CWV levers to verify:**

- [ ] `next/image` with `priority` on LCP images (hero, above-fold)
- [ ] Font loading via `next/font` with `display: swap` and preloading
- [ ] No layout shift from dynamic ad insertions (CLS guard)
- [ ] Vercel Edge cache headers configured on static assets
- [ ] `loading.js` and `Suspense` boundaries for INP-sensitive routes
- [ ] No blocking third-party scripts in `<head>` without `defer`/async

**CrUX field data review:**
Pull the CrUX dashboard for the entire origin. Compare quarter-over-quarter:
- Origin-level LCP/INP/CLS trends
- Specific page-type patterns (e.g., blog posts degrading while product pages improve)
- Mobile vs. desktop gap

### 3.3 Structured Data Audit

**Tool stack:** Rich Results Test API, Schema.org validator, custom Screaming Frog extraction

**Process:**
1. Extract all JSON-LD from live pages via Screaming Frog custom extraction
2. Validate against Google Search Gallery requirements
3. Cross-reference with GSC Enhancements reports for warnings

**Schema types in scope for AgenticMarketingPro (assumed content marketing + service pages):**

| Schema | Critical Pages | Validation Frequency |
|---|---|---|
| Organization | Homepage, About | Quarterly + on deployment |
| Article / BlogPosting | All blog posts | Monthly sample of 50 |
| BreadcrumbList | All non-homepage | Crawl-wide monthly |
| FAQ | Any page with FAQ block | Quarterly |
| Product | Service pages if applicable | Monthly |
| Author | Author archives | Quarterly |

**Validation script (Node.js example):**

```javascript
// scripts/validate-schema.js
import { validateSchema } from 'schema-dts';

async function validate(urls) {
  for (const url of urls) {
    const html = await fetch(url).then(r => r.text());
    const jsonLd = extractJsonLd(html);
    const errors = validateSchema(jsonLd);
    if (errors.length) console.error(`${url}:`, errors);
  }
}
```

### 3.4 Link Velocity Analysis

**Tool stack:** Ahrefs or Semrush API

**Track quarterly:**
- New referring domains (DR/DRT distribution)
- Lost referring domains (especially DR 60+)
- Anchor text distribution (over-optimized anchors → risk)
- Internal link growth per top-100 pages

**Action thresholds:**
- Lost > 10% of DR 60+ referring domains QoQ → investigate outreach recovery
- New referring domains growth < 5% QoQ → flag to content team
- Anchor text entropy decreasing → risk of over-optimization

### 3.5 Competitor Gap Refresh

**Process:**
1. Identify 5–8 primary organic competitors (re-validate quarterly)
2. Pull top 1,000 ranking URLs from each
3. Identify:
   - Keywords they rank for where we don't (gap)
   - Keywords we rank for where they outrank us (defense)
4. Map gaps to existing content inventory
5. Feed output to editorial calendar for next quarter

**Tool:** Ahrefs Content Gap, Semrush Keyword Gap

### 3.6 CrUX Field Data Review

Beyond the CWV regression test (3.2), perform a **competitive CrUX benchmark**:
- Pull CrUX for top 3 organic competitors
- If our origin-level CWV is in "Poor" while competitors are "Good", CWV is likely a ranking factor we're losing on
- Document as quarterly KPI

---

## 4. Tool Reference & Usage Guide

### 4.1 Screaming Frog SEO Spider

**When to use:** Monthly crawl, on-demand deep dives
**License:** Desktop (one-time), or Cloud (subscription)

**Best practices for Next.js:**
- Always enable JS rendering for App Router sites
- Set custom user-agent to `Googlebot` for accurate rendering simulation
- Connect to GSC API (Settings → API Access) for live indexation data overlay
- Use **List Mode** for known URL audits (e.g., checking 500 specific URLs after a deploy)

**Top 5 reports we run monthly:**
1. Response Codes → 4xx/5xx filtered
2. Page Titles → Duplicates + Missing + Over 60 chars
3. Meta Descriptions → Missing on indexable pages
4. Images → Missing alt text + over 100KB
5. Hreflang → Errors + non-200 returns

### 4.2 Sitebulb

**When to use:** Quarterly architecture reviews, stakeholder visualization
**License:** Subscription

**Unique advantages over Screaming Frog:**
- Better visualization for non-technical stakeholders (use in exec reviews)
- Built-in **CWV integration** — pull live PSI data into crawl
- **Orphan page visualization** in graph view (excellent for architecture reviews)
- Schema validation built-in

### 4.3 PageSpeed Insights API

**Setup:**
1. Get API key from Google Cloud Console (free tier: 25,000 queries/month)
2. Store in Vercel environment variables
3. Run nightly against top 100 URLs by traffic

**Sample request:**
```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://agenticmarketingpro.com/&strategy=mobile&key=$PSI_KEY"
```

**CI integration:** Block deploys that regress LCP by > 500ms on top 20 pages (requires Lighthouse CI integration with Vercel preview deployments).

### 4.4 Supporting Tools

| Tool | Purpose | Frequency |
|---|---|---|
| Google Search Console | Indexation, manual actions, enhancements | Daily check (15 min) |
| Vercel Analytics | Real-user CWV, traffic anomalies | Weekly review |
| Ahrefs/Semrush | Backlinks, keyword gaps, content gaps | Weekly + quarterly deep |
| Better Stack / Datadog | Uptime, logs, synthetics | Real-time |
| Rich Results Test | Schema validation | On-deploy + monthly |

---

## 5. Emergency Response Procedures

### 5.1 Severity Classification

| Code | Definition | Examples | Response SLA |
|---|---|