# AgenticMarketingPro — Deployment Guide

> Complete production deployment guide for the AgenticMarketingPro operating system: Vercel admin dashboard + Supabase database + Kimi Work poller + cron-job.org triggers.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Architecture Overview](#architecture-overview)
- [Step 1: Supabase Database](#step-1-supabase-database)
- [Step 2: Vercel Admin Dashboard](#step-2-vercel-admin-dashboard)
- [Step 3: Kimi Work Poller](#step-3-kimi-work-poller)
- [Step 4: Scheduled Triggers (cron-job.org)](#step-4-scheduled-triggers-cron-jobsorg)
- [Step 5: Test the Full Loop](#step-5-test-the-full-loop)
- [Environment Variables Reference](#environment-variables-reference)
- [Troubleshooting](#troubleshooting)
- [Updating After Deployment](#updating-after-deployment)
- [Security Considerations](#security-considerations)
- [Next Steps](#next-steps)

---

## Prerequisites

| Tool | Version | Purpose | Link |
|------|---------|---------|------|
| Node.js | 18+ | Vercel admin build | [nodejs.org](https://nodejs.org) |
| npm or pnpm | 8+ | Package management | [pnpm.io](https://pnpm.io) |
| Python | 3.9+ | Kimi Work poller + skills | [python.org](https://python.org) |
| Git | 2.30+ | Source control | [git-scm.com](https://git-scm.com) |
| Supabase account | — | Database + Realtime | [supabase.com](https://supabase.com) |
| Vercel account | — | Hosting (free tier) | [vercel.com](https://vercel.com) |
| cron-job.org account | — | Scheduled triggers (free) | [cron-job.org](https://cron-job.org) |

**Optional but recommended:**
- [Vercel CLI](https://vercel.com/docs/cli) for command-line deployment
- [Supabase CLI](https://supabase.com/docs/guides/cli) for local database development

---

## Architecture Overview

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│      Vercel         │     │     Supabase        │     │     Kimi Work       │
│   (Next.js Admin)   │ ←→  │   (PostgreSQL DB)   │ ←→  │   (Local Poller)    │
│                     │     │   + Realtime        │     │   + Skills          │
│  • Dashboard        │     │   + Storage         │     │   + Vault           │
│  • Skills editor    │     │                     │     │   + RAG             │
│  • Job queue UI     │     │  • clients table    │     │   + API wrappers    │
│  • Form launcher    │     │  • skills table     │     │                     │
│  • Brain map iframe │     │  • jobs table ←     │     │  • Polls jobs       │
│                     │     │  • agent_logs       │     │  • Executes skills  │
│  HTTPS endpoint     │     │  • form_responses   │     │  • Writes results   │
│  /api/webhook       │     │  • kpis             │     │  • Updates vault    │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
         ↑                          ↑                          ↑
         │                          │                          │
   cron-job.org               User fills forms          Local filesystem
   (free external              in browser              (.env, vault .md)
    cron scheduler)
```

### Data Flow: End to End

1. **User clicks "Run Agent"** in Vercel admin → Vercel writes `job` row to Supabase (`status: pending`)
2. **Supabase Realtime** pushes new job to any connected frontend (live UI updates)
3. **Kimi Work poller** (running on your local machine) polls every 5 min → picks up `pending` job
4. **Poller marks job `running`** → loads the skill from `~/.kimi/daimon/skills/` → executes it
5. **Skill reads vault** (local `.md` files), calls APIs via wrappers, writes outputs to vault
6. **Poller writes result back** to Supabase (`status: completed`, `result: {...}`, `cost_usd: ...`)
7. **Supabase Realtime** pushes update to Vercel frontend → UI shows "Done" with result

### Vercel Limitations & Workarounds

| Vercel Limitation | Our Workaround |
|---------------------|---------------|
| Function timeout: 10s | Vercel only does DB writes (10ms). Heavy work runs on Kimi Work. |
| Cron jobs: 1000 hrs/mo | Use cron-job.org (free, unlimited) → hits `/api/webhook` → enqueues DB job. |
| No persistent filesystem | Vault stays local on Kimi Work. Supabase stores all shared state. |
| No local file access | Admin shows vault via iframe or static file hosting from Kimi Work machine. |

---

## Step 1: Supabase Database

### 1.1 Create Project

1. Go to [supabase.com](https://supabase.com) → Sign in → **New Project**
2. Name: `agentic-marketing-pro`
3. Region: Choose closest to your Kimi Work machine (e.g., `us-east-1` for US, `eu-west-1` for Europe)
4. Database password: Generate a strong one, save in 1Password
5. Wait ~2 min for provisioning

### 1.2 Get Credentials

After project is ready:

1. Go to **Project Settings → API**
2. Copy:
   - `Project URL` (e.g., `https://xxxxxxxx.supabase.co`)
   - `anon public` (starts with `eyJ...`)
   - `service_role secret` (starts with `eyJ...` — **NEVER expose this to frontend**)
3. Save all three to a secure note. You'll need them in Steps 2 and 3.

### 1.3 Run Schema

1. In Supabase dashboard, go to **SQL Editor → New Query**
2. Copy the entire contents of `supabase/schema.sql` from this repo
3. Paste into SQL Editor
4. Click **Run** → Should see "Success. No rows returned"

### 1.4 Verify Setup

```sql
-- Test: list all tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
-- Should return: clients, skills, jobs, agent_logs, form_responses, kpis

-- Test: realtime is enabled
SELECT pubname FROM pg_publication WHERE pubname = 'supabase_realtime';
```

### 1.5 Seed Skills Table

Run this to populate the skills table with all 31 agents:

```sql
INSERT INTO public.skills (slug, name, description, category, status, instructions, config) VALUES
('atlas-orchestrator', 'Atlas', 'Master orchestrator. 9-step daily ops loop, agent dispatch, HITL gates.', 'core', 'active', 'See skills/agentic-marketing-os/SKILL.md', '{}'),
('content-strategist', 'Content Strategist', 'Briefs, calendar, topic clusters, keyword opportunity scoring.', 'seo', 'active', 'See skills/content-strategist/SKILL.md', '{}'),
('competitor-intel', 'Competitor Intelligence', '5 competitor workflows: SWOT, content, backlink, ad, positioning.', 'seo', 'active', 'See skills/competitor-intel/SKILL.md', '{}'),
('gsc-expert', 'GSC Expert', 'Google Search Console monitoring, CTR opportunities, index coverage.', 'seo', 'active', 'See skills/gsc-expert/SKILL.md', '{}'),
('bing-wmt-expert', 'Bing WMT Expert', 'Bing + Copilot optimization, crawl issues, index status.', 'seo', 'active', 'See skills/bing-wmt-expert/SKILL.md', '{}'),
('tech-seo-auditor', 'Technical SEO Auditor', 'Monthly technical health audits, Core Web Vitals, site structure.', 'seo', 'active', 'See skills/tech-seo-auditor/SKILL.md', '{}'),
('longform-writer', 'Longform Writer', 'Authority articles (2,000–5,000 words), persona-matched writing.', 'content', 'active', 'See skills/longform-writer/SKILL.md', '{}'),
('copywriter', 'Copywriter', 'Landing pages, CTAs, emails, ad copy, social captions.', 'content', 'active', 'See skills/copywriter/SKILL.md', '{}'),
('on-page-optimizer', 'On-Page Optimizer', 'Title, meta, H1–H3, schema, internal linking, cannibalization.', 'seo', 'active', 'See skills/on-page-optimizer/SKILL.md', '{}'),
('video-image-producer', 'Video/Image Producer', 'Scripts, AI image prompts, infographic specs, thumbnail briefs.', 'content', 'active', 'See skills/video-image-producer/SKILL.md', '{}'),
('pseo-engineer', 'Programmatic SEO Engineer', 'Programmatic SEO at scale: data feeds, templates, guardrails.', 'seo', 'active', 'See skills/pseo-engineer/SKILL.md', '{}'),
('aeo-geo-specialist', 'AEO/GEO Specialist', 'AI citation optimization, entity registry, schema, corroboration.', 'seo', 'active', 'See skills/aeo-geo-specialist/SKILL.md', '{}'),
('off-page-strategist', 'Off-Page Strategist', 'Link building, outreach, digital PR, HARO/Connectively.', 'off-page', 'active', 'See skills/off-page-strategist/SKILL.md', '{}'),
('influencer-agent', 'Influencer Agent', 'Creator vetting, outreach, campaign management, ROI tracking.', 'off-page', 'active', 'See skills/influencer-agent/SKILL.md', '{}'),
('ad-expert', 'Ad Expert', 'Google, Meta, LinkedIn, TikTok, Reddit ads: budget, creative, targeting.', 'paid', 'active', 'See skills/ad-expert/SKILL.md', '{}'),
('social-media-manager', 'Social Media Manager', '10+ format repurposing engine, community health, calendar.', 'social', 'active', 'See skills/social-media-manager/SKILL.md', '{}'),
('email-lifecycle-agent', 'Email/Lifecycle Agent', 'Sequences, segmentation, deliverability, A/B testing.', 'email', 'active', 'See skills/email-lifecycle-agent/SKILL.md', '{}'),
('local-seo-agent', 'Local SEO Agent', 'GBP, geo-grid, review management, citation building.', 'local', 'active', 'See skills/local-seo-agent/SKILL.md', '{}'),
('analytics-expert', 'Analytics Expert', 'Weekly digests, attribution, funnels, anomaly detection.', 'analytics', 'active', 'See skills/analytics-expert/SKILL.md', '{}'),
('reporting-agent', 'Reporting Agent', 'Monthly reports, QBRs, executive summaries.', 'analytics', 'active', 'See skills/reporting-agent/SKILL.md', '{}'),
('market-signals', 'Market Signals', 'Algorithm detection, SERP volatility, trend monitoring.', 'intel', 'active', 'See skills/market-signals/SKILL.md', '{}'),
('revenue-scout', 'Revenue Scout', 'Revenue channel evaluation, expansion opportunities.', 'business', 'active', 'See skills/revenue-scout/SKILL.md', '{}'),
('forecasting-agent', 'Forecasting Agent', 'Revenue, traffic, conversion forecasting.', 'business', 'active', 'See skills/forecasting-agent/SKILL.md', '{}'),
('cro-agent', 'CRO Agent', 'A/B tests, landing page optimization, form optimization.', 'conversion', 'active', 'See skills/cro-agent/SKILL.md', '{}'),
('reputation-agent', 'Reputation Agent', 'Brand mentions, review monitoring, crisis response.', 'reputation', 'active', 'See skills/reputation-agent/SKILL.md', '{}'),
('onboarding-agent', 'Onboarding Agent', '30-day client intake, 47-item audit, setup checklist.', 'operations', 'active', 'See skills/onboarding-agent/SKILL.md', '{}'),
('pitch-agent', 'Pitch Agent', 'Proposal building, competitive audits, pitch decks.', 'sales', 'active', 'See skills/pitch-agent/SKILL.md', '{}'),
('playbook-librarian', 'Playbook Librarian', 'SOP maintenance, versioning, institutional knowledge.', 'operations', 'active', 'See skills/playbook-librarian/SKILL.md', '{}'),
('martech-integration-agent', 'MarTech Integration Agent', 'API health, credential rotation, integration mapping.', 'operations', 'active', 'See skills/martech-integration-agent/SKILL.md', '{}'),
('qa-pipeline', 'QA Pipeline', '7-check QA: brand voice, factual, legal, formatting, SEO, brief, plagiarism.', 'operations', 'active', 'See skills/qa-pipeline/SKILL.md', '{}'),
('agent-prompt-engineer', 'Agent Prompt Engineer', '5-layer agent config template builder.', 'operations', 'active', 'See skills/agent-prompt-engineer/SKILL.md', '{}');
```

### 1.6 Enable Realtime (Already in Schema)

The schema already includes:
```sql
ALTER PUBLICATION supabase_realtime ADD TABLE public.jobs;
ALTER PUBLICATION supabase_realtime ADD TABLE public.agent_logs;
```

Verify in Supabase dashboard → **Database → Realtime** → `jobs` and `agent_logs` should be listed.

---

## Step 2: Vercel Admin Dashboard

### 2.1 Install Dependencies

```bash
cd web/
npm install
# or: pnpm install
```

### 2.2 Configure Environment

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```bash
# Required: from Supabase Project Settings → API
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...  # anon key (public)

# Optional: for webhook verification
WEBHOOK_SECRET=your-webhook-secret-here  # any random string, save it for Step 4
```

### 2.3 Test Locally

```bash
npm run dev
# Open http://localhost:3000
```

You should see the dashboard with:
- 6 metric cards (all showing 0 — no data yet)
- Navigation sidebar with 7 sections
- Empty job table

### 2.4 Deploy to Vercel

**Option A: Vercel CLI**
```bash
# Install Vercel CLI if not already
npm i -g vercel

# Deploy
vercel --prod
# Follow prompts, link to your project
```

**Option B: Git Integration**
1. Push repo to GitHub
2. Go to [vercel.com](https://vercel.com) → Import Project → Select repo
3. Framework preset: Next.js
4. Root directory: `web/` (IMPORTANT — not the repo root)
5. Environment variables: Add `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY`
6. Deploy

**Option C: Manual Upload**
```bash
cd web/
vercel build
# Or zip the .next/standalone output and upload via Vercel dashboard
```

### 2.5 Verify Deployment

1. Open your Vercel URL (e.g., `https://amp-admin.vercel.app`)
2. You should see the dark dashboard
3. `/api/webhook` should return: `{"status": "ok", "message": "Webhook endpoint active..."}`
4. `/api/jobs` should return: `{"jobs": []}` (empty — no jobs yet)
5. `/api/skills` should return all 31 seeded skills

### 2.6 Add Webhook Secret to Vercel

In Vercel dashboard → Project Settings → Environment Variables:
- Add `WEBHOOK_SECRET` with the same value you set in `.env.local`
- Redeploy (environment variables need a new deploy)

---

## Step 3: Kimi Work Poller

The poller runs on your local machine (where Kimi Work is installed). It connects to Supabase, polls for jobs, and executes agent skills.

### 3.1 Install Python Dependencies

```bash
# From the project root
cd "F:\Agentic Marketing Pro\marketing"  # or your equivalent

# Install Supabase Python client
pip install supabase

# Verify all other deps are installed
pip install -r infrastructure/requirements.txt
```

### 3.2 Configure Environment

Add to your main `.env` file (project root, alongside `OPENAI_API_KEY`):

```bash
# Supabase (Service Role Key — this has full DB access, keep it secret)
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # service_role key (NOT the anon key)
```

### 3.3 Test the Poller

```bash
# Single run (processes pending jobs once, then exits)
python infrastructure/webhooks/poller.py --once --verbose
```

Expected output:
```
2025-06-20 12:00:00 | amp.poller | INFO | ========================================
2025-06-20 12:00:00 | amp.poller | INFO | AgenticMarketingPro — Job Poller
2025-06-20 12:00:00 | amp.poller | INFO | ========================================
2025-06-20 12:00:01 | amp.poller | INFO | No pending jobs
2025-06-20 12:00:01 | amp.poller | INFO | Processed 0 jobs. Exiting.
```

### 3.4 Run Continuously

```bash
# Run in background (Linux/macOS)
python infrastructure/webhooks/poller.py --interval 300 &

# Or with nohup
nohup python infrastructure/webhooks/poller.py --interval 300 > poller.log 2>&1 &

# On Windows, use PowerShell
Start-Process python -ArgumentList "infrastructure/webhooks/poller.py", "--interval", "300" -WindowStyle Hidden
```

### 3.5 Run as a System Service (Recommended for Production)

**Linux (systemd):**
```bash
# Create service file
sudo tee /etc/systemd/system/amp-poller.service << 'EOF'
[Unit]
Description=AgenticMarketingPro Job Poller
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/AgenticMarketingPro/marketing
Environment="SUPABASE_URL=https://xxxxxxxx.supabase.co"
Environment="SUPABASE_SERVICE_ROLE_KEY=eyJ..."
Environment="OPENAI_API_KEY=sk-..."
Environment="VAULT_ROOT=/home/your-username/AgenticMarketingPro/marketing/AgenticMarketingPro-Vault"
ExecStart=/usr/bin/python3 /home/your-username/AgenticMarketingPro/marketing/infrastructure/webhooks/poller.py --interval 300
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable amp-poller
sudo systemctl start amp-poller
sudo systemctl status amp-poller

# View logs
sudo journalctl -u amp-poller -f
```

**Windows (Task Scheduler):**
1. Open Task Scheduler → Create Basic Task
2. Name: `AMP Job Poller`
3. Trigger: When computer starts
4. Action: Start a program
5. Program: `python.exe`
6. Arguments: `infrastructure/webhooks/poller.py --interval 300`
7. Start in: `F:\Agentic Marketing Pro\marketing` (your project root)
8. Check "Run whether user is logged on or not"

---

## Step 4: Scheduled Triggers (cron-job.org)

This replaces Vercel's limited cron functionality with a free, unlimited external scheduler.

### 4.1 Create Account

1. Go to [cron-job.org](https://cron-job.org)
2. Sign up with email → Verify → Log in

### 4.2 Create Daily Ops Trigger

1. Click **Create cronjob**
2. Title: `AMP — Daily Ops Loop`
3. Address: `https://your-vercel-app.vercel.app/api/webhook`
   (replace with your actual Vercel URL)
4. Schedule: `Every day` → `06:00` UTC (adjust to your timezone)
5. HTTP method: `POST`
6. Request body:
   ```json
   {
     "type": "daily_ops",
     "secret": "your-webhook-secret-here",
     "payload": {
       "clients": ["all"]
     }
   }
   ```
7. Click **Create**

### 4.3 Create Weekly Report Trigger

1. Click **Create cronjob**
2. Title: `AMP — Weekly Report`
3. Address: `https://your-vercel-app.vercel.app/api/webhook`
4. Schedule: `Every week` → `Monday` → `09:00` UTC
5. HTTP method: `POST`
6. Request body:
   ```json
   {
     "type": "weekly_report",
     "secret": "your-webhook-secret-here",
     "payload": {
       "report_type": "weekly_digest"
     }
   }
   ```
7. Click **Create**

### 4.4 Test the Trigger

1. In cron-job.org, click the **▶ Run now** button next to your job
2. Check Vercel logs: `vercel logs` or Vercel dashboard → Logs
3. You should see a POST to `/api/webhook` with a 200 response
4. Check Supabase: `SELECT * FROM jobs WHERE type = 'daily_ops';` — should show a new row with `status: pending`
5. Check Kimi Work poller logs: should show "Found 1 pending jobs" and process it

### 4.5 Alternative: Test Webhook Manually

```bash
# From your local machine
curl -X POST https://your-vercel-app.vercel.app/api/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "type": "daily_ops",
    "secret": "your-webhook-secret-here",
    "payload": {"clients": ["all"]}
  }'
```

Expected response:
```json
{
  "status": "queued",
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Job 550e8400... queued for daily_ops"
}
```

---

## Step 5: Test the Full Loop

### 5.1 Test 1: Trigger from Vercel → Execute on Kimi Work → Result in Vercel

1. **In Vercel admin**, go to `/skills`
2. Click **Run** on any skill (e.g., `content-strategist`)
3. **Check Supabase:** `SELECT * FROM jobs WHERE skill_slug = 'content-strategist';`
   - Should show a new row with `status: pending`
4. **Wait up to 5 minutes** (or run poller manually)
5. **Check poller logs:** `python infrastructure/webhooks/poller.py --once --verbose`
   - Should show: `Found 1 pending jobs` → `Job started` → `Job completed`
6. **Check Supabase:** Same job should now have `status: completed` and a `result` JSON
7. **Check Vercel admin:** Go to `/jobs` → the job should show as `completed` with timestamp

### 5.2 Test 2: Form Fill → Process → Vault Creation

1. **In Vercel admin**, go to `/forms`
2. Click **Client Onboarding** → opens `forms/client-onboarding.html` in new tab
3. Fill the form with a test client (e.g., "Test Corp", `https://testcorp.com`)
4. Click **Submit & Save** → downloads `client-onboarding-response.json`
5. **Run the processor:**
   ```bash
   python infrastructure/ui/processors.py client forms/client-onboarding-response.json
   ```
6. **Check vault:** `AgenticMarketingPro-Vault/01-Clients/test-corp/` should exist with `client-profile.md`, `website-manifest.md`, `kpis-and-goals.md`, `strategy-90-day.md`
7. **Check Supabase:** `SELECT * FROM clients WHERE slug = 'test-corp';` should show the new client
8. **Check Vercel admin:** Go to `/clients` → Test Corp should appear

### 5.3 Test 3: Scheduled Trigger → Daily Ops Loop

1. **In cron-job.org**, click **Run now** on your `AMP — Daily Ops Loop` job
2. **Check Supabase:** A new job with `type: 'daily_ops'` should appear
3. **Check poller logs:** Should process it within 5 minutes
4. **Check vault:** `AgenticMarketingPro-Vault/11-Ops/daily-ops-log.md` should be updated

### 5.4 Test 4: Realtime Updates (Live UI)

1. **Open Vercel admin** `/jobs` in two browser tabs
2. **Trigger a job** from one tab (click Run on a skill)
3. **Watch the other tab:** The new job should appear automatically without refresh (Supabase Realtime)

---

## Environment Variables Reference

### `.env` (Project Root — Kimi Work Machine)

```bash
# === Supabase (for poller) ===
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ...  # service_role key (secret!)

# === LLM / Embeddings ===
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
KIMI_API_KEY=...
MINIMAX_API_KEY=...

# === SEO APIs ===
AHREFS_API_KEY=...
SEMRUSH_API_KEY=...
SERPAPI_KEY=...

# === Google APIs ===
GOOGLE_CLIENT_SECRETS_FILE=client_secrets.json
GA4_PROPERTY_ID=properties/123456789
GSC_PROPERTY=https://example.com/
BING_API_KEY=...

# === Paid Ads ===
GOOGLE_ADS_DEVELOPER_TOKEN=...
META_ACCESS_TOKEN=...
LINKEDIN_ADS_TOKEN=...

# === Social / CRM ===
HUBSPOT_API_KEY=...
SLACK_WEBHOOK_URL=...

# === Monitoring ===
CLOUDFLARE_API_TOKEN=...
PAGESPEED_API_KEY=...

# === Paths ===
VAULT_ROOT=./AgenticMarketingPro-Vault
LOG_DIR=./AgenticMarketingPro-Vault/11-Ops/agent-logs
COST_LOG=./AgenticMarketingPro-Vault/11-Ops/agent-logs/cost-tracker.jsonl
HEALTH_LOG=./AgenticMarketingPro-Vault/11-Ops/agent-logs/health-check.jsonl

# === Budgets ===
LLM_DAILY_BUDGET_USD=5.0
LLM_MONTHLY_BUDGET_USD=100.0
```

### `web/.env.local` (Vercel Admin)

```bash
# === Supabase (public — these go to the browser) ===
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...  # anon key (safe for frontend)

# === Webhook Security ===
WEBHOOK_SECRET=your-webhook-secret-here
```

### Vercel Dashboard Environment Variables

If you deployed via Git integration, also set these in Vercel dashboard → Project Settings → Environment Variables:

| Variable | Value | Environment |
|----------|-------|-------------|
| `NEXT_PUBLIC_SUPABASE_URL` | `https://...` | Production, Preview, Development |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` | Production, Preview, Development |
| `WEBHOOK_SECRET` | `your-secret` | Production, Preview |

---

## Troubleshooting

### Problem: Poller can't connect to Supabase

**Symptoms:** `Failed to initialize Supabase: ...` or `Connection refused`

**Fixes:**
1. Check `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` in `.env` (project root, not `web/.env.local`)
2. Verify the service key is correct (Project Settings → API → service_role)
3. Check if `supabase` Python package is installed: `pip install supabase`
4. Test connectivity: `curl $SUPABASE_URL/rest/v1/skills?select=* -H "apikey: $SUPABASE_SERVICE_ROLE_KEY"`

### Problem: Vercel API returns 500

**Symptoms:** `{"error": "..."}` when calling `/api/jobs` or `/api/webhook`

**Fixes:**
1. Check Vercel logs: `vercel logs` or dashboard → Logs
2. Verify `NEXT_PUBLIC_SUPABASE_URL` and `NEXT_PUBLIC_SUPABASE_ANON_KEY` are set in Vercel
3. Make sure Supabase RLS is configured (the schema has `CREATE POLICY "Allow all"` for MVP)
4. Test locally: `npm run dev` → `curl http://localhost:3000/api/jobs`

### Problem: Webhook returns 401 Unauthorized

**Symptoms:** `{"error": "Unauthorized"}`

**Fixes:**
1. Check `WEBHOOK_SECRET` is set in Vercel environment variables
2. Make sure the POST body includes `"secret": "your-webhook-secret-here"`
3. The secret must match exactly (case-sensitive)
4. For testing without secret: remove `WEBHOOK_SECRET` from Vercel env (not recommended for production)

### Problem: cron-job.org trigger fails

**Symptoms:** Job shows "Failed" in cron-job.org dashboard

**Fixes:**
1. Check Vercel URL is correct (include `https://`)
2. Verify the POST body is valid JSON (no trailing commas)
3. Check Vercel function logs for the error
4. Test manually with `curl` first (see Step 4.5)

### Problem: Realtime updates not showing in UI

**Symptoms:** New jobs appear only after page refresh

**Fixes:**
1. Verify Supabase Realtime is enabled for `jobs` table: Database → Realtime → check `jobs`
2. Check browser console for WebSocket errors
3. The Vercel admin doesn't yet subscribe to Realtime — this requires adding a Supabase Realtime subscription in the React components (future enhancement)
4. Workaround: Add a `setInterval` poll in `useEffect` (already in the jobs page)

### Problem: Poller executes jobs but skills don't run

**Symptoms:** Jobs show `completed` but no vault files created

**Fixes:**
1. The `execute_job()` in `poller.py` is currently a **stub**. It logs but doesn't actually run skills.
2. To wire it: edit `poller.py` line ~120, replace the stub with actual skill dispatch
3. Or: run skills manually via Kimi Work while the poller is still being developed

### Problem: Cost tracking shows $0

**Symptoms:** All jobs have `cost_usd: 0`

**Fixes:**
1. Cost tracking is not yet wired to the poller. The `cost_tracker.py` exists but isn't called during job execution.
2. To wire it: import `CostTracker` in `poller.py` and call `log_call()` after each skill execution.

---

## Updating After Deployment

### Update Supabase Schema

```bash
# If you make changes to schema.sql, apply them via Supabase SQL Editor
# Or use Supabase CLI:
supabase db push
```

### Update Vercel Admin

```bash
cd web/
git pull origin main  # if using Git integration
npm install
npm run build
vercel --prod  # or push to Git for auto-deploy
```

### Update Kimi Work Skills

```bash
# On your Kimi Work machine:
cd "F:\Agentic Marketing Pro\marketing"
git pull origin main

# Copy updated skills to Kimi managed directory
cp -r skills/* ~/.kimi/daimon/skills/

# Restart poller if running as service
sudo systemctl restart amp-poller
```

### Update Poller

```bash
git pull origin main
# The poller will pick up changes on next restart
# If running as systemd service:
sudo systemctl restart amp-poller
```

---

## Security Considerations

### Current State (MVP — Tighten Before Production)

| Risk | Current State | Recommended Fix |
|------|-------------|---------------|
| **RLS policies** | `Allow all` (no auth) | Add Supabase Auth + row-level policies per user |
| **Webhook secret** | Optional | Make mandatory, use strong random string |
| **Service role key** | In `.env` on local machine | Keep it there. Never commit to Git. Never expose to frontend. |
| **API keys** | In `.env` | Use a secrets manager (1Password, Doppler) for production |
| **Vercel admin** | No auth | Add Clerk/NextAuth.js for login |
| **Poller logs** | Local file | Rotate logs, don't log sensitive data |

### Recommended Hardening (Phase 2)

1. **Add authentication** to Vercel admin using [Clerk](https://clerk.com) or [NextAuth.js](https://next-auth.js.org)
2. **Replace RLS policies** with user-specific policies (e.g., `USING (auth.uid() = user_id)`)
3. **Add rate limiting** to `/api/webhook` (Vercel Edge Config or Upstash Redis)
4. **Encrypt sensitive vault data** at rest (Supabase has encryption options)
5. **Add IP allowlisting** to Supabase (Project Settings → API → IP Allowlist)
6. **Use Doppler or HashiCorp Vault** for secret management instead of `.env` files

---

## Next Steps

After successful deployment, here are the recommended priorities:

### Immediate (Week 1)
- [ ] Wire `execute_job()` in `poller.py` to actually run skills (not just a stub)
- [ ] Add authentication to Vercel admin (Clerk recommended)
- [ ] Add real-time job updates via Supabase Realtime subscription
- [ ] Create your first real client via the onboarding form
- [ ] Run a full daily ops loop end-to-end and verify all outputs in the vault

### Short Term (Month 1)
- [ ] Add email/Slack notifications for failed jobs and completed reports
- [ ] Build the Analytics page with charts (Recharts already installed)
- [ ] Add client-specific dashboards (filter jobs, KPIs, reports by client)
- [ ] Wire cost tracking so the dashboard shows real spend
- [ ] Add job retry logic (failed jobs auto-retry up to 3x)

### Medium Term (Month 2-3)
- [ ] Add multi-user support (team members, roles, permissions)
- [ ] Build an API playground for testing individual skills
- [ ] Add AI-powered chat interface in the admin (ask questions about any client)
- [ ] Integrate with Kimi Work's native tools for deeper orchestration
- [ ] Add automated billing/invoicing based on job execution logs

---

## Support & Resources

| Resource | Location |
|----------|----------|
| **Skills** | `skills/*/SKILL.md` (31 skills) |
| **Forms** | `forms/*.html` (30 interactive forms) |
| **API Wrappers** | `infrastructure/api_client/` (6 wrappers) |
| **RAG Pipeline** | `infrastructure/rag/pipeline.py` |
| **Poller** | `infrastructure/webhooks/poller.py` |
| **Schema** | `supabase/schema.sql` |
| **Admin** | `web/` (Next.js 14) |
| **Main README** | `README.md` (project root) |

---

*Last updated: 2025-06-20*
*AgenticMarketingPro v1.0 — Production Deployment Guide*
