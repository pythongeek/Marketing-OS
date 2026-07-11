/**
 * Set Supabase secrets via Management API
 * Usage: node scripts/set-secrets.js
 */
const fs = require('fs');
const https = require('https');

const PROJECT_REF = 'pusttdxrtmgvhdzdyvbd';
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function setSecrets(secrets) {
  const postData = JSON.stringify(secrets);

  const options = {
    hostname: 'api.supabase.com',
    port: 443,
    path: `/v1/projects/${PROJECT_REF}/secrets`,
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      'Content-Length': Buffer.byteLength(postData),
    },
  };

  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve({ status: res.statusCode, body: data });
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.write(postData);
    req.end();
  });
}

async function main() {
  // Read GSC service account JSON
  const gscJsonPath = 'C:\\Users\\Administrator\\Downloads\\pageforge-466314-75b94d613b1d.json';
  const gscJson = fs.readFileSync(gscJsonPath, 'utf8');

  const secrets = {
    secrets: [
      { name: 'GSC_SERVICE_ACCOUNT_JSON', value: gscJson },
      { name: 'GSC_PROPERTY', value: 'sc-domain:agenticmarketingpro.com' },
      { name: 'MINIMAX_API_KEY', value: 'sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ' },
    ],
  };

  console.log('Setting secrets...');
  const result = await setSecrets(secrets);
  console.log('✅ Secrets set successfully!');
  console.log('Response:', result.body);
}

main().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
