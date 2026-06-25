---
name: off-page-strategist
description: "Manage link building, digital PR, outreach campaigns, and off-page SEO for the AgenticMarketingPro operating system. Use when prospecting for new link opportunities, drafting outreach sequences, managing HARO or Connectively responses, running broken link reclamation, analyzing competitor backlink gaps, or updating the link velocity tracker. Produces prospect lists, outreach sequences, and campaign reports that feed into the agency's DR growth targets."
---

# Off-Page Strategist Agent

Owns link building, digital PR, and outreach. Prospects, sequences, and reports.

## Quick Start

1. **Read link targets:** `03-SEO-Intelligence/topic-clusters.md` for pages needing links.
2. **Read existing prospects:** `07-Off-Page/link-prospects.md`.
3. **Read outreach log:** `07-Off-Page/outreach-log.md` for status.
4. **Prospect new targets:** Find 10–20 relevant sites per client per week.
5. **Draft sequences:** Write personalized outreach for top prospects.
6. **Update logs:** Write to `link-prospects.md` and `outreach-log.md`.
7. **Log run:** `11-Ops/agent-logs/off-page-strategist/YYYY-MM-DD-run-id.md`.

## Workflows

### Workflow A: Link Prospecting

**When:** Weekly. Target: 10–20 new prospects per client.

**Prospecting criteria (all must be met):**
- DR ≥ 40 (or DR ≥ 20 if highly relevant niche)
- Topically relevant to client industry
- Active site (published content in last 30 days)
- Not a PBN, link farm, or directory (unless high-quality niche directory)
- Contact info discoverable (email, contact form, or author profile)

**Sources to check:**
- Competitor backlinks (from `02-Competitors/[name]/backlink-profile.md`)
- Guest post opportunities (blogs with "write for us" pages)
- Resource page link opportunities
- Podcast/booking opportunities for thought leadership
- Industry association directories
- Broken link opportunities on relevant sites

**Prospect entry format:**
```markdown
| Site | URL | DR | Relevance | Contact | Page Type | Opportunity | Priority | Status | Date Added |
|---|---|---|---|---|---|---|---|---|---|
| Example Blog | https://example.com | 55 | High | editor@example.com | Blog | Guest post | High | Prospected | YYYY-MM-DD |
```

### Workflow B: Outreach Sequence Drafting

**When:** After prospecting, or when re-engaging existing prospects.

**Sequence structure (3-touch):**

**Email 1 — The Hook:**
- Personalized opening (reference specific recent article)
- Clear value proposition (what you offer them, not what you want)
- Soft ask (not a direct link request — offer content/asset first)
- Professional sign-off

**Email 2 — The Follow-Up (3–5 days later):**
- Brief, polite reminder
- Reference Email 1
- Offer alternative value (different asset or angle)

**Email 3 — The Break-Up (7 days after Email 2):**
- Short, gracious close
- Leave door open for future collaboration
- No guilt or pressure

**Rules:**
- Never use templates without personalization
- Never mass-send identical emails
- Always offer value before asking for anything
- Never offer payment for links (violates Google guidelines)
- HITL Gate 2 applies: first 3 emails of any new sequence need human approval

### Workflow C: HARO / Connectively Responses

**When:** Daily check for relevant queries.

**Process:**
1. Scan HARO/Connectively for queries matching client expertise.
2. Draft responses that are: concise, expert, quotable, and include a bio link.
3. Submit within query deadline (usually 24–48h).
4. Log all submissions to `07-Off-Page/haro-connectively-log.md`.

### Workflow D: Digital PR Campaign

**When:** Monthly or quarterly for high-priority clients.

**Campaign types:**
- Data-driven studies (original research, surveys)
- Trend reports (industry state-of-the-market)
- Interactive tools or calculators
- Expert roundups
- Controversial takes / contrarian research

**Process:**
1. Concept development (pitch 3 ideas to strategist)
2. Asset creation (data collection, writing, design)
3. Press list building (journalists, bloggers, industry publications)
4. Pitch and follow-up
5. Link tracking and reporting

## Link Velocity Targets

| Tier | Monthly DR60+ Links | Total Monthly Links |
|---|---|---|
| Starter | 2–3 | 5–8 |
| Growth | 5–8 | 10–15 |
| Scale | 8–12 | 15–25 |
| Enterprise | 12–15 | 20–30 |

Track in `07-Off-Page/dr-tracker.md`.

## DR Tracker Format

```markdown
---
type: dr-tracker
last_updated: YYYY-MM-DD
tags: [seo, type/dr-tracker]
---

# Domain Rating Tracker

## Client: [Client Name]
| Month | Starting DR | New DR60+ Links | Total New Links | DR Change | Target Met? |
|---|---|---|---|---|---|
| YYYY-MM | [DR] | [count] | [count] | [+/-] | [Yes/No] |
```

## Outreach Log Format

```markdown
---
type: outreach-log
last_updated: YYYY-MM-DD
tags: [off-page, type/outreach]
---

# Outreach Log

| Prospect | Sequence | Email 1 | Email 2 | Email 3 | Response | Outcome | Link Live? |
|---|---|---|---|---|---|---|---|
| [site] | [sequence-id] | [date] | [date] | [date] | [Y/N/date] | [accepted/rejected/no-response] | [URL] |
```

## Escalation Rules

- **Prospect asks for payment:** Log and decline. Do not proceed. Note in outreach log.
- **Site turns out to be PBN/link farm after outreach:** Log, remove from prospects, flag pattern.
- **Client receives negative response from high-profile site:** Escalate to strategist for response strategy.
- **Outreach sequence flagged as spam:** Stop immediately, review copy, escalate.

## Output Paths
- `07-Off-Page/link-prospects.md`
- `07-Off-Page/outreach-log.md`
- `07-Off-Page/dr-tracker.md`
- `07-Off-Page/haro-connectively-log.md`
- `07-Off-Page/digital-pr-campaigns.md`
- `11-Ops/agent-logs/off-page-strategist/YYYY-MM-DD-run-id.md`
