/**
 * Client Vault Generator
 * Generates vault markdown content from templates using client data.
 */

export interface ClientData {
  name: string;
  slug: string;
  website: string;
  industry: string;
  tier: string;
  mrr?: number;
  target_geo?: string;
  primary_language?: string;
  business_goal_1?: string;
  business_goal_2?: string;
  business_goal_3?: string;
  contact_name?: string;
  contact_email?: string;
  contact_phone?: string;
  status?: string;
  created_at?: string;
}

export function generateVaultContent(client: ClientData): Record<string, string> {
  const today = new Date().toISOString().split("T")[0];
  const contractEnd = new Date();
  contractEnd.setFullYear(contractEnd.getFullYear() + 1);
  const contractEndStr = contractEnd.toISOString().split("T")[0];

  return {
    "client-profile": generateClientProfile(client, today, contractEndStr),
    "strategy-90-day": generateStrategy(client, today),
    "kpis-and-goals": generateKPIs(client, today),
    "website-manifest": generateWebsiteManifest(client, today),
    "onboarding": generateOnboarding(client, today),
    "competitor-watch": generateCompetitorWatch(client, today),
    "campaign-log": generateCampaignLog(client, today),
    "technical-fix-queue": generateTechnicalFixQueue(client, today),
  };
}

function generateClientProfile(client: ClientData, today: string, contractEnd: string): string {
  return `---
type: client-profile
client: "${client.name}"
website: "${client.website || "https://example.com"}"
status: ${client.status || "active"}
tier: ${client.tier || "Growth"}
start_date: ${today}
mrr: ${client.mrr || 4500}
contract_end: ${contractEnd}
industry: ${client.industry || "SaaS / B2B"}
target_geo: ${client.target_geo || "US, Canada"}
primary_language: ${client.primary_language || "en"}
---

# Client Profile — ${client.name}

## Overview

| Field | Value |
|---|---|
| **Website** | [${client.website || "—"}](${client.website || "#"}) |
| **Tier** | ${client.tier || "Growth"} |
| **Status** | ${client.status || "Active"} |
| **Industry** | ${client.industry || "—"} |
| **Target Geo** | ${client.target_geo || "—"} |
| **Start Date** | ${today} |
| **Contract End** | ${contractEnd} |
| **MRR** | $${client.mrr?.toLocaleString() || "4,500"} |

## Business Goals (from onboarding)

1. **Primary:** ${client.business_goal_1 || "Increase organic SQLs by 50% by Q3 2026"}
2. **Secondary:** ${client.business_goal_2 || "Achieve AI citation in Perplexity for 5 keywords by Q2 2026"}
3. **Tertiary:** ${client.business_goal_3 || "Reduce CAC from paid search by 30% via SEO lift"}

## Key Contacts

| Role | Name | Email | Phone |
|---|---|---|---|
| Primary | ${client.contact_name || "[Name]"} | ${client.contact_email || "[email]"} | ${client.contact_phone || "[phone]"} |

## Website Manifest

See \`website-manifest\` tab for full technical details.

## KPIs

See \`kpis-and-goals\` tab for current metrics and targets.

## Notes

- Client onboarded via AgenticMarketingPro platform on ${today}.
- Vault auto-generated from onboarding form data.
`;
}

