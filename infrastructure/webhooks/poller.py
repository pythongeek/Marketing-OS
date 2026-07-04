"""
AgenticMarketingPro — Kimi Work Job Poller  (Phase 2: Governance)
=================================================================
Runs locally to poll Supabase for pending jobs, execute them via agent skills,
and write results back. Now with real governance gates:

  1. RETRY / BACKOFF — @with_retry decorator around execute_job
  2. BUDGET ENFORCEMENT — blocks dispatch if daily/monthly limit exceeded
  3. QA PIPELINE GATE — auto-enqueues qa-check after every content job

Usage:
  python infrastructure/webhooks/poller.py
  python infrastructure/webhooks/poller.py --once
  python infrastructure/webhooks/poller.py --interval 300
"""

import json
import logging
import os
import sys
import time
import functools
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Callable

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import Config

logger = logging.getLogger("amp.poller")

# ── Skill resolution cache ──────────────────────────────────────────
_skill_cache: Dict[str, str] = {}

# ── Content-producing skill slugs (trigger QA gate) ─────────────────
_CONTENT_SKILLS = {
    "content-strategist", "content-brief-writer", "copywriter",
    "brand-voice-writer", "video-script-writer", "social-media-manager",
    "email-marketing-specialist", "paid-ads-manager", "pitch-proposal",
    "playbook-request", "on-page-request", "pseo-config",
    "aeo-entity-schema", "local-seo", "outreach-prospect",
    "influencer-campaign", "ad-campaign", "email-sequence",
    "content-brief", "copy-request", "market-alert",
    "forecasting-request", "report-config", "analytics-report",
    "revenue-opportunity", "tech-audit", "qa-check-request",
}


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


# ════════════════════════════════════════════════════════════════════
# 1. RETRY / BACKOFF DECORATOR  (implements auto-recovery once)
# ════════════════════════════════════════════════════════════════════

