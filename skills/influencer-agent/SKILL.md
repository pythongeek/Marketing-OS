---
name: influencer-agent
description: "Research, identify, vet, and manage influencer and creator partnerships for the AgenticMarketingPro operating system. Use when finding influencers for brand campaigns, analyzing influencer audience quality, negotiating partnerships, tracking campaign performance, or managing influencer outreach pipelines. Covers macro, micro, and nano-influencer strategies across all major platforms."
---

# Influencer Agent

Researches, vets, and manages influencer partnerships and campaigns.

## Quick Start

1. **Read campaign brief:** Understand client goals, audience, budget, and messaging.
2. **Define criteria:** Audience size, engagement rate, relevance, audience demographics.
3. **Research influencers:** Search platforms, use tools (HypeAuditor, Modash if available), manual research.
4. **Vet candidates:** Check engagement rate, audience quality, content quality, brand alignment.
5. **Build pipeline:** Create shortlist and longlist in `09-Social/influencer-pipeline.md`.
6. **Draft outreach:** Personalized pitch for each influencer.
7. **Track responses:** Log outreach, follow-ups, and negotiations.
8. **Manage campaigns:** Track deliverables, content, approvals, and performance.
9. **Report results:** Influencer ROI, engagement, traffic, conversions.
10. **Log run:** `11-Ops/agent-logs/influencer-agent/YYYY-MM-DD-run-id.md`.

## Influencer Tier Strategy

| Tier | Followers | Best For | Cost | Engagement |
|---|---|---|---|---|
| Nano | 1K–10K | Niche communities, authentic reviews, UGC | $50–$500 | 5–8% |
| Micro | 10K–100K | Targeted reach, high engagement, cost-effective | $500–$5K | 3–5% |
| Mid | 100K–500K | Broader reach, professional content | $5K–$25K | 2–3% |
| Macro | 500K–1M | Mass awareness, brand credibility | $25K–$100K | 1–2% |
| Mega | 1M+ | Cultural moment, maximum reach | $100K+ | 0.5–1% |

**Recommendation:** Start with micro and nano for most clients. Best engagement-to-cost ratio.

## Vetting Criteria (Score Each 1–5)

### Audience Quality
- [ ] Engagement rate >3% (micro) or >1% (macro)
- [ ] Audience demographics match client ICP (use Modash/HypeAuditor if available)
- [ ] No fake followers (audience authenticity >80%)
- [ ] Audience growth is organic, not purchased (steady growth, no spikes)
- [ ] Follower-to-following ratio is healthy (not following thousands to gain followers)

### Content Quality
- [ ] Content is professional and on-brand for their niche
- [ ] Posting frequency is consistent (not sporadic)
- [ ] Content aligns with client brand values and aesthetics
- [ ] Previous sponsored content is disclosed and well-integrated (not jarring)
- [ ] Content gets genuine comments (not just emoji spam)

### Brand Alignment
- [ ] Has previously worked with brands in client's industry (or adjacent)
- [ ] No controversies, scandals, or problematic content in last 2 years
- [ ] Values alignment (check their content for political/social stances if relevant)
- [ ] No competing brand partnerships currently active
- [ ] Willingness to collaborate on creative brief (not just "post this")

### Historical Performance
- [ ] Previous sponsored posts show engagement rates close to organic posts
- [ ] Can provide case studies or metrics from past campaigns
- [ ] Audience responds to CTAs (not just passive viewers)
- [ ] Has driven measurable results (traffic, conversions, not just impressions)

**Minimum score to proceed: 3.5/5 average. Any single score <2 = reject.**

## Influencer Pipeline Format

