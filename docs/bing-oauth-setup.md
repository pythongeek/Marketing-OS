# Bing Webmaster Tools OAuth 2.0 Setup Guide

Complete walkthrough for connecting AgenticMarketingPro to Bing Webmaster Tools via Microsoft OAuth 2.0.

**Time required:** ~20 minutes
**Difficulty:** Intermediate
**Cost:** Free

---

## Why OAuth?

Microsoft **deprecated** the static API key for Bing Webmaster in late 2023. OAuth 2.0 is now the only officially supported auth method. The old `BING_API_KEY` approach returns `ErrorCode: 3 InvalidApiKey` regardless of whether the key is valid.

---

## What You Need

| Variable Name (in Vercel) | Source |
|---------------------------|--------|
| `BING_CLIENT_ID` | Azure app registration — Application (client) ID |
| `BING_CLIENT_SECRET` | Azure app registration — Client secret Value |
| `BING_TENANT` | "common" for multi-tenant (recommended) |
| `BING_REDIRECT_URI` | `https://marketing-os-chi-three.vercel.app/api/bing-auth/callback` |

---

## Step 1: Register Azure App (5 minutes)

1. Go to https://portal.azure.com/#blade/Microsoft_AAD_RegisteredApps/ApplicationsListBlade
2. Click **"+ New registration"**
3. Fill in:
   - **Name**: `AgenticMarketingPro Bing WMT`
   - **Supported account types**: `Accounts in any organizational directory (Any Microsoft Entra ID tenant - Multitenant) and personal Microsoft accounts (e.g. Skype, Xbox)`
   - **Redirect URI**:
     - Platform: **Web**
     - URL: `https://marketing-os-chi-three.vercel.app/api/bing-auth/callback`
4. Click **Register**

## Step 2: Save the Client ID

After registration, you'll land on the **Overview** page. Copy the **Application (client) ID** — this is your `BING_CLIENT_ID`.

It looks like: `12345678-abcd-efgh-ijkl-123456789012`

## Step 3: Create Client Secret (2 minutes)

1. Left sidebar → **Certificates & secrets**
2. **Client secrets** tab → **"+ New client secret"**
3. Fill in:
   - **Description**: `AgenticMarketingPro Production`
   - **Expires**: `24 months` (recommended)
4. Click **Add**
5. ⚠️ **IMMEDIATELY copy the Value** column — you can never see it again!

This is your `BING_CLIENT_SECRET`. It looks like: `abc8~XYZ_long-random-string-here`

## Step 4: Add API Permissions (2 minutes)

1. Left sidebar → **API permissions**
2. Click **"+ Add a permission"**
3. Choose **"Microsoft APIs"** tab
4. Search for and click **"Bing Webmaster API"**
5. Choose **"Delegated permissions"**
6. Check: **`webmaster.readwrite`** (recommended) OR **`webmaster.read`** (read-only)
7. Click **"Add permissions"**

## Step 5: Save to Vercel (2 minutes)

Go to **Vercel Dashboard** → **marketing-os-chi-three** project → **Settings** → **Environment Variables**

Add these 4 variables (one per row):

| Variable Name | Value |
|--------------|-------|
| `BING_CLIENT_ID` | `<paste Application client ID from Step 2>` |
| `BING_CLIENT_SECRET` | `<paste secret Value from Step 3>` |
| `BING_TENANT` | `common` |
| `BING_REDIRECT_URI` | `https://marketing-os-chi-three.vercel.app/api/bing-auth/callback` |

Set these for **all environments**: Production, Preview, Development.

## Step 6: Deploy the OAuth Routes (3 minutes)

The OAuth code is already in your repo. Just deploy:

```bash
cd "F:\Agentic Marketing Pro\marketing\web"
npx vercel deploy --prod
```

This pushes the three new routes:
- `/api/bing-auth/start` — initiates OAuth flow
- `/api/bing-auth/callback` — receives Microsoft redirect
- `/api/bing-auth/refresh` — auto-refreshes expired tokens

## Step 7: Run the Migration (1 minute)

The `bing_tokens` Supabase table needs to exist:

```bash
cd "F:\Agentic Marketing Pro\marketing"
npx supabase db push
```

Or run the migration manually in Supabase SQL Editor:
```sql
-- Paste contents of supabase/migrations/008_bing_tokens.sql
```

