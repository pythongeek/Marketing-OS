---
name: local-seo-agent
description: "Manage local SEO, Google Business Profile optimization, geo-grid ranking tracking, review response automation, and multi-location programmatic SEO for the AgenticMarketingPro operating system. Use when optimizing GBP listings, tracking local pack rankings, managing review responses, building local citations, or running local SEO audits for multi-location service businesses. Covers GBP posts, Q&A, photo optimization, and local schema deployment."
---

# Local SEO Agent

Manages local SEO at scale: GBP, geo-grid, reviews, citations, local schema.

## Quick Start

1. **Read client locations:** `01-Clients/[client]/local-seo/locations.md` or onboarding.
2. **Read review data:** Recent reviews across all locations.
3. **Read geo-grid data:** `01-Clients/[client]/local-seo/geo-grid-tracker.md`.
4. **Audit GBP listings:** Check completeness, posts, photos, Q&A, attributes.
5. **Track rankings:** Run geo-grid for target keywords per location.
6. **Manage reviews:** Respond to new reviews (positive and negative).
7. **Build citations:** Ensure NAP consistency across directories.
8. **Write updates:** Update local SEO files in vault.
9. **Log run:** `11-Ops/agent-logs/local-seo-agent/YYYY-MM-DD-run-id.md`.


## Interactive Mode (Form-First)

When this skill needs data that doesn't exist in the vault, it generates an interactive HTML form instead of failing silently.

### How It Works

1. **Check vault** for required data (client context, configs, prior outputs)
2. **If data is missing** → generate the appropriate form via `FormEngine`
3. **Present the form** to the user and wait for the JSON response
4. **Process the response** → create vault artifacts, update configs, or run the analysis

### Form Generation

```bash
python infrastructure/ui/form_engine.py --local-seo
# Fill the form in your browser, save the JSON response
# Then tell the agent: "I filled the form"
```

### After Form Submission

```bash
# The agent reads the response and proceeds with the workflow
# Response file: forms/local-seo-response.json
```

### Security

- **Sensitive data** (API keys, passwords) goes to `.env` only — NEVER to the vault
- **Application passwords** (WordPress) are used instead of login passwords
- All password fields are masked in the HTML form
- Form responses are local to your machine

## GBP Optimization Checklist (Per Location)

### Profile Completeness
- [ ] Business name is exact, no keyword stuffing
- [ ] Category is primary and accurate (most specific possible)
- [ ] Secondary categories added (max 9)
- [ ] Description is 750 chars, includes services and location naturally
- [ ] Phone number matches website NAP exactly
- [ ] Website URL is correct and UTM-tagged for tracking
- [ ] Hours are accurate and updated for holidays/special hours
- [ ] Service area is defined (if service-area business)
- [ ] Attributes are filled (wheelchair accessible, women-led, etc.)
- [ ] Products/services listed with descriptions and prices (if applicable)
- [ ] Booking link or appointment URL added

### Posts & Updates
- [ ] Weekly GBP post (update, offer, event, or product)
- [ ] Posts include photo, CTA button, and UTM link
- [ ] Posts use relevant keywords naturally
- [ ] No duplicate posts across locations (customize per location)

### Photos
- [ ] Exterior photo (street view, signage)
- [ ] Interior photos (workspace, team)
- [ ] Team photos (with names if possible)
- [ ] Product/service photos
- [ ] Logo and cover photo
- [ ] Minimum 10 photos per location
- [ ] Photos optimized: file name includes location, <5MB, good resolution

### Q&A
- [ ] Pre-populate 5–10 common questions with answers
- [ ] Monitor for new questions, answer within 24h
- [ ] Answers include keywords naturally
- [ ] Flag inappropriate questions for removal

### Reviews
- [ ] New reviews responded to within 24h
- [ ] Positive reviews: thank + specific detail + soft CTA
- [ ] Negative reviews: acknowledge + apologize + take offline + no excuses
- [ ] Review response templates are location-specific, not generic
- [ ] Review generation campaign active (SMS/email follow-up)

## Geo-Grid Ranking Tracking

Track local pack rankings from multiple points within the service area:

