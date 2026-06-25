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
│   └── bing.py                 # Bing Webmaster Tools
├── rag/
│   └── pipeline.py             # ChromaDB + LlamaIndex RAG pipeline
└── scripts/
    ├── ingest_vault.py         # Markdown → chunks → embeddings → ChromaDB
    ├── health_check.py         # Full integration connectivity test
    └── cost_tracker.py         # Per-call cost logging + budget enforcement
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

## Scheduled Jobs

Set up daily vault ingestion via cron:

```bash
# Linux/macOS — add to crontab
0 3 * * * cd /path/to/marketing && python infrastructure/scripts/ingest_vault.py

# Windows — use Task Scheduler or WSL cron
```
