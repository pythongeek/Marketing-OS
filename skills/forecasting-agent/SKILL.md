---
name: forecasting-agent
description: "Forecast revenue, traffic, conversions, and marketing performance for the AgenticMarketingPro operating system. Use when projecting MRR growth, forecasting organic traffic trajectories, predicting conversion outcomes, modeling client lifetime value, or running scenario planning for resource allocation. Combines historical data, seasonality patterns, and compounding assumptions to produce realistic projections with confidence intervals."
---

# Forecasting Agent

Models revenue, traffic, and performance trajectories. Produces realistic projections with confidence intervals.

## Quick Start

1. **Read historical data:** `10-Analytics/kpi-attainment.md`, `11-Ops/profit-plan.md`
2. **Read current pipeline:** `11-Ops/deal-pipeline.md`, `01-Clients/` for active client data
3. **Read goals:** `00-Agency-Core/revenue-targets.md`, `01-Clients/[client]/kpis-and-goals.md`
4. **Build model:** Historical trend + seasonality + compounding assumptions
5. **Run scenarios:** Base case, optimistic, pessimistic
6. **Validate assumptions:** Check against historical accuracy of past forecasts
7. **Write forecast:** `10-Analytics/funnel-analysis.md` or client-specific forecast
8. **Log run:** `11-Ops/agent-logs/forecasting-agent/YYYY-MM-DD-run-id.md`


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --forecasting-request
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/forecasting-request-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Revenue Forecasting Model

### Inputs
- **Current MRR:** From `11-Ops/profit-plan.md`
- **Churn rate:** Historical monthly churn %
- **New client pipeline:** `11-Ops/deal-pipeline.md` (weighted by close probability)
- **Expansion revenue:** Upsells, tier upgrades from existing clients
- **Contraction revenue:** Downgrades, scope reductions
- **Seasonality:** Known patterns (e.g., B2B slows in December, e-commerce peaks in Q4)

### Model Structure

```
MRR(t+1) = MRR(t) 
           + New MRR from pipeline × close probability
           - Churned MRR × churn rate
           + Expansion MRR × expansion rate
           - Contraction MRR × contraction rate
           + Seasonality adjustment
```

### Scenario Planning

| Scenario | New Clients | Churn | Expansion | Confidence |
|---|---|---|---|---|
| Pessimistic | 50% of pipeline | 1.5x historical churn | 0% | 90% we hit this |
| Base | 75% of pipeline | Historical churn | Historical expansion | 70% we hit this |
| Optimistic | 100% of pipeline + 1 wildcard | 0.5x historical churn | 2x historical expansion | 50% we hit this |

### Confidence Intervals

Always present forecasts with confidence intervals:
- "Base case: $50K MRR by Q3 (70% confidence). Range: $45K–$55K."
- Never present a single number without a range. Single numbers create false precision.

## Traffic Forecasting Model

### Inputs
- **Current organic sessions:** From GA4
- **Content velocity:** Pieces published per month
- **Keyword trajectory:** How many keywords are moving up vs. down
- **Link velocity:** New referring domains per month
- **Technical health:** Is the site improving or declining?
- **Algorithm risk:** Historical algorithm impact on this client
- **Seasonality:** Industry-specific traffic patterns

### Compounding Assumptions

Content compounding model (conservative):
- Each new content piece generates traffic in month 1, then grows at 10–20% per month for 6 months as it ranks.
- Content decay: After 12 months, traffic declines 5% per month without refresh.
- Content refresh: Updating a piece restores 80% of its peak traffic.

### Traffic Forecast Format

```markdown
---
type: funnel
client: [client-name]
last_updated: YYYY-MM-DD
tags: [forecasting, type/traffic]
---

# Traffic Forecast — [Client] — [Period]

## Current State (Month 0)
- Organic sessions: [X]
- Top 10 keywords: [count]
- Content pieces: [count]
- Referring domains: [count]
- DR: [X]

## Assumptions
- Content velocity: [X] pieces/month
- Average traffic per new piece (month 1): [Y] sessions
- Link velocity: [Z] new domains/month
- Seasonality factor: [X%] (100% = no change)
- Algorithm risk: [low / medium / high]

## Forecast
| Month | Pessimistic | Base | Optimistic | Confidence |
|---|---|---|---|---|
| Month 1 | | | | |
| Month 2 | | | | |
| Month 3 | | | | |
| Month 6 | | | | |
| Month 12 | | | | |

## Key Drivers
- [What matters most for this forecast]
- [What could change the trajectory]

## If We Hit Base Case
- Month 3: [metric]
- Month 6: [metric]
- Month 12: [metric]

## If We Miss Base Case
- Likely cause: [what would drive the miss]
- Mitigation: [what we would do]
```

## KPI Forecasting

For each KPI, forecast trajectory over 90 days:

| KPI | Current | Target | Forecast (Base) | Forecast (Pessimistic) | Forecast (Optimistic) |
|---|---|---|---|---|---|
| Organic sessions | | | | | |
| Keyword rankings (top 10) | | | | | |
| Content published | | | | | |
| Links acquired | | | | | |
| AI citation rate | | | | | |
| Conversion rate | | | | | |
| CPA | | | | | |
| ROAS | | | | | |

## Forecast Accuracy Tracking

Track forecast accuracy to improve models over time:

```markdown
# Forecast Accuracy Log

| Forecast Date | Metric | Forecast | Actual | Variance | Error % | Lesson |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | Organic sessions | | | | | |
```

**Accuracy targets:**
- Month 1 forecast: ±10% error
- Month 3 forecast: ±20% error
- Month 6 forecast: ±30% error
- Month 12 forecast: ±40% error (long-term is inherently uncertain)

If error exceeds target for 2 consecutive forecasts, adjust model assumptions.

## Scenario Planning for Resource Allocation

When strategist asks "what if we do X?":

1. **Define the scenario:** What exactly changes? (e.g., double content velocity, add paid channel, reduce off-page)
2. **Model the impact:** Apply the change to the forecast model.
3. **Compare scenarios:** Present 2–3 options with trade-offs.
4. **Recommend:** Base case vs. scenario A vs. scenario B, with ROI and risk analysis.

Example:
- **Option A (Base):** 4 content pieces/month, 10 links/month → Forecast: 25% organic growth
- **Option B (Content-heavy):** 8 content pieces/month, 5 links/month → Forecast: 35% organic growth, but slower authority build
- **Option C (Link-heavy):** 4 content pieces/month, 20 links/month → Forecast: 20% organic growth, but faster authority and ranking potential

## Escalation Rules

- **90-day forecast variance >30% from actual:** Investigate model assumptions. Are inputs wrong? Is the model missing a variable?
- **Revenue forecast shows agency will miss quarterly target by >20%:** Escalate to founder immediately.
- **Client's forecast shows they will miss their KPI targets by >30%:** Escalate to strategist for strategy pivot.
- **Model requires data not available in vault:** Flag data gap, propose tracking improvements.
- **Forecast assumes compounding that hasn't been observed historically:** Flag assumption as high-risk, present conservative and optimistic ranges.
- **Strategist requests unrealistic forecast:** Escalate to founder if pressured to produce numbers that aren't data-driven.

## Output Paths
- `10-Analytics/funnel-analysis.md` (traffic and conversion forecasts)
- `11-Ops/profit-plan.md` (revenue forecasts)
- `01-Clients/[client]/kpis-and-goals.md` (client-specific KPI forecasts)
- `11-Ops/agent-logs/forecasting-agent/YYYY-MM-DD-run-id.md`
