# AgenticMarketingPro — AI-Native Marketing OS

> The full agent operating system for running a digital marketing agency with AI. 30 specialist agents, an Obsidian vault brain, and a RAG pipeline that compounds with every client engagement.

## What's in This Repo

```
AgenticMarketingPro-Vault/   ← The Obsidian vault (persistent data, client files, logs)
  00-Agency-Core/            ← Mission, ICPs, pricing, brand voice, positioning
  01-Clients/                ← One folder per active client
  02-Competitors/            ← Competitor intelligence maps
  03-SEO-Intelligence/       ← Keywords, topic clusters, GSC/Bing logs
  04-Content-Production/     ← Briefs, drafts, published index, writer personas
  05-Programmatic-SEO/       ← pSEO templates, data sources, guardrails
  06-AEO-GEO/                ← AI citation tracking, entity registry, schema
  07-Off-Page/               ← Link prospects, outreach, DR tracker
  08-Paid-Ads/               ← Campaigns, ad copy, budget, audiences
  09-Social/                 ← Calendars, repurpose queue, community health
  10-Analytics/              ← Weekly digests, anomaly logs, attribution, KPIs
  11-Ops/                    ← Agent configs, playbooks, integrations, logs

skills/                      ← Kimi Work runtime skills (30 agent capabilities)
  agentic-marketing-os/      ← Atlas orchestrator (master skill)
  agent-prompt-engineer/     ← 5-layer config builder
  qa-pipeline/               ← 7-check QA system
  content-strategist/        ← Briefs, calendar, topic clusters
  competitor-intel/          ← 5 competitor workflows
  longform-writer/           ← Authority articles (2,000–5,000 words)
  on-page-optimizer/         ← Title, meta, H1–H3, schema, links
  off-page-strategist/       ← Link building, outreach, PR
  gsc-expert/                ← Google Search Console monitoring
  bing-wmt-expert/           ← Bing + Copilot optimization
  aeo-geo-specialist/        ← AI citation optimization
  pseo-engineer/             ← Programmatic SEO at scale
  ad-expert/                 ← Google, Meta, LinkedIn, TikTok, Reddit ads
  copywriter/                ← Landing pages, CTAs, emails, ad copy
  social-media-manager/      ← 10+ format repurposing engine
  email-lifecycle-agent/     ← Sequences, segmentation, deliverability
  local-seo-agent/           ← GBP, geo-grid, reviews, citations
  tech-seo-auditor/          ← Monthly technical health audits
  analytics-expert/          ← Weekly digests, attribution, funnels
  revenue-scout/             ← Revenue channel evaluation
  market-signals/            ← Algorithm detection, trend monitoring
  reporting-agent/           ← Monthly reports, QBRs
  reputation-agent/          ← Brand mentions, reviews, crisis response
  cro-agent/                 ← A/B tests, landing page optimization
  onboarding-agent/          ← 30-day client intake, 47-item audit
  pitch-agent/               ← Proposal building, competitive audits
  forecasting-agent/           ← Revenue, traffic, conversion forecasting
  influencer-agent/          ← Creator vetting, outreach, campaigns
  video-image-producer/      ← Scripts, AI prompts, infographic specs
  playbook-librarian/        ← SOP maintenance, versioning
  martech-integration-agent/ ← API health, credentials, integrations

agentic_marketing_os_master_plan.html         ← Visual agent architecture dashboard
obsidian_rag_techstack_architecture.html    ← RAG pipeline & tech stack docs
```

## How It Works

### Two-Location Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| **Skills** (`skills/`) | Runtime capabilities — How agents execute | Procedural memory for 30+ specialist roles |
| **Vault** (`AgenticMarketingPro-Vault/`) | Persistent data — What agents know and produce | Client data, competitor maps, content, KPIs, logs |

### Daily Ops Loop (Atlas Orchestrator)

1. **Site Health Check** → tech-seo-auditor
2. **GSC / Bing Monitoring** → gsc-expert, bing-wmt-expert
3. **Content Brief Generation** → content-strategist
4. **Writer Assignment** → longform-writer (matched to persona)
5. **On-Page Review** → on-page-optimizer
6. **Social Repurposing** → social-media-manager
7. **Outreach Queue** → off-page-strategist
8. **Analytics Digest** → analytics-expert
9. **Profit Plan Update** → Atlas (revenue-scout weekly)

All outputs are written to the vault with YAML frontmatter. All actions are logged. HITL gates enforce human approval on high-risk decisions.

## The 7 Non-Negotiables

1. **Obsidian is the single source of truth**
2. **Every agent reads before it writes** (RAG context injection)
3. **Every action is logged** (inputs, context, outputs, cost, latency)
4. **Humans approve high-risk decisions** (10 HITL gates)
5. **No PII in the vault** (credentials in 1Password, not vault)
6. **Every output passes QA** (7-check pipeline)
7. **The vault compounds** (every engagement captured, every decision logged)

## 10 Human-in-the-Loop Gates

1. Publish content
2. Send outreach email
3. Change ad budget >$100/day
4. Modify site technical structure
5. Publish pSEO batch >50 pages
6. Respond to negative review (<3 stars)
7. Send client report
8. Approve agent prompt change
9. Launch new client campaign
10. Declare incident

## Getting Started

### 1. Open the Vault in Obsidian
1. Install [Obsidian](https://obsidian.md/)
2. Open `AgenticMarketingPro-Vault/` as a vault
3. Install plugins: Dataview, Templater, Obsidian Git, Smart Connections

### 2. Install Skills (for Kimi Work)
Skills are managed in `~/.kimi/daimon/skills/` on your Kimi Work runtime. Copy the `skills/` folder contents there to make them active.

### 3. Configure Secrets
- Store API credentials in 1Password or HashiCorp Vault
- Reference them by environment variable name in `AgenticMarketingPro-Vault/11-Ops/integrations/`
- Never commit credentials to this repo

### 4. Stand Up the RAG Pipeline
1. Install Chroma DB: `pip install chromadb`
2. Install LlamaIndex: `pip install llama-index`
3. Run ingestion script (TBD) to index all vault `.md` files
4. Verify with sample query

### 5. Run the Daily Ops Loop
Trigger via Kimi Work Cron or manually: "Run the daily ops loop for [client]"

## Business Model

| Tier | Monthly | Best For |
|------|---------|----------|
| Starter | $2,500 | Early-stage startups |
| Growth | $4,500 | Series A–C SaaS, scaling e-commerce |
| Scale | $8,500 | Growth-stage with in-house marketing lead |
| Enterprise | $15,000+ | Series C+ / public companies |

2026 Targets: $15K MRR (Q1) → $75K MRR (Q4), 17 active clients, 65% gross margin.

## License

This is proprietary software for the AgenticMarketingPro agency. All agent configs, playbooks, and operational procedures are confidential.

---

*Built with Kimi Work. The vault is the agency's primary moat.*
