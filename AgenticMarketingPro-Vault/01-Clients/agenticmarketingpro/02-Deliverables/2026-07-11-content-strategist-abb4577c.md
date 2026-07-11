---
type: content-strategist
client: agenticmarketingpro
job_id: abb4577c-d7e3-4255-a6f8-7a1121964b4b
generated_at: 2026-07-11T16:47:03.287692+00:00
source: sync-from-db
---

# Master SEO Operations Cadence Calendar
**Client:** agenticmarketingpro
**Audience:** SEO operations team + agency leadership
**Version:** 1.0 (Master Playbook)
**Owner:** SEO Operations Lead
**Document type:** Repeatable operational SOP

---

## 📋 How to Use This Document

This calendar is a **living SOP** that governs every recurring SEO activity across client accounts and internal properties. Each task row includes: **purpose · owner · tool stack · step-by-step process · time estimate · output format · escalation trigger.**

> **Working assumption:** 15–30 active client domains + 1 internal brand property. Adapt volumes (HARO sends, mentions, backlink deltas) by client tier.

---

# ⏰ SECTION 1 — DAILY CADENCE (15–20 minutes, 7 days/week)

**Owner:** Rotating daily monitor (team rota) → escalation to SEO Lead if flagged.
**When:** 8:30–8:50 AM local time, *before* client-facing work begins.
**Block time:** 15 routine + 5 buffer for action.

---

### 1.1 SEO News & Algorithm Monitoring · 4 min

| Field | Detail |
|---|---|
| **Purpose** | Catch Google/Bing algo shifts within 24–48 hrs; protect client rankings. |
| **Tools** | Google Search Central blog RSS, Search Engine Roundtable, Search Engine Land, Barry Schwartz X feed, Moz algorithm weather report, X Lists ("SEO News", "Google Algo"), SparkToro. |
| **Process** | (1) Skim Search Central + SE Roundtable for confirmed updates. (2) Check Barry Schwartz X. (3) Cross-check Moz algo weather for category volatility. (4) Cross-reference with client GSC impressions (look for >15% day-over-day swings). |
| **Output** | Slack `#seo-ops-daily` post: *"No notable updates"* OR thread with updates + 2 affected clients + recommended action. |
| **Escalation** | Confirmed core update → ping SEO Lead within 30 min. |

### 1.2 Site Uptime & Indexability Check · 3 min

| Field | Detail |
|---|---|
| **Purpose** | Catch downtime, 5xx spikes, deindexation immediately. |
| **Tools** | UptimeRobot (free tier acceptable), Better Uptime, GSC "Page Indexing" widget, Pingdom public status page. |
| **Process** | (1) Glance at UptimeRobot dashboard (or summary email). (2) Open GSC → Settings → Page indexing count vs. yesterday. (3) Spot-check 3 hero pages on Bing site:search. |
| **Output** | Single line in Slack thread. Auto-PagerDuty/Opsgenie for >5 min outage. |
| **Escalation** | Any index count drop >5% or uptime <99.5% w/w → §immediate client flag-out via Account Lead. |

### 1.3 Brand Mention Sweep · 4 min

| Field | Detail |
|---|---|
| **Purpose** | Identify unlinked mentions, journalist queries, NPS/forum threads needing response. |
| **Tools** | Brand24 OR Mention.com OR Awario (set per brand keyword incl. "agenticmarketingpro", CEO names, flagship product names). |
| **Process** | (1) Review new mentions feed. (2) Tag: 💬 respond · 🔗 link request · ⚠️ negative · 📰 journalist lead. (3) Convert journalist leads into HARO parallel responses (§1.4). |
| **Output** | Notion "Mention Triage" database updated. 1–3 actions queued for daily operator. |
| **Escalation** | Negative press on Tier-1 client → escalate to Account Lead and PR partner. |

### 1.4 HARO / Featured Opportunity Responses · 4 min

| Field | Detail |
|---|---|
| **Purpose** | Land high-authority backlinks + media features for clients. |
| **Tools** | HARO daily digest email, SourceBottle, Featured.com, Terkel, Qwoted, Twitter/X journalist request lists. |
| **Process** | (1) Open latest HARO email or RSS. (2) Filter by client vertical + DA>60 outlets. (3) Draft 3–5 responses/day using **E-E-A-T template** (see Appendix below). (4) Send via assigned journalist email + log in Airtable CRM. |
| **Output** | Airtable "Outreach Tracker": outlet · query · client · status · link (when earned). |
| **Escalation** | High-value Forbes/Inc/WSJ placement → notify Account Lead + leadership. |

