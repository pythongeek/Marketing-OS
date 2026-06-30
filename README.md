# AgenticMarketingPro

> A complete AI-native marketing agency operating system. 31 specialized agents, interactive HTML forms, a visual Next.js admin dashboard, and a Supabase-backed job queue — all orchestrated by Kimi Work.

---

## 🚀 Quick Start (Vercel Deployment)

This repo is designed to deploy to **Vercel** in minutes. The admin dashboard lives in the `web/` folder.

### 1. Deploy to Vercel (One-Click)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/pythongeek/Marketing-OS)

**Important:** During import, set the **Root Directory** to `web/`:

```
Vercel Import Settings:
├── Framework Preset: Next.js
├── Root Directory: web/        ← IMPORTANT
└── Build Command: (default)
```

### 2. Add Environment Variables

In Vercel dashboard → Project Settings → Environment Variables, add:

| Variable | Value | Environment |
|----------|-------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://your-project.supabase.co` | Production, Preview, Development |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` | Production, Preview, Development |
| `WEBHOOK_SECRET` | `your-secret-string` | Production, Preview |

Get these from your [Supabase project](https://supabase.com) → Settings → API.

### 3. Set Up Supabase Database

1. Create a free project at [supabase.com](https://supabase.com)
2. Go to SQL Editor → New Query
3. Paste the contents of [`supabase/schema.sql`](supabase/schema.sql)
4. Click **Run**
5. Seed the skills table: paste the SQL from `DEPLOYMENT.md` Section 1.5

### 4. Set Up Kimi Work Poller (Local Machine)

On the machine where Kimi Work runs:

```bash
# Clone this repo
git clone https://github.com/pythongeek/Marketing-OS.git
cd Marketing-OS

# Install Python dependencies
pip install -r infrastructure/requirements.txt
pip install supabase

# Add to .env:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_SERVICE_KEY=your-service-role-key
# OPENAI_API_KEY=sk-...

# Run the poller
python infrastructure/webhooks/poller.py --verbose
```

Full instructions: [`DEPLOYMENT.md`](DEPLOYMENT.md)

---

## 📁 Repo Structure

```
Marketing-OS/
├── web/                          ← Next.js admin dashboard (Vercel deploys this)
│   ├── app/                      ← Pages: Dashboard, Clients, Skills, Jobs, Forms, Brain Map
│   ├── app/api/                  ← API routes: /webhook, /jobs, /skills, /clients
│   ├── components/             ← Nav, StatusBadge, MetricCard
│   ├── lib/supabase.ts           ← Supabase client + types
│   ├── package.json
│   └── .env.example
│
├── skills/                       ← 31 agent skill definitions (Kimi Work runtime)
│   ├── agentic-marketing-os/     ← Atlas orchestrator (master)
│   ├── onboarding-agent/
│   ├── content-strategist/
│   ├── gsc-expert/
│   ├── ad-expert/
│   ├── social-media-manager/
│   └── ... (31 total)
│
├── forms/                        ← 30 interactive HTML forms (dark theme, auto-save, JSON export)
│   ├── client-onboarding.html    ← 24 fields, creates vault folder
│   ├── api-credentials.html      ← 23 API integrations
│   ├── wordpress-config.html     ← WP REST API setup
│   ├── content-brief.html
│   ├── competitor-intake.html
│   ├── ad-campaign.html
│   └── ... (30 total)
│
├── infrastructure/               ← Python execution layer
│   ├── api_client/             ← GSC, GA4, Ahrefs, Semrush, Bing, WordPress
│   ├── rag/                    ← ChromaDB + LlamaIndex pipeline
│   ├── ui/                     ← Form engine + response processors
│   ├── webhooks/             ← Kimi Work poller (polls Supabase jobs)
│   ├── scripts/                ← ingest_vault, health_check, cost_tracker, generate_dashboard
│   ├── config.py               ← Central config (50+ env vars)
│   └── requirements.txt
│
├── AgenticMarketingPro-Vault/  ← Obsidian vault (persistent data, NOT deployed to Vercel)
│   ├── 00-Agency-Core/
│   ├── 01-Clients/
│   ├── 03-SEO-Intelligence/
│   ├── 04-Content-Production/
│   └── ... (11 folders)
│
├── supabase/
│   └── schema.sql              ← Database schema (6 tables, indexes, RLS, triggers, realtime)
│
├── .env.example                ← Root .env template (Kimi Work machine)
├── web/.env.example            ← Vercel admin .env template
├── DEPLOYMENT.md               ← Full production deployment guide (29.7 KB)
└── README.md                   ← This file
```

---

## 🧠 The 31 Agents

| Category | Agents |
|----------|--------|
| **Core** | Atlas Orchestrator, QA Pipeline, Agent Prompt Engineer |
| **SEO** | Content Strategist, Competitor Intel, GSC Expert, Bing WMT Expert, On-Page Optimizer, Technical SEO Auditor, PSEO Engineer, AEO/GEO Specialist, Local SEO Agent |
| **Content** | Longform Writer, Copywriter, Video/Image Producer |
| **Off-Page** | Off-Page Strategist, Influencer Agent |
| **Paid** | Ad Expert |
| **Social** | Social Media Manager |
| **Email** | Email/Lifecycle Agent |
| **Analytics** | Analytics Expert, Reporting Agent, Market Signals |
| **Business** | Revenue Scout, Forecasting Agent, CRO Agent, Pitch Agent |
| **Operations** | Onboarding Agent, Playbook Librarian, MarTech Integration Agent, Reputation Agent |

Every skill is **form-first interactive**: when data is missing, the agent generates an HTML form, the user fills it in their browser, and the agent processes the response.

---

## 🎨 The Admin Dashboard

### Pages

| Page | What You Can Do |
|------|-----------------|
| **Dashboard** | View metrics (clients, skills, jobs, cost), recent jobs, quick actions |
| **Clients** | View active clients, onboard new ones via form link, open vault files |
| **Skills** | View all 31 agents, edit instructions inline, trigger runs, open forms |
| **Jobs** | Monitor job queue, filter by status, track execution history and cost |
| **Forms** | Launch any of the 30 interactive HTML forms in a new tab |
| **Brain Map** | View the interactive D3.js force-directed graph of vault entities |
| **Analytics** | (Future: charts, KPIs, reports) |

### Features

- **Dark theme** (`#0f0f1a` background) matching the form aesthetic
- **Real-time job updates** via Supabase polling
- **Inline skill editing** — edit agent instructions directly in the browser
- **One-click agent runs** — enqueue a job for any skill
- **Cost tracking** — monitor cumulative agent spend
- **Mobile responsive** — works on phone, tablet, desktop

---

## 🔗 How the Pieces Connect

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│      Vercel         │     │     Supabase        │     │     Kimi Work       │
│   (Next.js Admin)   │ ←→  │   (PostgreSQL DB)   │ ←→  │   (Local Poller)    │
│                     │     │   + Realtime        │     │   + Skills + Vault    │
│  • Dashboard        │     │                     │     │                     │
│  • Skills editor    │     │  • clients table    │     │  • Polls jobs         │
│  • Job queue UI     │     │  • skills table     │     │  • Executes skills    │
│  • Form launcher    │     │  • jobs table ←     │     │  • Writes results     │
│  • Brain map iframe │     │  • agent_logs       │     │  • Updates vault      │
│                     │     │  • form_responses   │     │                     │
│  /api/webhook       │     │  • kpis             │     │   ~/.kimi/daimon/     │
│  (POST receiver)    │     │                     │     │   skills/             │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         ↑                          ↑                          ↑
         │                          │                          │
   cron-job.org               User fills forms          Local filesystem
   (free external              in browser              (.env, vault .md)
    cron scheduler)
```

### Data Flow: End to End

1. **User clicks "Run Agent"** in Vercel admin → Vercel writes `job` row to Supabase (`status: pending`)
2. **Kimi Work poller** (running on your local machine) polls every 5 min → picks up `pending` job
3. **Poller marks job `running`** → loads the skill from `~/.kimi/daimon/skills/` → executes it
4. **Skill reads vault** (local `.md` files), calls APIs via wrappers, writes outputs to vault
5. **Poller writes result back** to Supabase (`status: completed`, `result: {...}`, `cost_usd: ...`)
6. **Vercel admin** refreshes via polling → UI shows "Done" with result

---

## 📝 Interactive Forms

All 30 forms are **self-contained HTML files** with:
- Dark theme (matching admin dashboard)
- Conditional fields (e.g., WP fields only show if "Enable WordPress" is checked)
- Auto-save to browser localStorage (never lose progress)
- Validation (required fields, email/URL format, password masking)
- One-click JSON export (download `*-response.json`)
- Mobile responsive

### Example Flow: Client Onboarding

```bash
# 1. Agent generates form
python infrastructure/ui/form_engine.py --client-onboarding
# → forms/client-onboarding.html

# 2. User opens form in browser, fills it, clicks Submit
# → downloads client-onboarding-response.json

# 3. Agent processes response
python infrastructure/ui/processors.py client forms/client-onboarding-response.json
# → creates 01-Clients/[slug]/ with profile.md, manifest.md, kpis.md, strategy.md
```

---

## 🛠️ Local Development

### Prerequisites

- Node.js 18+ (for Vercel admin)
- Python 3.9+ (for Kimi Work infrastructure)
- Git

### Run the Admin Locally

```bash
cd web/
npm install
cp .env.example .env.local
# Edit .env.local with your Supabase credentials
npm run dev
# Open http://localhost:3000
```

### Run the Poller Locally

```bash
# From repo root
pip install -r infrastructure/requirements.txt
pip install supabase
python infrastructure/webhooks/poller.py --once --verbose
```

### Generate All Forms

```bash
python -c "from infrastructure.ui.form_engine import FormEngine; from infrastructure.ui.form_presets import FormPresets; e=FormEngine(); FormPresets(e).generate_all()"
```

---

## 📚 Documentation

| Document | What It Covers |
|----------|---------------|
| [`DEPLOYMENT.md`](DEPLOYMENT.md) | Full production deployment guide: Supabase → Vercel → Poller → Cron |
| [`infrastructure/README.md`](infrastructure/README.md) | Python infrastructure: API clients, RAG, scripts, form engine |
| [`web/.env.example`](web/.env.example) | Vercel admin environment variables |
| [`.env.example`](.env.example) | Kimi Work / local machine environment variables |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Admin UI** | Next.js 14, TypeScript, Tailwind CSS, App Router |
| **Database** | Supabase PostgreSQL + Realtime |
| **API** | Next.js API Routes, REST |
| **Agent Runtime** | Kimi Work (local) |
| **Skills** | Markdown SKILL.md files (31 agents) |
| **Forms** | Self-contained HTML with vanilla JS |
| **RAG** | ChromaDB + LlamaIndex + OpenAI embeddings |
| **API Wrappers** | Python (GSC, GA4, Ahrefs, Semrush, Bing, WordPress) |
| **Poller** | Python `supabase-py`, polling every 5 min |
| **Scheduling** | cron-job.org (free external cron) |
| **Vault** | Obsidian-compatible Markdown files |

---

## 🗺️ Roadmap

### Immediate (Week 1)
- [ ] Wire `execute_job()` in poller to actually run skills (currently a stub)
- [ ] Add authentication to Vercel admin (Clerk or NextAuth.js)
- [ ] Add real-time job updates via Supabase Realtime subscription
- [ ] Create first real client via onboarding form
- [ ] Run full daily ops loop end-to-end

### Short Term (Month 1)
- [ ] Email/Slack notifications for failed jobs and completed reports
- [ ] Analytics page with charts (Recharts already installed)
- [ ] Client-specific dashboards (filter by client)
- [ ] Real cost tracking in dashboard
- [ ] Job retry logic (failed jobs auto-retry up to 3x)

### Medium Term (Month 2-3)
- [ ] Multi-user support (team members, roles, permissions)
- [ ] API playground for testing individual skills
- [ ] AI chat interface in admin (ask questions about any client)
- [ ] Automated billing/invoicing based on job logs

---

## 🙏 Contributing

This is a private operating system for your agency. The repo is designed to be forked and customized for your specific clients, verticals, and workflows.

To add a new skill:
1. Create `skills/your-skill-name/SKILL.md` following the 5-layer template
2. Add a form in `infrastructure/ui/form_presets.py` if the skill needs user input
3. Seed the skill in Supabase `skills` table
4. Test via Vercel admin → Skills → Run

---

## 📄 License

Private / Proprietary. Built for your agency's internal use.

---

*Built with Kimi Work + Next.js + Supabase + ChromaDB + 31 specialized agents.*
*Last updated: 2025-06-20*
