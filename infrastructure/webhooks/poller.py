/**
 * AgenticMarketingPro — Kimi Work Job Poller
 * ============================================
 * Runs locally (on the Kimi Work machine) to poll Supabase for pending jobs,
 * execute them via the appropriate agent skill, and write results back.
 *
 * Usage:
 *   python infrastructure/webhooks/poller.py
 *   python infrastructure/webhooks/poller.py --once  # Single run, then exit
 *   python infrastructure/webhooks/poller.py --interval 300  # Poll every 5 min
 *
 * Setup:
 *   1. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
 *   2. Run this as a systemd service, cron job, or manually
 *   3. It will pick up jobs enqueued by the Vercel admin
 */

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.poller")


def get_supabase_client():
    """Initialize Supabase client from env vars."""
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
        return create_client(url, key)
    except ImportError:
        logger.error("supabase-py not installed. Run: pip install supabase")
        raise


def poll_pending_jobs(client) -> List[Dict[str, Any]]:
    """Fetch pending jobs from Supabase."""
    try:
        response = client.table("jobs").select("*").eq("status", "pending").order("created_at", desc=False).limit(10).execute()
        return response.data or []
    except Exception as e:
        logger.error(f"Failed to poll jobs: {e}")
        return []


def update_job_status(client, job_id: str, status: str, result: Dict = None, logs: List[str] = None, cost: float = 0, tokens_in: int = 0, tokens_out: int = 0):
    """Update job status and result in Supabase."""
    try:
        updates = {
            "status": status,
            "updated_at": datetime.utcnow().isoformat() + "Z",
        }
        if result is not None:
            updates["result"] = result
        if logs is not None:
            updates["logs"] = logs
        if cost:
            updates["cost_usd"] = cost
        if tokens_in:
            updates["tokens_in"] = tokens_in
        if tokens_out:
            updates["tokens_out"] = tokens_out
        if status == "running":
            updates["started_at"] = datetime.utcnow().isoformat() + "Z"
        if status in ("completed", "failed"):
            updates["completed_at"] = datetime.utcnow().isoformat() + "Z"

        client.table("jobs").update(updates).eq("id", job_id).execute()
        logger.info(f"Job {job_id} updated to {status}")
    except Exception as e:
        logger.error(f"Failed to update job {job_id}: {e}")


def log_event(client, job_id: str, level: str, message: str, metadata: Dict = None):
    """Write an agent log to Supabase."""
    try:
        client.table("agent_logs").insert({
            "job_id": job_id,
            "level": level,
            "message": message,
            "metadata": metadata or {},
            "created_at": datetime.utcnow().isoformat() + "Z",
        }).execute()
    except Exception as e:
        logger.error(f"Failed to write log: {e}")


def execute_job(job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a job by calling the appropriate agent skill.
    This is a stub — in production, this would import and run the actual skill.
    """
    job_type = job.get("type", "")
    skill_slug = job.get("skill_slug", "")
    client_slug = job.get("client_slug", "")
    payload = job.get("payload", {})

    logger.info(f"Executing job {job['id']}: {job_type} / {skill_slug} / {client_slug}")

    result = {
        "executed_at": datetime.utcnow().isoformat() + "Z",
        "job_type": job_type,
        "skill_slug": skill_slug,
        "client_slug": client_slug,
        "message": f"Job {job_type} executed for {client_slug or 'agency'} via {skill_slug or 'manual'}",
    }

    # TODO: Replace with actual skill execution
    # from skills import run_skill
    # result = run_skill(skill_slug, client_slug, payload)

    return result


def run_once(client):
    """Single polling cycle: fetch pending jobs, execute them, update status."""
    jobs = poll_pending_jobs(client)
    if not jobs:
        logger.info("No pending jobs")
        return 0

    logger.info(f"Found {len(jobs)} pending jobs")

    for job in jobs:
        job_id = job["id"]
        try:
            # Mark as running
            update_job_status(client, job_id, "running")
            log_event(client, job_id, "info", f"Job started: {job.get('type', 'unknown')}")

            # Execute
            result = execute_job(job)

            # Mark as completed
            update_job_status(client, job_id, "completed", result=result)
            log_event(client, job_id, "success", f"Job completed: {result.get('message', '')}")

        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            update_job_status(client, job_id, "failed", result={"error": str(e)})
            log_event(client, job_id, "error", f"Job failed: {str(e)}")

    return len(jobs)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AgenticMarketingPro Job Poller")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--interval", type=int, default=300, help="Polling interval in seconds (default: 300 = 5 min)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    )

    logger.info("=" * 60)
    logger.info("AgenticMarketingPro — Job Poller")
    logger.info("=" * 60)

    try:
        client = get_supabase_client()
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}")
        return 1

    if args.once:
        count = run_once(client)
        logger.info(f"Processed {count} jobs. Exiting.")
        return 0

    # Continuous loop
    logger.info(f"Starting continuous polling every {args.interval}s")
    logger.info("Press Ctrl+C to stop")

    while True:
        try:
            count = run_once(client)
            if count == 0:
                time.sleep(args.interval)
            else:
                # Brief pause between job batches
                time.sleep(5)
        except KeyboardInterrupt:
            logger.info("Poller stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error in polling loop: {e}")
            time.sleep(args.interval)

    return 0


if __name__ == "__main__":
    sys.exit(main())
