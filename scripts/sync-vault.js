/**
 * Sync completed job results from Supabase to local vault
 */
const fs = require('fs');
const path = require('path');

const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function supabaseRequest(table, method, body, query = '') {
  const url = `https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/${table}${query}`;
  const options = {
    method,
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
    },
  };
  if (method === 'POST') {
    options.headers['Prefer'] = 'return=representation';
    options.body = JSON.stringify(body);
  }
  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

function saveToVault(clientSlug, skillSlug, content, jobId, date) {
  const vaultBase = path.join(__dirname, '..', 'AgenticMarketingPro-Vault');
  const clientDir = path.join(vaultBase, '01-Clients', clientSlug || 'agency');
  const deliverablesDir = path.join(clientDir, '02-Deliverables');

  if (!fs.existsSync(deliverablesDir)) {
    fs.mkdirSync(deliverablesDir, { recursive: true });
  }

  const timestamp = date ? date.split('T')[0] : new Date().toISOString().split('T')[0];
  const filename = `${timestamp}-${skillSlug}-${jobId.slice(0, 8)}.md`;
  const filepath = path.join(deliverablesDir, filename);

  if (fs.existsSync(filepath)) {
    console.log(`  ⏭️  Already exists: ${filename}`);
    return filepath;
  }

  const frontmatter = `---
type: ${skillSlug}
client: ${clientSlug || 'agency'}
job_id: ${jobId}
generated_at: ${date || new Date().toISOString()}
source: sync-from-db
---

`;

  fs.writeFileSync(filepath, frontmatter + content, 'utf8');
  console.log(`  💾 Saved: ${filename}`);
  return filepath;
}

async function syncVault() {
  console.log('🔍 Fetching completed jobs from Supabase...\n');

  // Get all completed jobs for agenticmarketingpro
  const jobs = await supabaseRequest(
    'jobs',
    'GET',
    null,
    `?client_slug=eq.agenticmarketingpro&status=eq.completed&select=id,skill_slug,client_slug,status,created_at,result&order=created_at.desc&limit=50`
  );

  console.log(`Found ${jobs.length} completed jobs\n`);

  let saved = 0;
  let skipped = 0;

  for (const job of jobs) {
    const content = job.result?.content;
    if (!content || typeof content !== 'string' || content.length < 100) {
      console.log(`  ⏭️  Skipping ${job.skill_slug} (no content)`);
      skipped++;
      continue;
    }

    // Strip thinking tags if present
    const cleanContent = content.replace(/<think>[\s\S]*?<\/think>/g, '').trim();

    saveToVault(
      job.client_slug,
      job.skill_slug,
      cleanContent,
      job.id,
      job.created_at
    );
    saved++;
  }

  console.log(`\n📊 Sync complete: ${saved} saved, ${skipped} skipped`);
}

syncVault().catch(console.error);
