/**
 * API Route: /api/execute-jobs
 * =============================
 * Lightweight job queue endpoint that runs on Vercel.
 * For heavy processing, delegates to local execution via Supabase job status.
 *
 * Methods:
 *   GET  — Check pending job count + health status
 *   POST — Mark jobs for local pickup (sets status = "queued_for_local")
 */

import { NextResponse } from "next/server";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY!;

const supabase = createClient(supabaseUrl, supabaseServiceKey);

// ── GET: Health check + pending count ──────────────────────────────
export async function GET() {
  try {
    const { count: pendingCount, error: countErr } = await supabase
      .from("jobs")
      .select("*", { count: "exact", head: true })
      .eq("status", "pending");

    const { count: queuedCount, error: queuedErr } = await supabase
      .from("jobs")
      .select("*", { count: "exact", head: true })
      .eq("status", "queued_for_local");

    if (countErr || queuedErr) {
      return NextResponse.json(
        { error: "Failed to query jobs", details: countErr?.message || queuedErr?.message },
        { status: 500 }
      );
    }

    return NextResponse.json({
      status: "ok",
      pending_jobs: pendingCount || 0,
      queued_for_local: queuedCount || 0,
      message: pendingCount && pendingCount > 0
        ? `${pendingCount} jobs waiting. Run local executor to process.`
        : "No pending jobs.",
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}

// ── POST: Queue jobs for local execution ───────────────────────────
export async function POST(request: Request) {
  try {
    const body = await request.json().catch(() => ({}));
    const limit = Math.min(body.limit || 5, 10); // Max 10 at a time

    // Fetch pending jobs
    const { data: jobs, error: fetchErr } = await supabase
      .from("jobs")
      .select("*")
      .eq("status", "pending")
      .order("created_at", { ascending: true })
      .limit(limit);

    if (fetchErr) {
      return NextResponse.json({ error: fetchErr.message }, { status: 500 });
    }

    if (!jobs || jobs.length === 0) {
      return NextResponse.json({ status: "ok", queued: 0, message: "No pending jobs" });
    }

    // Mark them as queued for local execution
    const jobIds = jobs.map((j: any) => j.id);
    const { error: updateErr } = await supabase
      .from("jobs")
      .update({ status: "queued_for_local", updated_at: new Date().toISOString() })
      .in("id", jobIds);

    if (updateErr) {
      return NextResponse.json({ error: updateErr.message }, { status: 500 });
    }

    return NextResponse.json({
      status: "ok",
      queued: jobs.length,
      job_ids: jobIds,
      jobs: jobs.map((j: any) => ({
        id: j.id,
        skill_slug: j.skill_slug,
        client_slug: j.client_slug,
        type: j.type,
      })),
      message: `${jobs.length} jobs queued for local execution. Run: node scripts/local-executor.js`,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