## Step 8: Authorize (1 minute, one-time)

1. Visit **https://marketing-os-chi-three.vercel.app/credentials** in your browser
2. Click the **"Connect Bing WMT (OAuth)"** button (top-right of the page)
3. You'll be redirected to Microsoft's login
4. Sign in with the Microsoft account that owns the Bing Webmaster sites
5. Grant permission to "AgenticMarketingPro Bing WMT"
6. You'll be redirected back to the credentials page with a success banner

**Done!** Tokens are now stored in Supabase and will auto-refresh forever.

---

## How It Works After Setup

### Token Lifecycle
- Microsoft access tokens expire after **1 hour**
- Refresh tokens last until you revoke them (up to 24 months for 24-month secrets)
- Our `/api/bing-auth/refresh` route auto-refreshes when needed
- The Bing API client (`infrastructure/api_client/bing.py`) fetches fresh tokens before each call

### Where Tokens Live
```
User clicks "Connect Bing WMT"
        ↓
/api/bing-auth/start → Microsoft login
        ↓
/api/bing-auth/callback ← auth code
        ↓
POST to https://login.microsoftonline.com/common/oauth2/v2.0/token
        ↓
Store in Supabase table: bing_tokens (encrypted at rest, RLS protected)
        ↓
Any future Bing API call → fetch from Supabase → auto-refresh if expired
```

### Re-authorization

If tokens ever fail (e.g., you revoked access in Microsoft account settings), just click the "Connect" button again. The flow re-runs and updates the tokens.

---

## Verification

After completing setup, test with:

```bash
curl "https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs?mode=single&skill=bing-wmt-expert"
```

If configured correctly, the response will include `{"ok": true, "site_list": [...]}` or a similar Bing API result.

You can also check the `bing_tokens` table in Supabase:
```sql
SELECT id, expires_at, scope, updated_at FROM bing_tokens;
```

---

## Troubleshooting

### "AADSTS50011: The redirect URI specified in the request does not match"

The redirect URI in your Azure app doesn't match exactly. The URL must be **byte-identical**:
- ✅ `https://marketing-os-chi-three.vercel.app/api/bing-auth/callback`
- ❌ `https://marketing-os-chi-three.vercel.app/api/bing-auth/callback/`
- ❌ `http://marketing-os-chi-three.vercel.app/api/bing-auth/callback`

Fix: Update the redirect URI in Azure → App Registration → Authentication.

### "AADSTS700016: Application with identifier XXX was not found"

Wrong client ID. Copy the **Application (client) ID** (not Object ID or Directory ID) from the Azure Overview page.

### "Invalid client secret"

The secret expired or wasn't copied correctly. Generate a new one in Azure → Certificates & secrets → New client secret.

### "Bing Webmaster API not found in permission list"

The Bing Webmaster API may not be visible in your tenant's API list. Try typing the full name in the search box: "Bing Webmaster". If still not visible, you may need admin consent.

### Tokens stored but API returns 401

Wait 30 seconds for token propagation. If still failing, check that `BING_REDIRECT_URI` in Vercel exactly matches the one in Azure.

---

## Security Notes

- **Never** commit `BING_CLIENT_SECRET` to git
- The `.env` file is in `.gitignore` — keep it that way
- Vercel encrypts environment variables at rest
- Supabase `bing_tokens` table is RLS-protected — only the service role can read
- The OAuth flow uses a state token (CSRF protection)
- Refresh tokens are stored encrypted in Supabase

---

## Files Created/Modified

| File | Purpose |
|------|---------|
| `web/app/api/bing-auth/start/route.ts` | Initiate OAuth flow |
| `web/app/api/bing-auth/callback/route.ts` | Receive auth code, exchange for tokens |
| `web/app/api/bing-auth/refresh/route.ts` | Auto-refresh expired tokens |
| `web/app/credentials/page.tsx` | Added "Connect Bing WMT" button |
| `supabase/migrations/008_bing_tokens.sql` | Tokens table |
| `infrastructure/api_client/bing.py` | Updated to use OAuth with fallback |
| `.env.example` | Added Bing OAuth variables |

---

*Last updated: 2026-07-12*
*Part of the AgenticMarketingPro operating system.*