### 1.5 LinkedIn Engagement · 3 min

| Field | Detail |
|---|---|
| **Purpose** | Build agency/founder authority + drive inbound; signals E-E-A-T to Google. |
| **Tools** | LinkedIn (native), Shield app for analytics, AuthoredUp for drafting, Taplio (optional). |
| **Process** | (1) React to 5 industry posts (Kevin Indig, Lily Ray, Britney Muller, Rand Fishkin voices). (2) Comment meaningfully on 1 post. (3) Skip if no high-value post exists. |
| **Output** | 5 reactions + 1 comment logged in personal LinkedIn analytics. |
| **Escalation** | None — silent KPI. |

---

# 🗓️ SECTION 2 — WEEKLY CADENCE (Monday, 60 minutes)

**Owner:** SEO Analyst (rotating by client) + SEO Lead for client synthesis.
**When:** Monday 9:00–10:00 AM.
**Block:** 60 min on calendar (non-negotiable). Prep Slack thread for cross-team updates Friday EOD before.

---

### 2.1 GSC Performance Review · 10 min

| Field | Detail |
|---|---|
| **Purpose** | Track clicks, impressions, CTR, position trends; surface quick-win pages. |
| **Tools** | Google Search Console (Performance report), Looker Studio (pre-built client dashboard). |
| **Process** | Compare last 28 days vs. previous 28 days for **queries**, **pages**, **countries**, **devices**, **search appearance**. Flag pages with impressions ↑ but CTR ↓ (title/meta work). Flag pages with impressions ↓↓ (decay). |
| **Output** | Looker Studio section "Weekly Trend" auto-emailed Friday. Summary line in Slack: 3 wins, 3 concerns. |
| **Output template** | `[Client] · Wk[N] · Clicks +X% · Avg pos -X.X · Top up: [page] · Top dn: [page]` |

### 2.2 Index Coverage Audit · 6 min

| Field | Detail |
|---|---|
| **Purpose** | Ensure key pages are indexed; find errors before traffic loss. |
| **Tools** | GSC Pages report (Indexing → Pages), Bing WMT URL Inspection API. |
| **Process** | Filter by **Error** → group by reason (5xx, redirect, soft 404, blocked by robots, "Crawled - currently not indexed"). Export to CSV if errors >10. Spot-inspect 3 pages per error type. |
| **Output** | CSV attached to Slack + ticket created in ClickUp for any "Excluded" page jumping in count. |

### 2.3 Bing Webmaster Tools Sweep · 4 min

| Field | Detail |
|---|---|
| **Purpose** | Capture Bing Chat/Copilot visibility + Bing-specific issues. |
| **Tools** | Bing WMT, Bing SEO Analyzer (within WMT), IndexNow API dashboard. |
| **Process** | (1) Review **Recommendations** widget. (2) Check index coverage deltas vs. Google. (3) Submit top 10 new/updated URLs via **IndexNow**. (4) Review Bing Chat/Copilot citations if enabled in dashboard. |
| **Output** | Slack one-liner. URLs submitted logged in IndexNow dashboard. |

### 2.4 Keyword Position Tracking · 8 min

| Field | Detail |
|---|---|
| **Purpose** | Visibility movement, SERP feature capture, share-of-voice trends. |
| **Tools** | STAT, AccuRanker, or SE Ranking (rank-tracking tier); Ahrefs/SEMrush for competitor context. |
| **Process** | (1) Dashboard refresh. (2) Group keywords by intent (informational, commercial, transactional). (3) Pull **top 10 movers up/down** and **SERP feature changes** (featured snippet, PAA, image pack). (4) Note any "page 1 → page 2" drops — these trigger a content brief in §3.4. |
| **Output** | Looker Studio dashboard tab updated. "Winners/Losers" Loom (2 min) for client-facing accounts. |

### 2.5 Core Web Vitals Spot Check · 6 min

| Field | Detail |
|---|---|
| **Purpose** | Ensure LCP/INP/CLS remain in green zone at desktop + mobile. |
| **Tools** | PageSpeed Insights API, Chrome UX Report (CrUX) via Looker Studio, GTmetrix (paid). |
| **Process** | Test 5 hero URLs (homepage, top 3 by traffic, recent post). Compare CrUX 28-day p75 vs. last week. Any URL falling into "Needs Improvement" or "Poor" → add to next sprint backlog. |
| **Output** | Notion "CWV Watch" page auto-populated; Slack alert on red status. |

