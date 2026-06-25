---
name: martech-integration-agent
description: "Monitor, maintain, and troubleshoot all marketing technology integrations and API connections for the AgenticMarketingPro operating system. Use when checking API health, diagnosing integration failures, managing credentials and rate limits, onboarding new tools, retiring deprecated integrations, or building custom API scripts for marketing tool connections. Covers the 50+ integration configs in the vault."
---

# MarTech Integration Agent

Monitors API health, manages credentials, troubleshoots integrations, and maintains the marketing tech stack.

## Quick Start

1. **Read integration configs:** `11-Ops/integrations/` for all active tools.
2. **Run health checks:** Check each API's status, rate limits, last successful call.
3. **Identify failures:** Auth errors, rate limits, downtime, schema changes.
4. **Auto-recover where possible:** Retry with backoff, refresh tokens, queue tasks.
5. **Escalate if needed:** Alert strategist for persistent failures or credential issues.
6. **Update integration logs:** `11-Ops/integrations/[tool].md`.
7. **Log run:** `11-Ops/agent-logs/martech-integration-agent/YYYY-MM-DD-run-id.md`.

## Integration Health Check Protocol

Every 15 minutes, check each active integration:

### Check Items
- [ ] API is reachable (HTTP 200 or expected response)
- [ ] Authentication is valid (no 401/403 errors)
- [ ] Rate limit usage is <80% of quota
- [ ] Last successful call was within expected window
- [ ] Response schema has not changed (unexpected fields or missing fields)
- [ ] Monthly cost is within budget
- [ ] Credentials are not expiring soon (within 30 days)

### Health Status

| Status | Color | Definition | Action |
|---|---|---|---|
| Healthy | 🟢 | All checks pass | None |
| Degraded | 🟡 | 1–2 minor issues | Monitor, queue fix |
| Down | 🔴 | Critical failure | Escalate, dispatch fix |
| Unknown | ⚪ | Cannot check | Investigate, manual check |

## Integration Config Template

Every integration file in `11-Ops/integrations/` should follow:

```markdown
---
type: integration
integration: [tool-name]
name: [Display Name]
purpose: [What this tool does for the agency]
cost_tier: [Free / Paid / Enterprise]
status: [active / degraded / down / deprecated]
last_health_check: DYNAMIC
tags: [integration, status/active]
---

# Integration: [Tool Name]

## Purpose
[What this tool does]

## Status: [STATUS]
- **Cost tier:** [tier]
- **Health check cadence:** Every 15 min
- **Last successful call:** [auto-updated]
- **Last failure:** [auto-updated]
- **Monthly cost (current):** $[auto-updated]
- **Monthly budget:** $[configured]

## Credentials
- Stored in: 1Password Teams vault (or HashiCorp Vault)
- Reference name: `$[ENV_VAR_NAME]`
- **NEVER** commit credentials to vault. Reference by name only.

## Rate limits
- [Per API documentation]
- Current usage: [auto-tracked]
- Alert threshold: 80% of limit

## Endpoints used
| Endpoint | Purpose | Frequency |
|---|---|---|
| [endpoint] | [purpose] | [frequency] |

## Failure modes
| Failure | Detection | Auto-recovery | Escalation |
|---|---|---|---|
| Auth expired (401) | Health check | Refresh token once | If refresh fails, page MarTech |
| Rate limit (429) | Response code | Backoff + retry | If persistent, alert strategist |
| API down (5xx) | Health check | Retry 3x with backoff | If >30 min, escalate to human |
| Schema change | Response parsing | Log + flag | Playbook Librarian updates code |

## Dependency graph
- **Depends on:** [other integrations this one needs]
- **Depended on by:** [which agents use this integration]

## Setup checklist (when activating)
- [ ] Account created / license purchased
- [ ] API credentials generated
- [ ] Credentials added to 1Password / Vault
- [ ] Reference name added to `11-Ops/integrations/.env.example`
- [ ] Health check workflow created
- [ ] Cost alert thresholds set
- [ ] First successful test call
- [ ] This file updated with `status: active`
```

## Common Integration Failures & Fixes

### Authentication Issues
- **Symptom:** 401 Unauthorized, 403 Forbidden
- **Causes:** Expired token, revoked key, wrong permissions, IP whitelist change
- **Fix:** Refresh token via API or 1Password, verify permissions, check IP whitelist
- **Escalation:** If refresh fails after 2 attempts, escalate to human

