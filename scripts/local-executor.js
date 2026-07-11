/**
 * Local Job Executor — Runs on your Windows machine
 * =================================================
 * No resource limits. Full access to all APIs. Can run for hours.
 *
 * Usage:
 *   node scripts/local-executor.js           # Process all queued jobs
 *   node scripts/local-executor.js --once    # Process one job and exit
 *   node scripts/local-executor.js --watch   # Poll continuously
 *
 * Setup: Create .env file in project root with:
 *   SUPABASE_URL=https://pusttdxrtmgvhdzdyvbd.supabase.co
 *   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
 *   MINIMAX_API_KEY=sk-cp-9_VnYYpS_2tAbRPFfwhm9D2QCVpSvWQGzrE6LkmjgWeCntsT9B_0JzUMDVTIjrxRB-9blk1ZL9SVYW8uDXi8uydEvCLZNVn2B08rEBPkR6l-95ii7hW4jWQ
 *   OPENAI_API_KEY=sk-... (optional fallback)
 *   SLACK_WEBHOOK_URL=https://hooks.slack.com/... (optional)
 */

const fs = require('fs');
const path = require('path');

// Load .env file manually (no dotenv dependency)
const envPath = path.join(__dirname, '..', '.env');
if (fs.existsSync(envPath)) {
  const envContent = fs.readFileSync(envPath, 'utf8');
  for (const line of envContent.split('\n')) {
    // Skip comments and empty lines
    if (!line.trim() || line.startsWith('#')) continue;
    const idx = line.indexOf('=');
    if (idx > 0) {
      const key = line.slice(0, idx).trim();
      const value = line.slice(idx + 1).trim();
      if (key && !process.env[key]) {
        process.env[key] = value;
      }
    }
  }
}

// ── Configuration ──────────────────────────────────────────────────
const SUPABASE_URL = process.env.SUPABASE_URL || 'https://pusttdxrtmgvhdzdyvbd.supabase.co';
const SUPABASE_SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;
const MINIMAX_API_KEY = process.env.MINIMAX_API_KEY;
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const SLACK_WEBHOOK_URL = process.env.SLACK_WEBHOOK_URL;

const MINIMAX_BASE_URL = 'https://api.minimaxi.chat/v1';
const MINIMAX_MODEL = 'MiniMax-M3';
const OPENAI_BASE_URL = 'https://api.openai.com/v1';
const OPENAI_MODEL = 'gpt-4o';

const COST_RATES = {
  minimax: { input: 0.0015, output: 0.006 },
  openai: { input: 0.005, output: 0.015 },
};

