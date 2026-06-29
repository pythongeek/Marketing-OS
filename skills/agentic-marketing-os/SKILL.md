---
name: agentic-marketing-os
description: The master orchestration skill for the AgenticMarketingPro agent operating system. Use when running the daily ops loop, dispatching specialist agents, managing the task queue, reviewing anomalies, generating the daily agency digest, or handling any Atlas-level orchestration duty. Covers the 9-step daily ops cycle including site health checks, GSC/Bing monitoring, content brief generation, writer assignment, on-page review, social repurposing, outreach queue management, analytics compilation, and profit plan updates. Also handles Friday self-improvement cycles and anomaly triage.
---

# Agentic Marketing OS — Atlas Orchestrator

The master skill that runs the agency. Every agent dispatch starts here.

## Architecture: Client as the Center of Gravity

Every action, every agent, every artifact is scoped to a **client** and their **website(s)**. The vault is not a flat file system — it's a graph of entities centered on the client.

```
                    ┌─────────────┐
                    │   Client    │
                    │   Profile   │
                    └──────┬──────┘
                           │ owns
           ┌───────────────┼───────────────┐
           ▼               ▼               ▼
      ┌─────────┐    ┌─────────┐    ┌─────────┐
      │ Website │    │ Website │    │ Website │
      │   #1    │    │   #2    │    │   #3    │
      └────┬────┘    └────┬────┘    └────┬────┘
           │              │              │
     ┌─────┴─────┐   ┌────┴────┐    ┌────┴────┐
     ▼           ▼   ▼         ▼    ▼         ▼
 Keywords   Pages  Competitors  Content  Agents  Metrics
```

### Key Principle
- **No agent runs without a client context**. Even agency-wide tasks (competitor intel, market signals) are tagged with the client(s) they affect.
- **Website manifest is the single source of truth** for API properties, tech stack, and known issues.
- **Every output is visualized** in the brain map and dashboard after the loop completes.

## Quick Start

1. **Read context** from the vault before any action. See `references/vault-context.md` for path mappings.
2. **Check the task queue** (`11-Ops/agent-task-queue.md`) for P1/P2 items.
3. **Run the daily ops loop** (9 steps below) or handle the specific user request.
4. **Dispatch sub-agents** via the `Agent` tool for specialist work.
5. **Write outputs** back to the vault with proper YAML frontmatter.
6. **Log every run** to `11-Ops/agent-logs/atlas/YYYY-MM-DD-[run-id].md`.

## Vault Path

