---
type: integration
integration: hotjar
name: Hotjar API
purpose: Heatmaps + session recording
cost_tier: Paid
status: pending
last_health_check: DYNAMIC
tags: [integration, status/pending]
---

# Integration: Hotjar API

## Purpose
Heatmaps + session recording

## Status: PENDING
- **Cost tier:** Paid
- **Health check cadence:** Every 15 min (by MarTech Integration Agent)
- **Last successful call:** [auto-updated]
- **Last failure:** [auto-updated]
- **Monthly cost (current):** $[auto-updated]
- **Monthly budget:** $[configured]

## Credentials
- Stored in: 1Password Teams vault (or HashiCorp Vault)
- Reference name: `$HOTJAR_API_KEY`
- **NEVER** commit credentials to vault. Reference by name only.

## Rate limits
- [Per the API documentation]
- Current usage: [auto-tracked]
- Alert threshold: 80% of limit

## Endpoints used
| Endpoint | Purpose | Frequency |
|---|---|---|
| | | |

## Failure modes
| Failure | Detection | Auto-recovery | Escalation |
|---|---|---|---|
| Auth expired (401) | Health check | Refresh token once | If refresh fails, page MarTech |
| Rate limit (429) | Response code | Backoff + retry | If persistent, alert strategist |
| API down (5xx) | Health check | Retry 3x with backoff | If >30 min, escalate to human |
| Schema change | Response parsing | Log + flag | Playbook Librarian updates integration code |

## Dependency graph
- **Depends on:** [other integrations this one needs]
- **Depended on by:** [which agents use this integration]

## Setup checklist (when activating)
- [ ] Account created / license purchased
- [ ] API credentials generated
- [ ] Credentials added to 1Password / Vault
- [ ] Reference name added to `11-Ops/integrations/.env.example`
- [ ] Health check workflow created in n8n
- [ ] Cost alert thresholds set
- [ ] First successful test call
- [ ] This file updated with `status: active`
