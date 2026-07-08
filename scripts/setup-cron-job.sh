#!/bin/bash
# Cron-Job.org Setup Script for AMP Job Execution
# ================================================
# This script creates a cron job that triggers the Supabase Edge Function
# every 5 minutes to poll for and execute pending jobs.

API_KEY="WJnmdRwO6iHDH7NIlyYadsQzniVxFctEDLKVZEtExoE="
SUPABASE_URL="https://pusttdxrtmgvhdzdyvbd.supabase.co"
FUNCTION_URL="${SUPABASE_URL}/functions/v1/execute-jobs"

echo "Setting up Cron-Job.org for AMP Job Execution..."
echo "Function URL: ${FUNCTION_URL}"
echo ""

# Create the cron job
curl -s -X POST https://api.cron-job.org/jobs \
  -H "Authorization: Bearer ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "{
    \"job\": {
      \"title\": \"AMP Job Execution - Every 5 min\",
      \"url\": \"${FUNCTION_URL}\",
      \"enabled\": true,
      \"saveResponses\": true,
      \"schedule\": {
        \"timezone\": \"UTC\",
        \"hours\": [-1],
        \"mdays\": [-1],
        \"minutes\": [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
        \"months\": [-1],
        \"wdays\": [-1]
      },
      \"notification\": {
        \"onFailure\": true,
        \"onSuccess\": false,
        \"onDisable\": true
      }
    }
  }" | jq .

echo ""
echo "Done! The cron job is now active."
echo "It will trigger the edge function every 5 minutes."
