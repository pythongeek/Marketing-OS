/**
 * Check pending jobs count
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function checkJobs() {
  const url = 'https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?select=status,id,skill_slug,client_slug&order=created_at.desc&limit=20';
  const res = await fetch(url, {
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
    },
  });
  const jobs = await res.json();

  const byStatus = {};
  for (const job of jobs) {
    byStatus[job.status] = (byStatus[job.status] || 0) + 1;
  }

  console.log('Recent jobs by status:');
  for (const [status, count] of Object.entries(byStatus)) {
    console.log(`  ${status}: ${count}`);
  }

  console.log('\nLast 5 jobs:');
  jobs.slice(0, 5).forEach(j => {
    console.log(`  ${j.status.padEnd(12)} | ${j.skill_slug?.padEnd(20)} | ${j.client_slug || 'agency'}`);
  });
}

checkJobs().catch(console.error);