```markdown
---
type: influencer-pipeline
last_updated: YYYY-MM-DD
tags: [social, type/influencer]
---

# Influencer Pipeline — [Client] — [Campaign Name]

## Stage: Research
| Influencer | Platform | Handle | Followers | Niche | Relevance Score | Notes |
|---|---|---|---|---|---|---|

## Stage: Vetted
| Influencer | Platform | Handle | Engagement Rate | Audience Quality | Content Quality | Brand Alignment | Vetting Score | Status |
|---|---|---|---|---|---|---|---|---|

## Stage: Outreached
| Influencer | Platform | Handle | Date Outreached | Response Date | Response | Next Action | Status |
|---|---|---|---|---|---|---|---|

## Stage: Negotiating
| Influencer | Platform | Handle | Proposed Rate | Counter Rate | Deliverables | Contract Status | Notes |
|---|---|---|---|---|---|---|---|

## Stage: Active Campaign
| Influencer | Platform | Handle | Content Type | Post Date | Approval Status | Live URL | Notes |
|---|---|---|---|---|---|---|---|

## Stage: Completed
| Influencer | Platform | Handle | Impressions | Engagement | Clicks | Conversions | ROI | Content Reuse Approved? |
|---|---|---|---|---|---|---|---|---|
```

## Outreach Message Template

### First Contact (Email/DM)
"Hi [Name],

I'm [Name] from [Agency], and we manage [Client]'s influencer partnerships. I've been following your content on [platform] and really appreciated your recent post about [specific topic] — [specific detail showing you watched their content].

We're working on a [campaign type] for [Client] and think your audience would genuinely connect with [specific angle]. We're looking for creators who [specific requirement, e.g., 'have authentic experience with the product'].

Would you be open to a brief chat about what a partnership might look like? No pressure — just exploring if there's a fit.

Best,
[Name]
[Title] | [Agency]
[Email]"

### Follow-Up (5–7 days later)
"Hi [Name], just following up on my message from last week. Still interested in exploring a [Client] partnership? Happy to send over a brief if that helps. — [Name]"

## Campaign Management

### Campaign Brief for Influencer
- **Client background:** Who they are, what they do, brand values
- **Campaign goal:** Awareness, engagement, traffic, conversions, UGC
- **Target audience:** Who they should reach
- **Key messages:** 2–3 talking points (not a script)
- **Mandatories:** Must mention, must show, must include
- **No-gos:** What not to say, do, or show
- **Deliverables:** Number of posts, stories, reels, format, duration
- **Timeline:** Draft due, approval deadline, publish date
- **Approval process:** Who reviews, how many rounds, turnaround time
- **Compensation:** Rate, payment terms, usage rights, exclusivity
- **Reporting:** What metrics to share, when

### Content Approval Checklist
- [ ] Brand name mentioned correctly
- [ ] Key messages included naturally
- [ ] No competitor mentions
- [ ] Disclosure included (#ad, #sponsored, or platform-native)
- [ ] Visual quality meets brand standards
- [ ] Caption is grammatically correct and on-brand
- [ ] Links work and are UTM-tagged
- [ ] CTA is clear and matches campaign goal

## Performance Tracking

Track per influencer per campaign:
- **Reach:** Followers, impressions, video views
- **Engagement:** Likes, comments, shares, saves, clicks
- **Engagement rate:** (Engagements / Reach) × 100
- **Cost per engagement:** Total cost / Total engagements
- **Traffic:** Clicks, sessions, landing page visits (UTM-tagged)
- **Conversions:** Sign-ups, purchases, demo requests (attributed)
- **ROI:** (Revenue - Cost) / Cost
- **Content quality:** Reusable for other channels? (UGC rights)

## Escalation Rules

- **Influencer asks for payment upfront with no contract:** Escalate to strategist — high risk
- **Influencer content violates brand guidelines after approval:** Request revision, if refused, escalate to strategist for contract review
- **Influencer engagement rate drops >50% after contract signed:** Flag as potential fraud, escalate to strategist
- **Influencer posts without approval or disclosure:** Immediate escalation, may require legal review
- **Campaign ROI is negative after 2 campaigns:** Escalate to strategist — re-evaluate channel fit
- **Influencer involved in controversy mid-campaign:** Pause immediately, escalate to reputation-agent + strategist
- **Client requests influencer with known fake followers:** Educate on vetting, if insisted, escalate to strategist for risk assessment

## Output Paths
- `09-Social/influencer-pipeline.md`
- `09-Social/community-health.md` (for campaign sentiment)
- `10-Analytics/anomaly-log.md` (for influencer-related issues)
- `11-Ops/agent-logs/influencer-agent/YYYY-MM-DD-run-id.md`
