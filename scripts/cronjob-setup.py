#!/usr/bin/env python3
"""
AgenticMarketingPro — cron-job.org Configuration Generator
==========================================================
Prints the exact URLs to paste into cron-job.org for each scheduled task.

Strategy: Bypass Edge Function 8s/150s timeout by triggering MANY short
calls (each processing ONE job) instead of one long call processing many.

Usage:
    python scripts/cronjob-setup.py
    python scripts/cronjob-setup.py --base-url https://your-project.supabase.co
"""

import argparse
import sys
from pathlib import Path

# Add infrastructure to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "infrastructure"))

DEFAULT_BASE_URL = "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs"


def generate_schedule(base_url: str, secret: str = None) -> str:
    """Generate the cron-job.org URL list."""

    # Optional: append the function secret as a query param for auth
    auth = f"&secret={secret}" if secret else ""

    jobs = [
        {
            "name": "AMP - Single Job Tick (every 1 min)",
            "url": f"{base_url}?mode=single{auth}",
            "cron": "* * * * *",  # every minute
            "purpose": "Process ONE pending job per call. Stays well under 8s timeout.",
        },
        {
            "name": "AMP - Light Batch (every 5 min)",
            "url": f"{base_url}?mode=batch&limit=3{auth}",
            "cron": "*/5 * * * *",
            "purpose": "Process up to 3 jobs per call. Catches up if single-tick queue is full.",
        },
        {
            "name": "AMP - GSC Weekly (Mondays 9am)",
            "url": f"{base_url}?mode=single&skill=gsc-expert{auth}",
            "cron": "0 9 * * 1",
            "purpose": "Triggers GSC weekly report generation.",
        },
        {
            "name": "AMP - GA4 Weekly (Mondays 9:05am)",
            "url": f"{base_url}?mode=single&skill=analytics-expert{auth}",
            "cron": "5 9 * * 1",
            "purpose": "Triggers GA4 traffic report.",
        },
        {
            "name": "AMP - Bing WMT Weekly (Mondays 9:10am)",
            "url": f"{base_url}?mode=single&skill=bing-wmt-expert{auth}",
            "cron": "10 9 * * 1",
            "purpose": "Triggers Bing Webmaster report (after OAuth is configured).",
        },
        {
            "name": "AMP - Content Refresh (daily 6am)",
            "url": f"{base_url}?mode=single&skill=longform-writer{auth}",
            "cron": "0 6 * * *",
            "purpose": "Daily content refresh check.",
        },
        {
            "name": "AMP - Hourly Heavy Batch (top of hour)",
            "url": f"{base_url}?mode=batch&limit=10{auth}",
            "cron": "0 * * * *",
            "purpose": "Hourly catch-up: processes up to 10 jobs to drain backlog.",
        },
    ]

    output = []
    output.append("=" * 78)
    output.append("  CRON-JOB.ORG SETUP — paste each URL below into a new cron job")
    output.append("=" * 78)
    output.append(f"\nBase URL: {base_url}")
    if secret:
        output.append(f"Secret:   {secret[:8]}...")
    else:
        output.append("Secret:   (none — public endpoint)")
    output.append("")

    for i, job in enumerate(jobs, 1):
        output.append(f"--- Job #{i}: {job['name']} ---")
        output.append(f"Purpose: {job['purpose']}")
        output.append(f"Cron:    {job['cron']}")
        output.append(f"URL:     {job['url']}")
        output.append("")

    output.append("=" * 78)
    output.append("  HOW TO SET UP IN CRON-JOB.ORG")
    output.append("=" * 78)
    output.append("""
1. Go to https://cron-job.org/en/members/jobs/
2. Click "Create cronjob"
3. For each job above:
   - Title: copy from "Job #N: ..."
   - URL: copy the full URL
   - Schedule: paste the cron expression (use https://crontab.guru to verify)
   - Notifications: enable failure emails
4. Save and verify the first run shows 200 OK in the logs

────────────────────────────────────────────────────────────────────
  WHY THIS WORKS (bypasses the Edge Function 8s/150s timeout)
────────────────────────────────────────────────────────────────────

The Supabase Edge Function has a default 8-second timeout (extendable
to 150s via config.toml). The strategy:

  BAD:  1 cron call  →  Edge Function processes 50 jobs  →  TIMES OUT
  GOOD: 50 cron calls  →  Edge Function processes 1 job each  →  DONE

With cron-job.org firing every 1 minute:
  - 60 calls/hour × 24 hours = 1,440 jobs/day capacity
  - Each call stays well under the 8s timeout (1 LLM call ≈ 5-7s)
  - If a job takes >8s, we have retry logic to mark it pending again
  - Heavy batches run hourly as backup catch-up

The hourly "?mode=batch&limit=10" provides:
  - Catch-up if queue has more than 1 job/min sustained
  - Multi-job processing during off-peak hours
  - A 10-job batch × 8s/job = 80s total, under the 150s cap
""")
    return "\n".join(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate cron-job.org URL list")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL,
                        help="Edge Function base URL")
    parser.add_argument("--secret", default=None,
                        help="Optional shared secret for webhook auth")
    args = parser.parse_args()

    print(generate_schedule(args.base_url, args.secret))