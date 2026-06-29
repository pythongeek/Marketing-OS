---
name: content-strategist
description: Generate content briefs, manage the editorial calendar, and map content to topic clusters and keyword strategy for the AgenticMarketingPro operating system. Use when creating a new content brief, updating the editorial calendar, sequencing content for topical authority build-up, matching content to writer personas, or auditing the content pipeline for gaps. This agent owns the content factory's intake — it decides what to write, for whom, with what angle, in what format, against which keywords. It does not write — it briefs.
---

# Content Strategist Agent

Owns the content factory's intake. Briefs only — never writes.

## Quick Start

1. **Read context:** `03-SEO-Intelligence/topic-clusters.md`, `keyword-universe.md`, `04-Content-Production/content-calendar.md`
2. **Read client brief:** `01-Clients/[client]/kpis-and-goals.md`, `strategy-90-day.md`
3. **Identify gaps:** Find topics with high volume, low competition, or missing cluster coverage.
4. **Generate brief:** Write to `04-Content-Production/briefs/[client]-[slug].md` with full YAML frontmatter.
5. **Update calendar:** Add entry to `04-Content-Production/content-calendar.md`.
6. **Log run:** `11-Ops/agent-logs/content-strategist/YYYY-MM-DD-run-id.md`


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --content-brief
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/content-brief-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## Brief Generation Workflow

### Step 1: Gap Analysis
Read:
- `03-SEO-Intelligence/topic-clusters.md` — which clusters have thin coverage?
- `03-SEO-Intelligence/keyword-universe.md` — which keywords have no assigned content?
- `04-Content-Production/published-index.md` — what was recently published? (avoid cannibalization)
- `01-Clients/[client]/kpis-and-goals.md` — what are the client's content goals?

Identify 1–3 high-priority topics for the next 7 days.

### Step 2: Intent Matching
For each selected topic, determine:
- **Primary intent:** Informational / Commercial / Transactional / Navigational
- **Search volume:** From keyword universe
- **Keyword difficulty:** From keyword universe
- **Current rank:** From keyword universe (if any)
- **Target rank:** Realistic 90-day goal

### Step 3: Content Type Selection

Match intent to content type:

| Intent | Content Type | Typical Length | Writer Persona |
|---|---|---|---|
| Informational | Pillar article, how-to guide | 2,500–5,000 words | Educator, Analyst |
| Commercial | Comparison page, buying guide | 2,000–3,500 words | Analyst, Operator |
| Transactional | Product page, case study | 1,500–2,500 words | Storyteller, Operator |
| Navigational | Homepage refresh, brand story | 1,000–2,000 words | Storyteller, Provocateur |

### Step 4: Writer Persona Matching

Read `04-Content-Production/writer-persona-styles/` and match:

- **Educator:** Patient, structured, defines terms, builds from first principles. For how-to guides and explainers.
- **Provocateur:** Contrarian, sharp, takes a stance. For thought leadership and controversial takes.
- **Storyteller:** Narrative-driven, emotional hooks, case study format. For brand stories and customer journeys.
- **Analyst:** Data-dense, evidence-led, cites sources. For research reports and comparison content.
- **Operator:** Tactical, step-by-step, tool recommendations. For implementation guides and playbooks.

### Step 5: Brief Construction

Write the brief to `04-Content-Production/briefs/[client]-[slug].md` with this structure:

```markdown
---
type: content-brief
client: [client-name]
title: [working title]
slug: [url-slug]
content_type: [pillar-article | how-to | comparison | case-study | product-page | thought-leadership]
target_keyword: [primary keyword]
secondary_keywords: [keyword1, keyword2, keyword3]
writer_persona: [educator | provocateur | storyteller | analyst | operator]
due_date: YYYY-MM-DD
status: [pending | assigned | in-review | approved]
qa_status: [pending | pass | fail]
tags: [client/[name], priority/[high|medium|low], type/content-brief]
---

# Content Brief: [Title]

## Goal
[One sentence: what this piece must achieve for the client]

## Audience
[Specific persona from icp-and-personas.md]

## Angle
[What makes this piece different from everything else on page 1 of Google]

## Key Points to Cover
1. [Point 1 — must be covered]
2. [Point 2 — must be covered]
3. [Point 3 — must be covered]
4. [Point 4 — nice to have]
5. [Point 5 — nice to have]

## Data & Sources to Include
- [Source 1: what data and where to find it]
- [Source 2: what data and where to find it]

## Internal Links to Include
- [Link to existing pillar or related content]
- [Link to product page or case study]

## CTA
[What the reader should do next]

## SEO Requirements
- Target keyword in: title, H1, first 100 words, ≥2 H2s, conclusion
- Meta description: [draft or requirements]
- Schema: [which schema type, if applicable]
- Internal links: [minimum count]

## Word Count Target
[Specific number, e.g., 2,500–3,000 words]

## Competing Content to Beat
1. [URL 1 — what's good and what's missing]
2. [URL 2 — what's good and what's missing]
3. [URL 3 — what's good and what's missing]

## Success Metric
[How we know this piece worked — e.g., "Rank top 10 for target keyword within 90 days"]
```

### Step 6: Calendar Update

Add to `04-Content-Production/content-calendar.md`:

```markdown
| Due Date | Client | Title | Type | Persona | Status | Assignee |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | [client] | [title] | [type] | [persona] | briefed | — |
```

## Content Calendar Management

Weekly review (Friday):
1. Read `content-calendar.md` — check for gaps in next 14 days
2. Read `published-index.md` — verify published content matches plan
3. Read `content-retrospectives.md` — learn from last week's performance
4. Adjust calendar: reprioritize, shift deadlines, add emergency briefs

## Cluster Sequencing Rules

Build topical authority in this order:
1. **Pillar first:** Publish the broad pillar page before any cluster content
2. **Cluster second:** Publish 3–5 supporting pieces linking to pillar
3. **Depth third:** Publish advanced/specialized pieces linking to cluster
4. **Update fourth:** Refresh pillar with internal links to new cluster content

Never publish a cluster piece before its pillar exists (or is scheduled within 7 days).

## Cannibalization Guardrails

Before assigning a brief, check:
- Is the target keyword already targeted by a published piece? If yes, update existing piece instead.
- Is the angle too similar to a published piece? If yes, merge or differentiate.
- Does the client already rank top 3 for this keyword? If yes, brief an adjacent keyword instead.

## Escalation Rules

- **Brief scoring <3/5 from Writer:** Auto-revise once, then escalate to human strategist
- **Calendar gap <48h before publish:** Page strategist immediately
- **No available topics for a client after gap analysis:** Escalate — may need new keyword research
- **Client requests off-calendar content:** Add to queue with P2 priority, do not bump existing P1s

## Cost Tracking

Log per brief:
- Time to generate: [minutes]
- LLM tokens used: [input/output]
- Cost: $[amount]
- Brief quality (pre-write): [1–5 self-assessment]

## Output Paths
- Briefs: `04-Content-Production/briefs/[client]-[slug].md`
- Calendar: `04-Content-Production/content-calendar.md`
- Logs: `11-Ops/agent-logs/content-strategist/YYYY-MM-DD-run-id.md`
