"""
AgenticMarketingPro — Cost Tracking & Budget Enforcement
=========================================================
Tracks every API call's cost, enforces daily/monthly budgets, and logs to vault.

Usage:
    from scripts.cost_tracker import CostTracker
    tracker = CostTracker()
    tracker.log_call("openai", "gpt-4", tokens_in=1000, tokens_out=500)
    tracker.check_budget()  # Raises if exceeded

The log file is JSONL at: AgenticMarketingPro-Vault/11-Ops/agent-logs/cost-tracker.jsonl
"""

import json
import logging
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, Optional
from dataclasses import dataclass, asdict

from config import Config

logger = logging.getLogger("amp.cost")


# Cost per 1K tokens (USD) — update as models/pricing change
MODEL_COSTS = {
    # Minimax M3 (Primary)
    "MiniMax-M3": {"input": 0.0015, "output": 0.0015},
    "MiniMax-Text-01": {"input": 0.0015, "output": 0.0015},
    "minimax-m3": {"input": 0.0015, "output": 0.0015},
    # OpenAI (Fallback)
    "gpt-4": {"input": 0.03, "output": 0.06},
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
    "text-embedding-3-small": {"input": 0.00002, "output": 0.0},
    "text-embedding-3-large": {"input": 0.00013, "output": 0.0},
    # Hermes Agent Desktop (default model)
    # Legacy Minimax
    "minimax-abab5.5": {"input": 0.0015, "output": 0.0015},
}


@dataclass
class CostEntry:
    """A single cost log entry."""
    timestamp: str  # ISO format
    agent_name: str
    provider: str  # openai, anthropic, hermes_agent, etc.
    model: str
    tokens_in: int
    tokens_out: int
    cost_usd: float
    call_type: str  # "completion", "embedding", "image", "function"
    metadata: Dict


