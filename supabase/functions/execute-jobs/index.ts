/**
 * Supabase Edge Function: execute-jobs
 * ====================================
 * Hosted worker that polls Supabase for pending jobs, executes them via LLM API,
 * and writes results back. Replaces the local laptop poller.
 *
 * Trigger: HTTP (from pg_cron) or manual
 * Runtime: Deno (Supabase Edge Functions)
 */

import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const SUPABASE_URL = Deno.env.get("SUPABASE_URL")!;
const SUPABASE_SERVICE_ROLE_KEY = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;
const LLM_API_KEY = Deno.env.get("OPENAI_API_KEY") || Deno.env.get("MINIMAX_API_KEY")!;
const LLM_PROVIDER = Deno.env.get("DEFAULT_LLM_PROVIDER") || "openai";
const LLM_MODEL = Deno.env.get("DEFAULT_LLM_MODEL") || "kimi-latest";
const LLM_BASE_URL = Deno.env.get("LLM_BASE_URL") || "https://api.openai.com/v1";
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

// ── Skill prompts (mirrors poller.py) ─────────────────────────────
const SKILL_PROMPTS: Record<string, string> = {
  "content-strategist": "You are an expert content strategist for digital marketing agencies.",
  "on-page-optimizer": "You are an expert SEO on-page optimizer.",
  "technical-seo-auditor": "You are a senior technical SEO consultant.",
  "keyword-researcher": "You are an expert keyword researcher.",
  "competitor-intelligence": "You are a competitive intelligence analyst.",
  "aeo-geo-strategist": "You are an AI Engine Optimization specialist.",
  "link-building-outreach": "You are a link building and digital PR specialist.",
  "pseo-pipeline": "You are a programmatic SEO expert.",
  "content-brief-writer": "You are a content brief specialist.",
  "copywriter": "You are an expert conversion copywriter.",
  "social-media-manager": "You are a social media strategist.",
  "paid-ads-manager": "You are a performance marketing specialist.",
  "analytics-expert": "You are a marketing analytics expert.",
  "conversion-optimizer": "You are a CRO specialist.",
  "brand-voice-writer": "You are a brand voice specialist.",
  "email-marketing-specialist": "You are an email marketing expert.",
  "local-seo-manager": "You are a local SEO specialist.",
  "video-script-writer": "You are a video content strategist.",
  "reputation-manager": "You are a reputation management specialist.",
  "market-researcher": "You are a market research analyst.",
  "forecasting-revenue": "You are a revenue forecasting specialist.",
  "reporting-automation": "You are a reporting automation expert.",
  "playbook-creator": "You are a marketing operations specialist.",
  "off-page-optimizer": "You are an off-page SEO specialist.",
  "agentic-marketing-os": "You are the master orchestrator of an AI-native marketing agency.",
  "qa-check": "You are a QA gatekeeper. Run binary and scored checks.",
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
          { type: "mrkdwn", text: `*Worker:*\nSupabase Edge Function` },
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

// ── LLM execution ─────────────────────────────────────────────────
async function callLLM(systemPrompt: string, userPrompt: string): Promise<{
  content: string;
  tokensIn: number;
  tokensOut: number;
}> {
  // Use LLM_BASE_URL from env (defaults to OpenAI, set to https://api.moonshot.cn/v1 for Kimi)
  const apiUrl = `${LLM_BASE_URL}/chat/completions`;
  const res = await fetch(apiUrl, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${LLM_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: LLM_MODEL,
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
        temperature: 1.0,
        max_tokens: 4096,
      }),
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`LLM error ${res.status}: ${err}`);
    }
    const data = await res.json();
    const content = data.choices?.[0]?.message?.content ?? "";
    const tokensIn = data.usage?.prompt_tokens ?? 0;
    const tokensOut = data.usage?.completion_tokens ?? 0;
    return { content, tokensIn, tokensOut };
}

