---
name: cro-agent
description: "Design, run, and analyze conversion rate optimization experiments including A/B tests, multivariate tests, landing page optimization, funnel analysis, and UX audits for the AgenticMarketingPro operating system. Use when optimizing landing pages, designing A/B tests, analyzing conversion funnels, identifying friction points, or running user experience audits. Covers hypothesis design, experiment setup, statistical significance, and implementation of winning variants."
---

# CRO Agent

Designs, runs, and analyzes conversion rate optimization experiments.

## Quick Start

1. **Read funnel data:** `10-Analytics/funnel-analysis.md`
2. **Identify friction:** Find the highest drop-off stage in the conversion funnel.
3. **Form hypothesis:** Why are users dropping off? What change would improve conversion?
4. **Design experiment:** Define control, variant, success metric, duration, sample size.
5. **Build test:** Coordinate with tech-seo-auditor or client dev team for implementation.
6. **Run experiment:** Monitor daily for anomalies or early significance.
7. **Analyze results:** Statistical significance, confidence interval, business impact.
8. **Implement winner:** Coordinate implementation with client or dev team.
9. **Document learnings:** Write to experiment log and update playbooks.
10. **Log run:** `11-Ops/agent-logs/cro-agent/YYYY-MM-DD-run-id.md`.

## Experiment Design Framework

### The CRO Hypothesis Formula
"Because we observed [data/qualitative insight], we believe that changing [element] from [current state] to [new state] for [audience] will cause [metric] to [increase/decrease]."

**Example:** "Because we observed 65% drop-off on the pricing page, we believe that adding a 'start free' CTA above the fold instead of 'schedule demo' for mobile visitors will cause trial signups to increase by 15%."

### Experiment Types

| Type | When to Use | Minimum Sample | Duration |
|---|---|---|---|
| A/B Test | Test one element change | 100 per variant | 1–2 weeks |
| Multivariate | Test multiple elements simultaneously | 500 per combination | 2–4 weeks |
| Before/After | No split testing capability | Historical data | 2–4 weeks |
| Sequential | Test one change after another | 100 per period | 2+ weeks total |

### Success Metrics by Funnel Stage

| Stage | Primary Metric | Secondary Metrics |
|---|---|---|
| Awareness | Click-through rate (CTR) | Bounce rate, time on page |
| Interest | Engagement rate (>60s) | Scroll depth, pages per session |
| Consideration | Add to cart / demo request | Form completion rate, pricing page views |
| Conversion | Purchase / sign-up | Revenue per visitor, checkout completion |
| Retention | Repeat purchase / activation | Time to first value, NPS |

### Statistical Significance Rules

- **Minimum confidence:** 95% (p < 0.05)
- **Minimum sample:** 100 conversions per variant
- **Minimum duration:** 1 full business cycle (typically 7 days) to capture day-of-week effects
- **Early stopping:** Do not stop early unless: p < 0.01 AND sample >200 per variant AND duration >7 days
- **Practical significance:** The lift must be large enough to justify implementation effort (typically >5% relative lift)

## Landing Page Optimization Checklist

### Above the Fold (First 600px)
- [ ] Headline matches ad/search intent (message match)
- [ ] Subheadline clarifies the value proposition
- [ ] Hero image or video is relevant and high-quality
- [ ] Primary CTA is visible without scrolling
- [ ] No navigation distractions (minimal or no header nav)
- [ ] Social proof is visible (logos, testimonials, user count)
- [ ] Page loads in <2.5 seconds (LCP)

### Below the Fold
- [ ] Problem section (PAS framework)
- [ ] Solution/features with benefits (not just features)
- [ ] Social proof: testimonials, case studies, reviews, ratings
- [ ] Trust signals: security badges, guarantees, certifications
- [ ] FAQ section (handles objections)
- [ ] Final CTA with urgency or risk reversal
- [ ] Footer with contact info, privacy policy, terms

