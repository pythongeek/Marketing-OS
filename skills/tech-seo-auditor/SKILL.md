---
name: tech-seo-auditor
description: "Crawl site architecture, audit JavaScript rendering, validate structured data, analyze page speed, check mobile usability, and review log files for the AgenticMarketingPro operating system. Use when running a monthly technical health audit, investigating indexation issues, validating schema markup, diagnosing Core Web Vitals regressions, or responding to site health alerts. Produces technical health reports with prioritized fix queues."
---

# Technical SEO Auditor Agent

Crawls site architecture, validates structured data, checks speed, mobile, and logs.

## Quick Start

1. **Read previous audit:** `03-SEO-Intelligence/technical-audit-log.md`
2. **Read anomaly log:** `10-Analytics/anomaly-log.md` for open technical issues.
3. **Run audit:** Site crawl, schema validation, CWV check, mobile test, log analysis.
4. **Write findings:** `03-SEO-Intelligence/technical-audit-log.md`
5. **Queue fixes:** Write to `01-Clients/[client]/technical-fix-queue.md`.
6. **Log run:** `11-Ops/agent-logs/tech-seo-auditor/YYYY-MM-DD-run-id.md`

## Monthly Audit Checklist

### 1. Crawlability & Indexation
- [ ] robots.txt is valid and not blocking critical content
- [ ] XML sitemap is valid, complete, and submitted to GSC/Bing
- [ ] No orphan pages (pages with 0 internal links)
- [ ] No crawl traps (infinite pagination, faceted nav without canonicals)
- [ ] No noindex on pages that should rank
- [ ] Canonical tags are correct and self-referencing where appropriate
- [ ] Pagination uses rel=next/prev or proper canonical handling
- [ ] Hreflang is correct (if multi-language)

### 2. JavaScript Rendering
- [ ] Key content is visible in rendered HTML (not JS-dependent)
- [ ] Meta tags (title, description, canonical) are in static HTML
- [ ] Internal links are <a href> not JS onclick
- [ ] Lazy loading doesn't block LCP images
- [ ] No hydration errors that block content

### 3. Structured Data
- [ ] All required schema fields are populated
- [ ] No conflicting schema types on same page
- [ ] JSON-LD is valid (test with Google's Rich Results Test)
- [ ] BreadcrumbList schema present on non-homepage pages
- [ ] Organization schema present on homepage
- [ ] Article/NewsArticle schema on blog posts (with author, date)
- [ ] Product schema on product pages (with price, availability, reviews)
- [ ] FAQ/HowTo schema where applicable
- [ ] No review markup on non-product pages (violates guidelines)

### 4. Core Web Vitals
- [ ] LCP (Largest Contentful Paint) < 2.5s
- [ ] INP (Interaction to Next Paint) < 200ms
- [ ] CLS (Cumulative Layout Shift) < 0.1
- [ ] TTFB (Time to First Byte) < 600ms
- [ ] No render-blocking resources above the fold
- [ ] Images are properly sized and compressed (WebP where possible)
- [ ] Fonts are preloaded or use font-display: swap

### 5. Mobile Usability
- [ ] No "Content wider than screen" errors in GSC
- [ ] Text is readable without zooming (font size ≥16px)
- [ ] Tap targets are appropriately sized (≥48px)
- [ ] Viewport meta tag is correct
- [ ] No intrusive interstitials on mobile
- [ ] hamburger menu works, footer links accessible

### 6. Security
- [ ] HTTPS enforced (no mixed content warnings)
- [ ] HSTS header present
- [ ] Security headers: X-Content-Type-Options, X-Frame-Options, Referrer-Policy
- [ ] No malware or security issues in GSC
- [ ] CSP (Content Security Policy) defined (if applicable)

### 7. Log File Analysis (if available)
- [ ] Crawl budget is not wasted on 404s, redirects, or parameter pages
- [ ] Important pages are crawled frequently
- [ ] New content is discovered within 48 hours
- [ ] No bot anomalies (aggressive scrapers, fake bots)

## Audit Report Format

```markdown
---
type: audit-log
client: [client-name]
last_updated: YYYY-MM-DD
tags: [client/[name], type/technical-audit]
---

# Technical SEO Audit — [Client] — YYYY-MM-DD

## Overall Health Score: [X/100]

## Critical Issues (Fix within 24h)
| Issue | Pages Affected | Impact | Fix | Owner |
|---|---|---|---|---|

## High Priority (Fix within 1 week)
| Issue | Pages Affected | Impact | Fix | Owner |
|---|---|---|---|---|

## Medium Priority (Fix within 1 month)
| Issue | Pages Affected | Impact | Fix | Owner |
|---|---|---|---|---|

## Low Priority (Fix when convenient)
| Issue | Pages Affected | Impact | Fix | Owner |
|---|---|---|---|---|

## Core Web Vitals
| Metric | Mobile | Desktop | Status |
|---|---|---|---|
| LCP | [value] | [value] | [Pass/Fail] |
| INP | [value] | [value] | [Pass/Fail] |
| CLS | [value] | [value] | [Pass/Fail] |

## Schema Validation
| Page Type | Schema | Valid? | Errors |
|---|---|---|---|

## Comparison to Last Audit
- Issues resolved: [count]
- New issues: [count]
- Regressions: [count]
```

## Priority Scoring

Score each issue: `Impact × Urgency × Effort`

| Impact | Score | Urgency | Score | Effort | Score |
|---|---|---|---|---|---|
| Deindexation risk | 5 | Fix within 24h | 5 | 1 hour | 1 |
| Ranking drop | 4 | Fix within 1 week | 4 | 1 day | 2 |
| CWV failure | 3 | Fix within 1 month | 3 | 1 week | 3 |
| Minor issue | 2 | Fix when convenient | 2 | 1 month | 4 |
| Nice to have | 1 | Backlog | 1 | >1 month | 5 |

**Priority = Impact × Urgency / Effort. Higher = fix first.**

## Escalation Rules

- **Manual action in GSC:** Escalate immediately. Do not proceed with other fixes until resolved.
- **Site completely deindexed:** Critical escalation. Check robots.txt, sitemap, security issues.
- **CWV all fail on mobile:** High priority — impacts rankings and UX.
- **Schema errors on >20% of pages:** Investigate template or CMS issue.
- **Log files show aggressive bot consuming crawl budget:** Escalate to developer for robots.txt / WAF rules.

## Output Paths
- `03-SEO-Intelligence/technical-audit-log.md`
- `01-Clients/[client]/technical-fix-queue.md`
- `10-Analytics/anomaly-log.md` (for critical findings)
- `11-Ops/agent-logs/tech-seo-auditor/YYYY-MM-DD-run-id.md`
