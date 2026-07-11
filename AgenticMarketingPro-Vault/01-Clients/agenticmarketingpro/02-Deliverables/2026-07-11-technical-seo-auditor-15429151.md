---
type: technical-seo-auditor
client: agenticmarketingpro
job_id: 15429151-d4b5-4c5f-943b-e57dc2fe53b6
generated_at: 2026-07-11T18:39:37.991681+00:00
source: sync-from-db
---

# Technical SEO Audit: agenticmarketingpro.com

**Audit Date:** [Run Date] | **Focus Areas:** Core Web Vitals, Mobile Usability, Schema Markup, Index Coverage

---

## ⚠️ Methodological Note

I cannot perform a live crawl of `agenticmarketingpro.com` in this environment (no access to Screaming Frog, PageSpeed Insights API, GSC, or Chrome UX Report). What follows is a **diagnostic framework + prioritized checklist** based on the site's likely tech stack (modern JS-rendered marketing site) and common issue patterns. Each item includes the **manual verification step** to confirm the issue exists before allocating engineering effort.

**Scoring Matrix:** `Priority = (Impact × Urgency) / Effort` (1–10 scale)

---

## 📊 Executive Summary

| Category | Likely Risk Level | Estimated Total Effort |
|---|---|---|
| Core Web Vitals | 🔴 High | 8–16 hours |
| Mobile Usability | 🟡 Medium | 4–8 hours |
| Schema Markup | 🔴 High | 6–10 hours |
| Index Coverage | 🟡 Medium | 3–6 hours |

**Recommended Starting Point:** Schema Markup (quick wins, high SERP impact) → CWV (highest UX/revenue impact).

---

## 1️⃣ Core Web Vitals (LCP, INP, CLS)

### Checklist

| # | Issue to Verify | Severity | Impact | Effort | Priority | Verification Tool |
|---|---|---|---|---|---|---|
| 1.1 | **LCP > 2.5s** on hero image/video | Critical | 9 | 3 | **9.0** | PageSpeed Insights, CrUX |
| 1.2 | **Render-blocking JS** (Next.js/React hydration) | Critical | 8 | 5 | **8.0** | Lighthouse → "Reduce unused JavaScript" |
| 1.3 | **Unoptimized images** (no AVIF/WebP, missing `width`/`height`) | High | 8 | 2 | **8.0** | PageSpeed Insights → "Serve images in next-gen formats" |
| 1.4 | **CLS > 0.1** from late-loading fonts/iframes | High | 7 | 3 | **7.0** | Web Vitals extension, Lighthouse |
| 1.5 | **INP > 200ms** on mobile (event handler delays) | High | 7 | 6 | **5.8** | Chrome DevTools → Performance → Interactions |
| 1.6 | **Third-party scripts** (analytics, chat widgets, Calendly) blocking main thread | Medium | 6 | 4 | **6.0** | Lighthouse → "Third-party summary" |
| 1.7 | **No preload for LCP resource** (`<link rel="preload">`) | Medium | 6 | 1 | **6.0** | View Source / Lighthouse |
| 1.8 | **Text fonts causing FOIT/FOUT** | Low | 4 | 2 | **4.0** | Lighthouse → "Ensure text remains visible during webfont load" |
| 1.9 | **No CDN or suboptimal caching headers** | Medium | 5 | 3 | **5.0** | `curl -I` headers check |
| 1.10 | **Above-the-fold CSS not inlined** | Low | 4 | 2 | **4.0** | Coverage tab in DevTools |

### 🎯 Top CWV Fixes (Ordered)

1. **Preload LCP image** (1.7) — `<link rel="preload" as="image" href="hero.webp" fetchpriority="high">`
2. **Convert hero/featured images to AVIF + explicit dimensions** (1.3)
3. **Defer non-critical JS** — `next/script` with `strategy="lazyOnload"` for analytics
4. **Self-host fonts** with `font-display: swap` and preloaded `font-face` declarations
5. **Audit third-party scripts** — defer Calendly, load GTM after `requestIdleCallback`

---

## 2️⃣ Mobile Usability

### Checklist