function generateStrategy(client: ClientData, today: string): string {
  return `---
type: client-strategy
client: ${client.name}
status: active
last_updated: ${today}
tags: [client/${client.slug}, type/strategy]
---

# 90-Day Strategy — ${client.name}

## Strategic Thesis
${client.name} operates in the ${client.industry || "[industry]"} space. We believe AI-powered automation and AEO/GEO optimization will compound to reduce operational costs by 40–70% while capturing intent from AI search engines (ChatGPT, Perplexity, Gemini). Our bet is on workflow automation via n8n + semantic SEO as the primary growth levers.

## Phase 1 (Days 1–30): Foundation
- **Goal:** Establish baselines, fix critical technical issues, ship first content batch
- **Key Initiatives:**
  - Technical SEO audit + fix critical issues
  - Deploy n8n automation for lead capture and follow-up
  - Publish 4 pillar articles on commercial keywords
  - Deploy AEO/GEO schema across priority pages
- **Exit Criteria:**
  - All critical technical issues resolved
  - 4 pillar articles published + indexed
  - AEO baseline established
  - Weekly digest flowing to client

## Phase 2 (Days 31–60): Build
- **Goal:** Compounding content velocity, off-page foundation, paid experiments
- **Key Initiatives:**
  - Launch off-page campaign: 10 link prospects/week
  - Publish 8 supporting content pieces
  - Launch paid search test ($5K/mo budget)
- **Exit Criteria:**
  - 10+ referring domains acquired
  - Top-10 ranking for 5+ target keywords
  - Paid CPA within 20% of target

## Phase 3 (Days 61–90): Compound
- **Goal:** Cross-channel compounding, AEO lift visible, QBR-ready results
- **Key Initiatives:**
  - Programmatic SEO batch: 200 location pages
  - Email lifecycle automation: 3 flows live
  - CRO program: 4 A/B tests
- **Exit Criteria:**
  - Organic traffic +25% QoQ
  - AEO citation rate +50% QoQ
  - MQLs from organic +30% QoQ
  - QBR deck delivered + 90-day renewal signed

## Risks & Mitigations
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Search algorithm changes | Medium | High | Diversify across AEO + GEO + traditional SEO |
| Client resource constraints | Medium | Medium | Prioritize high-impact, low-effort wins first |
| Automation workflow failures | Low | Medium | Build monitoring + fallback triggers in n8n |

## Resource Allocation (Monthly)
| Channel | Hours (Agent-Equivalent) | Budget (Ad Spend) |
|---|---|---|
| SEO (Technical + On-Page) | 20 | — |
| Content (8 pieces/mo) | 15 | — |
| Off-Page (10 links/mo) | 10 | — |
| AEO/GEO | 8 | $800 |
| Paid Search | 5 | $5,000 |
| Email/Lifecycle | 5 | — |
| **Total** | **63** | **$5,800** |

## Renewal Hypothesis
By day 90, we will have demonstrated a 25% increase in organic MQLs and 40% reduction in admin costs. The client will renew at the current tier or upgrade to Scale. Upsell opportunity: Custom SaaS build or Odoo ERP integration.
`;
}

function generateKPIs(client: ClientData, today: string): string {
  return `---
type: client-kpis
client: ${client.name}
status: active
last_updated: ${today}
tags: [client/${client.slug}, type/kpis]
---

# KPIs & Goals — ${client.name}

## North Star Metric
Qualified pipeline generated from organic + paid channels

## 90-Day Targets
| KPI | Baseline | 90-Day Target | Source | Cadence |
|---|---|---|---|---|
| Organic traffic (sessions/mo) | ___ | +25% | GA4 | Weekly |
| Branded search volume | ___ | +15% | GSC | Weekly |
| Non-branded keyword rankings (top-10) | ___ | +20 | Ahrefs | Weekly |
| AEO citation rate (% of tracked queries) | ___ | +50% | Profound | Weekly |
| Referring domains | ___ | +15% | Ahrefs | Weekly |
| Lead-to-MQL conversion rate | ___ | +10% | HubSpot | Monthly |
| MQLs from organic | ___ | +30% | HubSpot | Monthly |
| Email deliverability (inbox %) | ___ | ≥98% | Postmark | Weekly |
| Paid ROAS (if applicable) | ___ | Per tier | Platform | Weekly |

## KPI Definitions

### Organic Traffic
GA4 sessions where \`sessionDefaultChannelGroup = "Organic Search"\`. Excludes branded paid campaigns.

### AEO Citation Rate
% of 50 tracked queries where the client's brand is cited by at least one of: ChatGPT, Perplexity, Claude, Gemini, Copilot. Tracked weekly via Profound.

## KPI Owners
| KPI | Owner (Agent) | Human Reviewer |
|---|---|---|
| Organic traffic | On-Page + Content Strategist | Strategist |
| Branded search | AEO/GEO + Content | Strategist |
| AEO citation rate | AEO/GEO Specialist | Strategist |
| Referring domains | Off-Page Strategist | Strategist |
| Lead conversion | CRO + Analytics Expert | Strategist |

## KPI Review Cadence
- **Weekly (Monday 10:00):** Atlas produces KPI snapshot
- **Monthly (1st):** Reporting Agent produces full client report with KPI trend
- **Quarterly:** QBR deck with KPI deep dive + 90-day reforecast
`;
}

