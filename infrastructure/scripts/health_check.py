"""
AgenticMarketingPro — Integration Health Check
===============================================
Tests connectivity and auth for all configured APIs.

Usage:
    python scripts/health_check.py [--verbose] [--output path]

Output: JSONL to health-check log + console summary
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config
from api_client.base import APIClient


def setup_logging(verbose: bool = False):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def check_llm_apis() -> List[Dict[str, Any]]:
    """Check LLM / embedding API connectivity."""
    results = []
    
    # OpenAI (Primary)
    if Config.OPENAI_API_KEY:
        client = APIClient(
            base_url="https://api.openai.com",
            auth_header="Authorization",
            auth_value=f"Bearer {Config.OPENAI_API_KEY}",
            name="openai",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "openai", "status": "not_configured", "timestamp": datetime.utcnow().isoformat() + "Z"})

    # Minimax (Fallback)
    if Config.MINIMAX_API_KEY:
        try:
            from api_client.minimax import MinimaxClient
            client = MinimaxClient()
            results.append(client.health_check())
            client.close()
        except Exception as e:
            results.append({"name": "minimax", "status": "error", "error": str(e), "timestamp": datetime.utcnow().isoformat() + "Z"})
    else:
        results.append({"name": "minimax", "status": "not_configured", "timestamp": datetime.utcnow().isoformat() + "Z"})

    # Anthropic (Fallback)
    if Config.ANTHROPIC_API_KEY:
        client = APIClient(
            base_url="https://api.anthropic.com",
            auth_header="x-api-key",
            auth_value=Config.ANTHROPIC_API_KEY,
            name="anthropic",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "anthropic", "status": "not_configured", "timestamp": datetime.utcnow().isoformat() + "Z"})

    return results


def check_seo_apis() -> List[Dict[str, Any]]:
    """Check SEO data APIs."""
    results = []
    
    # Ahrefs
    if Config.AHREFS_API_KEY:
        client = APIClient(
            base_url="https://apiv3.ahrefs.com",
            auth_header="X-Api-Token",
            auth_value=Config.AHREFS_API_KEY,
            name="ahrefs",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "ahrefs", "status": "not_configured"})

    # Semrush
    if Config.SEMRUSH_API_KEY:
        client = APIClient(
            base_url="https://api.semrush.com",
            api_key_param="key",
            api_key_value=Config.SEMRUSH_API_KEY,
            name="semrush",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "semrush", "status": "not_configured"})

    # DataForSEO
    if Config.DATAFORSEO_LOGIN and Config.DATAFORSEO_PASSWORD:
        client = APIClient(
            base_url="https://api.dataforseo.com",
            auth_header="Authorization",
            auth_value=f"Basic {Config.DATAFORSEO_LOGIN}:{Config.DATAFORSEO_PASSWORD}",
            name="dataforseo",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "dataforseo", "status": "not_configured"})

    # SERPAPI
    if Config.SERPAPI_KEY:
        client = APIClient(
            base_url="https://serpapi.com",
            api_key_param="api_key",
            api_key_value=Config.SERPAPI_KEY,
            name="serpapi",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "serpapi", "status": "not_configured"})

    return results


def check_google_apis() -> List[Dict[str, Any]]:
    """Check Google APIs (GSC, GA4, Ads)."""
    results = []
    
    # GSC (uses OAuth, hard to health-check without property)
    if Config.GSC_PROPERTY:
        results.append({"name": "gsc", "status": "configured", "property": Config.GSC_PROPERTY})
    else:
        results.append({"name": "gsc", "status": "not_configured"})

    # GA4
    if Config.GA4_PROPERTY_ID:
        results.append({"name": "ga4", "status": "configured", "property": Config.GA4_PROPERTY_ID})
    else:
        results.append({"name": "ga4", "status": "not_configured"})

    # Bing
    if Config.BING_API_KEY:
        client = APIClient(
            base_url="https://ssl.bing.com/webmaster/api.svc/json",
            api_key_param="apikey",
            api_key_value=Config.BING_API_KEY,
            name="bing_wmt",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "bing_wmt", "status": "not_configured"})

    return results


def check_paid_ads() -> List[Dict[str, Any]]:
    """Check paid ads APIs."""
    results = []
    
    for name, config_key in [
        ("google_ads", Config.GOOGLE_ADS_DEVELOPER_TOKEN),
        ("meta_ads", Config.META_ACCESS_TOKEN),
        ("linkedin_ads", Config.LINKEDIN_ADS_TOKEN),
    ]:
        if config_key:
            results.append({"name": name, "status": "configured"})
        else:
            results.append({"name": name, "status": "not_configured"})
    
    return results


def check_social_crm() -> List[Dict[str, Any]]:
    """Check social and CRM APIs."""
    results = []
    
    for name, config_key in [
        ("hubspot", Config.HUBSPOT_API_KEY),
        ("hunter", Config.HUNTER_API_KEY),
        ("buffer", Config.BUFFER_ACCESS_TOKEN),
        ("slack", Config.SLACK_WEBHOOK_URL),
    ]:
        if config_key:
            results.append({"name": name, "status": "configured"})
        else:
            results.append({"name": name, "status": "not_configured"})
    
    return results


def check_monitoring() -> List[Dict[str, Any]]:
    """Check monitoring APIs."""
    results = []
    
    # Cloudflare
    if Config.CLOUDFLARE_API_TOKEN:
        client = APIClient(
            base_url="https://api.cloudflare.com",
            auth_header="Authorization",
            auth_value=f"Bearer {Config.CLOUDFLARE_API_TOKEN}",
            name="cloudflare",
        )
        results.append(client.health_check())
    else:
        results.append({"name": "cloudflare", "status": "not_configured"})

    # PageSpeed
    if Config.PAGESPEED_API_KEY:
        results.append({"name": "pagespeed", "status": "configured"})
    else:
        results.append({"name": "pagespeed", "status": "not_configured"})

    return results


def check_vector_db() -> List[Dict[str, Any]]:
    """Check ChromaDB status."""
    results = []
    try:
        import chromadb
        from rag.pipeline import VaultRAG
        
        rag = VaultRAG()
        stats = rag.stats()
        results.append({
            "name": "chroma_db",
            "status": "healthy",
            "total_chunks": stats.get("total_chunks", 0),
            "collection": stats.get("collection_name"),
        })
    except Exception as e:
        results.append({"name": "chroma_db", "status": "error", "error": str(e)})
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Integration health check")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--output", "-o", type=str, help="Output JSON file path")
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger("amp.health")

    logger.info("=" * 60)
    logger.info("AgenticMarketingPro — Integration Health Check")
    logger.info("=" * 60)

    all_results = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": {},
    }

    categories = {
        "llm_apis": check_llm_apis,
        "seo_apis": check_seo_apis,
        "google_apis": check_google_apis,
        "paid_ads": check_paid_ads,
        "social_crm": check_social_crm,
        "monitoring": check_monitoring,
        "vector_db": check_vector_db,
    }

    for category, check_fn in categories.items():
        logger.info(f"\n--- {category.replace('_', ' ').upper()} ---")
        results = check_fn()
        all_results["checks"][category] = results
        
        for r in results:
            status = r.get("status", "unknown")
            icon = "✅" if status in ("healthy", "configured", "ok") else "❌" if status in ("down", "error") else "⚠️"
            logger.info(f"  {icon} {r['name']}: {status}")
            if "latency_ms" in r:
                logger.info(f"     Latency: {r['latency_ms']}ms")
            if "error" in r:
                logger.info(f"     Error: {r['error']}")

    # Summary
    total = sum(len(v) for v in all_results["checks"].values())
    healthy = sum(
        1 for cat in all_results["checks"].values() 
        for r in cat if r.get("status") in ("healthy", "configured", "ok")
    )
    not_configured = sum(
        1 for cat in all_results["checks"].values() 
        for r in cat if r.get("status") == "not_configured"
    )
    errors = total - healthy - not_configured

    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"  Total checks:      {total}")
    logger.info(f"  Healthy/Configured: {healthy}")
    logger.info(f"  Not configured:    {not_configured}")
    logger.info(f"  Errors/Down:       {errors}")
    logger.info(f"  Config coverage:   {healthy}/{total - not_configured} ({healthy / max(total - not_configured, 1) * 100:.1f}%)")

    # Save to log
    Config.HEALTH_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(Config.HEALTH_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps(all_results) + "\n")
    logger.info(f"\nHealth log written to: {Config.HEALTH_LOG}")

    # Optional output file
    if args.output:
        out_path = Path(args.output)
        out_path.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
        logger.info(f"Report saved to: {out_path}")

    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
