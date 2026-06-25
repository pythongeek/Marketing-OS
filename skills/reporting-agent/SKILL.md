---
name: reporting-agent
description: "Generate client-facing monthly reports, quarterly business reviews (QBRs), and executive dashboards for the AgenticMarketingPro operating system. Use when compiling monthly SEO and marketing reports, building QBR decks, creating performance summaries, or generating data visualizations for client presentations. Covers report templates, data storytelling, narrative structure, and executive summary writing. All client reports require HITL Gate 7 approval before sending."
---

# Reporting Agent

Generates client-facing monthly reports, QBRs, and executive dashboards.

## Quick Start

1. **Read KPIs:** `01-Clients/[client]/kpis-and-goals.md`
2. **Read analytics data:** `10-Analytics/weekly-digest.md` (aggregate last 4 weeks)
3. **Read content performance:** `04-Content-Production/published-index.md`
4. **Read SEO data:** `03-SEO-Intelligence/gsc-weekly-log.md`, `bing-weekly-log.md`
5. **Read off-page data:** `07-Off-Page/dr-tracker.md`, `outreach-log.md`
6. **Read paid data:** `08-Paid-Ads/campaign-log.md`, `budget-allocation.md`
7. **Compile report:** Use monthly report template.
8. **HITL Gate 7:** Submit for strategist approval before sending to client.
9. **Log run:** `11-Ops/agent-logs/reporting-agent/YYYY-MM-DD-run-id.md`

## Monthly Report Structure

### Section 1: Executive Summary (1 page)
- **Headline:** One sentence summary of the month (e.g., "Organic traffic up 23% QoQ, 4 new keywords in top 10, off-page campaign delivered 12 links")
- **Traffic light dashboard:**
  - 🟢 On track: [metrics]
  - 🟡 Needs attention: [metrics]
  - 🔴 Off track: [metrics]
- **Key wins:** 3 bullet points, specific and quantified
- **Key challenges:** 2 bullet points, with mitigation plan
- **Next month focus:** 3 priorities

### Section 2: SEO Performance
- **Organic traffic:** Sessions, users, % change MoM, % change YoY
- **Keyword rankings:** Top 10 keywords, new entrants, movers, losers
- **Indexation:** Valid pages, errors, CWV status
- **Content published:** Count, word count, topics, performance of new content
- **Technical health:** Open issues, resolved issues, health score

### Section 3: Content Performance
- **Content published this month:** List with URLs, traffic, engagement
- **Top performers:** Best 3 pieces by traffic and conversions
- **Underperformers:** Worst 3 pieces + analysis of why
- **Content pipeline:** What's in progress, what's planned next month

### Section 4: Off-Page Performance
- **Links acquired:** Count, DR breakdown, referring domains
- **Outreach metrics:** Emails sent, response rate, conversion rate
- **Digital PR:** Media mentions, placements, authority gained
- **DR progression:** Current DR, change, target vs. actual

### Section 5: Paid Performance (if applicable)
- **Spend vs. budget:** Actual vs. planned
- **ROAS/CPA:** By channel, by campaign, trend
- **Creative performance:** Top 3, bottom 3, tests completed
- **Audience insights:** New segments, lookalike performance

### Section 6: Social Performance (if applicable)
- **Posting cadence:** Posts published, platforms
- **Engagement:** Likes, comments, shares, follower growth
- **Top posts:** Best 3 by engagement
- **Community health:** Sentiment, response rate, issues

### Section 7: AEO/GEO Performance (if applicable)
- **AI citation rate:** By engine (GPT, Perplexity, Gemini, Copilot)
- **Change vs. baseline:** Trend direction
- **Corroboration status:** Sources verified, gaps closed
- **Schema deployment:** Pages with schema, rich results earned

### Section 8: KPI Attainment
- **Scorecard:** Baseline vs. target vs. actual for each KPI
- **Attainment %:** Color-coded (green ≥90%, yellow 70–89%, red <70%)
- **Trend:** Direction and velocity
- **90-day forecast:** Based on current trajectory

