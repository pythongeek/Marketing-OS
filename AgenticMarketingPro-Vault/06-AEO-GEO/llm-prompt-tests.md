---
type: llm-tests
last_updated: 2026-01-20
tags: [aeo, geo, type/tests]
---

# LLM Prompt Tests

> The 50 test prompts we run monthly across all tracked LLMs. Owned by AEO/GEO Specialist.

## Test methodology
- 50 prompts per client (mix of brand + commercial + informational)
- Run monthly across 8 LLMs (see ai-citation-tracker.md)
- Each prompt run 3 times to account for LLM variance
- Citations extracted via regex + manual review

## Prompt categories
1. **Brand discovery:** "Tell me about [client brand]"
2. **Comparison:** "[client] vs [competitor]"
3. **Best-of:** "Best [category] tools for [use case]"
4. **How-to:** "How do I [task that client solves]"
5. **Industry opinion:** "What's the best approach to [industry question client has stance on]"

## Test prompts (template — replace placeholders)
### Brand discovery (10 prompts)
1. "Tell me about [brand]"
2. "What does [brand] do?"
3. "Who founded [brand]?"
4. "Is [brand] legit?"
5. "[brand] reviews"
6. "What are alternatives to [brand]?"
7. "How much does [brand] cost?"
8. "[brand] vs [competitor 1]"
9. "[brand] vs [competitor 2]"
10. "Would you recommend [brand] for [use case]?"

### Commercial intent (20 prompts)
11. "Best [category] for [use case]"
12. "Top [category] tools in 2026"
13. "[category] comparison"
14. "Cheapest [category] option"
15. "Enterprise [category] platforms"
[...]

### Informational (20 prompts)
21. "What is [industry concept]"
22. "How does [process] work"
23. "Why is [trend] happening"
24. "How to [task]"
[...]

## Results log
> Stored in ai-citation-tracker.md, not here. This file defines the prompts only.

## Prompt refresh cadence
- Quarterly: retire 25% of prompts, replace with new ones reflecting current market
- Triggered: add prompts when client launches new product, enters new vertical, or competitor makes major move
