/**
 * Update .env file with all required secrets
 * Handles special characters in values properly
 */
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');

const envContent = `# AgenticMarketingPro — Local Executor Configuration
# ===================================================
# NEVER commit this file to git (it's in .gitignore).

# Supabase
SUPABASE_URL=https://pusttdxrtmgvhdzdyvbd.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk

# AI Providers (priority: MiniMax → OpenAI)
MINIMAX_API_KEY=sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ
# OPENAI_API_KEY=sk-... (optional fallback)

# Notifications (optional)
# SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
`;

fs.writeFileSync(envPath, envContent, 'utf8');
console.log('✅ .env file updated with MiniMax API key');
