#!/usr/bin/env python3
"""
Replace all Kimi Work / Kimi references with Hermes Agent Desktop.
This script performs the migrations identified during the assessment.
"""
import os
import re

ROOT = r"F:\Agentic Marketing Pro\marketing"

# ── 1. infrastructure/webhooks/poller.py ─────────────────────────────
POLLER = os.path.join(ROOT, r"infrastructure\webhooks\poller.py")
with open(POLLER, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Kimi Work references
content = content.replace(
    "AgenticMarketingPro — Kimi Work Job Poller",
    "AgenticMarketingPro — Hermes Agent Desktop Job Poller",
)
content = content.replace(
    "Disable the local Kimi Work cron job",
    "Disable the local Hermes Agent Desktop cron job",
)
content = content.replace(
    "via Minimax M3.",
    "via Hermes Agent Desktop.",
)

# Replace provider/model config calls
content = content.replace(
    "provider=\"minimax\"",
    "provider=\"hermes_agent\"",
)
content = content.replace(
    "Config.DEFAULT_LLM_MODEL",
    "Config.DEFAULT_HERMES_AGENT_MODEL",
)

with open(POLLER, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {POLLER}")


# ── 2. infrastructure/scripts/cost_tracker.py ─────────────────────────
COST_TRACKER = os.path.join(ROOT, r"infrastructure\scripts\cost_tracker.py")
with open(COST_TRACKER, "r", encoding="utf-8") as f:
    content = f.read()

# Remove kimi-specific cost entries (or replace with hermes_agent)
content = content.replace(
    '    "kimi-moonshot-v1-8k": {"input": 0.003, "output": 0.003},\n',
    "",
)
content = content.replace(
    '    "kimi-moonshot-v1-32k": {"input": 0.006, "output": 0.006},\n',
    "",
)
content = content.replace(
    "provider: str  # openai, anthropic, kimi, minimax, etc.",
    "provider: str  # openai, anthropic, hermes_agent, etc.",
)

with open(COST_TRACKER, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {COST_TRACKER}")


# ── 3. infrastructure/config.py ──────────────────────────────────────
CONFIG = os.path.join(ROOT, r"infrastructure\config.py")
with open(CONFIG, "r", encoding="utf-8") as f:
    content = f.read()

# Replace Kimi API key check with Hermes Agent Desktop
content = content.replace(
    '"kimi": cls.KIMI_API_KEY is not None,',
    '"hermes_agent": cls.HERMES_AGENT_API_KEY is not None,',
)

with open(CONFIG, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {CONFIG}")


# ── 4. infrastructure/ui/processors.py ────────────────────────────────
PROCESSORS = os.path.join(ROOT, r"infrastructure\ui\processors.py")
with open(PROCESSORS, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '"kimi_api_key": "KIMI_API_KEY",',
    '"hermes_agent_api_key": "HERMES_AGENT_API_KEY",',
)

with open(PROCESSORS, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {PROCESSORS}")


# ── 5. infrastructure/ui/form_engine.py ──────────────────────────────
FORM_ENGINE = os.path.join(ROOT, r"infrastructure\ui\form_engine.py")
with open(FORM_ENGINE, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    'FormField("kimi_api_key", "password", label="Kimi API Key", placeholder="Optional — for Kimi Moonshot fallback"),',
    'FormField("hermes_agent_api_key", "password", label="Hermes Agent Desktop API Key", placeholder="Required for Hermes Agent Desktop runtime"),',
)

with open(FORM_ENGINE, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {FORM_ENGINE}")


# ── 6. web/app/credentials/page.tsx ──────────────────────────────────
CRED_PAGE = os.path.join(ROOT, r"web\app\credentials\page.tsx")
with open(CRED_PAGE, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    '    key: "kimi",\r\n    label: "Kimi (Moonshot)",',
    '    key: "hermes_agent",\r\n    label: "Hermes Agent Desktop",',
)
content = content.replace(
    '{ key: "model", label: "Model", type: "text", placeholder: "kimi-latest" },',
    '{ key: "model", label: "Model", type: "text", placeholder: "MiniMax-M3" },',
)

with open(CRED_PAGE, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {CRED_PAGE}")


# ── 7. skills/longform-writer/SKILL.md ───────────────────────────────
LONGFORM = os.path.join(ROOT, r"skills\longform-writer\SKILL.md")
with open(LONGFORM, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "kimi_search_v2",
    "hermes_agent_search",
)

with open(LONGFORM, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {LONGFORM}")


# ── 8. AgenticMarketingPro-Vault/11-Ops/job-execution-workflow.md ────
WORKFLOW = os.path.join(
    ROOT, r"AgenticMarketingPro-Vault\11-Ops\job-execution-workflow.md"
)
with open(WORKFLOW, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "| `LLM_API_KEY` | OpenAI/Kimi API key |",
    "| `HERMES_AGENT_API_KEY` | Hermes Agent Desktop API key |",
)
content = content.replace(
    "| `LLM_MODEL` | Model name (e.g., `kimi-latest`) |",
    "| `HERMES_AGENT_MODEL` | Model name (e.g., `MiniMax-M3`) |",
)

with open(WORKFLOW, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {WORKFLOW}")


# ── 9. README.md ─────────────────────────────────────────────────────
README = os.path.join(ROOT, "README.md")
with open(README, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "all orchestrated by Kimi Work.",
    "all orchestrated by Hermes Agent Desktop.",
)
content = content.replace(
    "### 4. Set Up Kimi Work Poller (Local Machine)",
    "### 4. Set Up Hermes Agent Desktop Poller (Local Machine)",
)
content = content.replace(
    "On the machine where Kimi Work runs:",
    "On the machine where Hermes Agent Desktop runs:",
)
content = content.replace(
    "31 agent skill definitions (Kimi Work runtime)",
    "31 agent skill definitions (Hermes Agent Desktop runtime)",
)
content = content.replace(
    "Kimi Work poller (polls Supabase jobs)",
    "Hermes Agent Desktop poller (polls Supabase jobs)",
)
content = content.replace(
    "Root .env template (Kimi Work machine)",
    "Root .env template (Hermes Agent Desktop machine)",
)
content = content.replace(
    "│     Kimi Work       │",
    "│     Hermes Agent Desktop │",
)
content = content.replace(
    "**Kimi Work poller** (running on your local machine)",
    "**Hermes Agent Desktop poller** (running on your local machine)",
)
content = content.replace(
    "Python 3.9+ (for Kimi Work infrastructure)",
    "Python 3.9+ (for Hermes Agent Desktop infrastructure)",
)
content = content.replace(
    "Kimi Work / local machine environment variables",
    "Hermes Agent Desktop / local machine environment variables",
)
content = content.replace(
    "| **Agent Runtime** | Kimi Work (local) |",
    "| **Agent Runtime** | Hermes Agent Desktop (local) |",
)
content = content.replace(
    "Built with Kimi Work + Next.js + Supabase + ChromaDB + 31 specialized agents.",
    "Built with Hermes Agent Desktop + Next.js + Supabase + ChromaDB + 31 specialized agents.",
)
content = content.replace(
    "~/.kimi/daimon/\r\n     │  skills/             │",
    "~/.hermes/skills/             │",
)
content = content.replace(
    "loads the skill from `~/.kimi/daimon/skills/`",
    "loads the skill from `~/.hermes/skills/`",
)

with open(README, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {README}")


# ── 10. DEPLOYMENT.md ────────────────────────────────────────────────
DEPLOYMENT = os.path.join(ROOT, "DEPLOYMENT.md")
with open(DEPLOYMENT, "r", encoding="utf-8") as f:
    content = f.read()

content = content.replace(
    "Supabase database + Kimi Work poller + cron-job.org triggers.",
    "Supabase database + Hermes Agent Desktop poller + cron-job.org triggers.",
)
content = content.replace(
    "## Step 3: Kimi Work Poller",
    "## Step 3: Hermes Agent Desktop Poller",
)
content = content.replace(
    "[Step 3: Kimi Work Poller](#step-3-kimi-work-poller)",
    "[Step 3: Hermes Agent Desktop Poller](#step-3-hermes-agent-desktop-poller)",
)
content = content.replace(
    "| Python | 3.9+ | Kimi Work poller + skills |",
    "| Python | 3.9+ | Hermes Agent Desktop poller + skills |",
)
content = content.replace(
    "│     Kimi Work       │",
    "│     Hermes Agent Desktop │",
)
content = content.replace(
    "**Kimi Work poller** (running on your local machine)",
    "**Hermes Agent Desktop poller** (running on your local machine)",
)
content = content.replace(
    "loads the skill from `~/.kimi/daimon/skills/`",
    "loads the skill from `~/.hermes/skills/`",
)
content = content.replace(
    "Vercel only does DB writes (10ms). Heavy work runs on Kimi Work.",
    "Vercel only does DB writes (10ms). Heavy work runs on Hermes Agent Desktop.",
)
content = content.replace(
    "Vault stays local on Kimi Work.",
    "Vault stays local on Hermes Agent Desktop.",
)
content = content.replace(
    "Admin shows vault via iframe or static file hosting from Kimi Work machine.",
    "Admin shows vault via iframe or static file hosting from Hermes Agent Desktop machine.",
)
content = content.replace(
    "Choose closest to your Kimi Work machine",
    "Choose closest to your Hermes Agent Desktop machine",
)
content = content.replace(
    "The poller runs on your local machine (where Kimi Work is installed).",
    "The poller runs on your local machine (where Hermes Agent Desktop is installed).",
)
content = content.replace(
    "Check Kimi Work poller logs:",
    "Check Hermes Agent Desktop poller logs:",
)
content = content.replace(
    "### 5.1 Test 1: Trigger from Vercel → Execute on Kimi Work → Result in Vercel",
    "### 5.1 Test 1: Trigger from Vercel → Execute on Hermes Agent Desktop → Result in Vercel",
)
content = content.replace(
    "### `.env` (Project Root — Kimi Work Machine)",
    "### `.env` (Project Root — Hermes Agent Desktop Machine)",
)
content = content.replace(
    "KIMI_API_KEY=...",
    "HERMES_AGENT_API_KEY=...",
)
content = content.replace(
    "run skills manually via Kimi Work",
    "run skills manually via Hermes Agent Desktop",
)
content = content.replace(
    "### Update Kimi Work Skills",
    "### Update Hermes Agent Desktop Skills",
)
content = content.replace(
    "# On your Kimi Work machine:",
    "# On your Hermes Agent Desktop machine:",
)
content = content.replace(
    "# Copy updated skills to Kimi managed directory",
    "# Copy updated skills to Hermes Agent Desktop managed directory",
)
content = content.replace(
    "cp -r skills/* ~/.kimi/daimon/skills/",
    "cp -r skills/* ~/.hermes/skills/",
)
content = content.replace(
    "Integrate with Kimi Work's native tools for deeper orchestration",
    "Integrate with Hermes Agent Desktop's native tools for deeper orchestration",
)

with open(DEPLOYMENT, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[ok] {DEPLOYMENT}")


# ── 11. .env.example ─────────────────────────────────────────────────
ENV_EXAMPLE = os.path.join(ROOT, ".env.example")
if os.path.exists(ENV_EXAMPLE):
    with open(ENV_EXAMPLE, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace(
        "KIMI_API_KEY=",
        "HERMES_AGENT_API_KEY=",
    )
    content = content.replace(
        "KIMI_BASE_URL=",
        "HERMES_AGENT_BASE_URL=",
    )
    content = content.replace(
        "KIMI_MODEL=",
        "HERMES_AGENT_MODEL=",
    )
    # Remove OpenAI/MiniMax sections if any (kept for parity)

    with open(ENV_EXAMPLE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[ok] {ENV_EXAMPLE}")


print("\nAll Kimi Work references replaced with Hermes Agent Desktop.")