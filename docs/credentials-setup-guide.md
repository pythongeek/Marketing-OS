# AgenticMarketingPro — SEO Credentials Setup Guide

A step-by-step guide to configuring Google Analytics 4 (GA4) and Bing Webmaster Tools (Bing WMT) for the AgenticMarketingPro operating system.

**Time required:** ~30 minutes total
**Difficulty:** Intermediate (Google Cloud Console knowledge helpful)
**Cost:** Free for both APIs

---

## Table of Contents

1. [Quick Reference: What You Need](#quick-reference)
2. [Part A — Google Analytics 4 (GA4)](#part-a-ga4)
3. [Part B — Bing Webmaster Tools API](#part-b-bing-wmt)
4. [Part C — Adding Credentials to AgenticMarketingPro](#part-c-add-credentials)
5. [Verification Checklist](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Quick Reference: What You Need

| Service | What to Get | Format | Where to Put It |
|---------|------------|--------|-----------------|
| **GSC** ✅ Done | Service account JSON file | File path | `GSC_SERVICE_ACCOUNT_FILE` |
| **GA4** | Service account email + Property ID | Email + ID like `properties/123456789` | `GA4_SERVICE_ACCOUNT` (same JSON) + `GA4_PROPERTY_ID` |
| **Bing WMT** | API key (simple) | 32-char hex string | `BING_API_KEY` |

**Key insight:** You can reuse the SAME Google service account JSON file for both GSC and GA4! Just add the GA4 property access (step A.4 below).

---

## Part A — Google Analytics 4 (GA4)

GA4 uses the **Google Analytics Data API v1** (the new "GA4 API", not the older Universal Analytics one).

### A.1 — Enable the API in Google Cloud Console

1. Go to https://console.cloud.google.com/
2. Select your existing project (`pageforge-466314` — same one as GSC)
3. **APIs & Services → Library** (left sidebar)
4. Search for **"Google Analytics Data API"**
5. Click it → Click **"ENABLE"**
6. Wait ~30 seconds for propagation

> ℹ️ **Already done?** You can skip to A.2. If you can't find the project, see Troubleshooting §6.

### A.2 — Find Your GA4 Property ID

1. Go to https://analytics.google.com/
2. Click **Admin** (gear icon, bottom-left)
3. In the **Property** column, click **Property Settings**
4. Your **Property ID** is shown at the top — looks like `123456789`
5. Copy just the digits

**Set up the env var:**
```
GA4_PROPERTY_ID=properties/123456789
```
Note the `properties/` prefix is required by the API.

### A.3 — Grant Service Account Access to GA4

The same service account that works for GSC (`service-acc-agentic-marketing@pageforge-466314.iam.gserviceaccount.com`) needs access to GA4:

1. In GA4 → **Admin** → **Property** column → **Property Access Management**
2. Click **+** (top right) → **Add users**
3. Paste the service account email: `service-acc-agentic-marketing@pageforge-466314.iam.gserviceaccount.com`
4. Role: **Viewer** (read-only is enough for analytics; use **Analyst** if you want to create audiences)
5. Uncheck "Notify new users by email" (it's a robot)
6. Click **Add**

**Verification (optional):** You should see the service account email listed under users.

### A.4 — Add to .env

Add these lines to `F:\Agentic Marketing Pro\marketing\.env`:

```bash
# Already configured for GSC — reuse for GA4
GSC_SERVICE_ACCOUNT_FILE=C:\Users\Administrator\Downloads\pageforge-466314-75b94d613b1d.json

# Add these for GA4
GA4_PROPERTY_ID=properties/YOUR_PROPERTY_ID_HERE
GA4_SCOPES=https://www.googleapis.com/auth/analytics.readonly
```

### A.5 — Test the Connection

Run this quick test:
```bash
cd "F:\Agentic Marketing Pro\marketing"
python -c "
import os
os.environ['GA4_PROPERTY_ID'] = 'properties/YOUR_ID_HERE'
from infrastructure.api_client.ga4 import GA4Client
client = GA4Client()
print('Sessions last 7 days:', client.get_sessions(days=7))
"
```

If you see a number, you're connected. If you see an error, see Troubleshooting §1.

---

## Part B — Bing Webmaster Tools API

Bing's API is much simpler — just an API key. No service account dance required.

### B.1 — Create a Bing Webmaster Tools Account

1. Go to https://www.bing.com/webmasters
2. Sign in with a Microsoft account (Outlook, Hotmail, or Azure AD)
3. Add your site if not already added: **Settings → Add a Site**
4. Verify ownership (file upload, DNS TXT, or meta tag — same as Google Search Console)

### B.2 — Generate an API Key

1. Go to https://www.bing.com/webmasters
2. **Settings → API Access** (left sidebar)
3. Click **"Generate API Key"** (or "Add" if you have one already)
4. Copy the 32-character hex key (looks like `a1b2c3d4e5f6...`)

> ⚠️ **Important:** Treat this like a password. Anyone with this key can read all your Bing Webmaster data.

### B.3 — Add to .env

```bash
# Bing Webmaster Tools
BING_API_KEY=YOUR_32_CHAR_HEX_KEY_HERE
```

### B.4 — Test the Connection

```bash
cd "F:\Agentic Marketing Pro\marketing"
python -c "
import os
os.environ['BING_API_KEY'] = 'YOUR_KEY_HERE'
from infrastructure.api_client.bing import BingWMTClient
client = BingWMTClient('https://agenticmarketingpro.com/')
print('Sites list:', client.list_sites())
"
```

---

## Part C — Adding Credentials to AgenticMarketingPro

There are 3 places credentials can live. Pick the one that matches your use case:

### Option 1: Local .env file (recommended for local dev)

Add to `F:\Agentic Marketing Pro\marketing\.env`:
```bash
GSC_SERVICE_ACCOUNT_FILE=C:\Users\Administrator\Downloads\pageforge-466314-75b94d613b1d.json
GSC_PROPERTY=sc-domain:agenticmarketingpro.com
GA4_PROPERTY_ID=properties/123456789
BING_API_KEY=***
```

### Option 2: System environment variables

Set in Windows System Properties → Environment Variables:
```
GSC_SERVICE_ACCOUNT_FILE=C:\path\to\service-account.json
GSC_PROPERTY=sc-domain:yourdomain.com
GA4_PROPERTY_ID=properties/123456789
BING_API_KEY=***
```

### Option 3: ~/.amp/secrets.json (project convention)

Create `%USERPROFILE%\.amp\secrets.json`:
```json
{
  "GSC_SERVICE_ACCOUNT_FILE": "C:\\path\\to\\service-account.json",
  "GSC_PROPERTY": "sc-domain:yourdomain.com",
  "GA4_PROPERTY_ID": "properties/123456789",
  "BING_API_KEY": "***"
}
```

This file is auto-loaded by `infrastructure/config.py` if it exists.

### Option 4: Supabase secrets (for hosted Edge Function)

If you want the **Edge Function** (not just the local poller) to access these APIs:

```powershell
# From the project root
npx supabase secrets set GSC_SERVICE_ACCOUNT_FILE=/var/task/service-account.json
npx supabase secrets set GSC_PROPERTY=sc-domain:agenticmarketingpro.com
npx supabase secrets set GA4_PROPERTY_ID=properties/123456789
npx supabase secrets set BING_API_KEY=***
# JSON contents (escape carefully):
npx supabase secrets set GSC_SERVICE_ACCOUNT_JSON="$(Get-Content 'C:\path\to\sa.json' -Raw)"
```

---

## Verification Checklist

After setup, run this verification script:

```python
# scripts/verify-seo-credentials.py
from infrastructure.config import Config
deps = Config.check_deps()
print("=" * 50)
for service, ok in deps.items():
    if service in ("gsc", "ga4", "bing"):
        status = "✅ READY" if ok else "❌ MISSING"
        print(f"  {service:10} {status}")
print("=" * 50)
```

Expected output:
```
==================================================
  gsc        ✅ READY
  ga4        ✅ READY
  bing       ✅ READY
==================================================
```

Then test each one:

```bash
# GSC weekly report
python infrastructure/webhooks/gsc_handler.py --mode weekly --days 7

# GA4 traffic
python infrastructure/api_client/ga4.py

# Bing WMT
python infrastructure/api_client/bing.py
```

---

## Troubleshooting

### 1. "GA4 API has not been used in project" or "API not enabled"

→ Go to Google Cloud Console → APIs & Services → Library → Search "Google Analytics Data API" → Enable. Wait 30 seconds and retry.

### 2. "User does not have permission to access property"

→ The service account isn't added to GA4. Re-do step A.3. Also confirm you used the FULL service account email (`service-acc-agentic-...@pageforge-466314.iam.gserviceaccount.com`), not just the project ID.

### 3. "Property ID not found"

→ Format must be `properties/123456789` (with prefix). The numeric ID alone won't work.

### 4. "Bing API: 401 Unauthorized"

→ API key is wrong or revoked. Regenerate at https://www.bing.com/webmasters → Settings → API Access. Confirm there are no leading/trailing spaces when you paste it.

### 5. "Bing API: 403 Forbidden"

→ The site hasn't been added/verified in Bing Webmaster Tools. Add it at https://www.bing.com/webmasters first.

### 6. "Project pageforge-466314 not found"

→ You may be signed in with a different Google account. Sign out and back in with the account that owns the `pageforge-466314` project, OR create a new service account:
   1. Google Cloud Console → IAM & Admin → Service Accounts → Create Service Account
   2. Grant it "Service Account User" role
   3. Create a JSON key, download it
   4. Add it to GSC (Settings → Users → Add User → paste email)
   5. Add it to GA4 (step A.3 above)
   6. Update `GSC_SERVICE_ACCOUNT_FILE` in .env

### 7. Token expiration issues

→ Service account tokens expire after 1 hour. The GSC client auto-refreshes. If you see "401 Token expired", restart the poller.

---

## What This Enables

Once all 3 services are configured, the agentic-marketing-os can:

1. **Weekly SEO report** combining GSC + GA4 + Bing WMT data
2. **Content refresh queue** — pages with declining traffic (GSC) or rising bounce (GA4)
3. **AEO/GEO monitoring** — track how AI engines cite your content (GSC + Bing)
4. **Cross-engine CTR benchmarking** — your CTR in Google vs Bing
5. **SERP feature tracking** — featured snippets, knowledge panels, sitelinks
6. **Mobile vs desktop analysis** — both APIs support device dimension
7. **Geo analysis** — country/region breakdowns for international SEO
8. **Daily automated alerts** — significant drops/improvements trigger Slack notifications

---

*Last updated: 2026-07-12*
*Part of the AgenticMarketingPro operating system.*