"""
Test suite: processors.py idempotency.
Run: python -m pytest tests/test_processors.py -v
"""

import json
import tempfile
from pathlib import Path

import pytest

import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "infrastructure"))

from ui.processors import process_client_onboarding


class TestClientOnboardingIdempotency:
    """Running client onboarding twice must not duplicate files/folders."""

    def test_onboarding_creates_expected_files(self):
        """First run creates client folder, profile, manifest, kpis, strategy."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from config import Config
            # Patch vault root for testing
            original_vault = Config.VAULT_ROOT
            Config.VAULT_ROOT = Path(tmpdir) / "vault"

            try:
                resp_path = Path(tmpdir) / "response.json"
                resp_path.write_text(json.dumps({
                    "client_name": "TestCo",
                    "website": "https://testco.com",
                    "industry": "SaaS",
                    "tier": "Growth ($4,500/mo)",
                    "business_goal_1": "Grow MRR",
                    "contact_name": "Alice",
                    "contact_email": "alice@testco.com",
                }), encoding="utf-8")

                result = process_client_onboarding(str(resp_path))
                assert result["status"] == "success"
                assert result["client"] == "TestCo"

                # Check files created
                client_dir = Path(result["folder"])
                assert client_dir.exists()
                assert (client_dir / "client-profile.md").exists()
                assert (client_dir / "website-manifest.md").exists()
                assert (client_dir / "kpis-and-goals.md").exists()
                assert (client_dir / "strategy-90-day.md").exists()
                assert (client_dir / "campaigns").is_dir()
                assert (client_dir / "competitors").is_dir()
            finally:
                Config.VAULT_ROOT = original_vault

    def test_onboarding_twice_does_not_duplicate(self):
        """Second run with same client must not create duplicate files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from config import Config
            original_vault = Config.VAULT_ROOT
            Config.VAULT_ROOT = Path(tmpdir) / "vault"

            try:
                resp_path = Path(tmpdir) / "response.json"
                resp_path.write_text(json.dumps({
                    "client_name": "TestCo",
                    "website": "https://testco.com",
                    "industry": "SaaS",
                    "tier": "Growth ($4,500/mo)",
                    "business_goal_1": "Grow MRR",
                    "contact_name": "Alice",
                    "contact_email": "alice@testco.com",
                }), encoding="utf-8")

                # First run
                result1 = process_client_onboarding(str(resp_path))
                folder1 = result1["folder"]
                files1 = set(Path(folder1).glob("*"))

                # Second run (same client)
                result2 = process_client_onboarding(str(resp_path))
                folder2 = result2["folder"]
                files2 = set(Path(folder2).glob("*"))

                # Same folder
                assert folder1 == folder2
                # Same file count (no duplicates)
                assert len(files1) == len(files2)
                # Profile should still be readable and have client name
                profile = Path(folder2) / "client-profile.md"
                content = profile.read_text(encoding="utf-8")
                assert "TestCo" in content
            finally:
                Config.VAULT_ROOT = original_vault

    def test_onboarding_different_clients_separate_folders(self):
        """Two different clients get separate folders."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from config import Config
            original_vault = Config.VAULT_ROOT
            Config.VAULT_ROOT = Path(tmpdir) / "vault"

            try:
                resp_a = Path(tmpdir) / "resp_a.json"
                resp_a.write_text(json.dumps({
                    "client_name": "Alpha Corp",
                    "website": "https://alpha.com",
                    "industry": "Fintech",
                    "tier": "Starter ($2,500/mo)",
                    "business_goal_1": "Goal A",
                    "contact_name": "Bob",
                    "contact_email": "bob@alpha.com",
                }), encoding="utf-8")

                resp_b = Path(tmpdir) / "resp_b.json"
                resp_b.write_text(json.dumps({
                    "client_name": "Beta Inc",
                    "website": "https://beta.com",
                    "industry": "E-commerce",
                    "tier": "Scale ($8,500/mo)",
                    "business_goal_1": "Goal B",
                    "contact_name": "Carol",
                    "contact_email": "carol@beta.com",
                }), encoding="utf-8")

                result_a = process_client_onboarding(str(resp_a))
                result_b = process_client_onboarding(str(resp_b))

                assert result_a["folder"] != result_b["folder"]
                assert "alpha-corp" in result_a["folder"].lower() or "alpha" in result_a["folder"].lower()
                assert "beta-inc" in result_b["folder"].lower() or "beta" in result_b["folder"].lower()
            finally:
                Config.VAULT_ROOT = original_vault

    def test_onboarding_missing_client_name_fails(self):
        """Missing client_name must return error, not create folder."""
        with tempfile.TemporaryDirectory() as tmpdir:
            from config import Config
            original_vault = Config.VAULT_ROOT
            Config.VAULT_ROOT = Path(tmpdir) / "vault"

            try:
                resp_path = Path(tmpdir) / "bad.json"
                resp_path.write_text(json.dumps({
                    "website": "https://example.com",
                    # missing client_name
                }), encoding="utf-8")

                result = process_client_onboarding(str(resp_path))
                assert result["status"] == "error"
                assert "client_name" in result["error"].lower()

                # No folder should be created
                vault_clients = Path(tmpdir) / "vault" / "01-Clients"
                if vault_clients.exists():
                    assert len(list(vault_clients.iterdir())) == 0
            finally:
                Config.VAULT_ROOT = original_vault


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
