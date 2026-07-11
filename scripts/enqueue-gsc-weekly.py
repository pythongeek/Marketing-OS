#!/usr/bin/env python3
"""
Enqueue a GSC weekly job in Supabase.

This script is meant to be triggered by cron-job.org (or any cron)
every Monday morning. It writes a job row to the jobs table with
type='gsc_pull', which the poller (or Edge Function) will pick up
within seconds and execute.

Usage:
    python scripts/enqueue-gsc-weekly.py
    python scripts/enqueue-gsc-weekly.py --days 14
    python scripts/enqueue-gsc-weekly.py --client-slug my-client
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path

# Allow running from anywhere in the repo
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root / "infrastructure"))

from config import Config  # noqa: E402


def enqueue_weekly_job(
    days: int = 7,
    client_slug: str = None,
    job_type: str = "gsc_pull",
    skill_slug: str = "gsc-expert",
) -> dict:
    """Insert a weekly report job row into Supabase.

    job_type examples:
        - "gsc_pull"   → GSC search analytics
        - "ga4_pull"   → GA4 traffic
        - "bing_pull"  → Bing Webmaster
    """
    try:
        from supabase import create_client
    except ImportError:
        return {"ok": False, "error": "supabase-py not installed (pip install supabase)"}

    url = Config.SUPABASE_URL or os.getenv("SUPABASE_URL")
    key = Config.SUPABASE_SERVICE_ROLE_KEY or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        return {"ok": False, "error": "SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not set"}

    client = create_client(url, key)

    payload = {
        "mode": "weekly",
        "days": days,
    }
    if client_slug:
        payload["client_slug"] = client_slug

    job_row = {
        "type": job_type,
        "skill_slug": skill_slug,
        "client_slug": client_slug,
        "payload": payload,
        "status": "pending",
    }

    try:
        result = client.table("jobs").insert(job_row).execute()
        job_id = result.data[0]["id"] if result.data else None
        return {
            "ok": True,
            "job_id": job_id,
            "job_type": job_type,
            "skill_slug": skill_slug,
            "scheduled_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
    except Exception as e:
        return {"ok": False, "error": str(e)}


# Backward-compat alias
enqueue_gsc_weekly_job = enqueue_weekly_job


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enqueue a weekly report job")
    parser.add_argument("--type", choices=["gsc_pull", "ga4_pull", "bing_pull"],
                        default="gsc_pull", help="Job type")
    parser.add_argument("--skill", default=None, help="Skill slug (defaults based on --type)")
    parser.add_argument("--days", type=int, default=7, help="Days of analytics to pull")
    parser.add_argument("--client-slug", default=None, help="Optional client slug")
    args = parser.parse_args()

    skill_defaults = {
        "gsc_pull": "gsc-expert",
        "ga4_pull": "analytics-expert",
        "bing_pull": "bing-wmt-expert",
    }
    skill = args.skill or skill_defaults[args.type]

    print(json.dumps(
        enqueue_weekly_job(args.days, args.client_slug, args.type, skill),
        indent=2,
    ))