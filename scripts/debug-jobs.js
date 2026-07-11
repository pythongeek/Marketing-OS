/**
 * Debug job fetching
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function debug() {
  // Test 1: Simple select
  console.log('Test 1: All jobs (limit 3)');
  const res1 = await fetch('https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?select=id,status,skill_slug&limit=3', {
    headers: { 'apikey': SERVICE_ROLE_KEY, 'Authorization': `Bearer ${SERVICE_ROLE_KEY}` },
  });
  console.log('Status:', res1.status);
  console.log('Data:', await res1.json());

  // Test 2: Filter by status
  console.log('\nTest 2: Pending jobs');
  const res2 = await fetch('https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/jobs?select=id,status,skill_slug&status=eq.pending&limit=3', {
    headers: { 'apikey': SERVICE_ROLE_KEY, 'Authorization': `Bearer ${SERVICE_ROLE_KEY}` },
  });
  console.log('Status:', res2.status);
  const data2 = await res2.json();
  console.log('Count:', data2.length);
  console.log('Data:', data2);
}

debug().catch(console.error);
