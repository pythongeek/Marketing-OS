/**
 * Supabase Edge Function: execute-jobs
 * ====================================
 * Hosted worker that polls Supabase for pending jobs, executes them via
 * Hermes Agent Desktop (primary), and writes results back.
 *
 * Trigger: HTTP (from cron-job.org) or manual
 * Runtime: Deno (Supabase Edge Functions)
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

// ── Hermes Agent Desktop Configuration ────────────────────────────
const HERMES_AGENT_API_KEY = Deno.env.get("HERMES_AGENT_API_KEY");
const HERMES_AGENT_BASE_URL = Deno.env.get("HERMES_AGENT_BASE_URL") || "https://hermes-agent.local/api";
const HERMES_AGENT_MODEL = Deno.env.get("HERMES_AGENT_MODEL") || "MiniMax-M3";

const LLM_TEMPERATURE = Number(Deno.env.get("LLM_TEMPERATURE") || "0.7");
const LLM_MAX_TOKENS = Number(Deno.env.get("LLM_MAX_TOKENS") || "4096");

// Cost tracking (approximate per 1K tokens)
const COST_RATES: Record<string, { input: number; output: number }> = {
  hermes_agent: { input: 0.0015, output: 0.006 },
};

const SLACK_WEBHOOK_URL = Deno.env.get("SLACK_WEBHOOK_URL");

const supabase = createClient(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY);

// ── Content-producing skills that trigger QA ──────────────────────
const CONTENT_SKILLS = new Set([
  "content-strategist", "content-brief-writer", "copywriter",
  "brand-voice-writer", "video-script-writer", "social-media-manager",
  "email-marketing-specialist", "paid-ads-manager", "pitch-proposal",
  "playbook-request", "on-page-request", "pseo-config",
  "aeo-entity-schema", "local-seo", "outreach-prospect",
  "influencer-campaign", "ad-campaign", "email-sequence",
  "content-brief", "copy-request", "market-alert",
  "forecasting-request", "report-config", "analytics-report",
  "revenue-opportunity", "tech-audit", "qa-check-request",
]);

// ── Skill prompts optimized for AI execution ──────────────────────
const SKILL_PROMPTS: Record<string, string> = {
  "content-strategist": `You are an expert content strategist for digital marketing agencies. Think step-by-step before answering. Provide structured, actionable content briefs with clear SEO targets.`,
  "on-page-optimizer": `You are an expert SEO on-page optimizer. Audit pages systematically: title tags, meta descriptions, H1-H3 structure, schema markup, internal links, image alt text, keyword density. Provide before/after recommendations.`,
  "technical-seo-auditor": `You are a senior technical SEO consultant. Crawl site architecture, validate structured data, analyze Core Web Vitals, check mobile usability, review log files. Score issues by Impact x Urgency / Effort.`,
  "keyword-researcher": `You are an expert keyword researcher. Analyze search volume, difficulty, intent, and competition. Group keywords into topic clusters with clear prioritization.`,
  "competitor-intelligence": `You are a competitive intelligence analyst. Monitor competitor rankings, backlinks, content gaps, and pricing. Identify opportunities and threats with data-backed insights.`,
  "aeo-geo-strategist": `You are an AI Engine Optimization (AEO) and Generative Engine Optimization (GEO) specialist. Optimize content for ChatGPT, Gemini, Perplexity citations. Build entity schemas and knowledge graph presence.`,
  "link-building-outreach": `You are a link building and digital PR specialist. Identify high-authority prospects, craft personalized outreach emails, and track campaign performance.`,
  "pseo-pipeline": `You are a programmatic SEO expert. Build data-driven content at scale. Design templates, data sources, and URL patterns for long-tail keyword coverage.`,
  "content-brief-writer": `You are a content brief specialist. Create detailed briefs with target keywords, audience personas, content angles, word counts, and competitor analysis.`,
  "copywriter": `You are an expert conversion copywriter. Write persuasive copy for ads, landing pages, emails, and sales pages. Use AIDA framework and psychological triggers.`,
  "social-media-manager": `You are a social media strategist. Create platform-native content calendars, engagement strategies, and repurposing workflows.`,
  "paid-ads-manager": `You are a performance marketing specialist. Manage PPC campaigns across Google, Meta, LinkedIn. Optimize bids, audiences, creatives, and landing pages for ROAS.`,
  "analytics-expert": `You are a marketing analytics expert. Compile reports, identify anomalies (>2σ), track KPIs vs targets, and provide actionable recommendations.`,
  "conversion-optimizer": `You are a CRO specialist. Design A/B tests, analyze funnel drop-offs, and implement conversion improvements based on data.`,
  "brand-voice-writer": `You are a brand voice specialist. Maintain consistent tone, style, and messaging across all content. Create voice guides and train other writers.`,
  "email-marketing-specialist": `You are an email marketing expert. Build lifecycle sequences, A/B test subject lines, optimize deliverability, and track engagement metrics.`,
  "local-seo-manager": `You are a local SEO specialist. Optimize Google Business Profile, manage citations, monitor map pack rankings, and drive local organic traffic.`,
  "video-script-writer": `You are a video content strategist. Write scripts for explainer videos, ads, and social content. Optimize for retention and engagement.`,
  "reputation-manager": `You are a reputation management specialist. Monitor brand sentiment, respond to reviews, and manage crisis communications.`,
  "market-researcher": `You are a market research analyst. Identify trends, analyze market size, and provide strategic insights for business decisions.`,
  "forecasting-revenue": `You are a revenue forecasting specialist. Build predictive models, analyze historical data, and provide resource allocation recommendations.`,
  "reporting-automation": `You are a reporting automation expert. Build dashboards, automate data pipelines, and create client-ready reports.`,
  "playbook-creator": `You are a marketing operations specialist. Document SOPs, create playbooks, and standardize processes for scale.`,
  "off-page-optimizer": `You are an off-page SEO specialist. Manage backlink profiles, disavow toxic links, and build authority through digital PR.`,
  "agentic-marketing-os": `You are the master orchestrator of an AI-native marketing agency. You run the daily ops loop, dispatch specialist agents, manage the task queue, and ensure all deliverables meet quality standards.`,
  "qa-check": `You are a QA gatekeeper. Run binary checks (legal risk, plagiarism) that block deliverability. Run scored checks (grammar, tone, brand voice) that log and continue. Be strict but fair.`,
};

// ── Logging ───────────────────────────────────────────────────────
async function logEvent(
  jobId: string,
  level: "info" | "warning" | "error" | "success",
  message: string,
  metadata?: Record<string, unknown>,
) {
  try {
    await supabase.from("agent_logs").insert({
      job_id: jobId,
      level,
      message,
      metadata: metadata ?? {},
    });
  } catch (_e) {
    console.error(`Failed to write log for job ${jobId}:`, _e);
  }
}

// ── Slack alerts ──────────────────────────────────────────────────
async function sendSlackAlert(
  message: string,
  level: "error" | "warning" | "info" = "warning",
  jobId?: string,
  metadata?: Record<string, unknown>,
) {
  if (!SLACK_WEBHOOK_URL) return;
  const emoji = { error: "🔴", warning: "🟡", info: "🔵" }[level];
  const payload = {
    text: `${emoji} AMP Alert — ${level.toUpperCase()}`,
    blocks: [
      {
        type: "header",
        text: { type: "plain_text", text: `${emoji} AMP Alert: ${level.toUpperCase()}`, emoji: true },
      },
      {
        type: "section",
        fields: [
          { type: "mrkdwn", text: `*Message:*\n${message}` },
          { type: "mrkdwn", text: `*Job ID:*\n${jobId ?? "N/A"}` },
          { type: "mrkdwn", text: `*Time:*\n${new Date().toISOString()}` },
          { type: "mrkdwn", text: `*AI Provider:*\nHermes Agent Desktop` },
        ],
      },
    ],
  };
  if (metadata) {
    payload.blocks.push({
      type: "section",
      text: {
        type: "mrkdwn",
        text: "```json\n" + JSON.stringify(metadata, null, 2).slice(0, 2000) + "\n```",
      },
    });
  }
  try {
    await fetch(SLACK_WEBHOOK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  } catch (_e) {
    console.error("Slack alert failed:", _e);
  }
}

// ── Fetch credentials for a job ───────────────────────────────────
async function fetchCredentialsForJob(
  credentialIds: string[],
  jobId: string
): Promise<Array<{ service: string; config: Record<string, unknown>; secrets: Record<string, unknown> }>> {
  if (credentialIds.length === 0) return [];

  try {
    const { data, error } = await supabase
      .from("credentials")
      .select("service, config, secrets")
      .in("id", credentialIds)
      .eq("is_active", true);

    if (error) {
      console.error("Failed to fetch credentials:", error);
      return [];
    }

    await logEvent(jobId, "info", `Fetched ${data?.length || 0} credentials for job`, {
      credential_ids: credentialIds,
    });

    return (data || []).map((c: any) => ({
      service: c.service,
      config: c.config || {},
      secrets: c.secrets || {},
    }));
  } catch (e) {
    console.error("Credential fetch error:", e);
    return [];
  }
}

// ── Provider health check ────────────────────────────────────────
interface ProviderHealth {
  name: string;
  available: boolean;
  error?: string;
  latencyMs?: number;
}

async function checkProviderHealth(provider: string, apiKey: string | undefined, baseUrl: string): Promise<ProviderHealth> {
  if (!apiKey) {
    return { name: provider, available: false, error: "API key not configured" };
  }

  const start = Date.now();
  try {
    const res = await fetch(`${baseUrl}/models`, {
      method: "GET",
      headers: { Authorization: `Bearer ${apiKey}` },
    });
    const latencyMs = Date.now() - start;

    if (res.ok) {
      return { name: provider, available: true, latencyMs };
    } else if (res.status === 401) {
      return { name: provider, available: false, error: "Invalid API key (401)", latencyMs };
    } else {
      const errText = await res.text();
      return { name: provider, available: false, error: `HTTP ${res.status}: ${errText.slice(0, 200)}`, latencyMs };
    }
  } catch (e) {
    return { name: provider, available: false, error: `Network error: ${e instanceof Error ? e.message : String(e)}` };
  }
}

async function getAvailableProvider(): Promise<{ name: string; apiKey: string; baseUrl: string; model: string } | null> {
  // Hermes Agent Desktop is the only provider
  if (HERMES_AGENT_API_KEY) {
    const health = await checkProviderHealth("hermes_agent", HERMES_AGENT_API_KEY, HERMES_AGENT_BASE_URL);
    if (health.available) {
      return { name: "hermes_agent", apiKey: HERMES_AGENT_API_KEY, baseUrl: HERMES_AGENT_BASE_URL, model: HERMES_AGENT_MODEL };
    }
    console.warn(`Hermes Agent Desktop unavailable: ${health.error}`);
  }

  return null;
}

// ── Unified LLM API call ────────────────────────────────────────
interface LLMMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

interface LLMResponse {
  choices: Array<{
    message: {
      content: string;
      reasoning_details?: string;
    };
    finish_reason: string | null;
  }>;
  usage: {
    prompt_tokens: number;
    completion_tokens: number;
    total_tokens: number;
  };
}

async function callLLM(
  provider: { name: string; apiKey: string; baseUrl: string; model: string },
  systemPrompt: string,
  userPrompt: string,
  credentials: Array<{ service: string; config: Record<string, unknown>; secrets: Record<string, unknown> }> = []
): Promise<{ content: string; tokensIn: number; tokensOut: number; reasoning?: string; provider: string; model: string }> {
  const messages: LLMMessage[] = [
    { role: "system", content: systemPrompt },
  ];

  // If credentials are provided, include them as context
  if (credentials.length > 0) {
    const credContext = credentials.map((c) => {
      const safeConfig = { ...c.config };
      // Never include secrets in the prompt
      return `- ${c.service}: ${JSON.stringify(safeConfig)}`;
    }).join("\n");

    messages.push({
      role: "user",
      content: `Available credentials for this task:\n${credContext}\n\nNow execute the task:`,
    });
  }

  messages.push({ role: "user", content: userPrompt });

  const apiUrl = `${provider.baseUrl}/chat/completions`;
  const res = await fetch(apiUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${provider.apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: provider.model,
      messages,
      temperature: LLM_TEMPERATURE,
      max_tokens: LLM_MAX_TOKENS,
      top_p: 1.0,
      // Hermes Agent Desktop: reasoning split (if supported)
      ...(provider.name === "hermes_agent" ? { reasoning_split: true } : {}),
    }),
  });

  if (!res.ok) {
    const err = await res.text();
    throw new Error(`${provider.name} API error ${res.status}: ${err}`);
  }

  const data: LLMResponse = await res.json();
  const choice = data.choices[0];
  const content = choice?.message?.content ?? "";
  const reasoning = choice?.message?.reasoning_details ?? "";
  const usage = data.usage || { prompt_tokens: 0, completion_tokens: 0, total_tokens: 0 };

  return {
    content,
    tokensIn: usage.prompt_tokens,
    tokensOut: usage.completion_tokens,
    reasoning: reasoning || undefined,
    provider: provider.name,
    model: provider.model,
  };
}

// ── Calculate cost ────────────────────────────────────────────────
function calculateCost(provider: string, tokensIn: number, tokensOut: number): number {
  const rates = COST_RATES[provider] || COST_RATES.openai;
  const inputCost = (tokensIn / 1000) * rates.input;
  const outputCost = (tokensOut / 1000) * rates.output;
  return Number((inputCost + outputCost).toFixed(6));
}

// ── Build prompts ─────────────────────────────────────────────────
function buildSystemPrompt(skillSlug: string, clientSlug?: string): string {
  const base = SKILL_PROMPTS[skillSlug] ??
    `You are an expert marketing consultant. Think step-by-step before answering. Provide high-quality, actionable advice.`;

  let prompt = base;

  // Add response format instructions
  prompt += `\n\n## Response Format\n- Think step-by-step before answering\n- Use markdown formatting for readability\n- Be specific and actionable\n- When uncertain, state your reasoning clearly`;

  if (clientSlug) {
    prompt += `\n\nYou are working for client: ${clientSlug}. Adapt output to their business context.`;
  }

  return prompt;
}

function buildUserPrompt(skillSlug: string, payload: Record<string, unknown>): string {
  const parts = [`Task: ${skillSlug}`];

  for (const [key, value] of Object.entries(payload)) {
    // Skip internal/meta fields
    if (["temperature", "max_tokens", "model", "credential_ids", "prompt_override"].includes(key)) continue;
    if (typeof value === "string" && value.trim()) {
      parts.push(`${key}: ${value}`);
    } else if (Array.isArray(value) || (typeof value === "object" && value !== null)) {
      parts.push(`${key}: ${JSON.stringify(value)}`);
    }
  }

  // If prompt override is provided, use it
  const promptOverride = payload.prompt_override as string;
  if (promptOverride?.trim()) {
    parts.push(`\n\n## Custom Instructions\n${promptOverride}`);
  }

  return parts.join("\n\n");
}

// ── QA checks ─────────────────────────────────────────────────────
async function runQAChecks(job: Record<string, unknown>): Promise<{
  blocked: boolean;
  warnings: string[];
  binaryPassed: Record<string, boolean>;
  scored: Record<string, number>;
}> {
  const payload = (job.payload as Record<string, unknown>) ?? {};
  const content = String(payload.artifact_content ?? "");
  const checks = (payload.checks as Record<string, string[]>) ?? {};
  const result = { blocked: false, warnings: [] as string[], binaryPassed: {} as Record<string, boolean>, scored: {} as Record<string, number> };

  // Binary: legal risk
  if (checks.binary?.includes("legal_risk")) {
    const riskTerms = ["guarantee", "guaranteed", "100%", "miracle", "cure", "fda approved"];
    const found = riskTerms.filter((t) => content.toLowerCase().includes(t));
    if (found.length > 0) {
      result.blocked = true;
      result.binaryPassed.legal_risk = false;
      result.warnings.push(`Legal risk flagged: ${found.join(", ")}`);
    } else {
      result.binaryPassed.legal_risk = true;
    }
  }

  // Binary: plagiarism (proxy = content too short)
  if (checks.binary?.includes("plagiarism_flag")) {
    if (content.length < 200) {
      result.blocked = true;
      result.binaryPassed.plagiarism_flag = false;
      result.warnings.push("Content too short — possible low quality");
    } else {
      result.binaryPassed.plagiarism_flag = true;
    }
  }

  // Scored: grammar
  if (checks.scored?.includes("grammar_score")) {
    const score = Math.min(100, Math.max(0, 100 - Math.floor(content.length / 1000)));
    result.scored.grammar_score = score;
    if (score < 70) result.warnings.push(`Grammar score low: ${score}/100`);
  }

  return result;
}

// ── Enqueue QA check ──────────────────────────────────────────────
async function enqueueQACheck(parentJob: Record<string, unknown>, content: string) {
  const { data, error } = await supabase.from("jobs").insert({
    type: "qa_check",
    client_slug: parentJob.client_slug as string | null,
    skill_slug: "qa-check",
    payload: {
      parent_job_id: parentJob.id,
      artifact_type: "content",
      artifact_content: content.slice(0, 8000),
      checks: {
        binary: ["legal_risk", "plagiarism_flag"],
        scored: ["grammar_score", "tone_match", "brand_voice_score"],
      },
    },
    status: "pending",
    parent_job_id: parentJob.id as string,
  }).select().single();

  if (error) {
    console.error("Failed to enqueue QA:", error);
    return null;
  }
  return data;
}

// ── Retry wrapper with backoff ────────────────────────────────────
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3,
  baseDelayMs: number = 1000
): Promise<T> {
  let lastError: Error | undefined;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err instanceof Error ? err : new Error(String(err));
      if (attempt < maxRetries) {
        const delay = baseDelayMs * Math.pow(2, attempt);
        console.log(`Retry ${attempt + 1}/${maxRetries} after ${delay}ms: ${lastError.message}`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// ── Execute a single job ──────────────────────────────────────────
async function executeJob(job: Record<string, unknown>) {
  const jobId = job.id as string;
  const skillSlug = (job.skill_slug as string) || "";
  const clientSlug = (job.client_slug as string) || undefined;
  const payload = (job.payload as Record<string, unknown>) ?? {};
  const credentialIds = (payload.credential_ids as string[]) ?? [];

  console.log(`Executing job ${jobId}: ${skillSlug} / ${clientSlug ?? "agency"}`);

  // Get available AI provider
  const provider = await getAvailableProvider();
  if (!provider) {
    const errorMsg = "No AI provider available. Please configure HERMES_AGENT_API_KEY in Supabase secrets.";
    await supabase.from("jobs").update({
      status: "failed",
      result: { error: errorMsg, provider_status: "none_available" },
      completed_at: new Date().toISOString(),
    }).eq("id", jobId);
    await logEvent(jobId, "error", errorMsg, { provider_status: "none_available" });
    await sendSlackAlert(errorMsg, "error", jobId);
    throw new Error(errorMsg);
  }

  await logEvent(jobId, "info", `Executing job: ${skillSlug} via ${provider.name} (${provider.model})`, {
    client_slug: clientSlug,
    provider: provider.name,
    model: provider.model,
  });

  // Mark running
  await supabase.from("jobs").update({ status: "running", started_at: new Date().toISOString() }).eq("id", jobId);

  try {
    // Fetch credentials if specified
    const credentials = await fetchCredentialsForJob(credentialIds, jobId);

    // Build and call LLM with retry
    const systemPrompt = buildSystemPrompt(skillSlug, clientSlug);
    const userPrompt = buildUserPrompt(skillSlug, payload);

    const llmResult = await withRetry(
      () => callLLM(provider, systemPrompt, userPrompt, credentials),
      3,
      1000
    );

    // Calculate cost
    const costUsd = calculateCost(llmResult.provider, llmResult.tokensIn, llmResult.tokensOut);

    const result = {
      executed_at: new Date().toISOString(),
      job_type: job.type,
      skill_slug: skillSlug,
      client_slug: clientSlug,
      content: llmResult.content,
      reasoning: llmResult.reasoning,
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      model: llmResult.model,
      provider: llmResult.provider,
      cost_usd: costUsd,
      message: `Job executed for ${clientSlug ?? "agency"} via ${skillSlug} (${llmResult.provider})`,
    };

    // Update job
    await supabase.from("jobs").update({
      status: "completed",
      result,
      cost_usd: costUsd,
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      completed_at: new Date().toISOString(),
    }).eq("id", jobId);

    await logEvent(jobId, "success", `Job completed: ${result.message}`, {
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      cost_usd: costUsd,
      provider: llmResult.provider,
    });

    // QA gate for content skills
    if (CONTENT_SKILLS.has(skillSlug) && llmResult.content) {
      const qaJob = await enqueueQACheck(job, llmResult.content);
      if (qaJob) {
        await logEvent(jobId, "info", `QA check enqueued: ${qaJob.id}`, { qa_job_id: qaJob.id });
      }
    }

    return result;

  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    console.error(`Job ${jobId} failed:`, errorMsg);
    await supabase.from("jobs").update({
      status: "failed",
      result: { error: errorMsg, provider: provider.name },
      completed_at: new Date().toISOString(),
    }).eq("id", jobId);
    await logEvent(jobId, "error", `Job failed: ${errorMsg}`, { error: errorMsg, provider: provider.name });
    await sendSlackAlert(`Job ${jobId} failed: ${errorMsg}`, "error", jobId, { error: errorMsg, provider: provider.name });
    throw err;
  }
}

// ── Health check endpoint ─────────────────────────────────────────
async function handleHealthCheck(): Promise<Response> {
  const checks = await Promise.all([
    checkProviderHealth("hermes_agent", HERMES_AGENT_API_KEY, HERMES_AGENT_BASE_URL),
  ]);

  const available = checks.filter((c) => c.available);
  const status = available.length > 0 ? "healthy" : "unhealthy";

  return new Response(
    JSON.stringify({
      status,
      timestamp: new Date().toISOString(),
      providers: checks,
      active_provider: available[0]?.name || null,
    }),
    { headers: { "Content-Type": "application/json" } }
  );
}

// ── Main handler ──────────────────────────────────────────────────
Deno.serve(async (req) => {
  const url = new URL(req.url);
  const params = url.searchParams;

  // ── Endpoint modes ────────────────────────────────────────────
  // GET /                       → batch mode (default 5 jobs)
  // GET /?mode=single           → ONE job per call (cron-job.org default)
  // GET /?mode=batch&limit=N    → up to N jobs (default 5, max 10)
  // GET /?mode=single&skill=xyz → next pending job for a specific skill
  // GET /?mode=single&job_id=X  → run a specific job (admin UI triggered)
  // GET /health                 → health check
  // GET /stats                  → queue stats (no execution)

  if (url.pathname === "/health" || url.pathname === "/healthz") {
    return handleHealthCheck();
  }

  if (url.pathname === "/stats") {
    const { count: pending } = await supabase
      .from("jobs")
      .select("id", { count: "exact", head: true })
      .eq("status", "pending");
    const { count: running } = await supabase
      .from("jobs")
      .select("id", { count: "exact", head: true })
      .eq("status", "running");
    const { count: completed_today } = await supabase
      .from("jobs")
      .select("id", { count: "exact", head: true })
      .eq("status", "completed")
      .gte("completed_at", new Date(Date.now() - 86400000).toISOString());
    return new Response(JSON.stringify({
      pending: pending ?? 0,
      running: running ?? 0,
      completed_last_24h: completed_today ?? 0,
      timestamp: new Date().toISOString(),
    }), { headers: { "Content-Type": "application/json" } });
  }

  const mode = params.get("mode") ?? "single";
  const skillFilter = params.get("skill");
  const jobId = params.get("job_id");
  const limitParam = parseInt(params.get("limit") ?? "5", 10);
  // CRITICAL: in single mode, limit is ALWAYS 1 (safe under 8s timeout)
  const limit = mode === "single" ? 1 : Math.min(Math.max(limitParam, 1), 10);

  console.log(`=== AMP Edge Function: execute-jobs (mode=${mode}, limit=${limit}) ===`);
  const startTime = Date.now();

  try {
    let query = supabase
      .from("jobs")
      .select("*")
      .eq("status", "pending")
      .order("created_at", { ascending: true });

    if (jobId) {
      query = query.eq("id", jobId);
    } else if (skillFilter) {
      query = query.eq("skill_slug", skillFilter);
    }

    const { data: jobs, error } = await query.limit(limit);

    if (error) {
      throw new Error(`Failed to fetch jobs: ${error.message}`);
    }

    if (!jobs || jobs.length === 0) {
      return new Response(JSON.stringify({ status: "ok", processed: 0, message: "No pending jobs" }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    console.log(`Found ${jobs.length} pending jobs`);

    // Execute each job
    const results = [];
    for (const job of jobs) {
      try {
        if (job.type === "qa_check") {
          const qaResult = await runQAChecks(job);
          await supabase.from("jobs").update({
            status: "completed",
            result: qaResult,
            completed_at: new Date().toISOString(),
          }).eq("id", job.id as string);
          await logEvent(job.id as string, "success", `QA completed: blocked=${qaResult.blocked}`, qaResult);

          if (qaResult.blocked) {
            const parentId = (job.payload as Record<string, unknown>)?.parent_job_id as string;
            if (parentId) {
              await supabase.from("jobs").update({
                status: "blocked",
                result: { qa_result: qaResult, error: "QA binary check failed" },
              }).eq("id", parentId);
              await logEvent(parentId, "error", "QA binary check blocked deliverability", qaResult);
              await sendSlackAlert(`QA blocked deliverability for job ${parentId}`, "error", parentId, qaResult);
            }
          }
          results.push({ job_id: job.id, status: "qa_completed", blocked: qaResult.blocked });
        } else {
          const execResult = await executeJob(job);
          results.push({ job_id: job.id, status: "completed", skill: job.skill_slug });
        }
      } catch (_e) {
        results.push({ job_id: job.id, status: "failed", error: String(_e) });
      }
    }

    const elapsed = Date.now() - startTime;
    return new Response(
      JSON.stringify({
        status: "ok",
        mode,
        processed: jobs.length,
        requeued: jobsReEnqueued,
        results,
        elapsed_ms: elapsed,
        remaining_budget_ms: remainingBudgetMs(),
      }),
      { headers: { "Content-Type": "application/json" } },
    );

  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    console.error("Edge function failed:", errorMsg);
    await sendSlackAlert(`Edge function crashed: ${errorMsg}`, "error");
    return new Response(
      JSON.stringify({ status: "error", error: errorMsg }),
      { status: 500, headers: { "Content-Type": "application/json" } },
    );
  }
});
