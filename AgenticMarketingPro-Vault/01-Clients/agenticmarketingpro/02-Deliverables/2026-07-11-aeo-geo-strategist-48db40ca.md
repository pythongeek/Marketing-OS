---
type: aeo-geo-strategist
client: agenticmarketingpro
job_id: 48db40ca-4a35-44fa-9211-16a640762f48
generated_at: 2026-07-11T16:47:03.012857+00:00
source: sync-from-db
---

# Advanced SEO Tactics Playbook: The 2025-2026 Edition

*Practices Most Competitors Skip | Optimized for Agentic Marketing Pro*

---

## Executive Summary

This playbook targets the 10% of SEO tactics that drive 90% of competitive differentiation in saturated SERPs. Every section is engineered for advanced practitioners managing enterprise-scale properties, niche authority sites, or AI-search-optimized content ecosystems. Each tactic includes implementation steps, tooling recommendations, and measurable success criteria.

**Philosophy:** In the era of AI Overviews, Zero-Click SERPs, and Generative Engine Optimization (GEO), the competitive moat isn't keywords — it's **entity authority, behavioral signals, and machine-readable trust signals**.

---

## 1. Entity & Knowledge Graph Optimization

### Why This Matters
Google's Knowledge Graph is the substrate beneath AI Overviews, ChatGPT citations, and Gemini's answer synthesis. Most SEOs optimize pages; advanced practitioners optimize **entities** — the real currency of modern search.

### 1.1 Wikidata Presence for Brand & Authors

**Step-by-Step Implementation:**

1. **Audit your brand's Wikidata status** — Search `wikidata.org` for your brand, founder, and key personnel
2. **Create/claim Wikidata items** using the structured form (Q-ID)
3. **Populate critical properties:**
   - `instance of` (P31) → organization type
   - `official website` (P856)
   - `founder` (P112)
   - `country` (P17)
   - `industry` (P452)
   - `LinkedIn company ID` (P4264)
   - `Crunchbase organization ID` (P2088)
4. **Add citations** (P248) for every claim — Google's Knowledge Vault weights sourced entities 3.7x higher (per Stanford KGMiner research)
5. **Link to Wikipedia** if eligible (notability threshold required)

**Tooling:** Mix'n'match (Google Knowledge Graph API), Wikidata Query Service, Scholia for author profiles.

