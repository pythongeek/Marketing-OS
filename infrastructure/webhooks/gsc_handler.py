"""
AgenticMarketingPro — GSC Job Handler
======================================
Pulls Google Search Console data on a scheduled basis and writes
weekly reports to the vault.

Two trigger modes:
  - "weekly"  → generates the weekly report and writes gsc-weekly-log.md
  - "pull"    → just fetches raw analytics for a given date range
"""

import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.gsc_handler")


def _get_gsc_client():
    """Lazy-import the GSC client so missing google libs don't break the poller."""
    try:
        from api_client.gsc import GSCClient
        return GSCClient()
    except Exception as e:
        logger.error(f"Failed to initialize GSC client: {e}")
        return None


def execute_gsc_job(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Dispatch table for GSC jobs.

    payload = {
        "mode": "weekly" | "pull",
        "days": int,                       # default 7 for weekly, 30 for pull
        "dimensions": ["query", "page"],   # for pull mode
        "client_slug": "...",              # optional, for vault tagging
    }
    """
    mode = payload.get("mode", "weekly")
    days = int(payload.get("days", 7 if mode == "weekly" else 30))
    dimensions = payload.get("dimensions", ["query"])
    client_slug = payload.get("client_slug")

    gsc = _get_gsc_client()
    if gsc is None:
        return {
            "ok": False,
            "error": "GSC client not initialized. Check credentials and GSC_PROPERTY env var.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    if not gsc._client:
        return {
            "ok": False,
            "error": (
                "GSC authentication failed. Set one of: "
                "GSC_SERVICE_ACCOUNT_FILE, GSC_SERVICE_ACCOUNT_JSON, "
                "GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLIENT_SECRETS_FILE."
            ),
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    try:
        if mode == "weekly":
            out_path = gsc.write_weekly_report_to_vault(days=days)
            return {
                "ok": True,
                "mode": "weekly",
                "vault_path": str(out_path),
                "property": gsc.property_url,
                "days": days,
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        elif mode == "pull":
            end = datetime.now().strftime("%Y-%m-%d")
            start = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
            result = gsc.search_analytics(
                start_date=start,
                end_date=end,
                dimensions=dimensions,
                row_limit=int(payload.get("row_limit", 1000)),
            )
            return {
                "ok": True,
                "mode": "pull",
                "property": gsc.property_url,
                "date_range": {"start": start, "end": end},
                "dimensions": dimensions,
                "rows": result.get("rows", []),
                "row_count": len(result.get("rows", [])),
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

        else:
            return {
                "ok": False,
                "error": f"Unknown GSC job mode: {mode}",
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }

    except Exception as e:
        logger.exception("GSC job failed")
        return {
            "ok": False,
            "error": str(e),
            "mode": mode,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


# ── CLI for manual / cron use ─────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run a GSC job (weekly report or pull)")
    parser.add_argument("--mode", choices=["weekly", "pull"], default="weekly")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--dimensions", default="query",
                        help="Comma-separated dimensions for pull mode")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

    payload = {
        "mode": args.mode,
        "days": args.days,
    }
    if args.mode == "pull":
        payload["dimensions"] = [d.strip() for d in args.dimensions.split(",")]

    result = execute_gsc_job(payload)
    print(json.dumps(result, indent=2, default=str))