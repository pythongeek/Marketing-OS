# SEO Ops Credential Setup Guide — AgenticMarketingPro

**Document:** How to get API keys and credentials for full SEO automation  
**Last Updated:** 2026-07-09  
**Status:** Action Required — User must obtain these credentials

---

## 1. Google Search Console (GSC) — CRITICAL

### What You Get
- Real-time ranking data (clicks, impressions, CTR, position)
- Index coverage status (indexed, not indexed, errors)
- Core Web Vitals reports (LCP, INP, CLS)
- Manual actions and security issues
- Backlink data (top linking sites, internal links)
- Structured data / rich results status

### How to Get Access

**Option A: Full API Access (Recommended for Automation)**

1. Go to https://search.google.com/search-console
2. Add your property: `agenticmarketingpro.com` (Domain property type)
3. Verify ownership via DNS record (recommended) or HTML file
4. Go to https://console.cloud.google.com/
5. Create a new project (or use existing)
6. Enable the **Search Console API**: APIs & Services → Library → Search for "Google Search Console API" → Enable
7. Create credentials: APIs & Services → Credentials → Create Credentials → Service Account
8. Download the JSON key file (this is your `gsc-service-account.json`)
9. In GSC, add the service account email as a **Owner** (Settings → Users and Permissions → Add User)

**What to send me:**
- The service account JSON file contents (or save it securely and give me the path)
- The property URL: `sc-domain:agenticmarketingpro.com` (if domain property) or `https://agenticmarketingpro.com/` (if URL prefix)

**Option B: Read-Only Access (Safer)**

If you don't want to give API access, you can:
1. Share view-only access to your GSC with a dedicated email
2. Export data manually weekly and upload to the system

---

## 2. Bing Webmaster Tools — HIGH PRIORITY

