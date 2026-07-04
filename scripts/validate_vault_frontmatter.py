#!/usr/bin/env python3
"""
Vault Frontmatter Validator
============================
Validates every .md file in the vault against frontmatter-standards.md.
Called by CI on every PR. Returns non-zero if any file fails.

Usage:
    python scripts/validate_vault_frontmatter.py [vault_path]

Checks:
  - YAML frontmatter present and parseable
  - Required fields: type, last_updated, tags
  - type exists in type registry
  - last_updated is valid YYYY-MM-DD
  - tags is a list (even if empty)
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple

# ── Type registry from frontmatter-standards.md ────────────────────
TYPE_REGISTRY: Dict[str, List[str]] = {
    "agency-core": ["title"],
    "client": ["client", "industry", "tier", "mrr", "status", "strategist"],
    "client-onboarding": ["client", "status"],
    "client-kpis": ["client", "status"],
    "client-strategy": ["client", "status"],
    "client-campaign-log": ["client", "status"],
    "competitor-map": [],
    "competitor-keyword-gaps": ["competitor"],
    "competitor-backlinks": ["competitor"],
    "competitor-content": ["competitor"],
    "competitor-paid": ["competitor"],
    "competitor-team": ["competitor"],
    "keyword-universe": [],
    "topic-clusters": [],
    "gsc-log": [],
    "bing-log": [],
    "audit-log": [],
    "content-calendar": [],
    "content-brief": ["client", "title", "slug", "content_type", "target_keyword", "writer_persona", "due_date", "status", "qa_status"],
    "published-index": [],
    "content-retrospective": [],
    "writer-persona": ["persona"],
    "pseo-data": [],
    "pseo-guardrails": [],
    "pseo-log": [],
    "aeo-tracker": [],
    "entity-registry": [],
    "llm-tests": [],
    "corroboration-map": [],
    "schema-index": [],
    "link-prospects": [],
    "outreach-log": [],
    "dr-tracker": [],
    "pr-campaigns": [],
    "haro-log": [],
    "paid-campaign-log": [],
    "ad-copy-library": [],
    "paid-audiences": [],
    "creative-roadmap": [],
    "paid-budget": [],
    "social-calendar": [],
    "repurpose-queue": [],
    "social-community": [],
    "influencer-pipeline": [],
    "weekly-digest": [],
    "anomaly-log": [],
    "attribution": [],
    "funnel": [],
    "lift-studies": [],
    "kpi-dashboard": [],
    "kpi": ["client", "kpi", "period", "baseline", "target", "actual", "attainment_pct"],
    "daily-ops-log": [],
    "task-queue": [],
    "profit-plan": [],
    "incident-log": [],
    "deal-pipeline": [],
    "compliance-log": [],
    "dashboard": [],
    "agent-config": ["agent", "name", "category", "model"],
    "agent-log": ["agent", "run_id", "trigger", "task", "status", "timestamp"],
    "playbook": ["title", "description", "owner"],
    "client-report": ["client", "period", "status"],
}

REQUIRED_GLOBAL = {"type", "last_updated", "tags"}


def parse_frontmatter(text: str) -> Tuple[Dict, str]:
    """Extract YAML frontmatter from markdown text. Returns (frontmatter_dict, body)."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    try:
        import yaml
        fm = yaml.safe_load(parts[1])
        return (fm if isinstance(fm, dict) else {}), parts[2]
    except ImportError:
        # Fallback: basic regex parsing for type, last_updated, tags
        fm = {}
        for line in parts[1].strip().split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                if val.startswith("["):
                    # Simple list parsing
                    val = [v.strip().strip('"').strip("'") for v in val.strip("[]").split(",") if v.strip()]
                fm[key] = val
        return fm, parts[2]
    except Exception:
        return {}, text


def validate_file(path: Path) -> List[str]:
    """Validate a single .md file. Returns list of error strings (empty = valid)."""
    errors = []
    text = path.read_text(encoding="utf-8")

    # Must have frontmatter
    if not text.startswith("---"):
        errors.append("Missing YAML frontmatter (must start with ---)")
        return errors

    fm, _ = parse_frontmatter(text)
    if not fm:
        errors.append("Failed to parse YAML frontmatter")
        return errors

    # Required global fields
    for field in REQUIRED_GLOBAL:
        if field not in fm:
            errors.append(f"Missing required field: '{field}'")

    # Type must exist in registry
    note_type = fm.get("type")
    if note_type:
        if note_type not in TYPE_REGISTRY:
            errors.append(f"Unknown type: '{note_type}' (not in type registry)")
        else:
            # Type-specific required fields
            type_required = TYPE_REGISTRY.get(note_type, [])
            for field in type_required:
                if field not in fm:
                    errors.append(f"Type '{note_type}' missing required field: '{field}'")

    # Date format check
    last_updated = fm.get("last_updated")
    if last_updated:
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", str(last_updated)):
            errors.append(f"Invalid last_updated format: '{last_updated}' (expected YYYY-MM-DD)")

    # Tags must be a list
    tags = fm.get("tags")
    if tags is not None and not isinstance(tags, list):
        errors.append(f"Invalid tags: must be a YAML list, got {type(tags).__name__}")

    return errors


def main():
    vault_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("AgenticMarketingPro-Vault")
    if not vault_path.exists():
        print(f"❌ Vault path not found: {vault_path}")
        sys.exit(1)

    md_files = list(vault_path.rglob("*.md"))
    print(f"🔍 Scanning {len(md_files)} markdown files in {vault_path}")

    failed = 0
    passed = 0

    for path in sorted(md_files):
        rel = path.relative_to(vault_path)
        errors = validate_file(path)
        if errors:
            failed += 1
            print(f"\n❌ {rel}")
            for err in errors:
                print(f"   • {err}")
        else:
            passed += 1

    print(f"\n{'=' * 50}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"{'=' * 50}")

    if failed > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