// ── Build prompts ─────────────────────────────────────────────────
function buildSystemPrompt(skillSlug: string, clientSlug?: string): string {
  const base = SKILL_PROMPTS[skillSlug] ??
    "You are an expert marketing consultant. Provide high-quality, actionable advice.";
  if (clientSlug) {
    return `${base}\n\nYou are working for client: ${clientSlug}. Adapt output to their business context.`;
  }
  return base;
}

function buildUserPrompt(skillSlug: string, payload: Record<string, unknown>): string {
  const parts = [`Task: ${skillSlug}`];
  for (const [key, value] of Object.entries(payload)) {
    if (["temperature", "max_tokens", "model"].includes(key)) continue;
    if (typeof value === "string" && value.trim()) {
      parts.push(`${key}: ${value}`);
    } else if (Array.isArray(value) || typeof value === "object") {
      parts.push(`${key}: ${JSON.stringify(value)}`);
    }
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

// ── Execute a single job ──────────────────────────────────────────
async function executeJob(job: Record<string, unknown>) {
  const jobId = job.id as string;
  const skillSlug = (job.skill_slug as string) || "";
  const clientSlug = (job.client_slug as string) || undefined;
  const payload = (job.payload as Record<string, unknown>) ?? {};

  console.log(`Executing job ${jobId}: ${skillSlug} / ${clientSlug ?? "agency"}`);
  await logEvent(jobId, "info", `Executing job: ${skillSlug}`, { client_slug: clientSlug });

  // Mark running
  await supabase.from("jobs").update({ status: "running", started_at: new Date().toISOString() }).eq("id", jobId);

  try {
    // Build and call LLM
    const systemPrompt = buildSystemPrompt(skillSlug, clientSlug);
    const userPrompt = buildUserPrompt(skillSlug, payload);
    const llmResult = await callLLM(systemPrompt, userPrompt);

    // Estimate cost (simplified)
    const costUsd = LLM_PROVIDER === "openai"
      ? (llmResult.tokensIn / 1000) * 0.005 + (llmResult.tokensOut / 1000) * 0.015
      : (llmResult.tokensIn / 1000) * 0.0015 + (llmResult.tokensOut / 1000) * 0.0015;

    const result = {
      executed_at: new Date().toISOString(),
      job_type: job.type,
      skill_slug: skillSlug,
      client_slug: clientSlug,
      content: llmResult.content,
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      model: LLM_MODEL,
      provider: LLM_PROVIDER,
      message: `Job executed for ${clientSlug ?? "agency"} via ${skillSlug}`,
    };

    // Update job
    await supabase.from("jobs").update({
      status: "completed",
      result,
      cost_usd: Number(costUsd.toFixed(6)),
      tokens_in: llmResult.tokensIn,
      tokens_out: llmResult.tokensOut,
      completed_at: new Date().toISOString(),
    }).eq("id", jobId);

    await logEvent(jobId, "success", `Job completed: ${result.message}`, result);

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
      result: { error: errorMsg },
      completed_at: new Date().toISOString(),
    }).eq("id", jobId);
    await logEvent(jobId, "error", `Job failed: ${errorMsg}`, { error: errorMsg });
    await sendSlackAlert(`Job ${jobId} failed: ${errorMsg}`, "error", jobId, { error: errorMsg });
    throw err;
  }
}

// ── Main handler ──────────────────────────────────────────────────
Deno.serve(async (_req) => {
  console.log("=== AMP Edge Function: execute-jobs ===");
  const startTime = Date.now();

  try {
    // Fetch pending jobs
    const { data: jobs, error } = await supabase
      .from("jobs")
      .select("*")
      .eq("status", "pending")
      .order("created_at", { ascending: true })
      .limit(5);

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
          // QA jobs are handled inline
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
      JSON.stringify({ status: "ok", processed: jobs.length, results, elapsed_ms: elapsed }),
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
