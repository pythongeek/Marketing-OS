"""
AgenticMarketingPro — Central Configuration
============================================
Reads environment variables and provides typed config for all scripts.
Credentials are NEVER hardcoded. Use .env file, system env vars, or
~/.amp/secrets.json for local dev.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env from vault integrations folder (or local .env)
_ENV_PATHS = [
    Path(__file__).parent.parent / ".env",
    Path(__file__).parent / ".env",
    Path(__file__).parent.parent / "AgenticMarketingPro-Vault" / "11-Ops" / "integrations" / ".env",
]
for _p in _ENV_PATHS:
    if _p.exists():
        load_dotenv(dotenv_path=_p)
        break

# Load external secrets.json for local dev (outside repo, never committed)
_SECRETS_PATH = Path.home() / ".amp" / "secrets.json"
if _SECRETS_PATH.exists():
    try:
        import json as _json
        _secrets = _json.loads(_SECRETS_PATH.read_text(encoding="utf-8"))
        for _k, _v in _secrets.items():
            if _k not in os.environ:
                os.environ[_k] = str(_v)
    except Exception:
        pass  # Graceful degradation if secrets.json is malformed


class Config:
    """Central configuration. All keys are optional — scripts degrade gracefully."""

    # ── LLM / Embeddings ────────────────────────────────────────────
    # Primary LLM: Minimax M3
    MINIMAX_API_KEY: Optional[str] = os.getenv("MINIMAX_API_KEY")
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "MiniMax-M3")
    DEFAULT_LLM_PROVIDER: str = os.getenv("DEFAULT_LLM_PROVIDER", "minimax")
    
    # Fallback LLMs (optional)
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    HERMES_AGENT_API_KEY: Optional[str] = os.getenv("HERMES_AGENT_API_KEY")
    DEFAULT_HERMES_AGENT_MODEL: str = os.getenv("DEFAULT_HERMES_AGENT_MODEL", "MiniMax-M3")

    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    EMBEDDING_DIMENSION: int = int(os.getenv("EMBEDDING_DIMENSION", "1536"))

    # ── Vector DB ─────────────────────────────────────────────────────
    CHROMA_PERSIST_DIR: Path = Path(os.getenv("CHROMA_PERSIST_DIR", str(Path(__file__).parent.parent / "chroma_db")))
    CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "amp_vault")
    # Pinecone (optional — for scale)
    PINECONE_API_KEY: Optional[str] = os.getenv("PINECONE_API_KEY")
    PINECONE_INDEX_NAME: Optional[str] = os.getenv("PINECONE_INDEX_NAME")

    # ── SEO Data APIs ─────────────────────────────────────────────────
    AHREFS_API_KEY: Optional[str] = os.getenv("AHREFS_API_KEY")
    SEMRUSH_API_KEY: Optional[str] = os.getenv("SEMRUSH_API_KEY")
    DATAFORSEO_LOGIN: Optional[str] = os.getenv("DATAFORSEO_LOGIN")
    DATAFORSEO_PASSWORD: Optional[str] = os.getenv("DATAFORSEO_PASSWORD")
    SERPAPI_KEY: Optional[str] = os.getenv("SERPAPI_KEY")

    # ── Google APIs ───────────────────────────────────────────────────
    GOOGLE_CLIENT_SECRETS_FILE: Optional[str] = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
    GOOGLE_APPLICATION_CREDENTIALS: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    # GSC service account JSON — can be a file path OR the JSON string itself
    # (file path takes precedence; useful for secrets injected via env vars)
    GSC_SERVICE_ACCOUNT_FILE: Optional[str] = os.getenv("GSC_SERVICE_ACCOUNT_FILE")
    GSC_SERVICE_ACCOUNT_JSON: Optional[str] = os.getenv("GSC_SERVICE_ACCOUNT_JSON")
    GA4_PROPERTY_ID: Optional[str] = os.getenv("GA4_PROPERTY_ID")
    GSC_PROPERTY: Optional[str] = os.getenv("GSC_PROPERTY")
    BING_API_KEY: Optional[str] = os.getenv("BING_API_KEY")
    # OAuth 2.0 (replaces deprecated API key)
    _raw_bing_client_id = os.getenv("BING_CLIENT_ID")
    if _raw_bing_client_id:
        _raw_bing_client_id = _raw_bing_client_id.strip()
    BING_CLIENT_ID: Optional[str] = (
        f"{_raw_bing_client_id[:8]}-{_raw_bing_client_id[8:12]}-{_raw_bing_client_id[12:16]}-{_raw_bing_client_id[16:20]}-{_raw_bing_client_id[20:]}"
        if _raw_bing_client_id and len(_raw_bing_client_id) == 32 and "-" not in _raw_bing_client_id
        else _raw_bing_client_id
    )
    BING_CLIENT_SECRET: Optional[str] = os.getenv("BING_CLIENT_SECRET").strip() if os.getenv("BING_CLIENT_SECRET") else None
    BING_TENANT: str = os.getenv("BING_TENANT", "common").strip()
    BING_REDIRECT_URI: Optional[str] = os.getenv("BING_REDIRECT_URI").strip() if os.getenv("BING_REDIRECT_URI") else None

    # ── WordPress (CMS) ───────────────────────────────────────────────
    WORDPRESS_SITE_URL: Optional[str] = os.getenv("WORDPRESS_SITE_URL")
    WORDPRESS_USERNAME: Optional[str] = os.getenv("WORDPRESS_USERNAME")
    WORDPRESS_APP_PASSWORD: Optional[str] = os.getenv("WORDPRESS_APP_PASSWORD")
    WORDPRESS_SEO_PLUGIN: str = os.getenv("WORDPRESS_SEO_PLUGIN", "None")

    # ── Paid Ads APIs ─────────────────────────────────────────────────
    GOOGLE_ADS_DEVELOPER_TOKEN: Optional[str] = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN")
    GOOGLE_ADS_CLIENT_ID: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_ID")
    GOOGLE_ADS_CLIENT_SECRET: Optional[str] = os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    GOOGLE_ADS_REFRESH_TOKEN: Optional[str] = os.getenv("GOOGLE_ADS_REFRESH_TOKEN")
    GOOGLE_ADS_LOGIN_CUSTOMER_ID: Optional[str] = os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID")
    META_ACCESS_TOKEN: Optional[str] = os.getenv("META_ACCESS_TOKEN")
    LINKEDIN_ADS_TOKEN: Optional[str] = os.getenv("LINKEDIN_ADS_TOKEN")

    # ── Social / Outreach / CRM ───────────────────────────────────────
    BUFFER_ACCESS_TOKEN: Optional[str] = os.getenv("BUFFER_ACCESS_TOKEN")
    AYRSHARE_API_KEY: Optional[str] = os.getenv("AYRSHARE_API_KEY")
    HUBSPOT_API_KEY: Optional[str] = os.getenv("HUBSPOT_API_KEY")
    HUNTER_API_KEY: Optional[str] = os.getenv("HUNTER_API_KEY")
    INSTANTLY_API_KEY: Optional[str] = os.getenv("INSTANTLY_API_KEY")
    KLAVIYO_API_KEY: Optional[str] = os.getenv("KLAVIYO_API_KEY")
    NOTION_TOKEN: Optional[str] = os.getenv("NOTION_TOKEN")
    SLACK_WEBHOOK_URL: Optional[str] = os.getenv("SLACK_WEBHOOK_URL")

    # ── Content / AI Tools ────────────────────────────────────────────
    SURFER_API_KEY: Optional[str] = os.getenv("SURFER_API_KEY")
    CLEARSCOPE_API_KEY: Optional[str] = os.getenv("CLEARSCOPE_API_KEY")
    PERPLEXITY_API_KEY: Optional[str] = os.getenv("PERPLEXITY_API_KEY")
    ELEVENLABS_API_KEY: Optional[str] = os.getenv("ELEVENLABS_API_KEY")
    HEYGEN_API_KEY: Optional[str] = os.getenv("HEYGEN_API_KEY")
    RUNWAY_API_KEY: Optional[str] = os.getenv("RUNWAY_API_KEY")
    MIDJOURNEY_API_KEY: Optional[str] = os.getenv("MIDJOURNEY_API_KEY")

    # ── Monitoring ──────────────────────────────────────────────────────
    CLOUDFLARE_API_TOKEN: Optional[str] = os.getenv("CLOUDFLARE_API_TOKEN")
    CLOUDFLARE_ZONE_ID: Optional[str] = os.getenv("CLOUDFLARE_ZONE_ID")
    UPTIME_ROBOT_API_KEY: Optional[str] = os.getenv("UPTIME_ROBOT_API_KEY")
    PAGESPEED_API_KEY: Optional[str] = os.getenv("PAGESPEED_API_KEY")

    # ── GEO / AI Citation Tracking ────────────────────────────────────
    # ── Supabase ─────────────────────────────────────────────────────
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    SUPACKAGE_SERVICE_ROLE_KEY: Optional[str] = os.getenv("SUPACKAGE_SERVICE_ROLE_KEY")

    # ── Supabase ─────────────────────────────────────────────────────
    OTTERLY_API_KEY: Optional[str] = os.getenv("OTTERLY_API_KEY")
    BRANDWATCH_API_KEY: Optional[str] = os.getenv("BRANDWATCH_API_KEY")

    # ── Paths ───────────────────────────────────────────────────────────
    VAULT_ROOT: Path = Path(os.getenv("VAULT_ROOT", str(Path(__file__).parent.parent / "AgenticMarketingPro-Vault")))
    LOG_DIR: Path = Path(os.getenv("LOG_DIR", str(Path(__file__).parent.parent / "AgenticMarketingPro-Vault" / "11-Ops" / "agent-logs")))
    COST_LOG: Path = Path(os.getenv("COST_LOG", str(Path(__file__).parent.parent / "AgenticMarketingPro-Vault" / "11-Ops" / "agent-logs" / "cost-tracker.jsonl")))
    HEALTH_LOG: Path = Path(os.getenv("HEALTH_LOG", str(Path(__file__).parent.parent / "AgenticMarketingPro-Vault" / "11-Ops" / "agent-logs" / "health-check.jsonl")))

    # ── Rate Limits ─────────────────────────────────────────────────────
    DEFAULT_RATE_LIMIT_RPS: float = float(os.getenv("DEFAULT_RATE_LIMIT_RPS", "1.0"))
    DEFAULT_MAX_RETRIES: int = int(os.getenv("DEFAULT_MAX_RETRIES", "3"))
    DEFAULT_BACKOFF_BASE: float = float(os.getenv("DEFAULT_BACKOFF_BASE", "2.0"))

    # ── Cost Budgets ────────────────────────────────────────────────────
    LLM_DAILY_BUDGET_USD: float = float(os.getenv("LLM_DAILY_BUDGET_USD", "5.0"))
    LLM_MONTHLY_BUDGET_USD: float = float(os.getenv("LLM_MONTHLY_BUDGET_USD", "100.0"))

    @classmethod
    def check_deps(cls) -> dict:
        """Return which optional dependencies are available."""
        return {
            "minimax": cls.MINIMAX_API_KEY is not None,
            "openai": cls.OPENAI_API_KEY is not None,
            "anthropic": cls.ANTHROPIC_API_KEY is not None,
            "hermes_agent": cls.HERMES_AGENT_API_KEY is not None,
            "chroma": True,  # local, always available if installed
            "pinecone": cls.PINECONE_API_KEY is not None and cls.PINECONE_INDEX_NAME is not None,
            "ahrefs": cls.AHREFS_API_KEY is not None,
            "semrush": cls.SEMRUSH_API_KEY is not None,
            "dataforseo": cls.DATAFORSEO_LOGIN is not None and cls.DATAFORSEO_PASSWORD is not None,
            "serpapi": cls.SERPAPI_KEY is not None,
            "ga4": cls.GA4_PROPERTY_ID is not None,
            "gsc": cls.GSC_PROPERTY is not None and (
                cls.GSC_SERVICE_ACCOUNT_FILE is not None
                or cls.GSC_SERVICE_ACCOUNT_JSON is not None
                or cls.GOOGLE_APPLICATION_CREDENTIALS is not None
            ),
            "bing": cls.BING_API_KEY is not None,
            "google_ads": cls.GOOGLE_ADS_DEVELOPER_TOKEN is not None,
            "meta_ads": cls.META_ACCESS_TOKEN is not None,
            "linkedin_ads": cls.LINKEDIN_ADS_TOKEN is not None,
            "hubspot": cls.HUBSPOT_API_KEY is not None,
            "hunter": cls.HUNTER_API_KEY is not None,
            "buffer": cls.BUFFER_ACCESS_TOKEN is not None,
            "slack": cls.SLACK_WEBHOOK_URL is not None,
            "cloudflare": cls.CLOUDFLARE_API_TOKEN is not None,
            "pagespeed": cls.PAGESPEED_API_KEY is not None,
            "supabase": cls.SUPABASE_URL is not None and cls.SUPABASE_SERVICE_ROLE_KEY is not None,
        }


if __name__ == "__main__":
    import json
    print(json.dumps(Config.check_deps(), indent=2))
