---
type: playbook
title: Frontmatter Standards
description: YAML frontmatter templates for every note type in the vault.
last_updated: 2026-01-20
owner: Playbook Librarian Agent
tags: [playbook, type/frontmatter-standards]
---

# Frontmatter Standards

> Every note in the vault must have valid YAML frontmatter. QA Agent rejects notes with missing/invalid fields.

## Required fields (all notes)
- `type:` — note type (see type registry below)
- `last_updated:` — YYYY-MM-DD format
- `tags:` — list of approved tags (see tag-dictionary.md)

## Type registry

| Type | Used for | Required additional fields |
|---|---|---|
| agency-core | 00-Agency-Core notes | title |
| client | Client folder root | client, industry, tier, mrr, status, strategist |
| client-onboarding | Onboarding notes | client, status |
| client-kpis | KPI definitions | client, status |
| client-strategy | 90-day strategy | client, status |
| client-campaign-log | Campaign log | client, status |
| competitor-map | Competitor master list | (none) |
| competitor-keyword-gaps | Keyword gap analysis | competitor |
| competitor-backlinks | Backlink profile | competitor |
| competitor-content | Content audit | competitor |
| competitor-paid | Paid strategy | competitor |
| competitor-team | Team/hiring | competitor |
| keyword-universe | Master keyword list | (none) |
| topic-clusters | Topic clusters | (none) |
| gsc-log | GSC weekly log | (none) |
| bing-log | Bing weekly log | (none) |
| audit-log | Technical audit log | (none) |
| content-calendar | Content calendar | (none) |
| content-brief | Content brief | client, title, slug, content_type, target_keyword, writer_persona, due_date, status, qa_status |
| published-index | Published content index | (none) |
| content-retrospective | Weekly retro | (none) |
| writer-persona | Writer persona config | persona |
| pseo-data | pSEO data sources | (none) |
| pseo-guardrails | pSEO quality rules | (none) |
| pseo-log | pSEO publish log | (none) |
| aeo-tracker | AI citation tracker | (none) |
| entity-registry | Entity registry | (none) |
| llm-tests | LLM prompt tests | (none) |
| corroboration-map | Corroboration map | (none) |
| schema-index | Schema library index | (none) |
| link-prospects | Link prospect list | (none) |
| outreach-log | Outreach log | (none) |
| dr-tracker | DR tracker | (none) |
| pr-campaigns | PR campaigns | (none) |
| haro-log | HARO log | (none) |
| paid-campaign-log | Paid campaign log | (none) |
| ad-copy-library | Ad copy library | (none) |
| paid-audiences | Audience research | (none) |
| creative-roadmap | Creative testing roadmap | (none) |
| paid-budget | Budget allocation | (none) |
| social-calendar | Social calendar | (none) |
| repurpose-queue | Repurpose queue | (none) |
| social-community | Community health | (none) |
| influencer-pipeline | Influencer pipeline | (none) |
| weekly-digest | Weekly digest | (none) |
| anomaly-log | Anomaly log | (none) |
| attribution | Attribution | (none) |
| funnel | Funnel analysis | (none) |
| lift-studies | Conversion lift studies | (none) |
| kpi-dashboard | KPI dashboard | (none) |
| kpi | Single KPI entry | client, kpi, period, baseline, target, actual, attainment_pct |
| daily-ops-log | Daily ops log | (none) |
| task-queue | Task queue | (none) |
| profit-plan | Profit plan | (none) |
| incident-log | Incident log | (none) |
| deal-pipeline | Deal pipeline | (none) |
| compliance-log | Compliance log | (none) |
| dashboard | Dataview dashboard | (none) |
| agent-config | Agent configuration | agent, name, category, model |
| agent-log | Agent run log | agent, run_id, trigger, task, status, timestamp |
| playbook | SOP document | title, description, owner |
| client-report | Monthly client report | client, period, status |
| client-onboarding | Client onboarding | client, status |

## Date format
- All dates: `YYYY-MM-DD` (ISO 8601)
- Date+time: `YYYY-MM-DDTHH:MM:SSZ` (UTC)
- Period fields: `YYYY-MM` (month) or `YYYY-Q[1-4]` (quarter)

## Tag rules
- Every tag follows `category/value` pattern
- Tags must exist in `tag-dictionary.md`
- QA Agent rejects notes with undefined tags (auto-fix: suggest closest match)

## Validation
- Pre-commit hook runs YAML linter on every commit
- QA Agent validates frontmatter on every artifact
- Playbook Librarian runs monthly audit: any notes missing required fields?