function generateWebsiteManifest(client: ClientData, today: string): string {
  return `---
type: website-manifest
client: "${client.name}"
website: "${client.website || "https://example.com"}"
last_updated: ${today}
---

# Website Manifest — ${client.name}

## Domains

| Domain | Primary? | Subdomains | Status |
|---|---|---|---|
| ${client.website?.replace("https://", "").replace("http://", "").split("/")[0] || "example.com"} | ✅ | www | Active |

## Tech Stack

| Layer | Technology | Version | Notes |
|---|---|---|---|
| CMS | [WordPress / Webflow / Custom] | | |
| Hosting | [AWS / Vercel / Cloudflare] | | |
| CDN | [Cloudflare / None] | | |
| Analytics | [GA4 / Plausible] | | Property ID: |
| Tag Manager | [GTM / None] | | |
| SEO Tools | [Yoast / RankMath / None] | | |
| CRM | [HubSpot / Salesforce / None] | | |

## API Properties (for Agent Integration)

| Service | Property ID | Configured? | Status |
|---|---|---|---|
| Google Search Console | [property URL] | ☐ | [healthy / issue] |
| Google Analytics 4 | [properties/123456789] | ☐ | [healthy / issue] |
| Bing Webmaster Tools | [site URL] | ☐ | [healthy / issue] |
| Ahrefs | [domain] | ☐ | [healthy / issue] |
| Google Ads | [Customer ID] | ☐ | [healthy / issue] |
| Meta Ads | [Ad Account ID] | ☐ | [healthy / issue] |
| LinkedIn Ads | [Account ID] | ☐ | [healthy / issue] |
| HubSpot | [Portal ID] | ☐ | [healthy / issue] |
| Slack | [Webhook URL] | ☐ | [healthy / issue] |

## Important Pages

| Page Type | URL | Agent Notes |
|---|---|---|
| Homepage | ${client.website || "https://example.com"}/ | |
| Pricing | ${client.website || "https://example.com"}/pricing | |
| Blog | ${client.website || "https://example.com"}/blog | |
| Contact | ${client.website || "https://example.com"}/contact | |
| Key Landing Page | [URL] | [Primary conversion page] |

## URL Patterns (for pSEO / Scraping)

| Pattern Type | Example URL | Notes |
|---|---|---|
| Blog posts | /blog/[slug] | |
| Product pages | /products/[slug] | |
| Category pages | /category/[slug] | |

## Schema Setup

| Schema Type | Implemented? | Pages |
|---|---|---|
| Organization | ☐ | All |
| Product | ☐ | Product pages |
| FAQ | ☐ | FAQ pages |
| HowTo | ☐ | Tutorial pages |
| BreadcrumbList | ☐ | All |

## Known Issues

| Issue | Severity | Discovered | Status | Ticket |
|---|---|---|---|---|
| [e.g., slow TTFB] | [P1/P2/P3] | [date] | [open/closed] | [#] |
`;
}

function generateOnboarding(client: ClientData, today: string): string {
  return `---
type: client-onboarding
client: ${client.name}
status: completed
onboarded_at: ${today}
---

# Onboarding Record — ${client.name}

## Onboarding Date
${today}

## Onboarding Form Data

| Field | Value |
|---|---|
| Client Name | ${client.name} |
| Website | ${client.website || "—"} |
| Industry | ${client.industry || "—"} |
| Tier | ${client.tier || "—"} |
| MRR | $${client.mrr || "4,500"} |
| Target Geo | ${client.target_geo || "—"} |
| Primary Language | ${client.primary_language || "en"} |
| Business Goal 1 | ${client.business_goal_1 || "—"} |
| Business Goal 2 | ${client.business_goal_2 || "—"} |
| Business Goal 3 | ${client.business_goal_3 || "—"} |
| Contact Name | ${client.contact_name || "—"} |
| Contact Email | ${client.contact_email || "—"} |
| Contact Phone | ${client.contact_phone || "—"} |

## Welcome Sequence
- [x] Vault folder created
- [x] Client profile generated
- [x] 90-day strategy drafted
- [x] KPIs established
- [x] Website manifest created
- [ ] Kickoff call scheduled
- [ ] Access credentials collected (GSC, GA4, etc.)
- [ ] First weekly digest sent

## Next Steps
1. Schedule kickoff call within 48 hours
2. Collect API credentials for all connected platforms
3. Run technical SEO audit
4. Publish first pillar article within 14 days
`;
}

