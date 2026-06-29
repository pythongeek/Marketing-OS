---
name: pitch-agent
description: "Build prospect-specific sales proposals, pitch decks, and competitive site audits for the AgenticMarketingPro operating system. Use when creating a new business proposal, building a competitive positioning deck for a prospect, running a prospect site audit, or drafting follow-up sequences for warm leads. Combines competitive intelligence, historical case studies from the vault, and the agency's positioning to produce evidence-led proposals that convert."
---

# Pitch / Proposal Agent

Builds prospect-specific proposals using competitive intel, case studies, and prospect audits.

## Quick Start

1. **Read deal pipeline:** `11-Ops/deal-pipeline.md` for prospect details.
2. **Read prospect info:** Industry, website, pain points, decision-makers.
3. **Read positioning:** `00-Agency-Core/positioning-statements.md` for ICP match.
4. **Read competitor intel:** `02-Competitors/` for relevant competitor data.
5. **Read case studies:** `01-Clients/` for similar-client success stories.
6. **Run prospect audit:** Quick site audit (lighter than full onboarding audit).
7. **Build proposal:** Competitive positioning + findings + solution + pricing + timeline.
8. **HITL review:** Strategist approves before sending.
9. **Write to vault:** `11-Ops/pitches/[prospect]-YYYY-MM-DD.md`
10. **Log run:** `11-Ops/agent-logs/pitch-agent/YYYY-MM-DD-run-id.md`


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --pitch-proposal
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/pitch-proposal-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Prospect Audit (Lightweight, 4–6 Hours)

### Quick Technical Check (1 hour)
- [ ] Site speed (PageSpeed Insights mobile + desktop)
- [ ] Mobile-friendliness
- [ ] Core Web Vitals (if data available)
- [ ] Indexation status (site: search + sitemap check)
- [ ] Basic schema presence
- [ ] SSL/security

### Content Quick Scan (1 hour)
- [ ] Content inventory: blog frequency, topics, quality
- [ ] Target keyword signals: what do they rank for? (use search or Ahrefs/Semrush if available)
- [ ] Content gaps: obvious missing topics vs. competitors
- [ ] E-E-A-T signals: author bios, credentials, citations
- [ ] CTA quality: are CTAs clear and compelling?

### Competitive Snapshot (1 hour)
- [ ] Top 2–3 competitors identified
- [ ] Competitor keyword overlap (shared rankings)
- [ ] Competitor content velocity (how often they publish)
- [ ] Competitor backlink advantage (DR difference)
- [ ] Competitor paid presence (are they running ads?)

### Off-Page Snapshot (1 hour)
- [ ] DR and referring domains (Ahrefs/Semrush)
- [ ] Review profile (Google, G2, Trustpilot, etc.)
- [ ] Social presence and engagement
- [ ] Brand mentions and sentiment
- [ ] Existing backlinks quality

### Paid Snapshot (if applicable, 1 hour)
- [ ] Are they running Google Ads? Meta? LinkedIn?
- [ ] Ad copy and landing page quality (if visible)
- [ ] Estimated spend (if detectable via tools)
- [ ] Competitor ad presence

## Proposal Structure

### 1. Cover / Title Slide
- Prospect name, date, agency name
- Clean, professional, no gimmicks

### 2. Executive Summary (1 page)
- "We audited [Prospect] and found [3 key findings]. We believe [strategic thesis]. Our plan will [specific outcome] in 90 days."
- One paragraph. No more.

### 3. What We Found (The Audit)
- 3–5 key findings, each with evidence
- Use the prospect's own data or screenshots
- Be specific: "Your site loads in 4.2s on mobile vs. industry benchmark of 2.5s"
- Show, don't just tell: include screenshots where possible

### 4. Competitive Landscape (The Kill)
- Top 2–3 competitors analyzed
- Where competitors are winning (be honest)
- Where the opportunity is (the gap)
- Why the prospect can win (their unique advantage)