class CostTracker:
    """Tracks and enforces API costs."""

    def __init__(self, log_path: Path = None):
        self.log_path = log_path or Config.COST_LOG
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.daily_budget = Config.LLM_DAILY_BUDGET_USD
        self.monthly_budget = Config.LLM_MONTHLY_BUDGET_USD

    def _estimate_cost(self, provider: str, model: str, tokens_in: int, tokens_out: int) -> float:
        """Estimate cost in USD."""
        costs = MODEL_COSTS.get(model)
        if not costs:
            # Fallback: generic pricing
            logger.warning(f"Unknown model {model}, using generic pricing")
            costs = {"input": 0.01, "output": 0.03}

        in_cost = (tokens_in / 1000) * costs["input"]
        out_cost = (tokens_out / 1000) * costs["output"]
        return round(in_cost + out_cost, 6)

    def log_call(
        self,
        agent_name: str,
        provider: str,
        model: str,
        tokens_in: int = 0,
        tokens_out: int = 0,
        call_type: str = "completion",
        metadata: Dict = None,
    ) -> CostEntry:
        """Log a single API call and its cost."""
        cost = self._estimate_cost(provider, model, tokens_in, tokens_out)
        
        entry = CostEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            agent_name=agent_name,
            provider=provider,
            model=model,
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            cost_usd=cost,
            call_type=call_type,
            metadata=metadata or {},
        )

        # Append to JSONL
        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(entry)) + "\n")

        logger.info(
            f"[{agent_name}] {provider}/{model}: ${cost:.6f} "
            f"({tokens_in} in + {tokens_out} out tokens)"
        )
        return entry

    def get_spending(self, days: int = 1) -> Dict[str, float]:
        """Get spending summary for the last N days."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        
        total = 0.0
        by_agent: Dict[str, float] = {}
        by_provider: Dict[str, float] = {}
        by_model: Dict[str, float] = {}

        if not self.log_path.exists():
            return {
                "total": 0.0,
                "by_agent": {},
                "by_provider": {},
                "by_model": {},
                "call_count": 0,
            }

        with open(self.log_path, "r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                    entry_time = datetime.fromisoformat(entry["timestamp"].replace("Z", "+00:00"))
                    if entry_time < cutoff:
                        continue
                    
                    cost = entry["cost_usd"]
                    total += cost
                    by_agent[entry["agent_name"]] = by_agent.get(entry["agent_name"], 0) + cost
                    by_provider[entry["provider"]] = by_provider.get(entry["provider"], 0) + cost
                    by_model[entry["model"]] = by_model.get(entry["model"], 0) + cost
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

        return {
            "total": round(total, 6),
            "by_agent": {k: round(v, 6) for k, v in by_agent.items()},
            "by_provider": {k: round(v, 6) for k, v in by_provider.items()},
            "by_model": {k: round(v, 6) for k, v in by_model.items()},
            "call_count": sum(len(v) for v in [by_agent]),
        }

    def check_budget(self, agent_name: str = "global") -> Dict[str, any]:
        """
        Check if budget is exceeded. Returns status dict.
        Raises BudgetExceeded if hard limit hit.
        """
        today_spending = self.get_spending(days=1)["total"]
        month_spending = self.get_spending(days=30)["total"]

        status = {
            "agent": agent_name,
            "daily_spent": round(today_spending, 4),
            "daily_budget": self.daily_budget,
            "daily_remaining": round(self.daily_budget - today_spending, 4),
            "daily_pct": round(today_spending / self.daily_budget * 100, 2) if self.daily_budget else 0,
            "monthly_spent": round(month_spending, 4),
            "monthly_budget": self.monthly_budget,
            "monthly_remaining": round(self.monthly_budget - month_spending, 4),
            "monthly_pct": round(month_spending / self.monthly_budget * 100, 2) if self.monthly_budget else 0,
            "throttle": False,
            "pause": False,
        }

        # Throttle at 80% of daily budget
        if status["daily_pct"] >= 80:
            status["throttle"] = True
            logger.warning(f"[{agent_name}] Daily budget at {status['daily_pct']}% — throttling")

        # Pause at 100% of daily budget
        if status["daily_pct"] >= 100:
            status["pause"] = True
            logger.error(f"[{agent_name}] Daily budget EXCEEDED (${today_spending:.4f} / ${self.daily_budget:.4f})")

        # Monthly check
        if status["monthly_pct"] >= 100:
            status["pause"] = True
            logger.error(f"[{agent_name}] Monthly budget EXCEEDED (${month_spending:.4f} / ${self.monthly_budget:.4f})")

        return status

    def enforce_budget(self, agent_name: str = "global"):
        """Enforce budget — raise if exceeded."""
        status = self.check_budget(agent_name)
        if status["pause"]:
            raise BudgetExceeded(
                f"Budget exceeded for {agent_name}. Daily: ${status['daily_spent']:.4f}/${self.daily_budget:.4f}, "
                f"Monthly: ${status['monthly_spent']:.4f}/${self.monthly_budget:.4f}"
            )
        return status

    def daily_report(self) -> Dict:
        """Generate a daily cost report for vault write-back."""
        spending = self.get_spending(days=1)
        status = self.check_budget()
        
        return {
            "date": date.today().isoformat(),
            "total_spent_today": spending["total"],
            "daily_budget": self.daily_budget,
            "daily_remaining": status["daily_remaining"],
            "daily_pct_used": status["daily_pct"],
            "monthly_spent": status["monthly_spent"],
            "monthly_budget": self.monthly_budget,
            "monthly_remaining": status["monthly_remaining"],
            "monthly_pct_used": status["monthly_pct"],
            "by_agent": spending["by_agent"],
            "by_provider": spending["by_provider"],
            "by_model": spending["by_model"],
            "throttle_active": status["throttle"],
            "paused": status["pause"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }


class BudgetExceeded(Exception):
    """Raised when budget is exceeded."""
    pass


if __name__ == "__main__":
    # Demo usage
    tracker = CostTracker()
    
    # Log a few example calls with Minimax M3
    tracker.log_call("content-strategist", "minimax", "MiniMax-M3", tokens_in=2000, tokens_out=800)
    tracker.log_call("on-page-optimizer", "minimax", "MiniMax-M3", tokens_in=1500, tokens_out=500)
    tracker.log_call("analytics-expert", "openai", "text-embedding-3-small", tokens_in=1000, tokens_out=0, call_type="embedding")
    
    print("Daily spending:", tracker.get_spending(days=1))
    print("Budget status:", tracker.check_budget())
    print("Daily report:", tracker.daily_report())
