---
name: pseo-engineer
description: "Build and manage programmatic SEO pipelines that generate 100s to 1000s of unique landing pages from structured data templates. Use when creating location-based service pages, comparison pages, tool pages, or any data-driven page architecture. Covers data source management, template design, quality guardrails, batch publishing, and post-publish monitoring. Part of the AgenticMarketingPro operating system."
---

# Programmatic SEO Engineer

Generates pages at scale from structured data. Owns the pSEO pipeline from data to CMS publish.

## Quick Start

1. **Read data sources:** `05-Programmatic-SEO/data-sources.md`
2. **Read quality guardrails:** `05-Programmatic-SEO/quality-guardrails.md`
3. **Read publish log:** `05-Programmatic-SEO/publish-log.md`
4. **Design page template:** Define the page structure, variables, and unique elements.
5. **Generate batch:** Create 50–500 pages per batch (max 500 without HITL Gate 5).
6. **QA review:** Run qa-pipeline skill on sample pages.
7. **Publish or queue:** Write to CMS or queue for human approval.
8. **Log:** `05-Programmatic-SEO/publish-log.md` + `11-Ops/agent-logs/pseo-engineer/YYYY-MM-DD-run-id.md`.

## pSEO Architecture Types

### Type 1: Location × Service
**Example:** "Plumber in [City], [State]" for 500 cities
- Data: City name, state, population, local service areas, zip codes
- Variables: City, state, nearby cities, local regulations, service hours
- Unique elements per page: City-specific intro, local landmarks, neighborhood mentions, service area map

### Type 2: Comparison / List
**Example:** "Best [Tool] for [Use Case]" or "Top 10 [Category] in [Year]"
- Data: Tool names, features, pricing, ratings, categories
- Variables: Tool attributes, comparison criteria, rankings
- Unique elements per page: Dynamic comparison tables, pros/cons per tool, pricing widgets

### Type 3: Data / Tool
**Example:** "[Metric] Calculator", "[Industry] Statistics [Year]"
- Data: Formulas, datasets, time-series data
- Variables: Input parameters, calculated outputs, data ranges
- Unique elements per page: Interactive calculator, data visualizations, methodology sections

### Type 4: Category × Attribute
**Example:** "[Product] for [Audience] with [Feature]"
- Data: Product catalog, audience segments, feature lists
- Variables: Product names, audience descriptors, feature highlights
- Unique elements per page: Curated product lists, use-case scenarios, compatibility info

## Quality Guardrails (Non-Negotiable)

Every pSEO page must pass these before publish:

1. **Minimum unique content:** ≥70% of page content must be unique vs. other pSEO pages (not just variable swap).
2. **Minimum word count:** ≥500 words per page (unless pure tool/interactive).
3. **Human-written intro:** First 150 words must be human-quality (not template-generated), or pass qa-pipeline Check 1 (brand voice) ≥4/5.
4. **Internal linking:** Every pSEO page must link to 2+ other pSEO pages and 1+ pillar page.
5. **No thin variable swaps:** Cannot just swap [City] and call it a new page. Must include city-specific context, data, or angles.
6. **Schema markup:** Every pSEO page gets appropriate schema (LocalBusiness, Product, FAQ, etc.).
7. **Canonical + pagination:** Proper canonical tags. No infinite pagination traps.
8. **Load speed:** Core Web Vitals must pass on template (LCP <2.5s, INP <200ms).
9. **No doorway pages:** Every page must provide standalone value. No "click here to see real content" intermediates.
10. **H1 uniqueness:** Every page must have a unique H1 (no two pages share identical H1).

## Page Template Structure

```markdown
---
# Page Template: [Template Name]

## Variables
| Variable | Source | Example |
|---|---|---|
| {{city}} | data-sources.md | "Austin" |
| {{state}} | data-sources.md | "Texas" |
| {{population}} | data-sources.md | "978,908" |
| {{service}} | data-sources.md | "emergency plumbing" |

## Page Structure

### H1
[service] in [city], [state] — [value prop]

### Intro (150+ words, unique per page)
[Context about city + service + why this matters locally]

### H2: What to Expect
[Service details specific to city/region]

### H2: Common [Service] Issues in [City]
[City-specific problems, climate factors, local regulations]

### H2: Service Areas
[List of neighborhoods/zip codes served]

### H2: Why Choose Us
[Differentiation, social proof, local credentials]

### H2: FAQ
[3–5 city-specific FAQs with schema]

### CTA
[City-specific call-to-action]

### Schema
[LocalBusiness or Service schema with city-specific data]
```

## Data Source Management

Maintain `05-Programmatic-SEO/data-sources.md`:

```markdown
---
type: pseo-data
last_updated: YYYY-MM-DD
tags: [pseo, type/data-sources]
---

# Data Sources

## Source: [Name]
- **Type:** Airtable / Google Sheets / API / Database
- **Location:** [URL or path]
- **Refresh cadence:** [daily / weekly / monthly]
- **Last refresh:** YYYY-MM-DD
- **Row count:** [number]
- **Key fields:** [list]
- **Quality status:** [clean / needs cleaning / stale]
```

## Publish Log Format

```markdown
---
type: pseo-log
last_updated: YYYY-MM-DD
tags: [pseo, type/publish-log]
---

# Publish Log

## Batch: [batch-id]
- **Date:** YYYY-MM-DD
- **Template:** [template name]
- **Pages generated:** [count]
- **Pages published:** [count]
- **Pages queued (HITL):** [count]
- **QA status:** [pass / fail / partial]
- **HITL Gate 5:** [approved / pending]
- **Indexation status:** [X% indexed after 14 days]

## Performance (30 days post-publish)
| Page Pattern | Impressions | Clicks | Avg Position | CTR |
|---|---|---|---|---|
```

## HITL Gate 5: pSEO Batch Approval

Any batch >50 pages requires strategist approval. Present:
1. Template design and variable list
2. Sample of 3 fully generated pages (beginning, middle, end of data range)
3. QA scores on sample
4. Expected indexation rate and traffic estimate
5. Cannibalization risk assessment

## Escalation Rules

- **Batch >50 pages:** HITL Gate 5 mandatory
- **Batch >200 pages:** Requires technical SEO review for crawl budget
- **Indexation rate <50% after 30 days:** Investigate — likely thin content or technical issue
- **Cannibalization with existing pages:** Merge, redirect, or differentiate before publish
- **Data source error (missing values, duplicates):** Fix data before generating pages

## Output Paths
- `05-Programmatic-SEO/data-sources.md`
- `05-Programmatic-SEO/page-templates/[template-name].md`
- `05-Programmatic-SEO/publish-log.md`
- `05-Programmatic-SEO/quality-guardrails.md`
- `11-Ops/agent-logs/pseo-engineer/YYYY-MM-DD-run-id.md`
