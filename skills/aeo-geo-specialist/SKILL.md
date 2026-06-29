---
name: aeo-geo-specialist
description: "Optimize content and technical elements for AI search engine visibility including ChatGPT, Perplexity, Google AI Overviews, and Microsoft Copilot citations. Use when deploying FAQ schema, building entity registries, testing LLM prompt visibility, creating corroboration maps, tracking AI citation rates, or auditing content for answer-engine compatibility. Covers Answer Engine Optimization (AEO) and Generative Engine Optimization (GEO) as defined in the AgenticMarketingPro operating system."
---

# AEO/GEO Specialist Agent

Optimizes every page to be cited by AI engines. Schema, entities, corroboration, testing.

## Quick Start

1. **Read current state:** `06-AEO-GEO/ai-citation-tracker.md`, `entity-registry.md`, `corroboration-map.md`
2. **Read target page:** Content from `04-Content-Production/published-index.md` or brief.
3. **Apply AEO/GEO optimizations:** FAQ schema, entity markup, expert quotes, statistic injection.
4. **Test LLM visibility:** Run spot checks against GPT, Perplexity, Gemini, Copilot.
5. **Update trackers:** Write citation results to `ai-citation-tracker.md`.
6. **Log run:** `11-Ops/agent-logs/aeo-geo-specialist/YYYY-MM-DD-run-id.md`.


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --aeo-entity-schema
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/aeo-entity-schema-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## AEO (Answer Engine Optimization)

AEO focuses on traditional answer boxes and featured snippets.

### Tactics
- **FAQ Schema:** Add FAQPage schema to commercial and informational pages.
- **Answer-first structure:** Lead with a 40–60 word direct answer, then elaborate.
- **Question-based H2s:** Frame section headers as questions ("What is X?", "How does Y work?").
- **Table and list formatting:** Use tables for comparisons, numbered lists for steps.
- **Definition boxes:** Define key terms in a highlighted box with schema markup.
- **HowTo schema:** For instructional content, use HowTo schema with steps and tools.

### FAQ Schema Template
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[Question text]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[Answer text, 40-80 words]"
      }
    }
  ]
}
```

Rules for FAQ content:
- Each Q&A must be directly answerable from the page content
- No duplicate questions across pages (cannibalization risk)
- Answers must be factual, not promotional
- Include 3–5 FAQs per page minimum, 8 maximum

## GEO (Generative Engine Optimization)

GEO focuses on being cited by LLMs (ChatGPT, Perplexity, Gemini, Copilot).

### Tactics
- **Entity consistency:** Use the same entity names, product names, and terminology across all pages.
- **Expert quotes:** Include attributed quotes from subject matter experts (real or client team).
- **Statistic injection:** Every claim backed by a citable statistic with source.
- **Corroboration mapping:** Ensure key claims appear on 2+ authoritative third-party sites.
- **Structured data richness:** Use the most specific schema type possible (not just Article).
- **Unique data and research:** Original data, surveys, or studies are highly citable by LLMs.

### Entity Registry

Maintain `06-AEO-GEO/entity-registry.md`:

```markdown
---
type: entity-registry
last_updated: YYYY-MM-DD
tags: [aeo-geo, type/entities]
---

# Entity Registry

## Client: [Client Name]
| Entity | Preferred Label | Alternate Labels | Schema Type | Key Pages | Consistency Status |
|---|---|---|---|---|---|
| [Product Name] | [exact name] | [alt1], [alt2] | Product | /product, /features | Pass |
| [Founder Name] | [exact name] | [alt1] | Person | /about, /blog | Needs fix |
```

### Corroboration Map

Maintain `06-AEO-GEO/corroboration-map.md`:

```markdown
---
type: corroboration-map
last_updated: YYYY-MM-DD
tags: [aeo-geo, type/corroboration]
---

# Corroboration Map

## Key Claims to Corroborate
| Claim | Our Page | Corroboration Source 1 | Corroboration Source 2 | Status |
|---|---|---|---|---|
| [Claim text] | /page | [URL] | [URL] | Fully corroborated |
| [Claim text] | /page | [URL] | Missing | Needs second source |
```

Corroboration sources (in order of authority):
1. Academic papers and journals
2. Industry research reports (Gartner, Forrester, McKinsey)
3. Government data (Census, BLS, EPA)
4. Major news outlets (Reuters, Bloomberg, WSJ)
5. Respected industry blogs and publications
6. Client's own case studies (with third-party validation)

## LLM Prompt Testing

Test client visibility quarterly using `06-AEO-GEO/llm-prompt-tests.md`:

```markdown
---
type: llm-tests
last_updated: YYYY-MM-DD
tags: [aeo-geo, type/tests]
---

# LLM Prompt Tests — [Client] — Q[X] YYYY

## Test Queries
| Query | GPT-4 | Perplexity | Gemini | Copilot | Our Citation? | Rank |
|---|---|---|---|---|---|---|
| "best [category] for [use case]" | [result] | [result] | [result] | [result] | Yes/No | [position] |
| "what is [entity]" | [result] | [result] | [result] | [result] | Yes/No | [position] |
| "[client] vs [competitor]" | [result] | [result] | [result] | [result] | Yes/No | [position] |
```

### Testing protocol:
1. Run 10–15 queries relevant to client's domain.
2. Check if client is cited in the response.
3. Check position/prominence of citation.
4. Check if cited URL is the optimal landing page.
5. Document and compare quarter-over-quarter.

## AI Citation Tracker

Maintain `06-AEO-GEO/ai-citation-tracker.md`:

```markdown
---
type: aeo-tracker
last_updated: YYYY-MM-DD
tags: [aeo-geo, type/citations]
---

# AI Citation Tracker — [Client]

## Baseline (established at onboarding)
- ChatGPT citation rate: [X]% of tracked queries
- Perplexity citation rate: [Y]% of tracked queries
- Gemini citation rate: [Z]% of tracked queries
- Copilot citation rate: [W]% of tracked queries

## Current Quarter
- ChatGPT: [X]% ([+/-] vs baseline)
- Perplexity: [Y]% ([+/-] vs baseline)
- Gemini: [Z]% ([+/-] vs baseline)
- Copilot: [W]% ([+/-] vs baseline)

## Drivers of change
- [What was implemented and its observed effect]
- [Correlations with other metrics: branded search, direct traffic]
```

## Escalation Rules

- **Citation rate drops >50% across 3 LLMs:** Investigate immediately. Check for: site changes, schema errors, content removal, negative third-party mentions.
- **Client cited with wrong/outdated information:** Escalate to content-strategist for content update + to off-page-strategist for corroboration correction.
- **LLM generates false information about client:** Escalate to reputation-agent and strategist. May require PR response.
- **Competitor cited where client should be:** Analyze competitor's AEO/GEO tactics, brief counter-measures.

## Output Paths
- `06-AEO-GEO/ai-citation-tracker.md`
- `06-AEO-GEO/entity-registry.md`
- `06-AEO-GEO/corroboration-map.md`
- `06-AEO-GEO/llm-prompt-tests.md`
- `06-AEO-GEO/schema-library/_index.md`
- `11-Ops/agent-logs/aeo-geo-specialist/YYYY-MM-DD-run-id.md`
