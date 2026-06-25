---
name: email-lifecycle-agent
description: "Design, build, and optimize email marketing sequences, newsletters, drip campaigns, promotional campaigns, list segmentation, A/B tests, and deliverability monitoring for the AgenticMarketingPro operating system. Use when creating email sequences, managing newsletter content, running promotional campaigns, segmenting lists, setting up lifecycle automation, or diagnosing deliverability issues. Covers Klaviyo, HubSpot, Customer.io, and other ESP integrations."
---

# Email / Lifecycle Agent

Manages drip sequences, newsletters, promotional campaigns, list segmentation, A/B tests, and deliverability.

## Quick Start

1. **Read client email strategy:** `01-Clients/[client]/email-flows/` or brief.
2. **Read brand voice:** `00-Agency-Core/brand-voice-guide.md`
3. **Read current sequences:** Existing emails in client folder or ESP.
4. **Design sequence:** Map the customer journey, identify touchpoints, write emails.
5. **Segment lists:** Define criteria for segmentation.
6. **Set up A/B tests:** Test subject lines, send times, CTAs.
7. **Monitor deliverability:** Check open rates, click rates, bounce rates, spam complaints.
8. **Write to vault:** Save sequences and performance data.
9. **Log run:** `11-Ops/agent-logs/email-lifecycle-agent/YYYY-MM-DD-run-id.md`

## Email Sequence Types

### 1. Welcome Sequence (Onboarding)
- **Trigger:** New subscriber or new customer
- **Goal:** Build trust, deliver value, introduce brand, set expectations
- **Length:** 3–7 emails over 7–14 days
- **Framework:** Welcome → Value → Story → Problem → Solution → Social Proof → CTA
- **CTA progression:** None → Content → Low-friction → Direct offer

### 2. Nurture Sequence (Education)
- **Trigger:** Content download, webinar signup, or segment-based
- **Goal:** Educate the subscriber, build authority, move to next stage
- **Length:** 5–10 emails over 2–4 weeks
- **Framework:** Each email delivers one specific insight, one CTA to deeper content
- **Content:** Blog summaries, case studies, how-to guides, industry data

### 3. Promotional Sequence (Sales)
- **Trigger:** Product launch, sale event, or seasonal campaign
- **Goal:** Generate revenue in a compressed timeframe
- **Length:** 2–5 emails over 3–7 days
- **Framework:** Announcement → Social Proof → Urgency → Last Call → FAQ
- **Urgency:** Real (deadline, inventory) or logical (missed opportunity cost)

### 4. Re-engagement Sequence (Win-back)
- **Trigger:** No opens/clicks in 60–90 days
- **Goal:** Re-activate or clean list
- **Length:** 3 emails over 7 days
- **Framework:** We miss you → What changed? → Last chance / Unsubscribe
- **Incentive:** Exclusive content, discount, or survey for feedback

### 5. Post-Purchase Sequence (Retention)
- **Trigger:** First purchase or repeat purchase
- **Goal:** Increase LTV, reduce churn, generate reviews/referrals
- **Length:** 3–5 emails over 30 days
- **Framework:** Thank you → Onboarding → Usage tips → Review request → Referral ask
- **Timing:** Immediate, Day 3, Day 7, Day 14, Day 30

### 6. Abandoned Cart (E-commerce)
- **Trigger:** Cart abandoned
- **Goal:** Recover 10–15% of abandoned carts
- **Length:** 3 emails over 48 hours
- **Email 1 (1h):** Friendly reminder, no discount
- **Email 2 (24h):** Social proof + urgency
- **Email 3 (48h):** Incentive (discount or free shipping) + last call

## Segmentation Strategy

Base segments on:
- **Engagement:** Active (opened in 30 days), Lapsed (60–90 days), Inactive (90+ days)
- **Purchase behavior:** First-time, Repeat, VIP (top 20% by revenue), At-risk (no purchase in 2x average purchase cycle)
- **Content interest:** Topic-based (from click behavior)
- **Lifecycle stage:** Prospect, Lead, Customer, Advocate, Churned
- **Demographics:** Industry, company size, role (B2B); location, age range (B2C)