### 5. Our Approach (The Solution)
- Phase 1: Foundation (30 days) — what we fix first
- Phase 2: Build (30 days) — what we add
- Phase 3: Compound (30 days) — how we scale
- Tie each phase to the prospect's specific goals

### 6. Evidence (Case Studies)
- 1–2 case studies from similar clients in the vault
- Specific results: "Client X grew organic traffic 47% in Q1 using this exact playbook"
- Make it relatable: similar industry, similar size, similar challenge
- If no exact match, use the closest available with caveats

### 7. Investment (Pricing)
- Recommended tier: Starter / Growth / Scale / Enterprise
- What's included (reference services-and-pricing.md)
- Add-ons if relevant (AEO monitoring, crisis management, etc.)
- Onboarding fee (if applicable)
- Contract terms (3-month minimum, 30-day cancellation after)
- No hidden fees, no surprise charges

### 8. Next Steps
- Timeline from signature to first deliverable
- What we need from them (access, assets, approval process)
- What they can expect from us (communication cadence, reporting)
- One clear CTA: "Reply to confirm the kickoff call date"

### 9. About Us (Brief)
- One paragraph: who we are, what makes us different
- The agent OS angle (not a traditional agency)
- 1–2 client logos or testimonials (if available and permitted)
- Contact info

## Proposal Writing Rules

- **Lead with their problem, not your solution:** They care about their business, not your process.
- **Use their language:** Mirror the terminology from their website, industry, and communications.
- **Be specific, not generic:** "We'll fix your technical SEO" is generic. "We'll reduce your LCP from 4.2s to <2.5s" is specific.
- **Show evidence, not claims:** Screenshots, data, competitor comparisons.
- **No jargon without definition:** If you use AEO, define it the first time.
- **Acknowledge trade-offs:** "This approach prioritizes speed over depth. We'll add depth in Phase 2."
- **End with action:** Every section should move them closer to saying yes.

## Follow-Up Sequence

After proposal send, track in `11-Ops/deal-pipeline.md`:

| Day | Action | Channel | Message |
|---|---|---|---|
| Day 1 | Send proposal | Email | Proposal + executive summary |
| Day 3 | Follow-up | Email | "Quick question about the timeline" |
| Day 5 | Value-add | Email | Share relevant article/case study |
| Day 7 | Check-in | Email/LinkedIn | "Any questions I can answer?" |
| Day 10 | Urgency | Email | "Two spots left for Q[X] starts" |
| Day 14 | Break-up | Email | "If timing isn't right, let's stay in touch" |
| Day 30 | Nurture | Newsletter | Add to nurture list if no response |

## HITL Gate: Proposal Approval

Before any proposal goes to a prospect, it must pass strategist review:
- [ ] Pricing is correct (no unauthorized discounts)
- [ ] Scope matches tier (no scope creep)
- [ ] Case studies are accurate and client-permitted
- [ ] Competitive claims are factual and defensible
- [ ] Timeline is realistic (not over-promising)
- [ ] Brand voice is consistent
- [ ] No forbidden phrases
- [ ] Prospect name is correct throughout (embarrassing but common error)

## Escalation Rules

- **Prospect audit reveals red flag (penalized site, fake traffic, major technical debt):** Flag for bizdev before pitching. May need to decline the prospect.
- **Active litigation with current client:** Hard stop. Do not pitch until resolved.
- **Prospect requests pricing before audit:** Provide tier ranges, but insist on audit for accurate scoping.
- **Prospect is a competitor or potential conflict:** Escalate to founder for conflict-of-interest review.
- **Case study client withdraws permission:** Remove immediately, find alternative.
- **Proposal deadline is <48h:** Prioritize, but do not skip strategist review.
- **Prospect asks for custom pricing not in tier structure:** Requires founder approval.

## Output Paths
- `11-Ops/pitches/[prospect]-YYYY-MM-DD.md`
- `11-Ops/deal-pipeline.md` (update status and notes)
- `11-Ops/agent-logs/pitch-agent/YYYY-MM-DD-run-id.md`
