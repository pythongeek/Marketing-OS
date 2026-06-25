"""
AgenticMarketingPro — Bing Webmaster Tools API Wrapper
========================================================
Pulls search analytics, site health, and crawl data from Bing.

Auth: OAuth2 (same as Google APIs) or API key
Docs: https://www.bing.com/webmaster/help/webmaster-api-8c5b4b77
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from config import Config
from api_client.base import APIClient

logger = logging.getLogger("amp.bing")


class BingWMTClient:
    """Bing Webmaster Tools API client."""

    BASE_URL = "https://ssl.bing.com/webmaster/api.svc/json"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.BING_API_KEY
        if not self.api_key:
            raise ValueError("Bing API key not configured. Set BING_API_KEY env var.")

        self.client = APIClient(
            base_url=self.BASE_URL,
            api_key_param="apikey",
            api_key_value=self.api_key,
            rate_limit_rps=1.0,
            name="bing_wmt",
        )

    # ── Site Management ─────────────────────────────────────────────────

    def list_sites(self) -> List[Dict]:
        """List all sites in the account."""
        resp = self.client.get("/GetSites")
        return resp.body if isinstance(resp.body, list) else []

    def site_details(self, site_url: str) -> Dict[str, Any]:
        """Get details for a specific site."""
        return self.client.get(
            "/GetSiteDetails",
            params={"siteUrl": site_url},
        ).body

    # ── Traffic & Search Analytics ────────────────────────────────────

    def traffic_stats(self, site_url: str, days: int = 7) -> Dict[str, Any]:
        """Get traffic statistics for a site."""
        end = datetime.now()
        start = end - timedelta(days=days)
        
        return self.client.get(
            "/GetTrafficStats",
            params={
                "siteUrl": site_url,
                "startDate": start.strftime("%Y-%m-%d"),
                "endDate": end.strftime("%Y-%m-%d"),
            },
        ).body

    def search_keywords(self, site_url: str, days: int = 7, limit: int = 100) -> List[Dict]:
        """Get search keywords for a site."""
        end = datetime.now()
        start = end - timedelta(days=days)
        
        resp = self.client.get(
            "/GetSearchKeywords",
            params={
                "siteUrl": site_url,
                "startDate": start.strftime("%Y-%m-%d"),
                "endDate": end.strftime("%Y-%m-%d"),
                "top": limit,
            },
        )
        return resp.body if isinstance(resp.body, list) else []

    def crawl_stats(self, site_url: str, days: int = 7) -> Dict[str, Any]:
        """Get crawl statistics."""
        end = datetime.now()
        start = end - timedelta(days=days)
        
        return self.client.get(
            "/GetCrawlStats",
            params={
                "siteUrl": site_url,
                "startDate": start.strftime("%Y-%m-%d"),
                "endDate": end.strftime("%Y-%m-%d"),
            },
        ).body

    # ── Index & Crawl Issues ────────────────────────────────────────

    def crawl_issues(self, site_url: str) -> List[Dict]:
        """Get crawl issues (404s, redirects, etc.)."""
        resp = self.client.get(
            "/GetCrawlIssues",
            params={"siteUrl": site_url},
        )
        return resp.body if isinstance(resp.body, list) else []

    def indexed_pages(self, site_url: str) -> Dict[str, Any]:
        """Get indexed pages count."""
        return self.client.get(
            "/GetIndexedPages",
            params={"siteUrl": site_url},
        ).body

    def inbound_links(self, site_url: str, limit: int = 100) -> List[Dict]:
        """Get inbound links."""
        resp = self.client.get(
            "/GetInboundLinks",
            params={"siteUrl": site_url, "top": limit},
        )
        return resp.body if isinstance(resp.body, list) else []

    # ── Submit URLs ─────────────────────────────────────────────────

    def submit_url(self, site_url: str, url: str) -> Dict[str, Any]:
        """Submit a URL for indexing."""
        return self.client.post(
            "/SubmitUrl",
            json_body={"siteUrl": site_url, "url": url},
        ).body

    def submit_sitemap(self, site_url: str, sitemap_url: str) -> Dict[str, Any]:
        """Submit a sitemap."""
        return self.client.post(
            "/SubmitSitemap",
            json_body={"siteUrl": site_url, "sitemapUrl": sitemap_url},
        ).body

    # ── Weekly Report Export ──────────────────────────────────────────

    def weekly_report(self, site_url: str, days: int = 7) -> Dict[str, Any]:
        """Generate structured weekly report for vault."""
        traffic = self.traffic_stats(site_url, days)
        keywords = self.search_keywords(site_url, days, limit=100)
        crawl = self.crawl_stats(site_url, days)
        issues = self.crawl_issues(site_url)
        indexed = self.indexed_pages(site_url)
        links = self.inbound_links(site_url, limit=50)

        return {
            "site": site_url,
            "period_days": days,
            "traffic": traffic,
            "top_keywords": [
                {
                    "keyword": k.get("Query", ""),
                    "clicks": k.get("Clicks", 0),
                    "impressions": k.get("Impressions", 0),
                    "ctr": round(k.get("Clicks", 0) / max(k.get("Impressions", 1), 1) * 100, 2),
                    "position": k.get("Position", 0),
                }
                for k in keywords[:20]
            ],
            "crawl_stats": crawl,
            "crawl_issues": issues[:20] if isinstance(issues, list) else [],
            "indexed_pages": indexed,
            "inbound_links": [
                {
                    "source": l.get("SourceUrl", ""),
                    "target": l.get("TargetUrl", ""),
                    "anchor": l.get("AnchorText", ""),
                }
                for l in (links[:20] if isinstance(links, list) else [])
            ],
        }


if __name__ == "__main__":
    try:
        client = BingWMTClient()
        print("BingWMTClient initialized. Health check:")
        print(client.client.health_check())
    except ValueError as e:
        print(f"Config error: {e}")
