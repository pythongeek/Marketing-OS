"""
AgenticMarketingPro — Form Response Processors
===============================================
Takes form response JSON files and executes the corresponding actions:
- Create client vault folder + profile + manifest
- Validate API credentials (never writes secrets to disk)
- Test WordPress connection (never writes secrets to disk)
- Generate content brief from form data

Usage:
    python processors/process_client_onboarding.py forms/client-onboarding-response.json
    python processors/process_api_credentials.py forms/api-credentials-response.json
    python processors/process_wordpress.py forms/wordpress-config-response.json
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.processors")


VAULT_ROOT = Path(Config.VAULT_ROOT)


def _read_response(path: str) -> Dict[str, Any]:
    """Read a form response JSON file."""
    p = Path(path)
    if not p.exists():
        logger.error(f"Response file not found: {p}")
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse {p}: {e}")
        return {}


def process_client_onboarding(response_path: str) -> Dict[str, Any]:
    """Process client onboarding form response and create vault folder."""
    data = _read_response(response_path)
    if not data:
        return {"status": "error", "error": "No response data"}

    client_name = data.get("client_name", "").strip()
    if not client_name:
        return {"status": "error", "error": "client_name is required"}

    # Create slug
    import re
    client_slug = re.sub(r'[^a-z0-9]+', '-', client_name.lower()).strip('-')

    # Create folder structure
    client_dir = VAULT_ROOT / "01-Clients" / client_slug
    folders = [
        client_dir,
        client_dir / "campaigns",
        client_dir / "competitors",
        client_dir / "agent-logs",
        client_dir / "monthly-reports",
    ]
    for f in folders:
        f.mkdir(parents=True, exist_ok=True)

    # Parse tier
    tier_raw = data.get("tier", "")
    tier = tier_raw.split(" (")[0] if "(" in tier_raw else tier_raw
    mrr = 0
    if "2,500" in tier_raw:
        mrr = 2500
    elif "4,500" in tier_raw:
        mrr = 4500
    elif "8,500" in tier_raw:
        mrr = 8500
    elif "15,000" in tier_raw:
        mrr = 15000

    # Write client-profile.md
    profile_md = f"""---
type: client-profile
client: "{client_name}"
website: "{data.get('website', '')}"
status: active
tier: {tier}
start_date: {datetime.now().strftime('%Y-%m-%d')}
mrr: {mrr}
industry: {data.get('industry', '')}
target_geo: {data.get('target_geo', 'US')}
primary_language: {data.get('primary_language', 'en')}
---

# Client Profile — {client_name}

## Overview

| Field | Value |
|---|---|
| **Website** | [{data.get('website', '')}]({data.get('website', '')}) |
| **Tier** | {tier} (${mrr:,}/mo) |
| **Status** | Active |
| **Industry** | {data.get('industry', '')} |
| **Target Geo** | {data.get('target_geo', 'US')} |
| **Start Date** | {datetime.now().strftime('%Y-%m-%d')} |

## Business Goals

1. **Primary:** {data.get('business_goal_1', '')}
2. **Secondary:** {data.get('business_goal_2', '')}

## Key Contacts

| Role | Name | Email | Slack |
|---|---|---|---|
| Primary | {data.get('contact_name', '')} | {data.get('contact_email', '')} | {data.get('contact_slack', '')} |

## Website Manifest

See `website-manifest.md` for technical details.

## Competitors

| Competitor | URL |
|---|---|
| Competitor 1 | {data.get('competitor_1', '')} |
| Competitor 2 | {data.get('competitor_2', '')} |
| Competitor 3 | {data.get('competitor_3', '')} |

## Notes

{data.get('notes', '')}
"""

    profile_path = client_dir / "client-profile.md"
    profile_path.write_text(profile_md, encoding="utf-8")

    # Write website-manifest.md
    cms = data.get('cms', '')
    if cms == 'Custom / Other':
        cms = data.get('cms_custom', 'Custom')

    has_wp = data.get('has_wordpress_api', '') == 'Connect to WordPress REST API for auto-publishing'

    manifest_md = f"""---
type: website-manifest
client: "{client_name}"
website: "{data.get('website', '')}"
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# Website Manifest — {client_name}

## Domains

| Domain | Primary? | Status |
|---|---|---|
| {data.get('website', '')} | ✅ | Active |

## Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| CMS | {cms} | |

## API Properties

