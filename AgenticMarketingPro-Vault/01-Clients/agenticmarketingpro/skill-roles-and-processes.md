# AgenticMarketingPro — Skill Roles & Process Plan

**Date:** 2026-07-09  
**Client:** AgenticMarketingPro  
**Purpose:** Define what each skill does, its role in the client journey, and how processes flow between skills.

---

## Skill Ecosystem Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AGENTICMARKETINGPRO SKILL ECOSYSTEM                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │  ONBOARDING  │───→│   STRATEGY   │───→│  EXECUTION   │                  │
│   │    AGENT     │    │   AGENTS     │    │   AGENTS     │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│          │                   │                   │                          │
│          ▼                   ▼                   ▼                          │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │ Client Vault │    │  90-Day Plan │    │ Content/Blog │                  │
│   │   Generator  │    │   KPI Set    │    │   SEO/PSEO   │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│                                              │                              │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                  │
│   │   QA GATE    │←───│  ANALYTICS   │←───│  PUBLISHING  │                  │
│   │  (Binary +   │    │   REPORTING  │    │   (WP/GSC)   │                  │
│   │   Scored)    │    │              │    │              │                  │
│   └──────────────┘    └──────────────┘    └──────────────┘                  │
│          │                                                              │
│          ▼                                                              │
│   ┌──────────────┐                                                      │
│   │  DELIVERABLE │──────────────────────────────────────────────────────│
│   │   TO CLIENT  │                                                      │
│   └──────────────┘                                                      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Skill Definitions by Phase

### PHASE 1: Discovery & Onboarding

#### 1. `onboarding-agent`
**Role:** First touch. Captures client requirements, generates vault structure.
**Process:**
1. Collect business goals, competitors, target geo, industry
2. Generate client vault folder structure
3. Create initial strategy documents
4. Set up credential requirements list
**Inputs:** Client intake form  
**Outputs:** Client vault, profile.md, strategy-90-day.md  
**Default Prompt:** "You are a senior client onboarding specialist for an AI automation agency. Extract key business requirements and create a comprehensive client profile."
**Prompt Override Field:** Yes — allows custom onboarding questions

---

### PHASE 2: Strategy & Planning

#### 2. `content-strategist`
**Role:** Develops content strategy aligned with business goals.
**Process:**
1. Analyze client industry and competitors
2. Identify content gaps and opportunities
3. Create topic cluster map
4. Define content calendar (90-day)
**Inputs:** Client profile, competitor analysis, keyword research  
**Outputs:** content-strategy.md, topic-clusters.md, content-calendar.md  
**Default Prompt:** "You are a content strategist for an AI automation agency. Create a data-driven content strategy that targets high-intent keywords and builds topical authority."
**Prompt Override Field:** Yes

#### 3. `competitor-intel`
**Role:** Monitors competitor movements and identifies opportunities.
**Process:**
1. Track competitor rankings and content
2. Analyze backlink profiles
3. Identify content gaps
4. Monitor pricing and positioning changes
**Inputs:** Competitor URLs, industry keywords  
**Outputs:** competitor-watch.md, keyword-gaps.md, content-audit.md  
**Default Prompt:** "You are a competitive intelligence analyst. Monitor competitor digital presence and identify actionable opportunities for your client."
**Prompt Override Field:** Yes

#### 4. `aeo-geo-specialist`
**Role:** Optimizes for AI search engines (ChatGPT, Perplexity, Gemini).
**Process:**
1. Build entity registry for client
2. Create corroboration map (where client is mentioned)
3. Optimize for AI citations
4. Test LLM prompt responses
**Inputs:** Client website, target keywords, entity list  
**Outputs:** entity-registry.md, corroboration-map.md, ai-citation-tracker.md  
**Default Prompt:** "You are an AEO/GEO specialist. Optimize this client's digital presence for AI search engines. Build entity schemas and knowledge graph presence."
**Prompt Override Field:** Yes

---

### PHASE 3: Content Production

#### 5. `copywriter`
**Role:** Writes conversion-focused copy for ads, landing pages, emails.
**Process:**
1. Understand target audience and pain points
2. Write using AIDA framework
3. Include psychological triggers
4. Optimize for channel (Google Ads, Meta, LinkedIn)
**Inputs:** Brief, target audience, channel specs  
**Outputs:** Ad copy, landing page copy, email sequences  
**Default Prompt:** "You are an expert conversion copywriter. Write persuasive copy using AIDA framework and psychological triggers. Be specific and actionable."
**Prompt Override Field:** Yes

