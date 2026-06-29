---
name: revenue-scout
description: "Identify and evaluate untapped revenue channels for the AgenticMarketingPro agency including affiliate partnerships, white-label fulfillment, productized service offerings, retainer upsells, consulting extensions, and SaaS productization opportunities. Use when exploring new revenue streams, evaluating channel ROI potential, building profit models, or updating the agency's revenue plan. Scores each opportunity by effort, risk, and ROI potential."
---

# Revenue Channel Scout

Identifies untapped revenue channels. Scores each by effort vs. ROI.

## Quick Start

1. **Read current revenue:** `11-Ops/profit-plan.md`, `00-Agency-Core/revenue-targets.md`
2. **Read services:** `00-Agency-Core/services-and-pricing.md`
3. **Scan market signals:** Industry trends, competitor moves, client requests.
4. **Evaluate opportunities:** Score each by effort, risk, and ROI.
5. **Write report:** `11-Ops/profit-plan.md` (revenue opportunities section)
6. **Log run:** `11-Ops/agent-logs/revenue-scout/YYYY-MM-DD-run-id.md`


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --revenue-opportunity
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/revenue-opportunity-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Revenue Channel Evaluation Framework

For each opportunity, score on 1–5 scale:

| Dimension | 1 (Low) | 5 (High) |
|---|---|---|
| **Effort to launch** | 1–2 weeks | 6+ months |
| **Ongoing effort** | Minimal | Full-time team |
| **Upfront investment** | <$1K | >$50K |
| **Time to first revenue** | <30 days | >6 months |
| **Scalability** | Linear (hours = revenue) | Exponential (productized) |
| **Margin potential** | <30% | >70% |
| **Strategic fit** | Off-brand | Core to mission |
| **Competitive moat** | Commodity | Defensible |

**Score = average of all dimensions. ≥4.0 = greenlight. 3.0–3.9 = investigate further. <3.0 = pass.**

## Revenue Channel Types

### 1. SEO Retainer Clients (Active)
- **Status:** Active — primary revenue
- **Range:** $2,500–$15,000/mo per client
- **Scalability:** Medium (agent OS enables 20+ clients simultaneously)
- **Margin:** 55–68% at scale
- **Action:** Maintain and expand. This is the core business.

### 2. Productized SEO Sprints (High Potential)
- **Status:** Not yet launched
- **Examples:** "100-page pSEO build" ($5K), "AEO audit + fix" ($3K), "12-month link plan" ($2K)
- **Effort:** Medium (template the deliverable once, sell repeatedly)
- **Scalability:** High (no custom scoping per sale)
- **Margin:** 70–80% (templates amortize cost)
- **Action:** Launch 2–3 productized offerings in Q2.

### 3. White-Label Fulfillment (Medium Potential)
- **Status:** Policy says "no" (business-context.md), but evaluate as Year 2 option
- **Effort:** Medium (need separate white-label processes)
- **Scalability:** Very high (other agencies handle sales)
- **Margin:** 40–50% (lower margin, higher volume)
- **Risk:** Compromises direct client relationship needed for vault compounding
- **Action:** Defer to Year 2. Re-evaluate at $250K MRR.

### 4. GEO/AEO Consulting (Very High Potential)
- **Status:** Not yet launched
- **Effort:** Low (we already do this for retainer clients)
- **Scalability:** High (methodology is repeatable)
- **Margin:** 75–85% (high-value, low-delivery cost)
- **Market:** Only ~20% of orgs have started AEO. First-mover opportunity.
- **Action:** Launch as standalone offering in Q2. Price: $3,000–$8,000 one-time audit + $800/mo monitoring.

### 5. Programmatic SEO Builds (High Potential)
- **Status:** Included in Scale tier, but not sold standalone
- **Effort:** High (one-time architecture build)
- **Scalability:** High (same architecture, different data)
- **Margin:** 60–70%
- **Price:** $5K–$30K one-time + $1,500/mo monitoring
- **Action:** Package as standalone offering. Case study required.

### 6. AI Marketing Tools / SaaS (Very High Potential — Year 2+)
- **Status:** Vision item, not yet built
- **Effort:** Very high (product development)
- **Scalability:** Exponential (software margins)
- **Margin:** 80–90%
- **Risk:** High (product-market fit, competition)
- **Action:** Start building internal tools in Q3. Productize in Year 2.

### 7. Affiliate / Partnership Revenue (Low Potential)
- **Status:** Not evaluated
- **Effort:** Low (recommend tools we already use)
- **Scalability:** Low (revenue ceiling)
- **Risk:** Medium (conflict of interest with client recommendations)
- **Action:** Not recommended. Compromises objectivity.

### 8. Training / Courses (Medium Potential)
- **Status:** Not yet launched
- **Effort:** High (content creation, platform)
- **Scalability:** High (record once, sell repeatedly)
- **Margin:** 85%+
- **Action:** Defer to Year 2. Use as SaaS onboarding/training layer.

## Profit Model Template

For each evaluated opportunity, produce:

```markdown
## Opportunity: [Name]

### Scorecard
| Dimension | Score |
|---|---|
| Effort to launch | [1-5] |
| Ongoing effort | [1-5] |
| Upfront investment | [1-5] |
| Time to first revenue | [1-5] |
| Scalability | [1-5] |
| Margin potential | [1-5] |
| Strategic fit | [1-5] |
| Competitive moat | [1-5] |
| **Average** | **[X.X]** |

### Financial Model (Year 1)
| Metric | Value |
|---|---|
| Launch cost | $[X] |
| Monthly operating cost | $[Y] |
| Price per unit | $[Z] |
| Units sold (conservative) | [N] |
| Revenue | $[total] |
| Margin | [pct]% |
| Payback period | [months] |

### Recommendation
[Greenlight / Investigate / Pass] — [one-paragraph justification]
```

## Quarterly Revenue Review

Every quarter, produce a revenue channel review:
1. Score each active and proposed channel
2. Update financial models with actuals
3. Recommend resource reallocation
4. Flag channels approaching maturity or decline
5. Propose new channels based on market signals

## Escalation Rules

- **Any channel scoring >4.5:** Immediate greenlight recommendation to founder
- **Any channel with negative margin after 3 months:** Recommend sunsetting
- **Competitor launches identical offering:** Accelerate timeline or differentiate
- **Client requests service not in current offerings:** Log as signal, evaluate for productization

## Output Paths
- `11-Ops/profit-plan.md` (revenue opportunities section)
- `11-Ops/deal-pipeline.md` (new opportunities)
- `11-Ops/agent-logs/revenue-scout/YYYY-MM-DD-run-id.md`
