# AgenticMarketingPro Infrastructure

Python infrastructure layer that wires the 30 agent skills to actual APIs, Chroma DB, and the RAG pipeline.

## Quick Start

```bash
# 1. Install dependencies
python setup.py --install

# 2. Create your .env file
cp .env.example .env
# Edit .env with your actual API keys

# 3. Run health check
python infrastructure/scripts/health_check.py --verbose

# 4. Ingest vault into ChromaDB
python infrastructure/scripts/ingest_vault.py --force

# 5. Test the RAG pipeline
python -c "from infrastructure.rag.pipeline import VaultRAG; rag = VaultRAG(); print(rag.stats())"
```

## Structure

```
infrastructure/
├── config.py                   # Central config from env vars (50+ integrations)
├── requirements.txt            # Python dependencies
├── api_client/
│   ├── base.py                 # Generic HTTP client (retry, rate limit, OAuth2)
│   ├── gsc.py                  # Google Search Console
│   ├── ga4.py                  # Google Analytics 4
│   ├── ahrefs.py               # Ahrefs API v3
│   ├── semrush.py              # Semrush API v3
│   ├── bing.py                 # Bing Webmaster Tools
│   └── wordpress.py            # WordPress REST API (posts, media, SEO meta)
├── rag/
│   └── pipeline.py             # ChromaDB + LlamaIndex RAG pipeline
├── ui/
│   ├── form_engine.py          # Schema-driven HTML form generator
│   └── processors.py           # Form response → vault action processors
└── scripts/
    ├── ingest_vault.py         # Markdown → chunks → embeddings → ChromaDB
    ├── health_check.py         # Full integration connectivity test
    ├── cost_tracker.py         # Per-call cost logging + budget enforcement
    ├── generate_brain_map.py   # D3.js force-directed graph of vault entities
    └── generate_dashboard.py   # HTML dashboard with PNG charts + brain map
```

## Environment Variables

All configuration is via environment variables (see `.env.example`). Critical ones:

| Variable | Required For | Description |
|---|---|---|
| `OPENAI_API_KEY` | Embeddings, LLM fallback | OpenAI API key for embeddings |
| `VAULT_ROOT` | RAG ingestion | Path to your Obsidian vault |
| `CHROMA_PERSIST_DIR` | RAG | Where ChromaDB stores vectors |

Optional: `AHREFS_API_KEY`, `SEMRUSH_API_KEY`, `GSC_PROPERTY`, `GA4_PROPERTY_ID`, `BING_API_KEY`, etc.

## API Clients

Each client follows the same pattern:

```python
from infrastructure.api_client.gsc import GSCClient
from infrastructure.api_client.ahrefs import AhrefsClient

# GSC: pull CTR opportunities
gsc = GSCClient("https://example.com/")
opportunities = gsc.get_ctr_opportunities(days=7)

# Ahrefs: weekly report
ahrefs = AhrefsClient()
report = ahrefs.weekly_report("example.com")

# WordPress: publish content from vault
from infrastructure.api_client.wordpress import WordPressClient
wp = WordPressClient("https://example.com", "username", "app_password")
wp.test_connection()
post = wp.create_post(title="My Article", content="<p>Hello world</p>", status="draft")
```

All clients return structured dicts ready for vault write-back.

## RAG Pipeline

```python
from infrastructure.rag.pipeline import VaultRAG

rag = VaultRAG()
rag.ingest_vault(force=True)  # One-time full ingestion

# Query by semantic similarity
results = rag.query(
    "How do we handle brand voice for technical audiences?",
    top_k=5,
    source_type="persona",  # Optional: filter by source type
)

# Query by source type
personas = rag.query_by_source("persona", top_k=10)
```

## Health Check

```bash
python infrastructure/scripts/health_check.py --verbose --output health-report.json
```

Checks 7 categories across 20+ integrations and produces a JSON report.

## Cost Tracking

```python
from infrastructure.scripts.cost_tracker import CostTracker

tracker = CostTracker()
tracker.log_call("content-strategist", "openai", "gpt-4o", tokens_in=2000, tokens_out=800)
status = tracker.check_budget()  # Returns daily/monthly status + throttle/pause flags
```

Budgets are enforced via `LLM_DAILY_BUDGET_USD` and `LLM_MONTHLY_BUDGET_USD` env vars.

## Visual Tools (`scripts/generate_brain_map.py`)
Interactive D3.js force-directed graph showing all vault entities:
- **Clients** (blue) as central nodes
- **Websites** (green) owned by clients
- **Keywords** (yellow) targeted by clients
- **Competitors** (red) mapped to clients
- **Agents** (purple) connected to their outputs
- **Content** (orange) linked to keywords and clients

```bash
python infrastructure/scripts/generate_brain_map.py --client acme
# Generates: 00-Agency-Core/_dashboards/brain-map.html
```

### Dashboard (`scripts/generate_dashboard.py`)
HTML dashboard with PNG charts:
- Daily agent cost utilization (vs. $5/day cap)
- API integration health check frequency
- Key metrics cards (vault nodes, active agents, clients, content pieces)
- Embedded brain map iframe

```bash
python infrastructure/scripts/generate_dashboard.py --client acme
# Generates: 00-Agency-Core/_dashboards/dashboard.html + cost-chart.png + agent-performance.png
```

Auto-generated after each daily ops loop (Step 10).

## Interactive Form Engine (`ui/form_engine.py`)

Every skill can generate interactive HTML forms to collect data from the user before acting. Forms are dark-themed, mobile-responsive, and support conditional fields, validation, and auto-save.

### Generate Forms

```bash
# All pre-built forms
python infrastructure/ui/form_engine.py --all

# Individual forms
python infrastructure/ui/form_engine.py --client-onboarding    # Onboard a new client
python infrastructure/ui/form_engine.py --api-credentials     # Collect API keys
python infrastructure/ui/form_engine.py --wordpress            # WordPress integration
python infrastructure/ui/form_engine.py --content-brief      # Generate content brief
```

### Form Features

- **Conditional fields:** Show WordPress fields only if "Enable WordPress" is checked
- **Auto-save to localStorage:** Never lose progress if browser closes
- **Validation:** Required fields, email format, URL format, password masking
- **JSON export:** One-click download of the response for the agent
- **Dark theme:** Matches the dashboard aesthetic

### Process Form Responses

```bash
# Create client vault folder from onboarding response
python infrastructure/ui/processors.py client forms/client-onboarding-response.json

# Write API credentials to .env
python infrastructure/ui/processors.py api forms/api-credentials-response.json

# Test WordPress connection and save config
python infrastructure/ui/processors.py wordpress forms/wordpress-config-response.json
```

### Custom Forms

Build your own form programmatically:

```python
from infrastructure.ui.form_engine import FormEngine, FormField, FormDefinition

engine = FormEngine()
form = FormDefinition(
    title="My Custom Form",
    fields=[
        FormField("name", "text", required=True, label="Name"),
        FormField("email", "email", required=True, label="Email"),
        FormField("type", "select", label="Type", options=["A", "B"]),
        FormField("detail", "text", label="Detail", depends_on="type", depends_value="A"),
    ],
)
path = engine.create_form(form, output_path="forms/my-form.html")
```

## Scheduled Jobs

Set up daily vault ingestion via cron:

```bash
# Linux/macOS — add to crontab
0 3 * * * cd /path/to/marketing && python infrastructure/scripts/ingest_vault.py

# Windows — use Task Scheduler or WSL cron
```