#### 6. `longform-writer`
**Role:** Produces long-form SEO content (blog posts, guides, pillar pages).
**Process:**
1. Research topic thoroughly
2. Create detailed outline
3. Write comprehensive content (2000+ words)
4. Include schema markup recommendations
**Inputs:** Content brief, target keywords, competitor content  
**Outputs:** Blog posts, guides, pillar pages  
**Default Prompt:** "You are an expert SEO content writer. Create comprehensive, authoritative content that ranks. Include data, examples, and actionable advice."
**Prompt Override Field:** Yes

#### 7. `pseo-engineer`
**Role:** Builds programmatic SEO systems at scale.
**Process:**
1. Identify scalable keyword patterns
2. Design page templates
3. Build data sources and URL patterns
4. Create content generation pipeline
**Inputs:** Product/service data, keyword patterns, templates  
**Outputs:** Programmatic page specs, data source configs, publish pipeline  
**Default Prompt:** "You are a programmatic SEO engineer. Design data-driven content systems that scale. Focus on long-tail keyword coverage and template efficiency."
**Prompt Override Field:** Yes

---

### PHASE 4: Technical SEO

#### 8. `tech-seo-auditor`
**Role:** Audits technical SEO health.
**Process:**
1. Crawl site architecture
2. Validate structured data
3. Analyze Core Web Vitals
4. Check mobile usability
5. Review log files
**Inputs:** Website URL, GSC data, Screaming Frog export  
**Outputs:** technical-audit.md, fix-queue.md  
**Default Prompt:** "You are a senior technical SEO consultant. Audit sites systematically and score issues by Impact x Urgency / Effort."
**Prompt Override Field:** Yes

#### 9. `on-page-optimizer`
**Role:** Optimizes individual pages for target keywords.
**Process:**
1. Audit title tags, meta descriptions
2. Optimize H1-H3 structure
3. Add/review schema markup
4. Optimize internal links
5. Check image alt text
**Inputs:** Page URL, target keyword, competitor pages  
**Outputs:** on-page-recommendations.md  
**Default Prompt:** "You are an expert on-page SEO optimizer. Audit pages systematically and provide before/after recommendations."
**Prompt Override Field:** Yes

#### 10. `local-seo-agent`
**Role:** Manages local SEO presence.
**Process:**
1. Optimize Google Business Profile
2. Manage citations
3. Monitor map pack rankings
4. Drive local organic traffic
**Inputs:** Business location, GBP data, citation list  
**Outputs:** local-seo-plan.md, citation-audit.md  
**Default Prompt:** "You are a local SEO specialist. Optimize Google Business Profile, manage citations, and dominate local search."
**Prompt Override Field:** Yes

---

### PHASE 5: Off-Page & Authority

#### 11. `off-page-strategist`
**Role:** Manages backlink profile and digital PR.
**Process:**
1. Analyze backlink profile
2. Disavow toxic links
3. Build authority through digital PR
4. Monitor brand mentions
**Inputs:** Backlink data, competitor backlinks, brand mentions  
**Outputs:** link-prospects.md, outreach-log.md, dr-tracker.md  
**Default Prompt:** "You are an off-page SEO specialist. Build authority through strategic link building and digital PR."
**Prompt Override Field:** Yes

#### 12. `influencer-agent`
**Role:** Manages influencer campaigns.
**Process:**
1. Identify relevant influencers
2. Outreach and negotiation
3. Campaign management
4. Performance tracking
**Inputs:** Target audience, budget, campaign goals  
**Outputs:** influencer-pipeline.md, campaign-log.md  
**Default Prompt:** "You are an influencer marketing specialist. Identify, outreach, and manage influencer partnerships."
**Prompt Override Field:** Yes

---

### PHASE 6: Paid Advertising

#### 13. `ad-expert`
**Role:** Manages PPC campaigns across Google, Meta, LinkedIn.
**Process:**
1. Set up campaign structure
2. Optimize bids and audiences
3. Test creatives
4. Optimize landing pages for ROAS
**Inputs:** Budget, target CPA/ROAS, creative assets  
**Outputs:** campaign-log.md, ad-copy-library.md, budget-allocation.md  
**Default Prompt:** "You are a performance marketing specialist. Manage PPC campaigns for maximum ROAS. Optimize bids, audiences, and creatives."
**Prompt Override Field:** Yes

---

### PHASE 7: Analytics & Reporting

#### 14. `analytics-expert`
**Role:** Compiles reports, identifies anomalies, tracks KPIs.
**Process:**
1. Pull data from GA4, GSC, ad platforms
2. Identify anomalies (>2σ)
3. Track KPIs vs targets
4. Provide actionable recommendations
**Inputs:** GA4 data, GSC data, ad platform data  
**Outputs:** weekly-digest.md, kpi-attainment.md, anomaly-log.md  
**Default Prompt:** "You are a marketing analytics expert. Compile reports, identify anomalies, and provide actionable recommendations."
**Prompt Override Field:** Yes