`F:\Agentic Marketing Pro\marketing\AgenticMarketingPro-Vault\`

Always read relevant files from this path before acting. Never write outside this path.

## The 9-Step Daily Ops Loop (Client-Centric)

Run this sequence once per day (typically 06:00–08:00) **per active client** (or in parallel for multiple clients). Each step loads the client context before acting.

### Step 0: Client Context Load
**Before any other step**, read the client's:
- `01-Clients/[client]/client-profile.md` — goals, tier, MRR, contacts
- `01-Clients/[client]/website-manifest.md` — all domains, API properties, tech stack, known issues
- `01-Clients/[client]/kpis-and-goals.md` — current metrics and targets
- `01-Clients/[client]/competitors/` — active competitor profiles

If this is the first run for a new client, run `onboarding-agent` first.

### Step 1: Site Health Check
- Load the **primary website** from the manifest's "Domains" table.
- Read `10-Analytics/anomaly-log.md` for open issues related to this client.
- Dispatch `tech-seo-auditor` with the client's domain and tech stack as context.
- Log findings to `01-Clients/[client]/technical-fix-queue.md`.
- If critical (site down, SSL expired, CWV > threshold), **pause the loop** and alert the client contact immediately.

### Step 2: GSC / Bing Monitoring
- Load the **GSC property** and **Bing API property** from the website manifest.
- Read `03-SEO-Intelligence/gsc-weekly-log.md` and `bing-weekly-log.md` for this client.
- Dispatch `gsc-expert` with the GSC property URL from the manifest.
- Dispatch `bing-wmt-expert` with the Bing site URL from the manifest.
- Update anomaly log if material changes found (CTR drop >20%, index errors >10, new query spike >2σ).
- Write CTR opportunities to `03-SEO-Intelligence/[client]-ctr-opportunities.md`.

### Step 3: Content Brief Generation
- Read `04-Content-Production/content-calendar.md` for this client's upcoming slots.
- Read `03-SEO-Intelligence/topic-clusters.md` and `keyword-universe.md` filtered to this client's keywords.
- Dispatch `content-strategist` agent with:
  - Client's brand voice guide
  - Client's website manifest (for tech constraints: CMS, schema, URL patterns)
  - Client's competitor map (to identify content gaps)
- Briefs written to `04-Content-Production/briefs/[client]-[slug].md` with YAML frontmatter `client: [client]`.

### Step 4: Writer Assignment
- Read `04-Content-Production/briefs/` for unassigned briefs tagged with this client.
- Match brief to writer persona per `04-Content-Production/writer-persona-styles/`.
- The persona choice is influenced by the client's brand voice and ICP (from client-profile.md).
- Dispatch appropriate `longform-writer` agent with the full brief + client context.
- Update task queue with assignment: `01-Clients/[client]/agent-task-queue.md`.

### Step 5: On-Page Review
- Read `04-Content-Production/published-index.md` for this client's recent publishes.
- Dispatch `on-page-optimizer` with the client's website manifest (CMS, schema, URL patterns).
- Fix queue written to `01-Clients/[client]/technical-fix-queue.md`.
- If the client's CMS is WordPress, recommend RankMath/Yoast schema. If HubSpot, recommend HubSpot schema. If custom, recommend JSON-LD.

### Step 6: Social Repurposing
- Read `04-Content-Production/published-index.md` for this client's new content.
- Dispatch `social-media-manager` with the client's brand voice and target geo.
- Queue written to `09-Social/repurpose-queue.md` with `client: [client]` tag.
- If the client is B2B, prioritize LinkedIn + Twitter/X. If e-commerce, prioritize Instagram + TikTok. If SaaS, prioritize LinkedIn + Reddit communities.

### Step 7: Outreach Queue
- Read `07-Off-Page/link-prospects.md` for this client's domain.
- Read `07-Off-Page/outreach-log.md` for sequence status.
- Dispatch `off-page-strategist` with the client's domain and competitor backlink profiles.
- **HITL Gate 2 applies** — first 3 emails of any sequence need human approval.
- Log all outreach to `07-Off-Page/outreach-log.md` with `client: [client]` tag.

### Step 8: Analytics Digest
- Read `10-Analytics/weekly-digest.md` template.
- Load the client's GA4 property ID from the website manifest.
- Dispatch `analytics-expert` with the client's GA4 property and funnel goals.
- Write digest to `10-Analytics/weekly-digest.md` (if Monday) or `01-Clients/[client]/daily-ops-log.md`.
- Include client-specific KPIs: organic SQLs, AEO citations, CAC reduction, etc.

### Step 9: Profit Plan Update
- Read `11-Ops/profit-plan.md`.
- Update this client's MRR, OPEX, and margin using current vault data.
- If client is <50% margin or OPEX >110% of budget, **flag for founder review**.
- Update client's `client-profile.md` with current metrics.

### Step 10: Visual Dashboard Generation (NEW)
- After all 9 steps, run the visual generators:
  - `python infrastructure/scripts/generate_brain_map.py --client [client]` — generates a client-centered brain map
  - `python infrastructure/scripts/generate_dashboard.py --client [client]` — generates charts + HTML dashboard
- The brain map shows the client as the central node, connected to all websites, keywords, competitors, content, and agents.
- The dashboard shows: traffic trends, keyword rankings, CTR opportunities, agent costs, site health status.
- Output paths: `00-Agency-Core/_dashboards/brain-map-[client].html` and `dashboard-[client].html`
- **HITL Gate 7 applies** — client reports (including dashboards) need human approval before sending to the client.

## Agent Dispatch Protocol

When dispatching a sub-agent via the `Agent` tool:

1. **Read the agent config** from `11-Ops/agent-configs/[agent-name].md` first.
2. **Pull relevant vault context** — client briefs, KPIs, recent logs, playbooks.
3. **Construct the prompt** with 5 layers: Role → RAG Context → Toolset → Output Format → Escalation.
4. **Set timeout** based on task complexity: 1800s for standard, 3600s for complex.
5. **After completion**: read the agent's output, validate it exists, update the task queue.

## HITL Gate Handling

When any step triggers a HITL gate (see `references/hitl-gates.md`):

1. **Pause the loop** at that step. Do not proceed to the next step.
2. **Present the pending decision** to the human with: (a) what the agent wants to do, (b) why, (c) the risk, (d) the recommended action.
3. **Wait for explicit approval** — do not proceed on silence.
4. **On approval**: log the decision, complete the step, resume the loop.
5. **On rejection**: log the rejection, update the task queue with the revised approach, move to the next step.

## Output Format for Vault Writes

Every file written to the vault must have:

```yaml
---
type: [see references/frontmatter-standards.md for type registry]
last_updated: YYYY-MM-DD
tags: [category/value, category/value]
---
```

See `references/frontmatter-standards.md` for the full type registry and tag dictionary.

## Interactive Form-First Workflow (NEW)

Atlas is not a black box that assumes everything is configured. **When any agent needs data that doesn't exist in the vault, Atlas generates an interactive HTML form** and asks the user to fill it before proceeding.

### How It Works

```
Agent needs data → Check vault → Not found → Generate HTML form
     ↑                                                              ↓