### 1.2 sameAs Markup Architecture

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Agentic Marketing Pro",
  "sameAs": [
    "https://www.wikidata.org/wiki/Q[your-Q-ID]",
    "https://www.linkedin.com/company/agenticmarketingpro",
    "https://twitter.com/agenticmktpro",
    "https://www.youtube.com/@agenticmarketingpro",
    "https://www.crunchbase.com/organization/agenticmarketingpro",
    "https://github.com/agenticmarketingpro",
    "https://medium.com/@agenticmarketingpro"
  ]
}
```

**Implementation Steps:**
1. Generate JSON-LD for Organization, Person (founders), and each Product/Service
2. Deploy site-wide in `<head>` or footer template
3. Validate via [Schema Markup Validator](https://validator.schema.org/) and [Rich Results Test](https://search.google.com/test/rich-results)
4. **Critical:** Use *exact* URL strings as they appear on third-party sites — mismatches collapse the entity graph

### 1.3 Google Business Profile Optimization (Even for Non-Local)

GBP signals feed Google's local knowledge graph, which influences brand authority scoring universally. For multi-location or hybrid businesses:

1. Create GBP for each physical location
2. **Add 100+ photos monthly** — including team, office, products, behind-the-scenes
3. **Post weekly GBP posts** with keywords + CTAs
4. **Q&A seeding** — ask and answer your own questions with full keyword variants
5. **Product/Service catalog** — fully populated with descriptions and photos
6. **Enable messaging** + respond within 1 hour (engagement signal)

### 1.4 Author Entity Optimization

Google's Author Rank is algorithmically active in YMYL and E-E-A-T-sensitive queries.

**Step-by-Step Author Entity Build:**

1. **Create author landing page** at `/author/[name]` with:
   - Full bio with credentials, experience, awards
   - `Person` schema markup with `sameAs` to LinkedIn, Twitter, ORCID, Google Scholar
   - Photo (real, professional)
   - List of credentials with linked sources
2. **Claim Google Scholar profile** for subject-matter experts
3. **Acquire `author` markup on external publications** — Pitch guest posts with proper byline + bio link
4. **Cross-link publications** — every Medium, LinkedIn, Forbes article should link to your author page with `rel="author"`
5. **Implement `knowsAbout`** schema property (emerging — see Search Engine Roundtable coverage) listing 5-10 core expertise areas

---

## 2. SERP Feature Targeting

### The SERP Feature Stack
Modern SERPs are multi-feature battlegrounds. Ranking #1 means nothing if you don't own the feature.

### 2.1 Featured Snippet Capture

**Three Snippet Formats & Attack Plans:**

**a) Paragraph Snippets (40-50 character answer)**
- Target question keywords (5-7 words, "how," "what," "why")
- Place answer in first 50-60 words after a heading
- Format: declarative sentence + supporting detail

**b) List Snippets (Numbered/Bulleted)**
- Use `<ol>` or `<ul>` markup (not just visual bullets)
- Lead each item with a capitalized noun/keyword
- Keep 5-8 items max
- Include the query in the H2 immediately above

**c) Table Snippets**
- Use `<table>` markup with `<thead>` and proper headers
- Include comparison keywords in row/column labels
- Schema-enhance with `ItemList` or comparison schemas

**Implementation Workflow:**
1. Export keywords ranking positions 2-10 in Ahrefs/SEMrush
2. Filter for question keywords (regex: `^(how|what|why|when|where|who|which)`)
3. Identify keywords with existing snippets you don't own
4. Restructure content to match the snippet format
5. Submit via IndexNow — speed matters (first mover advantage measured in days, not weeks)

### 2.2 People Also Ask (PAA) Domination

**PAA Mining & Insertion Strategy:**

1. **Mine PAA at scale** using tools: AlsoAsked, AnswerThePublic, Ahrefs PAA export
2. **Cluster PAAs by intent** — group 8-12 related PAAs per pillar page
3. **Embed PAA answers as FAQ schema** at bottom of pillar pages:
   ```json
   {
     "@context": "https://schema.org",
     "@type": "FAQPage",
     "mainEntity": [
       {
         "@type": "Question",
         "name": "What is entity SEO?",
         "acceptedAnswer": {
           "@type": "Answer",
           "text": "Entity SEO optimizes..."
         }
       }
     ]
   }
   ```
4. **Internal link PAAs to dedicated articles** for deep coverage
5. **Refresh PAA content quarterly** — PAA results decay within 90 days

### 2.3 AI Overview Optimization (AEO)

This is where traditional SEO and Generative Engine Optimization converge.

**AI Overview Capture Tactics:**

1. **Citation-Worthy Content Structure**
   - Lead with 40-50 word definitive answers (answer-first)
   - Use `claim` language ("Studies show...", "According to [Source]...")
   - Include source citations with linked studies
   - Add `about`, `mentions`, `speakable` schema where appropriate

2. **Citation Density Optimization**
   - Reference primary sources (.edu, .gov, peer-reviewed)
   - Use original data (proprietary surveys, tests, data)
   - Include methodology sections — Google AI Overviews cite methodology-rich content 2.4x more

3. **Listicle + Question Pairing**
   - Structure as "Top X Tools for Y" lists
   - Each item: 50-word description with embedded statistics

4. **Speakable Schema for Voice/AI Surfaces**
   ```json
   {
     "@type": "WebPage",
     "speakable": {
       "@type": "SpeakableSpecification",
       "xpath": ["/html/head/title", "/html/body/article/p[1]"]
     }
   }
   ```

### 2.4 Image Pack & Video Carousel Capture

**Image Pack Domination:**
1. **File naming:** keyword-descriptive (e.g., `entity-seo-knowledge-graph-diagram.png`)
2. **Alt text:** contextual, not stuffed (1-8 words, descriptive)
3. **ImageObject schema** with caption, creator, copyrightNotice
4. **Unique images only** — Google deduplicates; original infographics get 4x more pack inclusion
5. **Image sitemaps** with `<image:license>` and `<image:title>` populated

**Video Carousel Capture:**
1. Embed YouTube videos on-page (YouTube owns video SERP)
2. Add `VideoObject` schema with `thumbnailUrl`, `uploadDate`, `duration`
3. Use **YouTube chapters** with keyword-rich timestamps
4. Upload video transcripts (verbatim, not summarized)
5. Include video chapters in description (Google displays them)

### 2.5 Sitelinks Control

Google auto-generates sitelinks, but you can influence them:

1. **Top navigation hierarchy:** Use HTML anchor links, not just CSS menus
2. **Strong internal linking to 4-6 "satellite" pages** from homepage
3. **Brand name anchor text** in title tags of key pages: `Brand | Service | Tagline`
4. **Search box markup:** Add `WebSite` schema with `potentialAction` for sitelinks searchbox

---

## 3. Internal Linking Strategy (PageRank Sculpting 2.0)

### The Mathematics of Authority Flow

Internal links are the only links you fully control. Most sites treat this as an afterthought — that's the opportunity.

### 3.1 PageRank Sculpting — Modernized

**The Old (Broken) Approach:** `nofollow` internal links to "sculpt" PageRank. This hasn't worked since 2009 when Google disabled PageRank sculpting via nofollow.

**The New Approach:**

1. **Crawl your site** with Screaming Frog (max depth)
2. **Calculate PageRank distribution** using a tool like URL Profiler or internal Python script
3. **Identify "PageRank sinks"** — pages receiving lots of internal links but no outbound (orphan-like)
4. **Strategic outbound linking:**
   - From high-PR pages → 3-5 contextual links to money pages
   - From low-PR pages → 1-2 links to related mid-tier pages
   - From money pages → 1-2 links to relevant supporting pages (don't dead-end conversions)

5. **Hub-and-spoke architecture:** Each pillar page should receive 8-15 contextual internal links from cluster content

### 3.2 Anchor Text Diversity Matrix

**Danger:** Over-optimized anchors trigger Penguin-era penalties. Apply this distribution rule:

| Anchor Type | % of Internal Anchors | Example |
|---|---|---|
| Exact match | 5-10% | "entity SEO optimization" |
| Partial match | 25-35% | "best practices for entity SEO" |
| Branded | 20-25% | "Agentic Marketing Pro explains" |
| Naked URL | 5-10% | "agenticmarketingpro.com/entity-seo" |
| Generic | 15-20% | "read this guide," "learn more" |
| LSI/Related | 10-15% | "knowledge graph strategy," "schema markup" |

**Implementation:**
1. Export all internal anchors from Screaming Frog (Internal > All > Anchor)
2. Categorize each by type
3. Calculate % distribution
4. Identify over-optimized clusters (pages with 60%+ exact match)
5. Rewrite anchors over a 90-day period (avoid mass changes)

### 3.3 Contextual Link Placement

**Where links work hardest (research-validated):**

1. **Top of content (first 200 words):** Highest crawl priority, but feels promotional
2. **Mid-content, in contextually relevant paragraphs:** Best balance of UX + authority transfer
3. **Within lists/tables:** High click-through, easy to scan
4. **Footer links (sitewide):** Heavily discounted by Google's reasonable surfer
5. **Sidebar links (templated):** Treated as sitewide, low value

**Best Practice:** Place 60-70% of contextual links mid-content where they enhance user understanding, not at the top where they feel like CTAs.

### 3.4 Orphan Page Prevention

**Orphan Detection Workflow:**

1. **Run Screaming Frog crawl** with "Check Internal Links" enabled
2. **Export all URLs** discovered vs. all URLs in sitemap.xml
3. **Diff the lists** — URLs in sitemap but not crawled = orphans
4. **For each orphan:**
   - Find 2-3 topically related parent pages
   - Add contextual link with relevant anchor
   - Add to navigation if appropriate (e.g., "Resources" menu)
5. **Monthly orphan audit** — new orphans emerge from CMS updates

### 3.5 Topic Cluster Internal Linking

**The Pillar-Cluster Model (Reinforced):**

```
                    [PILLAR PAGE]
                   /      |      \
            [Cluster] [Cluster] [Cluster]
              / | \      /|\        / | \
          [Sub] [Sub] [Sub][Sub] [Sub][Sub]
