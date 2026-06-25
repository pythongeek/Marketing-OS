---
type: playbook
title: QA Checklist
description: The 7-check QA pipeline. Every artifact passes through this before client delivery.
last_updated: 2026-01-20
owner: QA Agent
tags: [playbook, type/qa-checklist, priority/critical]
---

# QA Checklist — 7 Checks

> Every artifact (content, ad copy, email, social post, brief, report) passes through QA Agent before client delivery. Pass threshold: every check ≥3/5 AND average ≥4/5.

## Check 1: Brand voice compliance
- **What:** Tone, vocabulary, forbidden phrases match `00-Agency-Core/brand-voice-guide.md`
- **How:** Custom fine-tuned classifier scores 0-100; ≥70 = pass
- **Pass threshold:** Score ≥4/5 (i.e., classifier score ≥80)
- **Common failures:** Use of forbidden phrases ("leverage", "synergy", "game-changing")

## Check 2: Factual accuracy
- **What:** Every factual claim has a citable source OR is common knowledge
- **How:** Anthropic Citation API + Perplexity verification
- **Pass threshold:** Score ≥4/5; 100% of claims must have source or be flagged for human verification
- **Common failures:** Statistics without source, dated stats presented as current

## Check 3: Legal/compliance
- **What:** FTC disclosures, trademark usage, no prohibited claims (health/financial), CAN-SPAM compliance for emails
- **How:** Pattern matching + LLM analysis against `11-Ops/playbooks/compliance-rules.md`
- **Pass threshold:** Score 5/5 (BINARY — any compliance issue = fail)
- **Common failures:** Missing #ad disclosure, comparative claims without citation, health claims without FDA disclaimer

## Check 4: Formatting consistency
- **What:** Markdown structure valid, headings hierarchical, links work, image alt text present
- **How:** Markdown linter + link checker + custom validator
- **Pass threshold:** Score ≥4/5; 0 broken links allowed
- **Common failures:** H3 without H2 parent, broken internal links, missing alt text

## Check 5: SEO basics
- **What:** Target keyword present, meta description, internal links, schema where applicable
- **How:** Surfer SEO API + custom validator
- **Pass threshold:** Score ≥4/5; target keyword must appear in title, first 100 words, and at least 2 H2s
- **Common failures:** Keyword not in H1, missing meta description, no internal links

## Check 6: Brief alignment
- **What:** Artifact addresses the brief's stated goal, audience, and angle
- **How:** LLM analysis comparing artifact to brief
- **Pass threshold:** Score ≥4/5
- **Common failures:** Drift from brief angle, wrong audience, missing CTA specified in brief

## Check 7: Plagiarism / originality
- **What:** No verbatim copy from external sources or vault content >50 words
- **How:** Custom similarity check against vault + web search for suspicious phrases
- **Pass threshold:** Score 5/5 (BINARY — any plagiarism = fail)
- **Common failures:** Copying from prior published piece without attribution, lifting from competitor content

## Pass/fail logic
- All 7 checks must pass threshold
- Any binary check (3, 7) fails → entire artifact fails
- ≥3 checks below threshold → artifact fails + senior editor review

## Failure handling
1. First failure: bounce back to producing agent with specific fixes required
2. Second failure: escalate to human senior editor
3. Three consecutive failures from same agent: Playbook Librarian reviews agent prompt

## QA log
- Every QA run logged in `11-Ops/agent-logs/qa/YYYY-MM-DD-[artifact-slug].md`
- Log contains: artifact path, scores per check, issues found, resolution
