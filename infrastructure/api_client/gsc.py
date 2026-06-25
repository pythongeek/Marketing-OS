"""
AgenticMarketingPro — Google Search Console API Wrapper
========================================================
Pulls search analytics, index coverage, and Core Web Vitals data.
Uses OAuth2 (service account or user credentials) via Google APIs.

Prerequisites:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

Authentication:
    1. Create OAuth2 credentials in Google Cloud Console
    2. Download client secrets JSON → set GOOGLE_CLIENT_SECRETS_FILE
    3. Or use service account JSON → set GOOGLE_APPLICATION_CREDENTIALS
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from config import Config
from api_client.base import APIClient

logger = logging.getLogger("amp.gsc")


class GSCClient:
    """Google Search Console API client."""

    BASE_URL = "https://www.googleapis.com/webmasters/v3"
    SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]

    def __init__(self, property_url: Optional[str] = None):
        self.property_url = property_url or Config.GSC_PROPERTY
        if not self.property_url:
            raise ValueError("GSC property URL not configured. Set GSC_PROPERTY env var.")

        # Try OAuth2 first, then service account, then API key
        self._client = None
        self._api_client = APIClient(
            base_url=self.BASE_URL,
            name="gsc",
            rate_limit_rps=0.5,  # GSC is strict
        )
        self._init_auth()

    def _init_auth(self):
        """Initialize Google OAuth2 or service account auth."""
        try:
            from google.oauth2 import service_account
            from google.auth.transport.requests import Request
            from google_auth_oauthlib.flow import InstalledAppFlow
            import pickle

            # Try service account first
            creds_path = Path("service_account.json")
            if creds_path.exists():
                credentials = service_account.Credentials.from_service_account_file(
                    str(creds_path), scopes=self.SCOPES
                )
                self._client = credentials
                logger.info("GSC auth: service account")
                return

            # Try OAuth2 user credentials
            token_path = Path("token.pickle")
            secrets_path = Path(Config.GOOGLE_CLIENT_SECRETS_FILE) if Config.GOOGLE_CLIENT_SECRETS_FILE else None

            if token_path.exists():
                with open(token_path, "rb") as token:
                    creds = pickle.load(token)
            elif secrets_path and secrets_path.exists():
                flow = InstalledAppFlow.from_client_secrets_file(str(secrets_path), self.SCOPES)
                creds = flow.run_local_server(port=0)
                with open(token_path, "wb") as token:
                    pickle.dump(creds, token)
            else:
                logger.warning("No GSC auth found. Set GOOGLE_CLIENT_SECRETS_FILE or place service_account.json")
                return

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            self._client = creds
            logger.info("GSC auth: OAuth2 user credentials")

        except ImportError:
            logger.warning("google-auth packages not installed. Run: pip install google-api-python-client")
        except Exception as e:
            logger.error(f"GSC auth init failed: {e}")

    def _make_request(self, endpoint: str, method: str = "GET", body: Optional[Dict] = None) -> Any:
        """Make authenticated request to GSC API."""
        if not self._client:
            return {"error": "Not authenticated"}

        try:
            import googleapiclient.discovery
            service = googleapiclient.discovery.build(
                "webmasters", "v3", credentials=self._client, cache_discovery=False
            )

            # Parse endpoint and call appropriate method
            parts = endpoint.strip("/").split("/")
            resource = service
            for part in parts:
                resource = getattr(resource, part)()

            if method == "GET":
                return resource.execute()
            elif method == "POST":
                return resource.execute(body=body)
            else:
                return resource.execute()

        except Exception as e:
            logger.error(f"GSC API error: {e}")
            return {"error": str(e)}

    # ── Search Analytics ────────────────────────────────────────────────

    def search_analytics(
        self,
        start_date: str,
        end_date: str,
        dimensions: List[str] = None,
        row_limit: int = 1000,
        start_row: int = 0,
        dimension_filter_groups: Optional[List] = None,
    ) -> Dict[str, Any]:
        """
        Pull search analytics data.

        Args:
            start_date: YYYY-MM-DD
            end_date: YYYY-MM-DD
            dimensions: ["query", "page", "country", "device", "searchAppearance"]
            row_limit: Max rows per request (max 25,000)
            start_row: Pagination offset
            dimension_filter_groups: Optional filters
        """
        dimensions = dimensions or ["query"]

        body = {
            "startDate": start_date,
            "endDate": end_date,
            "dimensions": dimensions,
            "rowLimit": min(row_limit, 25000),
            "startRow": start_row,
        }
        if dimension_filter_groups:
            body["dimensionFilterGroups"] = dimension_filter_groups

        return self._make_request(
            f"sites/{self.property_url}/searchAnalytics/query",
            method="POST",
            body=body,
        )

    def get_queries(self, days: int = 7, limit: int = 1000) -> List[Dict]:
        """Pull top queries for last N days."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        result = self.search_analytics(
            start_date=start,
            end_date=end,
            dimensions=["query"],
            row_limit=limit,
        )
        return result.get("rows", [])

    def get_pages(self, days: int = 7, limit: int = 1000) -> List[Dict]:
        """Pull top pages for last N days."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        result = self.search_analytics(
            start_date=start,
            end_date=end,
            dimensions=["page"],
            row_limit=limit,
        )
        return result.get("rows", [])

    def get_ctr_opportunities(self, days: int = 7) -> List[Dict]:
        """Find high-impression, low-CTR queries."""
        queries = self.get_queries(days=days, limit=5000)
        opportunities = []
        for row in queries:
            clicks = row.get("clicks", 0)
            impressions = row.get("impressions", 0)
            ctr = row.get("ctr", 0) if "ctr" in row else (clicks / impressions if impressions else 0)
            position = row.get("position", 0)
            query = row.get("keys", [""])[0]

            if impressions > 500 and ctr < 0.02 and position <= 10:
                opportunities.append({
                    "query": query,
                    "impressions": impressions,
                    "clicks": clicks,
                    "ctr": round(ctr * 100, 2),
                    "position": round(position, 1),
                })

        return sorted(opportunities, key=lambda x: x["impressions"], reverse=True)[:50]

    # ── Index Coverage ────────────────────────────────────────────────

    def index_status(self) -> Dict[str, Any]:
        """Get index coverage summary."""
        return self._make_request(f"sites/{self.property_url}")

    def sitemaps(self) -> List[Dict]:
        """List submitted sitemaps."""
        result = self._make_request(f"sites/{self.property_url}/sitemaps")
        return result.get("sitemap", [])

    # ── Core Web Vitals (CrUX) ────────────────────────────────────────

    def core_web_vitals(self, url: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Core Web Vitals from Chrome UX Report API.
        Requires CrUX API key (different from GSC OAuth).
        """
        # CrUX API uses API key, not OAuth
        api_key = Config.PAGESPEED_API_KEY  # or dedicated CrUX key
        if not api_key:
            return {"error": "No API key for CrUX. Set PAGESPEED_API_KEY."}

        target = url or self.property_url
        client = APIClient(
            base_url="https://chromeuxreport.googleapis.com",
            api_key_param="key",
            api_key_value=api_key,
            name="crux",
        )
        return client.get(
            "/v1/records:queryRecord",
            json_body={"origin": target},
        ).body

    # ── Export to Vault Format ────────────────────────────────────────

    def weekly_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate a structured weekly report for vault write-back."""
        queries = self.get_queries(days=days)
        pages = self.get_pages(days=days)
        ctr_opp = self.get_ctr_opportunities(days=days)
        index = self.index_status()

        total_clicks = sum(r.get("clicks", 0) for r in queries)
        total_impressions = sum(r.get("impressions", 0) for r in queries)
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions else 0
        avg_position = sum(r.get("position", 0) for r in queries) / len(queries) if queries else 0

        return {
            "period_days": days,
            "total_clicks": total_clicks,
            "total_impressions": total_impressions,
            "avg_ctr": round(avg_ctr, 2),
            "avg_position": round(avg_position, 1),
            "top_queries": [
                {
                    "query": r.get("keys", [""])[0],
                    "clicks": r.get("clicks", 0),
                    "impressions": r.get("impressions", 0),
                    "ctr": round(r.get("ctr", 0) * 100, 2) if "ctr" in r else round(
                        r.get("clicks", 0) / r.get("impressions", 1) * 100, 2
                    ),
                    "position": round(r.get("position", 0), 1),
                }
                for r in queries[:20]
            ],
            "top_pages": [
                {
                    "page": r.get("keys", [""])[0],
                    "clicks": r.get("clicks", 0),
                    "impressions": r.get("impressions", 0),
                    "position": round(r.get("position", 0), 1),
                }
                for r in pages[:20]
            ],
            "ctr_opportunities": ctr_opp[:20],
            "index_status": index,
        }


if __name__ == "__main__":
    # Test with dummy property (will fail auth but shows structure)
    try:
        gsc = GSCClient("https://example.com/")
        print("GSCClient initialized. Auth status:", "OK" if gsc._client else "MISSING")
    except ValueError as e:
        print(f"Config error: {e}")