### Section 9: Recommendations & Next Steps
- **Top 3 recommendations:** Each with expected impact, effort, and timeline
- **Resource needs:** Any additional budget, access, or approvals needed
- **Next month priorities:** What we're focusing on and why

## Quarterly Business Review (QBR) Structure

### QBR Deck (15–20 slides)

1. **Title Slide:** Client name, quarter, date, strategist name
2. **Agenda:** What we'll cover (3 minutes)
3. **Quarterly Executive Summary:** One-slide scorecard (5 minutes)
4. **Goal Progress:** How we're tracking against 90-day goals (5 minutes)
5. **SEO Deep Dive:** Traffic, rankings, content, technical (10 minutes)
6. **Content Performance:** What worked, what didn't, what's next (10 minutes)
7. **Off-Page Progress:** Links, PR, authority (5 minutes)
8. **Paid Performance (if applicable):** Spend, ROAS, learnings (5 minutes)
9. **AEO/GEO Performance (if applicable):** AI citations, schema, corroboration (5 minutes)
10. **Competitive Landscape:** What competitors did, how we responded (5 minutes)
11. **Wins & Learnings:** What we're proud of, what we learned (5 minutes)
12. **Challenges & Risks:** What's in our way, how we're mitigating (5 minutes)
13. **Next Quarter Strategy:** Top 3 priorities, resource allocation, timeline (10 minutes)
14. **KPI Reset:** Updated targets for next quarter (5 minutes)
15. **Open Discussion:** Client questions, concerns, feedback (10 minutes)
16. **Action Items:** Who does what by when (5 minutes)

### QBR Narrative Rules
- **Lead with outcomes, not activities:** "Organic traffic grew 32%" not "We published 8 articles"
- **Use the "So what?" test:** Every data point must answer why it matters to the client's business
- **Acknowledge misses honestly:** If a KPI was missed, say why and what we're doing differently
- **Show the money:** Connect every recommendation to revenue, pipeline, or cost savings
- **End with clear next steps:** No ambiguity about who owns what

## Data Storytelling Principles

1. **One insight per chart:** Don't make clients interpret charts. Tell them what to see.
2. **Context matters:** "32% growth" is good. "32% growth vs. industry average of 8%" is great.
3. **Trend over point-in-time:** Show the trajectory, not just the snapshot.
4. **Comparison drives insight:** Client vs. target, client vs. last quarter, client vs. competitor.
5. **Recommendations are actionable:** Every recommendation has a who, what, and when.

## HITL Gate 7: Client Report Approval

Before any report goes to a client, it must pass:
- **Strategist review:** Accuracy, narrative, recommendations make sense
- **Atlas review:** Data consistency, no contradictions, all sections complete
- **Brand voice check:** No forbidden phrases, agency voice consistent
- **QA pipeline:** Factual accuracy check, formatting consistency

**Approval checklist:**
- [ ] All data points verified against source
- [ ] No typos or broken links
- [ ] Brand voice consistent
- [ ] All charts labeled and sourced
- [ ] Recommendations are specific and actionable
- [ ] Client name and details correct throughout
- [ ] Attachments and links work
- [ ] Send from correct email address
- [ ] Subject line is clear and professional

## Escalation Rules

- **Data discrepancy between sources:** Pause report, investigate, resolve before sending
- **KPI attainment <50% for 2+ consecutive months:** Escalate to strategist for client retention strategy
- **Client requests data not in standard report:** Log request, evaluate for template update
- **Report is delayed >24h past deadline:** Alert strategist and client proactively
- **Client disputes reported data:** Escalate to analytics-expert for verification
- **Client requests additional reporting (custom dashboards, ad-hoc):** Evaluate effort, scope, and pricing impact

## Output Paths
- `01-Clients/[client]/monthly-reports/YYYY-MM-report.md`
- `01-Clients/[client]/quarterly-reviews/Q[X]-YYYY-qbr.md`
- `11-Ops/agent-logs/reporting-agent/YYYY-MM-DD-run-id.md`
