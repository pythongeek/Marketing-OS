"""
AgenticMarketingPro — Kimi Work Job Poller
============================================
Runs locally (on the Kimi Work machine) to poll Supabase for pending jobs,
execute them via the appropriate agent skill, and write results back.

Skills are resolved in this order:
  1. Supabase `skills` table (instructions column)
  2. Vault `skills/<slug>/SKILL.md` (fallback)
  3. Generic marketing consultant (last resort)

RAG context from the vault is injected into every system prompt.

Usage:
  python infrastructure/webhooks/poller.py
  python infrastructure/webhooks/poller.py --once  # Single run, then exit
  python infrastructure/webhooks/poller.py --interval 300  # Poll every 5 min

Setup:
  1. Set SUPABASE_URL and SUPABASE_SERVICE_KEY in .env
  2. Run this as a systemd service, cron job, or manually
  3. It will pick up jobs enqueued by the Vercel admin
"""

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

# ── Skill resolution cache ──────────────────────────────────────────
_skill_cache: Dict[str, str] = {}


def get_supabase_client():
    """Initialize Supabase client from env vars."""
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set")
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


# ── Skill resolution ────────────────────────────────────────────────

def load_skill_from_supabase(client, skill_slug: str) -> str:
    """Fetch skill instructions from Supabase skills table."""
    try:
        response = client.table("skills").select("instructions").eq("slug", skill_slug).limit(1).execute()
        if response.data and response.data[0].get("instructions"):
            return response.data[0]["instructions"]
    except Exception as e:
        logger.warning(f"Failed to load skill from Supabase: {e}")
    return ""


def load_skill_from_vault(skill_slug: str) -> str:
    """Fetch skill instructions from vault SKILL.md file."""
    skill_path = Path(Config.VAULT_ROOT).parent / "skills" / skill_slug / "SKILL.md"
    if not skill_path.exists():
        # Also check relative to repo root
        skill_path = Path(__file__).parent.parent.parent / "skills" / skill_slug / "SKILL.md"
    try:
        if skill_path.exists():
            text = skill_path.read_text(encoding="utf-8")
            # Strip YAML frontmatter if present
            if text.startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    return parts[2].strip()
            return text.strip()
    except Exception as e:
        logger.warning(f"Failed to load skill from vault: {e}")
    return ""


def resolve_skill_instructions(client, skill_slug: str) -> str:
    """Resolve skill instructions: cache → Supabase → vault → generic."""
    if skill_slug in _skill_cache:
        return _skill_cache[skill_slug]

    # 1. Try Supabase
    instructions = load_skill_from_supabase(client, skill_slug)
    source = "supabase"

    # 2. Fallback to vault SKILL.md
    if not instructions:
        instructions = load_skill_from_vault(skill_slug)
        source = "vault"

    # 3. Last resort generic
    if not instructions:
        instructions = (
            "You are an expert marketing consultant. You provide high-quality, "
            "actionable marketing advice."
        )
        source = "generic"

    _skill_cache[skill_slug] = instructions
    logger.info(f"Resolved skill '{skill_slug}' from {source} ({len(instructions)} chars)")
    return instructions


# ── RAG context injection ───────────────────────────────────────────

def fetch_rag_context(skill_slug: str, client_slug: str, query: str = "") -> str:
    """Query VaultRAG for relevant context and return as a formatted block."""
    try:
        from rag.pipeline import VaultRAG

        rag = VaultRAG()
        # Build a contextual query
        q = query or f"Best practices and context for {skill_slug}"
        if client_slug:
            q += f" for client {client_slug}"

        results = rag.query(
            query_text=q,
            top_k=5,
            source_type=None,  # Allow any source type
        )

        if not results:
            return ""

        context_parts = ["## Relevant Context from Vault\n"]
        for i, r in enumerate(results, 1):
            meta = r.get("metadata", {})
            source = meta.get("source_path", "unknown")
            section = meta.get("section", "")
            title = meta.get("title", "")
            text = r.get("text", "")
            # Truncate very long chunks
            if len(text) > 2000:
                text = text[:2000] + "\n...[truncated]"
            context_parts.append(
                f"### Context {i}: {title} — {section}\n"
                f"*Source: {source}*\n\n{text}\n"
            )

        return "\n".join(context_parts)

    except Exception as e:
        logger.warning(f"RAG context fetch failed: {e}")
        return ""


# ── Prompt builders ─────────────────────────────────────────────────

def build_system_prompt(client, skill_slug: str, client_slug: str, payload: Dict) -> str:
    """Build a system prompt from skill instructions + RAG context."""
    base = resolve_skill_instructions(client, skill_slug)

    # Inject RAG context
    rag_context = fetch_rag_context(skill_slug, client_slug)
    if rag_context:
        base += f"\n\n{rag_context}"

    if client_slug:
        base += (
            f"\n\nYou are working for client: {client_slug}. "
            f"Adapt your output to their specific business context and goals."
        )

    return base


def build_user_prompt(skill_slug: str, payload: Dict) -> str:
    """Build a user prompt from the job payload."""
    prompt_parts = [f"Task: {skill_slug}"]

    for key, value in payload.items():
        if key in ("temperature", "max_tokens", "model"):
            continue
        if isinstance(value, str) and value.strip():
            prompt_parts.append(f"{key}: {value}")
        elif isinstance(value, (list, dict)):
            prompt_parts.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")

    return "\n\n".join(prompt_parts)


# ── Job execution ───────────────────────────────────────────────────

def execute_job(client, job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a job by calling the appropriate agent skill via Minimax M3.
    """
    job_type = job.get("type", "")
    skill_slug = job.get("skill_slug", "")
    client_slug = job.get("client_slug", "")
    payload = job.get("payload", {})

    logger.info(f"Executing job {job['id']}: {job_type} / {skill_slug} / {client_slug}")

    # Build system prompt from skill context + RAG
    system_prompt = build_system_prompt(client, skill_slug, client_slug, payload)
    user_prompt = build_user_prompt(skill_slug, payload)

    # Call Minimax M3
    try:
        from api_client.minimax import generate_with_minimax
        from scripts.cost_tracker import CostTracker

        cost_tracker = CostTracker()

        result = generate_with_minimax(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=payload.get("temperature", 1.0),
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


# ── Polling loop ────────────────────────────────────────────────────

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
            result = execute_job(client, job)

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