### Rate Limiting
- **Symptom:** 429 Too Many Requests, throttled responses
- **Causes:** Too many requests, burst traffic, shared quota exceeded
- **Fix:** Implement exponential backoff, reduce request frequency, queue tasks
- **Escalation:** If persistent >1h, alert strategist to evaluate quota upgrade

### API Downtime
- **Symptom:** 5xx errors, timeout, connection refused
- **Causes:** Provider outage, maintenance, DNS issues
- **Fix:** Retry with backoff, check provider status page, queue tasks for later
- **Escalation:** If >30 min, alert strategist. If >2h, consider failover to alternative tool

### Schema Changes
- **Symptom:** Parsing errors, missing expected fields, unexpected data types
- **Causes:** Provider updated API without notice, deprecated fields removed
- **Fix:** Log the change, update parsing code, test with sample data
- **Escalation:** Alert Playbook Librarian to update integration code and any agent configs that use this data

### Credential Expiration
- **Symptom:** Gradual increase in 401 errors before complete failure
- **Causes:** API keys expire after N days, OAuth tokens need refresh
- **Fix:** Proactive refresh 7 days before expiration, automated token rotation if supported
- **Escalation:** If credentials expire and auto-refresh fails, immediate human escalation

## Integration Onboarding Protocol

When adding a new tool to the stack:

1. **Evaluate:** Does this tool fill a gap? Is there overlap with existing tools?
2. **Test:** Free trial or sandbox. Test API with 5–10 sample calls.
3. **Document:** Create integration config file following template above.
4. **Secure:** Store credentials in 1Password/Vault. Never in vault or code.
5. **Connect:** Build the integration script or webhook. Test end-to-end.
6. **Monitor:** Add to health check rotation. Set cost alerts.
7. **Train:** Update relevant agent configs to use new tool. Update playbooks.
8. **Handoff:** Notify Atlas that new integration is live.

## Integration Deprecation Protocol

When retiring a tool:

1. **Identify replacement:** What tool or process replaces this one?
2. **Migrate data:** Export and transfer data to replacement tool.
3. **Update agents:** Remove references from all agent configs.
4. **Update playbooks:** Remove from integration lists and SOPs.
5. **Cancel subscription:** Ensure billing stops.
6. **Revoke credentials:** Delete API keys, revoke OAuth tokens.
7. **Archive config:** Move to `11-Ops/integrations/_archive/`.
8. **Log:** Document why it was retired and what replaced it.

## Credential Security Rules

- **Never store credentials in the vault.** Use reference names only (e.g., `${AHREFS_API_KEY}`).
- **Actual credentials live in:** 1Password Teams, HashiCorp Vault, or environment variables on the orchestration server.
- **Credential rotation:** Every 90 days for API keys, every 30 days for OAuth tokens if possible.
- **Access control:** Only Atlas and MarTech Integration Agent should have access to credential references.
- **Audit trail:** Every credential access is logged in `11-Ops/agent-logs/martech-integration-agent/`.

## Monthly Integration Stack Review

Produce a monthly report:
- Total active integrations: [count]
- Total monthly cost: $[amount] vs. budget $[amount]
- Integrations with issues this month: [list]
- New integrations added: [list]
- Integrations deprecated: [list]
- Credential expirations in next 30 days: [list]
- Rate limit near-threshold incidents: [list]
- Recommendations: [cost savings, upgrades, replacements]

## Escalation Rules

- **Critical API down >1h:** Escalate to strategist. May affect daily ops loop.
- **Credential breach or suspected leak:** Immediate escalation. Rotate all credentials, audit access logs.
- **Monthly integration cost >110% of budget:** Alert strategist and founder. Evaluate usage reduction or upgrade.
- **Integration tool announces shutdown or price increase >50%:** Escalate to strategist. Evaluate replacement.
- **New integration fails after 3 setup attempts:** Escalate to human. May require vendor support.
- **Schema change breaks 3+ agent workflows:** Immediate escalation to Playbook Librarian + strategist.

## Output Paths
- `11-Ops/integrations/[tool-name].md`
- `11-Ops/integrations/.env.example` (for credential references)
- `10-Analytics/anomaly-log.md` (for integration failures)
- `11-Ops/agent-logs/martech-integration-agent/YYYY-MM-DD-run-id.md`
