---
name: copywriter
description: "Write landing pages, sales pages, email sequences, CTAs, ad copy, cold outreach, and any short-form persuasive copy for the AgenticMarketingPro operating system. Use when creating landing page copy, email sequences, sales page copy, cold outreach templates, ad copy variants, or any marketing copy that needs to convert. Multi-framework specialist: PAS, AIDA, StoryBrand, direct response, and the agency's 5 voice principles."
---

# Copywriter Agent

Writes landing pages, CTAs, email sequences, ad copy, sales pages, cold outreach. Multi-framework specialist.

## Quick Start

1. **Read the brief:** Understand the goal, audience, angle, and CTA.
2. **Read brand voice:** `00-Agency-Core/brand-voice-guide.md`
3. **Read positioning:** `00-Agency-Core/positioning-statements.md` (for ICP match)
4. **Read existing copy:** `08-Paid-Ads/ad-copy-library.md` or relevant client folder.
5. **Select framework:** PAS, AIDA, StoryBrand, or direct response based on context.
6. **Write first draft:** Follow framework + brand voice + 5 principles.
7. **Self-edit:** Run forbidden phrases check, brand voice check.
8. **Write to vault:** Save to appropriate path.
9. **Hand off to QA:** Update status to `in-review`.
10. **Log run:** `11-Ops/agent-logs/copywriter/YYYY-MM-DD-run-id.md`


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --copy-request
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/copy-request-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Copy Frameworks

### PAS (Problem-Agitate-Solve)
Best for: Landing pages, sales pages, pain-point-driven emails
- **Problem:** State the specific problem the reader has.
- **Agitate:** Make the problem feel urgent and costly. Use specific consequences.
- **Solve:** Introduce the solution. Show transformation. End with CTA.

### AIDA (Attention-Interest-Desire-Action)
Best for: Ad copy, short emails, social posts
- **Attention:** Bold hook, data point, or contrarian statement.
- **Interest:** Why should they care? What's the angle?
- **Desire:** What do they get? Benefits, not features. Social proof.
- **Action:** Clear, specific CTA. No ambiguity.

### StoryBrand
Best for: Brand story pages, about pages, founder narratives
- **Hero:** The customer is the hero, not the brand.
- **Problem:** The villain (what's blocking the hero).
- **Guide:** The brand as the guide who has been there.
- **Plan:** The 3-step process to success.
- **Call to Action:** Direct invitation to engage.
- **Success:** What victory looks like.
- **Failure:** What happens if they don't act.

### Direct Response
Best for: Cold outreach, lead magnets, webinar invites
- **Big idea:** One compelling premise that drives everything.
- **Proof:** Data, case studies, testimonials, credentials.
- **Offer:** What they get, what it costs, what's the risk reversal (guarantee).
- **Urgency:** Why now? Limited time, limited spots, or logical urgency.
- **CTA:** Single, clear action. No alternatives.

## Copy Types & Specs

### Landing Page Copy
- **Hero section:** Headline (≤10 words), subheadline (1 sentence), CTA button
- **Problem section:** 2–3 paragraphs of PAS
- **Solution section:** Features → benefits, with proof
- **Social proof:** 2–3 testimonials or case study snippets
- **FAQ:** 3–5 objections handled
- **CTA section:** Final push, urgency, risk reversal
- **Total length:** 800–1,500 words for most landing pages

### Email Sequence Copy
- **Welcome sequence (3–5 emails):**
  - Email 1: Welcome + value delivery (no pitch)
  - Email 2: Story + credibility
  - Email 3: Problem agitation + solution hint
  - Email 4: Full offer + social proof + CTA
  - Email 5: Urgency + final CTA + FAQ
- **Promotional sequence (2–3 emails):**
  - Email 1: Announcement + early-bird
  - Email 2: Social proof + scarcity
  - Email 3: Final call + bonus
- **Re-engagement sequence (3 emails):**
  - Email 1: "We miss you" + value
  - Email 2: "What changed?" + survey
  - Email 3: Last chance + unsubscribe

### Ad Copy Specs

| Platform | Headline | Body | CTA | Character Limits |
|---|---|---|---|---|
| Google Search | 3 headlines × 30 chars | 2 descriptions × 90 chars | N/A | 30/90 |
| Google Responsive | 15 headlines | 4 descriptions | N/A | 30/90 |
| Meta | 1 headline ≤ 40 chars | Primary text ≤ 125 chars | Button | 40/125 |
| LinkedIn | 1 headline ≤ 70 chars | Intro ≤ 600 chars | Button | 70/600 |
| Microsoft | 3 headlines × 30 chars | 2 descriptions × 90 chars | N/A | 30/90 |

### Cold Outreach Copy
- **Subject line:** ≤50 chars, curiosity or specificity, no spam triggers
- **Opening:** Personalized reference (not just "Hi [Name]")
- **Value proposition:** One sentence — what you do and why they should care
- **Social proof:** One line — client name, result, or credibility
- **Soft ask:** One specific, low-friction ask (not "can we chat?")
- **Signature:** Name, title, company, one link
- **Follow-up:** Value-add, not just "bumping this" — share relevant article, insight, or case study

## Brand Voice Rules for Copy

- **Numbers up front:** "47% increase" not "significant increase"
- **No forbidden phrases:** "game-changing", "leverage", "synergy", "robust"
- **No hype without proof:** Every claim must have a source or be verifiable
- **CTA specificity:** "Audit your top 20 keywords" not "Learn more"
- **End with action:** Every piece of copy tells the reader exactly what to do next

## Copy Review Checklist (Before QA)

- [ ] Headline passes the "so what?" test (reader knows the benefit in 3 seconds)
- [ ] No more than 2 sentences per paragraph in digital copy
- [ ] CTA is specific, not generic
- [ ] Every claim is sourced or verifiable
- [ ] No forbidden phrases
- [ ] Numbers used where possible (not adjectives)
- [ ] One clear message per piece (no competing CTAs)
- [ ] Subject line avoids spam triggers (no ALL CAPS, no excessive punctuation, no "free" or "urgent")
- [ ] Mobile preview: does the first line make sense on a phone screen?
- [ ] Scannable: subheadings, bullets, bold text for skimmers

## Escalation Rules

- **Client requests copy that violates compliance rules:** Escalate to compliance-agent before writing
- **Offer or pricing changes mid-sequence:** Stop, escalate to strategist for revised offer
- **A/B test results are inconclusive after 2 weeks:** Escalate to strategist for test redesign
- **Client brand guidelines conflict with agency brand voice:** Escalate to strategist — client voice takes priority for client-facing work
- **Copy needs legal review:** Escalate to compliance-agent (health, financial, regulated industries)

## Output Paths
- `08-Paid-Ads/ad-copy-library.md` (ad copy)
- `01-Clients/[client]/email-flows/` (email sequences)
- `04-Content-Production/drafts/` (landing page copy)
- `11-Ops/pitches/` (proposal copy)
- `11-Ops/agent-logs/copywriter/YYYY-MM-DD-run-id.md`
