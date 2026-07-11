/**
 * Trigger Edge Function in small batches to avoid resource limits
 */
const ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI4MzkwNDQsImV4cCI6MjA5ODQxNTA0NH0.czorJe8WQ2mLliNQqHraU2E3Tqor7lE0hYaksLRPwmU';

async function triggerExecution() {
  const res = await fetch('https://pusttdxrtmgvhdzdyvbd.supabase.co/functions/v1/execute-jobs', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${ANON_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ trigger: 'batch', limit: 3 }),
  });
  const data = await res.json();
  console.log('Result:', JSON.stringify(data, null, 2));
  return data;
}

// Run multiple times to process all pending jobs
async function runBatches(count) {
  for (let i = 0; i < count; i++) {
    console.log(`\n--- Batch ${i + 1}/${count} ---`);
    await triggerExecution();
    // Wait between batches
    await new Promise(r => setTimeout(r, 5000));
  }
  console.log('\n✅ All batches triggered');
}

runBatches(5).catch(console.error);