### What You Get
- Bing-specific ranking and indexing data
- IndexNow protocol (instant index notification)
- SEO Analyzer (Bing's own page quality checker)
- Keyword Research Tool (different data from Google)
- Backlinks discovery (sometimes finds links Ahrefs misses)
- Crawl control settings

### How to Get Access

1. Go to https://www.bing.com/webmasters
2. Sign in with Microsoft account (or create one)
3. Add your site: `https://agenticmarketingpro.com/`
4. Verify ownership (HTML meta tag, DNS, or XML file)
5. **For API access:**
   - Go to https://www.bing.com/webmasters/home/api
   - Click "Get API Key"
   - Copy the API key (looks like a long alphanumeric string)

**What to send me:**
- API Key (from Bing Webmaster Tools → API Access)
- Site URL: `https://agenticmarketingpro.com/`

**IndexNow Protocol (Bonus):**
1. Go to https://www.bing.com/indexnow
2. Generate an IndexNow key (random string, 32+ characters)
3. Upload the key file to your site root: `agenticmarketingpro.com/{your-key}.txt`
4. This allows instant index notification to Bing + Yandex + Seznam

**What to send me:**
- IndexNow key (the 32-char string you generated)

---

## 3. Ahrefs API — CRITICAL

### What You Get
- Rank tracking for all keywords
- Backlink profile analysis (new/lost links, DR, UR)
- Content gap analysis (what competitors rank for)
- Site audit data (technical issues)
- Keyword research data (volume, difficulty, CPC)
- Competitor analysis

### How to Get Access

**Important:** Ahrefs API is only available on **Ahrefs Enterprise** plan ($999+/month) or through **Ahrefs APIv3** (credits-based).

**Option A: Ahrefs APIv3 (Recommended — Pay-as-you-go)**

1. Go to https://ahrefs.com/api
2. Sign up for APIv3 (credits-based pricing)
3. Generate an API token
4. Each API call costs credits (e.g., 1 backlink check = ~10 credits)

**What to send me:**
- API Token (from Ahrefs API dashboard)
- Your target domain: `agenticmarketingpro.com`

**Option B: Ahrefs Standard/Advanced (Manual Export)**

If API is too expensive:
1. Use Ahrefs UI to export data manually
2. Upload CSV exports to the system
3. I can process the CSVs and generate reports

**What to send me:**
- Ahrefs login credentials (if you want me to export data), OR
- Weekly CSV exports of: Rank Tracker, Backlinks, Content Gap, Site Audit

**Option C: Alternatives (Cheaper)**

| Tool | API Available | Cost | Coverage |
|------|--------------|------|----------|
| **Semrush** | Yes | $200+/mo plan | Similar to Ahrefs |
| **DataForSEO** | Yes | Pay-as-you-go | Backlinks, rankings, on-page |
| **SerpApi** | Yes | Pay-as-you-go | SERP results only |
| **SEO PowerSuite** | No | One-time $300 | Desktop tool, manual |

**Recommendation:** Start with DataForSEO or SerpApi if Ahrefs API is too expensive.

---

## 4. Google Analytics 4 (GA4) — CRITICAL

### What You Get
- Traffic volume and sources (organic, paid, social, referral)
- User behavior (pages per session, bounce rate, time on page)
- Conversion tracking (form fills, demo requests, signups)
- Audience demographics and interests
- Event tracking (scroll depth, button clicks, downloads)
- E-commerce data (if applicable)

### How to Get Access

1. Go to https://analytics.google.com/
2. Create a GA4 property for `agenticmarketingpro.com`
3. Add a data stream (Web → `https://agenticmarketingpro.com/`)
4. Copy the Measurement ID (looks like `G-XXXXXXXXXX`)
5. Install the GA4 tracking tag on your site (via GTM or directly)

**For API Access (Data API):**

1. Go to https://console.cloud.google.com/
2. Enable the **Google Analytics Data API**: APIs & Services → Library → "Analytics Data API" → Enable
3. Create credentials: APIs & Services → Credentials → Create Credentials → Service Account
4. Download the JSON key file
5. In GA4: Admin → Property Access Management → Add the service account email as **Viewer** or **Analyst**

**What to send me:**
- Service account JSON file (for API access), OR
- GA4 Property ID (looks like `properties/123456789`)
- Measurement ID (`G-XXXXXXXXXX`)

**Option B: Read-Only Sharing**

1. In GA4: Admin → Property Access Management → Add User
2. Add my service account email with "Viewer" role
3. I can pull reports but not modify anything

---

## 5. PageSpeed Insights API — FREE

### What You Get
- Core Web Vitals scores (LCP, INP, CLS) for any URL
- Lab data (simulated) and field data (real users from CrUX)
- Performance diagnostics and recommendations
- Mobile and desktop scores separately

### How to Get Access

**This is completely FREE and takes 2 minutes:**

1. Go to https://console.cloud.google.com/
2. Create a new project (or use existing)
3. Enable the **PageSpeed Insights API**: APIs & Services → Library → Search "PageSpeed Insights API" → Enable
4. Create credentials: APIs & Services → Credentials → Create Credentials → API Key
5. Copy the API key (looks like `AIzaSy...`)

**What to send me:**
- API Key (the `AIzaSy...` string)

**Rate Limits:**
- 100 queries per 100 seconds (free tier)
- Sufficient for weekly batch testing of your top pages

---

## 6. UptimeRobot — FREE TIER AVAILABLE

### What You Get
- Website uptime monitoring (checks every 5 minutes)
- Downtime alerts (email, SMS, webhook)
- Response time tracking
- SSL certificate expiry monitoring
- Multi-location monitoring

### How to Get Access

1. Go to https://uptimerobot.com/
2. Sign up for free account (50 monitors, 5-minute intervals)
3. Create a new monitor:
   - Type: HTTP(s)
   - URL: `https://agenticmarketingpro.com/`
   - Monitoring Interval: 5 minutes
   - Alert Contacts: Add your email
4. **For API access:**
   - Go to Settings → API Settings
   - Generate a Main API Key (read-only) or Monitor-Specific API Key

**What to send me:**
- API Key (from Settings → API Settings)
- Monitor ID (optional, for specific monitor access)

**Pro Plan ($15/month):**
- 1-minute monitoring intervals
- 100 monitors
- Advanced notifications (Slack, Teams, PagerDuty)
- Recommended for production sites

---

## BONUS CREDENTIALS (Optional but Recommended)

### 7. Brand24 / Brandmentions (Brand Monitoring)
- **Purpose:** Track unlinked brand mentions across the web
- **Cost:** Brand24 starts at $79/month
- **Alternative:** Google Alerts (free but limited)
- **What to send me:** API key or RSS feed URL

### 8. HARO / Connectively (PR Queries)
- **Purpose:** Respond to journalist queries for backlinks
- **Cost:** Free tier available; paid plans $19-149/month
- **What to send me:** Login credentials (or you respond manually)

### 9. Profound / Otterly (AI Citation Tracking)
- **Purpose:** Track when LLMs cite your brand
- **Cost:** $50-200/month
- **What to send me:** API key or account access

### 10. Google Ads API (If Running Paid Ads)
- **Purpose:** Automated campaign management and reporting
- **Cost:** Free API, but requires active Google Ads account
- **What to send me:** Developer token + OAuth credentials

---

## SUMMARY: What to Send Me

| # | Tool | Credential Type | How to Get It | Priority |
|---|------|----------------|---------------|----------|
| 1 | **Google Search Console** | Service Account JSON + Property URL | Google Cloud Console → Create Service Account → Add to GSC as Owner | CRITICAL |
| 2 | **Bing Webmaster Tools** | API Key + Site URL | Bing WMT → API Access → Get Key | HIGH |
| 3 | **Ahrefs** | API Token OR CSV exports | Ahrefs APIv3 dashboard OR manual export | CRITICAL |
| 4 | **Google Analytics 4** | Service Account JSON + Property ID | Google Cloud Console → Enable Analytics Data API → Add to GA4 | CRITICAL |
| 5 | **PageSpeed Insights** | API Key (free) | Google Cloud Console → Enable PSI API → Create API Key | HIGH |
| 6 | **UptimeRobot** | API Key | UptimeRobot → Settings → API Settings | HIGH |
| 7 | **Bing IndexNow** | 32-char Key | Bing IndexNow → Generate Key → Upload to site root | MEDIUM |

---

## SECURITY NOTES

1. **Service Account JSON files** contain private keys. Treat them like passwords.
2. **Store them securely** — the system will encrypt them in Supabase credentials table
3. **Never commit them to Git** — use Supabase secrets or environment variables
4. **Use read-only permissions** where possible (Viewer/Analyst roles instead of Admin)
5. **Rotate keys quarterly** for security best practice

---

## NEXT STEPS

1. **Get the credentials above** (start with GSC, GA4, and PageSpeed Insights — they're free)
2. **Send them to me** via the credentials page in the Vercel app
3. **I'll build the automated SEO Ops agents** that pull data and generate reports
4. **Run the first automated report** within 24 hours of receiving credentials

**Start with the free ones (GSC, GA4, PageSpeed Insights, UptimeRobot) — they cover 80% of the SEO Ops workflows!**
