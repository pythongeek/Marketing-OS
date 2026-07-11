/**
 * Check job results from Supabase
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function fetchJobs() {
  const url = 'https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?select=*&order=created_at.desc&limit=5';
  const res = await fetch(url, {
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
    },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function main() {
  const jobs = await fetchJobs();

  for (const job of jobs) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Job: ${job.skill_slug} | Status: ${job.status}`);
    console.log(`Client: ${job.client_slug || 'agency'} | Created: ${job.created_at}`);
    console.log(`Cost: $${job.cost_usd || 0} | Tokens: ${job.tokens_in || 0} in / ${job.tokens_out || 0} out`);

    if (job.result) {
      console.log(`\n--- Result Preview ---`);
      const content = job.result.content || job.result.error || JSON.stringify(job.result);
      console.log(content.slice(0, 1500));
      if (content.length > 1500) console.log(`\n... (${content.length - 1500} more chars)`);
    }
  }
}

main().catch(console.error);
