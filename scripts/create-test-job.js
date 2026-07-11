/**
 * Create a test job in Supabase to verify the Edge Function pipeline
 * Uses native fetch (Node 18+) instead of supabase-js
 */
const SERVICE_ROLE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InB1c3R0ZHhydG1ndmhkemR5dmJkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MjgzOTA0NCwiZXhwIjoyMDk4NDE1MDQ0fQ.KUJmCCFWcYxRL9uf8blLiR9Q5EHAp7bFPc6sptuCZLk';

async function supabaseRequest(table, method, body) {
  const url = `https://pusttdxrtmgvhdzdyvbd.supabase.co/rest/v1/${table}`;
  const res = await fetch(url, {
    method,
    headers: {
      'apikey': SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
      'Prefer': method === 'POST' ? 'return=representation' : '',
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json();
}

async function createTestJobs() {
  // Test 1: Content strategy job
  const job1 = await supabaseRequest('jobs', 'POST', {
    type: 'skill_execution',
    skill_slug: 'content-strategist',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      topic: 'AI Automation for Dental Practices',
      target_audience: 'Dental practice owners in the US',
      goal: 'Generate leads for AI phone answering and appointment scheduling automation',
      prompt_override: 'Focus on ROI metrics, time savings, and patient satisfaction improvements. Include specific numbers and case studies where possible.',
    },
  });
  console.log('✅ Test job 1 created:', job1[0]?.id);

  // Test 2: SEO audit job
  const job2 = await supabaseRequest('jobs', 'POST', {
    type: 'skill_execution',
    skill_slug: 'technical-seo-auditor',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      website: 'https://agenticmarketingpro.com',
      focus_areas: ['Core Web Vitals', 'Mobile Usability', 'Schema Markup', 'Index Coverage'],
      prompt_override: 'Provide a prioritized checklist with severity ratings (Critical/High/Medium/Low) and estimated effort for each fix.',
    },
  });
  console.log('✅ Test job 2 created:', job2[0]?.id);

  // Test 3: Analytics/reporting job
  const job3 = await supabaseRequest('jobs', 'POST', {
    type: 'skill_execution',
    skill_slug: 'analytics-expert',
    client_slug: 'agenticmarketingpro',
    status: 'pending',
    payload: {
      report_type: 'search_performance_summary',
      date_range: 'last_28_days',
      prompt_override: 'Analyze search performance data and provide actionable recommendations for improving CTR and rankings.',
    },
  });
  console.log('✅ Test job 3 created:', job3[0]?.id);

  console.log('\n📋 Jobs created. Now trigger the Edge Function to execute them.');
  console.log('The cron-job.org webhook will trigger automatically, or run manually via the Supabase dashboard.');
}

createTestJobs().catch(err => {
  console.error('❌ Error:', err.message);
  process.exit(1);
});