function generateCompetitorWatch(client: ClientData, today: string): string {
  return `---
type: competitor-map
client: ${client.name}
last_updated: ${today}
---

# Competitor Watch — ${client.name}

## Primary Competitors

| Competitor | Domain | Threat Level | Notes |
|---|---|---|---|
| [Competitor 1] | [domain.com] | High | [Notes] |
| [Competitor 2] | [domain.com] | Medium | [Notes] |
| [Competitor 3] | [domain.com] | Low | [Notes] |

## Keyword Overlap

| Keyword | Client Rank | Competitor 1 | Competitor 2 | Opportunity |
|---|---|---|---|---|
| [keyword 1] | — | — | — | High |
| [keyword 2] | — | — | — | Medium |

## Backlink Gap

| Competitor | RDs | Gap | Priority Targets |
|---|---|---|---|
| [Competitor 1] | — | — | [target sites] |
| [Competitor 2] | — | — | [target sites] |

## Content Gap

| Topic | Client Has It? | Competitor 1 | Competitor 2 | Priority |
|---|---|---|---|---|
| [topic 1] | ☐ | ✅ | ✅ | High |
| [topic 2] | ☐ | ☐ | ✅ | Medium |

## Monitoring
- Weekly competitor backlink alerts via Ahrefs
- Monthly SERP position tracking
- Quarterly content gap analysis
`;
}

function generateCampaignLog(client: ClientData, today: string): string {
  return `---
type: client-campaign-log
client: ${client.name}
last_updated: ${today}
---

# Campaign Log — ${client.name}

## Active Campaigns

| Campaign | Type | Status | Start | End | Budget | Owner |
|---|---|---|---|---|---|---|
| [Campaign 1] | [SEO / Paid / Content] | [Active / Paused] | ${today} | — | $ | [Agent] |

## Completed Campaigns

| Campaign | Type | Result | ROI | Notes |
|---|---|---|---|---|
| — | — | — | — | — |

## Upcoming Campaigns

| Campaign | Type | Planned Start | Budget | Owner |
|---|---|---|---|---|
| — | — | — | — | — |

## Campaign Assets

See \`campaigns/\` folder for full creative assets, briefs, and reports.
`;
}

function generateTechnicalFixQueue(client: ClientData, today: string): string {
  return `---
type: technical-fix-queue
client: ${client.name}
last_updated: ${today}
---

# Technical Fix Queue — ${client.name}

## Critical (P1)

| Issue | Impact | Fix | Owner | Status | Due |
|---|---|---|---|---|---|
| [e.g., slow TTFB > 600ms] | SEO + CRO | Optimize hosting / CDN | Tech SEO | ☐ | [date] |
| [e.g., mobile CLS > 0.25] | CRO | Fix layout shifts | Tech SEO | ☐ | [date] |

## High (P2)

| Issue | Impact | Fix | Owner | Status | Due |
|---|---|---|---|---|---|
| [e.g., 404s on old product pages] | SEO | Implement 301 redirects | Tech SEO | ☐ | [date] |
| [e.g., missing canonicals] | SEO | Add canonical tags | On-Page | ☐ | [date] |

## Medium (P3)

| Issue | Impact | Fix | Owner | Status | Due |
|---|---|---|---|---|---|
| [e.g., alt text missing on 50 images] | SEO + A11y | Add descriptive alt text | Content | ☐ | [date] |
| [e.g., H1 tags duplicated] | SEO | Restructure headings | On-Page | ☐ | [date] |

## Resolved

| Issue | Fix Date | Result |
|---|---|---|
| — | — | — |
`;
}