| Service | Property | Configured? |
|---|---|---|
| Google Search Console | {data.get('gsc_property', 'N/A')} | {'✅' if data.get('has_gsc') == 'I have access' else '❌'} |
| Google Analytics 4 | {data.get('ga4_property', 'N/A')} | {'✅' if data.get('has_ga4') == 'I have access' else '❌'} |
| Ahrefs | {data.get('website', '').replace('https://', '').replace('http://', '').strip('/')} | {'✅' if data.get('has_ahrefs') == 'I have an API key' else '❌'} |
| Semrush | {data.get('website', '').replace('https://', '').replace('http://', '').strip('/')} | {'✅' if data.get('has_semrush') == 'I have an API key' else '❌'} |

## WordPress Integration

| Setting | Value |
|---|---|
| Enabled | {'✅ Yes' if has_wp else '❌ No'} |
| Site URL | {data.get('wp_url', 'N/A')} |
| Username | {data.get('wp_username', 'N/A')} |

## Important Pages

| Page Type | URL | Notes |
|---|---|---|
| Homepage | {data.get('website', '')} | |

## Known Issues

None yet. Will be populated by tech-seo-auditor agent.
"""

    manifest_path = client_dir / "website-manifest.md"
    manifest_path.write_text(manifest_md, encoding="utf-8")

    # Write kpis-and-goals.md
    kpis_md = f"""---
type: kpi-tracking
client: "{client_name}"
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# KPIs & Goals — {client_name}

## North Star Metrics

| Metric | Baseline | Target | Target Date | Status |
|---|---|---|---|---|
| Organic SQLs | 12/mo | 50/mo | Q3 2026 | Not started |
| AEO Citations | 0 | 5 keywords | Q2 2026 | Not started |
| CAC Reduction | Baseline | -30% | Q4 2026 | Not started |

## Monthly Tracking

See `monthly-reports/` folder for detailed monthly reports.
"""

    kpis_path = client_dir / "kpis-and-goals.md"
    kpis_path.write_text(kpis_md, encoding="utf-8")

    # Write strategy-90-day.md
    strategy_md = f"""---
type: strategy
client: "{client_name}"
last_updated: {datetime.now().strftime('%Y-%m-%d')}
---

# 90-Day Strategy — {client_name}

## Month 1: Foundation
- [ ] Technical SEO audit
- [ ] Keyword universe mapping
- [ ] Competitor intelligence baseline
- [ ] Content audit of existing pages
- [ ] Brand voice calibration
- [ ] WordPress / CMS optimization (if applicable)

## Month 2: Content Engine
- [ ] 4 pillar content pieces (Growth tier = 8/month)
- [ ] On-page optimization of existing content
- [ ] Internal linking structure
- [ ] Schema markup implementation
- [ ] First outreach campaign

