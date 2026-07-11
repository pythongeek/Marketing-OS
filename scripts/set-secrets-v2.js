/**
 * Create a properly formatted env file for Supabase secrets
 * Then instruct user to run: npx supabase secrets set --env-file <file>
 */
const fs = require('fs');
const path = require('path');

// Read GSC service account JSON
const gscJsonPath = 'C:\\Users\\Administrator\\Downloads\\pageforge-466314-75b94d613b1d.json';
const gscJson = fs.readFileSync(gscJsonPath, 'utf8').trim();

// Create env file content - single line format
const envContent = `GSC_SERVICE_ACCOUNT_JSON=${gscJson}
GSC_PROPERTY=sc-domain:agenticmarketingpro.com
MINIMAX_API_KEY=sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ
`;

const envFile = path.join(__dirname, '..', 'supabase', 'functions', 'execute-jobs', '.env');
fs.writeFileSync(envFile, envContent, 'utf8');

console.log('✅ Env file created:', envFile);
console.log('\nNow run this command in PowerShell:');
console.log(`  cd "F:\Agentic Marketing Pro\marketing"`);
console.log(`  npx supabase secrets set --env-file "${envFile}"`);
console.log(`  npx supabase functions deploy execute-jobs`);
