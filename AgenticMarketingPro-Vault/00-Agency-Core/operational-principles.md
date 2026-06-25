---
type: agency-core
title: Operational Principles
last_updated: 2026-01-20
tags: [agency/core, type/principles]
---

# Operational Principles — The 7 Non-Negotiables

Every agent in the fleet is programmed to obey these principles. Violations are logged as incidents and trigger Playbook Librarian review.

## 1. Obsidian is the single source of truth
Every client brief, audit, content draft, backlink prospect, ad campaign, and report lives as a versioned markdown file in the vault. No Google Docs, no Notion pages, no Slack threads as source of truth. Other tools are interfaces to the vault, not replacements for it.

## 2. Every agent reads before it writes
No agent produces output without first retrieving relevant context from the vault via the RAG pipeline. This is enforced at the orchestration layer — an agent that skips retrieval is a bug, not a shortcut.

## 3. Every action is logged
Every agent run produces a log entry with inputs, retrieved context, LLM response, output file path, token cost, latency, and approval status. Logs are retained for 90 days at full fidelity, then summarized.

## 4. Humans approve high-risk decisions
The HITL gates in §12.5 of the architecture plan are non-negotiable. Atlas cannot bypass them, even under direct human instruction — the human must edit the playbook in Git to change the rule (itself an audited action).

## 5. No PII in the vault
Email addresses, phone numbers, customer names, transaction records stay in source systems (HubSpot, Klaviyo, Stripe). The vault stores aggregate metrics + strategy + agent outputs only. This single rule eliminates 80% of regulatory exposure.

## 6. Every output passes QA
No artifact reaches a client without passing the 7-check QA pipeline (§13.1). No exceptions, even for "urgent" requests. The QA Agent has veto power over every producing agent.

## 7. The vault compounds
Every client engagement, every test result, every failed experiment is captured in the vault. After 12 months, the vault is the agency's primary moat. Agents that don't write back to the vault are defects — fix them immediately.