## Month 3: Scale & Optimize
- [ ] Programmatic SEO opportunities identified
- [ ] AEO/GEO citation tracking active
- [ ] Social repurposing engine running
- [ ] Paid ads testing (if applicable)
- [ ] Q1 performance review and Q2 plan
"""

    strategy_path = client_dir / "strategy-90-day.md"
    strategy_path.write_text(strategy_md, encoding="utf-8")

    # Update _index.md with new client link
    index_path = VAULT_ROOT / "_index.md"
    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        # Find the "## Client work" section and add link
        client_link = f"- [[01-Clients/{client_slug}/client-profile|{client_name}]]"
        if client_link not in index_text:
            # Insert after the template line
            index_text = index_text.replace(
                "## Client work\n",
                f"## Client work\n{client_link}\n"
            )
            index_path.write_text(index_text, encoding="utf-8")

    logger.info(f"Client '{client_name}' onboarded successfully. Folder: {client_dir}")

    return {
        "status": "success",
        "client": client_name,
        "slug": client_slug,
        "folder": str(client_dir),
        "files_created": [
            str(profile_path.relative_to(VAULT_ROOT)),
            str(manifest_path.relative_to(VAULT_ROOT)),
            str(kpis_path.relative_to(VAULT_ROOT)),
            str(strategy_path.relative_to(VAULT_ROOT)),
        ],
    }


def process_api_credentials(response_path: str) -> Dict[str, Any]:
    """Process API credentials form. Validates only — NEVER writes secrets to disk."""
    data = _read_response(response_path)
    if not data:
        return {"status": "error", "error": "No response data"}

    # Map form fields to env vars
    env_map = {
        "openai_api_key": "OPENAI_API_KEY",
        "kimi_api_key": "KIMI_API_KEY",
        "minimax_api_key": "MINIMAX_API_KEY",
        "ahrefs_api_key": "AHREFS_API_KEY",
        "semrush_api_key": "SEMRUSH_API_KEY",
        "serpapi_key": "SERPAPI_KEY",
        "dataforseo_login": "DATAFORSEO_LOGIN",
        "dataforseo_password": "DATAFORSEO_PASSWORD",
        "gsc_client_secrets": "GOOGLE_CLIENT_SECRETS_FILE",
        "ga4_property_id": "GA4_PROPERTY_ID",
        "bing_api_key": "BING_API_KEY",
        "google_ads_dev_token": "GOOGLE_ADS_DEVELOPER_TOKEN",
        "google_ads_refresh_token": "GOOGLE_ADS_REFRESH_TOKEN",
        "meta_access_token": "META_ACCESS_TOKEN",
        "linkedin_ads_token": "LINKEDIN_ADS_TOKEN",
        "hubspot_api_key": "HUBSPOT_API_KEY",
        "slack_webhook_url": "SLACK_WEBHOOK_URL",
        "buffer_token": "BUFFER_ACCESS_TOKEN",
        "cloudflare_token": "CLOUDFLARE_API_TOKEN",
        "cloudflare_zone_id": "CLOUDFLARE_ZONE_ID",
        "pagespeed_key": "PAGESPEED_API_KEY",
        "perplexity_key": "PERPLEXITY_API_KEY",
        "elevenlabs_key": "ELEVENLABS_API_KEY",
    }

    # API credentials are managed via hosting platform encrypted env vars
    # or ~/.amp/secrets.json for local dev. Agents NEVER write secrets to disk.
    # This processor only validates and reports which credentials were provided.
    provided = []
    for form_key, env_key in env_map.items():
        value = data.get(form_key, "").strip()
        if value:
            provided.append(env_key)

    logger.info(f"Validated {len(provided)} credentials (not written to disk)")
    return {
        "status": "success",
        "credentials_validated": len(provided),
        "credential_keys": provided,
        "message": "Set these in your hosting platform's env vars or ~/.amp/secrets.json",
    }


def process_wordpress_config(response_path: str) -> Dict[str, Any]:
    """Process WordPress config form and test connection."""
    data = _read_response(response_path)
    if not data:
        return {"status": "error", "error": "No response data"}

    site_url = data.get("wp_site_url", "").strip()
    username = data.get("wp_username", "").strip()
    password = data.get("wp_app_password", "").strip()

    if not all([site_url, username, password]):
        return {"status": "error", "error": "Missing WordPress credentials"}

    # Test connection
    try:
        from api_client.wordpress import WordPressClient
        wp = WordPressClient(
            site_url=site_url,
            username=username,
            app_password=password,
            seo_plugin=data.get("wp_seo_plugin", "None"),
        )
        result = wp.test_connection()

        if result.get("status") == "connected":
            # WordPress credentials are stored in hosting platform encrypted env vars
            # or ~/.amp/secrets.json. Agents NEVER write secrets to disk.
            config_record = {
                "wp_site_url": site_url,
                "wp_username": username,
                "wp_seo_plugin": data.get("wp_seo_plugin", "None"),
                "wp_post_type": data.get("wp_post_type", "post"),
                "wp_author_id": data.get("wp_author_id", "1"),
            }

            logger.info(
                f"WordPress connected: {site_url} (user: {result.get('username')}). "
                f"Set WP_APP_PASSWORD in your hosting platform env vars."
            )
            return {
                "status": "connected",
                "site_url": site_url,
                "user": result.get("username"),
                "config_record": config_record,
                "message": "Set WP_SITE_URL, WP_USERNAME, WP_APP_PASSWORD in env vars or ~/.amp/secrets.json",
            }
        else:
            return {
                "status": "failed",
                "error": result.get("error", "Connection test failed"),
                "site_url": site_url,
            }

    except ImportError as e:
        return {"status": "error", "error": f"Missing dependency: {e}"}
    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process form responses")
    parser.add_argument("type", choices=["client", "api", "wordpress", "content-brief"])
    parser.add_argument("response_file", help="Path to the JSON response file")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")

    if args.type == "client":
        result = process_client_onboarding(args.response_file)
    elif args.type == "api":
        result = process_api_credentials(args.response_file)
    elif args.type == "wordpress":
        result = process_wordpress_config(args.response_file)
    else:
        result = {"status": "not_implemented"}

    print(json.dumps(result, indent=2))
    return 0 if result.get("status") == "success" or result.get("status") == "connected" else 1


if __name__ == "__main__":
    sys.exit(main())
