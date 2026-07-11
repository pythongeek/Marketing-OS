# Google Search Console Service Account Setup — Exact Steps

**For:** AgenticMarketingPro SEO Automation  
**Project:** pageforge-466314 (your Google Cloud project)  
**Last Updated:** 2026-07-09

---

## STEP 1: Create the Service Account

Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=pageforge-466314

### Fill in these exact values:

| Field | Value | Why |
|-------|-------|-----|
| **Service account name** | `gsc-seo-agent` | Descriptive name for the SEO automation agent |
| **Service account ID** | `gsc-seo-agent` | Auto-generates email: `gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com` |
| **Service account description** | `Read-only access to Google Search Console data for automated SEO reporting and monitoring. Used by AgenticMarketingPro SEO Ops system.` | Clear purpose for security audits |

Click **Create and Continue**

---

## STEP 2: Grant Roles (PERMISSIONS)

This is the **most critical step**. You need to assign the correct roles.

### For READ-ONLY Access (Recommended — Safer):

Grant this service account these **2 roles**:

| Role | Purpose | Why |
|------|---------|-----|
| **Viewer** (`roles/viewer`) | Read access to ALL project resources | Allows API calls to read GSC data |
| **Search Console Viewer** | Read access to Search Console data specifically | Required for GSC API access |

**How to add:**
1. In the "Grant this service account access to project" section
2. Click the **Select a role** dropdown
3. Type "Viewer" → select **Basic → Viewer**
4. Click **Add another role**
5. Type "Search Console" → select **Search Console → Search Console Viewer**
6. Click **Continue**

### Alternative: If you want FULL ADMIN access (not recommended unless needed):

| Role | Purpose |
|------|---------|
| **Editor** (`roles/editor`) | Full project access |
| **Search Console Owner** | Full GSC access |

**⚠️ WARNING:** Only use admin roles if the system needs to MODIFY GSC settings (e.g., submit sitemaps, request indexing). For reporting only, use Viewer.

---

## STEP 3: Principals with Access (OPTIONAL — Skip for now)

This step is for **who can impersonate this service account**.

**For your use case:** Skip this step (click **Done**) unless you have specific security requirements.

The service account will be used directly by your Edge Function with its own key.

---

## STEP 4: Create and Download the JSON Key

After creating the service account:

1. Find the service account in the list: `gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com`
2. Click on it to open details
3. Go to the **Keys** tab
4. Click **Add Key → Create new key**
5. Select **JSON** format (not P12)
6. Click **Create**
7. **The JSON file will download automatically** — save it securely!

### What the JSON file looks like:
```json
{
  "type": "service_account",
  "project_id": "pageforge-466314",
  "private_key_id": "abc123...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n-----END PRIVATE KEY-----\n",
  "client_email": "gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com",
  "client_id": "123456789",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gsc-seo-agent%40pageforge-466314.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

---

## STEP 5: Enable the Search Console API

Before the service account can work, you MUST enable the API:

1. Go to: https://console.cloud.google.com/apis/library?project=pageforge-466314
2. Search for **"Google Search Console API"**
3. Click on it → Click **Enable**
4. Wait 2-3 minutes for activation

**Also enable these related APIs:**
- **Google Analytics Data API** (for GA4 integration)
- **PageSpeed Insights API** (for CWV checks)

---

## STEP 6: Add Service Account to GSC Property

This is the step most people miss! The service account needs permission in GSC itself.

1. Go to: https://search.google.com/search-console
2. Select your property: `agenticmarketingpro.com`
3. Click **Settings** (gear icon) → **Users and Permissions**
4. Click **Add User**
5. Enter the service account email: `gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com`
6. Set permission level:
   - **Full** → can read AND modify (submit sitemaps, request indexing)
   - **Restricted** → read-only (view data, cannot modify)
   
   **For reporting only:** Select **Restricted**
   **For full automation:** Select **Full**

7. Click **Add**

---

## STEP 7: Verify Everything Works

Test the service account with a simple API call:

```bash
# Install gcloud CLI if you haven't: https://cloud.google.com/sdk/docs/install

# Authenticate with the service account
gcloud auth activate-service-account gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com --key-file=/path/to/your-key.json

# Test GSC API access
curl "https://searchconsole.googleapis.com/v1/sites?prettyPrint=true" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)"
```

You should see a list of sites you have access to.

---

## STEP 8: Add to AgenticMarketingPro System

### Option A: Upload via Vercel App (Recommended)

1. Go to: https://marketing-os-chi-three.vercel.app/credentials
2. Click **Add Credential**
3. Fill in:
   | Field | Value |
   |-------|-------|
   | **Service** | `google-search-console` |
   | **Label** | `GSC - agenticmarketingpro.com` |
   | **Config** | `{"property": "sc-domain:agenticmarketingpro.com"}` |
   | **Secrets** | Paste the entire JSON key content here |

4. Click **Save**
5. Click **Test Connection** to verify

### Option B: Add to Supabase Secrets (For Edge Function)

```bash
npx supabase secrets set GSC_SERVICE_ACCOUNT_KEY="$(cat /path/to/your-key.json | tr -d '\n')"
npx supabase secrets set GSC_PROPERTY="sc-domain:agenticmarketingpro.com"
```

---

## SUMMARY: What You Need to Send Me

| Item | Format | Where to Find |
|------|--------|---------------|
| **Service Account JSON** | `.json` file | Downloaded in Step 4 |
| **Property URL** | `sc-domain:agenticmarketingpro.com` or `https://agenticmarketingpro.com/` | GSC property settings |
| **Service Account Email** | `gsc-seo-agent@pageforge-466314.iam.gserviceaccount.com` | Service account details page |

---

## SECURITY CHECKLIST

- [ ] JSON key file stored securely (not in Git, not in public folders)
- [ ] Service account has minimum required permissions (Viewer, not Editor)
- [ ] GSC permission set to "Restricted" if only reporting needed
- [ ] Key rotated if accidentally exposed
- [ ] Access logged and monitored

---

## TROUBLESHOOTING

### Error: "API has not been used in project... before or it is disabled"
**Fix:** Go to Google Cloud Console → APIs & Services → Library → Search "Google Search Console API" → Click **Enable**

### Error: "User does not have sufficient permission for site"
**Fix:** Go to GSC → Settings → Users and Permissions → Add the service account email with Full or Restricted access

### Error: "The caller does not have permission"
**Fix:** The service account needs BOTH the Cloud IAM role AND the GSC property permission. Check both.

### Error: "Invalid JWT Signature"
**Fix:** The JSON key file is corrupted or expired. Create a new key (Step 4).

---

**Once you complete these steps, send me the JSON key file and I'll configure the automated GSC reporting agent!**
