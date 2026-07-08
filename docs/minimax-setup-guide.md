# MiniMax M3 Setup Guide for AgenticMarketingPro

## Current Status

⚠️ **The provided MiniMax API key is INVALID.**

The key `sk-cp-1STfj5S2zIDo4QPqzHT3x6nAwkH6C5ZScYm-dfbBJeukrP4fE_8GJx24w7cwB6Czw9YBbaYWFFiO5aFaji6etIEBhrkfjthGcxkftP6q9ODHGUw-Uxy-rOE` returns:
```json
{"type":"error","error":{"type":"authorized_error","message":"invalid api key (2049)","http_code":"401"}}
```

## Why It's Invalid

The `sk-cp-` prefix is **not a standard MiniMax API key format**. MiniMax keys typically start with `sk-` (without the `cp-` suffix). This suggests:

1. **Wrong service**: The key may be from a different provider (e.g., a reseller or proxy service)
2. **Expired**: The key may have been deactivated
3. **Not activated**: The key requires activation on the MiniMax platform
4. **Different plan**: The key may be for a different product tier

## How to Get a Valid MiniMax API Key

### Step 1: Create a MiniMax Account
1. Go to [https://www.minimaxi.com/](https://www.minimaxi.com/) or [https://platform.minimaxi.com/](https://platform.minimaxi.com/)
2. Sign up with your email or phone
3. Complete identity verification (KYC) if required

### Step 2: Get API Access
1. Navigate to **Developer Center** → **API Keys**
2. Click **Create New Key**
3. Select the **MiniMax-M3** model access
4. Copy the key (should start with `sk-` followed by random characters, NOT `sk-cp-`)

### Step 3: Add Funds (Pay-as-you-go)
1. Go to **Billing** → **Recharge**
2. Add a payment method (credit card or Alipay)
3. Add at least $10 to activate API access

### Step 4: Configure in Supabase

```bash
# Using the Supabase CLI
npx supabase secrets set MINIMAX_API_KEY=sk-your-valid-key-here

# Or set all at once from the .env file
npx supabase secrets set --env-file ./supabase/functions/execute-jobs/.env
```

## Fallback Strategy (No Valid MiniMax Key)

The Edge Function now supports **multi-provider fallback**:

```
MiniMax M3 → OpenAI → Kimi
```

If MiniMax is unavailable, it automatically tries OpenAI, then Kimi.

### Option A: Use OpenAI Instead (Recommended for now)

1. Get an OpenAI API key: [https://platform.openai.com/](https://platform.openai.com/)
2. Set it in Supabase:
   ```bash
   npx supabase secrets set OPENAI_API_KEY=sk-your-openai-key
   ```
3. The function will use OpenAI as the primary provider

### Option B: Use Kimi Instead

1. Get a Kimi API key: [https://platform.moonshot.cn/](https://platform.moonshot.cn/)
2. Set it in Supabase:
   ```bash
   npx supabase secrets set KIMI_API_KEY=your-kimi-key
   ```

## Testing the Setup

### Test 1: Health Check
```bash
curl https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs/health \
  -H "Authorization: Bearer <anon-key>"
```

Expected response:
```json
{
  "status": "healthy",
  "providers": [
    { "name": "minimax", "available": true, "latencyMs": 245 },
    { "name": "openai", "available": false, "error": "API key not configured" },
    { "name": "kimi", "available": false, "error": "API key not configured" }
  ],
  "active_provider": "minimax"
}
```

### Test 2: Create a Test Job
```bash
curl -X POST https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs \
  -H "apikey: <anon-key>" \
  -H "Authorization: Bearer <anon-key>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "skill_execution",
    "skill_slug": "content-strategist",
    "client_slug": "agenticmarketingpro",
    "payload": {
      "topic": "AI automation for dental practices",
      "target_audience": "Dental practice owners in the US"
    },
    "status": "pending"
  }'
```

### Test 3: Trigger the Edge Function
```bash
curl -X POST https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs \
  -H "Authorization: Bearer <anon-key>"
```

## Troubleshooting

### Error: "invalid api key (2049)"
- Your key is invalid or expired
- Get a new key from the MiniMax platform
- Check if you need to add funds to your account

### Error: "No AI provider available"
- None of the three provider keys are configured
- Set at least one key in Supabase secrets

### Error: "Failed to fetch jobs"
- The Supabase service role key is incorrect
- Check `SUPABASE_SERVICE_ROLE_KEY` in secrets

## Next Steps

1. ✅ Get a valid MiniMax API key (or use OpenAI/Kimi for now)
2. ✅ Set the key in Supabase secrets
3. ✅ Deploy the updated Edge Function
4. ✅ Test with a sample job
5. ✅ Set up cron-job.org to trigger the function every 5 minutes

## Contact

- MiniMax Support: [https://www.minimaxi.com/contact](https://www.minimaxi.com/contact)
- OpenAI Support: [https://help.openai.com/](https://help.openai.com/)
- Kimi Support: [https://platform.moonshot.cn/docs/support](https://platform.moonshot.cn/docs/support)
