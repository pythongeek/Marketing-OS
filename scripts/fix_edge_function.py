#!/usr/bin/env python3
"""Fix the Supabase Edge Function index.ts to remove all remaining Kimi references."""
import os

EDGE_FN = r"F:\Agentic Marketing Pro\marketing\supabase\functions\execute-jobs\index.ts"
with open(EDGE_FN, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix the getAvailableProvider function - remove MiniMax/OpenAI/Kimi fallbacks
old_provider = """async function getAvailableProvider(): Promise<{ name: string; apiKey: string; baseUrl: string; model: string } | null> {
  // Check MiniMax first
  if (MINIMAX_API_KEY) {
    const health = await checkProviderHealth("minimax", MINIMAX_API_KEY, MINIMAX_BASE_URL);
    if (health.available) {
      return { name: "minimax", apiKey: MINIMAX_API_KEY, baseUrl: MINIMAX_BASE_URL, model: MINIMAX_MODEL };
    }
    console.warn(`MiniMax unavailable: ${health.error}`);
  }

  // Fall back to OpenAI
  if (OPENAI_API_KEY) {
    const health = await checkProviderHealth("openai", OPENAI_API_KEY, OPENAI_BASE_URL);
    if (health.available) {
      return { name: "openai", apiKey: OPENAI_API_KEY, baseUrl: OPENAI_BASE_URL, model: OPENAI_MODEL };
    }
    console.warn(`OpenAI unavailable: ${health.error}`);
  }

  // Fall back to Kimi
  if (KIMI_API_KEY) {
    const health = await checkProviderHealth("kimi", KIMI_API_KEY, KIMI_BASE_URL);
    if (health.available) {
      return { name: "kimi", apiKey: KIMI_API_KEY, baseUrl: KIMI_BASE_URL, model: KIMI_MODEL };
    }
    console.warn(`Kimi unavailable: ${health.error}`);
  }

  return null;
}"""

new_provider = """async function getAvailableProvider(): Promise<{ name: string; apiKey: string; baseUrl: string; model: string } | null> {
  // Hermes Agent Desktop is the only provider
  if (HERMES_AGENT_API_KEY) {
    const health = await checkProviderHealth("hermes_agent", HERMES_AGENT_API_KEY, HERMES_AGENT_BASE_URL);
    if (health.available) {
      return { name: "hermes_agent", apiKey: HERMES_AGENT_API_KEY, baseUrl: HERMES_AGENT_BASE_URL, model: HERMES_AGENT_MODEL };
    }
    console.warn(`Hermes Agent Desktop unavailable: ${health.error}`);
  }

  return null;
}"""

if old_provider in content:
    content = content.replace(old_provider, new_provider)
    print("[ok] Replaced getAvailableProvider function")
else:
    print("[warn] getAvailableProvider function not matched - file may already be updated")

# 2. Fix the handleHealthCheck function - remove MiniMax/OpenAI/Kimi checks
old_health = """  const checks = await Promise.all([
    checkProviderHealth("minimax", MINIMAX_API_KEY, MINIMAX_BASE_URL),
    checkProviderHealth("openai", OPENAI_API_KEY, OPENAI_BASE_URL),
    checkProviderHealth("kimi", KIMI_API_KEY, KIMI_BASE_URL),
  ]);"""

new_health = """  const checks = await Promise.all([
    checkProviderHealth("hermes_agent", HERMES_AGENT_API_KEY, HERMES_AGENT_BASE_URL),
  ]);"""

if old_health in content:
    content = content.replace(old_health, new_health)
    print("[ok] Replaced handleHealthCheck function")
else:
    print("[warn] handleHealthCheck function not matched")

# 3. Fix the error message in executeJob
old_err = '"No AI provider available. Please configure MINIMAX_API_KEY, OPENAI_API_KEY, or KIMI_API_KEY in Supabase secrets."'
new_err = '"No AI provider available. Please configure HERMES_AGENT_API_KEY in Supabase secrets."'
if old_err in content:
    content = content.replace(old_err, new_err)
    print("[ok] Replaced error message in executeJob")

# 4. Remove reasoning_split special case for MiniMax
old_reasoning = '''      // MiniMax-specific: reasoning split
      ...(provider.name === "minimax" ? { reasoning_split: true } : {}),'''
new_reasoning = '''      // Hermes Agent Desktop: reasoning split (if supported)
      ...(provider.name === "hermes_agent" ? { reasoning_split: true } : {}),'''
if old_reasoning in content:
    content = content.replace(old_reasoning, new_reasoning)
    print("[ok] Replaced reasoning_split")

# 5. Update console.log message
old_log = 'console.log("=== AMP Edge Function: execute-jobs (Multi-provider) ===");'
new_log = 'console.log("=== AMP Edge Function: execute-jobs (Hermes Agent Desktop) ===");'
if old_log in content:
    content = content.replace(old_log, new_log)
    print("[ok] Replaced console log")

# 6. Update Slack alert AI Provider field
old_slack = '{ type: "mrkdwn", text: `*AI Provider:*\\nMulti-provider fallback` },'
new_slack = '{ type: "mrkdwn", text: `*AI Provider:*\\nHermes Agent Desktop` },'
if old_slack in content:
    content = content.replace(old_slack, new_slack)
    print("[ok] Replaced Slack alert")

with open(EDGE_FN, "w", encoding="utf-8") as f:
    f.write(content)
print(f"[done] Wrote {EDGE_FN}")