Process response ← User fills & saves JSON ← Present form to user ←┘
```

### Form Generation Pattern

Every skill in the system can generate forms via the Form Engine:

```bash
# Client onboarding (onboarding-agent)
python infrastructure/ui/form_engine.py --client-onboarding
# → forms/client-onboarding.html

# API credentials (martech-integration-agent)
python infrastructure/ui/form_engine.py --api-credentials
# → forms/api-credentials.html

# WordPress config (wp-publishing-core)
python infrastructure/ui/form_engine.py --wordpress
# → forms/wordpress-config.html

# Content brief (content-strategist)
python infrastructure/ui/form_engine.py --content-brief
# → forms/content-brief.html
```

### Processing Form Responses

After the user fills a form and saves the JSON response:

```bash
# Create client vault folder from onboarding response
python infrastructure/ui/processors.py client forms/client-onboarding-response.json

# Write API credentials to .env
python infrastructure/ui/processors.py api forms/api-credentials-response.json

# Test WordPress connection and save config
python infrastructure/ui/processors.py wordpress forms/wordpress-config-response.json
```

### Form Features

- **Dark theme** matching the dashboard aesthetic
- **Conditional fields** (e.g., WordPress fields only show if "Enable WordPress" is checked)
- **Auto-save to localStorage** (never lose your progress)
- **Validation** (required fields, email format, URL format, password strength)
- **JSON export** (one-click download of the response)
- **Mobile-responsive** (works on phone, tablet, desktop)

### When Atlas Generates a Form

| Scenario | Form Generated | Action After Fill |
|---|---|---|
| New client onboarding | `client-onboarding.html` | Creates vault folder, profile, manifest, KPIs, strategy |
| API credentials missing | `api-credentials.html` | Writes `.env` with all secrets |
| WordPress not configured | `wordpress-config.html` | Tests connection, writes `.env` with WP config |
| Content brief needed | `content-brief.html` | Generates full content brief with RAG context |
| Competitor data missing | `competitor-intake.html` | Seeds competitor-intel agent with targets |
| New ad campaign | `ad-campaign-setup.html` | Configures ad accounts, budgets, audiences |

### Form Security

- **Credentials NEVER go to the vault.** API keys, passwords, tokens go to `.env` only.
- **Application passwords** (not login passwords) are used for WordPress.
- **All password fields are masked** (type="password") in the HTML form.
- **Form responses are local** — they never leave the user's machine unless explicitly shared.

## Daily Digest Generation

At the end of the loop, produce a daily digest with:
- What was completed today
- What's pending / blocked
- Any HITL gates awaiting approval
- Any anomalies flagged
- Token cost summary for the day

Write to `11-Ops/daily-ops-log.md` with frontmatter type `daily-ops-log`.

## Friday Self-Improvement Cycle

On Fridays, run an additional review:
1. Read all `11-Ops/agent-logs/` from the week.
2. Identify patterns: which agents succeeded, which failed, why.
3. Read `11-Ops/playbooks/qa-checklist.md` results.
4. Propose 1–3 playbook or agent-config improvements.
5. Present proposals to the human. Do not apply without approval.

## Cost Monitoring

- Track cumulative token cost per run in the agent log.
- Daily cap: $5. If exceeded, throttle non-critical agents.
- Monthly cap: $100. If exceeded, pause all non-essential agents and alert the founder.
- Log cost per step in `11-Ops/daily-ops-log.md`.

## Escalation Rules

### Auto-retry (no human needed)
- API timeout: retry once with exponential backoff
- Rate limit: queue + retry after 60s
- LLM response malformed: retry once with stricter prompt
- RAG retrieval returned 0 chunks: retry with broader query

### Escalate to human
- Any step fails twice after retry
- HITL gate triggered
- Daily cost cap exceeded
- Critical anomaly detected (site down, manual action, negative sentiment spike >2σ)
- Any agent produces output that fails QA checklist

## References

- `references/vault-context.md` — Path mappings for all 11 vault folders and key files, including client-centric paths (`01-Clients/[client]/`)
- `references/frontmatter-standards.md` — YAML frontmatter type registry and tag dictionary
- `references/hitl-gates.md` — The 10 non-negotiable human approval gates
- `references/anomaly-triage.md` — Anomaly decision matrix (ignore/monitor/investigate/escalate)
- `references/daily-ops-template.md` — Template for the daily ops log output
- `00-Agency-Core/_dashboards/brain-map.html` — Interactive force-directed graph of all vault entities (client-centered)
- `00-Agency-Core/_dashboards/dashboard.html` — Master HTML dashboard with charts, metrics, and brain map embed
- `infrastructure/scripts/generate_brain_map.py` — Brain map generator (run after each loop)
- `infrastructure/scripts/generate_dashboard.py` — Dashboard generator (run after each loop)
- `01-Clients/_template-client/client-profile.md` — Template for new client onboarding
- `01-Clients/_template-client/website-manifest.md` — Template for client's website + API properties
