# Deploy Edge Function to Supabase (PowerShell)
# ==============================================
# Run this script in PowerShell to deploy the execute-jobs Edge Function
#
# Prerequisites:
#   1. Supabase CLI installed: npm install -g supabase
#   2. Logged in: npx supabase login
#   3. Project linked: npx supabase link --project-ref pusttdxrtmgvhdzdyvbd

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "AMP Edge Function Deployment" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Supabase CLI is available
$supabaseCmd = Get-Command npx -ErrorAction SilentlyContinue
if (-not $supabaseCmd) {
    Write-Host "ERROR: npx not found. Please install Node.js and npm first." -ForegroundColor Red
    exit 1
}

Write-Host "Setting Supabase Edge Function secrets..." -ForegroundColor Green
Write-Host ""

# Supabase credentials
Write-Host "[1/8] Setting SUPABASE_URL..." -ForegroundColor Yellow
npx supabase secrets set SUPABASE_URL=https://pusttdxrtmgvhdzdyvbd.supabase.co

Write-Host "[2/8] Setting SUPABASE_SERVICE_ROLE_KEY..." -ForegroundColor Yellow
npx supabase secrets set SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk

# MiniMax M3 (Primary) - VALIDATED WORKING
Write-Host "[3/8] Setting MINIMAX_API_KEY..." -ForegroundColor Yellow
npx supabase secrets set MINIMAX_API_KEY=sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ

Write-Host "[4/8] Setting MINIMAX_BASE_URL..." -ForegroundColor Yellow
npx supabase secrets set MINIMAX_BASE_URL=https://api.minimax.io/v1

Write-Host "[5/8] Setting MINIMAX_MODEL..." -ForegroundColor Yellow
npx supabase secrets set MINIMAX_MODEL=MiniMax-M3

# Kimi (Fallback) - VALIDATED WORKING
Write-Host "[6/8] Setting KIMI_API_KEY..." -ForegroundColor Yellow
npx supabase secrets set KIMI_API_KEY=sk-kimi-zghFewOd27bXAyrIHFV3ZeYO1GaVVnCP4XKNtAhIBSQHftOPfhsfmWThgyxLQ7Bi

Write-Host "[7/8] Setting KIMI_BASE_URL..." -ForegroundColor Yellow
npx supabase secrets set KIMI_BASE_URL=https://api.moonshot.cn/v1

Write-Host "[8/8] Setting KIMI_MODEL..." -ForegroundColor Yellow
npx supabase secrets set KIMI_MODEL=kimi-latest

# LLM Parameters
Write-Host "[9/9] Setting LLM parameters..." -ForegroundColor Yellow
npx supabase secrets set LLM_TEMPERATURE=0.7
npx supabase secrets set LLM_MAX_TOKENS=4096

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "All secrets set successfully!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# Deploy the Edge Function
Write-Host "Deploying execute-jobs Edge Function..." -ForegroundColor Green
Write-Host "This may take 30-60 seconds..." -ForegroundColor Yellow
Write-Host ""

npx supabase functions deploy execute-jobs

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Deployment complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Test the function:" -ForegroundColor Cyan
Write-Host ""
Write-Host '  curl https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs/health \' -ForegroundColor Yellow
Write-Host "    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU'" -ForegroundColor Yellow
Write-Host ""
Write-Host "Expected response:" -ForegroundColor Cyan
Write-Host '  {"status":"healthy","providers":[...],"active_provider":"minimax"}' -ForegroundColor Gray
Write-Host ""
Write-Host "Create a test job in the Vercel app and it will execute within 5 minutes!" -ForegroundColor Green
