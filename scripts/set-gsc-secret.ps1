# Set GSC Service Account JSON Secret in Supabase
# This script handles the JSON escaping properly using a temp env file

$ErrorActionPreference = "Stop"

# Paths
$jsonPath = "C:\Users\Administrator\Downloads\pageforge-466314-75b94d613b1d.json"
$envFile = "$env:TEMP\gsc-env-$(Get-Random).txt"

# Validate JSON file exists
if (-not (Test-Path $jsonPath)) {
    Write-Error "JSON file not found at: $jsonPath"
    exit 1
}

# Read JSON content
$json = Get-Content $jsonPath -Raw

# Write to temp env file (no newlines in the value)
"GSC_SERVICE_ACCOUNT_JSON=$json" | Out-File -FilePath $envFile -Encoding utf8 -NoNewline

Write-Host "Temp env file created: $envFile"
Write-Host "Setting secret via Supabase CLI..."

# Set the secret using the env file
npx supabase secrets set --env-file $envFile

# Clean up temp file
Remove-Item $envFile -Force
Write-Host "Cleaned up temp file"

Write-Host "`n✅ GSC_SERVICE_ACCOUNT_JSON secret set successfully!"
Write-Host "`nNext steps:"
Write-Host "  1. Set GSC_PROPERTY: npx supabase secrets set GSC_PROPERTY=sc-domain:agenticmarketingpro.com"
Write-Host "  2. Deploy Edge Function: npx supabase functions deploy execute-jobs"
