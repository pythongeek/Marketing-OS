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
    Execute a job by calling the appropriate agent skill via Minimax M3.
    """
    job_type = job.get("type", "")
    skill_slug = job.get("skill_slug", "")
    client_slug = job.get("client_slug", "")
    payload = job.get("payload", {})

    logger.info(f"Executing job {job['id']}: {job_type} / {skill_slug} / {client_slug}")

    # Build system prompt from skill context
    system_prompt = build_system_prompt(skill_slug, client_slug, payload)
    user_prompt = build_user_prompt(skill_slug, payload)

    # Call Minimax M3
    try:
        from api_client.minimax import generate_with_minimax
        from scripts.cost_tracker import CostTracker

        cost_tracker = CostTracker()

        result = generate_with_minimax(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=payload.get("temperature", 0.7),
            max_tokens=payload.get("max_tokens", 4096),
            model=Config.DEFAULT_LLM_MODEL,
        )

        content = result["content"]
        tokens_in = result["tokens_in"]
        tokens_out = result["tokens_out"]

        # Log cost
        cost_tracker.log_call(
            agent_name=skill_slug or job_type,
            provider="minimax",
            model=Config.DEFAULT_LLM_MODEL,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            call_type="completion",
            metadata={"job_id": job["id"], "client_slug": client_slug, "skill_slug": skill_slug},
        )

        return {
            "executed_at": datetime.utcnow().isoformat() + "Z",
            "job_type": job_type,
            "skill_slug": skill_slug,
            "client_slug": client_slug,
            "content": content,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "model": Config.DEFAULT_LLM_MODEL,
            "provider": "minimax",
            "message": f"Job {job_type} executed for {client_slug or 'agency'} via {skill_slug or 'manual'}",
        }

    except Exception as e:
        logger.error(f"Minimax execution failed: {e}")
        raise


def build_system_prompt(skill_slug: str, client_slug: str, payload: Dict) -> str:
    """Build a system prompt for the skill based on its slug."""
    prompts = {
        "content-strategist": "You are an expert content strategist for digital marketing agencies. You analyze business goals, target audiences, and competitive landscapes to produce comprehensive content strategies.",
        "on-page-optimizer": "You are an expert SEO on-page optimizer. You analyze content for keyword optimization, semantic richness, internal linking opportunities, and technical SEO improvements.",
        "technical-seo-auditor": "You are a senior technical SEO consultant. You audit websites for crawlability, indexability, Core Web Vitals, structured data, and technical issues.",
        "keyword-researcher": "You are an expert keyword researcher. You identify high-intent keywords, map them to funnel stages, and analyze search volume and competition.",
        "competitor-intelligence": "You are a competitive intelligence analyst. You analyze competitor strategies, content gaps, backlink profiles, and market positioning.",
        "aeo-geo-strategist": "You are an AI Engine Optimization (AEO) and Generative Engine Optimization (GEO) specialist. You optimize content for AI citations, featured snippets, and generative AI visibility.",
        "link-building-outreach": "You are a link building and digital PR specialist. You craft personalized outreach campaigns, identify link opportunities, and build relationships.",
        "pseo-pipeline": "You are a programmatic SEO expert. You design data-driven content generation pipelines, identify scalable keyword opportunities, and build content templates.",
        "content-brief-writer": "You are a content brief specialist. You create detailed, actionable briefs for writers that include SEO requirements, structure, tone, and key messages.",
        "copywriter": "You are an expert conversion copywriter. You write compelling headlines, ad copy, landing pages, and email sequences that drive action.",
        "social-media-manager": "You are a social media strategist. You plan content calendars, write engaging posts, and optimize for platform-specific algorithms.",
        "paid-ads-manager": "You are a performance marketing specialist. You create and optimize Google Ads, Meta Ads, and LinkedIn campaigns for maximum ROI.",
        "analytics-expert": "You are a marketing analytics expert. You analyze data, build dashboards, and provide actionable insights for marketing optimization.",
        "conversion-optimizer": "You are a CRO (Conversion Rate Optimization) specialist. You analyze user behavior, design A/B tests, and optimize conversion funnels.",
        "brand-voice-writer": "You are a brand voice specialist. You define and maintain consistent brand voice, tone, and messaging across all channels.",
        "email-marketing-specialist": "You are an email marketing expert. You design sequences, optimize deliverability, and maximize engagement and conversions.",
        "local-seo-manager": "You are a local SEO specialist. You optimize Google Business Profiles, local citations, and location-specific content.",
        "video-script-writer": "You are a video content strategist. You write scripts, plan storyboards, and optimize video content for SEO and engagement.",
        "reputation-manager": "You are a reputation management specialist. You monitor brand sentiment, manage reviews, and protect brand reputation.",
        "market-researcher": "You are a market research analyst. You analyze market trends, customer segments, and competitive landscapes.",
        "forecasting-revenue": "You are a revenue forecasting specialist. You build predictive models, analyze funnels, and project revenue growth.",
        "reporting-automation": "You are a reporting automation expert. You build automated dashboards, data pipelines, and executive summaries.",
        "playbook-creator": "You are a marketing operations specialist. You document SOPs, create playbooks, and standardize processes.",
        "off-page-optimizer": "You are an off-page SEO specialist. You build backlinks, manage brand mentions, and improve domain authority.",
        "agentic-marketing-os": "You are the master orchestrator of an AI-native marketing agency. You coordinate all agents, manage workflows, and ensure quality.",
    }

    base = prompts.get(skill_slug, "You are an expert marketing consultant. You provide high-quality, actionable marketing advice.")

    if client_slug:
        base += f"\n\nYou are working for client: {client_slug}. Adapt your output to their specific business context and goals."

    return base


def build_user_prompt(skill_slug: str, payload: Dict) -> str:
    """Build a user prompt from the job payload."""
    # Default: serialize the payload as instructions
    prompt_parts = [f"Task: {skill_slug}"]

    for key, value in payload.items():
        if key in ("temperature", "max_tokens", "model"):
            continue
        if isinstance(value, str) and value.strip():
            prompt_parts.append(f"{key}: {value}")
        elif isinstance(value, (list, dict)):
            prompt_parts.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")

    return "\n\n".join(prompt_parts)


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
