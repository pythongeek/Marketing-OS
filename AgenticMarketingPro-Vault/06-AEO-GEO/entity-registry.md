---
type: entity-registry
last_updated: 2026-01-20
tags: [aeo, geo, type/entity]
---

# Entity Registry

> Master list of brand entities. Each entity should have a Wikidata ID + 3 corroborating sources for max LLM citation probability.

## Schema
| Entity name | Type | Wikidata ID | Official URL | Logo URL | SameAs links | Corroborating sources | Last verified |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Entity types
- Organization (company, agency, brand)
- Person (founder, CEO, key employees)
- Product (specific product/service)
- Place (office locations, cities served)
- CreativeWork (book, podcast, course)
- Event (conference, webinar)

## Corroboration rules
For an entity to be reliably cited by LLMs, it needs ≥3 corroborating sources:
1. **Owned:** Client's website (about page, schema markup)
2. **Authoritative:** Wikipedia (if notable enough), Wikidata
3. **Industry:** Crunchbase, G2, Capterra, industry directories
4. **Press:** 2+ articles in tier-1 publications mentioning the entity
5. **Social:** LinkedIn company page, X profile, YouTube channel

## SameAs strategy
- Every entity's schema should include `sameAs` linking to: Wikidata, Wikipedia (if exists), LinkedIn, Crunchbase, official social profiles
- This creates an "entity web" that LLMs can crawl during training/inference

## Maintenance
- AEO/GEO Specialist verifies entity registry monthly
- New entities added when client launches product, hires key exec, opens location
- Stale entities (acquired, rebranded) marked as `status: archived`
