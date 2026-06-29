---
name: qa-pipeline
description: Run the 7-check QA pipeline on any marketing artifact before it reaches a client or goes live. Use when reviewing content drafts, ad copy, email sequences, social posts, content briefs, client reports, or any artifact produced by a specialist agent. Covers brand voice compliance, factual accuracy, legal/compliance, formatting consistency, SEO basics, brief alignment, and plagiarism/originality. The QA Agent has veto power over every producing agent.
---

# QA Pipeline — 7 Checks

Every artifact passes through this before client delivery or publication.


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --qa-check-request
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/qa-check-request-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Pass Threshold

- Every check ≥3/5 AND average ≥4/5
- Binary checks (Check 3: Legal, Check 7: Plagiarism) are absolute gates — any fail = artifact fails entirely
- ≥3 checks below threshold → artifact fails + senior editor review

## The 7 Checks

### Check 1: Brand Voice Compliance
- **What:** Tone, vocabulary, forbidden phrases match `00-Agency-Core/brand-voice-guide.md`
- **How:** Read the brand voice guide. Scan artifact for forbidden phrases. Score against 5 voice principles.
- **Pass threshold:** Score ≥4/5
- **Common failures:**
  - Use of forbidden phrases: "leverage", "synergy", "game-changing", "cutting-edge", "robust", "seamless"
  - Adjectives before numbers: "incredible growth" instead of "47% growth"
  - "We believe" or "we think" instead of data-backed claims
  - Emoji in client-facing content (except social posts where platform-native)

### Check 2: Factual Accuracy
- **What:** Every factual claim has a citable source OR is common knowledge
- **How:** Scan for statistics, claims, comparisons. Flag any without source. For questionable claims, verify against known data or flag for human verification.
- **Pass threshold:** Score ≥4/5; 100% of claims must have source or be flagged
- **Common failures:**
  - Statistics without source or date
  - Dated stats presented as current
  - Competitive claims without citation
  - Percentage changes without baseline

### Check 3: Legal / Compliance (BINARY — absolute gate)
- **What:** FTC disclosures, trademark usage, no prohibited claims (health/financial), CAN-SPAM compliance for emails
- **How:** Pattern-match against `11-Ops/playbooks/compliance-rules.md`. For emails, verify unsubscribe link, physical address, subject line accuracy.
- **Pass threshold:** Score 5/5 — any compliance issue = fail
- **Common failures:**
  - Missing #ad disclosure on sponsored content
  - Comparative claims without citation
  - Health claims without FDA disclaimer
  - CAN-SPAM violations (missing unsubscribe, deceptive subject lines)
  - Trademark misuse

### Check 4: Formatting Consistency
- **What:** Markdown structure valid, headings hierarchical, links work, image alt text present
- **How:** Validate markdown syntax. Check heading hierarchy (no H3 without H2). Verify all links resolve. Check images have alt text.
- **Pass threshold:** Score ≥4/5; 0 broken links allowed
- **Common failures:**
  - H3 without H2 parent
  - Broken internal links (e.g., `[[missing-note]]`)
  - Missing alt text on images
  - Inconsistent heading levels
  - Missing YAML frontmatter or invalid frontmatter

### Check 5: SEO Basics
- **What:** Target keyword present, meta description, internal links, schema where applicable
- **How:** Read the content brief to find target keyword. Verify keyword appears in: title, first 100 words, at least 2 H2s. Check for internal links. Check for meta description.
- **Pass threshold:** Score ≥4/5; target keyword must appear in title, first 100 words, and ≥2 H2s
- **Common failures:**
  - Keyword not in H1/title
  - Missing meta description
  - No internal links
  - Keyword stuffing (density >2.5%)
  - Missing schema markup where applicable

### Check 6: Brief Alignment
- **What:** Artifact addresses the brief's stated goal, audience, and angle
- **How:** Read the content brief. Compare against artifact. Check: goal addressed, audience matched, angle followed, CTA present if specified.
- **Pass threshold:** Score ≥4/5
- **Common failures:**
  - Drift from brief angle
  - Wrong audience (e.g., B2B content written for B2C tone)
  - Missing CTA specified in brief
  - Wrong content type (e.g., brief asked for pillar page, got blog post)
  - Word count outside brief-specified range

### Check 7: Plagiarism / Originality (BINARY — absolute gate)
- **What:** No verbatim copy from external sources or vault content >50 words
- **How:** Scan for suspiciously polished passages. Check against vault content for self-plagiarism. Flag any verbatim matches >50 words.
- **Pass threshold:** Score 5/5 — any plagiarism = fail
- **Common failures:**
  - Copying from prior published piece without attribution
  - Lifting from competitor content
  - Large block quotes without proper attribution
  - Self-plagiarism from another client (vault content reuse)

## Failure Handling

1. **First failure:** Bounce back to producing agent with specific fixes required. Log the QA scores and issues.
2. **Second failure:** Escalate to human senior editor. Log the failure and the agent's attempt.
3. **Three consecutive failures from same agent:** Alert Playbook Librarian to review the agent's system prompt.

## QA Log Format

Every QA run must be logged to `11-Ops/agent-logs/qa/YYYY-MM-DD-[artifact-slug].md`:

```markdown
---
type: agent-log
agent: qa-agent
run_id: YYYY-MM-DD-###
task: QA review of [artifact path]
status: [pass / fail / escalated]
timestamp: YYYY-MM-DDTHH:MM:SSZ
---

# QA Run: [artifact name]

## Artifact
- Path: [vault path]
- Producing agent: [agent name]
- Client: [client name]

## Scores
| Check | Score | Issues |
|---|---|---|
| 1. Brand Voice | [1-5] | [notes] |
| 2. Factual Accuracy | [1-5] | [notes] |
| 3. Legal/Compliance | [1-5] | [notes] |
| 4. Formatting | [1-5] | [notes] |
| 5. SEO Basics | [1-5] | [notes] |
| 6. Brief Alignment | [1-5] | [notes] |
| 7. Plagiarism | [1-5] | [notes] |
| **Average** | **[X.X]** | |

## Result
- [pass / fail / bounced / escalated]
- Next action: [what happens next]
```

## Quick Reference: Forbidden Phrases

Auto-reject if any of these appear in client-facing content:
- "game-changing", "revolutionary", "next-generation", "cutting-edge"
- "leverage" (as a verb), "synergy", "best-in-class", "world-class"
- "seamless", "robust"
- "AI-powered" without specific capability described in next sentence
- "We believe" or "we think" (replace with data or action)

## Quick Reference: Preferred Vocabulary

| Use This | Not This |
|---|---|
| Compound, compounding | Scale (overused) |
| Outcome | Result (vague) |
| Specific | Granular (jargon) |
| Trade-off | Compromise (negative) |
| Evidence | Proof (absolute) |
| Visibility | Awareness (marketing jargon) |
