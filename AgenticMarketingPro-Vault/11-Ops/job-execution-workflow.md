# Job Execution Workflow

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Vercel    │────▶│  Supabase   │◀────│  Edge Function  │
│   (UI)      │     │  (Database) │     │ (execute-jobs)  │
└─────────────┘     └──────┬──────┘     └─────────────────┘
                           │                    ▲
                           │                    │
                           │            ┌───────┴───────┐
                           │            │  Cron-Job.org │
                           │            │ (HTTP trigger)│
                           │            └───────────────┘
                           │
                    ┌──────┴──────┐
                    │   Jobs Table │
                    │  - pending   │
                    │  - running   │
                    │  - completed │
                    │  - failed    │
                    │  - blocked   │
                    └─────────────┘
```

## Flow

### 1. User Creates Job (Vercel UI)
```
User clicks "Run" on skill
        │
        ▼
┌─────────────────┐
│ Skill Run Modal │
│ - Select client │
│ - Prompt override│
│ - Additional context│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ POST /api/jobs  │
│ Body: {         │
│   type: "agent_run"│
│   skill_slug: "..."│
│   client_slug: "..."│
│   payload: {    │
│     prompt_override: "..."│
│     additional_context: "..."│
│   }             │
│ }               │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Job inserted    │
│ status: pending │
└─────────────────┘
```

### 2. Edge Function Polls & Executes (Supabase)
```
Cron-Job.org triggers every 5 minutes
        │
        ▼
┌─────────────────────────┐
│ GET /execute-jobs       │
│ (Supabase Edge Function)│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 1. Fetch pending jobs   │
│    LIMIT 5              │
│    ORDER BY created_at  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 2. For each job:        │
│    a. Mark as running   │
│    b. Build LLM prompt  │
│    c. Call LLM API      │
│    d. Store result      │
│    e. Mark completed    │
│    f. Enqueue QA check  │
└─────────────────────────┘
```

### 3. Realtime Updates (Vercel UI)
```
Supabase Realtime
        │
        ▼
┌─────────────────────────┐
│ Jobs page subscribes to │
│ postgres_changes on     │
│ jobs table              │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Auto-refresh job list   │
│ when status changes     │
└─────────────────────────┘
```

## API Endpoints

### Create Job
```
POST /api/jobs
Content-Type: application/json

{
  "type": "agent_run",
  "skill_slug": "content-strategist",
  "client_slug": "agenticmarketingpro",
  "payload": {
    "prompt_override": "Focus on n8n automation agency keywords...",
    "additional_context": "Target: healthcare industry, Budget: $5K"
  }
}
```

### List Jobs
```
GET /api/jobs
Response: { jobs: [...] }
```

### Get Job Result
```
GET /api/jobs/:id
Response: { job: { id, status, result, ... } }
```

## Environment Variables (Edge Function)

| Variable | Description |
|----------|-------------|
| `SUPABASE_URL` | Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key (bypasses RLS) |
| `LLM_API_KEY` | OpenAI/Kimi API key |
| `LLM_PROVIDER` | `openai` or `minimax` |
| `LLM_MODEL` | Model name (e.g., `kimi-latest`) |
| `LLM_BASE_URL` | API base URL |
| `SLACK_WEBHOOK_URL` | For alerts (optional) |

## Cron-Job.org Setup

### Create Job
```bash
curl -X POST https://api.cron-job.org/jobs \
  -H "Authorization: Bearer WJnmdRwO6iHDH7NIlyYadsQzniVxFctEDLKVZEtExoE=" \
  -H "Content-Type: application/json" \
  -d '{
    "job": {
      "url": "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs",
      "enabled": true,
      "saveResponses": true,
      "schedule": {
        "timezone": "UTC",
        "hours": [-1],
        "mdays": [-1],
        "minutes": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
        "months": [-1],
        "wdays": [-1]
      },
      "extendedData": {
        "headers": {
          "Authorization": "Bearer YOUR_SUPABASE_ANON_KEY"
        }
      }
    }
  }'
```

### Schedule
- **Frequency:** Every 5 minutes
- **Purpose:** Poll for pending jobs and execute them
- **Timeout:** 30 seconds (edge function timeout)

## Job Status Lifecycle

```
┌─────────┐    ┌─────────┐    ┌──────────┐    ┌───────────┐
│ pending │───▶│ running │───▶│completed │    │  failed   │
└─────────┘    └─────────┘    └──────────┘    └───────────┘
     │                              ▲                ▲
     │                              │                │
     └──────────────────────────────┘                │
     (QA blocked)                                    │
     ┌─────────┐                                     │
     │ blocked │─────────────────────────────────────┘
     └─────────┘
```

## QA Pipeline

After any content-producing job completes:
1. Auto-enqueue `qa_check` job
2. Run binary checks (legal, plagiarism) — block if fail
3. Run scored checks (grammar, tone, brand voice) — log and continue
4. If blocked, parent job status → `blocked`

## Cost Tracking

Per job:
- Tokens in/out
- Cost USD (calculated from token usage)
- Model used
- Provider

Budget enforcement:
- Check `CostTracker.enforce_budget()` before dispatching
- Daily cap: $5
- Monthly cap: $100

## Error Handling

| Error | Action |
|-------|--------|
| API timeout | Retry once with exponential backoff |
| Rate limit | Queue + retry after 60s |
| LLM malformed | Retry once with stricter prompt |
| RAG 0 chunks | Retry with broader query |
| Fail twice | Escalate to human (Slack alert) |
| Daily budget exceeded | Pause non-critical, alert |

## Monitoring

### Slack Alerts
- Escalations
- HITL-pending jobs
- Budget-cap hits
- Job failures

### Agent Logs
Every code path writes to `agent_logs`:
- Job start/completion/failure
- QA results
- Budget checks
- Retries

## Deployment

### Deploy Edge Function
```bash
# Login to Supabase
npx supabase login

# Link project
npx supabase link --project-ref pusttdxrtmgvhdzdyvbd

# Deploy function
npx supabase functions deploy execute-jobs

# Set secrets
npx supabase secrets set --env-file ./supabase/functions/execute-jobs/.env
```

### Verify Deployment
```bash
# Invoke function manually
curl -X POST https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

## Testing

### Test Suite
1. **Form engine output validity** — validate JSON schema
2. **Processors idempotency** — running client-onboarding twice shouldn't duplicate folders
3. **Cost tracker math** — verify token → cost calculations

### GitHub Actions
- Lint + test on PR
- Validate vault .md frontmatter against `frontmatter-standards.md`

---

*Last updated: 2026-07-08*