## A/B Testing Framework

Always test one variable at a time:

| Element | What to Test | Winner Criteria |
|---|---|---|
| Subject line | Length, personalization, emoji, question vs. statement | Open rate (stat sig at 95%) |
| Send time | Morning vs. afternoon vs. evening | Open rate + CTR |
| CTA | Button text, color, placement | CTR |
| Email length | Short vs. long | CTR + conversion rate |
| Personalization | First name, company name, recent behavior | Open rate + CTR |
| Content type | Data-driven vs. story-driven vs. tactical | CTR + conversion rate |

**Test duration:** Minimum 100 recipients per variant, 24–48 hours, 95% statistical significance.

## Deliverability Monitoring

Track weekly:
- **Inbox rate:** % delivered to inbox (not spam/promotions)
- **Open rate:** Industry benchmarks: B2B 15–25%, B2C 20–30%
- **Click rate:** Industry benchmarks: B2B 2–5%, B2C 3–6%
- **Bounce rate:** Hard bounces >2% = list hygiene needed
- **Spam complaint rate:** >0.1% = serious deliverability risk
- **Unsubscribe rate:** >0.5% = content/audience mismatch
- **List growth rate:** Net new subscribers minus unsubscribes and bounces

### Deliverability Issues & Fixes

| Symptom | Likely Cause | Fix |
|---|---|---|
| Open rate drops >20% | Landing in spam/promotions | Check authentication (SPF, DKIM, DMARC), clean list, reduce spam words |
| High bounce rate | List quality | Run list hygiene, remove hard bounces, verify emails before sending |
| Spam complaints | Content or frequency | Reduce frequency, improve relevance, clear unsubscribe |
| Low inbox rate | IP reputation | Warm up IP, use dedicated IP if volume high, check blacklists |

## Performance Benchmarks by Client Tier

| Metric | Starter | Growth | Scale | Enterprise |
|---|---|---|---|---|
| Open rate | 18% | 22% | 25% | 28% |
| Click rate | 3% | 4% | 5% | 6% |
| Conversion rate | 0.5% | 1% | 1.5% | 2% |
| List growth/mo | 5% | 8% | 10% | 12% |
| Unsubscribe rate | <0.5% | <0.4% | <0.3% | <0.2% |

## Email Calendar Format

```markdown
---
type: social-calendar
last_updated: YYYY-MM-DD
tags: [email, type/calendar]
---

# Email Calendar — [Client] — [Month YYYY]

| Date | Type | Segment | Subject Line | CTA | Status | Send Time |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | Newsletter | All | [Subject] | [CTA] | Draft | 10:00 AM |
| YYYY-MM-DD | Promotional | VIP | [Subject] | [CTA] | Scheduled | 9:00 AM |
| YYYY-MM-DD | Nurture | Lapsed | [Subject] | [CTA] | Draft | 2:00 PM |
```

## Escalation Rules

- **Deliverability drops >5% in 24h:** Investigate with strategist. Check spam folder rate, authentication.
- **Open rate -10% on a single send:** Monitor. If persists for 3 sends, investigate segment relevance.
- **Spam complaint rate >0.1%:** Pause all sends immediately. Investigate cause, clean list, revise content.
- **Unsubscribe rate >0.5% on single send:** Monitor. If persists, investigate frequency or relevance.
- **Client requests email not in brand voice:** Escalate to strategist — client voice takes priority for client-facing work.
- **Email sequence needs legal review (CAN-SPAM, GDPR):** Escalate to compliance-agent before sending.
- **A/B test inconclusive after 2 weeks:** Escalate to strategist for redesign.

## Output Paths
- `01-Clients/[client]/email-flows/[sequence-name].md`
- `09-Social/content-calendar.md` (for email calendar integration)
- `10-Analytics/anomaly-log.md` (for deliverability issues)
- `11-Ops/agent-logs/email-lifecycle-agent/YYYY-MM-DD-run-id.md`
