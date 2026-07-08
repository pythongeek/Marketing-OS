# Deploy Edge Function Script
# ============================
# Run this script to deploy the execute-jobs Edge Function to Supabase
# 
# Prerequisites:
#   1. Supabase CLI installed: npm install -g supabase
#   2. Logged in: npx supabase login
#   3. Project linked: npx supabase link --project-ref pusttdxrtmgvhdzdyvbd

# Step 1: Set all secrets from .env file
echo "Setting Supabase Edge Function secrets..."

# Supabase credentials
npx supabase secrets set SUPABASE_URL=https://pusttdxrtmgvhdzdyvbd.supabase.co
npx supabase secrets set SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk

# AI Provider Keys
# NOTE: The MiniMax key is currently INVALID. Use OpenAI or Kimi for now.
# npx supabase secrets set MINIMAX_API_KEY=sk-cp-1STfj5S2zIDo4QPqzHT3x6nAwkH6C5ZScYm-dfbBJeukrP4fE_8GJx24w7cwB6Czw9YBbaYWFFiO5aFaji6etIEBhrkfjthGcxkftP6q9ODHGUw-Uxy-rOE

# OpenAI (currently using Kimi key as fallback)
# npx supabase secrets set OPENAI_API_KEY=sk-...

# Kimi (this is the working key - sk-kimi-... format)
npx supabase secrets set KIMI_API_KEY=sk-kimi-zghFewOd27bXAyrIHFV3ZeYO1GaVVnCP4XKNtAhIBSQHftOPfhsfmWThgyxLQ7Bi
npx supabase secrets set KIMI_BASE_URL=https://api.moonshot.cn/v1
npx supabase secrets set KIMI_MODEL=kimi-latest

# LLM Parameters
npx supabase secrets set LLM_TEMPERATURE=0.7
npx supabase secrets set LLM_MAX_TOKENS=4096

# Step 2: Deploy the Edge Function
echo "Deploying execute-jobs Edge Function..."
npx supabase functions deploy execute-jobs

echo "Deployment complete!"
echo ""
echo "Test the function:"
echo "  curl https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs/health \\"
echo "    -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU'"
