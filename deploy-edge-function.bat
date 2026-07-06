@echo off
REM Deploy AMP Edge Function to Supabase (Windows CMD)
REM Run this in Command Prompt as Administrator

echo === AMP Edge Function Deployment ===

cd /d "F:\Agentic Marketing Pro\marketing"

echo.
echo [1/5] Checking Supabase CLI...
where supabase >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing Supabase CLI via npm...
    npm install -g supabase
)

echo.
echo [2/5] Logging in...
supabase login

echo.
echo [3/5] Linking project pusttdxrtmgvhdzdyvbd...
supabase link --project-ref pusttdxrtmgvhdzdyvbd

echo.
echo [4/5] Deploying Edge Function 'execute-jobs'...
supabase functions deploy execute-jobs

echo.
echo [5/5] Setting secrets from .env file...
supabase secrets set --env-file ./supabase/functions/execute-jobs/.env

echo.
echo === Deployment Complete! ===
echo.
echo Next steps:
echo   1. Go to https://app.supabase.com/project/pusttdxrtmgvhdzdyvbd/functions
echo   2. Verify 'execute-jobs' appears in the list
echo   3. Go to https://console.cron-job.org/
echo   4. Click 'Execute' on job 8023152 to test
echo   5. Check https://app.supabase.com/project/pusttdxrtmgvhdzdyvbd/editor
echo      Any pending job should change to 'completed'

pause
