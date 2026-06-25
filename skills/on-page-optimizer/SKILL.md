---
name: on-page-optimizer
description: "Audit and optimize on-page SEO elements for any published page including title tags, meta descriptions, H1-H3 structure, internal links, schema markup, image alt text, and content semantic density. Use when reviewing a newly published page, running a scheduled on-page audit, fixing pages flagged by the GSC Expert, or optimizing existing content for a target keyword. Produces a structured fix queue with before/after recommendations."
---

# On-Page Optimizer Agent

Audits and rewrites on-page elements for every published page.

## Quick Start

1. **Read target page:** Get the URL and content from `04-Content-Production/published-index.md` or client request.
2. **Read brief:** Check `04-Content-Production/briefs/[client]-[slug].md` for target keyword and SEO requirements.
3. **Run audit:** Check title, meta, H1–H3, schema, internal links, alt text, keyword density, semantic density.
4. **Write fix queue:** `01-Clients/[client]/technical-fix-queue.md`
5. **Apply fixes (if approved):** Update the page content with optimized elements.
6. **Log run:** `11-Ops/agent-logs/on-page-optimizer/YYYY-MM-DD-run-id.md`

## Audit Checklist (Per Page)

### Title Tag
- [ ] Length: 50–60 characters
- [ ] Target keyword at the beginning
- [ ] No brand name duplication (unless homepage)
- [ ] Unique across site (no duplicates)
- [ ] Compelling click-through value

### Meta Description
- [ ] Length: 150–160 characters
- [ ] Target keyword present (naturally)
- [ ] Clear value proposition
- [ ] Call-to-action or curiosity gap
- [ ] Unique across site

### H1 Tag
- [ ] Only one H1 per page
- [ ] Contains target keyword (or close variant)
- [ ] Descriptive of page content
- [ ] Not identical to title tag (variation is good)

### H2–H3 Structure
- [ ] Logical hierarchy: H1 → H2 → H3 (no skips)
- [ ] H2s cover subtopics related to target keyword
- [ ] H3s nest under appropriate H2s
- [ ] At least 2 H2s contain target keyword or semantic variant
- [ ] No orphan H3s (H3 without H2 parent)

### Internal Links
- [ ] Minimum 2 internal links to relevant pages
- [ ] Anchor text is descriptive (not "click here")
- [ ] Links to pillar pages where relevant
- [ ] No broken internal links
- [ ] No excessive links (>100 per page risks dilution)

### Schema Markup
- [ ] Appropriate schema type present (Article, Product, FAQ, HowTo, etc.)
- [ ] Required fields populated
- [ ] Valid JSON-LD format
- [ ] No conflicting schema types on same page

### Image Alt Text
- [ ] Every image has alt text
- [ ] Alt text describes the image (not just keyword-stuffed)
- [ ] Target keyword in 1–2 image alt texts (naturally)
- [ ] Images have descriptive filenames

### Keyword & Semantic Density
- [ ] Target keyword in first 100 words
- [ ] Keyword density: 1–2% (not >2.5%)
- [ ] Semantic variants and related terms present (LSI keywords)
- [ ] No keyword stuffing
- [ ] Natural language flow maintained

### Content Depth
- [ ] Word count matches brief specification
- [ ] Covers topic comprehensively vs. top-ranking competitors
- [ ] E-E-A-T signals: author bio, credentials, publish date, citations
- [ ] No thin content (<300 words on non-gateway pages)

## Fix Queue Format

Write fixes to `01-Clients/[client]/technical-fix-queue.md`:

```markdown
---
type: client-campaign-log
client: [client-name]
last_updated: YYYY-MM-DD
tags: [client/[name], type/technical-fixes]
---

# Technical Fix Queue — [Client]

## On-Page Fixes (from on-page-optimizer run YYYY-MM-DD)

| Page | Element | Current | Recommended | Priority | Status |
|---|---|---|---|---|---|
| /blog/slug | Title | [current] | [recommended] | High | Pending |
| /blog/slug | Meta desc | [current] | [recommended] | High | Pending |
| /blog/slug | H2 structure | [current] | [recommended] | Medium | Pending |
| /blog/slug | Internal links | [current] | [recommended] | Medium | Pending |
| /blog/slug | Schema | [current] | [recommended] | Low | Pending |

## Batch Actions
- [ ] Apply all high-priority fixes
- [ ] Re-crawl after fixes applied
- [ ] Verify in GSC
```

## Priority Rules

- **High:** Title tag, meta description, H1 — these directly impact CTR and rankings
- **Medium:** H2–H3 structure, internal links, schema — impact indexing and topical relevance
- **Low:** Alt text, image filenames, minor semantic tweaks — incremental improvements

## Escalation Rules

- **Client page has manual action in GSC:** Escalate immediately, do not proceed with on-page fixes until action resolved
- **Page is deindexed:** Escalate to tech-seo-auditor before on-page optimization
- **Keyword cannibalization detected:** Escalate to content-strategist for merge/redirect strategy
- **Schema errors block rich results:** High priority, fix within 24h

## Output Paths
- `01-Clients/[client]/technical-fix-queue.md`
- `04-Content-Production/published-index.md` (update with optimization status)
- `11-Ops/agent-logs/on-page-optimizer/YYYY-MM-DD-run-id.md`
