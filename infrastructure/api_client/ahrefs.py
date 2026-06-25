"""
AgenticMarketingPro — Ahrefs API Wrapper
========================================
Uses Ahrefs API v3 (or DataForSEO as fallback for Ahrefs data).

Endpoints covered:
- Site Explorer: Overview, backlinks, referring domains, organic keywords
- Content Explorer: Top pages, content gaps
- Keywords Explorer: Keyword metrics, SERP overview

Auth: API token via X-Api-Token header
Docs: https://ahrefs.com/api/documentation
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from config import Config
from api_client.base import APIClient

logger = logging.getLogger("amp.ahrefs")


class AhrefsClient:
    """Ahrefs API v3 client."""

    BASE_URL = "https://apiv3.ahrefs.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.AHREFS_API_KEY
        if not self.api_key:
            raise ValueError("Ahrefs API key not configured. Set AHREFS_API_KEY env var.")

        self.client = APIClient(
            base_url=self.BASE_URL,
            auth_header="X-Api-Token",
            auth_value=self.api_key,
            rate_limit_rps=0.5,  # Ahrefs is conservative
            name="ahrefs",
        )

    # ── Site Explorer ─────────────────────────────────────────────────

    def site_overview(self, target: str, mode: str = "domain") -> Dict[str, Any]:
        """Get site overview (DR, UR, backlinks, referring domains, organic traffic)."""
        return self.client.get(
            "/v3/site-explorer/overview",
            params={"target": target, "mode": mode},
        ).body

    def backlinks(self, target: str, limit: int = 100, mode: str = "domain") -> List[Dict]:
        """Get backlink profile."""
        resp = self.client.get(
            "/v3/site-explorer/backlinks",
            params={"target": target, "limit": limit, "mode": mode, "where": "dofollow"},
        )
        return resp.body.get("backlinks", []) if isinstance(resp.body, dict) else []

    def referring_domains(self, target: str, limit: int = 100, mode: str = "domain") -> List[Dict]:
        """Get referring domains."""
        resp = self.client.get(
            "/v3/site-explorer/ref-domains",
            params={"target": target, "limit": limit, "mode": mode},
        )
        return resp.body.get("refdomains", []) if isinstance(resp.body, dict) else []

    def organic_keywords(self, target: str, limit: int = 100, mode: str = "domain", country: str = "us") -> List[Dict]:
        """Get organic keywords."""
        resp = self.client.get(
            "/v3/site-explorer/organic-keywords",
            params={"target": target, "limit": limit, "mode": mode, "country": country},
        )
        return resp.body.get("keywords", []) if isinstance(resp.body, dict) else []

    def top_pages(self, target: str, limit: int = 100, mode: str = "domain") -> List[Dict]:
        """Get top pages by organic traffic."""
        resp = self.client.get(
            "/v3/site-explorer/top-pages",
            params={"target": target, "limit": limit, "mode": mode},
        )
        return resp.body.get("pages", []) if isinstance(resp.body, dict) else []

    # ── Keywords Explorer ─────────────────────────────────────────────

    def keyword_metrics(self, keywords: List[str], country: str = "us") -> List[Dict]:
        """Get keyword metrics (volume, KD, CPC, parent topic)."""
        resp = self.client.get(
            "/v3/keywords-explorer/metrics",
            params={"keywords": ",".join(keywords), "country": country},
        )
        return resp.body.get("metrics", []) if isinstance(resp.body, dict) else []

    def keyword_suggestions(self, seed: str, limit: int = 100, country: str = "us") -> List[Dict]:
        """Get keyword suggestions."""
        resp = self.client.get(
            "/v3/keywords-explorer/suggestions",
            params={"seed": seed, "limit": limit, "country": country, "mode": "prefix"},
        )
        return resp.body.get("suggestions", []) if isinstance(resp.body, dict) else []

    # ── Competitor Analysis ──────────────────────────────────────────

    def content_gap(self, target: str, competitors: List[str], limit: int = 100) -> List[Dict]:
        """Find keywords competitors rank for but target doesn't."""
        # Ahrefs content gap API
        resp = self.client.get(
            "/v3/site-explorer/content-gap",
            params={
                "target": target,
                "competitors": ",".join(competitors),
                "limit": limit,
            },
        )
        return resp.body.get("keywords", []) if isinstance(resp.body, dict) else []

    # ── Weekly Report Export ──────────────────────────────────────────

    def weekly_report(self, target: str, days: int = 7) -> Dict[str, Any]:
        """Generate structured weekly report for vault."""
        overview = self.site_overview(target)
        keywords = self.organic_keywords(target, limit=1000)
        top_pages = self.top_pages(target, limit=50)
        backlinks = self.backlinks(target, limit=100)
        ref_domains = self.referring_domains(target, limit=100)

        # Calculate keyword changes (would need historical data for true comparison)
        return {
            "target": target,
            "period_days": days,
            "overview": {
                "domain_rating": overview.get("domain_rating", {}).get("value") if isinstance(overview, dict) else None,
                "url_rating": overview.get("url_rating", {}).get("value") if isinstance(overview, dict) else None,
                "backlinks": overview.get("backlinks", {}).get("value") if isinstance(overview, dict) else None,
                "referring_domains": overview.get("refdomains", {}).get("value") if isinstance(overview, dict) else None,
                "organic_traffic": overview.get("organic_traffic", {}).get("value") if isinstance(overview, dict) else None,
                "organic_keywords": overview.get("organic_keywords", {}).get("value") if isinstance(overview, dict) else None,
            },
            "top_keywords": [
                {
                    "keyword": k.get("keyword", ""),
                    "volume": k.get("volume", 0),
                    "kd": k.get("difficulty", 0),
                    "position": k.get("position", 0),
                    "traffic": k.get("traffic", 0),
                    "url": k.get("url", ""),
                }
                for k in keywords[:50]
            ],
            "top_pages": [
                {
                    "url": p.get("url", ""),
                    "traffic": p.get("traffic", 0),
                    "keywords": p.get("keywords", 0),
                }
                for p in top_pages[:20]
            ],
            "new_backlinks": [
                {
                    "source": b.get("url_from", ""),
                    "target": b.get("url_to", ""),
                    "anchor": b.get("anchor", ""),
                    "dr": b.get("domain_rating", 0),
                    "dofollow": b.get("dofollow", True),
                }
                for b in backlinks[:50]
            ],
            "referring_domains": [
                {
                    "domain": d.get("domain", ""),
                    "dr": d.get("domain_rating", 0),
                    "backlinks": d.get("backlinks", 0),
                }
                for d in ref_domains[:50]
            ],
        }


if __name__ == "__main__":
    try:
        client = AhrefsClient()
        print("AhrefsClient initialized. Health check:")
        print(client.client.health_check())
    except ValueError as e:
        print(f"Config error: {e}")
