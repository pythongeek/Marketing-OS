# Supabase Secrets Setup — PowerShell Commands
# ============================================
# Run these commands in PowerShell to set the GSC service account secret

# Step 1: Read the JSON file and store as a variable
$gscJson = Get-Content "C:\Users\Administrator\Downloads\pageforge-466314-75b94d613b1d.json" -Raw

# Step 2: Set the secret using the variable (correct syntax)
npx supabase secrets set GSC_SERVICE_ACCOUNT_JSON="$gscJson"

# Alternative if the above fails — use a temp file approach:
# $gscJson | Out-File -FilePath "$env:TEMP\gsc-secret.txt" -Encoding utf8
# npx supabase secrets set --env-file "$env:TEMP\gsc-secret.txt"
# Remove-Item "$env:TEMP\gsc-secret.txt"

# Step 3: Verify the secret was set
npx supabase secrets list

# Step 4: Also set the property reference
npx supabase secrets set GSC_PROPERTY="sc-domain:agenticmarketingpro.com"

# Step 5: Deploy the Edge Function with the new secrets
npx supabase functions deploy execute-jobs

# Step 6: Test the function
# curl https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs/health -H "Authorization: Bearer YOUR_ANON_KEY"