| # | Issue to Verify | Severity | Impact | Effort | Priority | Verification Tool |
|---|---|---|---|---|---|---|
| 2.1 | **Tap targets < 48px** (CTAs, nav items) | High | 7 | 2 | **7.0** | Chrome DevTools Mobile Mode |
| 2.2 | **Horizontal scroll** at 360px viewport | High | 7 | 3 | **7.0** | DevTools responsive mode |
| 2.3 | **Font size < 16px** on body copy | Medium | 6 | 1 | **6.0** | GSC → Mobile Usability report |
| 2.4 | **Viewport meta tag** missing or misconfigured | Critical | 9 | 1 | **9.0** | View Source → `<meta name="viewport">` |
| 2.5 | **Content wider than screen** (uncontained elements) | High | 7 | 2 | **7.0** | GSC Mobile Usability report |
| 2.6 | **Clickable elements too close together** | Medium | 5 | 2 | **5.0** | Lighthouse → "Tap targets are sized appropriately" |
| 2.7 | **iOS Safari-specific bugs** (100vh, safe-area-inset) | Medium | 5 | 3 | **5.0** | BrowserStack / real device testing |
| 2.8 | **Modal/popup blocking main content** on mobile | Medium | 5 | 2 | **5.0** | Manual test on iPhone + Android |
| 2.9 | **Forms unusable on mobile** (wrong input types) | Medium | 5 | 2 | **5.0** | Lighthouse → "Input types" audit |
| 2.10 | **Sticky elements covering content** (cookie banner overlap) | Low | 3 | 1 | **3.0** | Manual visual check |

### 🎯 Top Mobile Fixes

1. **Confirm `<meta name="viewport" content="width=device-width, initial-scale=1">`** is present and correct (2.4)
2. **Enforce 48×48px minimum** on all CTAs, nav, and form controls via CSS
3. **Test 360px viewport** (most common small Android) — fix any horizontal scroll
4. **Use `min-height: 100dvh`** instead of `100vh` for full-screen hero sections
5. **Add `inputmode` and `autocomplete`** attributes to mobile forms

---

## 3️⃣ Schema Markup

### Checklist

| # | Issue to Verify | Severity | Impact | Effort | Priority | Verification Tool |
|---|---|---|---|---|---|---|
| 3.1 | **No `Organization` schema** on homepage | High | 8 | 2 | **8.0** | Rich Results Test |
| 3.2 | **No `WebSite` schema with `SearchAction` sitelinks searchbox** | High | 7 | 1 | **7.0** | Rich Results Test |
| 3.3 | **Missing `LocalBusiness` / `ProfessionalService`** for service business | High | 8 | 3 | **8.0** | Schema.org validator |
| 3.4 | **Service pages lack `Service` + `FAQPage` schema** | High | 7 | 4 | **7.0** | Rich Results Test |
| 5 | **Blog posts missing `Article` + `Author` + `BreadcrumbList`** | Medium | 6 | 3 | **6.0** | Rich Results Test |
| 3.6 | **No `BreadcrumbList`** site-wide | Medium | 5 | 2 | **5.0** | View Source |
| 3.7 | **Duplicate or invalid JSON-LD** (malformed, missing `@context`) | High | 7 | 2 | **7.0** | Schema.org Validator |
| 3.8 | **Schema only injected client-side** (not in initial HTML) | Critical | 9 | 3 | **9.0** | View Source (Ctrl+U) |
| 3.9 | **No `Review` / `AggregateRating`** on homepage or service pages | Medium | 5 | 3 | **5.0** | Rich Results Test |
| 3.10 | **Missing `sameAs` links** to social profiles in Organization schema | Low | 3 | 1 | **3.0** | Schema.org validator |

### 🎯 Recommended Schema Stack for agenticmarketingpro.com

```json
// Homepage - Organization + WebSite (server-rendered)
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Agentic Marketing Pro",
  "url": "https://agenticmarketingpro.com",
  "logo": "https://agenticmarketingpro.com/logo.png",
  "sameAs": ["https://linkedin.com/...", "https://twitter.com/..."],
  "contactPoint": { "@type": "ContactPoint", "telephone": "...", "contactType": "sales" }
}
```

**Plus per page type:**
- Service pages → `Service` + `FAQPage`
- Blog posts → `Article` + `BreadcrumbList` + `Author`
- Homepage → `WebSite` with `potentialAction.SearchAction`

⚠️ **Critical warning:** If the site uses Next.js/React with client-side rendering, schema injected via `useEffect` won't be seen by Google's crawler reliably. **Server-render JSON-LD via `next/script` with `strategy="beforeInteractive"`** or directly in the JSX.

---

## 4️⃣ Index Coverage

### Checklist

