"""
AgenticMarketingPro — GA4 API Wrapper
======================================
Pulls Google Analytics 4 data: traffic, conversions, events, audiences.
Uses OAuth2 via google-analytics-data library.

Prerequisites:
    pip install google-analytics-data

Authentication:
    Same as GSC — OAuth2 or service account.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from config import Config

logger = logging.getLogger("amp.ga4")


class GA4Client:
    """Google Analytics 4 Data API client."""

    def __init__(self, property_id: Optional[str] = None):
        self.property_id = property_id or Config.GA4_PROPERTY_ID
        if not self.property_id:
            raise ValueError("GA4 property ID not configured. Set GA4_PROPERTY_ID env var.")

        # Property ID format: properties/123456789
        if not self.property_id.startswith("properties/"):
            self.property_id = f"properties/{self.property_id}"

        self._client = None
        self._init_auth()

    def _init_auth(self):
        """Initialize Google auth."""
        try:
            from google.oauth2 import service_account
            from google.analytics.data_v1beta import BetaAnalyticsDataClient
            from google.analytics.data_v1beta.types import RunReportRequest

            creds_path = Path("service_account.json")
            if creds_path.exists():
                credentials = service_account.Credentials.from_service_account_file(
                    str(creds_path)
                )
                self._client = BetaAnalyticsDataClient(credentials=credentials)
                logger.info("GA4 auth: service account")
                return

            # Try default credentials (ADC)
            self._client = BetaAnalyticsDataClient()
            logger.info("GA4 auth: default credentials")

        except ImportError:
            logger.warning("google-analytics-data not installed. Run: pip install google-analytics-data")
        except Exception as e:
            logger.error(f"GA4 auth init failed: {e}")

    def _run_report(
        self,
        dimensions: List[str],
        metrics: List[str],
        date_ranges: List[Dict[str, str]],
        row_limit: int = 1000,
        dimension_filter: Optional[Any] = None,
    ) -> List[Dict[str, Any]]:
        """Execute a GA4 report request."""
        if not self._client:
            return []

        try:
            from google.analytics.data_v1beta.types import (
                RunReportRequest,
                DateRange,
                Dimension,
                Metric,
            )

            request = RunReportRequest(
                property=self.property_id,
                dimensions=[Dimension(name=d) for d in dimensions],
                metrics=[Metric(name=m) for m in metrics],
                date_ranges=[DateRange(start_date=r["start"], end_date=r["end"]) for r in date_ranges],
                limit=row_limit,
            )
            if dimension_filter:
                request.dimension_filter = dimension_filter

            response = self._client.run_report(request)

            rows = []
            for row in response.rows:
                record = {}
                for dim, val in zip(dimensions, row.dimension_values):
                    record[dim] = val.value
                for metric, val in zip(metrics, row.metric_values):
                    record[metric] = val.value
                rows.append(record)
            return rows

        except Exception as e:
            logger.error(f"GA4 report error: {e}")
            return []

    # ── Common Reports ────────────────────────────────────────────────

    def traffic_overview(self, days: int = 7) -> Dict[str, Any]:
        """Get traffic overview for last N days."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        rows = self._run_report(
            dimensions=["date"],
            metrics=["sessions", "users", "newUsers", "bounceRate", "averageSessionDuration", "conversions"],
            date_ranges=[{"start": start, "end": end}],
            row_limit=1000,
        )

        total_sessions = sum(int(r.get("sessions", 0)) for r in rows)
        total_users = sum(int(r.get("users", 0)) for r in rows)
        total_new = sum(int(r.get("newUsers", 0)) for r in rows)
        total_conversions = sum(float(r.get("conversions", 0)) for r in rows)

        return {
            "period_days": days,
            "total_sessions": total_sessions,
            "total_users": total_users,
            "new_users": total_new,
            "conversions": total_conversions,
            "daily_breakdown": [
                {
                    "date": r["date"],
                    "sessions": int(r.get("sessions", 0)),
                    "users": int(r.get("users", 0)),
                    "bounce_rate": round(float(r.get("bounceRate", 0)) * 100, 2),
                    "avg_session_duration": round(float(r.get("averageSessionDuration", 0)), 2),
                    "conversions": float(r.get("conversions", 0)),
                }
                for r in rows
            ],
        }

    def channel_performance(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get performance by channel."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        return self._run_report(
            dimensions=["sessionDefaultChannelGroup"],
            metrics=["sessions", "users", "conversions", "totalAdRevenue", "engagementRate"],
            date_ranges=[{"start": start, "end": end}],
            row_limit=100,
        )

    def landing_pages(self, days: int = 7, limit: int = 20) -> List[Dict[str, Any]]:
        """Get top landing pages."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        return self._run_report(
            dimensions=["landingPage"],
            metrics=["sessions", "users", "conversions", "engagementRate"],
            date_ranges=[{"start": start, "end": end}],
            row_limit=limit,
        )

    def conversions(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get conversion events."""
        end = datetime.now().strftime("%Y-%m-%d")
        start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        return self._run_report(
            dimensions=["eventName"],
            metrics=["eventCount", "eventCountPerUser"],
            date_ranges=[{"start": start, "end": end}],
            row_limit=100,
        )

    # ── Weekly Report Export ──────────────────────────────────────────

    def weekly_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate structured weekly report for vault."""
        traffic = self.traffic_overview(days=days)
        channels = self.channel_performance(days=days)
        landings = self.landing_pages(days=days)
        conversions = self.conversions(days=days)

        return {
            "period_days": days,
            "traffic": traffic,
            "channel_performance": channels,
            "top_landing_pages": landings,
            "conversions": conversions,
        }


if __name__ == "__main__":
    try:
        ga4 = GA4Client()
        print("GA4Client initialized. Auth status:", "OK" if ga4._client else "MISSING")
    except ValueError as e:
        print(f"Config error: {e}")
