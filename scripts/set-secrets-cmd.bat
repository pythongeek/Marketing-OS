@echo off
REM Batch file to set Supabase secrets using temp env file approach
REM Run this in Command Prompt (not PowerShell)

cd /d "F:\Agentic Marketing Pro\marketing"

echo Creating temp env file...
set "ENVFILE=%TEMP%\gsc-env-%RANDOM%.txt"

REM Use PowerShell to properly create the env file
powershell -NoProfile -Command "$json = Get-Content 'C:\Users\Administrator\Downloads\pageforge-466314-75b94d613b1d.json' -Raw; $content = @('GSC_SERVICE_ACCOUNT_JSON=' + $json, 'GSC_PROPERTY=sc-domain:agenticmarketingpro.com', 'MINIMAX_API_KEY=sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ'); [System.IO.File]::WriteAllLines('%ENVFILE%', $content)"

echo Setting secrets via Supabase CLI...
npx supabase secrets set --env-file "%ENVFILE%"

echo Cleaning up...
del "%ENVFILE%"

echo.
echo ==========================================
echo Secrets set! Now deploy the Edge Function:
echo   npx supabase functions deploy execute-jobs
echo ==========================================
pause
