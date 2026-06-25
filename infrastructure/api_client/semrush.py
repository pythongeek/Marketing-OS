"""
AgenticMarketingPro — Semrush API Wrapper
=========================================
Uses Semrush Analytics API v3 for keyword, domain, and competitive data.

Auth: API key via API key parameter
Docs: https://developer.semrush.com/api/v3/
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any

from config import Config
from api_client.base import APIClient

logger = logging.getLogger("amp.semrush")


class SemrushClient:
    """Semrush Analytics API v3 client."""

    BASE_URL = "https://api.semrush.com"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or Config.SEMRUSH_API_KEY
        if not self.api_key:
            raise ValueError("Semrush API key not configured. Set SEMRUSH_API_KEY env var.")

        self.client = APIClient(
            base_url=self.BASE_URL,
            api_key_param="key",
            api_key_value=self.api_key,
            rate_limit_rps=1.0,
            name="semrush",
        )

    # ── Domain Overview ───────────────────────────────────────────────

    def domain_overview(self, domain: str, database: str = "us") -> List[Dict]:
        """Get domain overview metrics."""
        resp = self.client.get(
            "/",
            params={
                "type": "domain_ranks",
                "domain": domain,
                "database": database,
            },
        )
        return self._parse_csv(resp.body)

    def organic_keywords(self, domain: str, database: str = "us", limit: int = 100) -> List[Dict]:
        """Get organic keywords for a domain."""
        resp = self.client.get(
            "/",
            params={
                "type": "domain_organic",
                "domain": domain,
                "database": database,
                "display_limit": limit,
                "display_sort": "tr_desc",
            },
        )
        return self._parse_csv(resp.body)

    def paid_keywords(self, domain: str, database: str = "us", limit: int = 100) -> List[Dict]:
        """Get paid keywords for a domain."""
        resp = self.client.get(
            "/",
            params={
                "type": "domain_adwords",
                "domain": domain,
                "database": database,
                "display_limit": limit,
                "display_sort": "po_desc",
            },
        )
        return self._parse_csv(resp.body)

    def backlinks_overview(self, domain: str) -> List[Dict]:
        """Get backlink overview for a domain."""
        resp = self.client.get(
            "/",
            params={
                "type": "backlinks_overview",
                "target": domain,
                "target_type": "root_domain",
            },
        )
        return self._parse_csv(resp.body)

    # ── Keyword Research ──────────────────────────────────────────────

    def keyword_overview(self, keywords: List[str], database: str = "us") -> List[Dict]:
        """Get keyword overview (volume, CPC, competition, difficulty)."""
        resp = self.client.get(
            "/",
            params={
                "type": "phrase_all",
                "phrase": ",".join(keywords),
                "database": database,
            },
        )
        return self._parse_csv(resp.body)

    def keyword_difficulty(self, keywords: List[str], database: str = "us") -> List[Dict]:
        """Get keyword difficulty scores."""
        resp = self.client.get(
            "/",
            params={
                "type": "phrase_kdi",
                "phrase": ",".join(keywords),
                "database": database,
            },
        )
        return self._parse_csv(resp.body)

    def related_keywords(self, keyword: str, database: str = "us", limit: int = 100) -> List[Dict]:
        """Get related keyword suggestions."""
        resp = self.client.get(
            "/",
            params={
                "type": "phrase_related",
                "phrase": keyword,
                "database": database,
                "display_limit": limit,
                "display_sort": "re_desc",
            },
        )
        return self._parse_csv(resp.body)

    # ── Competitive Analysis ────────────────────────────────────────

    def organic_competitors(self, domain: str, database: str = "us", limit: int = 20) -> List[Dict]:
        """Find organic search competitors."""
        resp = self.client.get(
            "/",
            params={
                "type": "domain_organic_organic",
                "domain": domain,
                "database": database,
                "display_limit": limit,
            },
        )
        return self._parse_csv(resp.body)

    def keyword_gap(self, domain1: str, domain2: str, database: str = "us", limit: int = 100) -> List[Dict]:
        """Find keywords domain2 ranks for but domain1 doesn't."""
        resp = self.client.get(
            "/",
            params={
                "type": "domain_organic_organic",
                "domain": domain1,
                "display_limit": limit,
                "database": database,
            },
        )
        # Semrush doesn't have a direct content gap API; this is a workaround
        # In practice, you'd compare organic keywords of both domains
        return self._parse_csv(resp.body)

    # ── SERP Features ─────────────────────────────────────────────────

    def serp_features(self, keyword: str, database: str = "us") -> List[Dict]:
        """Get SERP features for a keyword."""
        resp = self.client.get(
            "/",
            params={
                "type": "phrase_fullsearch",
                "phrase": keyword,
                "database": database,
            },
        )
        return self._parse_csv(resp.body)

    # ── CSV Parser ────────────────────────────────────────────────────

    def _parse_csv(self, raw: Any) -> List[Dict]:
        """Parse Semrush CSV response into list of dicts."""
        if not raw or isinstance(raw, dict) and "error" in raw:
            return []
        
        text = raw if isinstance(raw, str) else str(raw)
        lines = text.strip().split("\n")
        if not lines:
            return []
        
        # Semrush returns semicolon-separated CSV
        headers = lines[0].split(";")
        rows = []
        for line in lines[1:]:
            if not line.strip():
                continue
            values = line.split(";")
            row = {}
            for h, v in zip(headers, values):
                row[h.strip()] = v.strip()
            rows.append(row)
        return rows

    # ── Weekly Report Export ──────────────────────────────────────────

    def weekly_report(self, domain: str, database: str = "us", days: int = 7) -> Dict[str, Any]:
        """Generate structured weekly report for vault."""
        overview = self.domain_overview(domain, database)
        keywords = self.organic_keywords(domain, database, limit=1000)
        competitors = self.organic_competitors(domain, database, limit=20)
        backlinks = self.backlinks_overview(domain)

        return {
            "domain": domain,
            "database": database,
            "period_days": days,
            "overview": overview[0] if overview else {},
            "top_keywords": [
                {
                    "keyword": k.get("Keyword", ""),
                    "position": k.get("Position", "0"),
                    "volume": k.get("Search Volume", "0"),
                    "cpc": k.get("CPC", "0"),
                    "traffic": k.get("Traffic (%)", "0"),
                    "url": k.get("Url", ""),
                }
                for k in keywords[:50]
            ],
            "competitors": [
                {
                    "domain": c.get("Domain", ""),
                    "common_keywords": c.get("Common Keywords", "0"),
                    "se_keywords": c.get("SE Keywords", "0"),
                }
                for c in competitors[:20]
            ],
            "backlinks": backlinks[0] if backlinks else {},
        }


if __name__ == "__main__":
    try:
        client = SemrushClient()
        print("SemrushClient initialized. Health check:")
        print(client.client.health_check())
    except ValueError as e:
        print(f"Config error: {e}")
