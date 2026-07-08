import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

/**
 * POST /api/credentials/fetch-for-job
 * ===================================
 * Internal API for the edge function or authorized workers to fetch
 * credential secrets by ID. Requires a valid job context.
 *
 * Body: { credential_ids: string[], job_id: string }
 */
export async function POST(request: Request) {
  try {
    if (!supabase) {
      return NextResponse.json({ error: "Supabase not configured" }, { status: 503 });
    }

    const body = await request.json();
    const { credential_ids, job_id } = body;

    if (!Array.isArray(credential_ids) || credential_ids.length === 0) {
      return NextResponse.json({ error: "Missing or invalid credential_ids" }, { status: 400 });
    }

    // Verify the job exists and is in a valid state
    const { data: job, error: jobError } = await supabase
      .from("jobs")
      .select("id, status")
      .eq("id", job_id)
      .single();

    if (jobError || !job) {
      return NextResponse.json({ error: "Job not found" }, { status: 404 });
    }

    if (job.status !== "pending" && job.status !== "running") {
      return NextResponse.json({ error: "Job is not active" }, { status: 403 });
    }

    // Fetch credentials with secrets (service role bypasses RLS)
    const { data: credentials, error: credsError } = await supabase
      .from("credentials")
      .select("id, client_slug, service, label, config, secrets, is_active")
      .in("id", credential_ids)
      .eq("is_active", true);

    if (credsError) {
      return NextResponse.json({ error: credsError.message }, { status: 500 });
    }

    // Log access for audit
    await supabase.from("agent_logs").insert({
      job_id,
      level: "info",
      message: `Credentials fetched for job execution`,
      metadata: {
        credential_count: credentials?.length || 0,
        credential_ids,
      },
    });

    return NextResponse.json({
      credentials: credentials || [],
      count: credentials?.length || 0,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}
