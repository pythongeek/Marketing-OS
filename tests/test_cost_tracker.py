"""
Test suite: cost_tracker math, budget enforcement, logging correctness.
Run: python -m pytest tests/test_cost_tracker.py -v
"""

import json
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import pytest

# Ensure repo root is on path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "infrastructure"))

from scripts.cost_tracker import CostTracker, BudgetExceeded, MODEL_COSTS


class TestCostTrackerMath:
    """Cost estimation must be mathematically correct."""

    def test_minimax_m3_pricing(self):
        """MiniMax M3: $0.0015 per 1K tokens in + out."""
        tracker = CostTracker()
        cost = tracker._estimate_cost("minimax", "MiniMax-M3", 2000, 800)
        expected = (2000 / 1000) * 0.0015 + (800 / 1000) * 0.0015
        assert cost == pytest.approx(expected, rel=1e-6)
        assert cost == pytest.approx(0.0042, rel=1e-6)

    def test_openai_gpt4o_pricing(self):
        """GPT-4o: $0.005 in, $0.015 out per 1K tokens."""
        tracker = CostTracker()
        cost = tracker._estimate_cost("openai", "gpt-4o", 1000, 500)
        expected = (1000 / 1000) * 0.005 + (500 / 1000) * 0.015
        assert cost == pytest.approx(expected, rel=1e-6)

    def test_unknown_model_fallback(self):
        """Unknown model uses generic pricing."""
        tracker = CostTracker()
        cost = tracker._estimate_cost("unknown", "some-model", 1000, 1000)
        expected = (1000 / 1000) * 0.01 + (1000 / 1000) * 0.03
        assert cost == pytest.approx(expected, rel=1e-6)

    def test_zero_tokens(self):
        """Zero tokens = zero cost."""
        tracker = CostTracker()
        cost = tracker._estimate_cost("minimax", "MiniMax-M3", 0, 0)
        assert cost == 0.0

    def test_embedding_no_output_cost(self):
        """Embeddings have no output cost."""
        tracker = CostTracker()
        cost = tracker._estimate_cost("openai", "text-embedding-3-small", 1000, 0)
        expected = (1000 / 1000) * 0.00002
        assert cost == pytest.approx(expected, rel=1e-6)


class TestBudgetEnforcement:
    """Budget enforcement must block when exceeded."""

    def test_budget_not_exceeded_allows(self):
        """When under budget, enforce_budget returns status."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "cost.jsonl"
            tracker = CostTracker(log_path=log_path)
            tracker.daily_budget = 10.0
            tracker.monthly_budget = 100.0
            status = tracker.enforce_budget("test-agent")
            assert status["pause"] is False
            assert status["throttle"] is False

    def test_daily_budget_exceeded_raises(self):
        """When daily budget exceeded, enforce_budget raises BudgetExceeded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "cost.jsonl"
            tracker = CostTracker(log_path=log_path)
            tracker.daily_budget = 0.01
            tracker.monthly_budget = 100.0
            # Log a call that exceeds daily budget
            tracker.log_call("test", "minimax", "MiniMax-M3", tokens_in=10000, tokens_out=5000)
            with pytest.raises(BudgetExceeded):
                tracker.enforce_budget("test-agent")

    def test_throttle_at_80_percent(self):
        """At 80% of daily budget, throttle flag is True but pause is False."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "cost.jsonl"
            tracker = CostTracker(log_path=log_path)
            tracker.daily_budget = 1.0
            tracker.monthly_budget = 100.0
            # Log a call at ~85% of budget
            tracker.log_call("test", "minimax", "MiniMax-M3", tokens_in=600, tokens_out=0)
            status = tracker.check_budget("test-agent")
            assert status["throttle"] is True
            assert status["pause"] is False


class TestSpendingAggregation:
    """Spending aggregation must be correct across time windows."""

    def test_daily_spending_aggregation(self):
        """get_spending(days=1) sums today's costs correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "cost.jsonl"
            tracker = CostTracker(log_path=log_path)
            tracker.log_call("a", "minimax", "MiniMax-M3", tokens_in=1000, tokens_out=0)
            tracker.log_call("b", "minimax", "MiniMax-M3", tokens_in=2000, tokens_out=0)
            spending = tracker.get_spending(days=1)
            expected = (3000 / 1000) * 0.0015
            assert spending["total"] == pytest.approx(expected, rel=1e-6)
            assert spending["by_agent"]["a"] == pytest.approx((1000 / 1000) * 0.0015, rel=1e-6)
            assert spending["by_agent"]["b"] == pytest.approx((2000 / 1000) * 0.0015, rel=1e-6)

    def test_old_entries_excluded(self):
        """Entries older than the window are excluded."""
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / "cost.jsonl"
            tracker = CostTracker(log_path=log_path)
            # Manually write an old entry
            old_entry = {
                "timestamp": (datetime.utcnow() - timedelta(days=2)).isoformat() + "Z",
                "agent_name": "old",
                "provider": "minimax",
                "model": "MiniMax-M3",
                "tokens_in": 100000,
                "tokens_out": 0,
                "cost_usd": 0.15,
                "call_type": "completion",
                "metadata": {},
            }
            with open(log_path, "a") as f:
                f.write(json.dumps(old_entry) + "\n")
            # And a fresh entry
            tracker.log_call("new", "minimax", "MiniMax-M3", tokens_in=1000, tokens_out=0)
            spending = tracker.get_spending(days=1)
            assert "old" not in spending["by_agent"]
            assert "new" in spending["by_agent"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