// ── Skill Prompts ──────────────────────────────────────────────────
const SKILL_PROMPTS = {
  'content-strategist': `You are an expert content strategist for digital marketing agencies. Think step-by-step before answering. Provide structured, actionable content briefs with clear SEO targets.`,
  'on-page-optimizer': `You are an expert SEO on-page optimizer. Audit pages systematically: title tags, meta descriptions, H1-H3 structure, schema markup, internal links, image alt text, keyword density. Provide before/after recommendations.`,
  'technical-seo-auditor': `You are a senior technical SEO consultant. Crawl site architecture, validate structured data, analyze Core Web Vitals, check mobile usability, review log files. Score issues by Impact x Urgency / Effort.`,
  'keyword-researcher': `You are an expert keyword researcher. Analyze search volume, difficulty, intent, and competition. Group keywords into topic clusters with clear prioritization.`,
  'competitor-intelligence': `You are a competitive intelligence analyst. Monitor competitor rankings, backlinks, content gaps, and pricing. Identify opportunities and threats with data-backed insights.`,
  'aeo-geo-strategist': `You are an AI Engine Optimization (AEO) and Generative Engine Optimization (GEO) specialist. Optimize content for ChatGPT, Gemini, Perplexity citations. Build entity schemas and knowledge graph presence.`,
  'link-building-outreach': `You are a link building and digital PR specialist. Identify high-authority prospects, craft personalized outreach emails, and track campaign performance.`,
  'pseo-pipeline': `You are a programmatic SEO expert. Build data-driven content at scale. Design templates, data sources, and URL patterns for long-tail keyword coverage.`,
  'content-brief-writer': `You are a content brief specialist. Create detailed briefs with target keywords, audience personas, content angles, word counts, and competitor analysis.`,
  'copywriter': `You are an expert conversion copywriter. Write persuasive copy for ads, landing pages, emails, and sales pages. Use AIDA framework and psychological triggers.`,
  'social-media-manager': `You are a social media strategist. Create platform-native content calendars, engagement strategies, and repurposing workflows.`,
  'paid-ads-manager': `You are a performance marketing specialist. Manage PPC campaigns across Google, Meta, LinkedIn. Optimize bids, audiences, creatives, and landing pages for ROAS.`,
  'analytics-expert': `You are a marketing analytics expert. Compile reports, identify anomalies (>2σ), track KPIs vs targets, and provide actionable recommendations.`,
  'conversion-optimizer': `You are a CRO specialist. Design A/B tests, analyze funnel drop-offs, and implement conversion improvements based on data.`,
  'brand-voice-writer': `You are a brand voice specialist. Maintain consistent tone, style, and messaging across all content. Create voice guides and train other writers.`,
  'email-marketing-specialist': `You are an email marketing expert. Build lifecycle sequences, A/B test subject lines, optimize deliverability, and track engagement metrics.`,
  'local-seo-manager': `You are a local SEO specialist. Optimize Google Business Profile, manage citations, monitor map pack rankings, and drive local organic traffic.`,
  'video-script-writer': `You are a video content strategist. Write scripts for explainer videos, ads, and social content. Optimize for retention and engagement.`,
  'reputation-manager': `You are a reputation management specialist. Monitor brand sentiment, respond to reviews, and manage crisis communications.`,
  'market-researcher': `You are a market research analyst. Identify trends, analyze market size, and provide strategic insights for business decisions.`,
  'forecasting-revenue': `You are a revenue forecasting specialist. Build predictive models, analyze historical data, and provide resource allocation recommendations.`,
  'reporting-automation': `You are a reporting automation expert. Build dashboards, automate data pipelines, and create client-ready reports.`,
  'playbook-creator': `You are a marketing operations specialist. Document SOPs, create playbooks, and standardize processes for scale.`,
  'off-page-optimizer': `You are an off-page SEO specialist. Manage backlink profiles, disavow toxic links, and build authority through digital PR.`,
  'agentic-marketing-os': `You are the master orchestrator of an AI-native marketing agency. You run the daily ops loop, dispatch specialist agents, manage the task queue, and ensure all deliverables meet quality standards.`,
  'qa-check': `You are a QA gatekeeper. Run binary checks (legal risk, plagiarism) that block deliverability. Run scored checks (grammar, tone, brand voice) that log and continue. Be strict but fair.`,
};

