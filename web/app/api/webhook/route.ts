import { supabase } from "@/lib/supabase";
import { NextResponse } from "next/server";

export const dynamic = "force-dynamic";

/**
 * Webhook receiver — called by cron-job.org, external systems, or the admin UI.
 * Enqueues a job in Supabase. Kimi Work polls for pending jobs and executes them.
 */
export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { type, client_slug, skill_slug, payload = {}, secret } = body;

    // Optional: verify webhook secret
    const webhookSecret = process.env.WEBHOOK_SECRET;
    if (webhookSecret && secret !== webhookSecret) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    // Validate required fields
    if (!type) {
      return NextResponse.json({ error: "Missing 'type'" }, { status: 400 });
    }

    // Insert job into Supabase
    const { data, error } = await supabase
      .from("jobs")
      .insert({
        type,
        client_slug: client_slug || null,
        skill_slug: skill_slug || null,
        payload,
        status: "pending",
      })
      .select()
      .single();

    if (error) {
      console.error("Supabase insert error:", error);
      return NextResponse.json({ error: error.message }, { status: 500 });
    }

    return NextResponse.json({
      status: "queued",
      job_id: data.id,
      message: `Job ${data.id} queued for ${type}`,
    });
  } catch (err: any) {
    console.error("Webhook error:", err);
    return NextResponse.json({ error: err.message || "Invalid JSON" }, { status: 400 });
  }
}

export async function GET() {
  return NextResponse.json({ status: "ok", message: "Webhook endpoint active. POST to enqueue jobs." });
}