```markdown
---
type: client-campaign-log
client: [client-name]
last_updated: YYYY-MM-DD
tags: [client/[name], type/local-seo]
---

# Geo-Grid Rankings — [Location] — YYYY-MM-DD

## Keywords Tracked
| Keyword | Grid Point 1 | Grid Point 2 | Grid Point 3 | Grid Point 4 | Grid Point 5 | Avg Rank |
|---|---|---|---|---|---|---|
| [keyword 1] | 3 | 2 | 4 | 3 | 2 | 2.8 |
| [keyword 2] | 5 | 4 | 6 | 5 | 4 | 4.8 |

## Trend (vs. last month)
| Keyword | Last Month Avg | This Month Avg | Change | Driver |
|---|---|---|---|---|

## Map Visibility Score
[Weighted average of rankings across all grid points and keywords]
```

## Review Response Templates

### Positive Review (4–5 stars)
"Thank you [Name] for your kind words about [specific service mentioned]. We're thrilled that [specific detail from review]. Our team at [location] takes pride in [relevant value]. If you ever need anything else, don't hesitate to reach out. — [Team Member Name], [Location]"

### Negative Review (1–2 stars)
"Hi [Name], thank you for taking the time to share your feedback. We sincerely apologize that [specific issue mentioned]. This is not the experience we strive to provide. Please contact us directly at [phone/email] so we can make this right. — [Manager Name], [Location]"

### Neutral Review (3 stars)
"Thank you [Name] for your feedback. We appreciate you sharing both what worked and what we can improve. We'd love the chance to earn a 5-star experience next time. Please reach out at [contact] if you'd like to discuss further. — [Team Member Name], [Location]"

## Citation Building & NAP Consistency

### Top Citation Sources (in priority order)
1. Google Business Profile
2. Apple Maps / Apple Business Connect
3. Bing Places
4. Yelp
5. Facebook Business
6. Yellow Pages / YP.com
7. BBB (Better Business Bureau)
8. Industry-specific directories (e.g., Healthgrades for medical, Avvo for legal)
9. Local chamber of commerce
10. City/regional directories

### NAP Consistency Rules
- Name: Exact match everywhere (no variations like "LLC" vs. "Inc." unless legally required)
- Address: USPS-standardized format everywhere
- Phone: Local number preferred over toll-free for local SEO
- Website: Same URL everywhere (no variations with/without www, http/https)
- Hours: Exact match across all platforms

Audit NAP quarterly and fix discrepancies within 30 days.

## Local Schema

Deploy LocalBusiness schema on homepage and location pages:

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "[Business Name]",
  "image": "[URL]",
  "@id": "[URL]",
  "url": "[URL]",
  "telephone": "[phone]",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "[street]",
    "addressLocality": "[city]",
    "addressRegion": "[state]",
    "postalCode": "[zip]",
    "addressCountry": "[country]"
  },
  "geo": {
    "@type": "GeoCoordinates",
    "latitude": [lat],
    "longitude": [lng]
  },
  "openingHoursSpecification": [{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "opens": "09:00",
    "closes": "17:00"
  }],
  "priceRange": "$$",
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "[rating]",
    "reviewCount": "[count]"
  }
}
```

## Multi-Location Programmatic SEO

For clients with 5+ locations, use the pSEO approach:
- **Template:** Location page with unique content per city
- **Variables:** City name, neighborhood highlights, local team photos, local reviews, service area map
- **URL structure:** `/locations/[city-state]` or `/[service]-in-[city]`
- **Internal linking:** Every location page links to nearest 3 locations + main service page

## Escalation Rules

- **Negative review with false claims or legal threat:** Escalate to strategist + compliance-agent
- **GBP suspension or listing removal:** Escalate immediately, begin reinstatement process
- **NAP inconsistency across >5 directories:** Escalate to strategist for cleanup priority
- **Geo-grid shows declining rankings for 2+ months:** Investigate with competitor-intel + tech-seo-auditor
- **Review generation campaign flagged by platform:** Stop immediately, escalate to compliance-agent
- **Duplicate GBP listings found:** Merge or remove, escalate if complex

## Output Paths
- `01-Clients/[client]/local-seo/`
- `01-Clients/[client]/technical-fix-queue.md` (for schema/technical issues)
- `10-Analytics/anomaly-log.md` (for ranking drops)
- `11-Ops/agent-logs/local-seo-agent/YYYY-MM-DD-run-id.md`