### 2.6 Backlinks Gained / Lost · 8 min

| Field | Detail |
|---|---|
| **Purpose** | Validate link velocity, catch negative SEO, surface link wins. |
| **Tools** | Ahrefs (preferred for agency) or SEMrush Backlink Audit. |
| **Process** | (1) New backlinks since last Monday → categorize (DR, anchor type, niche relevance, dofollow/nofollow). (2) Lost backlinks → distinguish "deindexed page" (free pass) vs "link removed" (outreach task). (3) Flag toxic links (DR<15 + irrelevant + sudden spike → Disavow file review). |
| **Output** | CSV saved to `/Clients/[Name]/Backlinks/[YYYY-WW].csv`. Notion DB entry per "link outreach task" created. |

### 2.7 Manual Actions / Security Issues · 4 min

| Field | Detail |
|---|---|
| **Purpose** | Catch manual penalties or hacked-content flags before traffic impact. |
| **Tools** | GSC → Security & Manual Actions. |
| **Process** | (1) Check both panels. (2) If clean, log "All clear" with date. (3) If issue, create P0 ticket + client notification within 1 hour. |
| **Output** | One-line in Slack. Audit trail saved quarterly. |

---

### Weekly Output Bundle (Monday 10:00 AM)

1. **Slack digest** to `#seo-ops-weekly`:
   - Per-client 3-bullet summary
   - 1 cross-client insight (e.g., "TTFB regression on WP Engine tier — agency-wide spike")
2. **Looker Studio dashboard** auto-share with client (white-labeled).
3. **Notion "Action queue"** auto-populated with new tickets.
4. **Risks/issues log** updated in risk register.

---

# 🗔️ SECTION 3 — MONTHLY CADENCE (First Monday, 3 hours)

**Owner:** SEO Lead + assigned SEO Analyst.
**When:** First Monday of month, 9:00 AM – 12:00 PM (preceded by 60 min prep Friday prior).
**Block:** Non-negotiable, leadership-protected time.
**Inputs:** Pulled weekly outputs aggregated.

---

### 3.1 Full GSC Deep Audit · 25 min

| Field | Detail |
|---|---|
| **Tools** | GSC API → BigQuery → Looker Studio; Screaming Frog Log File Analyzer for query-cluster review. |
| **Process** | (1) Pull 90-day query data. (2) Bucket by **query intent × URL** to find cannibalization. (3) Identify decay queries (>20% impressions drop MoM). (4) Identify "near-miss" queries (pos 11–20) → brief source. (5) Compare with previous quarter. |
| **Output** | Notion page "Monthly GSC Insights" with CSV + 5 hand-picked queries to action. |
| **Deliverable** | Content brief inputs for §4 quarterly and execution tasks for the month. |

### 3.2 Screaming Frog Crawl · 20 min

| Field | Detail |
|---|---|
| **Tools** | Screaming Frog SEO Spider v20+, configured with: render JS = yes, follow internal nofollow = yes, custom extraction = GA4 path, schema types, h1/h2. |
| **Process** | Crawl client full site (or first 50k URLs). Filter tabs: (a) **Status 4xx/5xx**, (b) **titles >60 chars or duplicate**, (c) **meta descriptions missing**, (d) **images >100KB without alt**, (e) **orphan URLs** (in sitemap not linked), (f) **redirect chains >3 hops**, (g) **hreflang mismatches** (multi-region clients). |
| **Output** | `/Clients/[Name]/Crawl/[YYYY-MM]/[main_export].csv` + Screaming Frog issue summary exported to Notion with severity tags. |

### 3.3 Content Refresh Execution · 30 min

| Field | Detail |
|---|---|
| **Tools** | Notion content calendar, SurferSEO / Page Optimizer Pro, internal brief template. |
| **Process** | (1) Pick **5 priority URLs** from decay queries (3.1) and CWV red list (2.5). (2) For each: update title/meta, refresh intro, add "Last updated [Month YYYY]", expand with semantic NLP terms, add internal links to authority pillars, add media. (3) Republish; ping IndexNow + resubmit in GSC. |
| **Output** | Loom (3 min) showing before/after GSC for refresh set. Updated URLs in Notion with link live-changes. |
| **Volume target** | 5–15 URLs/month/client depending on tier. |

### 3.