#### 15. `reporting-agent`
**Role:** Creates client-ready reports.
**Process:**
1. Gather data from all channels
2. Create visualizations
3. Write executive summary
4. Format for client presentation
**Inputs:** All channel data, KPI targets  
**Outputs:** monthly-report.md, campaign-log.md  
**Default Prompt:** "You are a reporting automation expert. Build client-ready reports with clear insights and actionable next steps."
**Prompt Override Field:** Yes

---

### PHASE 8: QA & Compliance

#### 16. `qa-pipeline`
**Role:** Quality gate for all deliverables.
**Process:**
1. Binary checks (legal risk, plagiarism) — BLOCK if failed
2. Scored checks (grammar, tone, brand voice) — LOG and continue
3. Flag deliverables for human review if needed
**Inputs:** Content artifact, check configuration  
**Outputs:** qa-result.json, flagged items list  
**Default Prompt:** "You are a QA gatekeeper. Run strict checks on all deliverables. Binary checks block deliverability. Scored checks log and continue."
**Prompt Override Field:** Yes

---

### PHASE 9: Orchestration

#### 17. `atlas-orchestrator`
**Role:** Master orchestrator. Runs daily ops loop, dispatches agents.
**Process:**
1. Review job queue
2. Dispatch specialist agents
3. Monitor execution
4. Escalate failures
5. Ensure deliverables meet standards
**Inputs:** Job queue, agent configs, client priorities  
**Outputs:** job-execution-workflow.md, escalation alerts  
**Default Prompt:** "You are the master orchestrator of an AI-native marketing agency. Run the daily ops loop, dispatch specialist agents, manage the task queue, and ensure all deliverables meet quality standards."
**Prompt Override Field:** Yes

---

## Process Flow Diagrams

### Content Production Pipeline
```
content-strategist → longform-writer → qa-pipeline → on-page-optimizer → publishing
     ↑                    ↑                ↓              ↓
competitor-intel ──────→ brief ───────→ blocked? ───→ tech-seo-auditor
```

### AEO/GEO Pipeline
```
ae0-geo-specialist → entity-registry → corroboration-map → llm-prompt-tests
        ↓
   content-strategist (feeds into content plan)
```

### Paid Ads Pipeline
```
ad-expert → copywriter → qa-pipeline → campaign-launch → analytics-expert
                                              ↓
                                        reporting-agent
```

---

## Credential Requirements by Skill

| Skill | Required Credentials | Optional Credentials |
|-------|---------------------|---------------------|
| `onboarding-agent` | — | — |
| `content-strategist` | — | ahrefs, semrush |
| `competitor-intel` | — | ahrefs, semrush |
| `aeo-geo-specialist` | — | — |
| `copywriter` | — | — |
| `longform-writer` | — | wordpress |
| `pseo-engineer` | — | wordpress |
| `tech-seo-auditor` | — | gsc, bing_wmt |
| `on-page-optimizer` | — | gsc, wordpress |
| `local-seo-agent` | — | gsc |
| `off-page-strategist` | — | ahrefs |
| `influencer-agent` | — | — |
| `ad-expert` | google_ads, meta_ads | linkedin_ads |
| `analytics-expert` | ga4, gsc | bing_wmt |
| `reporting-agent` | ga4, gsc | — |
| `qa-pipeline` | — | — |
| `atlas-orchestrator` | — | slack |

---

## Prompt Override System

Every skill supports a **Prompt Override** field that allows the user to:
1. Replace the default system prompt entirely
2. Add additional context to the default prompt
3. Specify custom output formats
4. Target specific audiences or tones

### How It Works:
1. User selects skill and client
2. User enters Prompt Override (optional)
3. System combines: `default_prompt + override_context`
4. Edge function sends combined prompt to MiniMax M3
5. Result is QA-checked and stored

### Example Overrides:

**For `copywriter`:**
```
Override: "Write in a conversational, friendly tone for small business owners. 
Avoid jargon. Use short sentences. Include a clear CTA at the end."
```

**For `aeo-geo-specialist`:**
```
Override: "Focus on dental industry. Target keywords: 'dental practice automation', 
'dental AI scheduling', 'dental patient intake automation'."
```

**For `pseo-engineer`:**
```
Override: "Create programmatic pages for real estate agents by city. 
Data source: MLS listings. Template: [City] Real Estate AI Automation."
```

---

## Integration with MiniMax M3

All skills use MiniMax M3 as the primary AI provider:
- **Model:** MiniMax-M3
- **Context Window:** 1M tokens
- **Features:** Reasoning split, streaming, tool calling
- **Cost:** $0.0015/1K input, $0.006/1K output
- **System Prompt Optimization:** All prompts include step-by-step reasoning instructions

---

*Document version: 1.0*  
*Last updated: 2026-07-09*  
*Next review: 2026-08-09*
