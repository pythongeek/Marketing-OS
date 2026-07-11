/**
 * Reset stuck jobs back to pending
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function resetJobs() {
  // Reset running jobs back to pending
  const url = 'https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?status=eq.running';
  const res = await fetch(url, {
    method: 'PATCH',
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=representation',
    },
    body: JSON.stringify({ status: 'pending', updated_at: new Date().toISOString() }),
  });

  if (res.ok) {
    const data = await res.json();
    console.log(`✅ Reset ${data.length} stuck jobs from 'running' to 'pending'`);
  } else {
    const text = await res.text();
    console.error('Error:', text);
  }

  // Also reset queued_for_local back to pending
  const url2 = 'https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?status=eq.queued_for_local';
  const res2 = await fetch(url2, {
    method: 'PATCH',
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': 'return=representation',
    },
    body: JSON.stringify({ status: 'pending', updated_at: new Date().toISOString() }),
  });

  if (res2.ok) {
    const data2 = await res2.json();
    console.log(`✅ Reset ${data2.length} jobs from 'queued_for_local' to 'pending'`);
  }
}

resetJobs().catch(console.error);