### Form Optimization
- [ ] Minimum fields (every field is a friction point)
- [ ] Inline validation (don't wait for submit)
- [ ] Progress indicator for multi-step forms
- [ ] Error messages are specific and helpful
- [ ] Auto-fill enabled where possible
- [ ] Mobile-optimized (thumb-friendly inputs)
- [ ] Clear privacy statement near submit button

### CTA Optimization
- [ ] Button color contrasts with page
- [ ] Button text is specific ("Get My Free Audit" not "Submit")
- [ ] Only one primary CTA per section
- [ ] CTA repeated 2–3 times on long pages
- [ ] Sticky CTA on mobile for long pages
- [ ] Urgency is real (deadline, limited spots) or logical (cost of inaction)

## Experiment Log Format

```markdown
---
type: lift-studies
client: [client-name]
last_updated: YYYY-MM-DD
tags: [cro, type/experiment]
---

# CRO Experiment Log — [Client]

## Experiment: [Name]
- **Hypothesis:** [Formula-based hypothesis]
- **Page/Element:** [URL or element]
- **Control:** [Description]
- **Variant:** [Description]
- **Success Metric:** [Primary metric]
- **Secondary Metrics:** [List]
- **Traffic Split:** 50/50
- **Start Date:** YYYY-MM-DD
- **End Date:** YYYY-MM-DD (or ongoing)
- **Expected Duration:** [X days]
- **Minimum Sample:** [N per variant]

## Results
| Metric | Control | Variant | Lift | Significance |
|---|---|---|---|---|

## Conclusion
- [Accept / Reject / Inconclusive] hypothesis
- Business impact: $[revenue] per month if implemented
- Implementation recommendation: [Apply / Iterate / Abandon]
- Next experiment: [What to test next based on learnings]
```

## Funnel Friction Analysis

For each funnel stage, identify:
- **Where:** Specific page or step
- **What:** What's causing drop-off (analytics + heatmap + user feedback)
- **Why:** Root cause hypothesis (confusing UX, too much friction, missing trust)
- **Fix:** Proposed experiment or change
- **Impact:** Estimated conversion improvement

Priority matrix: `Impact × Confidence × Ease`

## Heatmap & Session Recording Review

Monthly review (if client has Hotjar, Clarity, or similar):
- **Rage clicks:** Where do users click repeatedly in frustration?
- **Dead clicks:** Where do users click expecting something to happen?
- **Scroll depth:** How far do users scroll? Is key content below the fold?
- **Form abandonment:** Where do users drop off in forms?
- **Mobile vs. desktop:** Are mobile users having different friction points?

## UX Audit Checklist (Quarterly)

- [ ] All forms submit correctly and confirmation messages display
- [ ] Error messages are helpful and specific
- [ ] Navigation is intuitive (3-click rule for key actions)
- [ ] Search function works and returns relevant results
- [ ] Mobile experience is fully functional (no desktop-only features)
- [ ] Page speed is acceptable on 3G/4G connections
- [ ] Accessibility: alt text, color contrast, keyboard navigation, screen reader compatibility
- [ ] Broken links: none (or <1% of total)
- [ ] 404 page is helpful and branded
- [ ] Checkout/payment process is seamless and secure

## Escalation Rules

- **Experiment shows >20% negative lift:** Pause immediately, investigate, don't wait for significance
- **Form or checkout broken during experiment:** Pause all tests, fix issue, restart after verification
- **Client requests test that violates best practices:** Escalate to strategist (e.g., dark patterns, deceptive design)
- **Statistical significance never reached after 4 weeks:** Escalate to strategist — may need larger sample or different hypothesis
- **Test results contradict established UX best practices:** Document, investigate, escalate if needed
- **Client wants to implement non-significant winner:** Escalate to strategist — explain why this is risky

## Output Paths
- `10-Analytics/funnel-analysis.md`
- `10-Analytics/conversion-lift-studies.md`
- `01-Clients/[client]/technical-fix-queue.md` (for UX fixes)
- `11-Ops/agent-logs/cro-agent/YYYY-MM-DD-run-id.md`
