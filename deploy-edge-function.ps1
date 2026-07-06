# Deploy AMP Edge Function to Supabase
# Run this in PowerShell as Administrator

$ErrorActionPreference = "Stop"
$ProjectDir = "F:\Agentic Marketing Pro\marketing"
$ProjectRef = "pusttdxrtmgvhdzdyvbd"

Set-Location $ProjectDir
Write-Host "=== AMP Edge Function Deployment ===" -ForegroundColor Cyan

# Step 1: Check if Supabase CLI is installed
Write-Host "`n[1/5] Checking Supabase CLI..." -ForegroundColor Yellow
try {
    $sbVersion = supabase --version 2>$null
    if ($sbVersion) {
        Write-Host "Supabase CLI found: $sbVersion" -ForegroundColor Green
    } else {
        throw "not found"
    }
} catch {
    Write-Host "Supabase CLI not found. Installing via npm..." -ForegroundColor Yellow
    npm install -g supabase
    Write-Host "Supabase CLI installed." -ForegroundColor Green
}

# Step 2: Login (if needed)
Write-Host "`n[2/5] Logging in..." -ForegroundColor Yellow
supabase login

# Step 3: Link project
Write-Host "`n[3/5] Linking project $ProjectRef..." -ForegroundColor Yellow
supabase link --project-ref $ProjectRef

# Step 4: Deploy Edge Function
Write-Host "`n[4/5] Deploying Edge Function 'execute-jobs'..." -ForegroundColor Yellow
supabase functions deploy execute-jobs

# Step 5: Set secrets
Write-Host "`n[5/5] Setting secrets from .env file..." -ForegroundColor Yellow
supabase secrets set --env-file ./supabase/functions/execute-jobs/.env

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Cyan
Write-Host "  1. Go to https://app.supabase.com/project/$ProjectRef/functions"
Write-Host "  2. Verify 'execute-jobs' appears in the list"
Write-Host "  3. Go to https://console.cron-job.org/"
Write-Host "  4. Click 'Execute' on job 8023152 to test"
Write-Host "  5. Check https://app.supabase.com/project/$ProjectRef/editor"
Write-Host "     Any pending job should change to 'completed'"
