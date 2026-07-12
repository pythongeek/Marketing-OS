"""
AgenticMarketingPro — Bing Webmaster Tools API Wrapper
========================================================
Pulls search analytics, site health, and crawl data from Bing.

Auth: OAuth2 (same as Google APIs) or API key
Docs: https://www.bing.com/webmaster/help/webmaster-api-8c5b4b77
"""

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional, Any

from config import Config
from api_client.base import APIClient

try:
    from supabase_api import SupabaseAPI
    _SUPABASE_AVAILABLE = True
except ImportError:
    _SUPABASE_AVAILABLE = False

logger = logging.getLogger("amp.bing")


class BingWMTClient:
    """Bing Webmaster Tools API client.

    Auth: API key sent in the `apikey` HTTP HEADER (not query string).
    The query-string format documented at Microsoft Learn is no longer
    accepted (returns 404); only the header-based auth works.

    Error codes from Bing:
        0 = Success
        3 = InvalidApiKey (key revoked, wrong account, or wrong IP)
        4 = InvalidSiteUrl
    """

    BASE_URL = "https://ssl.bing.com/webmaster/api.svc/json"

    def _sb(self):
        """Get a SupabaseAPI instance (cached for connection reuse)."""
        if not hasattr(self, "_sb_instance") or self._sb_instance is None:
            self._sb_instance = SupabaseAPI()
        return self._sb_instance

    def _get_bing_oauth_tokens(self):
        """Retrieve Bing OAuth tokens from Supabase bing_tokens table."""
        if not _SUPABASE_AVAILABLE:
            return None, None
        try:
            resp = self._sb().select(
                table="bing_tokens",
                columns="access_token,refresh_token,expires_at",
                limit=1,
            )
            if not resp.is_success:
                logger.warning(f"Could not read bing_tokens table: {resp.status_code} {resp.error}")
                return None, None
            if not resp.body:
                logger.info("bing_tokens table empty -- complete OAuth flow at /credentials")
                return None, None
            row = resp.body[0]
            return row.get("access_token"), row.get("refresh_token")
        except Exception as e:
            logger.error(f"OAuth token retrieval failed: {e}")
            return None, None

    def _refresh_access_token(self):
        """Refresh the Bing OAuth access token using the stored refresh_token."""
        if not _SUPABASE_AVAILABLE or not self.refresh_token:
            return None
        try:
            import requests
            from datetime import datetime, timedelta, timezone
            token_url = f"https://login.microsoftonline.com/{Config.BING_TENANT}/oauth2/v2.0/token"
            data = {
                "client_id": Config.BING_CLIENT_ID,
                "client_secret": Config.BING_CLIENT_SECRET,
                "refresh_token": self.refresh_token,
                "grant_type": "refresh_token",
                "scope": "https://api.bing.microsoft.com/.default offline_access",
            }
            r = requests.post(token_url, data=data, timeout=30)
            if r.status_code == 200:
                payload = r.json()
                new_access = payload.get("access_token")
                new_refresh = payload.get("refresh_token", self.refresh_token)
                expires_at = datetime.now(timezone.utc) + timedelta(seconds=payload.get("expires_in", 3600))
                try:
                    self._sb().update(
                        table="bing_tokens",
                        filters={"id": "default"},
                        updates={
                            "access_token": new_access,
                            "refresh_token": new_refresh,
                            "expires_at": expires_at.isoformat(),
                        },
                    )
                except Exception as e:
                    logger.warning(f"Failed to persist refreshed token: {e}")
                self.access_token = new_access
                self.refresh_token = new_refresh
                logger.info("Refreshed Bing access token")
                return new_access
            logger.warning(f"Token refresh failed: HTTP {r.status_code}")
            return None
        except Exception as e:
            logger.error(f"Token refresh exception: {e}")
            return None

    def _ensure_valid_token(self):
        """Check expiry and refresh if needed."""
        if not _SUPABASE_AVAILABLE or not self.access_token:
            return
        try:
            resp = self._sb().select(
                table="bing_tokens",
                columns="expires_at",
                limit=1,
            )
            if not resp.is_success or not resp.body:
                return
            expires_at = resp.body[0].get("expires_at")
            if not expires_at:
                return
            from datetime import datetime, timezone
            # Handle ISO format with or without timezone
            if expires_at.endswith("Z"):
                expires_at = expires_at[:-1] + "+00:00"
            exp = datetime.fromisoformat(expires_at)
            if exp.tzinfo is None:
                exp = exp.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            if (exp - now).total_seconds() < 300:
                logger.info("Access token expiring soon -- refreshing")
                self._refresh_access_token()
        except Exception as e:
            logger.warning(f"Token expiry check failed: {e}")

    def __init__(self):
        # Prioritize OAuth tokens if available
        self.access_token, self.refresh_token = self._get_bing_oauth_tokens()
        if self.access_token:
            self.client = APIClient(
                base_url=self.BASE_URL,
                auth_header="Authorization",
                auth_value=f"Bearer {self.access_token}",
                rate_limit_rps=1.0,
                name="bing_wmt",
            )
            logger.info("Initialized BingWMTClient with OAuth.")
            # Verify token is still valid; refresh if expiring within 5 minutes
            self._ensure_valid_token()
            # Update auth_value in case _ensure_valid_token refreshed it
            self.client.auth_value = f"Bearer {self.access_token}"
        else:
            # Fallback to API Key only if explicitly provided
            self.api_key = Config.BING_API_KEY
            if self.api_key:
                self.client = APIClient(
                    base_url=self.BASE_URL,
                    auth_header="apikey",
                    auth_value=self.api_key,
                    rate_limit_rps=1.0,
                    name="bing_wmt",
                )
                logger.warning(
                    "Initialized BingWMTClient with API key fallback. "
                    "Complete the OAuth flow at /credentials for full functionality."
                )
            else:
                raise ValueError(
                    "Bing not configured. Complete OAuth flow at /credentials page, "
                    "or set BING_API_KEY env var as fallback."
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