// ── Supabase REST Helper ───────────────────────────────────────────
async function supabaseRequest(table, method, body, query = '') {
  const url = `${SUPABASE_URL}/rest/v1/${table}${query}`;
  const options = {
    method,
    headers: {
      'apikey': SUPABASE_SERVICE_ROLE_KEY,
      'Authorization': `Bearer ${SUPABASE_SERVICE_ROLE_KEY}`,
      'Content-Type': 'application/json',
    },
  };

  if (method === 'POST') {
    options.headers['Prefer'] = 'return=representation';
    options.body = body ? JSON.stringify(body) : undefined;
  } else if (method === 'PATCH') {
    options.headers['Prefer'] = 'return=minimal';
    options.body = body ? JSON.stringify(body) : undefined;
  }
  // GET requests: no body, no Prefer header

  const res = await fetch(url, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  if (res.status === 204) return { data: null, error: null };
  const data = await res.json();
  return { data, error: null };
}

// ── Logging ────────────────────────────────────────────────────────
async function logEvent(jobId, level, message, metadata = {}) {
  try {
    await supabaseRequest('agent_logs', 'POST', {
      job_id: jobId,
      level,
      message,
      metadata,
    });
  } catch (e) {
    console.error(`[LOG ERROR] ${e.message}`);
  }
}

// ── Slack Alerts ───────────────────────────────────────────────────
async function sendSlackAlert(message, level = 'warning', jobId, metadata) {
  if (!SLACK_WEBHOOK_URL) return;
  const emoji = { error: '🔴', warning: '🟡', info: '🔵' }[level];
  const payload = {
    text: `${emoji} AMP Local Executor — ${level.toUpperCase()}`,
    blocks: [
      { type: 'header', text: { type: 'plain_text', text: `${emoji} AMP Alert: ${level.toUpperCase()}`, emoji: true } },
      { type: 'section', fields: [
        { type: 'mrkdwn', text: `*Message:*\n${message}` },
        { type: 'mrkdwn', text: `*Job ID:*\n${jobId || 'N/A'}` },
        { type: 'mrkdwn', text: `*Time:*\n${new Date().toISOString()}` },
        { type: 'mrkdwn', text: `*Executor:*\nLocal (Windows)` },
      ]},
    ],
  };
  try {
    await fetch(SLACK_WEBHOOK_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
  } catch (e) {
    console.error('[SLACK ERROR]', e.message);
  }
}

// ── Provider Health Check ──────────────────────────────────────────
async function checkProviderHealth(provider, apiKey, baseUrl) {
  if (!apiKey) return { name: provider, available: false, error: 'No API key' };
  try {
    const start = Date.now();
    const res = await fetch(`${baseUrl}/models`, {
      headers: { 'Authorization': `Bearer ${apiKey}` },
    });
    const latencyMs = Date.now() - start;
    if (res.ok) return { name: provider, available: true, latencyMs };
    return { name: provider, available: false, error: `HTTP ${res.status}`, latencyMs };
  } catch (e) {
    return { name: provider, available: false, error: e.message };
  }
}

async function getAvailableProvider() {
  // Check MiniMax first
  if (MINIMAX_API_KEY) {
    const health = await checkProviderHealth('minimax', MINIMAX_API_KEY, MINIMAX_BASE_URL);
    if (health.available) {
      return { name: 'minimax', apiKey: MINIMAX_API_KEY, baseUrl: MINIMAX_BASE_URL, model: MINIMAX_MODEL };
    }
    console.warn(`MiniMax unavailable: ${health.error}`);
  }
  // Fall back to OpenAI
  if (OPENAI_API_KEY) {
    const health = await checkProviderHealth('openai', OPENAI_API_KEY, OPENAI_BASE_URL);
    if (health.available) {
      return { name: 'openai', apiKey: OPENAI_API_KEY, baseUrl: OPENAI_BASE_URL, model: OPENAI_MODEL };
    }
    console.warn(`OpenAI unavailable: ${health.error}`);
  }
  return null;
}

// ── LLM Call ───────────────────────────────────────────────────────
async function callLLM(provider, systemPrompt, userPrompt) {
  const messages = [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: userPrompt },
  ];

  const res = await fetch(`${provider.baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${provider.apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: provider.model,
      messages,
      temperature: 0.7,
      max_tokens: 8192,
      top_p: 1.0,
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`${provider.name} API error ${res.status}: ${err}`);
  }

  const data = await res.json();
  const choice = data.choices?.[0];
  const content = choice?.message?.content ?? '';
  const usage = data.usage || { prompt_tokens: 0, completion_tokens: 0 };

  return {
    content,
    tokensIn: usage.prompt_tokens,
    tokensOut: usage.completion_tokens,
    provider: provider.name,
    model: provider.model,
  };
}

function calculateCost(provider, tokensIn, tokensOut) {
  const rates = COST_RATES[provider] || COST_RATES.openai;
  return Number(((tokensIn / 1000) * rates.input + (tokensOut / 1000) * rates.output).toFixed(6));
}

function stripThinkingTags(content) {
  // Remove <think>...</think> blocks that MiniMax M3 includes
  return content.replace(/<think>[\s\S]*?<\/think>/g, '').trim();
}

// ── Build Prompts ──────────────────────────────────────────────────
function buildSystemPrompt(skillSlug, clientSlug) {
  const base = SKILL_PROMPTS[skillSlug] || `You are an expert marketing consultant. Think step-by-step before answering. Provide high-quality, actionable advice.`;
  let prompt = base + `\n\n## Response Format\n- Think step-by-step before answering\n- Use markdown formatting for readability\n- Be specific and actionable\n- When uncertain, state your reasoning clearly`;
  if (clientSlug) {
    prompt += `\n\nYou are working for client: ${clientSlug}. Adapt output to their business context.`;
  }
  return prompt;
}

function buildUserPrompt(skillSlug, payload) {
  const parts = [`Task: ${skillSlug}`];
  for (const [key, value] of Object.entries(payload)) {
    if (['temperature', 'max_tokens', 'model', 'credential_ids', 'prompt_override'].includes(key)) continue;
    if (typeof value === 'string' && value.trim()) {
      parts.push(`${key}: ${value}`);
    } else if (Array.isArray(value) || (typeof value === 'object' && value !== null)) {
      parts.push(`${key}: ${JSON.stringify(value)}`);
    }
  }
  const promptOverride = payload.prompt_override;
  if (promptOverride?.trim()) {
    parts.push(`\n\n## Custom Instructions\n${promptOverride}`);
  }
  return parts.join('\n\n');
}

// ── Retry Wrapper ──────────────────────────────────────────────────
async function withRetry(fn, maxRetries = 3, baseDelayMs = 2000) {
  let lastError;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt < maxRetries) {
        const delay = baseDelayMs * Math.pow(2, attempt);
        console.log(`  Retry ${attempt + 1}/${maxRetries} after ${delay}ms: ${err.message}`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }
  throw lastError;
}

// ── Save Result to Obsidian Vault ──────────────────────────────────
function saveToVault(clientSlug, skillSlug, content, jobId) {
  const vaultBase = path.join(__dirname, '..', 'AgenticMarketingPro-Vault');
  const clientDir = path.join(vaultBase, '01-Clients', clientSlug || 'agency');
  const deliverablesDir = path.join(clientDir, '02-Deliverables');

  if (!fs.existsSync(deliverablesDir)) {
    fs.mkdirSync(deliverablesDir, { recursive: true });
  }

  const timestamp = new Date().toISOString().split('T')[0];
  const filename = `${timestamp}-${skillSlug}-${jobId.slice(0, 8)}.md`;
  const filepath = path.join(deliverablesDir, filename);

  const frontmatter = `---
type: ${skillSlug}
client: ${clientSlug || 'agency'}
job_id: ${jobId}
generated_at: ${new Date().toISOString()}
source: local-executor
---

`;

  fs.writeFileSync(filepath, frontmatter + content, 'utf8');
  console.log(`  💾 Saved to vault: ${filepath}`);
  return filepath;
}

// ── Execute Single Job ─────────────────────────────────────────────
async function executeJob(job) {
  const jobId = job.id;
  const skillSlug = job.skill_slug || '';
  const clientSlug = job.client_slug || undefined;
  const payload = job.payload || {};

  console.log(`\n📝 Job ${jobId}: ${skillSlug} / ${clientSlug || 'agency'}`);

  // Get provider
  const provider = await getAvailableProvider();
  if (!provider) {
    const errorMsg = 'No AI provider available. Check MINIMAX_API_KEY or OPENAI_API_KEY.';
    await supabaseRequest('jobs', 'PATCH', {
      status: 'failed',
      result: { error: errorMsg },
      completed_at: new Date().toISOString(),
    }, `?id=eq.${jobId}`);
    await logEvent(jobId, 'error', errorMsg);
    throw new Error(errorMsg);
  }

  console.log(`  🤖 Using: ${provider.name} (${provider.model})`);
  await logEvent(jobId, 'info', `Executing via ${provider.name}`, { model: provider.model });

  // Mark running
  await supabaseRequest('jobs', 'PATCH', {
    status: 'running',
    started_at: new Date().toISOString(),
  }, `?id=eq.${jobId}`);

  try {
    // Build and call LLM
    const systemPrompt = buildSystemPrompt(skillSlug, clientSlug);
    const userPrompt = buildUserPrompt(skillSlug, payload);

    const llmResult = await withRetry(
      () => callLLM(provider, systemPrompt, userPrompt),
      3,
      2000
    );

    const costUsd = calculateCost(llmResult.provider, llmResult.tokensIn, llmResult.tokensOut);

    // Clean content (remove thinking tags from MiniMax M3)
    const cleanContent = stripThinkingTags(llmResult.content);

    const result = {
      executed_at: new Date().toISOString(),
      job_type: job.type,
      skill_slug: skillSlug,
      client_slug: clientSlug,
      content: cleanContent,
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      model: llmResult.model,
      provider: llmResult.provider,
      cost_usd: costUsd,
      executor: 'local',
      message: `Job executed via ${skillSlug} (${llmResult.provider})`,
    };

    // Update job
    await supabaseRequest('jobs', 'PATCH', {
      status: 'completed',
      result,
      cost_usd: costUsd,
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      completed_at: new Date().toISOString(),
    }, `?id=eq.${jobId}`);

    await logEvent(jobId, 'success', `Completed: ${result.message}`, {
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      cost_usd: costUsd,
    });

    // Save to vault
    const vaultPath = saveToVault(clientSlug, skillSlug, cleanContent, jobId);

    console.log(`  ✅ Completed | Cost: $${costUsd} | Tokens: ${llmResult.tokensIn}/${llmResult.tokensOut}`);

    return result;

  } catch (err) {
    const errorMsg = err.message || String(err);
    console.error(`  ❌ Failed: ${errorMsg}`);
    await supabaseRequest('jobs', 'PATCH', {
      status: 'failed',
      result: { error: errorMsg, provider: provider?.name },
      completed_at: new Date().toISOString(),
    }, `?id=eq.${jobId}`);
    await logEvent(jobId, 'error', `Failed: ${errorMsg}`);
    await sendSlackAlert(`Job ${jobId} failed: ${errorMsg}`, 'error', jobId);
    throw err;
  }
}

// ── Main Loop ──────────────────────────────────────────────────────
async function processJobs(limit = 5) {
  console.log(`\n🔍 Fetching up to ${limit} queued jobs...`);

  // Fetch jobs marked as queued_for_local OR pending (directly from DB)
  let allJobs = [];

  // First try queued_for_local
  const queuedResult = await supabaseRequest(
    'jobs',
    'GET',
    null,
    `?status=eq.queued_for_local&order=created_at.asc&limit=${limit}`
  );

  if (queuedResult.error) {
    console.error('Failed to fetch queued jobs:', queuedResult.error);
  } else if (queuedResult.data?.length > 0) {
    allJobs = queuedResult.data;
  }

  // Fallback to pending jobs
  if (allJobs.length === 0) {
    const pendingResult = await supabaseRequest(
      'jobs',
      'GET',
      null,
      `?status=eq.pending&order=created_at.asc&limit=${limit}`
    );
    if (pendingResult.error) {
      console.error('Failed to fetch pending jobs:', pendingResult.error);
    } else if (pendingResult.data?.length > 0) {
      allJobs = pendingResult.data;
      // Mark them as queued_for_local to prevent other executors from picking them up
      for (const job of allJobs) {
        try {
          await supabaseRequest('jobs', 'PATCH', { status: 'queued_for_local' }, `?id=eq.${job.id}`);
        } catch (e) {
          console.warn(`  Warning: Could not mark job ${job.id} as queued: ${e.message}`);
        }
      }
    }
  }

  if (allJobs.length === 0) {
    console.log('  No jobs to process.');
    return 0;
  }

  console.log(`  Found ${allJobs.length} jobs\n`);

  let completed = 0;
  let failed = 0;

  for (const job of allJobs) {
    try {
      await executeJob(job);
      completed++;
    } catch (e) {
      failed++;
    }
    // Small delay between jobs to avoid rate limits
    await new Promise(r => setTimeout(r, 1000));
  }

  console.log(`\n📊 Batch complete: ${completed} completed, ${failed} failed`);
  return completed;
}

// ── CLI ────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const once = args.includes('--once');
  const watch = args.includes('--watch');

  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║     AMP Local Job Executor — No Limits, Full Power          ║');
  console.log('╚══════════════════════════════════════════════════════════════╝');

  if (!SUPABASE_SERVICE_ROLE_KEY) {
    console.error('\n❌ Error: SUPABASE_SERVICE_ROLE_KEY not set.');
    console.error('Create a .env file in the project root with:');
    console.error('  SUPABASE_URL=https://pusttdxrtmgvhdzdyvbd.supabase.co');
    console.error('  SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIs...');
    console.error('  MINIMAX_API_KEY=sk-cp-...');
    process.exit(1);
  }

  if (once) {
    await processJobs(1);
  } else if (watch) {
    console.log('\n👁️  Watch mode: polling every 30 seconds (Ctrl+C to stop)\n');
    while (true) {
      const processed = await processJobs(3);
      if (processed === 0) {
        process.stdout.write('.');
      }
      await new Promise(r => setTimeout(r, 30000));
    }
  } else {
    await processJobs(5);
  }
}

main().catch(err => {
  console.error('\n💥 Fatal error:', err);
  process.exit(1);
});
