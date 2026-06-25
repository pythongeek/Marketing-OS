---
type: pseo-data
last_updated: 2026-01-20
tags: [pseo, type/data]
---

# Programmatic SEO — Data Sources

> Master list of data sources powering pSEO templates across clients.

## Active data sources

### [Source 1: e.g., "Acme locations database"]
- **Source type:** Airtable base
- **URL:** [Airtable URL]
- **Refresh cadence:** Daily (auto-sync via n8n)
- **Records:** [count]
- **Used by templates:** [list]
- **Schema:** [field list]

### [Source 2: e.g., "Industry × use-case matrix"]
- **Source type:** Google Sheets
- **URL:** [Sheets URL]
- **Refresh cadence:** Weekly (manual)
- **Records:** [count]
- **Used by templates:** [list]

## Data quality rules
- Every record must have a unique slug (used in URL)
- Required fields cannot be null (validation script runs before publish)
- Records with duplicate content >40% similarity are auto-merged or rejected
- Geocoding for location-based templates must be verified (lat/long within plausible range)

## Data source → template mapping
| Data source | Template | Pages generated | Last batch |
|---|---|---|---|
| | | | |
