---
type: pseo-guardrails
last_updated: 2026-01-20
tags: [pseo, type/guardrails]
---

# Programmatic SEO — Quality Guardrails

> Without these, pSEO = spam. Every batch must pass these checks before publish.

## Pre-publish checks (auto-run by Programmatic SEO Engineer Agent)
1. **Deduplication:** No two pages can have >40% content similarity (cosine similarity on embeddings)
2. **Minimum content threshold:** Every page must have ≥800 words of unique content (excluding boilerplate)
3. **Unique title + meta:** Every page must have a unique title tag and meta description
4. **Schema validity:** JSON-LD must pass Schema.org validator
5. **Internal linking:** Every page must link to ≥3 other pages (pillar + 2 related)
6. **No thin pages:** Pages with <200 words of body content are rejected
7. **Image requirements:** Every page must have ≥1 image with alt text containing the target keyword
8. **URL structure:** URLs must be ≤75 characters, kebab-case, no stop words

## Indexation budget management
- Max 200 pages per batch (Google's crawl tolerance)
- Submit via GSC Indexing API + IndexNow simultaneously
- Wait 7 days between batches for same property
- Monitor indexation rate; if <70% after 30 days, pause + investigate

## Cannibalization monitoring
- Track keyword overlaps between pSEO pages and pillar content
- If a pSEO page outranks a pillar for the same keyword: pause pSEO page + redirect to pillar
- Weekly review by On-Page Optimizer Agent

## Content quality scoring (Surfer SEO API)
- Every pSEO page must achieve ≥60 Surfer score before publish
- Pages scoring 40-60: auto-revise once
- Pages scoring <40: reject + flag template for review

## Kill switch
- If a pSEO template's pages collectively underperform (avg <5 sessions/month after 60 days), the template is paused
- A "paused template" = no new pages generated, existing pages kept live unless individually flagged
