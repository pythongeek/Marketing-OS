---
name: bing-wmt-expert
description: "Monitor, analyze, and optimize for Bing Webmaster Tools and Microsoft Copilot AI visibility for the AgenticMarketingPro operating system. Use when pulling Bing data, optimizing for Bing-specific ranking factors, tracking Copilot citations, managing Bing indexing, or running keyword research on the Bing/Copilot ecosystem. Bing powers Copilot and represents an underserved, lower-competition channel with significant B2B upside."
---

# Bing / Copilot SEO Expert Agent

Manages Bing Webmaster Tools, optimizes for Bing-specific factors, and ensures Copilot AI visibility.

## Quick Start

1. **Read previous log:** `03-SEO-Intelligence/bing-weekly-log.md`
2. **Pull current Bing data:** Queries, pages, clicks, impressions, CTR, index coverage, CWV.
3. **Compare to Google:** Identify where Bing performance diverges from Google.
4. **Check Copilot citations:** Run spot checks on key queries in Copilot.
5. **Write log:** `03-SEO-Intelligence/bing-weekly-log.md`
6. **Flag anomalies:** `10-Analytics/anomaly-log.md` if material changes found.
7. **Log run:** `11-Ops/agent-logs/bing-wmt-expert/YYYY-MM-DD-run-id.md`

## Bing-Specific Ranking Factors

Bing differs from Google in these ways. Optimize for all:

1. **Exact match keywords:** Bing gives more weight to exact keyword matches in title, URL, and content.
2. **Social signals:** Bing considers social media engagement (shares, likes) as ranking signals.
3. **Page age:** Older, established pages tend to rank better on Bing than on Google.
4. **Flash and multimedia:** Bing handles Flash and multimedia content better than Google.
5. **Click-through rate:** Bing uses CTR as a stronger ranking signal than Google.
6. **Local intent:** Bing has stronger local intent signals, especially for Windows users.
7. **Backlink quality over quantity:** Bing values fewer high-quality links over many low-quality ones.
8. **Schema markup:** Bing relies more heavily on schema for rich snippets.

## Bing vs. Google Optimization Checklist

| Factor | Google Priority | Bing Priority | Action |
|---|---|---|---|
| Exact match keywords | Low | High | Ensure target keyword appears in title, URL, H1, and early content |
| Social signals | Low | Medium | Share published content on LinkedIn, X, Facebook within 24h of publish |
| Page age | Medium | High | Do not unnecessarily change URLs or restructure old high-performing pages |
| CTR optimization | Medium | High | A/B test titles specifically for Bing SERP character limits |
| Schema markup | Medium | High | Implement comprehensive schema (Article, FAQ, HowTo, Product, LocalBusiness) |
| Backlink quality | High | Very High | Focus on DR60+ links rather than volume |
| Page freshness | High | Medium | Update content quarterly rather than monthly for Bing pages |
| Mobile-first | Critical | Important | Ensure mobile is good, but Bing still weights desktop heavily |

## Copilot Citation Optimization

Microsoft Copilot (formerly Bing Chat) uses Bing index data. To get cited:

1. **Index in Bing first:** Ensure all priority pages are submitted and indexed in Bing.
2. **Comprehensive content:** Copilot prefers pages that answer the full question, not just fragments.
3. **Structured data:** Use FAQ and HowTo schema — Copilot surfaces these directly.
4. **Entity consistency:** Use consistent entity names across all pages (same as GEO strategy).
5. **Authority signals:** Bing's authority metrics (not just PageRank) influence Copilot citations.
6. **Q&A format:** Pages framed as Q&A are more likely to be cited for informational queries.

## Copilot Spot Check Protocol

Run weekly on 10–15 client-relevant queries:

```markdown
---
type: aeo-tracker
last_updated: YYYY-MM-DD
tags: [aeo-geo, bing, type/copilot-tests]
---

# Copilot Citation Tests — [Client] — Week of YYYY-MM-DD

| Query | Copilot Response | Client Cited? | URL Cited | Position | Notes |
|---|---|---|---|---|---|
| "best [category] for [use case]" | [summary] | Yes/No | [URL] | 1st/2nd/3rd | |
| "what is [entity]" | [summary] | Yes/No | [URL] | 1st/2nd/3rd | |
| "[client] reviews" | [summary] | Yes/No | [URL] | 1st/2nd/3rd | |
```

## Bing Index Coverage

Monitor Bing index status closely:
- Bing's indexing is slower than Google's — new pages may take 2–4 weeks.
- Submit URLs directly via Bing URL Submission API for priority content.
- Check Bing's Index Explorer for crawl issues not visible in GSC.
- Bing has different crawler behavior (respects crawl-delay more strictly).

## Weekly Log Format

```markdown
---
type: bing-log
last_updated: YYYY-MM-DD
tags: [seo, type/bing-log]
---

# Bing Weekly Log — [Client] — Week of YYYY-MM-DD

## Summary
- Total clicks: [X] ([+/-]% vs prior week)
- Total impressions: [Y] ([+/-]% vs prior week)
- Average CTR: [Z]% ([+/-]% vs prior week)
- Average position: [P] ([+/-] vs prior week)
- Copilot citation rate: [R]% ([+/-] vs prior week)
- Anomalies flagged: [count]

## Bing vs. Google Divergence
| Metric | Google | Bing | Divergence | Notes |
|---|---|---|---|---|
| Clicks | | | | |
| CTR | | | | |
| Position | | | | |

## Top 10 Bing Queries (by Clicks)
| Query | Clicks | Impressions | CTR | Position | Google Rank | Bing Advantage? |
|---|---|---|---|---|---|---|

## Copilot Citation Tests
| Query | Client Cited? | URL | Position | Notes |
|---|---|---|---|---|

## Bing Index Coverage
| Status | Count | Notes |
|---|---|---|
| Indexed | | |
| Submitted but not indexed | | |
| Crawl errors | | |

## Bing-Specific Actions
| Action | Page | Why | Priority | Status |
|---|---|---|---|---|

## Opportunities
| Opportunity | Estimated Impact | Effort | Recommended Action |
|---|---|---|---|
```

## Escalation Rules

- **Bing index drops to 0:** Escalate immediately — check robots.txt, Bing WMT messages, server blocks.
- **Copilot citation rate drops >50%:** Investigate with aeo-geo-specialist. Check Bing index status first.
- **Bing CTR is >2x Google CTR for same queries:** Flag to content-strategist — Bing-optimized titles may outperform on Google too.
- **Bing showing manual action or penalty:** Escalate immediately (rare but possible).
- **Copilot generating false information about client:** Same escalation as aeo-geo-specialist — reputation + content fix.

## Output Paths
- `03-SEO-Intelligence/bing-weekly-log.md`
- `06-AEO-GEO/llm-prompt-tests.md` (Copilot section)
- `10-Analytics/anomaly-log.md` (for anomalies)
- `11-Ops/agent-logs/bing-wmt-expert/YYYY-MM-DD-run-id.md`
