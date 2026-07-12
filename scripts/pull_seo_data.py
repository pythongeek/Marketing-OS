"""
AgenticMarketingPro — SEO Data Pull Script
==========================================
Pulls search performance data from Bing WMT and (when configured) GSC.
Generates a formatted report that can be pasted into the master
SEO Search Ranking Report (docs/seo-search-ranking-report.md).

Usage:
    python scripts/pull_seo_data.py              # last 30 days
    python scripts/pull_seo_data.py --days 90    # last 90 days
    python scripts/pull_seo_data.py --site https://agenticmarketingpro.com

Requires:
- Bing OAuth tokens in bing_tokens Supabase table (auto-refreshed)
- GSC service account JSON in .env (optional)
- GA4 service account JSON in .env (optional)
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# Add infrastructure to path
sys.path.insert(0, str(Path(__file__).parent.parent / "infrastructure"))

from config import Config
from api_client.bing import BingWMTClient


def pull_bing_data(site_url: str, days: int) -> dict:
    """Pull Bing WMT data for the specified period."""
    print(f"\n[Bing] Pulling data for {site_url} (last {days} days)...")

    client = BingWMTClient()

    if not client.access_token:
        print("  [WARN] OAuth token not loaded — using API key fallback")
        print("         Visit /credentials and click 'Connect Bing WMT (OAuth)' to enable")

    result = {
        "site_details": {},
        "search_keywords": [],
        "traffic_stats": {},
        "crawl_stats": {},
        "errors": [],
    }

    try:
        result["site_details"] = client.site_details(site_url)
        print(f"  [OK] Site details retrieved")
    except Exception as e:
        result["errors"].append(f"site_details: {e}")
        print(f"  [ERR] site_details: {e}")

    try:
        result["search_keywords"] = client.search_keywords(site_url, days=days, limit=50)
        print(f"  [OK] {len(result['search_keywords'])} search keywords retrieved")
    except Exception as e:
        result["errors"].append(f"search_keywords: {e}")
        print(f"  [ERR] search_keywords: {e}")

    try:
        result["traffic_stats"] = client.traffic_stats(site_url, days=days)
        print(f"  [OK] Traffic stats retrieved")
    except Exception as e:
        result["errors"].append(f"traffic_stats: {e}")
        print(f"  [ERR] traffic_stats: {e}")

    try:
        result["crawl_stats"] = client.crawl_stats(site_url, days=days)
        print(f"  [OK] Crawl stats retrieved")
    except Exception as e:
        result["errors"].append(f"crawl_stats: {e}")
        print(f"  [ERR] crawl_stats: {e}")

    return result


def format_report(data: dict, days: int) -> str:
    """Format the data as a markdown report section."""
    lines = []
    lines.append(f"\n## Live Data Snapshot (last {days} days)")
    lines.append(f"\n*Pulled: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

    # Site details
    sd = data.get("site_details", {})
    if sd and "ErrorCode" not in sd:
        lines.append("### Site Details")
        lines.append(f"- **Domain:** {sd.get('RootDomain', 'N/A')}")
        lines.append(f"- **Subdomain:** {sd.get('SubDomain', 'N/A')}")
        lines.append(f"- **Verification:** {sd.get('IsVerified', 'N/A')}")
        lines.append(f"- **Crawl Allowed:** {sd.get('IsCrawlingAllowed', 'N/A')}")
        lines.append("")

    # Traffic stats
    ts = data.get("traffic_stats", {})
    if ts and "ErrorCode" not in ts:
        lines.append("### Traffic Stats Summary")
        # Bing returns aggregate data points
        total_clicks = 0
        total_impressions = 0
        if isinstance(ts, list):
            for day in ts:
                total_clicks += day.get("Clicks", 0)
                total_impressions += day.get("Impressions", 0)
        elif isinstance(ts, dict):
            total_clicks = ts.get("TotalClicks", 0)
            total_impressions = ts.get("TotalImpressions", 0)

        lines.append(f"- **Total Clicks:** {total_clicks:,}")
        lines.append(f"- **Total Impressions:** {total_impressions:,}")
        if total_impressions > 0:
            ctr = (total_clicks / total_impressions) * 100
            lines.append(f"- **Average CTR:** {ctr:.2f}%")
        lines.append("")

    # Top keywords
    kws = data.get("search_keywords", [])
    if kws:
        lines.append(f"### Top {min(20, len(kws))} Search Keywords")
        lines.append("")
        lines.append("| Keyword | Clicks | Impressions | Avg Position |")
        lines.append("|---------|-------:|------------:|-------------:|")
        for kw in kws[:20]:
            keyword = kw.get("Query", kw.get("Keyword", "(unknown)"))
            clicks = kw.get("Clicks", 0)
            impressions = kw.get("Impressions", 0)
            pos = kw.get("AvgClickPosition", kw.get("AvgImpressionPosition", "—"))
            lines.append(f"| {keyword} | {clicks} | {impressions} | {pos} |")
        lines.append("")

    # Crawl stats
    cs = data.get("crawl_stats", {})
    if cs and "ErrorCode" not in cs:
        lines.append("### Crawl Stats")
        lines.append(f"- **Total Pages Crawled:** {cs.get('TotalPagesCrawled', 'N/A'):,}")
        lines.append(f"- **Crawl Errors:** {cs.get('TotalErrors', cs.get('CrawlErrors', 'N/A'))}")
        lines.append(f"- **Avg Response Time:** {cs.get('AvgResponseTime', 'N/A')} ms")
        lines.append("")

    # Errors
    if data.get("errors"):
        lines.append("### Errors")
        for err in data["errors"]:
            lines.append(f"- ⚠️ {err}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Pull SEO data from Bing WMT and GSC")
    parser.add_argument("--days", type=int, default=30, help="Number of days to retrieve (default: 30)")
    parser.add_argument("--site", type=str, default=None, help="Site URL (default: from env)")
    parser.add_argument("--output", type=str, default=None, help="Output file (default: stdout)")
    args = parser.parse_args()

    site_url = args.site or Config.WORDPRESS_SITE_URL
    if not site_url:
        print("ERROR: No site URL provided. Set WORDPRESS_SITE_URL or use --site")
        sys.exit(1)

    print(f"=== SEO Data Pull for {site_url} ===")

    bing_data = pull_bing_data(site_url, args.days)

    report = format_report(bing_data, args.days)

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"\nReport saved to {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()