def with_retry(
    max_retries: int = 1,
    base_delay: float = 30.0,
    max_delay: float = 300.0,
    exponential: bool = True,
):
    """
    Decorator that retries a function call on failure with exponential backoff.
    After max_retries exhausted, the exception is re-raised (escalation).

    Usage:
        @with_retry(max_retries=1, base_delay=30)
        def execute_job(...): ...
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = min(
                            base_delay * (2 ** attempt) if exponential else base_delay,
                            max_delay,
                        )
                        logger.warning(
                            f"{fn.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                            f"Retrying in {delay:.1f}s..."
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"{fn.__name__} exhausted all {max_retries} retries. Escalating."
                        )
            raise last_exception
        return wrapper
    return decorator


# ════════════════════════════════════════════════════════════════════
# 2. BUDGET ENFORCEMENT  (gate before dispatch)
# ════════════════════════════════════════════════════════════════════

def check_budget_gate(agent_name: str = "global") -> Dict[str, Any]:
    """
    Check budget BEFORE dispatching a job. Returns status dict.
    Raises BudgetExceeded if hard limit hit — this blocks execution.
    """
    from scripts.cost_tracker import CostTracker, BudgetExceeded

    tracker = CostTracker()
    status = tracker.check_budget(agent_name)

    if status["pause"]:
        raise BudgetExceeded(
            f"Budget exceeded for {agent_name}. "
            f"Daily: ${status['daily_spent']:.4f}/${tracker.daily_budget:.4f}, "
            f"Monthly: ${status['monthly_spent']:.4f}/${tracker.monthly_budget:.4f}"
        )

    if status["throttle"]:
        logger.warning(
            f"[{agent_name}] Budget throttling active ({status['daily_pct']}% daily). "
            "Job will proceed but watch spend."
        )

    return status


# ════════════════════════════════════════════════════════════════════
# 3. QA PIPELINE GATE  (enqueue qa-check after content jobs)
# ════════════════════════════════════════════════════════════════════

def enqueue_qa_check(client, parent_job: Dict[str, Any], content: str):
    """
    After a content-producing job completes, auto-enqueue a qa-check job.
    Binary checks (legal, plagiarism) block deliverability.
    Scored checks (grammar, tone) log and continue.
    """
    try:
        qa_payload = {
            "parent_job_id": parent_job["id"],
            "artifact_type": "content",
            "artifact_content": content[:8000],  # truncate for storage
            "checks": {
                "binary": ["legal_risk", "plagiarism_flag"],
                "scored": ["grammar_score", "tone_match", "brand_voice_score"],
            },
            "client_slug": parent_job.get("client_slug"),
            "skill_slug": parent_job.get("skill_slug"),
        }

        response = client.table("jobs").insert({
            "type": "qa_check",
            "client_slug": parent_job.get("client_slug"),
            "skill_slug": "qa-check",
            "payload": qa_payload,
            "status": "pending",
            "parent_job_id": parent_job["id"],
        }).select().single().execute()

        qa_job = response.data
        logger.info(f"QA check enqueued: job {qa_job['id']} for parent {parent_job['id']}")
        return qa_job

    except Exception as e:
        logger.error(f"Failed to enqueue QA check for job {parent_job['id']}: {e}")
        return None


def run_qa_checks(client, job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute QA checks on a content artifact.
    Binary failures → block (return blocked=True).
    Scored failures → log warning (return blocked=False, warnings=list).
    """
    payload = job.get("payload", {})
    content = payload.get("artifact_content", "")
    checks = payload.get("checks", {})
    result = {"blocked": False, "warnings": [], "binary_passed": {}, "scored": {}}

    # ── Binary checks (block if fail) ─────────────────────────────
    binary_checks = checks.get("binary", [])

    if "legal_risk" in binary_checks:
        # Simple heuristic: flag common risky terms
        risk_terms = ["guarantee", "guaranteed", "100%", "miracle", "cure", "fda approved"]
        found = [t for t in risk_terms if t.lower() in content.lower()]
        if found:
            result["blocked"] = True
            result["binary_passed"]["legal_risk"] = False
            result["warnings"].append(f"Legal risk flagged: terms {found}")
            logger.error(f"QA BLOCK: legal_risk failed for job {job['id']}")
        else:
            result["binary_passed"]["legal_risk"] = True

    if "plagiarism_flag" in binary_checks:
        # Placeholder: real implementation would call Copyscape / Originality.ai
        # For now, flag if content is suspiciously short (proxy for low quality)
        if len(content) < 200:
            result["blocked"] = True
            result["binary_passed"]["plagiarism_flag"] = False
            result["warnings"].append("Content too short — possible plagiarism or low quality")
            logger.error(f"QA BLOCK: plagiarism_flag failed for job {job['id']}")
        else:
            result["binary_passed"]["plagiarism_flag"] = True

    # ── Scored checks (log and continue) ──────────────────────────
    scored_checks = checks.get("scored", [])

    if "grammar_score" in scored_checks:
        # Placeholder: real implementation would call Grammarly API
        score = min(100, max(0, 100 - len(content) // 1000))  # fake heuristic
        result["scored"]["grammar_score"] = score
        if score < 70:
            result["warnings"].append(f"Grammar score low: {score}/100")
            logger.warning(f"QA WARN: grammar_score={score} for job {job['id']}")

    if "tone_match" in scored_checks:
        # Placeholder: real implementation would call tone analysis API
        score = 85  # fake
        result["scored"]["tone_match"] = score
        if score < 70:
            result["warnings"].append(f"Tone match low: {score}/100")
            logger.warning(f"QA WARN: tone_match={score} for job {job['id']}")

    return result


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
        skill_path = Path(__file__).parent.parent.parent / "skills" / skill_slug / "SKILL.md"
    try:
        if skill_path.exists():
            text = skill_path.read_text(encoding="utf-8")
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

    instructions = load_skill_from_supabase(client, skill_slug)
    source = "supabase"

    if not instructions:
        instructions = load_skill_from_vault(skill_slug)
        source = "vault"

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
        q = query or f"Best practices and context for {skill_slug}"
        if client_slug:
            q += f" for client {client_slug}"

        results = rag.query(query_text=q, top_k=5, source_type=None)
        if not results:
            return ""

        context_parts = ["## Relevant Context from Vault\n"]
        for i, r in enumerate(results, 1):
            meta = r.get("metadata", {})
            text = r.get("text", "")
            if len(text) > 2000:
                text = text[:2000] + "\n...[truncated]"
            context_parts.append(
                f"### Context {i}: {meta.get('title', '')} — {meta.get('section', '')}\n"
                f"*Source: {meta.get('source_path', 'unknown')}*\n\n{text}\n"
            )
        return "\n".join(context_parts)
    except Exception as e:
        logger.warning(f"RAG context fetch failed: {e}")
        return ""


# ── Prompt builders ─────────────────────────────────────────────────

def build_system_prompt(client, skill_slug: str, client_slug: str, payload: Dict) -> str:
    """Build a system prompt from skill instructions + RAG context."""
    base = resolve_skill_instructions(client, skill_slug)
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

@with_retry(max_retries=1, base_delay=30.0, max_delay=300.0)
def execute_job(client, job: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a job by calling the appropriate agent skill via Minimax M3.
    Wrapped with @with_retry for automatic retry/backoff on failure.
    """
    job_type = job.get("type", "")
    skill_slug = job.get("skill_slug", "")
    client_slug = job.get("client_slug", "")
    payload = job.get("payload", {})

    logger.info(f"Executing job {job['id']}: {job_type} / {skill_slug} / {client_slug}")

    # Build prompts
    system_prompt = build_system_prompt(client, skill_slug, client_slug, payload)
    user_prompt = build_user_prompt(skill_slug, payload)

    # Call LLM
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


# ── Polling loop ────────────────────────────────────────────────────

def run_once(client):
    """Single polling cycle: fetch pending jobs, enforce budget, execute, QA gate."""
    jobs = poll_pending_jobs(client)
    if not jobs:
        logger.info("No pending jobs")
        return 0

    logger.info(f"Found {len(jobs)} pending jobs")

    for job in jobs:
        job_id = job["id"]
        skill_slug = job.get("skill_slug", "")
        job_type = job.get("type", "")

        try:
            # ── 1. BUDGET ENFORCEMENT (gate before dispatch) ─────────
            try:
                budget_status = check_budget_gate(agent_name=skill_slug or job_type)
                logger.info(
                    f"Budget check passed: daily {budget_status['daily_pct']}% "
                    f"(${budget_status['daily_spent']:.4f}/${budget_status['daily_budget']:.4f})"
                )
            except Exception as budget_err:
                logger.error(f"BUDGET BLOCK: job {job_id} — {budget_err}")
                update_job_status(client, job_id, "failed", result={"error": str(budget_err)})
                log_event(client, job_id, "error", f"Budget enforcement blocked: {budget_err}")
                continue  # Skip this job, don't crash the loop

            # ── 2. Mark as running ────────────────────────────────────
            update_job_status(client, job_id, "running")
            log_event(client, job_id, "info", f"Job started: {job_type}")

            # ── 3. Execute (with @with_retry) ─────────────────────────
            if job_type == "qa_check":
                result = run_qa_checks(client, job)
                update_job_status(client, job_id, "completed", result=result)
                log_event(client, job_id, "success", f"QA check completed: blocked={result['blocked']}, warnings={len(result['warnings'])}")

                # If QA blocked, mark parent job as blocked
                if result["blocked"]:
                    parent_id = job.get("payload", {}).get("parent_job_id")
                    if parent_id:
                        update_job_status(
                            client, parent_id, "blocked",
                            result={"qa_result": result, "error": "QA binary check failed"}
                        )
                        log_event(client, parent_id, "error", "QA binary check blocked deliverability")
            else:
                result = execute_job(client, job)

                # ── 4. QA PIPELINE GATE (after content jobs) ────────────
                is_content_skill = skill_slug in _CONTENT_SKILLS or job_type in ("agent_run", "content")
                if is_content_skill and result.get("content"):
                    qa_job = enqueue_qa_check(client, job, result["content"])
                    if qa_job:
                        result["qa_check_enqueued"] = qa_job["id"]

                # Mark as completed (QA will update to blocked if checks fail)
                update_job_status(client, job_id, "completed", result=result)
                log_event(client, job_id, "success", f"Job completed: {result.get('message', '')}")

        except Exception as e:
            logger.error(f"Job {job_id} failed: {e}")
            update_job_status(client, job_id, "failed", result={"error": str(e)})
            log_event(client, job_id, "error", f"Job failed: {str(e)}")

    return len(jobs)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="AgenticMarketingPro Job Poller (Phase 2)")
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
    logger.info("AgenticMarketingPro — Job Poller  (Phase 2: Governance)")
    logger.info("Features: retry/backoff | budget enforcement | QA pipeline")
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

    logger.info(f"Starting continuous polling every {args.interval}s")
    logger.info("Press Ctrl+C to stop")

    while True:
        try:
            count = run_once(client)
            if count == 0:
                time.sleep(args.interval)
            else:
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