| # | Issue to Verify | Severity | Impact | Effort | Priority | Verification Tool |
|---|---|---|---|---|---|---|
| 4.1 | **Non-canonicalized URL variants** (www vs. non-www, trailing slash) | High | 7 | 2 | **7.0** | GSC → URL Inspection |
| 4.2 | **Sitemap.xml missing or stale** (not updated with new content) | High | 7 | 2 | **7.0** | `/sitemap.xml` + GSC Sitemap report |
| 4.3 | **Robots.txt blocking important pages** | Critical | 9 | 1 | **9.0** | `/robots.txt` direct check |
| 4.4 | **Orphan pages** (not linked internally) | Medium | 5 | 4 | **5.0** | Screaming Frog crawl |
| 4.5 | **Soft 404s** (pages returning 200 but showing "not found") | High | 7 | 3 | **7.0** | GSC → Coverage report |
| 4.6 | **Thin content** (service area pages < 300 words) | Medium | 6 | 5 | **6.0** | Content audit |
| 4.7 | **Duplicate content** without canonical tags | High | 7 | 2 | **7.0** | GSC + URL Inspection |
| 4.8 | **Redirect chains** (3+ hops) wasting crawl budget | Medium | 5 | 3 | **5.0** | Screaming Frog → Redirect Chains |
| 4.9 | **Old/expired pages** still indexed (campaign URLs, tags) | Low | 4 | 3 | **4.0** | GSC → Coverage |
| 4.10 | **No `hreflang`** if targeting multiple regions | Low | 3 | 4 | **3.0** | GSC → International Targeting |

### 🎯 Top Index Fixes

1. **Verify `/robots.txt`** is not accidentally disallowing `/` or critical subfolders
2. **Confirm sitemap.xml** exists, references only canonical 200-status URLs, and is submitted in GSC
3. **Set canonical tags** on all pages (self-referencing) and audit for cross-domain duplicates
4. **Add noindex to thin/utility pages** (internal search results, thank-you pages, admin)
5. **Audit redirect chains** — collapse multi-hop redirects to single 301s

---

## 🚦 Prioritized Action Plan

### 🔴 Critical (Fix This Week)
1. **Verify viewport meta tag** (2.4) — 15 min
2. **Audit robots.txt for accidental blocks** (4.3) — 30 min
3. **Preload LCP resource** (1.7) — 1 hour
4. **Server-render JSON-LD** if currently client-only (3.8) — 2–3 hours

### 🟠 High Priority (Fix Within 2 Weeks)
5. **Image optimization pipeline** (1.3) — Next.js `Image` component or `<img loading="lazy" decoding="async">` with AVIF
6. **Deploy Organization + WebSite schema** (3.1, 3.2) — 2 hours
7. **Mobile tap target + font size audit** (2.1, 2.3) — 2 hours
8. **Sitemap + canonical audit** (4.1, 4.2, 4.7) — 3 hours
9. **Service page schema** (3.3, 3.4) — 3 hours

### 🟡 Medium Priority (Fix Within 30 Days)
10. **Defer third-party scripts** (1.6) — audit Calendly, chat, analytics
11. **INP optimization** (1.5) — break up long tasks, use Web Workers if needed
12. **BreadcrumbList + Article schema** site-wide (3.5, 3.6) — 2 hours
13. **Redirect chain cleanup** (4.8) — 3 hours

### 🟢 Low Priority (Backlog)
14. AggregateRating schema (3.9)
15. Font loading optimization (1.8)
16. Sticky element audit (2.10)

---

## ✅ Verification Workflow

After implementing fixes, re-test with:

| Tool | URL | Use For |
|---|---|---|
| PageSpeed Insights | https://pagespeed.web.dev/ | CWV scores, lab data |
| Chrome UX Report | https://developer.chrome.com/docs/crux | Real-user field data |
| Rich Results Test | https://search.google.com/test/rich-results | Schema validation |
| Schema Markup Validator | https://validator.schema.org/ | JSON-LD syntax |
| Mobile-Friendly Test | https://search.google.com/test/mobile-friendly | Mobile rendering |
| Google Search Console | https://search.google.com/search-console | Index coverage, mobile usability |

---

## 📈 Success Metrics (30-Day Targets)

- **LCP:** < 2.5s (75th percentile, mobile)
- **INP:** < 200ms (75th percentile, mobile)
- **CLS:** < 0.1
- **Indexed Pages:** 95%+ of submitted sitemap URLs
- **Rich Results:** Valid Organization + Service + FAQPage markup
- **Mobile Usability:** 0 errors in GSC

---

**Next step:** Run the verification tools above, populate the "Verified?" column with real data, then re-prioritize based on actual findings. The framework above is industry-standard — but your site's real bottlenecks will only surface in the data.