```

**Rules:**
1. Every cluster page links UP to pillar (with descriptive anchor)
2. Every cluster page links HORIZONTALLY to 2-3 sibling clusters
3. Pillar page links DOWN to all cluster pages
4. Sub-pages link UP to their cluster parent AND pillar

This creates a **topical mesh** that signals comprehensive authority to Google's NLP systems.

---

## 4. E-E-A-T Signals: Implementation Blueprint

### The Four Pillars of Trust

Google's Quality Rater Guidelines explicitly weight E-E-A-T. Here's how to operationalize each:

### 4.1 Experience Signals

**Implementation:**

1. **First-person narrative:** Use "I tested," "I built," "When I deployed this..." throughout content
2. **Original media:** Custom screenshots, behind-the-scenes photos, screen recordings (not stock)
3. **Case studies with metrics:** Real numbers, real timeframes, real outcomes
4. **Process documentation:** Show the work, not just the result
5. **"Last updated" timestamps** with author name and update notes

### 4.2 Expertise Signals

**Implementation:**

1. **Author credentials displayed prominently:**
   - Degree, certifications, years of experience
   - Linked to verifiable sources (LinkedIn profile, certifications site)
2. **Detailed author bios** (300+ words) on every article
3. **Topic-specific author assignment** — dermatology content from a dermatologist
4. **Citation density** — 3-5 authoritative external citations per 1,000 words
5. **"Methodology" or "How we test" pages** for product/content reviews

### 4.3 Authoritativeness Signals

**Implementation:**

1. **Digital PR cadence:** 2-4 HARO/Featured/SourceBottle pitches monthly
2. **Original research publishing:** Annual surveys, data studies (highly linkable)
3. **Speaking engagements** listed on author pages with event URLs
4. **Press coverage** with proper markup
5. **Wikipedia citations** (if eligible)
6. **Backlink profile quality** (assess via Ahrefs DR 70+ focus)

### 4.4 Trustworthiness Signals

**Implementation:**

1. **HTTPS + HSTS** (non-negotiable)
2. **Clear contact information** — physical address, phone, multiple contact methods
3. **Privacy policy, Terms of Service, Cookie Policy** — all dated, all accurate
4. **Editorial policy page** describing content standards and review process
5. **Reviews and testimonials** with `Review` schema markup
6. **Trust seals** (where relevant): BBB, industry accreditations
7. **Accessibility compliance** (WCAG 2.1 AA minimum)
8. **No misleading claims** — back every claim with a source
9. **Secure payment processing** signals (for ecommerce)

### 4.5 E-E-A-T Audit Template

Run quarterly:

| Signal | Check | Status |
|---|---|---|
| Author bios on all content | ☐ | |
| HTTPS sitewide | ☐ | |
| Last updated timestamps | ☐ | |
| External citations per article | ☐ | |
| Original media vs. stock | ☐ | |
| Editorial policy published | ☐ | |
| Credentials linked | ☐ | |
| Original research published YTD | ☐ | |

---

## 5. Log File Analysis for Crawl Intelligence

### Why Most SEOs Skip This
Log files require server access, technical setup, and BigQuery/Excel chops. The insights, however, dwarf any other crawl analysis method.

### 5.1 Setup & Access

**Step 1: Locate Your Log Files**
- Nginx: `/var/log/nginx/access.log`
- Apache: `/var/log/apache2/access.log`
- Cloudflare: Logpull API
- AWS CloudFront: S3 access logs

**Step 2: Extract & Format**

Required fields (parse with regex or log parser):
- Timestamp
- URL requested
- User agent
- Status code
- Bytes sent
- Referer

### 5.2 The Five Critical Analyses

**Analysis 1: Crawl Budget Waste**

Identify Googlebot requests for:
- Faceted nav URLs (`?color=red&size=large`)
- Filtered/sorted URLs
- Pagination loops
- Tag and category archives with no canonical

**Action:** Block via robots.txt, add canonicals, or use noindex.

**Analysis 2: Orphan Page Identification**

URLs Googlebot requests but no internal links point to = discovery-only pages.

**Action:** Add contextual internal links to high-traffic pages.

**Analysis 3: Crawl Frequency by Section**

Export crawl hits per